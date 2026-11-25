#!/usr/bin/env python3
"""
strategy_engine.py — Playlist Strategy Engine.

Implements the 5 core playlist strategies from references/playlist-strategies.md
and orchestrates candidate sourcing, scoring, sequencing, and playlist creation.

Strategies:
  deep-cuts       Hidden gems from artists you love
  mood            Mood/Activity-matched playlist (requires --mood)
  trend           Trending tracks filtered through your taste
  constellation   Gradual discovery from familiar to frontier
  refresh         Refresh an existing playlist (requires --playlist-id)
  similar         Songs like an artist or song (requires --similar-to; `seed` still works as an alias)
  era             Throwback from one decade (--decade, default: your top era)
  blend           One playlist for two listeners (requires --profile-b)
  remix           An Apple Music playlist made to fit your taste (requires --playlist-url)

Usage:
  python3 strategy_engine.py --strategy deep-cuts --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy mood --mood workout --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy trend --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy constellation --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy refresh --playlist-id <id> --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy similar --similar-to "Radiohead" --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy era --decade 90s --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy blend --profile <a.json> --profile-b <b.json> --storefront <sf>
  python3 strategy_engine.py --strategy remix --playlist-url <link or pl.id> --profile <path> --storefront <sf>

Common options:
  --name NAME         Custom playlist name (auto-generated if omitted)
  --size N            Target track count (default: from config or 30)
  --minutes N         Target running time instead (overrides --size; lands within about a minute)
  --clean             Keep explicit songs out (prefers a clean version of the same song)
  --include-library   Allow songs already in your library (refresh, seed, era)
  --create            Actually create the playlist in Apple Music
  --favorite          With --create: also favorite every track (writes to your account)
  --output PATH       Write playlist JSON to file

Requires: APPLE_MUSIC_DEV_TOKEN and APPLE_MUSIC_USER_TOKEN env vars.
"""

import sys

# Python version guard
if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import json
import subprocess
import tempfile
from datetime import datetime, UTC
from pathlib import Path

from compatibility import profile_compatibility
from share_code import load_profile_arg, resolve_artist_ids
from _common import (
    call_api,
    run_script,
    genre_proximity,  # noqa: F401  (kept importable from here)
    get_storefront,
    load_config,
    load_profile,
    rating_summary,
    require_env_tokens,
    user_filters,
    write_private,
)
from strategies.blend import strategy_blend
from strategies.candidates import USER_FILTERS, _cap_per_artist, _enforce_share, _finish, share_within
from strategies.constellation import strategy_constellation
from strategies.deep_cuts import _is_alt_version, _title_key, strategy_deep_cuts
from strategies.duration import MAX_MINUTES, fit_to_duration, pool_size_for, total_ms
from strategies.era import _release_decade, normalize_decade, strategy_era
from strategies.mood import MOOD_ENERGY, MOOD_MAP, strategy_mood
from strategies.refresh import strategy_refresh
from strategies.remix import LAST_REMIX, strategy_remix
from strategies.scoring import ARTIST_CAP, BLEND_MAX_SHARE, MIN_ENERGY_FIT, TREND_WILDCARDS
from strategies.seed import _resolve_seed, strategy_seed
from strategies.sequencing import ALBUM_CAP, ARCS, sequence_tracks
from strategies.trend import strategy_trend

# Moved to scripts/strategies/ but still importable from here (callers and tests use these names)
__all__ = [
    "ALBUM_CAP", "ARCS", "ARTIST_CAP", "BLEND_MAX_SHARE", "MIN_ENERGY_FIT", "MOOD_ENERGY", "TREND_WILDCARDS",
    "_cap_per_artist", "_enforce_share", "_finish", "_is_alt_version", "_release_decade", "_resolve_seed",
    "_title_key", "sequence_tracks",
]


# ── Playlist Creation ────────────────────────────────────────────

def generate_name(strategy: str, mood: str | None = None,
                  profile: dict | None = None, seed: str | None = None,
                  decade: str | None = None) -> str:
    """Auto-generate a playlist name."""
    date_str = datetime.now(UTC).strftime("%b %Y")
    if strategy == "deep-cuts":
        artists = profile.get("top_artists", [])[:2] if profile else []
        artist_str = " & ".join(a["name"] for a in artists) if artists else "Your Favorites"
        return f"Deep Cuts · {artist_str} · {date_str}"
    elif strategy == "mood":
        mood_label = (mood or "vibes").capitalize()
        return f"{mood_label} Mix · {date_str}"
    elif strategy == "trend":
        genres = profile.get("genre_distribution", [])[:2] if profile else []
        genre_str = " & ".join(g["genre"] for g in genres) if genres else "All Genres"
        return f"Trending For You · {genre_str} · {date_str}"
    elif strategy == "constellation":
        return f"New Horizons · {date_str}"
    elif strategy == "refresh":
        return f"Refreshed · {date_str}"
    elif strategy in ("similar", "seed"):
        return f"Like {seed or 'Your Favorites'} · {date_str}"
    elif strategy == "blend":
        return f"Blend · {date_str}"
    elif strategy == "remix":
        return f"Remix: {seed} · {date_str}" if seed else f"Remix · {date_str}"
    elif strategy == "era":
        return f"{decade} Throwback · {date_str}" if decade else f"Throwback · {date_str}"
    return f"Apple Music DJ · {date_str}"


def generate_description(strategy: str, mood: str | None = None,
                         track_count: int = 0) -> str:
    """Auto-generate a playlist description."""
    descriptions = {
        "deep-cuts": "Tracks you probably haven't heard from the artists you love. "
                     "No singles, no greatest hits — just the good stuff.",
        "mood": MOOD_MAP.get(mood or "", {}).get("description",
                "Tracks matched to your mood, filtered through your taste."),
        "trend": "What's trending right now, filtered through your taste. "
                 "A few wildcards in there too.",
        "constellation": "Starting from the artists you love, this playlist gradually "
                         "pulls you into new territory. The best discoveries are toward the end.",
        "refresh": "Fresh additions to keep your playlist evolving.",
        "similar": "Songs in the same orbit as your starting point, "
                   "weighted toward what you already like.",
        "blend": "One playlist for two listeners: the artists you share, plus each "
                 "other's favorites that fit both tastes.",
        "remix": "An Apple Music playlist remixed for you: what fits your taste stays, "
                 "the rest is swapped for closer matches.",
        "era": "A trip back to one decade, built from the artists and genres you play most.",
    }
    desc = descriptions.get(strategy, "Curated by Apple Music DJ.")
    return f"{desc} {track_count} tracks."


def check_playlist_exists(name: str) -> str | None:
    """Check if a playlist with this name already exists. Returns playlist ID or None."""
    try:
        result = run_script("apple_music_api.sh", "library-playlists", "100")
        if result.returncode != 0:
            detail = (result.stderr or "").strip().splitlines()
            print(f"WARN: Couldn't check for an existing playlist named '{name}': the API call exited "
                  f"{result.returncode}" + (f" ({detail[-1]})" if detail else "") + ".", file=sys.stderr)
        elif result.stdout.strip():
            data = json.loads(result.stdout)
            for pl in data.get("data", []):
                if pl.get("attributes", {}).get("name") == name:
                    return pl.get("id")
    except Exception as e:
        print(f"WARN: Couldn't check for an existing playlist named '{name}': {e}", file=sys.stderr)
    return None


def create_playlist_from_tracks(tracks: list[dict], name: str,
                                description: str) -> bool:
    """Create a playlist in Apple Music using build_playlist.sh."""
    if not tracks:
        print("ERROR: No tracks to create playlist from.", file=sys.stderr)
        return False

    # Check for existing playlist with same name
    existing_id = check_playlist_exists(name)
    if existing_id:
        print(f"⚠️  A playlist named '{name}' already exists (ID: {existing_id}).", file=sys.stderr)
        print("   Skipping creation. Use --strategy refresh to update it.", file=sys.stderr)
        return False

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for t in tracks:
            f.write(t["id"] + "\n")
        ids_file = f.name

    try:
        result = run_script("build_playlist.sh", "create", name, description, ids_file, "--yes", timeout=60)
        if result.returncode != 0:
            print(f"ERROR: Playlist creation failed: {result.stderr}", file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("ERROR: Playlist creation timed out.", file=sys.stderr)
        return False
    finally:
        Path(ids_file).unlink(missing_ok=True)


FAVORITE_BATCH_SIZE = 25


def favorite_tracks(tracks: list[dict]) -> dict:
    """Add tracks to the user's Apple Music favorites. This WRITES to the account."""
    ids = [t["id"] for t in tracks if t.get("id")]
    done, failed = 0, 0
    for i in range(0, len(ids), FAVORITE_BATCH_SIZE):
        batch = ids[i:i + FAVORITE_BATCH_SIZE]
        # raw=True: success is an empty body, which call_api can't parse as JSON
        if call_api("favorite", "songs", ",".join(batch), "--yes", raw=True) is None:
            failed += len(batch)
        else:
            done += len(batch)
    return {"favorited": done, "failed": failed}


# ── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Apple Music DJ — Playlist Strategy Engine"
    )
    parser.add_argument("--strategy", required=True,
                        choices=["deep-cuts", "mood", "trend", "constellation", "refresh", "similar", "seed", "era", "blend", "remix"],
                        help="Playlist strategy to use")
    parser.add_argument("--profile", required=True, help="Path to taste profile JSON")
    parser.add_argument("--storefront", default=None, help="Storefront code")
    parser.add_argument("--mood", default=None,
                        help=f"Mood for mood strategy ({', '.join(MOOD_MAP)})")
    parser.add_argument("--playlist-id", default=None,
                        help="Playlist ID for refresh strategy")
    parser.add_argument("--playlist-url", default=None,
                        help="Apple Music playlist link (or pl.… ID) to remix, for the remix strategy")
    parser.add_argument("--profile-b", default=None,
                        help="Second listener's taste profile JSON, or a taste code (amdj1:...) they sent you (blend strategy)")
    parser.add_argument("--similar-to", dest="similar_to", default=None,
                        help="Artist or song to find similar music to (similar strategy)")
    parser.add_argument("--similar-type", dest="similar_type", default="auto", choices=["auto", "artist", "song"],
                        help="Whether --similar-to is an artist or a song (default: auto-detect)")
    # Deprecated 3.2.0 spellings, accepted but not advertised. They were renamed because a
    # security scanner took the old flag's example as a crypto seed phrase on the command line.
    parser.add_argument("--seed", dest="similar_to", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--seed-type", dest="similar_type", default="auto",
                        choices=["auto", "artist", "song"], help=argparse.SUPPRESS)
    parser.add_argument("--decade", default=None,
                        help="Decade for the era strategy, e.g. 90s (default: your top era)")
    parser.add_argument("--name", default=None, help="Custom playlist name")
    parser.add_argument("--size", type=int, default=None,
                        help="Target track count")
    parser.add_argument("--minutes", type=float, default=None,
                        help="Target running time instead of a track count (overrides --size); the playlist lands "
                             "within about a minute of it, keeping the strategy's order")
    parser.add_argument("--include-library", action="store_true",
                        help="Refresh: allow songs already in your library")
    parser.add_argument("--clean", action="store_true",
                        help="Keep explicit songs out (uses the clean version when one exists); same as clean_only in config.json")
    parser.add_argument("--create", action="store_true",
                        help="Create the playlist in Apple Music")
    parser.add_argument("--favorite", action="store_true",
                        help="With --create: also add the playlist's tracks to your Apple Music favorites")
    parser.add_argument("--output", default=None, help="Write playlist JSON to file")

    args = parser.parse_args()
    if args.strategy == "seed":  # deprecated alias from 3.2.0
        args.strategy = "similar"
    if args.favorite and not args.create:
        parser.error("--favorite only applies together with --create")
    if args.minutes is not None and not 0 < args.minutes <= MAX_MINUTES:
        parser.error(f"--minutes must be between 0 and {MAX_MINUTES}")

    require_env_tokens()
    profile = load_profile(args.profile)
    config = load_config()

    sf = get_storefront(args.storefront or config.get("default_storefront"))

    target_size = args.size or config.get("playlist_size", 30)
    if args.minutes:
        target_size = pool_size_for(args.minutes)  # a pool to trim down to the running time

    # excluded_artists / preferred_genres from config.json, and tracks the DJ used recently
    repeat_days = config.get("avoid_repeat_days", 30)
    recent_ids: set[str] = set()
    if isinstance(repeat_days, int) and repeat_days > 0:
        from playlist_history import get_recent_track_ids
        recent_ids = get_recent_track_ids(repeat_days)
    USER_FILTERS.clear()
    clean_only = True if args.clean else None  # None: follow config.json
    USER_FILTERS.update(user_filters(config, recent_ids, profile, clean_only=clean_only, storefront=sf,
                                     include_library=args.include_library))
    profile_b: dict | None = None  # the second listener, for a blend

    target_label = f"{args.minutes:g} min" if args.minutes else f"{target_size} tracks"
    print(f"🎧 Strategy: {args.strategy} | Target: {target_label}", file=sys.stderr)

    # Run the selected strategy
    if args.strategy == "deep-cuts":
        tracks = strategy_deep_cuts(profile, sf, target_size)
    elif args.strategy == "mood":
        if not args.mood:
            print(f"ERROR: --mood required. Options: {', '.join(MOOD_MAP)}", file=sys.stderr)
            sys.exit(1)
        tracks = strategy_mood(profile, sf, args.mood, target_size)
    elif args.strategy == "trend":
        tracks = strategy_trend(profile, sf, target_size)
    elif args.strategy == "constellation":
        tracks = strategy_constellation(profile, sf, target_size)
    elif args.strategy == "refresh":
        if not args.playlist_id:
            print("ERROR: --playlist-id required for refresh strategy.", file=sys.stderr)
            sys.exit(1)
        tracks = strategy_refresh(profile, sf, args.playlist_id, target_size, args.include_library)
    elif args.strategy == "similar":
        if not args.similar_to:
            print("ERROR: --similar-to required for the similar strategy.", file=sys.stderr)
            sys.exit(1)
        tracks = strategy_seed(profile, sf, args.similar_to, args.similar_type, target_size, args.include_library)
    elif args.strategy == "blend":
        if not args.profile_b:
            print("ERROR: --profile-b required for blend strategy.", file=sys.stderr)
            sys.exit(1)
        profile_b = load_profile_arg(args.profile_b)
        if profile_b.get("shared_code"):
            found = resolve_artist_ids(profile_b, sf)
            print(f"  Found {found} of their top artists in the catalog "
                  "(a taste code has no song IDs, so their loved tracks and dislikes aren't used).", file=sys.stderr)
        USER_FILTERS.update(user_filters(config, recent_ids, profile, profile_b, clean_only=clean_only,
                                         storefront=sf, include_library=args.include_library))  # both ratings
        tracks = strategy_blend(profile, profile_b, sf, target_size)
    elif args.strategy == "remix":
        if not args.playlist_url:
            print("ERROR: --playlist-url required for the remix strategy.", file=sys.stderr)
            sys.exit(1)
        tracks = strategy_remix(profile, sf, args.playlist_url, target_size, args.include_library)
    elif args.strategy == "era":
        try:
            eras = profile.get("era_distribution", [])
            args.decade = normalize_decade(args.decade) if args.decade else (eras[0]["decade"] if eras else "2020s")
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        tracks = strategy_era(profile, sf, args.decade, target_size, args.include_library)
    else:  # argparse already restricts this; the branch keeps the variable provably assigned
        print(f"ERROR: unknown strategy '{args.strategy}'.", file=sys.stderr)
        sys.exit(1)

    if not tracks:
        print("No tracks found for this strategy. Try refreshing your profile.", file=sys.stderr)
        sys.exit(1)

    if args.minutes:
        # A blend must stay balanced after trimming, not just before it
        keep_balanced = (lambda t: share_within(t, BLEND_MAX_SHARE)) if args.strategy == "blend" else None
        tracks = fit_to_duration(tracks, round(args.minutes * 60_000), allowed=keep_balanced)

    # Generate name & description
    name = args.name or generate_name(args.strategy, args.mood, profile,
                                      LAST_REMIX.get("name") if args.strategy == "remix" else args.similar_to,
                                      args.decade)
    description = generate_description(args.strategy, args.mood, len(tracks))

    result = {
        "strategy": args.strategy,
        "name": name,
        "description": description,
        "track_count": len(tracks),
        "tracks": tracks,
    }
    if args.minutes:
        result["target_minutes"] = args.minutes
        result["duration_minutes"] = round(total_ms(tracks) / 60_000, 1)
    if args.strategy == "remix":
        # counted from the final list, so they still add up after --minutes trims it
        kept = sum(1 for t in tracks if t.get("source") == "remix_keep")
        result["remix"] = {"playlist": LAST_REMIX.get("name", ""), "original_tracks": LAST_REMIX.get("original", 0),
                           "kept": kept, "swapped": len(tracks) - kept}
        print(f"🔀 You'd keep {result['remix']['kept']} of {result['remix']['original_tracks']} tracks from "
              f"'{result['remix']['playlist']}'; {result['remix']['swapped']} swapped for closer matches.",
              file=sys.stderr)
    steered = rating_summary(*(p.get("rating_signals") or {} for p in (profile, profile_b) if p))
    if steered["boosted_artists"] or steered["demoted_artists"]:
        result["steered_by_ratings"] = steered
    if args.strategy == "blend":
        compat = profile_compatibility(profile, profile_b)
        result["compatibility"] = {k: compat[k] for k in ("compatibility_pct", "verdict", "shared_artists")}

    print(f"\n✅ {len(tracks)} tracks selected"
          + (f", {result['duration_minutes']:g} min (target {args.minutes:g})" if args.minutes else "") + ".",
          file=sys.stderr)

    # Output
    output_json = json.dumps(result, indent=2)
    if args.output:
        write_private(args.output, output_json)
        print(f"Playlist JSON written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    # Optionally create in Apple Music
    if args.create:
        print("Creating playlist in Apple Music...", file=sys.stderr)
        if create_playlist_from_tracks(tracks, name, description):
            print(f"✅ Playlist '{name}' created!", file=sys.stderr)
            # Log to playlist history
            try:
                from playlist_history import log_playlist
                track_ids = [t["id"] for t in tracks if t.get("id")]
                log_playlist(name, args.strategy, track_ids)
                print("📝 Logged to playlist history.", file=sys.stderr)
            except Exception as e:
                print(f"⚠️  Could not log to history: {e}", file=sys.stderr)
            if args.favorite:
                fav = favorite_tracks(tracks)
                print(f"⭐ Favorited {fav['favorited']} track(s)"
                      + (f", {fav['failed']} failed" if fav["failed"] else "") + ".", file=sys.stderr)
        else:
            print("❌ Failed to create playlist.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
