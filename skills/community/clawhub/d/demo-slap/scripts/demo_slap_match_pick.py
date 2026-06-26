#!/usr/bin/env python3
"""Select a Demo-Slap match by index and print structured info for downstream use.

This is the proper fallback path when Leetify is unavailable: list matches from
Demo-Slap, pick one, then continue by jobId.
"""
import argparse
import json
import sys
from datetime import datetime, timezone

from demo_slap_common import api_demo_slap, get_demo_slap_key
from leetify.leetify_common import get_steam_id as get_leetify_steam_id


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat()
    except Exception:
        return value


def has_player(match, steam_id):
    if not steam_id:
        return False
    for side in ('teamA', 'teamB'):
        for player in (match.get(side) or {}).get('players', []):
            if str(player.get('steamId')) == str(steam_id):
                return True
    return False


def extract_demo_url(match):
    for key in ('demoUrl', 'demoURL', 'replayUrl', 'replayURL', 'url'):
        value = match.get(key)
        if value:
            return value
    return None


def pick_match(username=None, match_index=0):
    get_demo_slap_key()

    steam_id = None
    if username:
        try:
            steam_id = get_leetify_steam_id(username)
        except SystemExit:
            steam_id = None

    page_size = max(match_index + 1, 10)
    res = api_demo_slap('GET', '/public-api/matches', params={'page': 1, 'pageSize': page_size})
    if not res['success']:
        print(f"❌ Demo-Slap error: {res['data']}", file=sys.stderr)
        sys.exit(1)

    matches = (res['data'] or {}).get('data') or []
    if steam_id:
        matches = [m for m in matches if has_player(m, steam_id)]

    if len(matches) <= match_index:
        print(f"❌ Match index {match_index} out of range (found {len(matches)}).", file=sys.stderr)
        sys.exit(1)

    match = matches[match_index]
    result = {
        'jobId': match.get('jobId'),
        'status': match.get('status'),
        'source': match.get('source'),
        'map': match.get('map'),
        'matchTime': parse_dt(match.get('matchTime')),
        'hasVideos': match.get('hasVideos'),
        'demoUrl': extract_demo_url(match),
        'teamA': match.get('teamA'),
        'teamB': match.get('teamB'),
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pick a Demo-Slap match and print structured info')
    parser.add_argument('username', nargs='?', help='Optional username mapped to Steam ID for filtering')
    parser.add_argument('--match-index', type=int, default=0, help='Match index (0=latest)')
    args = parser.parse_args()

    result = pick_match(username=args.username, match_index=args.match_index)
    print(json.dumps(result, indent=2, ensure_ascii=False))
