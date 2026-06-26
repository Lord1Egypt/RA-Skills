"""GitHub Releases Atom feed source."""
from __future__ import annotations

from datetime import datetime

from ..models import SourceResult
from .base import FeedSource, FetchError


class GitHubReleasesSource(FeedSource):
    source_type = "github_releases"

    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.repo = config.get("repo", "")

    def fetch(self) -> SourceResult:
        if not self.repo or "/" not in self.repo:
            return SourceResult(
                name=self.name,
                source_type=self.source_type,
                error="repo muss im Format 'owner/repo' sein",
            )

        url = f"https://github.com/{self.repo}/releases.atom"
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
