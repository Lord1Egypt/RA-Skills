"""Generic RSS/Atom feed source."""
from __future__ import annotations

from datetime import datetime

from ..models import SourceResult
from .base import FeedSource, FetchError


class GenericRSSSource(FeedSource):
    source_type = "generic_rss"

    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.url = config.get("url", "")

    def fetch(self) -> SourceResult:
        if not self.url:
            return SourceResult(
                name=self.name,
                source_type=self.source_type,
                error="url fehlt",
            )

        try:
            content = self._http_get(self.url)
            items = self._parse(content) if content else []
        except FetchError as e:
            return SourceResult(
                name=self.name,
                source_type=self.source_type,
                error=str(e),
            )

        return SourceResult(
            name=self.name,
            source_type=self.source_type,
            items=items,
            fetched_at=datetime.utcnow(),
        )
