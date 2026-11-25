"""Candidate sourcing and selection helpers shared by the seed, era and blend strategies."""

import random

from _common import apply_user_filters, call_api, filter_generic_genres
from collections import Counter
from strategies.scoring import ARTIST_CAP, JITTER
from strategies.sequencing import ALBUM_CAP, sequence_tracks


# config.json preferences and recent-playlist exclusions; main() fills this in
USER_FILTERS: dict = {}


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
        "duration_ms": attrs.get("durationInMillis"),
        "explicit": attrs.get("contentRating") == "explicit",
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


def _cap_per_artist(candidates: list[dict], target_size: int, cap: int = ARTIST_CAP,
                    side_cap: int | None = None) -> list[dict]:
    """Pick the best-scoring candidates with at most `cap` tracks per artist and
    ALBUM_CAP per album (the same album rule sequence_tracks applies, so nothing picked
    here is dropped there).

    `side_cap` (blend only) limits how many tracks may come from each of the
    "a" / "b" sources so neither listener dominates.
    """
    counts: Counter = Counter()
    sides: Counter = Counter()
    albums: Counter = Counter()
    picked: list[dict] = []
    if target_size <= 0:
        return picked
    for c in candidates:
        artist = c.get("artist", "")
        album = c.get("album", "")
        side = c.get("source")
        if counts[artist] >= cap or (album and albums[album] >= ALBUM_CAP):
            continue
        if side_cap is not None and side in ("a", "b") and sides[side] >= side_cap:
            continue
        counts[artist] += 1
        albums[album] += 1
        sides[side] += 1
        picked.append(c)
        if len(picked) >= target_size:
            break
    return picked


def share_within(tracks: list[dict], max_share: float) -> bool:
    """True when neither blend side supplies more than `max_share` of `tracks`."""
    if not tracks:
        return True
    counts = Counter(c.get("source") for c in tracks)
    return max(counts["a"], counts["b"]) / len(tracks) <= max_share + 1e-9


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


def _finish(candidates: list[dict], target_size: int, arc: str = "wave", cap: int = ARTIST_CAP,
            side_cap: int | None = None, max_share: float | None = None,
            rng: random.Random | None = None) -> list[dict]:
    """Apply the user's filters, jitter, sort, cap per artist, strip internals, then sequence."""
    rng = rng or random.Random()
    seen: set[str] = set()
    unique = []
    for c in apply_user_filters(candidates, USER_FILTERS):
        if c["id"] and c["id"] not in seen:
            seen.add(c["id"])
            c["_score"] += rng.random() * JITTER
            unique.append(c)
    unique.sort(key=lambda c: c["_score"], reverse=True)
    selected = _cap_per_artist(unique, target_size, cap, side_cap)
    if max_share is not None:
        selected = _enforce_share(selected, max_share)
    for c in selected:
        c.pop("_score", None)
        c.pop("_is_wildcard", None)
    return sequence_tracks(selected, arc=arc)
