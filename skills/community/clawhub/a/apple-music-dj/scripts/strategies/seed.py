"""Strategy: seed ("songs like X")."""

import random
import sys

from _common import best_genre_match, call_api, get_album_tracks, search_artist, taste_affinity
from strategies.candidates import USER_FILTERS, _artist_top_songs, _clean_genres, _finish, _first_data, _similar_artists, _song_candidate
from strategies.scoring import OWN_ARTIST_BOOST, SEED_BASE, SEED_MATCH_WEIGHT, TASTE_WEIGHT


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
                  target_size: int = 25, include_library: bool = False,
                  rng: random.Random | None = None) -> list[dict]:
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
    user_genres = profile.get("genre_distribution", [])
    # Artists you play a lot, or just added to your library, get a small boost
    loved_artists = {a["name"].lower() for a in profile.get("top_artists", [])}
    loved_artists |= {n.lower() for n in profile.get("recently_added_artists", [])}
    library_ids = set() if include_library else set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))
    seed_song_id = (song or {}).get("id", "")
    USER_FILTERS.setdefault("blocked_ids", set()).add(seed_song_id)  # a clean twin must not bring the seed back

    def score(genres: list[str], artist_name: str, base: float) -> float:
        total = (base + SEED_MATCH_WEIGHT * best_genre_match(genres, seed_genres)
                 + TASTE_WEIGHT * taste_affinity(genres, user_genres))
        if artist_name.lower() in loved_artists:
            total += OWN_ARTIST_BOOST
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
                c["_score"] = score(c["genre"], c["artist"], SEED_BASE["top"])
                candidates.append(c)

    # Source 2: other tracks from the seed song's album
    album_rel = (song or {}).get("relationships", {}).get("albums", {}).get("data", [])
    if album_rel:
        for t in get_album_tracks(sf, album_rel[0].get("id", "")):
            if usable(t.get("id", "")):
                c = _song_candidate(t, "seed", f"From the same album as {seed_name}.", 0.0, seed_artist_name)
                c["_score"] = score(c["genre"], c["artist"], SEED_BASE["album"])
                candidates.append(c)

    # Source 3: similar artists' top songs
    similar = _similar_artists(sf, artist["id"]) if artist and artist.get("id") else []
    for sim in similar[:8]:
        sim_name = sim.get("attributes", {}).get("name", "")
        print(f"  Sampling {sim_name}...", file=sys.stderr)
        for top in _artist_top_songs(sf, sim.get("id", ""))[:4]:
            if usable(top.get("id", "")):
                c = _song_candidate(top, "similar", f"Fans of {seed_name} tend to love {sim_name}.", 0.0, sim_name)
                c["_score"] = score(c["genre"], c["artist"], SEED_BASE["similar"])
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
                    c["_score"] = score(c["genre"], c["artist"], SEED_BASE["genre_fallback"])
                    candidates.append(c)

    return _finish(candidates, target_size, rng=rng)
