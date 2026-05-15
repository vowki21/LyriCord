import requests
import urllib.parse
import sys
import time
import re
import os

DISCORD_USER_TOKEN = "" # token here :3

def update_discord_status(text):
    if DISCORD_USER_TOKEN == '' or not DISCORD_USER_TOKEN:
        return
        
    url = "https://discord.com/api/v9/users/@me/settings"
    headers = {
        "authorization": DISCORD_USER_TOKEN,
        "content-type": "application/json"
    }
    
    payload = {
        "custom_status": {
            "text": text[:128]
        }
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload, timeout=3)
        if response.status_code not in (200, 204):
            print(f"[Discord API ERROR] Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[Script ERROR] Failed to update status: {e}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    print(f"{GREEN}{BOLD}LyriCord{RESET}")
    print(f"{CYAN}{BOLD}BASED ON https://github.com/newst4rt/Lyrify, EDITED BY: https://vowki.pics/{RESET}\n")
    print(f"{MAGENTA}--- Lyrics Search (Lrclib API) ---{RESET}\n")
    artist = input(f"{YELLOW}Enter Artist: {RESET}").strip()
    title = input(f"{YELLOW}Enter Track Title: {RESET}").strip()
    
    if not artist or not title:
        print(f"\n{RED}Artist and Title cannot be empty.{RESET}")
        return

    print(f"\n{GREEN}Fetching lyrics, please wait...{RESET}\n")
    
    url = f'https://lrclib.net/api/get?artist_name={urllib.parse.quote(artist)}&track_name={urllib.parse.quote(title)}'
    header = {"User-Agent": "Lyricord/vowki21"}
    
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            body = response.json()
            synced = body.get("syncedLyrics")
            plain = body.get("plainLyrics")
            
            if synced or plain:
                print(f"{MAGENTA}{BOLD}--- Lyrics: {artist} - {title} ---{RESET}\n")
            
            if synced:
                parsed = []
                for line in synced.split('\n'):
                    match = re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)', line)
                    if match:
                        mins = int(match.group(1))
                        secs = float(match.group(2))
                        text = match.group(3).strip()
                        parsed.append((mins * 60 + secs, text))
                
                if parsed:
                    print(f"{YELLOW}(Playing synchronized with track time...){RESET}\n")
                    start_t = time.time()
                    for ts, txt in parsed:
                        diff = ts - (time.time() - start_t)
                        if diff > 0:
                            time.sleep(diff)
                        print(f"{CYAN}{txt}{RESET}")
                        update_discord_status(txt)
                    update_discord_status("Used: https://github.com/vowki21/LyriCord")
                    time.sleep(5)
                    update_discord_status("")
                else:
                    for line in (plain or synced).split('\n'):
                        print(f"{CYAN}{line}{RESET}")
                        update_discord_status(line)
                        time.sleep(1.5)
                    update_discord_status("Used: https://github.com/vowki21/LyriCord")
                    time.sleep(5)
                    update_discord_status("")
            elif plain:
                print(f"{YELLOW}(Displaying line by line...){RESET}\n")
                for line in plain.split('\n'):
                    print(f"{CYAN}{line}{RESET}")
                    update_discord_status(line)
                    time.sleep(1.5)
            else:
                print(f"\n{RED}No lyrics found for this track.{RESET}")
        elif response.status_code == 404:
            print(f"\n{RED}Track not found in the database.{RESET}")
        else:
            print(f"\n{RED}API Error: {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"\n{RED}Connection error occurred: {e}{RESET}")
    except Exception as e:
        print(f"\n{RED}An unexpected error occurred: {e}{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        update_discord_status("Used: https://github.com/vowki21/LyriCord")
        time.sleep(5)
        update_discord_status("")
        sys.exit(0)
