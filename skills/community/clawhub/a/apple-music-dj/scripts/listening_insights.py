#!/usr/bin/env python3
"""
listening_insights.py — Listening Timeline, Streaks, Milestones, Year in Review.

Subcommands:
  timeline     Show how taste evolved across Replay years
  streaks      Analyze listening consistency from recent data
  year-review  Deep year-in-review analysis (better than Apple Replay)

Usage:
  python3 listening_insights.py timeline <profile.json>
  python3 listening_insights.py streaks <profile.json>
  python3 listening_insights.py year-review <profile.json> [--year 2025]

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
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import call_api, load_profile

SCRIPT_DIR = Path(__file__).parent


# ── Listening Timeline ───────────────────────────────────────────

def cmd_timeline(profile: dict) -> dict:
    """Show taste evolution across Replay years."""
    replay = profile.get("replay_highlights", {})
    genres = profile.get("genre_distribution", [])
    artists = profile.get("top_artists", [])

    # Try to fetch multi-year Replay data
    years_data = []
    current_year = datetime.now().year
    for year in range(2019, current_year + 1):
        print(f"  Fetching {year}...", file=sys.stderr)
        summary = call_api("replay-summary", str(year))
        if summary and "data" in summary and summary["data"]:
            year_info: dict[str, Any] = {"year": year}
            for s in summary["data"]:
                attrs = s.get("attributes", {})
                year_info["listen_minutes"] = attrs.get("listenTimeInMinutes")
                top_artists = attrs.get("topArtists", [])
                if top_artists:
                    year_info["top_artist"] = top_artists[0].get("name")
                top_genres_raw = attrs.get("topGenres", [])
                if top_genres_raw:
                    year_info["top_genre"] = (
                        top_genres_raw[0].get("name")
                        if isinstance(top_genres_raw[0], dict)
                        else str(top_genres_raw[0])
                    )
                top_songs = attrs.get("topSongs", [])
                if top_songs:
                    song = top_songs[0]
                    name = song.get("name") or song.get("attributes", {}).get("name", "Unknown")
                    year_info["top_song"] = name

            if len(year_info) > 1:  # has more than just 'year'
                years_data.append(year_info)

    # Build narrative
    narrative = []
    for yd in years_data:
        parts = [f"**{yd['year']}**:"]
        if yd.get("top_artist"):
            parts.append(f"Top artist: {yd['top_artist']}.")
        if yd.get("top_genre"):
            parts.append(f"Genre: {yd['top_genre']}.")
        if yd.get("listen_minutes"):
            hours = yd["listen_minutes"] // 60
            parts.append(f"Listened {hours:,} hours.")
        if yd.get("top_song"):
            parts.append(f"Song of the year: {yd['top_song']}.")
        narrative.append(" ".join(parts))

    return {
        "timeline": years_data,
        "narrative": narrative,
        "current_top_genres": [g["genre"] for g in genres[:5]],
        "current_top_artists": [a["name"] for a in artists[:5]],
        "replay_available": replay.get("available", False),
        "years_covered": len(years_data),
    }


# ── Listening Streaks & Milestones ───────────────────────────────

def cmd_streaks(profile: dict) -> dict:
    """Analyze listening patterns and surface milestones."""
    summary = profile.get("data_summary", {})
    artists = profile.get("top_artists", [])
    genres = profile.get("genre_distribution", [])
    velocity = profile.get("listening_velocity", "moderate")

    # Fetch milestones from API
    milestones_data = call_api("replay-milestones")
    milestones = []
    if milestones_data and "data" in milestones_data:
        for m in milestones_data["data"]:
            attrs = m.get("attributes", {})
            milestones.append({
                "type": attrs.get("kind", "unknown"),
                "value": attrs.get("value"),
                "description": attrs.get("description", ""),
            })

    # Compute insights from profile data
    insights = []

    # Artist loyalty
    if artists:
        top = artists[0]
        if top.get("count", 0) > 10:
            insights.append({
                "type": "artist_loyalty",
                "label": f"Most loyal to: {top['name']}",
                "detail": f"Appears {top['count']} times across your recent data",
            })

    # Genre dominance
    if genres and genres[0]["weight"] > 0.4:
        insights.append({
            "type": "genre_dominance",
            "label": f"{genres[0]['genre']} accounts for {int(genres[0]['weight']*100)}% of your listening",
            "detail": "Strong genre preference — your playlists lean heavily here.",
        })

    # Discovery rate
    unique_artists = len(artists)
    total_tracks = summary.get("recent_tracks", 0) + summary.get("library_songs", 0)
    if total_tracks > 0:
        discovery_rate = unique_artists / total_tracks
        if discovery_rate > 0.5:
            insights.append({
                "type": "discovery_rate",
                "label": "High discovery rate",
                "detail": "You listen to a lot of different artists — always exploring.",
            })
        elif discovery_rate < 0.15:
            insights.append({
                "type": "discovery_rate",
                "label": "Deep listener",
                "detail": "You go deep with fewer artists rather than skimming many.",
            })

    # Library size
    lib_songs = summary.get("library_songs", 0)
    if lib_songs > 500:
        insights.append({
            "type": "library_size",
            "label": f"Library: {lib_songs}+ songs",
            "detail": "Substantial collection — you take your music seriously.",
        })

    # Loved count
    loved = summary.get("loved_count", 0)
    if loved > 50:
        insights.append({
            "type": "active_rater",
            "label": f"Active rater: {loved} loved tracks",
            "detail": "Rating songs gives us much stronger taste signals.",
        })

    return {
        "milestones": milestones,
        "insights": insights,
        "listening_velocity": velocity,
        "data_summary": summary,
    }


# ── Year in Review ───────────────────────────────────────────────

def year_review_caption(year: int, total_minutes: int | None, top_artist: str | None,
                        top_genre: str | None, from_profile: bool = False) -> str:
    """A ready-to-post caption for the year-in-review card; leaves out whatever is unknown.

    `from_profile` means artist and genre are today's taste, not that year's Replay, so the
    caption says "right now" rather than claiming them for the year.
    """
    parts = []
    if total_minutes:
        parts.append(f"{total_minutes // 60:,} hours of music")
    if top_artist:
        parts.append(f"#1 artist {top_artist}")
    if top_genre:
        parts.append(f"mostly {top_genre}")
    if from_profile and parts:
        return f"My Apple Music taste right now: {', '.join(parts)}. 🎧"
    body = ", ".join(parts) if parts else "a year of music"
    return f"My {year} on Apple Music: {body}. 🎧"


def cmd_year_review(profile: dict, year: int) -> dict:
    """Comprehensive year-in-review — deeper than Apple Replay."""
    # Fetch year-specific Replay data
    summary = call_api("replay-summary", str(year))
    milestones = call_api("replay-milestones", str(year))

    year_data = {}
    if summary and "data" in summary:
        for s in summary["data"]:
            attrs = s.get("attributes", {})
            year_data["listen_minutes"] = attrs.get("listenTimeInMinutes")
            year_data["top_artists"] = [
                a.get("name", "Unknown") for a in attrs.get("topArtists", [])[:10]
            ]
            year_data["top_songs"] = []
            for song in attrs.get("topSongs", [])[:10]:
                name = song.get("name") or song.get("attributes", {}).get("name", "Unknown")
                artist = song.get("artistName") or song.get("attributes", {}).get("artistName", "Unknown")
                year_data["top_songs"].append({"name": name, "artist": artist})
            year_data["top_albums"] = [
                a.get("name", "Unknown") for a in attrs.get("topAlbums", [])[:10]
            ]
            year_data["top_genres"] = []
            for g in attrs.get("topGenres", [])[:5]:
                if isinstance(g, dict):
                    year_data["top_genres"].append(g.get("name", str(g)))
                else:
                    year_data["top_genres"].append(str(g))

    # Analyze from current profile (enrichments beyond Replay)
    variety = profile.get("variety_score", 0.5)
    mainstream = profile.get("mainstream_score", 0.5)

    # Compute insights
    insights = []
    if year_data.get("listen_minutes"):
        hours = year_data["listen_minutes"] // 60
        days = round(hours / 24, 1)
        insights.append(f"You listened for {hours:,} hours ({days} full days) in {year}.")

    if year_data.get("top_artists"):
        insights.append(f"Your #1 artist was {year_data['top_artists'][0]}.")

    if variety > 0.7:
        insights.append("You were an adventurous listener — high variety across artists.")
    elif variety < 0.3:
        insights.append("You went deep, not wide — loyal to a tight set of artists.")

    if mainstream > 0.6:
        insights.append("You stayed close to the mainstream this year.")
    elif mainstream < 0.2:
        insights.append("You were firmly off the beaten path — very few chart artists.")

    # Compute "obscurity score"
    obscurity = int((1.0 - mainstream) * 100)

    # Milestone highlights
    milestone_list = []
    if milestones and "data" in milestones:
        for m in milestones["data"]:
            attrs = m.get("attributes", {})
            desc = attrs.get("description", "")
            if desc:
                milestone_list.append(desc)

    # Flat fields for `taste_card.py --mode year-review`. Without Replay, fall back to the
    # current profile for artist and genre — and say so, since they aren't that year's numbers.
    top_artist = (year_data.get("top_artists") or [None])[0]
    top_genre = (year_data.get("top_genres") or [None])[0]
    if not year_data:
        top_artist = (profile.get("top_artists") or [{}])[0].get("name")
        top_genre = (profile.get("genre_distribution") or [{}])[0].get("genre")
        # Short enough for the SVG card, which cuts insights at 50 characters.
        insights.insert(0, f"No {year} Replay; artist and genre are current.")
    total_minutes = year_data.get("listen_minutes")

    return {
        "year": year,
        "total_minutes": total_minutes,
        "top_artist": top_artist,
        "top_genre": top_genre,
        "top_songs": year_data.get("top_songs", []),
        "caption": year_review_caption(year, total_minutes, top_artist, top_genre,
                                       from_profile=not year_data),
        "replay_data": year_data,
        "insights": insights,
        "obscurity_score": obscurity,
        "variety_score": variety,
        "mainstream_score": mainstream,
        "milestones": milestone_list,
        "replay_available": bool(year_data),
    }


# ── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Listening Insights")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tl = sub.add_parser("timeline", help="Taste evolution timeline")
    p_tl.add_argument("profile", help="Path to taste profile JSON")

    p_st = sub.add_parser("streaks", help="Listening streaks & milestones")
    p_st.add_argument("profile", help="Path to taste profile JSON")

    p_yr = sub.add_parser("year-review", help="Comprehensive year in review")
    p_yr.add_argument("profile", help="Path to taste profile JSON")
    p_yr.add_argument("--year", type=int, default=datetime.now().year - 1,
                      help="Year to review (default: last year)")

    args = parser.parse_args()
    profile = load_profile(args.profile)

    if args.command == "timeline":
        result = cmd_timeline(profile)
    elif args.command == "streaks":
        result = cmd_streaks(profile)
    elif args.command == "year-review":
        current_year = datetime.now().year
        if not (2015 <= args.year <= current_year):
            print(f"ERROR: Year must be between 2015 and {current_year}", file=sys.stderr)
            sys.exit(1)
        result = cmd_year_review(profile, args.year)
    else:  # argparse already restricts this; the branch keeps the variable provably assigned
        print(f"ERROR: unknown command '{args.command}'.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
