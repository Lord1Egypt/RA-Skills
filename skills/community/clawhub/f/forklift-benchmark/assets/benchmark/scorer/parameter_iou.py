"""FK-Bench v2 — Parameter continuous tolerance (IoU).

For each pair of (gold, pred) actions sharing the same ``kind`` and
``params`` keys, compute a per-key tolerance score:

    score(key) = 1.0                          if exact match
    score(key) = 1.0 - min(|g - p| / tol, 1)  if numeric (with tolerance)
    score(key) = 0.0                          if categorical mismatch

For NAVIGATE the (to_x, to_y) pair is treated as a 2D vector with
tolerance 1.0 m. For LIFT/LOWER the tolerance is 0.2 m. For TILT/ROTATE
it is 5 degrees. For SIDESHIFT it is 50 mm. For FORK_ADJUST 100 mm.
For TRAVERSE 0.2 m. For everything else (categorical) exact match.

The final IoU is the average per-key score over the union of keys.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from dsl.actions import Action


# Per-key tolerances for numeric parameters.
TOLERANCES: Dict[str, float] = {
    "to_height_m": 0.2,    # metres
    "to_deg": 5.0,         # degrees
    "offset_mm": 50.0,     # mm
    "width_mm": 100.0,     # mm
    "depth_m": 0.2,        # metres
    "max_speed_mps": 0.5,  # m/s
    "force_n": 200.0,      # N
    "to_x": 1.0,           # metres (combined with to_y for 2D)
    "to_y": 1.0,
}


def _score_key(gold_v: Any, pred_v: Any, key: str) -> float:
    if gold_v is None and pred_v is None:
        return 1.0
    if gold_v is None or pred_v is None:
        return 0.0
    # Numeric: relative tolerance
    if isinstance(gold_v, (int, float)) and isinstance(pred_v, (int, float)):
        tol = TOLERANCES.get(key, max(abs(float(gold_v)) * 0.1, 1e-6))
        return max(0.0, 1.0 - abs(float(gold_v) - float(pred_v)) / tol)
    # Categorical: exact
    return 1.0 if gold_v == pred_v else 0.0


def _score_action_pair(g: Action, p: Action) -> float:
    if g.kind != p.kind:
        return 0.0
    if not g.params and not p.params:
        return 1.0
    keys = set(g.params) | set(p.params)
    if not keys:
        return 1.0
    if g.kind == "NAVIGATE":
        # Treat (to_x, to_y) as a 2D vector
        dx = _score_key(g.params.get("to_x"), p.params.get("to_x"), "to_x")
        dy = _score_key(g.params.get("to_y"), p.params.get("to_y"), "to_y")
        return 0.5 * (dx + dy)
    return sum(_score_key(g.params.get(k), p.params.get(k), k) for k in keys) / len(keys)


def parameter_iou(gold: List[Action], pred: List[Action]) -> float:
    """Average parameter IoU over shared actions.

    For each pair of (gold[i], pred[i]) for i in range(min(len(gold),
    len(pred))), compute the per-action parameter score, then average
    over the max length so a too-short plan is penalised.
    """
    if not gold and not pred:
        return 1.0
    if not gold or not pred:
        return 0.0
    pairs: List[Tuple[Action, Action]] = list(zip(gold, pred))
    if not pairs:
        return 0.0
    avg = sum(_score_action_pair(g, p) for g, p in pairs) / len(pairs)
    # Penalise a length mismatch: scale by len(min)/len(max).
    length_factor = min(len(gold), len(pred)) / max(len(gold), len(pred))
    return round(avg * length_factor, 4)
