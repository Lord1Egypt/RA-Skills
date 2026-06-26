"""Stack Overflow API backend for /depradar.

API: https://api.stackexchange.com/2.3/search/advanced
Free: 300 req/day without key, 10000/day with STACKOVERFLOW_API_KEY.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
import importlib.util as _ilu
if "_depradar_http" not in sys.modules:
    _http_spec = _ilu.spec_from_file_location("_depradar_http", str(Path(__file__).parent / "http.py"))
    _http_mod = _ilu.module_from_spec(_http_spec)   # type: ignore[arg-type]
    sys.modules["_depradar_http"] = _http_mod
    _http_spec.loader.exec_module(_http_mod)         # type: ignore[union-attr]
_http_mod = sys.modules["_depradar_http"]
get_json       = _http_mod.get_json
RateLimitError = _http_mod.RateLimitError
HttpError      = _http_mod.HttpError
from schema import StackOverflowItem, SubScores
from dates import recency_score, days_ago
import cache


SO_API_URL = "https://api.stackexchange.com/2.3/search/advanced"

DEPTH_CONFIG = {
    "quick":   {"max_results": 3},
    "default": {"max_results": 8},
    "deep":    {"max_results": 15},
}

# Ecosystem-specific query terms yield more precise results with less noise.
# Each template is tried in order until max_results is reached.
_QUERY_TERMS_BY_ECOSYSTEM: Dict[str, List[str]] = {
    "npm": [
        "{package} breaking change javascript",
        "{package} migration import error",
        "{package} deprecated api removed node",
    ],
    "pypi": [
        "{package} breaking change python",
        "{package} migration import AttributeError",
        "{package} deprecated removed pip",
    ],
    "cargo": [
        "{package} breaking change rust",
        "{package} migration error cargo",
    ],
    "maven": [
        "{package} breaking change java",
        "{package} migration dependency maven",
    ],
    "gem": [
        "{package} breaking change ruby",
        "{package} migration deprecated gem",
    ],
    "go": [
        "{package} breaking change golang",
        "{package} migration error go module",
    ],
}
_QUERY_TERMS_DEFAULT = [
    "{package} breaking change",
    "{package} migration error",
    "{package} deprecated removed",
]


def search_stackoverflow(
    packages: List[str],
    days: int = 30,
    depth: str = "default",
    api_key: Optional[str] = None,
    ecosystem: str = "default",
) -> List[StackOverflowItem]:
    """Search Stack Overflow for each package's breaking change questions."""
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    max_results: int = cfg["max_results"]
    query_terms = _QUERY_TERMS_BY_ECOSYSTEM.get(ecosystem, _QUERY_TERMS_DEFAULT)

    all_items: List[StackOverflowItem] = []
    for package in packages:
        try:
            items = _search_package(package, days, api_key, max_results, query_terms, ecosystem)
            all_items.extend(items)
        except Exception:
            pass

    # Dedupe by URL
    seen: set = set()
    deduped: List[StackOverflowItem] = []
    for item in all_items:
        if item.question_url not in seen:
            seen.add(item.question_url)
            deduped.append(item)

    deduped.sort(key=lambda x: x.score, reverse=True)
    return deduped


def _search_package(
    package: str,
    days: int,
    api_key: Optional[str],
    max_results: int,
    query_terms: Optional[List[str]] = None,
    ecosystem: str = "default",
) -> List[StackOverflowItem]:
    """Search SO for a single package. Tries multiple query terms."""
    if query_terms is None:
        query_terms = _QUERY_TERMS_DEFAULT

    # Include ecosystem in cache key so npm "requests" and pypi "requests" don't collide.
    cache_key = cache.cache_key("so", package, days, max_results, ecosystem, str(query_terms[:1]))
    cached = cache.load(cache_key, ttl_hours=cache.COMMUNITY_TTL_HOURS, namespace="stackoverflow")
    if cached is not None:
        return [StackOverflowItem.from_dict(d) for d in cached]

    from_date_str = days_ago(days)
    # Convert YYYY-MM-DD to Unix timestamp
    from datetime import datetime, timezone
    from_ts = int(datetime.strptime(from_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())

    seen_urls: set = set()
    items: List[StackOverflowItem] = []

    for term_template in query_terms:
        if len(items) >= max_results:
            break
        query = term_template.format(package=package)
        params: Dict = {
            "q": query,
            "site": "stackoverflow",
            "sort": "creation",
            "order": "desc",
            "fromdate": from_ts,
            "pagesize": max_results,
            "filter": "withbody",
        }
        if api_key:
            params["key"] = api_key

        try:
            data = get_json(SO_API_URL, params=params)
        except RateLimitError:
            break
        except HttpError:
            continue

        for idx, raw in enumerate(data.get("items", [])):
            url = raw.get("link", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            item = _parse_question(raw, package, len(items) + 1)
            item = _score_so_item(item)
            items.append(item)
            if len(items) >= max_results:
                break

    # Reassign IDs
    for i, item in enumerate(items, 1):
        item.id = f"SO{i}"

    cache.save(cache_key, [it.to_dict() for it in items], namespace="stackoverflow")
    return items


def _parse_question(raw: dict, package: str, idx: int) -> StackOverflowItem:
    """Convert raw SO API question to StackOverflowItem."""
    # Stack Overflow API returns creation_date as Unix timestamp
    created_at: Optional[str] = None
    creation_ts = raw.get("creation_date")
    if creation_ts:
        from datetime import datetime, timezone
        created_at = datetime.fromtimestamp(creation_ts, tz=timezone.utc).strftime("%Y-%m-%d")

    # Extract accepted answer snippet from body if present
    body = raw.get("body", "") or ""
    accepted_snippet: Optional[str] = None
    if raw.get("is_answered") and body:
        accepted_snippet = body[:300].strip()

    return StackOverflowItem(
        id=f"SO{idx}",
        package=package,
        question_title=raw.get("title", ""),
        question_url=raw.get("link", ""),
        answer_count=raw.get("answer_count", 0),
        is_answered=bool(raw.get("is_answered", False)),
        accepted_answer_snippet=accepted_snippet,
        tags=raw.get("tags", []),
        view_count=raw.get("view_count", 0),
        so_score=raw.get("score", 0),
        created_at=created_at,
        subs=SubScores(),
        score=0,
        cross_refs=[],
    )


def _score_so_item(item: StackOverflowItem) -> StackOverflowItem:
    """Score formula:
    0.40*log1p(so_score)*12 + 0.30*log1p(answer_count)*20
    + 0.20*log1p(view_count/100)*15 + 0.10*recency
    Cap at 100.
    """
    score_component = 0.40 * math.log1p(max(0, item.so_score)) * 12
    answer_component = 0.30 * math.log1p(item.answer_count) * 20
    view_component = 0.20 * math.log1p(item.view_count / 100.0) * 15
    recency = recency_score(item.created_at)
    recency_component = 0.10 * recency

    raw_score = score_component + answer_component + view_component + recency_component
    final_score = min(100, int(round(raw_score)))

    item.subs = SubScores(
        severity=0,
        recency=recency,
        impact=min(100, int(round(score_component / 0.40))),
        community=min(100, int(round((answer_component + view_component) / 0.50))),
    )
    item.score = final_score
    return item
