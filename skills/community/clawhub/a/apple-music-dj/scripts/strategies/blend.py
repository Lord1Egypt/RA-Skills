"""Strategy: blend (two listeners, one playlist)."""

import random
import sys

from _common import call_api, taste_affinity
from compatibility import profile_compatibility
from strategies.candidates import _artist_top_songs, _clean_genres, _finish, _song_candidate
from strategies.scoring import BLEND_LOVED_SCORE, BLEND_MAX_SHARE, BLEND_SHARED_SCORE, BLEND_SIDE_BASE, BLEND_SIDE_MATCH


# ── Strategy: Blend (two listeners, one playlist) ────────────────

def strategy_blend(profile_a: dict, profile_b: dict, sf: str, target_size: int = 30,
                   rng: random.Random | None = None) -> list[dict]:
    """A playlist both listeners should enjoy.

    Tracks are tagged ``source`` "shared" (artists in both top lists), "a" or "b"
    (one listener's rotation that is genre-adjacent to the other's taste).
    """
    compat = profile_compatibility(profile_a, profile_b)
    shared_names = set(compat["shared_artists"])
    genres_a = profile_a.get("genre_distribution", [])
    genres_b = profile_b.get("genre_distribution", [])
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
            add(song, "shared", f"You both love {artist['name']}.", BLEND_SHARED_SCORE, artist["name"])

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
                match = taste_affinity(_clean_genres(song.get("attributes", {})), other_genres)
                if match > 0:
                    add(song, side, f"From {who} rotation — {artist['name']} should work for {whom} taste too.",
                        BLEND_SIDE_BASE + BLEND_SIDE_MATCH * match, artist["name"])

    # A few explicitly loved tracks from each listener
    for side, mine, who in (("a", profile_a, "your"), ("b", profile_b, "their")):
        for tid in mine.get("loved_track_ids", [])[:5]:
            detail = (call_api("song-detail", sf, tid) or {}).get("data", [])
            if detail:
                add(detail[0], side, f"A loved track from {who} library.", BLEND_LOVED_SCORE, "")

    cap = max(1, int(target_size * BLEND_MAX_SHARE))
    return _finish(candidates, target_size, side_cap=cap, max_share=BLEND_MAX_SHARE, rng=rng)
