"""Bilibili collector via official API."""

from __future__ import annotations

import re

import requests

from datapulse.core.models import MediaType, SourceType
from datapulse.core.retry import retry
from datapulse.core.utils import clean_text

from .base import BaseCollector, ParseResult


class BilibiliCollector(BaseCollector):
    name = "bilibili"
    source_type = SourceType.BILIBILI
    reliability = 0.84
    tier = 1
    setup_hint = ""
    api_url = "https://api.bilibili.com/x/web-interface/view"

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "public API (no auth)", "available": True}

    def can_handle(self, url: str) -> bool:
        return "bilibili.com" in url.lower() or "b23.tv" in url.lower()

    def parse(self, url: str) -> ParseResult:
        bvid = self._extract_bvid(url)
        if not bvid:
            return ParseResult.failure(url, "Could not detect BV/BVID.")

        try:
            payload = self._fetch_video_info(bvid)
        except (requests.RequestException, requests.Timeout, ValueError) as exc:
            return ParseResult.failure(url, f"Bilibili API error: {exc}")

        if payload.get("code") != 0:
            return ParseResult.failure(url, payload.get("message", "Bilibili API error"))

        data = payload.get("data", {})
        title = data.get("title", "")
        desc = data.get("desc", "")
        owner = data.get("owner", {})
        stat = data.get("stat", {})

        view = stat.get("view", 0)
        like = stat.get("like", 0)
        coin = stat.get("coin", 0)
        favorite = stat.get("favorite", 0)
        danmaku = stat.get("danmaku", 0)
        reply = stat.get("reply", 0)
        share = stat.get("share", 0)

        content = clean_text("\n\n".join([
            f"{title}",
            desc or "",
            f"Author: {owner.get('name', '')}",
            f"Views: {view:,}  Likes: {like:,}  Coins: {coin:,}",
            f"Favorites: {favorite:,}  Danmaku: {danmaku:,}  Replies: {reply:,}  Shares: {share:,}",
        ]))

        return ParseResult(
            url=url,
            title=title,
            author=owner.get("name", ""),
            content=content,
            excerpt=content[:240],
            source_type=self.source_type,
            media_type=MediaType.VIDEO.value,
            tags=["bilibili", "video"],
            confidence_flags=["api"],
            extra={
                "bvid": bvid,
                "video_id": bvid,
                "view": view,
                "like": like,
                "coin": coin,
                "favorite": favorite,
                "danmaku": danmaku,
                "reply": reply,
                "share": share,
            },
        )

    @retry(max_attempts=3, base_delay=1.0, retryable=(requests.RequestException,))
    def _fetch_video_info(self, bvid: str) -> dict:  # type: ignore[type-arg]
        resp = requests.get(
            self.api_url,
            params={"bvid": bvid},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    @staticmethod
    def _extract_bvid(url: str) -> str:
        m = re.search(r"BV[0-9A-Za-z]{10}", url)
        if m:
            return m.group(0)
        try:
            response = requests.get(url, timeout=8, allow_redirects=True)
            response.raise_for_status()
            redirected = response.url
            m = re.search(r"BV[0-9A-Za-z]{10}", redirected)
            if m:
                return m.group(0)
        except (requests.RequestException, OSError):
            pass
        return ""
