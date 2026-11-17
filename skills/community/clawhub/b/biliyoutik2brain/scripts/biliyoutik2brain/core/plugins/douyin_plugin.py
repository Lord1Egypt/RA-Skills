"""抖音平台插件 — 核心内置"""

from ..plugin_base import PlatformPlugin, PluginMeta
from typing import Dict, List


class DouyinPlugin(PlatformPlugin):
    """抖音平台适配器（douyin.com / iesdouyin.com / 分享链接）"""

    @property
    def meta(self) -> PluginMeta:
        return PluginMeta(
            name="douyin",
            version="3.1.0",
            author="biliyoutik2brain",
            description="抖音视频采集（含分享短链解析）",
            is_core=True,
        )

    @property
    def domain_regex(self) -> str:
        return r'(douyin\.com|iesdouyin\.com|v\.douyin\.com)'

    async def get_video_info(self, url: str) -> Dict:
        from ..platforms.douyin import DouyinExtractor
        ext = DouyinExtractor()
        return ext.get_video_info(url)

    async def download_audio(self, url: str, output_path: str) -> str:
        from ..platforms.douyin import DouyinExtractor
        ext = DouyinExtractor()
        return await ext.download_audio(url, output_path)

    async def download_video(self, url: str, output_path: str) -> str:
        from ..platforms.douyin import DouyinExtractor
        ext = DouyinExtractor()
        return await ext.download_video(url, output_path)

    async def fetch_subtitles(self, url: str) -> List[Dict]:
        # 抖音通常无字幕
        return []

    async def fetch_comments(self, url: str, limit: int = 100) -> List[Dict]:
        from ..platforms.douyin import DouyinExtractor
        ext = DouyinExtractor()
        return await ext.fetch_comments(url, limit=limit)

    def get_anti_crawl_config(self) -> Dict:
        return {
            "ua_pool": [],
            "cookie_strategy": "browser_extract",
            "cookie_browser": "chrome",
            "proxy_required": False,
            "proxy_ports": [7890, 7897],
            "referer": "https://www.douyin.com/",
            "prechecks": ["session_warmth", "domain_reachable"],
            "heal_actions": ["rebuild_session", "extract_video_id_fallback"],
            "throttle_cooldown": 900,
            "throttle_threshold": 3,
            "rate_limit": 2.0,
            "session_warmup": True,  # 抖音必须 Session 预热
        }
