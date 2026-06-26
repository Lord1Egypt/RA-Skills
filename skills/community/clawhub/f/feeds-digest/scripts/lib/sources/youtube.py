"""YouTube RSS feed source."""
from __future__ import annotations

from datetime import datetime

from ..models import FeedItem, SourceResult
from .base import FeedSource, FetchError


class YouTubeSource(FeedSource):
    source_type = "youtube"

    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.channel_id = config.get("channel_id", "")

    def fetch(self) -> SourceResult:
        if not self.channel_id or self.channel_id == "REPLACE_ME":
            return SourceResult(
                name=self.name,
                source_type=self.source_type,
                error="channel_id fehlt oder ist REPLACE_ME",
            )

        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={self.channel_id}"
        try:
            content = self._http_get(url)
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
