"""Confidence and quality scoring helpers."""

from __future__ import annotations

from typing import Iterable

BASE_RELIABILITY = {
    "twitter": 0.92,
    "reddit": 0.9,
    "youtube": 0.9,
    "bilibili": 0.84,
    "telegram": 0.78,
    "wechat": 0.8,
    "xhs": 0.72,
    "rss": 0.74,
    "arxiv": 0.88,
    "hackernews": 0.82,
    "github": 0.82,
    "trending": 0.78,
    "generic": 0.68,
    "jina": 0.72,
    "jina_search": 0.72,
    "manual": 1.0,
}


def compute_confidence(
    parser_name: str,
    *,
    has_title: bool,
    content_length: int,
    has_source: bool,
    has_author: bool,
    media_hint: str = "text",
    extra_flags: Iterable[str] | None = None,
) -> tuple[float, list[str]]:
    """Compute a bounded confidence score and return reasons."""
    reasons: list[str] = []
    score = BASE_RELIABILITY.get(parser_name, 0.62)

    if has_title:
        score += 0.04
        reasons.append("title")
    else:
        score -= 0.03
        reasons.append("no_title")

    if has_source:
        score += 0.03
        reasons.append("source_name")

    if has_author:
        score += 0.02
        reasons.append("author")

    if content_length >= 2500:
        score += 0.08
        reasons.append("long_content")
    elif content_length >= 800:
        score += 0.04
        reasons.append("medium_content")
    elif content_length < 150:
        score -= 0.12
        reasons.append("thin_content")

    if media_hint in {"video", "audio"}:
        score += 0.02
        reasons.append("media")

    for flag in extra_flags or []:
        if flag == "transcript":
            score += 0.04
            reasons.append("transcript")
        elif flag == "comments":
            score += 0.02
            reasons.append("comments")
        elif flag == "thread":
            score += 0.02
            reasons.append("thread")
        elif flag.startswith("lang:"):
            score += 0.01
            reasons.append("language_hint")
        elif flag == "jina":
            score -= 0.03
            reasons.append("proxy_fallback")
        elif flag == "wechat" or flag == "xiaohongshu":
            score += 0.0
            reasons.append(flag)
        elif flag == "css_targeted":
            score += 0.03
            reasons.append("css_targeted")
        elif flag == "image_captioned":
            score += 0.01
            reasons.append("image_captioned")
        elif flag == "search_result":
            score += 0.04
            reasons.append("search_result")
        elif flag == "engagement_metrics":
            score += 0.03
            reasons.append("engagement_metrics")
        elif flag == "high_engagement":
            score += 0.05
            reasons.append("high_engagement")
        elif flag == "low_engagement":
            score -= 0.35
            reasons.append("low_engagement")
        elif flag == "trending_snapshot":
            score += 0.02
            reasons.append("trending_snapshot")
        elif flag == "rich_data":
            score += 0.02
            reasons.append("rich_data")
        elif flag == "fetch_degraded":
            score -= 0.20
            reasons.append("fetch_degraded")

    score = max(0.01, min(0.99, score))
    return round(score, 4), list(dict.fromkeys(reasons))
