"""B站平台插件 — 核心内置"""

from ..plugin_base import PlatformPlugin, PluginMeta
from typing import Dict, List
import asyncio


class BilibiliPlugin(PlatformPlugin):
    """B站（bilibili.com）平台适配器"""

    @property
    def meta(self) -> PluginMeta:
        return PluginMeta(
            name="bilibili",
            version="3.1.0",
            author="biliyoutik2brain",
            description="B站视频采集（bilibili.com / b23.tv）",
            is_core=True,
        )

    @property
    def domain_regex(self) -> str:
        return r'(bilibili\.com|b23\.tv|BV[1-9]\w+)'

    async def get_video_info(self, url: str) -> Dict:
        from ..platforms.bilibili import BilibiliExtractor
        ext = BilibiliExtractor()
        return ext.get_video_info(url)

    async def download_audio(self, url: str, output_path: str) -> str:
        from ..platforms.bilibili import BilibiliExtractor
        ext = BilibiliExtractor()
        return await ext.download_audio(url, output_path)

    async def download_video(self, url: str, output_path: str) -> str:
        from ..platforms.bilibili import BilibiliExtractor
        ext = BilibiliExtractor()
        return await ext.download_video(url, output_path)

    async def fetch_subtitles(self, url: str) -> List[Dict]:
        from ..platforms.bilibili import BilibiliExtractor
        ext = BilibiliExtractor()
        return await ext.fetch_subtitles(url)

    async def fetch_comments(self, url: str, limit: int = 100) -> List[Dict]:
        from ..platforms.bilibili import BilibiliExtractor
        ext = BilibiliExtractor()
        return await ext.fetch_comments(url, limit=limit)

    def get_anti_crawl_config(self) -> Dict:
        return {
            "ua_pool": [],  # 用通用池
            "cookie_strategy": "browser_extract",
            "cookie_browser": "chrome",
            "proxy_required": False,
            "proxy_ports": [7890, 7897],
            "referer": "https://www.bilibili.com/",
            "prechecks": ["api_412"],
            "heal_actions": ["switch_to_dash_api"],
            "throttle_cooldown": 900,
            "throttle_threshold": 3,
            "rate_limit": 1.0,
            "session_warmup": True,
        }
