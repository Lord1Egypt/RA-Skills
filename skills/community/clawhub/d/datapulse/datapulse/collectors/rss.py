"""RSS feed collector."""

from __future__ import annotations

import feedparser
import requests

from datapulse.core.models import SourceType
from datapulse.core.retry import retry
from datapulse.core.utils import clean_text, generate_excerpt

from .base import BaseCollector, ParseResult

_MAX_ENTRIES = 5


class RssCollector(BaseCollector):
    name = "rss"
    source_type = SourceType.RSS
    reliability = 0.74
    tier = 0
    setup_hint = ""

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "feedparser available", "available": True}

    def can_handle(self, url: str) -> bool:
        lower = url.lower()
        return lower.endswith(".xml") or "/rss" in lower or "/atom" in lower

    def parse(self, url: str) -> ParseResult:
        try:
            raw_content = self._fetch_feed(url)
        except (requests.RequestException, OSError) as exc:
            return ParseResult.failure(url, f"RSS fetch failed: {exc}")

        feed = feedparser.parse(raw_content)
        if feed.bozo and not feed.entries:
            return ParseResult.failure(url, f"Invalid RSS feed: {feed.bozo_exception}")
        source_title = feed.feed.get("title", url)
        if not feed.entries:
            return ParseResult.failure(url, "RSS feed has no entries")

        entries = feed.entries[:_MAX_ENTRIES]
        parts: list[str] = []
        first_link = ""
        first_title = ""
        for i, entry in enumerate(entries):
            entry_title = entry.get("title", "")
            summary = clean_text(entry.get("summary", ""))
            link = entry.get("link", "")
            published = entry.get("published", "")
            if i == 0:
                first_link = link
                first_title = entry_title
            header = f"## {entry_title}" if entry_title else f"## Entry {i + 1}"
            meta = f"*{published}*" if published else ""
            body = summary or "No content available"
            if link:
                parts.append(f"{header}\n{meta}\n{body}\n[Link]({link})")
            else:
                parts.append(f"{header}\n{meta}\n{body}")

        content = "\n\n---\n\n".join(parts)

        return ParseResult(
            url=first_link or url,
            title=f"[{source_title}] {first_title}" if len(entries) == 1
                  else f"[{source_title}] {len(entries)} entries",
            content=content or "No content available",
            author=source_title,
            excerpt=generate_excerpt(content),
            source_type=self.source_type,
            tags=["rss", "feed"],
            confidence_flags=["rss-feed"] + (["multi-entry"] if len(entries) > 1 else ["latest-item"]),
            extra={
                "source_url": url,
                "entry_count": len(entries),
                "published": entries[0].get("published", "") if entries else "",
            },
        )

    @retry(max_attempts=2, base_delay=1.0, retryable=(requests.RequestException,))
    def _fetch_feed(self, url: str) -> str:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "DataPulse/0.2"})
        resp.raise_for_status()
        return str(resp.text)
