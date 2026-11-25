#!/usr/bin/env python3
"""
daily_pick.py — Daily Song Drop & "What Should I Listen To Right Now?"

Modes:
  daily     Select one track for today's daily song drop with rationale
  now       Context-aware instant recommendation (time of day, recent patterns)

Usage:
  python3 daily_pick.py daily <profile.json> <storefront>
  python3 daily_pick.py now <profile.json> <storefront>

Designed to be called by cron (daily mode) or on-demand (now mode).
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
import hashlib
import json
import random
from datetime import datetime, UTC
from pathlib import Path

from _common import (
    apply_user_filters,
    call_api,
    check_token_expiry,
    check_user_token_age,
    filter_generic_genres,
    load_config,
    load_profile,
    taste_affinity,
    user_filters,
)

from strategies.scoring import TASTE_WEIGHT

SCRIPT_DIR = Path(__file__).parent

# Scoring weights for one pick: taste and context outweigh chance
BASE_SCORE = 0.5
# TASTE_WEIGHT (x taste_affinity) is shared with the strategies: strategies/scoring.py
DEEP_CUT_BONUS = 0.2      # the interesting picks
TIME_OF_DAY_BONUS = 0.3   # a genre that suits the hour
JITTER = 0.15


# ── Seeded Random (deterministic per day) ────────────────────────

def daily_seed() -> int:
    """Generate a seed based on today's date so the pick is stable within a day."""
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    return int(hashlib.md5(today.encode()).hexdigest()[:8], 16)


# ── Time-of-Day Context ─────────────────────────────────────────

def get_time_context() -> dict:
    """Infer mood/energy from current time."""
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return {"period": "morning", "energy": "medium", "mood": "gentle, uplifting",
                "genres_boost": ["Indie Pop", "Folk", "Acoustic"]}
    elif 9 <= hour < 12:
        return {"period": "mid-morning", "energy": "medium-high", "mood": "focused, productive",
                "genres_boost": ["Alternative", "Indie", "Electronic"]}
    elif 12 <= hour < 14:
        return {"period": "midday", "energy": "medium", "mood": "relaxed, social",
                "genres_boost": ["Pop", "R&B/Soul", "Jazz"]}
    elif 14 <= hour < 17:
        return {"period": "afternoon", "energy": "medium-high", "mood": "steady, warm",
                "genres_boost": ["Rock", "Indie", "Hip-Hop/Rap"]}
    elif 17 <= hour < 20:
        return {"period": "evening", "energy": "high", "mood": "energized, unwinding",
                "genres_boost": ["Pop", "Dance", "Rock", "Hip-Hop/Rap"]}
    elif 20 <= hour < 23:
        return {"period": "night", "energy": "medium-low", "mood": "reflective, atmospheric",
                "genres_boost": ["Ambient", "Jazz", "Singer/Songwriter", "Electronic"]}
    else:
        return {"period": "late-night", "energy": "low", "mood": "calm, introspective",
                "genres_boost": ["Ambient", "Classical", "Lo-fi"]}


# ── Candidate Sourcing ───────────────────────────────────────────

def get_candidates(profile: dict, sf: str, context: dict | None = None) -> list[dict]:
    """Gather candidate tracks from multiple sources."""
    candidates = []
    top_artists = profile.get("top_artists", [])[:15]
    # Songs you own or disliked are never picked
    skip_ids = set(profile.get("library_song_ids", [])) | set(profile.get("disliked_song_ids", []))
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:5]]

    # Source 1: Deep cuts from top artists (tracks NOT in library)
    for i, artist in enumerate(top_artists[:5]):
        print(f"  Sourcing candidates from artist {i+1}/5...", file=sys.stderr)
        artist_id = artist.get("id")
        if not artist_id:
            continue
        albums = call_api("artist-albums", sf, artist_id)
        if not albums or "data" not in albums:
            continue
        for album in albums["data"][:3]:
            album_id = album.get("id", "")
            detail = call_api("album-tracks", sf, album_id)
            if not detail or "data" not in detail:
                continue
            for ad in detail["data"]:
                for track in ad.get("relationships", {}).get("tracks", {}).get("data", []):
                    tid = track.get("id", "")
                    if tid and tid not in skip_ids:
                        attrs = track.get("attributes", {})
                        candidates.append({
                            "id": tid,
                            "name": attrs.get("name", ""),
                            "artist": attrs.get("artistName", artist["name"]),
                            "album": album.get("attributes", {}).get("name", ""),
                            "genre": filter_generic_genres(attrs.get("genreNames", [])),
                            "explicit": attrs.get("contentRating") == "explicit",
                            "source": "deep_cut",
                            "reason": f"A deep cut from {artist['name']} you haven't heard yet.",
                        })

    # Source 2: Charts filtered by taste
    charts = call_api("charts", sf)
    if charts:
        for section in charts.get("results", {}).values():
            if isinstance(section, list):
                for chart in section:
                    for item in chart.get("data", [])[:10]:
                        attrs = item.get("attributes", {})
                        item_genres = filter_generic_genres(attrs.get("genreNames", []))
                        # Only include if genre overlaps with user taste
                        if any(g in user_genres for g in item_genres):
                            tid = item.get("id", "")
                            if tid and tid not in skip_ids:
                                candidates.append({
                                    "id": tid,
                                    "name": attrs.get("name", ""),
                                    "artist": attrs.get("artistName", ""),
                                    "genre": item_genres,
                                    "explicit": attrs.get("contentRating") == "explicit",
                                    "source": "trending",
                                    "reason": f"Trending right now and matches your {item_genres[0] if item_genres else 'music'} taste.",
                                })

    return candidates


def score_candidate(candidate: dict, profile: dict, context: dict | None = None, rng: random.Random | None = None) -> float:
    """Score a candidate track. Higher = better pick.

    BASE_SCORE + TASTE_WEIGHT x taste match + DEEP_CUT_BONUS + TIME_OF_DAY_BONUS + up to JITTER.
    """
    _rng = rng or random.Random()
    score = BASE_SCORE

    # How much you like the track's sound, weighted by how much you play each genre
    score += TASTE_WEIGHT * taste_affinity(candidate.get("genre", []), profile.get("genre_distribution", []))

    if candidate.get("source") == "deep_cut":
        score += DEEP_CUT_BONUS

    # Time-of-day genre boost
    if context:
        boosted = {g.lower() for g in context.get("genres_boost", [])}
        track_genres = {g.lower() for g in candidate.get("genre", [])}
        if boosted & track_genres:
            score += TIME_OF_DAY_BONUS

    # Add some randomness so picks vary
    score += _rng.random() * JITTER

    return score


# ── Daily Song Drop ──────────────────────────────────────────────

def get_token_renewal_reminder() -> str:
    """Return token renewal warnings for the daily song drop, if any."""
    warnings = []
    for status in (check_token_expiry(), check_user_token_age()):
        if status and status["warning"]:
            warnings.append(status["message"])
    return "\n".join(warnings)


def cmd_daily(profile: dict, sf: str) -> dict:
    """Pick one track for today's daily song drop."""
    rng = random.Random(daily_seed())

    # Score first so the user filters can boost preferred genres, then drop excluded artists
    candidates = get_candidates(profile, sf)
    for c in candidates:
        c["_score"] = score_candidate(c, profile, rng=rng)
    candidates = apply_user_filters(candidates, user_filters(load_config(), profile=profile, storefront=sf))
    if not candidates:
        return {"error": "No candidates found. Try refreshing your taste profile."}

    # Sort by score and pick from top tier (add deterministic variety)
    candidates.sort(key=lambda c: c["_score"], reverse=True)
    top_tier = candidates[:min(10, len(candidates))]
    pick = rng.choice(top_tier)

    # Clean up internal fields
    pick.pop("_score", None)

    message = f"🎧 Today's pick: *{pick['name']}* by {pick['artist']} — {pick.get('reason', '')}"
    reminder = get_token_renewal_reminder()
    if reminder:
        message = f"{message}\n\n{reminder}"

    return {
        "type": "daily_song_drop",
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "track": pick,
        "message": message,
    }


# ── What Should I Listen To Right Now ────────────────────────────

def cmd_now(profile: dict, sf: str) -> dict:
    """Context-aware instant recommendation."""
    context = get_time_context()

    # Score with time context first so the user filters can boost preferred genres
    rng = random.Random()  # fresh RNG for "now" mode
    candidates = get_candidates(profile, sf, context)
    for c in candidates:
        c["_score"] = score_candidate(c, profile, context, rng=rng)
    candidates = apply_user_filters(candidates, user_filters(load_config(), profile=profile, storefront=sf))
    if not candidates:
        return {"error": "No candidates found.", "context": context}

    candidates.sort(key=lambda c: c["_score"], reverse=True)
    pick = candidates[0]
    pick.pop("_score", None)

    # Also suggest an album if we can
    album_suggestion = None
    if pick.get("album"):
        album_suggestion = f"Or try the full album: {pick['album']}"

    return {
        "type": "instant_recommendation",
        "context": context,
        "track": pick,
        "album_suggestion": album_suggestion,
        "message": (
            f"It's {context['period']} — mood is {context['mood']}. "
            f"Try *{pick['name']}* by {pick['artist']}. {pick.get('reason', '')}"
        ),
    }


# ── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Daily Pick / Instant Recommendation")
    sub = parser.add_subparsers(dest="command", required=True)

    p_daily = sub.add_parser("daily", help="Daily song drop (one track)")
    p_daily.add_argument("profile", help="Path to taste profile JSON")
    p_daily.add_argument("storefront", help="Storefront code (e.g., us)")

    p_now = sub.add_parser("now", help="What should I listen to right now?")
    p_now.add_argument("profile", help="Path to taste profile JSON")
    p_now.add_argument("storefront", help="Storefront code (e.g., us)")

    args = parser.parse_args()
    profile = load_profile(args.profile)

    if args.command == "daily":
        result = cmd_daily(profile, args.storefront)
    elif args.command == "now":
        result = cmd_now(profile, args.storefront)
    else:  # argparse already restricts this; the branch keeps the variable provably assigned
        print(f"ERROR: unknown command '{args.command}'.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
