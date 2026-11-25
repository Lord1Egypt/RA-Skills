"""Strategy: era ("90s throwback")."""

import random
import re
import sys

from _common import call_api, get_album_tracks, taste_affinity
from strategies.candidates import _finish, _first_data, _song_candidate
from strategies.scoring import ERA_BASE, TASTE_WEIGHT, _artist_boost


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
                 include_library: bool = False, rng: random.Random | None = None) -> list[dict]:
    """A throwback playlist from one decade, built from the user's own taste."""
    eras = profile.get("era_distribution", [])
    decade = normalize_decade(decade) if decade else (eras[0]["decade"] if eras else "2020s")

    top_artists = profile.get("top_artists", [])[:15]
    user_genre_names = [g["genre"] for g in profile.get("genre_distribution", [])[:10]]
    user_genres = profile.get("genre_distribution", [])
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
        weight = _artist_boost(artist)
        for album in in_decade[:3]:
            album_name = album.get("attributes", {}).get("name", "")
            for t in get_album_tracks(sf, album["id"]):
                if usable(t.get("id", "")):
                    c = _song_candidate(t, "era", f"{artist_name} in the {decade} — from {album_name}.",
                                        ERA_BASE["artist"] + weight, artist_name, album_name)
                    c["_score"] += TASTE_WEIGHT * taste_affinity(c["genre"], user_genres)
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
                    c = _song_candidate(item, "era", f"A {decade} track that fits your taste.", ERA_BASE["chart"])
                    c["_score"] += TASTE_WEIGHT * taste_affinity(c["genre"], user_genres)
                    candidates.append(c)

    # Source 3: genre + decade search when we still don't have enough
    if len(candidates) < target_size:
        for genre in user_genre_names[:3]:
            found = _first_data(call_api("search", sf, f"{genre} {decade}", "songs"), "songs")
            for item in found:
                attrs = item.get("attributes", {})
                if _release_decade(attrs.get("releaseDate")) == decade and usable(item.get("id", "")):
                    c = _song_candidate(item, "era", f"{genre} from the {decade}.", ERA_BASE["search"])
                    c["_score"] += TASTE_WEIGHT * taste_affinity(c["genre"], user_genres)
                    candidates.append(c)

    return _finish(candidates, target_size, rng=rng)
