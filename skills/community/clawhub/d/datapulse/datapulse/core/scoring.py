"""Multi-dimensional scoring engine for DataPulse items."""

import math
import os
import re
from collections import Counter
from datetime import datetime, timezone

from .models import DataPulseItem
from .triage import normalize_review_state, review_state_score
from .utils import content_fingerprint, get_domain


# Default dimension weights (sum to 1.0; source_diversity is configurable for controlled rollout).
def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    try:
        return float(raw) if raw is not None else default
    except (TypeError, ValueError):
        return default


def _default_weights() -> dict[str, float]:
    return {
        "confidence": 0.25,
        "authority": 0.30,
        "corroboration": 0.25,
        "entity_corroboration": _env_float("DATAPULSE_ENTITY_CORROBORATION_WEIGHT", 0.0),
        "recency": 0.20,
        "source_diversity": _env_float("DATAPULSE_SOURCE_DIVERSITY_WEIGHT", 0.07),
        "cross_validation": _env_float("DATAPULSE_CROSS_VALIDATION_WEIGHT", 0.06),
        "recency_bonus": _env_float("DATAPULSE_RECENCY_BONUS_WEIGHT", 0.00),
        "engagement": _env_float("DATAPULSE_ENGAGEMENT_WEIGHT", 0.08),
        "search_noise_penalty": _env_float("DATAPULSE_SEARCH_NOISE_PENALTY_WEIGHT", 0.08),
        "review_state": _env_float("DATAPULSE_REVIEW_STATE_WEIGHT", 0.08),
    }


DEFAULT_WEIGHTS = _default_weights()

# Default half-life for recency decay (hours)
_DEFAULT_HALF_LIFE_HOURS = 24.0
_TWITTER_EPOCH_MS = 1288834974657


def recency_score(fetched_at: str, now: datetime | None = None) -> float:
    """Compute exponential decay recency score.

    Returns 1.0 for brand new, decays with half-life from DATAPULSE_RECENCY_HALF_LIFE env (default 24h).
    """
    if now is None:
        now = datetime.now(timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    else:
        now = now.astimezone(timezone.utc)
    try:
        ts = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError, TypeError):
        return 0.5  # fallback for unparseable timestamps
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    else:
        ts = ts.astimezone(timezone.utc)

    age_hours = max(0.0, (now - ts).total_seconds() / 3600.0)
    half_life = float(os.getenv("DATAPULSE_RECENCY_HALF_LIFE", str(_DEFAULT_HALF_LIFE_HOURS)))
    if half_life <= 0:
        half_life = _DEFAULT_HALF_LIFE_HOURS

    return math.pow(2, -age_hours / half_life)


def _parse_timestamp_candidate(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 1_000_000_000_000:  # milliseconds epoch
            ts = ts / 1000.0
        if ts <= 0:
            return None
        try:
            return datetime.fromtimestamp(ts, timezone.utc)
        except (ValueError, OSError):
            return None

    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        return _parse_timestamp_candidate(float(text))

    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _tweet_time_from_url(url: str) -> datetime | None:
    matched = re.search(r"/status/(\d+)", str(url or ""))
    if not matched:
        return None
    try:
        tid = int(matched.group(1))
    except (TypeError, ValueError):
        return None
    ms = (tid >> 22) + _TWITTER_EPOCH_MS
    if ms <= 0:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000.0, timezone.utc)
    except (ValueError, OSError):
        return None


def recency_reference(item: DataPulseItem) -> tuple[str, str]:
    """Resolve which timestamp should drive recency for an item.

    Priority:
    1) explicit source-published fields
    2) nested search_raw published fields
    3) twitter status snowflake time
    4) fallback fetched_at
    """
    extra = item.extra if isinstance(item.extra, dict) else {}

    direct_keys = (
        "source_published_at",
        "published_at",
        "published_date",
        "created_at",
        "created_utc",
        "timestamp",
    )
    for key in direct_keys:
        if key not in extra:
            continue
        parsed = _parse_timestamp_candidate(extra.get(key))
        if parsed is not None:
            return parsed.isoformat(), key

    search_raw = extra.get("search_raw")
    if isinstance(search_raw, dict):
        nested_keys = (
            "published_date",
            "published_at",
            "published",
            "created_at",
            "created_utc",
            "timestamp",
        )
        for key in nested_keys:
            if key not in search_raw:
                continue
            parsed = _parse_timestamp_candidate(search_raw.get(key))
            if parsed is not None:
                return parsed.isoformat(), f"search_raw.{key}"

    tweet_time = _tweet_time_from_url(item.url)
    if tweet_time is not None:
        return tweet_time.isoformat(), "twitter_status_id"

    return item.fetched_at, "fetched_at"


def authority_score(item: DataPulseItem, authority_map: dict[str, float]) -> float:
    """Look up source authority weight from the authority map.

    Checks source_name (lowered), then domain of url.
    Falls back to 0.5 if unknown.
    """
    name_key = item.source_name.lower()
    if name_key in authority_map:
        return authority_map[name_key]

    domain = get_domain(item.url)
    if domain in authority_map:
        return authority_map[domain]

    return 0.5


def corroboration_score(item: DataPulseItem, fingerprint_counts: dict[str, int]) -> float:
    """Score based on how many sources reported the same story.

    Single source → 0.0, two sources → 0.5, three+ → 1.0.
    """
    fp = content_fingerprint(item.content)
    count = fingerprint_counts.get(fp, 1)
    if count <= 1:
        return 0.0
    if count == 2:
        return 0.5
    return 1.0


def entity_corroboration_bonus(
    item: DataPulseItem,
    entity_source_counts: dict[str, int] | None = None,
) -> float:
    """Bonus score for entities confirmed by multiple source documents."""
    if not entity_source_counts:
        return 0.0

    raw_entities = item.extra.get("entities") or []
    entity_names = []
    for entity in raw_entities:
        if isinstance(entity, dict):
            name = str(entity.get("name", "")).strip().upper()
        elif isinstance(entity, str):
            name = entity.strip().upper()
        else:
            continue
        if name:
            entity_names.append(name)

    if not entity_names:
        return 0.0

    multi_source_count = 0
    for name in entity_names:
        if entity_source_counts.get(name, 0) >= 2:
            multi_source_count += 1

    if multi_source_count <= 0:
        return 0.0
    return min(0.3, multi_source_count * 0.1)


def source_diversity_score(item: DataPulseItem) -> float:
    """Score based on multi-source search confirmation."""
    sources = item.extra.get("search_sources")
    if not sources:
        return 0.0
    uniq = {s.lower() for s in sources if s}
    if len(uniq) <= 1:
        return 0.0
    if len(uniq) == 2:
        return 0.8
    return 1.0


def cross_validation_score(item: DataPulseItem) -> float:
    """Score based on search cross-source consistency and multi-source hits."""
    search_consistency = item.extra.get("search_cross_validation") or item.extra.get(
        "search_consistency",
    )
    if isinstance(search_consistency, dict):
        if search_consistency.get("is_cross_validated"):
            return 1.0
        provider_count = search_consistency.get("provider_count", 0)
        if provider_count >= 2:
            return 0.7
        if provider_count == 1:
            return 0.1
    source_count = item.extra.get("search_source_count", 0)
    if source_count >= 2:
        return 0.4
    return 0.0


def _to_nonnegative_float(value: object) -> float:
    try:
        parsed = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, parsed)


def engagement_score(item: DataPulseItem) -> float:
    """Source-native engagement score for sorting differentiation.

    Uses Reddit-native metrics when present and falls back to 0 for items
    without engagement metadata.
    """
    score_raw = _to_nonnegative_float(item.extra.get("score"))
    comments_raw = _to_nonnegative_float(item.extra.get("num_comments"))
    upvote_ratio_raw = item.extra.get("upvote_ratio")

    has_any = bool(score_raw or comments_raw or upvote_ratio_raw is not None)
    if not has_any:
        return 0.0

    # Saturating normalization to avoid outliers dominating rank.
    score_norm = min(score_raw / 2000.0, 1.0)
    comments_norm = min(comments_raw / 500.0, 1.0)

    upvote_ratio = _to_nonnegative_float(upvote_ratio_raw)
    upvote_ratio_norm = min(upvote_ratio, 1.0)

    # Score/comments are stronger discussion intensity signals; upvote ratio
    # provides quality directionality when available.
    return round(
        (score_norm * 0.5)
        + (comments_norm * 0.35)
        + (upvote_ratio_norm * 0.15),
        4,
    )


def search_noise_penalty(item: DataPulseItem) -> float:
    """Penalty for likely low-value search listicles/marketing pages."""
    extra = item.extra if isinstance(item.extra, dict) else {}
    parser = (item.parser or "").lower()
    if "search_query" not in extra and "search" not in parser:
        return 0.0

    title_url = f"{item.title} {item.url}".lower()
    content = (item.content or "").lower()
    penalty = 0.0

    marketing_markers = (
        "top ",
        "top-",
        "best ",
        "alternatives",
        "comparison",
        " vs ",
        "list of",
        "tools for",
        "software for",
    )
    if any(marker in title_url for marker in marketing_markers):
        penalty += 0.35
    if len(content.strip()) < 120:
        penalty += 0.12
    if "sponsored" in content or "affiliate" in content:
        penalty += 0.20
    if "github.com/" in title_url or "github.com/" in content:
        penalty -= 0.20

    return round(max(0.0, min(1.0, penalty)), 4)


def compute_composite_score(
    item: DataPulseItem,
    *,
    authority_map: dict[str, float] | None = None,
    fingerprint_counts: dict[str, int] | None = None,
    entity_source_counts: dict[str, int] | None = None,
    now: datetime | None = None,
    weights: dict[str, float] | None = None,
) -> tuple[int, dict[str, float | str]]:
    """Compute composite score (0-100) and return dimension breakdown.

    Does NOT modify item.confidence.
    """
    w = weights or DEFAULT_WEIGHTS
    amap = authority_map or {}
    fp_counts = fingerprint_counts or {}

    dim_confidence = item.confidence
    dim_authority = authority_score(item, amap)
    dim_corroboration = corroboration_score(item, fp_counts)
    dim_entity = entity_corroboration_bonus(item, entity_source_counts=entity_source_counts)
    recency_anchor, recency_source = recency_reference(item)
    dim_recency = recency_score(recency_anchor, now=now)
    dim_source_diversity = source_diversity_score(item)
    w_source_diversity = w.get("source_diversity", 0.0)
    dim_cross_validation = cross_validation_score(item)
    w_cross_validation = w.get("cross_validation", 0.0)
    dim_engagement = engagement_score(item)
    w_engagement = w.get("engagement", 0.0)
    dim_search_noise = search_noise_penalty(item)
    w_search_noise = w.get("search_noise_penalty", 0.0)
    dim_review_state = review_state_score(item.review_state)
    w_review_state = w.get("review_state", 0.0)
    review_state_label = normalize_review_state(item.review_state, processed=item.processed)
    # Backward-compatible alias to satisfy acceptance docs using "recency_bonus" naming.
    recency_bonus = dim_recency * w.get("recency_bonus", 0.0)

    raw = (
        w.get("confidence", 0.25) * dim_confidence
        + w.get("authority", 0.30) * dim_authority
        + w.get("corroboration", 0.25) * dim_corroboration
        + w.get("entity_corroboration", 0.0) * dim_entity
        + w.get("recency", 0.20) * dim_recency
        + w_source_diversity * dim_source_diversity
        + w_cross_validation * dim_cross_validation
        + w_engagement * dim_engagement
        + w_review_state * dim_review_state
        - w_search_noise * dim_search_noise
        + recency_bonus
    )

    score = max(0, min(100, round(raw * 100)))

    breakdown: dict[str, float | str] = {
        "confidence": round(dim_confidence, 4),
        "authority": round(dim_authority, 4),
        "corroboration": round(dim_corroboration, 4),
        "entity_corroboration": round(dim_entity, 4),
        "entity_corroboration_weight": round(w.get("entity_corroboration", 0.0), 4),
        "recency": round(dim_recency, 4),
        "recency_source": recency_source,
        "source_diversity": round(dim_source_diversity, 4),
        "source_diversity_weight": round(w_source_diversity, 4),
        "cross_validation": round(dim_cross_validation, 4),
        "cross_validation_weight": round(w_cross_validation, 4),
        "engagement": round(dim_engagement, 4),
        "engagement_weight": round(w_engagement, 4),
        "review_state": round(dim_review_state, 4),
        "review_state_weight": round(w_review_state, 4),
        "review_state_label": review_state_label,
        "search_noise_penalty": round(dim_search_noise, 4),
        "search_noise_penalty_weight": round(w_search_noise, 4),
        "recency_bonus": round(dim_recency * w.get("recency_bonus", 0.0), 4),
    }

    return score, breakdown


def rank_items(
    items: list[DataPulseItem],
    *,
    authority_map: dict[str, float] | None = None,
    entity_source_counts: dict[str, int] | None = None,
    now: datetime | None = None,
    weights: dict[str, float] | None = None,
) -> list[DataPulseItem]:
    """Score, rank, and annotate items. Returns items sorted by score descending."""
    if not items:
        return []

    amap = authority_map or {}

    # Build fingerprint counts for corroboration
    fp_counter: Counter[str] = Counter()
    for item in items:
        fp = content_fingerprint(item.content)
        fp_counter[fp] += 1

    fingerprint_counts = dict(fp_counter)

    # Score each item
    for item in items:
        score, breakdown = compute_composite_score(
            item,
            authority_map=amap,
            fingerprint_counts=fingerprint_counts,
            entity_source_counts=entity_source_counts,
            now=now,
            weights=weights,
        )
        item.score = score
        item.extra["score_breakdown"] = breakdown

    # Sort by score descending, then source-native engagement, then confidence.
    items.sort(
        key=lambda it: (
            it.score,
            float(it.extra.get("score_breakdown", {}).get("engagement", 0.0)),
            it.confidence,
        ),
        reverse=True,
    )

    # Assign quality_rank (1-based)
    for rank, item in enumerate(items, 1):
        item.quality_rank = rank

    return items
