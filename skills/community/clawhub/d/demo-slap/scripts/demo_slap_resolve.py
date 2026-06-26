#!/usr/bin/env python3
"""Resolve match info from Demo-Slap match history by match index.

Prints a replay/demo URL if the API exposes one. Otherwise prints the analyze jobId
and exits non-zero with a clear explanation.
"""
import argparse
import sys

from demo_slap_common import api_demo_slap, get_demo_slap_key
from leetify.leetify_common import get_steam_id as get_leetify_steam_id


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


def resolve_replay_url(username=None, match_index=0):
    get_demo_slap_key()

    steam_id = None
    if username:
        try:
            steam_id = get_leetify_steam_id(username)
        except SystemExit:
            steam_id = None

    page_size = max(match_index + 1, 10)
    res = api_demo_slap("GET", "/public-api/matches", params={"page": 1, "pageSize": page_size})
    if not res["success"]:
        print(f"❌ Demo-Slap error: {res['data']}", file=sys.stderr)
        sys.exit(1)

    matches = (res["data"] or {}).get("data") or []
    if steam_id:
        matches = [m for m in matches if has_player(m, steam_id)]

    if len(matches) <= match_index:
        print(f"❌ Match index {match_index} out of range (found {len(matches)}).", file=sys.stderr)
        sys.exit(1)

    match = matches[match_index]
    replay_url = extract_demo_url(match)
    if replay_url:
        return replay_url

    job_id = match.get("jobId") or "?"
    print(
        f"❌ Demo-Slap /public-api/matches returned match jobId={job_id} but no replay/demo URL. "
        f"This endpoint can be used for match discovery, but not for replay URL resolution unless the API starts exposing a URL field.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resolve replay/demo URL from Demo-Slap matches")
    parser.add_argument("username", nargs="?", help="Optional username mapped to Steam ID for filtering")
    parser.add_argument("--match-index", type=int, default=0, help="Match index (0=latest)")
    args = parser.parse_args()

    url = resolve_replay_url(username=args.username, match_index=args.match_index)
    print(url)
