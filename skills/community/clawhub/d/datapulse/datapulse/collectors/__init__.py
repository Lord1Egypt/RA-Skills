"""Collector exports."""

from .arxiv import ArxivCollector
from .base import BaseCollector, ParseResult
from .bilibili import BilibiliCollector
from .generic import GenericCollector
from .github import GitHubCollector
from .hackernews import HackerNewsCollector
from .jina import JinaCollector
from .native_bridge import NativeBridgeCollector
from .reddit import RedditCollector
from .rss import RssCollector
from .telegram import TelegramCollector
from .trending import TrendingCollector
from .twitter import TwitterCollector
from .wechat import WeChatCollector
from .weibo import WeiboCollector
from .xhs import XiaohongshuCollector
from .youtube import YouTubeCollector

try:
    from .browser import BrowserCollector
except ImportError:
    BrowserCollector = None  # type: ignore[assignment,misc]

__all__ = [
    "BaseCollector",
    "ParseResult",
    "ArxivCollector",
    "TwitterCollector",
    "RedditCollector",
    "YouTubeCollector",
    "BilibiliCollector",
    "RssCollector",
    "TelegramCollector",
    "WeChatCollector",
    "WeiboCollector",
    "XiaohongshuCollector",
    "HackerNewsCollector",
    "GitHubCollector",
    "TrendingCollector",
    "GenericCollector",
    "JinaCollector",
    "NativeBridgeCollector",
    "BrowserCollector",
]
