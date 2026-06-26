"""Data models for feeds-digest."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FeedItem:
    """Single item from a feed source."""

    source: str
    source_type: str
    title: str
    link: str
    published: datetime | None
    description: str = ""
    topics: list[str] = field(default_factory=list)
    guid: str = ""

    def __post_init__(self):
        if not self.guid:
            self.guid = self.link or self.title


@dataclass
class SourceResult:
    """Result of fetching one source."""

    name: str
    source_type: str
    items: list[FeedItem] = field(default_factory=list)
    error: str | None = None
    fetched_at: datetime | None = None

    @property
    def ok(self) -> bool:
        return self.error is None
