"""Bilibili All-in-One Skill - Main Entry Point.

A comprehensive Bilibili toolkit that integrates:
- Hot/trending video monitoring
- Video downloading
- Video watching & stats tracking
- Subtitle downloading & processing
- Video playback & danmaku
- Video uploading & publishing
"""

import asyncio
import json
import sys
from typing import Dict, Any, Optional

from src.auth import BilibiliAuth
from src.hot_monitor import HotMonitor
from src.downloader import BilibiliDownloader
from src.watcher import BilibiliWatcher
from src.subtitle import SubtitleDownloader
from src.player import BilibiliPlayer
from src.publisher import BilibiliPublisher


class BilibiliAllInOne:
    """Unified interface for all Bilibili skill capabilities."""

    def __init__(
        self,
        sessdata: Optional[str] = None,
        bili_jct: Optional[str] = None,
        buvid3: Optional[str] = None,
        credential_file: Optional[str] = None,
        persist: Optional[bool] = None,
    ):
        """Initialize BilibiliAllInOne.

        Args:
            sessdata: Bilibili SESSDATA cookie.
            bili_jct: Bilibili bili_jct (CSRF) cookie.
            buvid3: Bilibili buvid3 cookie.
            credential_file: Path to JSON credential file.
            persist: Whether to persist credentials to disk (default: False).
                Set to True or env BILIBILI_PERSIST=1 to auto-save/load
                credentials from .credentials.json.
        """
        self.auth = BilibiliAuth(
            sessdata=sessdata,
            bili_jct=bili_jct,
            buvid3=buvid3,
            credential_file=credential_file,
            persist=persist,
        )

        # Initialize all modules
        self.hot_monitor = HotMonitor(auth=self.auth)
        self.downloader = BilibiliDownloader(auth=self.auth)
        self.watcher = BilibiliWatcher(auth=self.auth)
        self.player = BilibiliPlayer(auth=self.auth)
        self.subtitle = SubtitleDownloader(
            auth=self.auth,
            downloader=self.downloader,
            player=self.player,
        )
        self._publisher = None  # Lazy init (requires auth)

    @property
    def publisher(self) -> BilibiliPublisher:
        """Get the publisher module (requires authentication).

        Returns:
            BilibiliPublisher instance.

        Raises:
            ValueError: If not authenticated.
        """
        if self._publisher is None:
            self._publisher = BilibiliPublisher(auth=self.auth)
        return self._publisher

    async def execute(self, skill_name: str, action: str, **kwargs) -> Dict[str, Any]:
        """Execute any skill action through a unified interface.

        Args:
            skill_name: Name of the skill module.
            action: Action to perform.
            **kwargs: Additional parameters.

        Returns:
            Action result dict.
        """
        skill_map = {
            "bilibili_hot_monitor": lambda: self.hot_monitor,
            "hot_monitor": lambda: self.hot_monitor,
            "hot": lambda: self.hot_monitor,

            "bilibili_downloader": lambda: self.downloader,
            "downloader": lambda: self.downloader,
            "download": lambda: self.downloader,

            "bilibili_watcher": lambda: self.watcher,
            "watcher": lambda: self.watcher,
            "watch": lambda: self.watcher,

            "bilibili_subtitle": lambda: self.subtitle,
            "subtitle": lambda: self.subtitle,

            "bilibili_player": lambda: self.player,
            "player": lambda: self.player,
            "play": lambda: self.player,

            "bilibili_publisher": lambda: self.publisher,
            "publisher": lambda: self.publisher,
            "publish": lambda: self.publisher,
        }

        skill_factory = skill_map.get(skill_name)
        if not skill_factory:
            return {
                "success": False,
                "message": f"Unknown skill: {skill_name}. Available: {list(skill_map.keys())}",
            }

        skill = skill_factory()

        return await skill.execute(action=action, **kwargs)


async def main():
    """CLI entry point for testing."""
    if len(sys.argv) < 3:
        print("Usage: python main.py <skill_name> <action> [params_json]")
        print()
        print("Skills:")
        print("  hot_monitor   - Monitor hot/trending videos")
        print("  downloader    - Download videos")
        print("  watcher       - Watch and track video stats")
        print("  subtitle      - Download subtitles")
        print("  player        - Play videos and get danmaku")
        print("  publisher     - Upload and publish videos")
        print()
        print("Examples:")
        print('  python main.py hot_monitor get_hot \'{"limit": 5}\'')
        print('  python main.py downloader get_info \'{"url": "BV1xx411c7mD"}\'')
        print('  python main.py subtitle list \'{"url": "BV1xx411c7mD"}\'')
        print('  python main.py player get_danmaku \'{"url": "BV1xx411c7mD"}\'')
    skill_name = sys.argv[1]
    action = sys.argv[2]
    params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}

    app = BilibiliAllInOne()
    result = await app.execute(skill_name=skill_name, action=action, **params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
