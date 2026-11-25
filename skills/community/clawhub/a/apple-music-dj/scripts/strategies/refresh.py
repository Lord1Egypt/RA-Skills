"""Strategy: refresh an existing playlist with new material."""

import random
import sys

from _common import best_genre_match, call_api, filter_generic_genres, get_album_tracks, search_artist
from collections import Counter
from strategies.candidates import USER_FILTERS, _finish
from strategies.scoring import REFRESH_ARTIST_SCORE


# ── Strategy: Refresh ────────────────────────────────────────────

def strategy_refresh(profile: dict, sf: str, playlist_id: str, target_add: int = 10,
                     include_library: bool = False, rng: random.Random | None = None) -> list[dict]:
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

    USER_FILTERS.setdefault("blocked_ids", set()).update(existing_ids)  # nor may a clean twin repeat a track

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
                                "duration_ms": attrs.get("durationInMillis"),
                                "explicit": attrs.get("contentRating") == "explicit",
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
        newest_first = sorted(albums_data["data"], key=lambda a: a.get("attributes", {}).get("releaseDate", ""),
                              reverse=True)
        for album in newest_first[:2]:
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
                    "duration_ms": attrs.get("durationInMillis"),
                    "explicit": attrs.get("contentRating") == "explicit",
                    "source": "refresh",
                    "reason": f"New from {artist_name}, matching your playlist.",
                    "_score": REFRESH_ARTIST_SCORE,
                })

    # Additions keep their score order (no arc): they're appended to a playlist that already has one
    return _finish(candidates, target_add, arc="none", rng=rng)
