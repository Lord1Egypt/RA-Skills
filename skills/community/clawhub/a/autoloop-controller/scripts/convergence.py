"""Convergence detection for autoloop."""

from __future__ import annotations


def detect_plateau(score_history: list[dict], window: int = 3) -> bool:
    """Consecutive `window` rounds with no weighted_score improvement.

    Returns True if the best score in the last `window` rounds
    does not exceed the historical best before that window.
    """
    if len(score_history) < window + 1:
        return False
    recent = score_history[-window:]
    earlier = score_history[:-window]
    best_before = max(h["weighted_score"] for h in earlier)
    best_recent = max(h["weighted_score"] for h in recent)
    return best_recent <= best_before


def detect_oscillation(score_history: list[dict], window: int = 4) -> bool:
    """Detect keep-reject-keep-reject oscillation pattern.

    If the last `window` decisions alternate between keep and reject,
    the loop is unlikely to converge.
    """
    if len(score_history) < window:
        return False
    recent_decisions = [h["decision"] for h in score_history[-window:]]
    # Check for alternating pattern
    pattern = ["keep", "reject"] * (window // 2)
    alt_pattern = ["reject", "keep"] * (window // 2)
    return recent_decisions == pattern or recent_decisions == alt_pattern


def compute_weighted_score(scores: dict[str, float], weights: dict[str, float] | None = None) -> float:
    """Compute weighted average score across dimensions.

    Default weights treat all dimensions equally.
    """
    if weights is None:
        # Equal weights for all dimensions
        n = len(scores)
        if n == 0:
            return 0.0
        return sum(scores.values()) / n

    total = 0.0
    weight_sum = 0.0
    for dim, score in scores.items():
        w = weights.get(dim, 0.0)
        total += score * w
        weight_sum += w

    return total / weight_sum if weight_sum > 0 else 0.0
