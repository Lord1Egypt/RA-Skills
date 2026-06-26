"""Filtering logic for feed items."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import FeedItem


def filter_by_date(items: list[FeedItem], since: timedelta, now: datetime | None = None) -> list[FeedItem]:
    """Keep only items published within the last `since` time."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - since

    def _in_range(item: FeedItem) -> bool:
        if item.published is None:
            # No date → keep (can't filter)
            return True
        # Normalize to UTC for comparison
        pub = item.published
        if pub.tzinfo is None:
            pub = pub.replace(tzinfo=timezone.utc)
        return pub >= cutoff

    return [i for i in items if _in_range(i)]


def filter_by_topics(items: list[FeedItem], topics: list[str]) -> list[FeedItem]:
    """Keep only items matching at least one of the given topics.

    A topic matches if it appears in the source's `topics` field.
    """
    if not topics:
        return items

    topics_lower = {t.lower() for t in topics}
    return [i for i in items if topics_lower & {t.lower() for t in i.topics}]


def deduplicate(items: list[FeedItem]) -> list[FeedItem]:
    """Remove duplicates by guid."""
    seen: set[str] = set()
    result: list[FeedItem] = []
    for item in items:
        if item.guid in seen:
            continue
        seen.add(item.guid)
        result.append(item)
    return result


def limit_per_source(items: list[FeedItem], max_per_source: int) -> list[FeedItem]:
    """Limit items per source, keeping newest first."""
    from collections import defaultdict

    by_source: dict[str, list[FeedItem]] = defaultdict(list)
    for item in items:
        by_source[item.source].append(item)

    result: list[FeedItem] = []
    for source, source_items in by_source.items():
        source_items.sort(key=_sort_key, reverse=True)
        result.extend(source_items[:max_per_source])
    return result


def _sort_key(item: FeedItem) -> datetime:
    if item.published is None:
        return datetime.min.replace(tzinfo=timezone.utc)
    pub = item.published
    if pub.tzinfo is None:
        pub = pub.replace(tzinfo=timezone.utc)
    return pub
