"""Bilibili video watching and stats tracking module."""

import asyncio
import time
from typing import Optional, Dict, Any, List

import httpx

from .auth import BilibiliAuth
from .utils import (
    API_VIDEO_INFO,
    API_VIDEO_DETAIL,
    DEFAULT_HEADERS,
    extract_bvid,
    format_number,
    format_duration,
    parse_video_url,
)


class BilibiliWatcher:
    """Watch and monitor Bilibili videos.

    Track view counts, comments, likes, and other engagement metrics over time.
    """

    def __init__(self, auth: Optional[BilibiliAuth] = None):
        """Initialize BilibiliWatcher.

        Args:
            auth: Optional BilibiliAuth instance for authenticated requests.
        """
        self.auth = auth
        self._tracking_data: Dict[str, List[Dict]] = {}

    def _get_client(self) -> httpx.AsyncClient:
        """Get an HTTP client, using auth if available."""
        if self.auth:
            return self.auth.get_client()
        return httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True,
        )

    async def watch(self, url: str) -> Dict[str, Any]:
        """Get detailed video information for watching.

        Args:
            url: Video URL (supports Bilibili).

        Returns:
            Detailed video information.
        """
        video_info = parse_video_url(url)

        if video_info["platform"] == "bilibili":
            return await self._watch_bilibili(video_info.get("bvid"), url)
        else:
            return {"success": False, "message": f"Unsupported platform for URL: {url}"}

    async def _watch_bilibili(self, bvid: Optional[str], url: str) -> Dict[str, Any]:
        """Get detailed Bilibili video information.

        Args:
            bvid: BV ID of the video.
            url: Original URL.

        Returns:
            Video details dict.
        """
        if not bvid:
            bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Cannot extract BV ID from: {url}"}

        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_DETAIL, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        video = data["data"].get("View", {})
        stat = video.get("stat", {})
        owner = video.get("owner", {})
        tags = [t.get("tag_name") for t in data["data"].get("Tags", []) if t.get("tag_name")]
        related = []
        for r in data["data"].get("Related", [])[:5]:
            related.append({
                "bvid": r.get("bvid"),
                "title": r.get("title"),
                "author": r.get("owner", {}).get("name"),
            })

        return {
            "success": True,
            "platform": "bilibili",
            "bvid": video.get("bvid"),
            "aid": video.get("aid"),
            "title": video.get("title"),
            "description": video.get("desc"),
            "cover": video.get("pic"),
            "duration": format_duration(video.get("duration", 0)),
            "author": {
                "mid": owner.get("mid"),
                "name": owner.get("name"),
                "face": owner.get("face"),
            },
            "stats": {
                "views": stat.get("view", 0),
                "views_formatted": format_number(stat.get("view", 0)),
                "danmaku": stat.get("danmaku", 0),
                "likes": stat.get("like", 0),
                "coins": stat.get("coin", 0),
                "favorites": stat.get("favorite", 0),
                "shares": stat.get("share", 0),
                "comments": stat.get("reply", 0),
            },
            "tags": tags,
            "related_videos": related,
            "url": f"https://www.bilibili.com/video/{video.get('bvid')}",
        }

    async def get_stats(self, url: str) -> Dict[str, Any]:
        """Get current engagement statistics for a video.

        Args:
            url: Video URL.

        Returns:
            Current engagement statistics.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        stat = data["data"].get("stat", {})
        return {
            "success": True,
            "bvid": bvid,
            "title": data["data"].get("title"),
            "timestamp": int(time.time()),
            "stats": {
                "views": stat.get("view", 0),
                "danmaku": stat.get("danmaku", 0),
                "likes": stat.get("like", 0),
                "coins": stat.get("coin", 0),
                "favorites": stat.get("favorite", 0),
                "shares": stat.get("share", 0),
                "comments": stat.get("reply", 0),
            },
        }

    async def track(
        self,
        url: str,
        interval: int = 60,
        duration: int = 24,
        callback=None,
    ) -> Dict[str, Any]:
        """Track video metrics over time.

        Args:
            url: Video URL.
            interval: Tracking interval in minutes.
            duration: Total tracking duration in hours.
            callback: Optional async callback function called with each data point.

        Returns:
            Tracking summary with all collected data points.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        data_points = []
        end_time = time.time() + duration * 3600
        interval_seconds = interval * 60

        while time.time() < end_time:
            stats = await self.get_stats(url)
            if stats.get("success"):
                data_points.append(stats)
                if callback:
                    await callback(stats)

            self._tracking_data[bvid] = data_points

            remaining = end_time - time.time()
            if remaining <= 0:
                break
            await asyncio.sleep(min(interval_seconds, remaining))

        # Calculate changes
        summary = self._calculate_changes(data_points)

        return {
            "success": True,
            "bvid": bvid,
            "data_points": len(data_points),
            "duration_hours": duration,
            "interval_minutes": interval,
            "summary": summary,
            "data": data_points,
        }

    async def compare(self, urls: List[str]) -> Dict[str, Any]:
        """Compare engagement metrics of multiple videos.

        Args:
            urls: List of video URLs to compare.

        Returns:
            Comparison results.
        """
        results = []
        tasks = [self.get_stats(url) for url in urls]
        stats_list = await asyncio.gather(*tasks, return_exceptions=True)

        for url, stats in zip(urls, stats_list):
            if isinstance(stats, Exception):
                results.append({"url": url, "success": False, "message": str(stats)})
            else:
                results.append(stats)

        # Rank by views
        successful = [r for r in results if r.get("success")]
        successful.sort(key=lambda r: r.get("stats", {}).get("views", 0), reverse=True)

        return {
            "success": True,
            "total": len(urls),
            "compared": len(successful),
            "ranking": [
                {
                    "rank": i + 1,
                    "bvid": r.get("bvid"),
                    "title": r.get("title"),
                    "views": r.get("stats", {}).get("views", 0),
                    "likes": r.get("stats", {}).get("likes", 0),
                }
                for i, r in enumerate(successful)
            ],
            "results": results,
        }

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a watcher action.

        Args:
            action: Action name ('watch', 'get_stats', 'track', 'compare').
            **kwargs: Additional parameters for the action.

        Returns:
            Action result dict.
        """
        actions = {
            "watch": self.watch,
            "get_stats": self.get_stats,
            "track": self.track,
            "compare": self.compare,
        }

        handler = actions.get(action)
        if not handler:
            return {"success": False, "message": f"Unknown action: {action}"}

        import inspect
        sig = inspect.signature(handler)
        valid_params = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return await handler(**valid_params)

    @staticmethod
    def _calculate_changes(data_points: List[Dict]) -> Dict[str, Any]:
        """Calculate metric changes from data points.

        Args:
            data_points: List of stat snapshots.

        Returns:
            Summary of changes.
        """
        if len(data_points) < 2:
            return {"message": "Not enough data points for comparison"}

        first = data_points[0].get("stats", {})
        last = data_points[-1].get("stats", {})

        changes = {}
        for key in first:
            if isinstance(first.get(key), (int, float)):
                changes[key] = {
                    "start": first[key],
                    "end": last[key],
                    "change": last[key] - first[key],
                    "change_percent": round(
                        ((last[key] - first[key]) / first[key] * 100) if first[key] > 0 else 0, 2
                    ),
                }

        return changes
