"""X/Twitter backend for /depradar via xAI Grok API.

Optional — gracefully skipped if no credentials.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlencode
import urllib.request

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
from schema import TwitterItem, SubScores
from dates import recency_score, days_ago
import cache


XAI_API_URL = "https://api.x.ai/v1/chat/completions"

DEPTH_CONFIG = {
    "quick":   {"max_results": 3},
    "default": {"max_results": 8},
    "deep":    {"max_results": 15},
}

# ── Security ──────────────────────────────────────────────────────────────────

def _sanitize_package_name(name: str) -> str:
    """Sanitize a package name before interpolating into an LLM prompt.

    Keeps only characters valid in package names (alphanumeric, hyphens,
    underscores, dots, @, /) and truncates to 100 chars to prevent prompt
    injection via maliciously crafted package names.
    """
    import re as _re
    sanitized = _re.sub(r"[^a-zA-Z0-9\-_@/.]", "", name)
    return sanitized[:100]


def search_twitter(
    packages: List[str],
    days: int = 30,
    depth: str = "default",
    xai_api_key: Optional[str] = None,
    auth_token: Optional[str] = None,
    ct0: Optional[str] = None,
) -> List[TwitterItem]:
    """Search X/Twitter for breaking change tweets about the packages.

    Uses xAI Grok API if xai_api_key provided.
    Falls back to empty list gracefully if no credentials.
    """
    if not xai_api_key:
        return []

    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    max_results: int = cfg["max_results"]

    all_items: List[TwitterItem] = []

    for package in packages:
        cache_key = cache.cache_key("twitter", package, days, depth)
        cached = cache.load(cache_key, ttl_hours=cache.COMMUNITY_TTL_HOURS, namespace="twitter")
        if cached is not None:
            all_items.extend(TwitterItem.from_dict(d) for d in cached)
            continue

        try:
            items = _search_via_grok(package, days, xai_api_key)
            items = items[:max_results]
        except Exception:
            items = []

        # Mark all items as LLM-sourced (not live search) so renderers can note this
        for item in items:
            if item.url and not item.url.startswith("https://x.com"):
                item.url = None   # discard fabricated URLs

        # Score items
        scored: List[TwitterItem] = []
        for i, item in enumerate(items, 1):
            item.id = f"TW{len(all_items) + i}"
            item = _score_twitter_item(item)
            scored.append(item)

        cache.save(cache_key, [it.to_dict() for it in scored], namespace="twitter")
        all_items.extend(scored)

    # Dedupe by url
    seen: set = set()
    deduped: List[TwitterItem] = []
    for item in all_items:
        key = item.url or item.text[:80]
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    deduped.sort(key=lambda x: x.score, reverse=True)

    # Reassign sequential IDs
    for i, item in enumerate(deduped, 1):
        item.id = f"TW{i}"

    return deduped


def _search_via_grok(
    package: str, days: int, api_key: str
) -> List[TwitterItem]:
    """Use xAI Grok to search for recent tweets about the package breaking changes.

    NOTE: Grok is an LLM, not a live search engine. Results reflect tweets Grok
    was trained on (knowledge cutoff applies). Engagement metrics may be
    approximate. Results are flagged as synthesized in the output.
    """
    since_date = days_ago(days)
    # Sanitize package name to prevent prompt injection
    safe_package = _sanitize_package_name(package)
    if not safe_package:
        return []

    system_prompt = (
        "You are a technical researcher with knowledge of developer communities. "
        "Based on your training data, recall real tweets or posts from X/Twitter "
        "by developers mentioning breaking changes, migration issues, or deprecated APIs "
        "for the given package. "
        "Return results as a JSON array of objects with these fields: "
        "text (string), author_handle (string), likes (int), reposts (int), "
        "replies (int), date (YYYY-MM-DD string), url (string or null). "
        "Only include content you have high confidence actually existed. "
        "Return an empty array if nothing relevant is found in your training data."
    )
    user_prompt = (
        f"Recall developer tweets or posts since {since_date} about breaking changes "
        f"or API removals for the '{safe_package}' package/library. "
        "Return JSON array only. Return [] if unsure."
    )

    payload = json.dumps({
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 2000,
    }).encode("utf-8")

    req = urllib.request.Request(
        XAI_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            response = json.loads(raw)
    except Exception as exc:
        raise HttpError(XAI_API_URL, 0, str(exc)) from exc

    # Extract the content from Grok's response
    content = (
        response.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )

    # Parse JSON from content — Grok may wrap it in markdown
    tweet_data = _extract_json_array(content)
    if not isinstance(tweet_data, list):
        return []

    items: List[TwitterItem] = []
    for idx, entry in enumerate(tweet_data, 1):
        if not isinstance(entry, dict):
            continue
        text = entry.get("text", "")
        if not text:
            continue
        items.append(TwitterItem(
            id=f"TW{idx}",
            package=package,
            text=text,
            author_handle=entry.get("author_handle", "unknown"),
            likes=int(entry.get("likes", 0) or 0),
            reposts=int(entry.get("reposts", 0) or 0),
            replies=int(entry.get("replies", 0) or 0),
            date=entry.get("date"),
            url=entry.get("url"),
            subs=SubScores(),
            score=0,
            cross_refs=[],
        ))

    return items


def _extract_json_array(text: str) -> list:
    """Extract a JSON array from text that may contain markdown fences."""
    import re
    # Strip markdown code fences
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    # Find first [ ... ]
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        return json.loads(text[start:end + 1])
    except (json.JSONDecodeError, ValueError):
        return []


def _score_twitter_item(item: TwitterItem) -> TwitterItem:
    """Score based on engagement: likes, reposts, replies, recency."""
    engagement = item.likes + item.reposts * 2 + item.replies
    engagement_score = min(100, int(round(math.log1p(engagement) * 15)))

    recency = recency_score(item.date)

    raw_score = 0.60 * engagement_score + 0.40 * recency
    final_score = min(100, int(round(raw_score)))

    item.subs = SubScores(
        severity=0,
        recency=recency,
        impact=0,
        community=engagement_score,
    )
    item.score = final_score
    return item
