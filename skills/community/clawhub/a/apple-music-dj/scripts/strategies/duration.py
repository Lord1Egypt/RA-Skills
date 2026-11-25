"""Fit a finished playlist to a running time (`--minutes`), keeping its order.

Every strategy hands back its tracks already in their final order (an energy arc, or
constellation's familiar-to-frontier gradient). Dropping tracks from such a list leaves a
subsequence, which keeps the shape: an ascending workout still ascends, a wave still peaks
in the middle. So fitting is only a question of *which* tracks to drop.
"""

import math
from collections.abc import Callable

AVERAGE_TRACK_MS = 210_000  # 3.5 min: sizes the candidate pool and stands in for a missing duration
OVERSAMPLE = 1.3            # ask the strategy for this much extra so there is room to trim
TOLERANCE_MS = 60_000       # the playlist lands within this of the target
MAX_MINUTES = 600


def pool_size_for(minutes: float) -> int:
    """How many tracks to ask a strategy for so that trimming can reach `minutes`."""
    return math.ceil(minutes * 60_000 / AVERAGE_TRACK_MS * OVERSAMPLE) + 2


def track_ms(track: dict) -> int:
    ms = track.get("duration_ms")
    return ms if isinstance(ms, int) and ms > 0 else AVERAGE_TRACK_MS


def total_ms(tracks: list[dict]) -> int:
    return sum(track_ms(t) for t in tracks)


def fit_to_duration(tracks: list[dict], target_ms: int, tolerance_ms: int = TOLERANCE_MS,
                    allowed: Callable[[list[dict]], bool] | None = None) -> list[dict]:
    """Drop tracks until the total is within `tolerance_ms` of `target_ms`; never reorders.

    Each step removes the track whose loss keeps the total closest to the target without
    undershooting it by more than the tolerance, preferring tracks far from ones already
    dropped (so no stretch of the arc is hollowed out) and never the opener or closer unless
    nothing else works. A list already shorter than the target is returned as is: the caller
    reports the real length.

    `allowed(playlist)` is a constraint the result must keep satisfying (blend's per-listener
    share): every removal and every later adjustment is checked against it.
    """
    ok = allowed or (lambda _tracks: True)
    kept = list(tracks)
    removed: list[int] = []  # positions in the original list
    positions = list(range(len(kept)))
    total = total_ms(kept)
    while total - target_ms > tolerance_ms and len(kept) > 1:
        candidates = range(1, len(kept) - 1) if len(kept) > 2 else range(len(kept))
        interior = [i for i in candidates if ok(kept[:i] + kept[i + 1:])]
        if not interior:
            break
        after = {i: total - track_ms(kept[i]) for i in interior}  # the total if track i were dropped
        fits = [i for i in interior if after[i] >= target_ms - tolerance_ms]
        pool = fits or interior
        # a gap-aware pick: farthest from earlier removals, then closest to the target
        best = max(pool, key=lambda i: (min((abs(positions[i] - r) for r in removed), default=len(tracks)),
                                        -abs(after[i] - target_ms)))
        if not fits and abs(after[best] - target_ms) >= abs(total - target_ms):
            break  # every removal overshoots further than where we are
        removed.append(positions[best])
        total = after[best]
        del kept[best]
        del positions[best]
    return _settle(tracks, positions, target_ms, tolerance_ms, ok)


def _settle(tracks: list[dict], positions: list[int], target_ms: int, tolerance_ms: int,
            ok: Callable[[list[dict]], bool]) -> list[dict]:
    """Greedy removal can get stuck a few seconds outside the tolerance when track lengths don't
    divide the gap. Finish with the best single move (drop any one track, drop two, add one back,
    or swap a kept track for a dropped one) that keeps `ok` true, until it lands or nothing
    improves it. Always keeps at least one track."""
    keep = set(positions)
    total = sum(track_ms(tracks[i]) for i in keep)
    ms = {i: track_ms(tracks[i]) for i in range(len(tracks))}
    for _ in range(len(tracks)):
        if abs(total - target_ms) <= tolerance_ms:
            break
        out = [i for i in range(len(tracks)) if i not in keep]
        ordered = sorted(keep)
        moves: list[tuple[int, set[int], set[int]]] = []  # (new total, positions removed, positions added)
        moves += [(total + ms[j], set(), {j}) for j in out]
        moves += [(total - ms[i] + ms[j], {i}, {j}) for i in ordered for j in out]
        if len(keep) > 1:
            moves += [(total - ms[i], {i}, set()) for i in ordered]
        if len(keep) > 2:
            moves += [(total - ms[a] - ms[b], {a, b}, set()) for a in ordered for b in ordered if a < b]
        moves = [m for m in moves if abs(m[0] - target_ms) < abs(total - target_ms)
                 and ok([tracks[i] for i in sorted((keep - m[1]) | m[2])])]
        if not moves:
            break
        best = min(moves, key=lambda m: abs(m[0] - target_ms))
        total = best[0]
        keep = (keep - best[1]) | best[2]
    return [tracks[i] for i in sorted(keep)]
