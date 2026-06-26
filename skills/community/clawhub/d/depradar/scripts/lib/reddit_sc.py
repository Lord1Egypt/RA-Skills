"""Reddit backend for /depradar via ScrapeCreators API.

Searches relevant developer subreddits for breaking change pain reports.
Requires SCRAPECREATORS_API_KEY.
"""
from __future__ import annotations

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
from schema import RedditItem, SubScores
from dates import recency_score, days_ago
import cache


SCRAPECREATORS_BASE = "https://api.scrapecreators.com/v1/reddit"

# Most relevant subreddits per ecosystem
ECOSYSTEM_SUBREDDITS = {
    "npm":   ["node", "javascript", "typescript", "reactjs", "webdev", "programming"],
    "pypi":  ["Python", "django", "flask", "learnpython", "programming"],
    "cargo": ["rust", "programming"],
    "maven": ["java", "programming", "androiddev"],
    "gem":   ["ruby", "rails", "programming"],
    "go":    ["golang", "programming"],
    "all":   ["programming", "softwaredevelopment"],
}

DEPTH_CONFIG = {
    "quick":   {"subreddits": 1, "results_per_sub": 3, "max_results": 5},
    "default": {"subreddits": 2, "results_per_sub": 5, "max_results": 10},
    "deep":    {"subreddits": 4, "results_per_sub": 8, "max_results": 20},
}


def search_reddit(
    packages: List[str],
    ecosystem: str = "all",
    days: int = 30,
    depth: str = "default",
    token: Optional[str] = None,
) -> List[RedditItem]:
    """Search Reddit for breaking change discussions about the given packages."""
    if not token:
        return []

    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    subreddits_count: int = cfg["subreddits"]
    results_per_sub: int = cfg["results_per_sub"]
    max_results: int = cfg["max_results"]

    # Resolve subreddits for the ecosystem
    subreddit_list = ECOSYSTEM_SUBREDDITS.get(ecosystem, ECOSYSTEM_SUBREDDITS["all"])
    subreddits = subreddit_list[:subreddits_count]

    all_items: List[RedditItem] = []

    for package in packages:
        for subreddit in subreddits:
            if len(all_items) >= max_results * len(packages):
                break
            try:
                items = _search_package_subreddit(
                    package, subreddit, days, token, results_per_sub
                )
                all_items.extend(items)
            except Exception:
                pass

    # Dedupe by URL
    seen: set = set()
    deduped: List[RedditItem] = []
    for item in all_items:
        if item.url not in seen:
            seen.add(item.url)
            deduped.append(item)

    deduped.sort(key=lambda x: x.score, reverse=True)
    deduped = deduped[:max_results * len(packages)]

    # Reassign sequential IDs
    for i, item in enumerate(deduped, 1):
        item.id = f"RI{i}"

    return deduped


def _search_package_subreddit(
    package: str,
    subreddit: str,
    days: int,
    token: str,
    max_results: int,
) -> List[RedditItem]:
    """Search one subreddit for a package's breaking change mentions."""
    cache_key = cache.cache_key("reddit", package, subreddit, days, max_results)
    cached = cache.load(cache_key, ttl_hours=cache.COMMUNITY_TTL_HOURS, namespace="reddit")
    if cached is not None:
        return [RedditItem.from_dict(d) for d in cached]

    since_date = days_ago(days)
    query = f"{package} breaking change"

    url = f"{SCRAPECREATORS_BASE}/search"
    params: Dict = {
        "query": query,
        "subreddit": subreddit,
        "after": since_date,
        "limit": max_results,
        "sort": "relevance",
    }
    headers = {
        "x-api-key": token,
        "Accept": "application/json",
    }

    try:
        data = get_json(url, headers=headers, params=params)
    except RateLimitError:
        return []
    except HttpError:
        return []

    posts = data if isinstance(data, list) else data.get("posts", data.get("data", []))

    items: List[RedditItem] = []
    for idx, raw in enumerate(posts[:max_results], 1):
        item = _parse_reddit_post(raw, package, subreddit, idx)
        item = _score_reddit_item(item)
        items.append(item)

    cache.save(cache_key, [it.to_dict() for it in items], namespace="reddit")
    return items


def _parse_reddit_post(raw: dict, package: str, subreddit: str, idx: int) -> RedditItem:
    """Convert raw ScrapeCreators Reddit post to RedditItem."""
    # ScrapeCreators may return different field names; handle variations
    title = raw.get("title", raw.get("name", ""))
    url = raw.get("url", raw.get("permalink", raw.get("link", "")))
    if url and url.startswith("/r/"):
        url = f"https://www.reddit.com{url}"

    reddit_score = int(raw.get("score", raw.get("ups", raw.get("upvotes", 0))) or 0)
    num_comments = int(raw.get("num_comments", raw.get("comments", 0)) or 0)

    # Date field variations
    date: Optional[str] = None
    date_confidence = "low"
    created = raw.get("created_utc", raw.get("created", raw.get("date")))
    if created:
        try:
            if isinstance(created, (int, float)):
                from datetime import datetime, timezone
                date = datetime.fromtimestamp(float(created), tz=timezone.utc).strftime("%Y-%m-%d")
                date_confidence = "high"
            elif isinstance(created, str) and len(created) >= 10:
                date = created[:10]
                date_confidence = "med"
        except Exception:
            pass

    # Top comment
    top_comment: Optional[str] = None
    comments_list = raw.get("comments", [])
    if isinstance(comments_list, list) and comments_list:
        first = comments_list[0]
        if isinstance(first, dict):
            body = first.get("body", first.get("text", ""))
            if body:
                top_comment = body[:300].strip()

    detected_sub = raw.get("subreddit", subreddit)

    return RedditItem(
        id=f"RI{idx}",
        package=package,
        subreddit=detected_sub,
        title=title,
        url=url,
        reddit_score=reddit_score,
        num_comments=num_comments,
        top_comment=top_comment,
        date=date,
        date_confidence=date_confidence,
        subs=SubScores(),
        score=0,
        cross_refs=[],
    )


def _score_reddit_item(item: RedditItem) -> RedditItem:
    """Scoring:
    0.50*log1p(reddit_score) + 0.35*log1p(num_comments) + 0.15*recency
    Scale to 0-100.
    """
    import math

    score_part = 0.50 * math.log1p(max(0, item.reddit_score))
    comment_part = 0.35 * math.log1p(item.num_comments)
    recency = recency_score(item.date)
    recency_part = 0.15 * recency

    # Raw combination — log1p(10000) ~ 9.2, so max raw ≈ 0.50*9.2 + 0.35*9.2 + 0.15*100 = 4.6+3.2+15 = 22.8
    # Scale to 0-100: multiply by ~4.4
    raw = score_part + comment_part + recency_part
    final_score = min(100, int(round(raw * 4.4)))

    item.subs = SubScores(
        severity=0,
        recency=recency,
        impact=0,
        community=min(100, int(round((score_part + comment_part) * 10))),
    )
    item.score = final_score
    return item
