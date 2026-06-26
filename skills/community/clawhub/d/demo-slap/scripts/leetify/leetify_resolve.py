#!/usr/bin/env python3
"""Resolve a replay URL from Leetify by username + match index.

Prints the replay URL to stdout. Used by demo_slap_analyze.py.
"""
import sys
import argparse
import requests
from leetify_common import get_leetify_key, get_steam_id, LEETIFY_API_BASE


def resolve_replay_url(username, match_index):
    steam_id = get_steam_id(username)
    leetify_key = get_leetify_key()

    print(f"🔍 Fetching match #{match_index} from Leetify for {username} ({steam_id})...", file=sys.stderr)
    headers = {"Authorization": f"Bearer {leetify_key}"}
    url = f"{LEETIFY_API_BASE}/v3/profile/matches?steam64_id={steam_id}&limit={match_index + 1}"
    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        print(f"❌ Leetify error: {r.text}", file=sys.stderr)
        sys.exit(1)

    matches = r.json()
    if isinstance(matches, dict) and "matches" in matches:
        matches = matches["matches"]

    if not isinstance(matches, list) or len(matches) <= match_index:
        print(f"❌ Match index {match_index} out of range (found {len(matches)}).", file=sys.stderr)
        sys.exit(1)

    replay_url = matches[match_index].get("replay_url")

    # Fallback: fetch match details
    if not replay_url:
        match_id = matches[match_index].get("id")
        if match_id:
            detail = requests.get(
                f"{LEETIFY_API_BASE}/v3/matches/{match_id}",
                headers=headers, timeout=30,
            )
            if detail.status_code == 200:
                replay_url = detail.json().get("replay_url")

    if not replay_url:
        print("❌ Could not resolve replay URL.", file=sys.stderr)
        sys.exit(1)

    return replay_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resolve replay URL from Leetify")
    parser.add_argument("username", help="Username mapped to Steam ID")
    parser.add_argument("--match-index", type=int, default=0, help="Match index (0=latest)")
    args = parser.parse_args()

    url = resolve_replay_url(args.username, args.match_index)
    print(url)
