"""小红书平台插件 — 核心内置"""

from ..plugin_base import PlatformPlugin, PluginMeta
from typing import Dict, List


class XiaohongshuPlugin(PlatformPlugin):
    """小红书平台适配器（xiaohongshu.com / xhslink.com）"""

    @property
    def meta(self) -> PluginMeta:
        return PluginMeta(
            name="xiaohongshu",
            version="3.1.0",
            author="biliyoutik2brain",
            description="小红书视频采集（需 yt-dlp >= 2026.6.9）",
            is_core=True,
        )

    @property
    def domain_regex(self) -> str:
        return r'(xiaohongshu\.com|xhslink\.com)'

    async def get_video_info(self, url: str) -> Dict:
        from ..platforms.xiaohongshu import XiaohongshuExtractor
        ext = XiaohongshuExtractor()
        return ext.get_video_info(url)

    async def download_audio(self, url: str, output_path: str) -> str:
        from ..platforms.xiaohongshu import XiaohongshuExtractor
        ext = XiaohongshuExtractor()
        return await ext.download_audio(url, output_path)

    async def download_video(self, url: str, output_path: str) -> str:
        from ..platforms.xiaohongshu import XiaohongshuExtractor
        ext = XiaohongshuExtractor()
        return await ext.download_video(url, output_path)

    async def fetch_subtitles(self, url: str) -> List[Dict]:
        # 小红书通常无字幕
        return []

    async def fetch_comments(self, url: str, limit: int = 100) -> List[Dict]:
        from ..platforms.xiaohongshu import XiaohongshuExtractor
        ext = XiaohongshuExtractor()
        return await ext.fetch_comments(url, limit=limit)

    def get_anti_crawl_config(self) -> Dict:
        return {
            "ua_pool": [],
            "cookie_strategy": "browser_extract",
            "cookie_browser": "chrome",
            "proxy_required": False,
            "proxy_ports": [7890, 7897],
            "referer": "https://www.xiaohongshu.com/",
            "prechecks": ["ytdlp_version"],
            "heal_actions": ["upgrade_ytdlp"],
            "throttle_cooldown": 600,
            "throttle_threshold": 3,
            "rate_limit": 3.0,  # 小红书限流最严格
            "session_warmup": False,
        }
