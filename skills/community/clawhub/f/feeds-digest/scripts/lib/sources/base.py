"""Base class for all feed sources."""
from __future__ import annotations

from abc import ABC, abstractmethod

import feedparser
import requests

from ..models import FeedItem, SourceResult

USER_AGENT = "feeds-digest/0.1 (+https://github.com/openclaw/openclaw)"
TIMEOUT = 15  # seconds


class FeedSource(ABC):
    """Abstract base for all feed sources."""

    source_type: str = "base"

    def __init__(self, name: str, config: dict):
        self.name = name
        self.topics = config.get("topics", [])
        self.enabled = config.get("enabled", True)

    @abstractmethod
    def fetch(self) -> SourceResult:
        """Fetch items from this source."""
        raise NotImplementedError

    def _http_get(self, url: str) -> bytes | None:
        """HTTP GET with timeout + UA. Returns None on error."""
        try:
            r = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            return r.content
        except requests.RequestException as e:
            raise FetchError(f"HTTP error: {e}") from e

    def _parse(self, content: bytes) -> list[FeedItem]:
        """Parse feed content into FeedItems."""
        parsed = feedparser.parse(content)
        items: list[FeedItem] = []

        for entry in parsed.entries:
            published = _parse_date(entry)
            description = _extract_description(entry)
            link = entry.get("link", "")

            items.append(
                FeedItem(
                    source=self.name,
                    source_type=self.source_type,
                    title=entry.get("title", "").strip(),
                    link=link,
                    published=published,
                    description=description,
                    topics=list(self.topics),
                    guid=entry.get("id", "") or entry.get("guid", "") or link,
                )
            )
        return items


class FetchError(Exception):
    """Raised when a source fetch fails."""


def _parse_date(entry) -> "datetime | None":
    """Extract published date from feed entry."""
    from dateutil import parser as dateparser

    for key in ("published", "updated", "created"):
        raw = entry.get(key)
        if not raw:
            continue
        try:
            return dateparser.parse(raw)
        except (ValueError, TypeError):
            continue
    return None


def _extract_description(entry) -> str:
    """Extract short description from entry."""
    desc = entry.get("summary", "") or entry.get("description", "")
    if not desc:
        return ""
    # Strip HTML tags naively
    import re

    text = re.sub(r"<[^>]+>", "", desc)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 280:
        text = text[:277] + "..."
    return text
