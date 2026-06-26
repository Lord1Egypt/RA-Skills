import sys
import requests
import json
import time

def get_player_stats(username):
    url = f"https://api.chess.com/pub/player/{username}/stats"
    headers = {'User-Agent': 'OpenClaw-Chess-Coach'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_recent_games(username, year, month):
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}"
    headers = {'User-Agent': 'OpenClaw-Chess-Coach'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing username"}))
        sys.exit(1)
    
    username = sys.argv[1]
    cmd = sys.argv[2] if len(sys.argv) > 2 else "stats"
    
    if cmd == "stats":
        stats = get_player_stats(username)
        print(json.dumps(stats, indent=2))
    elif cmd == "games":
        now = time.gmtime()
        games = get_recent_games(username, now.tm_year, now.tm_mon)
        print(json.dumps(games, indent=2))
