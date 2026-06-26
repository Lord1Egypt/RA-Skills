#!/usr/bin/env python3
"""Fetch recent CS2 matches from Leetify for a given username."""
import argparse
import requests
from leetify_common import get_leetify_key, get_steam_id, LEETIFY_API_BASE

DEFAULT_LIMIT = 10


def parse_score(match, steam_id):
    """Parse team scores and determine player's team score vs enemy score."""
    team_scores = match.get("team_scores", [])
    stats = match.get("stats", [])

    player_team = None
    for s in stats:
        if s.get("steam64_id") == steam_id:
            player_team = s.get("initial_team_number")
            break

    if not team_scores or player_team is None:
        return "?", "?"

    my_score = "?"
    enemy_score = "?"
    for ts in team_scores:
        if ts.get("team_number") == player_team:
            my_score = ts.get("score", "?")
        else:
            enemy_score = ts.get("score", "?")

    return my_score, enemy_score


def parse_player_stats(match, steam_id):
    """Extract player kills/deaths from match stats."""
    for s in match.get("stats", []):
        if s.get("steam64_id") == steam_id:
            return s.get("total_kills", "?"), s.get("total_deaths", "?")
    return "?", "?"


def cmd_matches(username, limit):
    steam_id = get_steam_id(username)
    leetify_key = get_leetify_key()

    headers = {"Authorization": f"Bearer {leetify_key}"}
    url = f"{LEETIFY_API_BASE}/v3/profile/matches?steam64_id={steam_id}&limit={limit}"
    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        print(f"❌ Leetify error: {r.text}")
        exit(1)

    matches = r.json()
    if isinstance(matches, dict) and "matches" in matches:
        matches = matches["matches"]

    matches = matches[:limit]

    if not matches:
        print("No matches found.")
        return

    print(f"\n🎮 Recent Matches for {username} ({steam_id}):")
    print(f"{'Idx':<4} | {'Map':<15} | {'Score':<8} | {'K/D':<8} | {'Date':<20}")
    print("-" * 70)
    for i, m in enumerate(matches):
        map_name = m.get("map_name", "?")
        my_score, enemy_score = parse_score(m, steam_id)
        kills, deaths = parse_player_stats(m, steam_id)
        dt = m.get("finished_at", "?")
        if isinstance(dt, str) and len(dt) > 16:
            dt = dt[:16].replace("T", " ")
        print(f"{i:<4} | {map_name:<15} | {my_score}:{enemy_score:<5} | {kills}/{deaths:<5} | {dt:<20}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List recent CS2 matches via Leetify")
    parser.add_argument("username", help="Username mapped to Steam ID")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max matches (default {DEFAULT_LIMIT})")
    args = parser.parse_args()
    cmd_matches(args.username, args.limit)
