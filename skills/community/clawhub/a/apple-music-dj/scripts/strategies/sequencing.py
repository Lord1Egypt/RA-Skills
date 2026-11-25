"""Ordering a finished candidate list into a listenable playlist (energy arcs, album caps)."""

from _common import track_energy
from collections import Counter


# ── Sequencing ───────────────────────────────────────────────────

ARCS = ("wave", "ascending", "descending", "none")


ALBUM_CAP = 2  # max tracks from one album in any playlist


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
        if album and album_counts[album] >= ALBUM_CAP:
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
