"""Bilibili hot/trending video monitoring module."""

import asyncio
from typing import Optional, Dict, Any, List

import httpx

from .auth import BilibiliAuth
from .utils import (
    API_HOT,
    API_TRENDING,
    API_WEEKLY,
    API_RANK,
    CATEGORY_TID,
    DEFAULT_HEADERS,
    format_number,
    format_duration,
)


class HotMonitor:
    """Monitor Bilibili hot and trending videos.

    Provides access to popular videos, trending topics, weekly must-watch lists,
    and category-specific rankings.
    """

    def __init__(self, auth: Optional[BilibiliAuth] = None):
        """Initialize HotMonitor.

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

    async def get_hot(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Get popular/hot videos from Bilibili.

        Args:
            page: Page number (1-indexed).
            page_size: Number of results per page.

        Returns:
            Dict containing list of hot videos and pagination info.
        """
        async with self._get_client() as client:
            resp = await client.get(
                API_HOT,
                params={"pn": page, "ps": page_size},
            )
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        videos = []
        for item in data.get("data", {}).get("list", []):
            videos.append(self._parse_video(item))

        return {
            "success": True,
            "videos": videos,
            "page": page,
            "has_more": bool(data.get("data", {}).get("no_more") is False),
        }

    async def get_trending(self, limit: int = 20) -> Dict[str, Any]:
        """Get trending series/topics list.

        Args:
            limit: Maximum number of results.

        Returns:
            Dict containing list of trending series.
        """
        async with self._get_client() as client:
            resp = await client.get(API_TRENDING)
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        series_list = []
        for item in data.get("data", {}).get("list", [])[:limit]:
            series_list.append({
                "number": item.get("number"),
                "subject": item.get("subject"),
                "status": item.get("status"),
                "name": item.get("name"),
            })

        return {"success": True, "series": series_list}

    async def get_weekly(self, number: Optional[int] = None) -> Dict[str, Any]:
        """Get weekly must-watch video list.

        Args:
            number: Specific week number. If None, gets the latest week.

        Returns:
            Dict containing the weekly video list.
        """
        params = {}
        if number is not None:
            params["number"] = number

        async with self._get_client() as client:
            resp = await client.get(API_WEEKLY, params=params)
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        config = data.get("data", {}).get("config", {})
        videos = []
        for item in data.get("data", {}).get("list", []):
            videos.append(self._parse_video(item))

        return {
            "success": True,
            "week_number": config.get("number"),
            "subject": config.get("subject"),
            "label": config.get("label"),
            "videos": videos,
        }

    async def get_rank(
        self,
        category: str = "all",
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get category ranking videos.

        Args:
            category: Category name (see CATEGORY_TID keys).
            limit: Maximum number of results.

        Returns:
            Dict containing ranked video list.
        """
        tid = CATEGORY_TID.get(category, 0)

        async with self._get_client() as client:
            resp = await client.get(
                API_RANK,
                params={"rid": tid, "type": "all"},
            )
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        videos = []
        for item in data.get("data", {}).get("list", [])[:limit]:
            video = self._parse_video(item)
            video["score"] = item.get("score")
            videos.append(video)

        return {
            "success": True,
            "category": category,
            "videos": videos,
        }

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a hot monitor action.

        Args:
            action: Action name ('get_hot', 'get_trending', 'get_weekly', 'get_rank').
            **kwargs: Additional parameters for the action.

        Returns:
            Action result dict.
        """
        actions = {
            "get_hot": self.get_hot,
            "get_trending": self.get_trending,
            "get_weekly": self.get_weekly,
            "get_rank": self.get_rank,
        }

        handler = actions.get(action)
        if not handler:
            return {"success": False, "message": f"Unknown action: {action}"}

        # Filter kwargs to only pass valid parameters
        import inspect
        sig = inspect.signature(handler)
        valid_params = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return await handler(**valid_params)

    @staticmethod
    def _parse_video(item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a video item from API response.

        Args:
            item: Raw video data from API.

        Returns:
            Parsed video information dict.
        """
        stat = item.get("stat", {})
        owner = item.get("owner", {})

        return {
            "bvid": item.get("bvid"),
            "aid": item.get("aid"),
            "title": item.get("title"),
            "description": item.get("desc", ""),
            "cover": item.get("pic"),
            "duration": format_duration(item.get("duration", 0)),
            "duration_seconds": item.get("duration", 0),
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
            "url": f"https://www.bilibili.com/video/{item.get('bvid')}",
            "publish_time": item.get("pubdate"),
        }
