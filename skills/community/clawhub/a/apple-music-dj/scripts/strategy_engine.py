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

Usage:
  python3 strategy_engine.py --strategy deep-cuts --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy mood --mood workout --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy trend --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy constellation --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy refresh --playlist-id <id> --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy similar --similar-to "Radiohead" --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy era --decade 90s --profile <path> --storefront <sf>
  python3 strategy_engine.py --strategy blend --profile <a.json> --profile-b <b.json> --storefront <sf>

Common options:
  --name NAME         Custom playlist name (auto-generated if omitted)
  --size N            Target track count (default: from config or 30)
  --include-library   Allow songs already in your library (refresh, seed, era)
  --create            Actually create the playlist in Apple Music
  --favorite          With --create: also favorite every track (writes to your account)
  --output PATH       Write playlist JSON to file

Requires: APPLE_MUSIC_DEV_TOKEN and APPLE_MUSIC_USER_TOKEN env vars.
"""

import sys

# Python version guard
if sys.version_info < (3, 10):
    sys.exit(
        f"ERROR: Python 3.10+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import json
import random
import re
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from compatibility import profile_compatibility
from share_code import load_profile_arg, resolve_artist_ids
from _common import (
    call_api,
    filter_generic_genres,
    get_album_tracks,
    get_storefront,
    load_config,
    load_profile,
    require_env_tokens,
    search_artist,
    track_energy,
    write_private,
)

SCRIPT_DIR = Path(__file__).parent


# ── Mood/Activity Mapping ────────────────────────────────────────

MOOD_MAP = {
    "workout": {
        "arc": "ascending",
        "energy": "high", "genres": ["Electronic", "Hip-Hop/Rap", "Pop", "Rock", "Dance"],
        "description": "High-energy tracks to keep you moving.",
    },
    "focus": {
        "arc": "descending",
        "energy": "low-med", "genres": ["Ambient", "Classical", "Electronic", "Jazz"],
        "description": "Steady, minimal tracks for deep focus.",
    },
    "chill": {
        "energy": "low", "genres": ["Folk", "Jazz", "Ambient", "Indie Pop", "Singer/Songwriter"],
        "description": "Warm, relaxed vibes for unwinding.",
    },
    "party": {
        "energy": "high", "genres": ["Pop", "Dance", "Hip-Hop/Rap", "Funk", "R&B/Soul"],
        "description": "Singalongs and crowd-pleasers.",
    },
    "drive": {
        "energy": "med-high", "genres": ["Rock", "Indie", "Alternative", "Pop"],
        "description": "Confident, road-trip anthems.",
    },
    "sleep": {
        "arc": "descending",
        "energy": "very-low", "genres": ["Ambient", "Classical", "New Age"],
        "description": "Progressively quieter and slower.",
    },
    "cooking": {
        "energy": "medium", "genres": ["Jazz", "R&B/Soul", "Bossa Nova", "Indie Pop"],
        "description": "Warm, soulful backdrop for the kitchen.",
    },
    "morning": {
        "energy": "medium", "genres": ["Indie Pop", "Folk", "Acoustic"],
        "description": "Gentle and uplifting to start your day.",
    },
    "sad": {
        "arc": "descending",
        "energy": "low", "genres": ["Singer/Songwriter", "Indie", "Classical", "Folk"],
        "description": "Emotional, raw tracks for reflective moments.",
    },
    "anger": {
        "arc": "ascending",
        "energy": "very-high", "genres": ["Metal", "Punk", "Rock"],
        "description": "Aggressive catharsis.",
    },
}


# ── Genre Adjacency (imported concept from compatibility.py) ─────

GENRE_ADJACENCY = {
    "rock_family": {"Rock", "Alternative", "Indie", "Punk", "Metal", "Grunge"},
    "electronic_family": {"Electronic", "Dance", "House", "Techno", "Ambient", "IDM"},
    "hiphop_family": {"Hip-Hop/Rap", "R&B/Soul", "Funk"},
    "folk_family": {"Folk", "Singer/Songwriter", "Country", "Americana", "Bluegrass"},
    "jazz_family": {"Jazz", "Blues", "Bossa Nova", "Soul"},
    "classical_family": {"Classical", "Soundtrack", "New Age"},
    "pop_family": {"Pop", "Synth Pop", "Indie Pop", "K-Pop", "J-Pop"},
}


def genre_proximity(genre_a: str, genre_b: str) -> float:
    """Score genre proximity: 1.0 exact, 0.5 same family, 0.0 different."""
    if genre_a.lower() == genre_b.lower():
        return 1.0
    for family in GENRE_ADJACENCY.values():
        lower = {g.lower() for g in family}
        if genre_a.lower() in lower and genre_b.lower() in lower:
            return 0.5
    return 0.0


def best_genre_match(track_genres: list[str], target_genres: list[str]) -> float:
    """Best proximity score between any track genre and any target genre."""
    best = 0.0
    for tg in track_genres:
        for target in target_genres:
            best = max(best, genre_proximity(tg, target))
    return best


# ── Sequencing ───────────────────────────────────────────────────

ARCS = ("wave", "ascending", "descending", "none")


def _arc_order(tracks: list[dict], arc: str) -> list[dict]:
    """Order tracks by energy according to the requested arc."""
    by_energy = sorted(tracks, key=lambda t: t["energy"])  # stable: ties keep input order
    if arc == "ascending":
        return by_energy
    if arc == "descending":
        return by_energy[::-1]

    # wave: medium opener -> build -> peak in the middle -> wind-down. Each slot gets
    # a target energy (opener 0.55, peak 1.0, closer 0.2 — deliberately asymmetric so
    # the opener isn't the quietest track), then tracks are handed out lowest-energy
    # first to the lowest-target slots.
    n = len(tracks)

    def target(i: int) -> float:
        x = i / (n - 1)
        return 0.55 + 0.9 * x if x <= 0.5 else 1.0 - 1.6 * (x - 0.5)

    targets = [target(i) for i in range(n)]
    slots = sorted(range(n), key=lambda i: targets[i])
    ordered: list[dict] = [{}] * n
    for slot, track in zip(slots, by_energy, strict=True):
        ordered[slot] = track
    return ordered


def sequence_tracks(tracks: list[dict], max_same_artist: int = 5, arc: str = "wave") -> list[dict]:
    """Reorder tracks to follow an energy arc and enforce spacing rules.

    Rules:
    - No artist repeat within max_same_artist tracks
    - Max 2 songs from same album
    - Energy arc (each track gets an ``energy`` value from its genres):
        wave        medium opener -> build -> peak in the middle -> wind-down
        ascending   lowest to highest energy (workouts)
        descending  highest to lowest energy (sleep, chill)
        none        keep the incoming order
    """
    if arc not in ARCS:
        raise ValueError(f"Unknown arc '{arc}'. Options: {', '.join(ARCS)}")
    if len(tracks) <= 3:
        return tracks

    # Enforce album cap: max 2 per album
    album_counts: Counter = Counter()
    filtered = []
    for t in tracks:
        album = t.get("album", "")
        if album and album_counts[album] >= 2:
            continue
        album_counts[album] += 1
        filtered.append(t)

    if arc != "none" and len(filtered) > 1:
        for t in filtered:
            t["energy"] = round(track_energy(t.get("genre", [])), 2)
        filtered = _arc_order(filtered, arc)

    # Greedy scheduling with artist spacing
    result = []
    remaining = list(filtered)
    recent_artists: list[str] = []

    while remaining:
        placed = False
        for i, track in enumerate(remaining):
            artist = track.get("artist", "")
            if artist not in recent_artists[-max_same_artist:]:
                result.append(remaining.pop(i))
                recent_artists.append(artist)
                placed = True
                break
        if not placed:
            # Can't satisfy spacing — just append next
            result.append(remaining.pop(0))
            recent_artists.append(result[-1].get("artist", ""))

    return result


# ── Strategy: Deep Cuts ──────────────────────────────────────────

def strategy_deep_cuts(profile: dict, sf: str, target_size: int = 30) -> list[dict]:
    """Hidden gems from artists the user already loves."""
    top_artists = profile.get("top_artists", [])[:15]
    library_ids = set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))
    candidates = []

    for i, artist in enumerate(top_artists):
        artist_id = artist.get("id")
        artist_name = artist.get("name", "")
        if not artist_id:
            continue
        print(f"  [{i+1}/{len(top_artists)}] Scanning {artist_name}...", file=sys.stderr)

        # Get top songs to identify hits to exclude
        top_data = call_api("artist-top", sf, artist_id)
        top_song_names = set()
        if top_data and "data" in top_data:
            for ad in top_data["data"]:
                views = ad.get("views", {})
                for ts in views.get("top-songs", {}).get("data", []):
                    name = ts.get("attributes", {}).get("name", "")
                    if name:
                        top_song_names.add(name.lower())

        # Fetch discography
        albums_data = call_api("artist-albums", sf, artist_id)
        if not albums_data or "data" not in albums_data:
            continue

        for album in albums_data["data"]:
            album_attrs = album.get("attributes", {})
            if album_attrs.get("isSingle", False):
                continue

            album_tracks = get_album_tracks(sf, album["id"])
            for track in album_tracks:
                tid = track.get("id", "")
                attrs = track.get("attributes", {})
                name = attrs.get("name", "")

                # Exclude: in library, disliked, top songs
                if tid in library_ids or tid in disliked:
                    continue
                if name.lower() in top_song_names:
                    continue

                track_num = attrs.get("trackNumber", 1)
                candidates.append({
                    "id": tid,
                    "name": name,
                    "artist": attrs.get("artistName", artist_name),
                    "album": album_attrs.get("name", ""),
                    "genre": filter_generic_genres(attrs.get("genreNames", [])),
                    "source": "deep_cut",
                    "reason": f"A deep cut from {artist_name} — album track you haven't heard.",
                    "_score": 0.5 + (track_num / 30),  # later tracks score slightly higher
                })

        if len(candidates) >= target_size * 3:
            break  # enough candidates

    # Score and sort
    rng = random.Random()
    for c in candidates:
        c["_score"] += rng.random() * 0.2

    candidates.sort(key=lambda c: c["_score"], reverse=True)
    selected = candidates[:target_size]

    # Clean up internal fields
    for c in selected:
        c.pop("_score", None)

    return sequence_tracks(selected)


# ── Strategy: Mood/Activity ──────────────────────────────────────

def strategy_mood(profile: dict, sf: str, mood: str, target_size: int = 30) -> list[dict]:
    """Mood/Activity-matched playlist filtered through user taste."""
    mood_config = MOOD_MAP.get(mood)
    if not mood_config:
        print(f"ERROR: Unknown mood '{mood}'. Available: {', '.join(MOOD_MAP)}", file=sys.stderr)
        sys.exit(1)

    target_genres = mood_config["genres"]
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:10]]
    library_ids = set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))

    # Cross-reference mood genres with user preferences
    personalized_genres = []
    for mg in target_genres:
        if mg in user_genres:
            personalized_genres.append(mg)
    # Add mood genres even if not in user taste (that's the point)
    for mg in target_genres:
        if mg not in personalized_genres:
            personalized_genres.append(mg)

    candidates = []

    # Source 1: Charts for mood-relevant genres
    print("  Fetching charts for mood-relevant genres...", file=sys.stderr)
    charts = call_api("charts", sf)
    if charts:
        for section in charts.get("results", {}).values():
            if isinstance(section, list):
                for chart in section:
                    for item in chart.get("data", []):
                        attrs = item.get("attributes", {})
                        item_genres = filter_generic_genres(attrs.get("genreNames", []))
                        tid = item.get("id", "")
                        if tid in library_ids or tid in disliked:
                            continue
                        match = best_genre_match(item_genres, personalized_genres)
                        if match > 0:
                            candidates.append({
                                "id": tid,
                                "name": attrs.get("name", ""),
                                "artist": attrs.get("artistName", ""),
                                "album": "",
                                "genre": item_genres,
                                "source": "trending",
                                "reason": f"Matches your {mood} vibe.",
                                "_score": match,
                            })

    # Source 2: Deep cuts from user's artists in mood-relevant genres
    top_artists = profile.get("top_artists", [])[:10]
    for artist in top_artists[:5]:
        artist_id = artist.get("id")
        if not artist_id:
            continue
        print(f"  Scanning {artist['name']} for {mood} tracks...", file=sys.stderr)
        albums_data = call_api("artist-albums", sf, artist_id)
        if not albums_data or "data" not in albums_data:
            continue
        for album in albums_data["data"][:3]:
            album_tracks = get_album_tracks(sf, album["id"])
            for track in album_tracks:
                tid = track.get("id", "")
                attrs = track.get("attributes", {})
                if tid in library_ids or tid in disliked:
                    continue
                item_genres = filter_generic_genres(attrs.get("genreNames", []))
                match = best_genre_match(item_genres, personalized_genres)
                if match > 0:
                    candidates.append({
                        "id": tid,
                        "name": attrs.get("name", ""),
                        "artist": attrs.get("artistName", artist["name"]),
                        "album": album.get("attributes", {}).get("name", ""),
                        "genre": item_genres,
                        "source": "deep_cut",
                        "reason": f"From {artist['name']} — fits your {mood} mood.",
                        "_score": match + 0.1,  # slight boost for familiar artists
                    })

    # Add randomness and sort
    rng = random.Random()
    for c in candidates:
        c["_score"] += rng.random() * 0.2

    candidates.sort(key=lambda c: c["_score"], reverse=True)
    selected = candidates[:target_size]
    for c in selected:
        c.pop("_score", None)

    return sequence_tracks(selected, arc=mood_config.get("arc", "wave"))


# ── Strategy: Trend Radar ────────────────────────────────────────

def strategy_trend(profile: dict, sf: str, target_size: int = 20) -> list[dict]:
    """Trending tracks filtered through user's taste, with wildcards."""
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:5]]
    user_artist_names = {a["name"].lower() for a in profile.get("top_artists", [])[:15]}
    library_ids = set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))

    candidates = []
    seen_ids = set()

    # Fetch overall charts
    print("  Fetching overall charts...", file=sys.stderr)
    charts = call_api("charts", sf)
    if charts:
        for section in charts.get("results", {}).values():
            if isinstance(section, list):
                for chart in section:
                    for rank, item in enumerate(chart.get("data", [])):
                        attrs = item.get("attributes", {})
                        tid = item.get("id", "")
                        if not tid or tid in library_ids or tid in disliked or tid in seen_ids:
                            continue
                        seen_ids.add(tid)
                        item_genres = filter_generic_genres(attrs.get("genreNames", []))
                        artist_name = attrs.get("artistName", "")

                        taste_match = best_genre_match(item_genres, user_genres)
                        if artist_name.lower() in user_artist_names:
                            taste_match = max(taste_match, 0.8)

                        rank_weight = 1.0 - (rank / 25) * 0.3  # top-ranked gets slight bonus
                        score = taste_match * rank_weight

                        candidates.append({
                            "id": tid,
                            "name": attrs.get("name", ""),
                            "artist": artist_name,
                            "album": "",
                            "genre": item_genres,
                            "source": "trending",
                            "reason": "Trending and matches your taste.",
                            "_score": score,
                            "_is_wildcard": taste_match == 0,
                        })

    # Separate wildcards (zero taste match) and matched
    matched = [c for c in candidates if not c.get("_is_wildcard")]
    wildcards = [c for c in candidates if c.get("_is_wildcard")]

    # Sort matched by score
    matched.sort(key=lambda c: c["_score"], reverse=True)

    # Pick main tracks + 2-3 wildcards
    wildcard_count = min(3, len(wildcards))
    main_count = target_size - wildcard_count
    selected = matched[:main_count]

    if wildcards:
        rng = random.Random()
        rng.shuffle(wildcards)
        selected.extend(wildcards[:wildcard_count])

    for c in selected:
        c.pop("_score", None)
        c.pop("_is_wildcard", None)
        if c in wildcards[:wildcard_count]:
            c["reason"] = "A wildcard pick — something outside your usual taste."

    return sequence_tracks(selected)


# ── Strategy: Constellation Discovery ────────────────────────────

def strategy_constellation(profile: dict, sf: str, target_size: int = 25) -> list[dict]:
    """Gradual discovery: familiar → expansion → frontier."""
    top_artists = profile.get("top_artists", [])[:5]
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:10]]
    library_ids = set(profile.get("library_song_ids", []))
    library_artists = {a["name"].lower() for a in profile.get("top_artists", [])}
    disliked = set(profile.get("disliked_song_ids", []))

    # Discover adjacent artists
    discovered = []
    visited_ids = set()

    for artist in top_artists:
        artist_name = artist.get("name", "")
        print(f"  Exploring from {artist_name}...", file=sys.stderr)

        # Search for adjacent artists using name + genre terms
        artist_obj = search_artist(sf, artist_name)
        if not artist_obj:
            continue
        artist_genres = [g for g in artist_obj.get("attributes", {}).get("genreNames", [])
                         if g.lower() != "music"]
        search_query = f"{artist_name} {' '.join(artist_genres[:2])}"

        results = call_api("search", sf, search_query, "artists")
        if not results:
            continue

        candidates = results.get("results", {}).get("artists", {}).get("data", [])
        for c in candidates:
            cid = c.get("id", "")
            cname = c.get("attributes", {}).get("name", "")
            if cid in visited_ids or cname.lower() in library_artists:
                continue
            visited_ids.add(cid)

            c_genres = [g for g in c.get("attributes", {}).get("genreNames", [])
                        if g.lower() != "music"]
            proximity = best_genre_match(c_genres, user_genres)

            # Classify zone
            if proximity >= 0.9:
                zone = "familiar"
            elif proximity >= 0.4:
                zone = "expansion"
            else:
                zone = "frontier"

            discovered.append({
                "artist_id": cid,
                "artist_name": cname,
                "genres": c_genres,
                "proximity": proximity,
                "zone": zone,
                "seed_artist": artist_name,
            })

    # Fetch top songs from discovered artists
    all_tracks = []
    for disc in discovered:
        top_data = call_api("artist-top", sf, disc["artist_id"])
        if not top_data or "data" not in top_data:
            continue
        for ad in top_data["data"]:
            views = ad.get("views", {})
            for ts in views.get("top-songs", {}).get("data", [])[:3]:
                tid = ts.get("id", "")
                if tid in library_ids or tid in disliked:
                    continue
                attrs = ts.get("attributes", {})
                all_tracks.append({
                    "id": tid,
                    "name": attrs.get("name", ""),
                    "artist": disc["artist_name"],
                    "album": "",
                    "genre": filter_generic_genres(attrs.get("genreNames", [])),
                    "source": "constellation",
                    "zone": disc["zone"],
                    "reason": f"Discovered via {disc['seed_artist']} — {disc['zone']} zone.",
                    "_proximity": disc["proximity"],
                })

    # Build gradient: familiar first, then expansion, then frontier
    familiar = [t for t in all_tracks if t.get("zone") == "familiar"]
    expansion = [t for t in all_tracks if t.get("zone") == "expansion"]
    frontier = [t for t in all_tracks if t.get("zone") == "frontier"]

    # Allocate proportionally to target:  ~30% familiar, ~45% expansion, ~25% frontier
    fam_count = max(1, int(target_size * 0.3))
    exp_count = max(1, int(target_size * 0.45))
    fro_count = target_size - fam_count - exp_count

    rng = random.Random()
    rng.shuffle(familiar)
    rng.shuffle(expansion)
    rng.shuffle(frontier)

    selected = familiar[:fam_count] + expansion[:exp_count] + frontier[:fro_count]

    # Clean internal fields
    for c in selected:
        c.pop("_proximity", None)

    # Don't re-sequence — the gradient order IS the sequence
    return selected


# ── Strategy: Refresh ────────────────────────────────────────────

def strategy_refresh(profile: dict, sf: str, playlist_id: str, target_add: int = 10,
                     include_library: bool = False) -> list[dict]:
    """Refresh an existing playlist with fresh matching tracks."""
    # Analyze the existing playlist's sonic signature
    tracks_data = call_api("playlist-tracks", playlist_id)
    if not tracks_data or "data" not in tracks_data:
        print("ERROR: Could not fetch playlist tracks.", file=sys.stderr)
        return []

    existing_tracks = tracks_data["data"]
    existing_ids = set()
    playlist_genres: Counter = Counter()
    playlist_artists: Counter = Counter()

    for track in existing_tracks:
        attrs = track.get("attributes", {})
        catalog_rel = track.get("relationships", {}).get("catalog", {}).get("data", [])
        if catalog_rel:
            existing_ids.add(catalog_rel[0].get("id", ""))
        else:
            existing_ids.add(track.get("id", ""))

        for g in attrs.get("genreNames", []):
            if g.lower() != "music":
                playlist_genres[g] += 1
        artist = attrs.get("artistName", "")
        if artist:
            playlist_artists[artist] += 1

    # Build a target genre profile from the existing playlist
    target_genres = [g for g, _ in playlist_genres.most_common(5)]

    # Songs already in the library are excluded unless the caller opts back in
    library_ids = set() if include_library else set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))

    candidates = []

    # Source 1: Charts matching playlist genres
    print("  Fetching fresh tracks matching playlist signature...", file=sys.stderr)
    charts = call_api("charts", sf)
    if charts:
        for section in charts.get("results", {}).values():
            if isinstance(section, list):
                for chart in section:
                    for item in chart.get("data", []):
                        tid = item.get("id", "")
                        if tid in existing_ids or tid in disliked or tid in library_ids:
                            continue
                        attrs = item.get("attributes", {})
                        item_genres = filter_generic_genres(attrs.get("genreNames", []))
                        match = best_genre_match(item_genres, target_genres)
                        if match > 0:
                            candidates.append({
                                "id": tid,
                                "name": attrs.get("name", ""),
                                "artist": attrs.get("artistName", ""),
                                "album": "",
                                "genre": item_genres,
                                "source": "refresh",
                                "reason": "Fresh track matching your playlist's vibe.",
                                "_score": match,
                            })

    # Source 2: New tracks from artists already in the playlist
    top_playlist_artists = [a for a, _ in playlist_artists.most_common(5)]
    for artist_name in top_playlist_artists:
        artist = search_artist(sf, artist_name)
        if not artist:
            continue
        albums_data = call_api("artist-albums", sf, artist["id"])
        if not albums_data or "data" not in albums_data:
            continue
        for album in albums_data["data"][:2]:
            album_tracks = get_album_tracks(sf, album["id"])
            for track in album_tracks:
                tid = track.get("id", "")
                if tid in existing_ids or tid in disliked or tid in library_ids:
                    continue
                attrs = track.get("attributes", {})
                candidates.append({
                    "id": tid,
                    "name": attrs.get("name", ""),
                    "artist": attrs.get("artistName", artist_name),
                    "album": album.get("attributes", {}).get("name", ""),
                    "genre": filter_generic_genres(attrs.get("genreNames", [])),
                    "source": "refresh",
                    "reason": f"New from {artist_name}, matching your playlist.",
                    "_score": 0.7,
                })

    rng = random.Random()
    for c in candidates:
        c["_score"] += rng.random() * 0.2

    candidates.sort(key=lambda c: c["_score"], reverse=True)
    selected = candidates[:target_add]
    for c in selected:
        c.pop("_score", None)

    return selected


# ── Shared helpers for seed / era / blend ────────────────────────

def _first_data(result: dict | None, kind: str) -> list[dict]:
    """Pull results[kind].data from a search response."""
    if not result:
        return []
    return result.get("results", {}).get(kind, {}).get("data", []) or []


def _clean_genres(attrs: dict) -> list[str]:
    return filter_generic_genres(attrs.get("genreNames", []))


def _song_candidate(song: dict, source: str, reason: str, score: float,
                    fallback_artist: str = "", album: str | None = None) -> dict:
    """Build a candidate track dict from a catalog song resource."""
    attrs = song.get("attributes", {})
    return {
        "id": song.get("id", ""),
        "name": attrs.get("name", ""),
        "artist": attrs.get("artistName", fallback_artist),
        "album": album if album is not None else attrs.get("albumName", ""),
        "genre": _clean_genres(attrs),
        "source": source,
        "reason": reason,
        "_score": score,
    }


def _artist_top_songs(sf: str, artist_id: str) -> list[dict]:
    """Top songs for an artist (catalog song resources)."""
    top_data = call_api("artist-top", sf, artist_id)
    songs: list[dict] = []
    for ad in (top_data or {}).get("data", []):
        songs.extend(ad.get("views", {}).get("top-songs", {}).get("data", []))
    return songs


def _similar_artists(sf: str, artist_id: str) -> list[dict]:
    """Similar artists, tolerant of both the view and the relationship response shapes."""
    data = call_api("similar-artists", sf, artist_id)
    found: list[dict] = []
    for item in (data or {}).get("data", []):
        if item.get("type") == "artists":
            found.append(item)
        else:
            found.extend(item.get("views", {}).get("similar-artists", {}).get("data", []))
    return found


def _cap_per_artist(candidates: list[dict], target_size: int, cap: int = 3,
                    side_cap: int | None = None) -> list[dict]:
    """Pick the best-scoring candidates with at most `cap` tracks per artist.

    `side_cap` (blend only) limits how many tracks may come from each of the
    "a" / "b" sources so neither listener dominates.
    """
    counts: Counter = Counter()
    sides: Counter = Counter()
    picked = []
    for c in candidates:
        artist = c.get("artist", "")
        side = c.get("source")
        if counts[artist] >= cap:
            continue
        if side_cap is not None and side in ("a", "b") and sides[side] >= side_cap:
            continue
        counts[artist] += 1
        sides[side] += 1
        picked.append(c)
        if len(picked) >= target_size:
            break
    return picked


def _enforce_share(selected: list[dict], max_share: float) -> list[dict]:
    """Drop the lowest-scoring tracks from whichever blend side exceeds `max_share` of the
    *final* playlist. `selected` is in descending score order, so the last track of a side
    is its weakest. Can shrink the playlist (even to nothing) when one listener's
    candidates are scarce — a lopsided "blend" isn't returned."""
    picked = list(selected)
    while picked:
        counts = Counter(c.get("source") for c in picked)
        side = max(("a", "b"), key=lambda s: counts[s])
        if counts[side] / len(picked) <= max_share + 1e-9:
            break
        picked.pop(max(i for i, c in enumerate(picked) if c.get("source") == side))
    return picked


def _finish(candidates: list[dict], target_size: int, arc: str = "wave", cap: int = 3,
            side_cap: int | None = None, max_share: float | None = None) -> list[dict]:
    """Jitter, sort, cap per artist, strip internals, then sequence."""
    rng = random.Random()
    seen: set[str] = set()
    unique = []
    for c in candidates:
        if c["id"] and c["id"] not in seen:
            seen.add(c["id"])
            c["_score"] += rng.random() * 0.1
            unique.append(c)
    unique.sort(key=lambda c: c["_score"], reverse=True)
    selected = _cap_per_artist(unique, target_size, cap, side_cap)
    if max_share is not None:
        selected = _enforce_share(selected, max_share)
    for c in selected:
        c.pop("_score", None)
        c.pop("_is_wildcard", None)
    return sequence_tracks(selected, arc=arc)


# ── Strategy: Seed ("songs like X") ──────────────────────────────

def _resolve_seed(sf: str, seed: str, seed_type: str) -> tuple[dict | None, dict | None]:
    """Resolve a seed to (artist, song). Either may be None.

    ``auto`` searches artists and songs together: an exact artist-name match wins,
    then a song whose title matches, then the top artist hit, then the top song.
    """
    types = {"auto": "artists,songs", "artist": "artists", "song": "songs"}[seed_type]
    result = call_api("search", sf, seed, types)
    artists = _first_data(result, "artists")
    songs = _first_data(result, "songs")
    needle = seed.strip().lower()

    if seed_type == "artist":
        return (artists[0] if artists else None), None
    if seed_type == "song":
        song = songs[0] if songs else None
        return (search_artist(sf, song["attributes"].get("artistName", "")) if song else None), song

    for a in artists:
        if a.get("attributes", {}).get("name", "").lower() == needle:
            return a, None
    for song in songs:
        if needle in song.get("attributes", {}).get("name", "").lower():
            return search_artist(sf, song["attributes"].get("artistName", "")), song
    if artists:
        return artists[0], None
    if songs:
        song = songs[0]
        return search_artist(sf, song["attributes"].get("artistName", "")), song
    return None, None


def strategy_seed(profile: dict, sf: str, seed: str, seed_type: str = "auto",
                  target_size: int = 25, include_library: bool = False) -> list[dict]:
    """Playlist of songs like a seed artist or song, filtered through the user's taste."""
    if seed_type not in ("auto", "artist", "song"):
        raise ValueError("seed_type must be auto, artist or song")

    artist, song = _resolve_seed(sf, seed, seed_type)
    if not artist and not song:
        print(f"ERROR: Couldn't find '{seed}' in the catalog.", file=sys.stderr)
        return []

    artist_attrs = (artist or {}).get("attributes", {})
    seed_artist_name = artist_attrs.get("name") or (song or {}).get("attributes", {}).get("artistName", seed)
    seed_name = (song or {}).get("attributes", {}).get("name") if song else seed_artist_name
    seed_genres = _clean_genres(artist_attrs) or _clean_genres((song or {}).get("attributes", {}))
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:10]]
    # Artists you play a lot, or just added to your library, get a small boost
    loved_artists = {a["name"].lower() for a in profile.get("top_artists", [])}
    loved_artists |= {n.lower() for n in profile.get("recently_added_artists", [])}
    library_ids = set() if include_library else set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))
    seed_song_id = (song or {}).get("id", "")

    def score(genres: list[str], artist_name: str, base: float) -> float:
        total = base + 0.6 * best_genre_match(genres, seed_genres) + 0.3 * best_genre_match(genres, user_genres)
        if artist_name.lower() in loved_artists:
            total += 0.1
        return total

    def usable(tid: str) -> bool:
        return bool(tid) and tid != seed_song_id and tid not in library_ids and tid not in disliked

    candidates: list[dict] = []

    # Source 1: the seed artist's own top songs
    if artist and artist.get("id"):
        print(f"  Gathering top songs for {seed_artist_name}...", file=sys.stderr)
        for top in _artist_top_songs(sf, artist["id"]):
            if usable(top.get("id", "")):
                c = _song_candidate(top, "seed", f"One of {seed_artist_name}'s best.", 0.0, seed_artist_name)
                c["_score"] = score(c["genre"], c["artist"], 0.5)
                candidates.append(c)

    # Source 2: other tracks from the seed song's album
    album_rel = (song or {}).get("relationships", {}).get("albums", {}).get("data", [])
    if album_rel:
        for t in get_album_tracks(sf, album_rel[0].get("id", "")):
            if usable(t.get("id", "")):
                c = _song_candidate(t, "seed", f"From the same album as {seed_name}.", 0.0, seed_artist_name)
                c["_score"] = score(c["genre"], c["artist"], 0.55)
                candidates.append(c)

    # Source 3: similar artists' top songs
    similar = _similar_artists(sf, artist["id"]) if artist and artist.get("id") else []
    for sim in similar[:8]:
        sim_name = sim.get("attributes", {}).get("name", "")
        print(f"  Sampling {sim_name}...", file=sys.stderr)
        for top in _artist_top_songs(sf, sim.get("id", ""))[:4]:
            if usable(top.get("id", "")):
                c = _song_candidate(top, "similar", f"Fans of {seed_name} tend to love {sim_name}.", 0.0, sim_name)
                c["_score"] = score(c["genre"], c["artist"], 0.3)
                candidates.append(c)

    # Fallback: no similar-artist data, so search by the seed's genre
    if not similar and seed_genres:
        for found in _first_data(call_api("search", sf, seed_genres[0], "artists"), "artists")[:6]:
            if found.get("attributes", {}).get("name", "").lower() == seed_artist_name.lower():
                continue
            fname = found.get("attributes", {}).get("name", "")
            for top in _artist_top_songs(sf, found.get("id", ""))[:3]:
                if usable(top.get("id", "")):
                    c = _song_candidate(top, "similar", f"Shares a {seed_genres[0]} sound with {seed_name}.", 0.0, fname)
                    c["_score"] = score(c["genre"], c["artist"], 0.2)
                    candidates.append(c)

    return _finish(candidates, target_size)


# ── Strategy: Era ("90s throwback") ──────────────────────────────

def normalize_decade(value: str) -> str:
    """Normalize '90s', "'90s", '1990', '1990s' → '1990s' (the era_distribution format)."""
    m = re.fullmatch(r"'?(\d{2}|\d{4})s?", value.strip().lower())
    if not m:
        raise ValueError(f"Can't read decade '{value}'. Try something like 90s or 1990s.")
    digits = m.group(1)
    year = int(digits) if len(digits) == 4 else (2000 + int(digits) if int(digits) < 30 else 1900 + int(digits))
    return f"{(year // 10) * 10}s"


def _release_decade(date_str: str | None) -> str | None:
    """'1994-09-12' → '1990s' (None if unparseable)."""
    if date_str and len(date_str) >= 4 and date_str[:4].isdigit():
        return f"{(int(date_str[:4]) // 10) * 10}s"
    return None


def strategy_era(profile: dict, sf: str, decade: str | None = None, target_size: int = 30,
                 include_library: bool = False) -> list[dict]:
    """A throwback playlist from one decade, built from the user's own taste."""
    eras = profile.get("era_distribution", [])
    decade = normalize_decade(decade) if decade else (eras[0]["decade"] if eras else "2020s")

    top_artists = profile.get("top_artists", [])[:15]
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:10]]
    library_ids = set() if include_library else set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))
    candidates: list[dict] = []

    def usable(tid: str) -> bool:
        return bool(tid) and tid not in library_ids and tid not in disliked

    # Source 1: albums from the user's top artists released in the decade
    for i, artist in enumerate(top_artists):
        artist_id, artist_name = artist.get("id"), artist.get("name", "")
        if not artist_id:
            continue
        print(f"  [{i+1}/{len(top_artists)}] Looking for {artist_name} in the {decade}...", file=sys.stderr)
        albums = (call_api("artist-albums", sf, artist_id) or {}).get("data", [])
        in_decade = [a for a in albums
                     if _release_decade(a.get("attributes", {}).get("releaseDate")) == decade
                     and not a.get("attributes", {}).get("isSingle", False)]
        weight = min(artist.get("play_weight", 0) * 2, 0.3)
        for album in in_decade[:3]:
            album_name = album.get("attributes", {}).get("name", "")
            for t in get_album_tracks(sf, album["id"]):
                if usable(t.get("id", "")):
                    c = _song_candidate(t, "era", f"{artist_name} in the {decade} — from {album_name}.",
                                        0.5 + weight, artist_name, album_name)
                    c["_score"] += 0.3 * best_genre_match(c["genre"], user_genres)
                    candidates.append(c)
        if len(candidates) >= target_size * 3:
            break

    # Source 2: charts, for songs released in the decade (mostly useful for the current one)
    charts = call_api("charts", sf)
    for section in (charts or {}).get("results", {}).values():
        if not isinstance(section, list):
            continue
        for chart in section:
            for item in chart.get("data", []):
                attrs = item.get("attributes", {})
                if item.get("type", "songs") == "songs" and _release_decade(attrs.get("releaseDate")) == decade \
                        and usable(item.get("id", "")):
                    c = _song_candidate(item, "era", f"A {decade} track that fits your taste.", 0.4)
                    c["_score"] += 0.3 * best_genre_match(c["genre"], user_genres)
                    candidates.append(c)

    # Source 3: genre + decade search when we still don't have enough
    if len(candidates) < target_size:
        for genre in user_genres[:3]:
            found = _first_data(call_api("search", sf, f"{genre} {decade}", "songs"), "songs")
            for item in found:
                attrs = item.get("attributes", {})
                if _release_decade(attrs.get("releaseDate")) == decade and usable(item.get("id", "")):
                    c = _song_candidate(item, "era", f"{genre} from the {decade}.", 0.3)
                    c["_score"] += 0.3 * best_genre_match(c["genre"], user_genres)
                    candidates.append(c)

    return _finish(candidates, target_size)


# ── Strategy: Blend (two listeners, one playlist) ────────────────

BLEND_MAX_SHARE = 0.6  # neither listener may supply more than this share of the tracks


def strategy_blend(profile_a: dict, profile_b: dict, sf: str, target_size: int = 30) -> list[dict]:
    """A playlist both listeners should enjoy.

    Tracks are tagged ``source`` "shared" (artists in both top lists), "a" or "b"
    (one listener's rotation that is genre-adjacent to the other's taste).
    """
    compat = profile_compatibility(profile_a, profile_b)
    shared_names = set(compat["shared_artists"])
    genres_a = [g["genre"] for g in profile_a.get("genre_distribution", [])[:10]]
    genres_b = [g["genre"] for g in profile_b.get("genre_distribution", [])[:10]]
    disliked = set(profile_a.get("disliked_song_ids", [])) | set(profile_b.get("disliked_song_ids", []))
    candidates: list[dict] = []

    def add(song: dict, source: str, reason: str, score: float, artist_name: str) -> None:
        if song.get("id") and song["id"] not in disliked:
            c = _song_candidate(song, source, reason, score, artist_name)
            candidates.append(c)

    # Shared artists first, using whichever profile has the artist ID
    ids_by_name = {a["name"].lower(): a for a in profile_b.get("top_artists", []) if a.get("id")}
    ids_by_name.update({a["name"].lower(): a for a in profile_a.get("top_artists", []) if a.get("id")})
    for name in sorted(shared_names):
        artist = ids_by_name.get(name)
        if not artist:
            continue
        print(f"  Shared favorite: {artist['name']}...", file=sys.stderr)
        for song in _artist_top_songs(sf, artist["id"]):
            add(song, "shared", f"You both love {artist['name']}.", 1.0, artist["name"])

    # Each listener's own artists, kept only when they fit the other's genres
    for side, mine, other_genres, who, whom in (
        ("a", profile_a, genres_b, "your", "their"),
        ("b", profile_b, genres_a, "their", "your"),
    ):
        own = [a for a in mine.get("top_artists", [])[:10]
               if a.get("id") and a["name"].lower() not in shared_names]
        for artist in own[:8]:
            print(f"  Checking {artist['name']} against the other taste profile...", file=sys.stderr)
            for song in _artist_top_songs(sf, artist["id"])[:5]:
                match = best_genre_match(_clean_genres(song.get("attributes", {})), other_genres)
                if match > 0:
                    add(song, side, f"From {who} rotation — {artist['name']} should work for {whom} taste too.",
                        0.4 + 0.5 * match, artist["name"])

    # A few explicitly loved tracks from each listener
    for side, mine, who in (("a", profile_a, "your"), ("b", profile_b, "their")):
        for tid in mine.get("loved_track_ids", [])[:5]:
            detail = (call_api("song-detail", sf, tid) or {}).get("data", [])
            if detail:
                add(detail[0], side, f"A loved track from {who} library.", 0.6, "")

    cap = max(1, int(target_size * BLEND_MAX_SHARE))
    return _finish(candidates, target_size, side_cap=cap, max_share=BLEND_MAX_SHARE)


# ── Playlist Creation ────────────────────────────────────────────

def generate_name(strategy: str, mood: str | None = None,
                  profile: dict | None = None, seed: str | None = None,
                  decade: str | None = None) -> str:
    """Auto-generate a playlist name."""
    date_str = datetime.now(timezone.utc).strftime("%b %Y")
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
        "era": "A trip back to one decade, built from the artists and genres you play most.",
    }
    desc = descriptions.get(strategy, "Curated by Apple Music DJ.")
    return f"{desc} {track_count} tracks."


def check_playlist_exists(name: str) -> str | None:
    """Check if a playlist with this name already exists. Returns playlist ID or None."""
    try:
        result = subprocess.run(
            [str(SCRIPT_DIR / "apple_music_api.sh"), "library-playlists", "100"],
            capture_output=True, text=True, timeout=30,
        )
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
        result = subprocess.run(
            [str(SCRIPT_DIR / "build_playlist.sh"), "create", name, description, ids_file, "--yes"],
            capture_output=True, text=True, timeout=60,
        )
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
                        choices=["deep-cuts", "mood", "trend", "constellation", "refresh", "similar", "seed", "era", "blend"],
                        help="Playlist strategy to use")
    parser.add_argument("--profile", required=True, help="Path to taste profile JSON")
    parser.add_argument("--storefront", default=None, help="Storefront code")
    parser.add_argument("--mood", default=None,
                        help=f"Mood for mood strategy ({', '.join(MOOD_MAP)})")
    parser.add_argument("--playlist-id", default=None,
                        help="Playlist ID for refresh strategy")
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
    parser.add_argument("--include-library", action="store_true",
                        help="Refresh: allow songs already in your library")
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

    require_env_tokens()
    profile = load_profile(args.profile)
    config = load_config()

    sf = get_storefront(args.storefront or config.get("default_storefront"))

    target_size = args.size or config.get("playlist_size", 30)

    print(f"🎧 Strategy: {args.strategy} | Target: {target_size} tracks", file=sys.stderr)

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
        tracks = strategy_blend(profile, profile_b, sf, target_size)
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

    # Generate name & description
    name = args.name or generate_name(args.strategy, args.mood, profile, args.similar_to, args.decade)
    description = generate_description(args.strategy, args.mood, len(tracks))

    result = {
        "strategy": args.strategy,
        "name": name,
        "description": description,
        "track_count": len(tracks),
        "tracks": tracks,
    }
    if args.strategy == "blend":
        compat = profile_compatibility(profile, profile_b)
        result["compatibility"] = {k: compat[k] for k in ("compatibility_pct", "verdict", "shared_artists")}

    print(f"\n✅ {len(tracks)} tracks selected.", file=sys.stderr)

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
