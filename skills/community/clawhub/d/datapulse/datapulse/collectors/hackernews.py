"""Hacker News collector via Firebase API."""

from __future__ import annotations

import re

import requests

from datapulse.core.models import SourceType
from datapulse.core.retry import retry
from datapulse.core.utils import generate_excerpt

from .base import BaseCollector, ParseResult

_HN_ITEM_PATTERN = re.compile(r"[?&]id=(\d+)")


def extract_hn_id(url: str) -> str | None:
    """Extract HN item ID from URL."""
    m = _HN_ITEM_PATTERN.search(url)
    if m:
        return m.group(1)
    return None


class HackerNewsCollector(BaseCollector):
    name = "hackernews"
    source_type = SourceType.HACKERNEWS
    reliability = 0.82
    tier = 0
    setup_hint = ""

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "requests available", "available": True}

    def can_handle(self, url: str) -> bool:
        return "news.ycombinator.com" in url.lower()

    def parse(self, url: str) -> ParseResult:
        hn_id = extract_hn_id(url)
        if not hn_id:
            return ParseResult.failure(url, "Could not extract HN item ID")

        try:
            data = self._fetch_item(hn_id)
        except requests.RequestException as exc:
            return ParseResult.failure(url, f"HN API fetch failed: {exc}")

        if not data or data.get("dead") or data.get("deleted"):
            return ParseResult.failure(url, "HN item not found or deleted")

        title = data.get("title", "")
        text = data.get("text", "")
        linked_url = data.get("url", "")
        author = data.get("by", "")
        score = data.get("score", 0)
        descendants = data.get("descendants", 0)
        item_type = data.get("type", "story")
        timestamp = data.get("time", 0)

        # Build content
        parts = []
        if title:
            parts.append(f"**{title}**")
        if linked_url:
            parts.append(f"Link: {linked_url}")
        if text:
            parts.append(text)
        parts.append(f"Score: {score} | Comments: {descendants}")

        content = "\n\n".join(parts)

        # Dynamic confidence flags
        flags: list[str] = ["hn_api"]
        if score >= 100:
            flags.append("high_engagement")
        if descendants >= 50:
            flags.append("comments")

        tags = ["hackernews", item_type]

        return ParseResult(
            url=url,
            title=title or f"HN #{hn_id}",
            content=content,
            author=author,
            excerpt=generate_excerpt(content),
            source_type=self.source_type,
            tags=tags,
            confidence_flags=flags,
            extra={
                "hn_id": hn_id,
                "hn_score": score,
                "hn_comments": descendants,
                "linked_url": linked_url,
                "hn_type": item_type,
                "hn_time": timestamp,
            },
        )

    @retry(max_attempts=2, retryable=(requests.RequestException,))
    def _fetch_item(self, hn_id: str) -> dict:
        resp = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{hn_id}.json",
            timeout=15,
            headers={"User-Agent": "DataPulse/0.4"},
        )
        resp.raise_for_status()
        return resp.json()
