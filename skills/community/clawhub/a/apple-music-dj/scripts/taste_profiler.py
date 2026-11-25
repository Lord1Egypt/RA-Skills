#!/usr/bin/env python3
"""
taste_profiler.py — Builds a structured taste profile from Apple Music API data.

Pulls from: recently played, heavy rotation, library, ratings, recommendations,
and Apple Music Replay / Music Summaries when available.

Usage:
  python3 taste_profiler.py [options]

Options:
  --storefront SF       Storefront code (default: auto-detect via API)
  --output PATH         Write JSON to file (default: stdout)
  --cache PATH          Cache file path for reuse
  --max-age HOURS       Re-generate if cache is older than N hours (default: 168 = 7 days)
  --skip-replay         Skip Replay/Music Summaries endpoints
  --verbose             Print progress to stderr

Requires: APPLE_MUSIC_DEV_TOKEN and APPLE_MUSIC_USER_TOKEN env vars.
"""

import sys

# Python version guard (also checked in _common, but be explicit for entry points)
if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import json
import math
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from _common import (
    GENRE_ENERGY,
    HIGH_ENERGY,
    LOW_ENERGY,
    call_api,
    check_token_expiry,
    check_user_token_age,
    get_storefront,
    rating_signals_from,
    require_env_tokens,
    save_snapshot,
    write_private,
)

SCRIPT_DIR = Path(__file__).parent


def log(msg: str, verbose: bool = True):
    if verbose:
        print(f"  → {msg}", file=sys.stderr)


def load_cache(path: str, max_age_hours: int) -> dict | None:
    """Load cached profile if it exists and is fresh enough."""
    try:
        p = Path(path)
        if not p.exists():
            return None
        age_hours = (time.time() - p.stat().st_mtime) / 3600
        if age_hours > max_age_hours:
            return None
        with open(p) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_cache(profile: dict, path: str):
    """Write profile to cache file with restrictive permissions."""
    try:
        write_private(path, json.dumps(profile, indent=2))
    except OSError as e:
        print(f"WARN: Could not save cache: {e}", file=sys.stderr)


def detect_storefront() -> str:
    """Auto-detect user's storefront via API (with caching)."""
    return get_storefront()


# How much one track from each source counts toward the profile. What the user plays
# outweighs what sits in the library, and Apple's suggestions only nudge.
SOURCE_WEIGHTS = {
    "heavy_rotation": 3.0,
    "loved": 2.5,
    "recent": 2.0,
    "recently_added": 1.5,
    "library": 1.0,
    "recommendations": 0.25,
}


def tag_source(tracks: list[dict], source: str) -> list[dict]:
    """Shallow copies of tracks tagged with the source they came from (see SOURCE_WEIGHTS)."""
    return [{**t, "_source": source} for t in tracks]


def track_weight(track: dict) -> float:
    """A track's weight from its source tag; untagged tracks count like a library song."""
    return SOURCE_WEIGHTS.get(track.get("_source", "library"), SOURCE_WEIGHTS["library"])


def extract_genres(tracks: list[dict], station_genres: list[str] | None = None) -> list[dict]:
    """Extract the weighted genre distribution from track data.

    A track's weight is split across its genres, so a parent genre listed alongside a
    sub-genre ("Rock" with "Alternative") doesn't count the track twice. Each matched
    station adds one library-weight unit (a deliberately light nudge). `count` stays the
    raw number of tracks/stations naming the genre.
    """
    genre_counts: Counter = Counter()
    genre_weights: defaultdict[str, float] = defaultdict(float)
    for track in tracks:
        attrs = track.get("attributes", {})
        genres = [g for g in attrs.get("genreNames", []) if g.lower() != "music"]  # drop generic "Music"
        if not genres:
            continue
        share = track_weight(track) / len(genres)
        for genre in genres:
            genre_counts[genre] += 1
            genre_weights[genre] += share
    for genre in station_genres or []:
        genre_counts[genre] += 1
        genre_weights[genre] += SOURCE_WEIGHTS["library"]
    total = sum(genre_weights.values()) or 1
    ranked = sorted(genre_weights, key=lambda g: (-genre_weights[g], -genre_counts[g]))
    return [
        {"genre": g, "count": genre_counts[g], "weight": round(genre_weights[g] / total, 3)}
        for g in ranked[:20]
    ]


def extract_recent_additions(recent_data: dict | None) -> tuple[list[dict], list[str]]:
    """Split a recently-added response into (track-like items, artist names by frequency).

    Library playlists have no artist and are skipped; albums/songs carry
    artistName and genreNames, so they can be analysed like tracks.
    """
    items = [
        i for i in (recent_data or {}).get("data", [])
        if i.get("attributes", {}).get("artistName")
    ]
    counts = Counter(i["attributes"]["artistName"] for i in items)
    return items, [name for name, _ in counts.most_common()]


def extract_station_genres(stations_data: dict | None) -> list[str]:
    """Genres named in recently played station titles (e.g. "Alternative Radio").

    Apple's station resources carry no genre attribute, so this matches known
    genre names in the title; stations named after an artist or mood match nothing.
    """
    found = []
    for station in (stations_data or {}).get("data", []):
        title = station.get("attributes", {}).get("name", "").lower()
        # Longest names first so "Indie Pop" wins over "Pop"
        for genre in sorted(GENRE_ENERGY, key=len, reverse=True):
            if re.search(rf"(?<![a-z0-9]){re.escape(genre.lower())}(?![a-z0-9])", title):
                found.append(genre)
                break
    return found


def extract_artists(tracks: list[dict]) -> list[dict]:
    """Extract artist frequency from tracks; `play_weight` is the source-weighted share."""
    artist_data: dict[str, dict] = {}
    for track in tracks:
        attrs = track.get("attributes", {})
        name = attrs.get("artistName", "Unknown")
        if name not in artist_data:
            artist_data[name] = {"name": name, "count": 0, "weight": 0.0, "ids": set()}
        artist_data[name]["count"] += 1
        artist_data[name]["weight"] += track_weight(track)
        # Try to get catalog artist ID from relationships
        rels = track.get("relationships", {})
        artists_rel = rels.get("artists", {}).get("data", [])
        for a in artists_rel:
            artist_data[name]["ids"].add(a.get("id", ""))

    total = sum(a["weight"] for a in artist_data.values()) or 1
    result = []
    for a in sorted(artist_data.values(), key=lambda x: (-x["weight"], -x["count"])):
        ids = sorted(a["ids"] - {""})
        result.append({
            "name": a["name"],
            "id": ids[0] if ids else None,
            "play_weight": round(a["weight"] / total, 3),
            "count": a["count"],
        })
    return result[:30]


def extract_eras(tracks: list[dict]) -> list[dict]:
    """Extract the weighted decade distribution from release dates."""
    decade_counts: Counter = Counter()
    decade_weights: defaultdict[str, float] = defaultdict(float)
    for track in tracks:
        date_str = track.get("attributes", {}).get("releaseDate", "")
        if date_str and len(date_str) >= 4 and date_str[:4].isdecimal():  # skip malformed dates
            year = int(date_str[:4])
            decade = f"{(year // 10) * 10}s"
            decade_counts[decade] += 1
            decade_weights[decade] += track_weight(track)
    total = sum(decade_weights.values()) or 1
    ranked = sorted(decade_weights, key=lambda d: (-decade_weights[d], -decade_counts[d]))
    return [
        {"decade": d, "count": decade_counts[d], "weight": round(decade_weights[d] / total, 3)}
        for d in ranked[:10]
    ]


def infer_energy_profile(genres: list[dict]) -> str:
    """Infer overall energy from genre distribution."""
    high_score = sum(g["weight"] for g in genres if GENRE_ENERGY.get(g["genre"], 0.5) >= HIGH_ENERGY)
    low_score = sum(g["weight"] for g in genres if GENRE_ENERGY.get(g["genre"], 0.5) <= LOW_ENERGY)
    if high_score > low_score + 0.2:
        return "high-energy"
    elif low_score > high_score + 0.2:
        return "chill"
    return "balanced"


def artist_weights(tracks: list[dict]) -> defaultdict[str, float]:
    """Source-weighted listening per artist over all tracks (no top-N cutoff)."""
    weights: defaultdict[str, float] = defaultdict(float)
    for t in tracks:
        weights[t.get("attributes", {}).get("artistName", "")] += track_weight(t)
    return weights


def compute_variety_score(artists: list[dict], tracks: list[dict]) -> float:
    """How diverse is the listening? 0=one artist, 1=an even spread.

    Normalized Shannon entropy of the source-weighted artist distribution over all
    tracks (not just the top artists).
    """
    if not tracks:
        return 0.5
    weights = artist_weights(tracks)
    total = sum(weights.values())
    if len(weights) < 2 or total <= 0:
        return 0.0
    entropy = -sum((w / total) * math.log(w / total) for w in weights.values() if w > 0)
    return round(min(entropy / math.log(len(weights)), 1.0), 2)


def compute_mainstream_score(top_artists: list[dict], chart_data: dict | None,
                             tracks: list[dict] | None = None) -> float:
    """How mainstream is the taste? The share of weighted listening that goes to charting artists.

    With `tracks`, the share is taken over every artist's weight, so listening to artists
    past the top-30 cutoff still counts. Without, it sums the top artists' `play_weight`.
    """
    if not chart_data or not top_artists:
        return 0.5  # unknown
    chart_artist_names = set()
    for section in chart_data.get("results", {}).values():
        if isinstance(section, list):
            for chart in section:
                for item in chart.get("data", []):
                    name = item.get("attributes", {}).get("artistName", "")
                    if name:
                        chart_artist_names.add(name.lower())
    if not chart_artist_names:
        return 0.5
    if tracks:
        weights = artist_weights(tracks)
        total = sum(weights.values())
        if total <= 0:
            return 0.5
        on_charts = sum(w for name, w in weights.items() if name.lower() in chart_artist_names) / total
    else:
        on_charts = sum(a.get("play_weight", 0) for a in top_artists if a["name"].lower() in chart_artist_names)
    return round(min(on_charts, 1.0), 2)


def extract_ratings(ratings_data: dict | None) -> tuple[list[str], list[str]]:
    """Extract loved and disliked song IDs from ratings."""
    loved_ids: list[str] = []
    disliked_song_ids: list[str] = []
    if not ratings_data or "data" not in ratings_data:
        return loved_ids, disliked_song_ids
    for item in ratings_data.get("data", []):
        attrs = item.get("attributes", {})
        value = attrs.get("value", 0)
        rid = item.get("id", "")
        if value == 1 and rid:
            loved_ids.append(rid)
        elif value == -1 and rid:
            disliked_song_ids.append(rid)
    return loved_ids, disliked_song_ids


MAX_RATING_LOOKUPS = 25  # rated songs not already fetched cost one catalog lookup each; cap the calls


def build_rating_signals(ratings_data: dict | None, known_tracks: list[dict], storefront: str) -> tuple[dict, int]:
    """Per-song ratings with artist and genre like/dislike counts, and how many rated songs fed them.

    Ratings carry only a song ID and a value, so each song's artist and genres come from
    tracks already fetched for the profile, else from a catalog lookup (at most
    MAX_RATING_LOOKUPS, dislikes first since they steer hardest).
    """
    known: dict[str, dict] = {}
    for track in known_tracks:
        attrs = track.get("attributes", {})
        ids = [track.get("id")] + [c.get("id") for c in track.get("relationships", {}).get("catalog", {}).get("data", [])]
        for tid in filter(None, ids):
            known.setdefault(tid, attrs)
    items = [(i.get("attributes", {}).get("value"), i.get("id")) for i in (ratings_data or {}).get("data", [])]
    items = sorted(((v, rid) for v, rid in items if v in (1, -1) and rid), key=lambda item: item[0])
    rated, lookups = [], 0
    for value, rid in items:
        attrs = known.get(rid)
        if attrs is None and lookups < MAX_RATING_LOOKUPS:
            lookups += 1
            data = (call_api("song-detail", storefront, rid) or {}).get("data", [])
            attrs = data[0].get("attributes") if data else None
        if attrs and attrs.get("artistName"):
            rated.append((rid, value, attrs))
    return rating_signals_from(rated), len(rated)


def extract_replay_highlights(summary_data: dict | None, milestones_data: dict | None) -> dict:
    """Extract Replay / Music Summaries highlights."""
    highlights: dict[str, Any] = {
        "available": False,
        "top_artist_all_time": None,
        "total_minutes_latest_year": None,
        "genre_evolution": [],
    }
    if not summary_data or "data" not in summary_data:
        return highlights

    highlights["available"] = True
    summaries = summary_data.get("data", [])
    for s in summaries:
        attrs = s.get("attributes", {})
        year = attrs.get("year", "")
        # Extract top genre from summary
        top_genres_list = attrs.get("topGenres", [])
        top_genre = top_genres_list[0].get("name") if top_genres_list else None
        # Fall back to genreNames if topGenres not available
        if not top_genre:
            genre_names = attrs.get("genreNames", [])
            top_genre = genre_names[0] if genre_names else None
        top_artists = attrs.get("topArtists", [])
        if top_artists:
            highlights["top_artist_all_time"] = top_artists[0].get("name")
        listen_time = attrs.get("listenTimeInMinutes")
        if listen_time:
            highlights["total_minutes_latest_year"] = listen_time
        if year and top_genre:
            highlights["genre_evolution"].append({"year": str(year), "top_genre": top_genre})

    if milestones_data and "data" in milestones_data:
        for m in milestones_data["data"]:
            attrs = m.get("attributes", {})
            listen_time = attrs.get("listenTimeInMinutes")
            if listen_time and listen_time > (highlights.get("total_minutes_latest_year") or 0):
                highlights["total_minutes_latest_year"] = listen_time

    return highlights


def build_profile(args) -> dict:
    """Main profile builder. Fetches all data and assembles the taste DNA."""
    require_env_tokens()
    verbose = args.verbose

    # Check token expiry on startup
    token_status = check_token_expiry()
    if token_status and token_status["warning"]:
        print(token_status["message"], file=sys.stderr)
        if token_status["expired"]:
            sys.exit(1)
    user_token = check_user_token_age()
    if user_token and user_token["warning"]:
        print(user_token["message"], file=sys.stderr)

    print("🎧 Building your Taste DNA profile...", file=sys.stderr)

    # Detect storefront (with caching)
    log("Detecting storefront...", verbose)
    sf = get_storefront(args.storefront)
    log(f"Storefront: {sf}", verbose)

    # ── Fetch all data sources ────────────────────────────────────
    log("Fetching recently played tracks...", verbose)
    recent_tracks = call_api("recent-tracks") or []
    log(f"Got {len(recent_tracks)} recent tracks", verbose)

    log("Fetching heavy rotation...", verbose)
    heavy_rotation = call_api("heavy-rotation")
    hr_count = len((heavy_rotation or {}).get("data", []))
    log(f"Got {hr_count} heavy rotation items", verbose)

    log("Fetching library artists...", verbose)
    lib_artists = call_api("library-artists", "100")
    la_count = len((lib_artists or {}).get("data", []))
    log(f"Got {la_count} library artists", verbose)

    log("Fetching library songs (sample)...", verbose)
    lib_songs = call_api("library-songs", "100")
    ls_count = len((lib_songs or {}).get("data", []))
    log(f"Got {ls_count} library songs", verbose)

    log("Fetching ratings...", verbose)
    ratings = call_api("ratings", "songs")

    log("Fetching recommendations...", verbose)
    recs = call_api("recommendations")
    rec_count = len((recs or {}).get("data", []))
    log(f"Got {rec_count} recommendation groups", verbose)

    log("Fetching recently added...", verbose)
    recent_added = call_api("recently-added", "25")
    log("Fetching recent stations...", verbose)
    recent_stations = call_api("recent-stations")

    # Replay data
    replay_summary = None
    replay_milestones = None
    if not args.skip_replay:
        log("Fetching Replay / Music Summaries...", verbose)
        replay_summary = call_api("replay-summary")
        replay_milestones = call_api("replay-milestones")
        if replay_summary and "data" in replay_summary:
            log("Replay data available!", verbose)
        else:
            log("Replay data not available (may not be supported)", verbose)

    # Chart data for mainstream scoring
    log("Fetching charts for mainstream scoring...", verbose)
    chart_data = call_api("charts", sf)

    # ── Analyze ───────────────────────────────────────────────────
    log("Analyzing patterns...", verbose)

    loved, disliked_songs = extract_ratings(ratings)
    loved_set = set(loved)

    # Combine all available track data for analysis, each tagged with its source (SOURCE_WEIGHTS)
    all_tracks = tag_source(recent_tracks, "recent")
    added_items, recently_added_artists = extract_recent_additions(recent_added)
    all_tracks.extend(tag_source(added_items, "recently_added"))

    # Library songs; loved ones count as "loved" (ratings may use library or catalog IDs)
    library_song_ids = []
    if lib_songs and "data" in lib_songs:
        for song in lib_songs["data"]:
            # Prefer catalog ID from the include=catalog relationship
            catalog_rel = song.get("relationships", {}).get("catalog", {}).get("data", [])
            cat_id = catalog_rel[0].get("id") if catalog_rel else None
            sid = song.get("id", "")
            if cat_id or sid:
                library_song_ids.append(cat_id or sid)
            is_loved = bool(loved_set & {cat_id, sid})
            all_tracks.extend(tag_source([song], "loved" if is_loved else "library"))

    # Extract tracks from heavy rotation (albums/playlists contain nested tracks)
    if heavy_rotation and "data" in heavy_rotation:
        for item in heavy_rotation["data"]:
            rels = item.get("relationships", {})
            for rel_key in ("tracks", "songs"):
                rel_tracks = rels.get(rel_key, {}).get("data", [])
                all_tracks.extend(tag_source(rel_tracks, "heavy_rotation"))
            # If no nested tracks, use the item itself (it has artistName, genreNames, etc.)
            if not any(rels.get(k, {}).get("data") for k in ("tracks", "songs")):
                all_tracks.extend(tag_source([item], "heavy_rotation"))

    # Extract tracks from recommendation groups (Apple's suggestions, not the user's listening)
    if recs and "data" in recs:
        for group in recs["data"]:
            rels = group.get("relationships", {})
            for rel_key in ("contents", "recommendations"):
                for container in rels.get(rel_key, {}).get("data", []):
                    container_rels = container.get("relationships", {})
                    for track_key in ("tracks", "songs"):
                        rec_tracks = container_rels.get(track_key, {}).get("data", [])
                        all_tracks.extend(tag_source(rec_tracks, "recommendations"))

    station_genres = extract_station_genres(recent_stations)
    genres = extract_genres(all_tracks, station_genres)

    if not all_tracks:
        print("ERROR: No track data retrieved from API. Check your tokens and network.", file=sys.stderr)
        print("  Run: scripts/verify_setup.sh  to diagnose issues.", file=sys.stderr)
        sys.exit(1)
    artists = extract_artists(all_tracks)
    eras = extract_eras(all_tracks)
    energy = infer_energy_profile(genres)
    variety = compute_variety_score(artists, all_tracks)
    mainstream = compute_mainstream_score(artists, chart_data, all_tracks)
    log("Reading your ratings for artist and genre signals...", verbose)
    rating_signals, rated_resolved = build_rating_signals(ratings, all_tracks, sf)
    replay = extract_replay_highlights(replay_summary, replay_milestones)

    # Listening velocity — compare library size to recent diversity
    velocity = "moderate"
    if len(recent_tracks) > 0:
        recent_unique = len(set(
            t.get("attributes", {}).get("name", "") for t in recent_tracks
        ))
        if recent_unique > 40:
            velocity = "high"
        elif recent_unique < 15:
            velocity = "low"

    # ── Assemble profile ──────────────────────────────────────────
    profile = {
        "top_artists": artists[:20],
        "genre_distribution": genres,
        "era_distribution": eras,
        "energy_profile": energy,
        "variety_score": variety,
        "mainstream_score": mainstream,
        "listening_velocity": velocity,
        "loved_track_ids": loved,
        "disliked_song_ids": disliked_songs,
        "rating_signals": rating_signals,
        "library_song_ids": library_song_ids,
        "recently_added_artists": recently_added_artists[:10],
        "station_genres": sorted(set(station_genres)),
        "replay_highlights": replay,
        "data_summary": {
            "recent_tracks": len(recent_tracks),
            "library_artists": la_count,
            "library_songs": ls_count,
            "library_song_ids_extracted": len(library_song_ids),
            "heavy_rotation_items": hr_count,
            "recommendation_groups": rec_count,
            "recently_added_items": len(added_items),
            "recent_stations": len((recent_stations or {}).get("data", [])),
            "loved_count": len(loved),
            "disliked_count": len(disliked_songs),
            "rated_songs_resolved": rated_resolved,
        },
        "storefront": sf,
        "generated_at": datetime.now(UTC).isoformat(),
    }

    print("\n✅ Taste DNA profile complete.", file=sys.stderr)
    return profile


def main():
    parser = argparse.ArgumentParser(description="Build Apple Music taste profile")
    parser.add_argument("--storefront", default="auto", help="Storefront code (default: auto-detect)")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    parser.add_argument("--cache", default=None, help="Cache file path")
    parser.add_argument("--max-age", type=int, default=168, help="Max cache age in hours (default: 168)")
    parser.add_argument("--skip-replay", action="store_true", help="Skip Replay endpoints")
    parser.add_argument("--no-snapshot", action="store_true",
                        help="Don't save a dated taste snapshot (used by taste_drift.py)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output to stderr")
    args = parser.parse_args()

    # Check cache first
    if args.cache:
        cached = load_cache(args.cache, args.max_age)
        if cached:
            print("Using cached taste profile.", file=sys.stderr)
            output = json.dumps(cached, indent=2)
            if args.output:
                write_private(args.output, output)
            else:
                print(output)
            return

    # Build fresh profile
    profile = build_profile(args)
    output = json.dumps(profile, indent=2)

    # Save cache
    if args.cache:
        save_cache(profile, args.cache)
        print(f"Cached to {args.cache}", file=sys.stderr)

    # Dated snapshot for drift tracking (fresh builds only)
    if not args.no_snapshot:
        try:
            snap_path = save_snapshot(profile)
            print(f"Snapshot saved to {snap_path}", file=sys.stderr)
        except OSError as e:
            print(f"⚠️  Could not save snapshot: {e}", file=sys.stderr)

    # Output
    if args.output:
        write_private(args.output, output)
        print(f"Profile written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
