#!/usr/bin/env python3
"""
feedback.py — Tell the DJ what you did (or didn't) like.

Rates songs in Apple Music (thumbs up / down) and updates your cached taste
profile, so later playlists skip what you disliked without a profile rebuild.
Songs can be given by ID, or by position in a playlist the DJ created
(positions come from ~/.apple-music-dj/playlist_history.json, 1-based).

Usage:
  python3 feedback.py dislike <song_id> [...]  [--profile PATH]
  python3 feedback.py dislike --playlist-name "Deep Cuts" --position 7 [9 ...] [--profile PATH]
  python3 feedback.py like    --position 3        (most recent playlist when no name given)
  python3 feedback.py clear   <song_id> [...]     (remove your rating)
  python3 feedback.py info    --position 3        (name/artist of a track, e.g. for "more like track 3")

These commands WRITE ratings to your Apple Music account (except `info`).

Requires: APPLE_MUSIC_DEV_TOKEN and APPLE_MUSIC_USER_TOKEN env vars.
"""

import sys

if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import json
from pathlib import Path

from _common import call_api, load_profile, require_env_tokens, set_song_rating, write_private
from playlist_history import load_history

RATING_VALUE = {"like": "1", "dislike": "-1"}


# ── Resolving positions ──────────────────────────────────────────

def resolve_positions(playlist_name: str | None, positions: list[int]) -> list[str]:
    """Song IDs at 1-based `positions` of a DJ-created playlist (newest match, or newest overall)."""
    history = load_history()
    if playlist_name:
        matches = [e for e in history if e.get("name", "").lower() == playlist_name.lower()]
        if not matches:
            raise ValueError(f"No playlist named '{playlist_name}' in the DJ's history.")
    else:
        matches = history
        if not matches:
            raise ValueError("No playlists in the DJ's history yet.")
    entry = matches[-1]
    ids = entry.get("track_ids", [])
    resolved = []
    for pos in positions:
        if not 1 <= pos <= len(ids):
            raise ValueError(f"Position {pos} is out of range — '{entry.get('name')}' has {len(ids)} tracks.")
        resolved.append(ids[pos - 1])
    return resolved


# ── Profile update ───────────────────────────────────────────────

def apply_to_profile(profile: dict, action: str, song_ids: list[str],
                     songs: dict[str, dict] | None = None) -> dict:
    """Move IDs between the profile's loved / disliked lists (returns the same dict).

    Also update ``rating_signals``, the per-song ratings behind the artist and genre counts
    that steer every playlist strategy. `songs` (song ID -> catalog attributes) supplies a
    song's artist and genres; `clear` needs none, and a re-rated song keeps what it had.
    """
    loved = list(profile.get("loved_track_ids", []))
    disliked = list(profile.get("disliked_song_ids", []))
    if action in ("dislike", "clear"):
        loved = [i for i in loved if i not in song_ids]
    if action in ("like", "clear"):
        disliked = [i for i in disliked if i not in song_ids]
    if action == "like":
        loved += song_ids
    elif action == "dislike":
        disliked += song_ids
    profile["loved_track_ids"] = list(dict.fromkeys(loved))
    profile["disliked_song_ids"] = list(dict.fromkeys(disliked))
    if songs or "rating_signals" in profile:
        value = int(RATING_VALUE.get(action, "0"))
        signals = profile.setdefault("rating_signals", {"songs": {}, "artists": {}, "genres": {}})
        for sid in dict.fromkeys(song_ids):
            set_song_rating(signals, sid, value, (songs or {}).get(sid))
    return profile


def save_profile(profile: dict, path: str) -> None:
    write_private(path, json.dumps(profile, indent=2))


# ── Commands ─────────────────────────────────────────────────────

def rate_songs(action: str, song_ids: list[str]) -> list[dict]:
    """Send ratings to Apple Music. A raw "" means success; None means the call failed."""
    results = []
    for sid in song_ids:
        if action == "clear":
            resp = call_api("unrate", sid, "--yes", raw=True)
        else:
            resp = call_api("rate", sid, RATING_VALUE[action], "--yes", raw=True)
        results.append({"id": sid, "ok": resp is not None})
    return results


def song_attributes(song_ids: list[str], storefront: str) -> dict[str, dict]:
    """Catalog attributes (artist, genres, ...) per song ID; songs the lookup can't find are left out."""
    found = {}
    for sid in song_ids:
        resp = call_api("song-detail", storefront, sid)
        data = resp.get("data", []) if isinstance(resp, dict) else []
        if data:
            found[sid] = data[0].get("attributes", {})
    return found


def run_rating(action: str, song_ids: list[str], profile_path: str | None, storefront: str = "us") -> dict:
    results = rate_songs(action, song_ids)
    ok_ids = [r["id"] for r in results if r["ok"]]
    profile_updated = False
    if profile_path and ok_ids:
        profile = load_profile(profile_path)
        songs = song_attributes(ok_ids, profile.get("storefront") or storefront)
        save_profile(apply_to_profile(profile, action, ok_ids, songs), profile_path)
        profile_updated = True
    return {"action": action, "results": results, "profile_updated": profile_updated}


def track_info(song_ids: list[str], storefront: str) -> list[dict]:
    """Name and artist for each song ID (via song-detail)."""
    info = []
    for sid in song_ids:
        data = (call_api("song-detail", storefront, sid) or {}).get("data", [])
        attrs = data[0].get("attributes", {}) if data else {}
        info.append({"id": sid, "name": attrs.get("name"), "artist": attrs.get("artistName")})
    return info


def main():
    parser = argparse.ArgumentParser(description="Rate songs and teach the DJ your taste")
    parser.add_argument("action", choices=["like", "dislike", "clear", "info"])
    parser.add_argument("song_ids", nargs="*", help="Song IDs")
    parser.add_argument("--playlist-name", default=None, help="DJ-created playlist to take positions from")
    parser.add_argument("--position", type=int, nargs="+", default=[], help="1-based track position(s)")
    parser.add_argument("--profile", default=None, help="Taste profile JSON to update")
    parser.add_argument("--storefront", default="us", help="Storefront for `info` (default: us)")
    parser.add_argument("--yes", action="store_true",
                        help="Actually send the rating (and update --profile). Without it, like/dislike/clear "
                             "only preview what they would change.")
    args = parser.parse_args()

    if args.playlist_name and not args.position:
        parser.error("--playlist-name needs --position")

    song_ids = list(args.song_ids)
    try:
        if args.position:
            song_ids += resolve_positions(args.playlist_name, args.position)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    if not song_ids:
        parser.error("give song IDs, or --position")

    if args.action == "info":
        require_env_tokens()
        print(json.dumps(track_info(song_ids, args.storefront), indent=2))
        return

    if args.profile and not Path(args.profile).exists():
        print(f"ERROR: Profile not found: {args.profile}", file=sys.stderr)
        sys.exit(1)

    if not args.yes:
        print(json.dumps({"action": args.action, "song_ids": song_ids, "applied": False,
                          "note": "Preview only: nothing was rated and no profile was changed. "
                                  "Re-run with --yes to apply."}, indent=2))
        return

    require_env_tokens()  # only the confirmed apply path calls the API
    result = run_rating(args.action, song_ids, args.profile, args.storefront)
    print(json.dumps(result, indent=2))
    failed = [r["id"] for r in result["results"] if not r["ok"]]
    if failed:
        print(f"❌ Couldn't rate: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)
    print(f"✅ {args.action.capitalize()}d {len(song_ids)} song(s)."
          if args.action != "clear" else f"✅ Cleared rating on {len(song_ids)} song(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
