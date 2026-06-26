#!/usr/bin/env python3
"""Fetch recent CS2 matches from Demo-Slap for the authenticated user.

If username is provided and mapped to a Steam ID, mark matches containing that player.
"""
import argparse
from datetime import datetime, timezone

from demo_slap_common import api_demo_slap, get_demo_slap_key
from leetify.leetify_common import get_steam_id as get_leetify_steam_id

DEFAULT_LIMIT = 10


def parse_dt(value):
    if not value:
        return "?"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(value)


def get_player_names(team):
    names = []
    for player in (team or {}).get("players", []):
        name = player.get("name") or player.get("steamId") or "?"
        names.append(name)
    return names


def has_player(match, steam_id):
    if not steam_id:
        return False
    for side in ("teamA", "teamB"):
        for player in (match.get(side) or {}).get("players", []):
            if str(player.get("steamId")) == str(steam_id):
                return True
    return False


def extract_demo_url(match):
    for key in ("demoUrl", "demoURL", "replayUrl", "replayURL", "url"):
        value = match.get(key)
        if value:
            return value
    return None


def cmd_matches(username=None, limit=DEFAULT_LIMIT, page=1):
    # fail fast with the same message style as the rest of the skill
    get_demo_slap_key()

    steam_id = None
    if username:
        try:
            steam_id = get_leetify_steam_id(username)
        except SystemExit:
            steam_id = None

    page_size = max(1, min(limit, 100))
    res = api_demo_slap("GET", "/public-api/matches", params={"page": page, "pageSize": page_size})
    if not res["success"]:
        print(f"❌ Demo-Slap error: {res['data']}")
        raise SystemExit(1)

    payload = res["data"] or {}
    matches = payload.get("data") or []
    if steam_id:
        matches = [m for m in matches if has_player(m, steam_id)]

    if not matches:
        if steam_id:
            print(f"No Demo-Slap matches found for {username}.")
        else:
            print("No Demo-Slap matches found.")
        return

    title = f"🎮 Recent Demo-Slap Matches"
    if username:
        suffix = f" for {username}"
        if steam_id:
            suffix += f" ({steam_id})"
        title += suffix
    print(title + ":")
    print(f"{'Idx':<4} | {'Map':<12} | {'Status':<18} | {'Date':<16} | {'Demo':<4} | Teams")
    print("-" * 110)

    for i, match in enumerate(matches[:limit]):
        map_name = match.get("map") or "?"
        status = match.get("status") or "?"
        dt = parse_dt(match.get("matchTime"))
        demo_flag = "yes" if extract_demo_url(match) else "no"
        team_a = ", ".join(get_player_names(match.get("teamA"))) or "?"
        team_b = ", ".join(get_player_names(match.get("teamB"))) or "?"
        print(f"{i:<4} | {map_name:<12} | {status:<18} | {dt:<16} | {demo_flag:<4} | {team_a} vs {team_b}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List recent CS2 matches via Demo-Slap")
    parser.add_argument("username", nargs="?", help="Optional username mapped to Steam ID for filtering")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max matches (default {DEFAULT_LIMIT})")
    parser.add_argument("--page", type=int, default=1, help="Page number (default 1)")
    args = parser.parse_args()
    cmd_matches(username=args.username, limit=args.limit, page=args.page)
