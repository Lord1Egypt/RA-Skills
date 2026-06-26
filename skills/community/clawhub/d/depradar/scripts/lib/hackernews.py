"""Hacker News backend for /depradar.

Uses HN Algolia search API.  The Algolia indexer was archived in Feb 2026 so
new stories are no longer indexed there, but pre-2026 content is still
searchable — useful for packages whose breaking changes landed before that date.
Falls back gracefully (returns empty list) when Algolia is unreachable.
No authentication required.
"""
from __future__ import annotations

import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).parent))
import importlib.util as _ilu
if "_depradar_http" not in sys.modules:
    _http_spec = _ilu.spec_from_file_location("_depradar_http", str(Path(__file__).parent / "http.py"))
    _http_mod = _ilu.module_from_spec(_http_spec)   # type: ignore[arg-type]
    sys.modules["_depradar_http"] = _http_mod
    _http_spec.loader.exec_module(_http_mod)         # type: ignore[union-attr]
_http_mod = sys.modules["_depradar_http"]
get_json  = _http_mod.get_json
HttpError = _http_mod.HttpError
from schema import HackerNewsItem, SubScores
from dates import recency_score, days_ago
import cache


HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"
HN_FIREBASE_ITEM = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
HN_ITEM_URL = "https://news.ycombinator.com/item?id={id}"

DEPTH_CONFIG = {
    "quick":   {"hits_per_page": 5,  "max_results": 5},
    "default": {"hits_per_page": 15, "max_results": 10},
    "deep":    {"hits_per_page": 30, "max_results": 20},
}

# Keywords to narrow to breaking-change relevant discussions
_BREAKING_TERMS = ["breaking change", "breaking", "migration", "deprecated", "removed"]


def search_hackernews(
    packages: List[str],
    days: int = 30,
    depth: str = "default",
) -> List[HackerNewsItem]:
    """Search HN for discussions about package breaking changes."""
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    max_results: int = cfg["max_results"]

    since_date = days_ago(days)
    from_ts = int(
        datetime.strptime(since_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
    )

    all_items: List[HackerNewsItem] = []
    for package in packages:
        try:
            items = _search_package(package, from_ts, depth)
            all_items.extend(items)
        except Exception:
            pass

    # Dedupe by hn_url
    seen: set = set()
    deduped: List[HackerNewsItem] = []
    for item in all_items:
        if item.hn_url not in seen:
            seen.add(item.hn_url)
            deduped.append(item)

    deduped.sort(key=lambda x: x.score, reverse=True)
    deduped = deduped[:max_results * len(packages)]

    # Reassign sequential IDs
    for i, item in enumerate(deduped, 1):
        item.id = f"HN{i}"

    return deduped


def _search_package(
    package: str,
    from_timestamp: int,
    depth: str,
) -> List[HackerNewsItem]:
    """Search one package. Returns HackerNewsItem list."""
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    hits_per_page: int = cfg["hits_per_page"]
    max_results: int = cfg["max_results"]

    cache_key = cache.cache_key("hn", package, from_timestamp, depth)
    cached = cache.load(cache_key, ttl_hours=cache.COMMUNITY_TTL_HOURS, namespace="hackernews")
    if cached is not None:
        return [HackerNewsItem.from_dict(d) for d in cached]

    query = f"{package} breaking change"
    params = {
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{from_timestamp}",
        "hitsPerPage": hits_per_page,
    }

    items: List[HackerNewsItem] = []

    try:
        data = get_json(HN_ALGOLIA_URL, params=params, timeout=10)
        hits = data.get("hits", [])
        if not isinstance(hits, list):
            hits = []
    except HttpError:
        # Algolia unavailable or archived — degrade gracefully, return empty
        hits = []
    except Exception:
        hits = []

    # Algolia data may be stale (indexer archived Feb 2026). For any hits found,
    # fetch fresh vote/comment counts from the live Firebase HN API.
    if hits:
        hits = _enrich_hits_from_firebase(hits)

    for idx, hit in enumerate(hits[:max_results], 1):
        parsed = _parse_hn_hit(hit, package, idx)
        if parsed is not None:
            parsed = _score_hn_item(parsed)
            items.append(parsed)

    cache.save(cache_key, [it.to_dict() for it in items], namespace="hackernews")
    return items


def _enrich_hits_from_firebase(hits: list) -> list:
    """Fetch fresh vote/comment counts from the Firebase HN API for each hit.

    The Algolia index was archived in Feb 2026, so points/num_comments stored
    there may be stale. Firebase is the authoritative live HN data source.
    Falls back to the Algolia values if Firebase is unreachable or returns
    no data for a given story ID.
    """
    enriched = []
    for hit in hits:
        object_id = hit.get("objectID", "")
        if not object_id:
            enriched.append(hit)
            continue
        url = HN_FIREBASE_ITEM.format(id=object_id)
        try:
            fb_data = get_json(url, timeout=5)
            if fb_data and isinstance(fb_data, dict):
                hit = dict(hit)  # shallow copy — don't mutate original
                # Firebase uses "score" for upvotes and "descendants" for comments
                hit["points"]       = fb_data.get("score",       hit.get("points", 0))
                hit["num_comments"] = fb_data.get("descendants", hit.get("num_comments", 0))
        except Exception:
            pass  # Firebase unreachable — keep Algolia values
        enriched.append(hit)
    return enriched


def _parse_hn_hit(hit: dict, package: str, idx: int) -> Optional[HackerNewsItem]:
    """Parse one Algolia hit into HackerNewsItem."""
    object_id = hit.get("objectID", "")
    if not object_id:
        return None

    title = hit.get("title") or hit.get("story_title") or ""
    if not title:
        return None

    hn_url = HN_ITEM_URL.format(id=object_id)
    story_url = hit.get("url")  # Can be None for Ask HN etc.

    points = int(hit.get("points") or 0)
    num_comments = int(hit.get("num_comments") or 0)

    # Parse date from created_at_i (Unix timestamp) or created_at string
    date: Optional[str] = None
    created_ts = hit.get("created_at_i")
    if created_ts:
        try:
            date = datetime.fromtimestamp(int(created_ts), tz=timezone.utc).strftime("%Y-%m-%d")
        except Exception:
            pass
    if not date:
        created_str = hit.get("created_at", "")
        if created_str:
            date = created_str[:10]

    # Quick relevance filter: must mention the package in title or
    # contain a breaking-change keyword
    title_lower = title.lower()
    pkg_lower = package.lower()
    has_pkg = pkg_lower in title_lower
    has_term = any(t in title_lower for t in _BREAKING_TERMS)
    if not (has_pkg or has_term):
        return None

    return HackerNewsItem(
        id=f"HN{idx}",
        package=package,
        title=title,
        url=story_url,
        hn_url=hn_url,
        points=points,
        num_comments=num_comments,
        top_comment=None,
        date=date,
        date_confidence="high",
        subs=SubScores(),
        score=0,
        cross_refs=[],
    )


def _score_hn_item(item: HackerNewsItem) -> HackerNewsItem:
    """Score: 0.55*log1p(points)*10 + 0.45*log1p(num_comments)*12, cap at 100."""
    points_part = 0.55 * math.log1p(item.points) * 10
    comments_part = 0.45 * math.log1p(item.num_comments) * 12

    raw_score = points_part + comments_part
    final_score = min(100, int(round(raw_score)))

    recency = recency_score(item.date)

    item.subs = SubScores(
        severity=0,
        recency=recency,
        impact=0,
        community=final_score,
    )
    item.score = final_score
    return item
