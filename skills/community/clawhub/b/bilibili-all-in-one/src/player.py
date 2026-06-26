"""Bilibili video playback and danmaku module."""

import asyncio
from typing import Optional, Dict, Any, List

import httpx

from .auth import BilibiliAuth
from .utils import (
    API_VIDEO_INFO,
    API_PLAY_URL,
    API_DANMAKU,
    QUALITY_MAP,
    DEFAULT_HEADERS,
    extract_bvid,
    format_duration,
    format_number,
)


class BilibiliPlayer:
    """Play Bilibili videos with danmaku (bullet comments) support.

    Provides playback URLs, danmaku retrieval, and playlist management.
    """

    def __init__(self, auth: Optional[BilibiliAuth] = None):
        """Initialize BilibiliPlayer.

        Args:
            auth: Optional BilibiliAuth instance for authenticated requests.
        """
        self.auth = auth

    def _get_client(self) -> httpx.AsyncClient:
        """Get an HTTP client, using auth if available."""
        if self.auth:
            return self.auth.get_client()
        return httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True,
        )

    async def play(self, url: str, quality: str = "1080p", page: int = 1) -> Dict[str, Any]:
        """Get complete playback information for a video.

        Args:
            url: Bilibili video URL or BV number.
            quality: Desired playback quality.
            page: Page/episode number for multi-part videos.

        Returns:
            Complete playback info including video details and play URLs.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        # Get video info and play URL in parallel
        info_task = self._get_video_info(bvid)
        play_url_task = self._get_play_url(bvid, quality, page)

        info, play_url_data = await asyncio.gather(info_task, play_url_task)

        if not info.get("success"):
            return info

        result = info.copy()
        result.update(play_url_data)

        return result

    async def get_playurl(
        self,
        url: str,
        quality: str = "1080p",
        page: int = 1,
    ) -> Dict[str, Any]:
        """Get direct play URLs for a video.

        Args:
            url: Bilibili video URL or BV number.
            quality: Desired quality.
            page: Page/episode number.

        Returns:
            Play URL information.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        return await self._get_play_url(bvid, quality, page)

    async def get_danmaku(
        self,
        url: str,
        page: int = 1,
        segment: int = 1,
    ) -> Dict[str, Any]:
        """Get danmaku (bullet comments) for a video.

        Args:
            url: Bilibili video URL or BV number.
            page: Page/episode number.
            segment: Danmaku segment index (each ~6 minutes).

        Returns:
            List of danmaku entries.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        # Get CID
        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        pages = data["data"].get("pages", [])
        if page > len(pages):
            return {"success": False, "message": f"Page {page} not found"}

        cid = pages[page - 1]["cid"]

        # Get danmaku XML
        async with self._get_client() as client:
            resp = await client.get(
                API_DANMAKU,
                params={"oid": cid},
            )

        danmaku_list = self._parse_danmaku_xml(resp.text)

        return {
            "success": True,
            "bvid": bvid,
            "cid": cid,
            "page": page,
            "danmaku_count": len(danmaku_list),
            "danmaku": danmaku_list,
        }

    async def get_playlist(self, url: str) -> Dict[str, Any]:
        """Get playlist/multi-part video information.

        Args:
            url: Bilibili video URL or BV number.

        Returns:
            Playlist information with all pages/episodes.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        video = data["data"]
        pages = []
        for p in video.get("pages", []):
            pages.append({
                "page": p.get("page"),
                "cid": p.get("cid"),
                "title": p.get("part"),
                "duration": format_duration(p.get("duration", 0)),
                "duration_seconds": p.get("duration", 0),
            })

        # Also check for season/collection info
        ugc_season = video.get("ugc_season")
        season_info = None
        if ugc_season:
            episodes = []
            for section in ugc_season.get("sections", []):
                for ep in section.get("episodes", []):
                    episodes.append({
                        "bvid": ep.get("bvid"),
                        "aid": ep.get("aid"),
                        "title": ep.get("title"),
                        "arc": {
                            "duration": format_duration(ep.get("arc", {}).get("duration", 0)),
                        },
                    })
            season_info = {
                "title": ugc_season.get("title"),
                "episode_count": len(episodes),
                "episodes": episodes,
            }

        return {
            "success": True,
            "bvid": video.get("bvid"),
            "title": video.get("title"),
            "page_count": len(pages),
            "pages": pages,
            "season": season_info,
        }

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a player action.

        Args:
            action: Action name ('play', 'get_playurl', 'get_danmaku', 'get_playlist').
            **kwargs: Additional parameters for the action.

        Returns:
            Action result dict.
        """
        actions = {
            "play": self.play,
            "get_playurl": self.get_playurl,
            "get_danmaku": self.get_danmaku,
            "get_playlist": self.get_playlist,
        }

        handler = actions.get(action)
        if not handler:
            return {"success": False, "message": f"Unknown action: {action}"}

        import inspect
        sig = inspect.signature(handler)
        valid_params = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return await handler(**valid_params)

    async def _get_video_info(self, bvid: str) -> Dict[str, Any]:
        """Get video information.

        Args:
            bvid: BV ID.

        Returns:
            Video info dict.
        """
        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        video = data["data"]
        stat = video.get("stat", {})
        owner = video.get("owner", {})

        return {
            "success": True,
            "bvid": video.get("bvid"),
            "aid": video.get("aid"),
            "title": video.get("title"),
            "description": video.get("desc"),
            "cover": video.get("pic"),
            "duration": format_duration(video.get("duration", 0)),
            "author": {
                "mid": owner.get("mid"),
                "name": owner.get("name"),
            },
            "stats": {
                "views": format_number(stat.get("view", 0)),
                "danmaku": stat.get("danmaku", 0),
                "likes": format_number(stat.get("like", 0)),
            },
        }

    async def _get_play_url(self, bvid: str, quality: str, page: int) -> Dict[str, Any]:
        """Get play URL for a video.

        Args:
            bvid: BV ID.
            quality: Desired quality.
            page: Page number.

        Returns:
            Play URL info dict.
        """
        # Get CID
        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"play_url": None, "message": data.get("message", "API error")}

        pages = data["data"].get("pages", [])
        if page > len(pages):
            return {"play_url": None, "message": f"Page {page} not found"}

        cid = pages[page - 1]["cid"]
        qn = QUALITY_MAP.get(quality, 80)

        async with self._get_client() as client:
            resp = await client.get(
                API_PLAY_URL,
                params={
                    "bvid": bvid,
                    "cid": cid,
                    "qn": qn,
                    "fnval": 4048,
                    "fourk": 1,
                },
            )
            play_data = resp.json()

        if play_data.get("code") != 0:
            return {"play_url": None, "message": play_data.get("message", "API error")}

        dash = play_data.get("data", {}).get("dash")
        if dash:
            video_streams = []
            for v in dash.get("video", []):
                quality_names = {val: key for key, val in QUALITY_MAP.items()}
                video_streams.append({
                    "quality": quality_names.get(v.get("id"), f"qn_{v.get('id')}"),
                    "qn": v.get("id"),
                    "codecs": v.get("codecs"),
                    "bandwidth": v.get("bandwidth"),
                    "url": v.get("baseUrl") or v.get("base_url"),
                })

            audio_streams = []
            for a in dash.get("audio", []):
                audio_streams.append({
                    "bandwidth": a.get("bandwidth"),
                    "codecs": a.get("codecs"),
                    "url": a.get("baseUrl") or a.get("base_url"),
                })

            return {
                "play_type": "dash",
                "video_streams": video_streams,
                "audio_streams": audio_streams,
                "current_quality": quality,
            }

        # Fallback to durl
        durl = play_data.get("data", {}).get("durl", [])
        urls = [{"url": d.get("url"), "size": d.get("size")} for d in durl]

        return {
            "play_type": "durl",
            "urls": urls,
            "current_quality": quality,
        }

    @staticmethod
    def _parse_danmaku_xml(xml_text: str) -> List[Dict[str, Any]]:
        """Parse danmaku XML response.

        Args:
            xml_text: XML response text.

        Returns:
            List of danmaku entries.
        """
        import re

        danmaku_list = []
        pattern = re.compile(r'<d p="([^"]+)">(.*?)</d>')

        for match in pattern.finditer(xml_text):
            params = match.group(1).split(",")
            content = match.group(2)

            if len(params) >= 8:
                danmaku_list.append({
                    "time": float(params[0]),
                    "mode": int(params[1]),  # 1=scroll, 4=bottom, 5=top
                    "font_size": int(params[2]),
                    "color": int(params[3]),
                    "timestamp": int(params[4]),
                    "pool": int(params[5]),  # 0=normal, 1=subtitle, 2=special
                    "user_hash": params[6],
                    "dmid": params[7],
                    "content": content,
                })

        # Sort by time
        danmaku_list.sort(key=lambda d: d["time"])

        return danmaku_list
