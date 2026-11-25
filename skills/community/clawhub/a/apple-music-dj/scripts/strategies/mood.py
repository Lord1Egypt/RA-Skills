"""Strategy: mood / activity-matched playlists filtered through your taste."""

import random
import sys

from _common import best_genre_match, call_api, filter_generic_genres, get_album_tracks, taste_affinity, track_energy
from strategies.candidates import _finish
from strategies.scoring import MIN_ENERGY_FIT, MOOD_ENERGY_WEIGHT, MOOD_GENRE_WEIGHT, MOOD_TASTE_WEIGHT, OWN_ARTIST_BOOST


# ── Mood/Activity Mapping ────────────────────────────────────────

MOOD_MAP: dict[str, dict] = {
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


# Numeric target for each MOOD_MAP energy label, on GENRE_ENERGY's 0-1 scale
MOOD_ENERGY = {
    "very-low": 0.1, "low": 0.25, "low-med": 0.35, "medium": 0.5,
    "med-high": 0.65, "high": 0.8, "very-high": 0.95,
}


# ── Strategy: Mood/Activity ──────────────────────────────────────

def strategy_mood(profile: dict, sf: str, mood: str, target_size: int = 30,
                  rng: random.Random | None = None) -> list[dict]:
    """Mood/Activity-matched playlist filtered through user taste.

    Score = 0.5 x mood-genre match + 0.35 x energy fit + 0.15 x taste match (+0.1 for your
    own artists). Energy fit is 1 - |track energy - the mood's target|; tracks below
    MIN_ENERGY_FIT are dropped: a short sleep mix beats one padded with loud tracks.
    A track qualifies through a mood genre *or* one of your own genres, so a jazz fan's
    sleep mix can be quiet jazz and a rock fan's workout loud rock.
    """
    mood_config = MOOD_MAP.get(mood)
    if not mood_config:
        print(f"ERROR: Unknown mood '{mood}'. Available: {', '.join(MOOD_MAP)}", file=sys.stderr)
        sys.exit(1)

    target_genres = mood_config["genres"]
    target_energy = MOOD_ENERGY[mood_config["energy"]]
    user_genres = profile.get("genre_distribution", [])
    library_ids = set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))

    def score(genres: list[str]) -> float | None:
        """None when the track's energy is too far from the mood's, or it fits neither the
        mood's genres nor yours."""
        energy_fit = 1 - abs(track_energy(genres) - target_energy)
        genre_match = best_genre_match(genres, target_genres)
        taste = taste_affinity(genres, user_genres)
        if energy_fit < MIN_ENERGY_FIT or (genre_match == 0 and taste == 0):
            return None
        return MOOD_GENRE_WEIGHT * genre_match + MOOD_ENERGY_WEIGHT * energy_fit + MOOD_TASTE_WEIGHT * taste

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
                        item_score = score(item_genres)
                        if item_score is not None:
                            candidates.append({
                                "id": tid,
                                "name": attrs.get("name", ""),
                                "artist": attrs.get("artistName", ""),
                                "album": "",
                                "genre": item_genres,
                                "duration_ms": attrs.get("durationInMillis"),
                                "explicit": attrs.get("contentRating") == "explicit",
                                "source": "trending",
                                "reason": f"Matches your {mood} vibe.",
                                "_score": item_score,
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
                item_score = score(item_genres)
                if item_score is not None:
                    candidates.append({
                        "id": tid,
                        "name": attrs.get("name", ""),
                        "artist": attrs.get("artistName", artist["name"]),
                        "album": album.get("attributes", {}).get("name", ""),
                        "genre": item_genres,
                        "duration_ms": attrs.get("durationInMillis"),
                        "explicit": attrs.get("contentRating") == "explicit",
                        "source": "deep_cut",
                        "reason": f"From {artist['name']} — fits your {mood} mood.",
                        "_score": item_score + OWN_ARTIST_BOOST,
                    })

    return _finish(candidates, target_size, arc=mood_config.get("arc", "wave"), rng=rng)
