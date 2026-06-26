"""Source registry."""
from __future__ import annotations

from .base import FeedSource, FetchError
from .generic_rss import GenericRSSSource
from .github_releases import GitHubReleasesSource
from .ms_techcommunity import MSTechCommunitySource
from .youtube import YouTubeSource

__all__ = [
    "FeedSource",
    "FetchError",
    "GenericRSSSource",
    "GitHubReleasesSource",
    "MSTechCommunitySource",
    "YouTubeSource",
    "build_source",
]

SOURCE_REGISTRY = {
    "youtube": YouTubeSource,
    "ms_techcommunity": MSTechCommunitySource,
    "github_releases": GitHubReleasesSource,
    "generic_rss": GenericRSSSource,
}


def build_source(source_type: str, name: str, config: dict) -> FeedSource | None:
    """Build a source instance by type name."""
    cls = SOURCE_REGISTRY.get(source_type)
    if cls is None:
        return None
    return cls(name, config)
