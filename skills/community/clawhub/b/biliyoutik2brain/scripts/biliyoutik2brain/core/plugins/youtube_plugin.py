"""YouTube 平台插件 — 核心内置"""

from ..plugin_base import PlatformPlugin, PluginMeta
from typing import Dict, List


class YouTubePlugin(PlatformPlugin):
    """YouTube 平台适配器（youtube.com / youtu.be）"""

    @property
    def meta(self) -> PluginMeta:
        return PluginMeta(
            name="youtube",
            version="3.1.0",
            author="biliyoutik2brain",
            description="YouTube 视频采集（需代理）",
            is_core=True,
        )

    @property
    def domain_regex(self) -> str:
        return r'(youtube\.com|youtu\.be|youtube-nocookie\.com)'

    async def get_video_info(self, url: str) -> Dict:
        from ..platforms.youtube import YouTubeExtractor
        ext = YouTubeExtractor()
        return ext.get_video_info(url)

    async def download_audio(self, url: str, output_path: str) -> str:
        from ..platforms.youtube import YouTubeExtractor
        ext = YouTubeExtractor()
        return await ext.download_audio(url, output_path)

    async def download_video(self, url: str, output_path: str) -> str:
        from ..platforms.youtube import YouTubeExtractor
        ext = YouTubeExtractor()
        return await ext.download_video(url, output_path)

    async def fetch_subtitles(self, url: str) -> List[Dict]:
        from ..platforms.youtube import YouTubeExtractor
        ext = YouTubeExtractor()
        return await ext.fetch_subtitles(url)

    async def fetch_comments(self, url: str, limit: int = 100) -> List[Dict]:
        from ..platforms.youtube import YouTubeExtractor
        ext = YouTubeExtractor()
        return await ext.fetch_comments(url, limit=limit)

    def get_anti_crawl_config(self) -> Dict:
        return {
            "ua_pool": [],
            "cookie_strategy": "browser_extract",
            "cookie_browser": "chrome",
            "proxy_required": True,  # YouTube 必须走代理（国内）
            "proxy_ports": [7890, 7897, 9981, 10809],
            "referer": "https://www.youtube.com/",
            "prechecks": ["proxy_reachable"],
            "heal_actions": ["start_mihomo", "upgrade_ytdlp"],
            "throttle_cooldown": 300,
            "throttle_threshold": 5,
            "rate_limit": 2.0,  # YouTube 限流严格
            "session_warmup": False,
        }
