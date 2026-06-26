"""Normalize raw API responses to canonical schema objects for /depradar."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any, Dict, List, TypeVar, Union

sys.path.insert(0, str(Path(__file__).parent))
from schema import (
    GithubIssueItem, StackOverflowItem, RedditItem,
    HackerNewsItem, TwitterItem, PackageUpdate, SubScores,
)
from dates import recency_score, days_since

# Union type for all community items
CommunityItem = Union[
    GithubIssueItem, StackOverflowItem, RedditItem, HackerNewsItem, TwitterItem
]

T = TypeVar("T")


# ── Min-max normalization ─────────────────────────────────────────────────────

def normalize_to_100(values: List[float]) -> List[int]:
    """Min-max normalize a list of floats to integers in [0, 100].

    If all values are equal, returns 50 for each.
    """
    if not values:
        return []
    min_v = min(values)
    max_v = max(values)
    span = max_v - min_v
    if span == 0:
        return [50] * len(values)
    return [int(round((v - min_v) / span * 100)) for v in values]


def normalize_scores(items: List[Any], score_attr: str = "score") -> List[Any]:
    """Re-normalize the `score` attribute of a list of items to [0, 100].

    Only applies min-max scaling when scores are on an *unbounded* scale
    (max > 100). Scores already in the calibrated [0, 100] range are left
    intact — rescaling them would destroy absolute meaning and make
    cross-batch comparison invalid (e.g. [80, 81, 82] → [0, 50, 100]).

    Mutates items in place and returns the list.
    """
    raw_scores = [float(getattr(item, score_attr, 0)) for item in items]
    if not raw_scores or max(raw_scores) <= 100:
        # Already in calibrated [0, 100] range — do not rescale.
        return items
    normalized = normalize_to_100(raw_scores)
    for item, norm in zip(items, normalized):
        setattr(item, score_attr, norm)
    return items


# ── Recency sub-score application ─────────────────────────────────────────────

def apply_recency_scores(items: List[CommunityItem]) -> List[CommunityItem]:
    """Add recency sub-scores to community items.

    Each item type stores its date in a different field; this function
    handles all variants. Mutates subs.recency in place.
    """
    for item in items:
        date_str = _get_date(item)
        recency = recency_score(date_str)
        if item.subs is None:
            item.subs = SubScores(recency=recency)
        else:
            item.subs.recency = recency
    return items


def _get_date(item: CommunityItem) -> str:
    """Extract a date string from any community item type."""
    if isinstance(item, GithubIssueItem):
        return item.created_at or ""
    if isinstance(item, StackOverflowItem):
        return item.created_at or ""
    if isinstance(item, (RedditItem, HackerNewsItem, TwitterItem)):
        return item.date or ""
    return ""


# ── Sub-score normalization across a batch ────────────────────────────────────

def normalize_sub_scores(items: List[CommunityItem]) -> List[CommunityItem]:
    """Normalize each sub-score dimension (severity, recency, impact, community)
    independently across all items using min-max scaling.

    Only applies scaling when a dimension uses an unbounded raw scale (max > 100).
    Sub-scores produced by score.py are already in [0, 100] — rescaling them
    independently would break the weight ratios in composite_score() and destroy
    the calibrated meaning of each dimension.

    Mutates items in place and returns the list.
    """
    if not items:
        return items

    dims = ("severity", "recency", "impact", "community")
    for dim in dims:
        raw = [float(getattr(item.subs, dim, 0)) if item.subs else 0.0 for item in items]
        if not raw or max(raw) <= 100:
            # Already in calibrated [0, 100] range — do not rescale.
            continue
        normed = normalize_to_100(raw)
        for item, val in zip(items, normed):
            if item.subs is None:
                item.subs = SubScores()
            setattr(item.subs, dim, val)

    return items


# ── Composite score helpers ───────────────────────────────────────────────────

def composite_score(subs: SubScores, weights: Dict[str, float] = None) -> int:
    """Compute a weighted composite score from SubScores.

    Default weights: severity=0.30, recency=0.30, impact=0.25, community=0.15
    """
    if weights is None:
        weights = {
            "severity":  0.30,
            "recency":   0.30,
            "impact":    0.25,
            "community": 0.15,
        }
    score = (
        weights.get("severity", 0)  * subs.severity
        + weights.get("recency", 0)   * subs.recency
        + weights.get("impact", 0)    * subs.impact
        + weights.get("community", 0) * subs.community
    )
    return min(100, max(0, int(round(score))))


def recompute_scores(
    items: List[CommunityItem],
    weights: Dict[str, float] = None,
) -> List[CommunityItem]:
    """Recompute item.score from item.subs using composite_score."""
    for item in items:
        if item.subs is not None:
            item.score = composite_score(item.subs, weights)
    return items


# ── Safe log helpers (used by backends) ───────────────────────────────────────

def safe_log1p(x: float) -> float:
    """log1p clamped to non-negative input."""
    return math.log1p(max(0.0, x))


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> int:
    """Clamp a float to [lo, hi] and return as int."""
    return int(round(max(lo, min(hi, value))))
