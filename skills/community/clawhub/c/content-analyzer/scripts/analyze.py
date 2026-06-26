#!/usr/bin/env python3
"""Content analyzer for Xiaohongshu and Douyin posts/profiles via TikHub API.

Usage:
    python3 analyze.py <url> [--max N]

Supports:
    - XHS note URLs (xiaohongshu.com/explore/{id}, xiaohongshu.com/discovery/item/{id})
    - XHS profile URLs (xiaohongshu.com/user/profile/{id})
    - Douyin video URLs (douyin.com/video/{id})
    - Douyin profile URLs (douyin.com/user/{sec_uid})
    - Short links (xhslink.com/xxx, v.douyin.com/xxx)
"""

from __future__ import annotations

# Clear proxy env vars to prevent httpx from using SOCKS proxy without socksio
import os as _os
for _k in ("all_proxy", "ALL_PROXY", "http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY"):
    _os.environ.pop(_k, None)

import argparse
import asyncio
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

TIKHUB_BASE_URL = "https://api.tikhub.io"
USER_AGENT = "openclaw-content-analyzer/1.0"
DEFAULT_MAX_POSTS = 50


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def _load_api_token() -> str:
    """Read TikHub API token from env var or ~/.openclaw/openclaw.json."""
    token = os.environ.get("TIKHUB_API_TOKEN", "")
    if token:
        return token

    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            token = (config.get("env") or {}).get("TIKHUB_API_TOKEN", "")
        except (json.JSONDecodeError, OSError):
            pass

    return token


# ---------------------------------------------------------------------------
# Count parsing (Chinese notation: "1.2w", "1.5万", "100+", "1k")
# ---------------------------------------------------------------------------

def _parse_count(value: Any) -> int:
    """Parse engagement count from various formats.

    Handles Chinese notation like "1.2w", "1.5万", "100+", "1k", raw ints.
    """
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip().rstrip("+")
    if not s:
        return 0
    try:
        if s.endswith(("w", "万")):
            return int(float(s[:-1]) * 10000)
        if s.endswith("k"):
            return int(float(s[:-1]) * 1000)
        return int(float(s))
    except (ValueError, TypeError):
        return 0


def _parse_timestamp(value: Any) -> str | None:
    """Parse timestamp (ms, seconds, or ISO string) to ISO 8601 string."""
    if not value:
        return None
    if isinstance(value, (int, float)):
        ts = value
        # Milliseconds if > 10 digits
        if ts > 1e12:
            ts = ts / 1000
        try:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt.isoformat()
        except (ValueError, OSError):
            return None
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.isoformat()
        except (ValueError, AttributeError):
            return None
    return None


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

class ParsedURL:
    """Represents a parsed content URL."""

    def __init__(self, platform: str, kind: str, identifier: str):
        self.platform = platform  # "xiaohongshu" | "douyin"
        self.kind = kind          # "note" | "profile" | "video"
        self.identifier = identifier

    def __repr__(self) -> str:
        return f"ParsedURL({self.platform}, {self.kind}, {self.identifier})"


# Patterns for direct URLs
_XHS_NOTE_RE = re.compile(
    r"xiaohongshu\.com/(?:explore|discovery/item)/([a-zA-Z0-9]+)"
)
_XHS_PROFILE_RE = re.compile(
    r"xiaohongshu\.com/user/profile/([a-zA-Z0-9]+)"
)
_DOUYIN_VIDEO_RE = re.compile(
    r"douyin\.com/video/(\d+)"
)
_DOUYIN_PROFILE_RE = re.compile(
    r"douyin\.com/user/([a-zA-Z0-9_-]+)"
)
_XHS_SHORT_RE = re.compile(r"xhslink\.com/")
_DOUYIN_SHORT_RE = re.compile(r"v\.douyin\.com/")


async def _resolve_short_link(url: str) -> str:
    """Follow redirects on short links to get the final URL."""
    if not url.startswith("http"):
        url = "https://" + url
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=15,
        headers={"User-Agent": USER_AGENT},
        proxy=None,
    ) as client:
        resp = await client.get(url)
        return str(resp.url)


async def parse_url(raw_url: str) -> ParsedURL | None:
    """Parse a URL into platform/kind/identifier, resolving short links."""
    url = raw_url.strip()
    if not url:
        return None

    # Resolve short links first
    if _XHS_SHORT_RE.search(url) or _DOUYIN_SHORT_RE.search(url):
        try:
            url = await _resolve_short_link(url)
        except httpx.HTTPError:
            return None

    # XHS note
    m = _XHS_NOTE_RE.search(url)
    if m:
        return ParsedURL("xiaohongshu", "note", m.group(1))

    # XHS profile
    m = _XHS_PROFILE_RE.search(url)
    if m:
        return ParsedURL("xiaohongshu", "profile", m.group(1))

    # Douyin video
    m = _DOUYIN_VIDEO_RE.search(url)
    if m:
        return ParsedURL("douyin", "video", m.group(1))

    # Douyin profile
    m = _DOUYIN_PROFILE_RE.search(url)
    if m:
        return ParsedURL("douyin", "profile", m.group(1))

    return None


# ---------------------------------------------------------------------------
# TikHub API client
# ---------------------------------------------------------------------------

class TikHubAPI:
    """Thin async wrapper around TikHub API endpoints."""

    def __init__(self, token: str):
        self._token = token
        self._client: httpx.AsyncClient | None = None

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=TIKHUB_BASE_URL,
                headers={
                    "Authorization": f"Bearer {self._token}",
                    "User-Agent": USER_AGENT,
                },
                timeout=30,
                proxy=None,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    # -- XHS --

    async def xhs_note_info(self, note_id: str) -> dict | None:
        """GET /api/v1/xiaohongshu/app/get_note_info?note_id=X

        Returns the first note from the response, or None.
        """
        client = await self._ensure_client()
        resp = await client.get(
            "/api/v1/xiaohongshu/app/get_note_info",
            params={"note_id": note_id},
        )
        resp.raise_for_status()
        items = resp.json().get("data", {}).get("data", [])
        if not items:
            return None
        note_list = items[0].get("note_list", [])
        return note_list[0] if note_list else None

    async def xhs_user_info(self, user_id: str) -> dict:
        """GET /api/v1/xiaohongshu/app/get_user_info?user_id=X"""
        client = await self._ensure_client()
        resp = await client.get(
            "/api/v1/xiaohongshu/app/get_user_info",
            params={"user_id": user_id},
        )
        resp.raise_for_status()
        return resp.json().get("data", {}).get("data", {})

    async def xhs_user_notes(self, user_id: str, cursor: str = "") -> dict:
        """GET /api/v1/xiaohongshu/app/get_user_notes?user_id=X&cursor=Y

        Returns {"notes": [...], "has_more": bool}.
        """
        client = await self._ensure_client()
        params: dict[str, str] = {"user_id": user_id}
        if cursor:
            params["cursor"] = cursor
        resp = await client.get(
            "/api/v1/xiaohongshu/app/get_user_notes",
            params=params,
        )
        resp.raise_for_status()
        inner = resp.json().get("data", {}).get("data", {})
        return {
            "notes": inner.get("notes", []),
            "has_more": bool(inner.get("has_more", False)),
        }

    # -- Douyin --

    async def douyin_video(self, aweme_id: str) -> dict | None:
        """GET /api/v1/douyin/app/v3/fetch_one_video_v3?aweme_id=X"""
        client = await self._ensure_client()
        resp = await client.get(
            "/api/v1/douyin/app/v3/fetch_one_video_v3",
            params={"aweme_id": aweme_id},
        )
        resp.raise_for_status()
        data = resp.json().get("data", {})
        return data.get("aweme_detail") or data

    async def douyin_search(
        self,
        keyword: str,
        cursor: int = 0,
        sort_type: int = 0,
        publish_time: int = 0,
    ) -> dict:
        """POST /api/v1/douyin/search/fetch_general_search_v3"""
        client = await self._ensure_client()
        body = {
            "keyword": keyword,
            "cursor": cursor,
            "sort_type": sort_type,
            "publish_time": publish_time,
            "filter_duration": 0,
            "content_type": 0,
        }
        resp = await client.post(
            "/api/v1/douyin/search/fetch_general_search_v3",
            json=body,
        )
        resp.raise_for_status()
        data = resp.json().get("data", {})
        raw_items = data.get("data", [])
        items = []
        for item in raw_items:
            aweme = item.get("aweme_info")
            if aweme:
                items.append(aweme)
        return {
            "items": items,
            "cursor": data.get("cursor", 0),
            "has_more": bool(data.get("has_more", 0)),
        }


# ---------------------------------------------------------------------------
# Data extraction / formatting
# ---------------------------------------------------------------------------

def _extract_xhs_note(note: dict) -> dict:
    """Convert raw TikHub XHS note data to output format."""
    # Handle TikHub nested format: {id, model_type, note_card: {...}}
    note_card = note.get("note_card")
    if note_card and isinstance(note_card, dict):
        flat = dict(note_card)
        flat.setdefault("noteId", note.get("id", ""))
        note = flat

    note_id = note.get("noteId") or note.get("id") or note.get("note_id") or ""
    title = note.get("displayTitle") or note.get("display_title") or note.get("title") or ""
    desc = note.get("desc") or note.get("content") or note.get("description") or ""

    # Author
    author_raw = note.get("user") or note.get("author") or {}
    if isinstance(author_raw, str):
        author_raw = {"nickname": author_raw}
    author = {
        "name": author_raw.get("nickname") or author_raw.get("nickName") or author_raw.get("name") or "",
        "id": author_raw.get("userId") or author_raw.get("user_id") or author_raw.get("userid") or "",
    }

    # Tags
    tags: list[str] = []
    tag_list = note.get("tagList") or note.get("tags") or note.get("tag_list") or []
    for t in tag_list:
        if isinstance(t, str):
            tags.append(t)
        elif isinstance(t, dict):
            name = t.get("name") or t.get("tag") or ""
            if name:
                tags.append(name)

    # Images
    images: list[str] = []
    image_list = (
        note.get("imageList") or note.get("images")
        or note.get("image_list") or note.get("images_list") or []
    )
    for img in image_list:
        if isinstance(img, str):
            images.append(img)
        elif isinstance(img, dict):
            url = img.get("url") or img.get("urlDefault") or ""
            if url:
                images.append(url)

    # Video
    video_out: dict[str, Any] | None = None
    note_type = note.get("type", "")
    if note_type == "video":
        video_raw = note.get("video") or {}
        video_url = (
            video_raw.get("url")
            or video_raw.get("media", {}).get("stream", {}).get("h264", [{}])[0].get("masterUrl", "")
        )
        if not video_url:
            for key in ("videoUrl", "video_url", "mediaUrl"):
                video_url = note.get(key, "")
                if video_url:
                    break
        if video_url:
            video_out = {"url": video_url}
            duration = video_raw.get("duration")
            if duration:
                video_out["duration_ms"] = duration

    # Stats
    interact = note.get("interactInfo") or note.get("interact_info") or {}
    stats = {
        "likes": _parse_count(
            interact.get("likedCount") or interact.get("liked_count")
            or note.get("likes") or note.get("liked_count")
        ),
        "collects": _parse_count(
            interact.get("collectedCount") or interact.get("collected_count")
            or note.get("collects") or note.get("collected_count")
        ),
        "comments": _parse_count(
            interact.get("commentCount") or interact.get("comment_count")
            or note.get("comments") or note.get("comments_count") or note.get("comment_count")
        ),
        "shares": _parse_count(
            interact.get("shareCount") or interact.get("share_count")
            or note.get("shares") or note.get("shared_count") or note.get("share_count")
        ),
        "views": 0,  # XHS doesn't expose view counts
    }

    # Published at
    published_at = _parse_timestamp(
        note.get("time") or note.get("createTime")
        or note.get("create_time") or note.get("publishTime")
    )

    # URL
    post_url = note.get("postUrl") or note.get("url") or note.get("link") or ""
    if not post_url and note_id:
        post_url = f"https://www.xiaohongshu.com/explore/{note_id}"

    result: dict[str, Any] = {
        "platform": "xiaohongshu",
        "type": "note",
        "title": title,
        "content": desc,
        "author": author,
        "tags": tags,
        "images": images,
    }
    if video_out:
        result["video"] = video_out
    result["stats"] = stats
    result["published_at"] = published_at
    result["url"] = post_url

    return result


def _extract_douyin_video(aweme: dict) -> dict:
    """Convert raw TikHub Douyin aweme data to output format."""
    aweme_id = aweme.get("aweme_id") or ""
    desc = aweme.get("desc", "")

    # Author
    author_raw = aweme.get("author") or {}
    author = {
        "name": author_raw.get("nickname", ""),
        "id": author_raw.get("uid") or author_raw.get("sec_uid") or "",
    }

    # Tags
    tags: list[str] = []
    for extra in aweme.get("text_extra", []):
        tag = extra.get("hashtag_name", "")
        if tag:
            tags.append(tag)

    # Images (aweme_type=68 is image post)
    images: list[str] = []
    is_image_post = aweme.get("aweme_type") == 68
    if is_image_post:
        for img in aweme.get("images", []):
            url_list = img.get("url_list", [])
            if url_list:
                images.append(url_list[0])

    # Video
    video_out: dict[str, Any] | None = None
    if not is_image_post:
        video_raw = aweme.get("video", {})
        play_addr = video_raw.get("play_addr", {})
        uri = play_addr.get("uri", "")
        if uri:
            permanent_url = f"https://www.douyin.com/aweme/v1/play/?video_id={uri}"
            video_out = {"url": permanent_url}
            duration = video_raw.get("duration", 0)
            if duration:
                video_out["duration_ms"] = duration

    # Stats
    raw_stats = aweme.get("statistics", {})
    stats = {
        "likes": raw_stats.get("digg_count", 0) or 0,
        "collects": raw_stats.get("collect_count", 0) or 0,
        "comments": raw_stats.get("comment_count", 0) or 0,
        "shares": raw_stats.get("share_count", 0) or 0,
        "views": raw_stats.get("play_count", 0) or 0,
    }

    # Published at
    published_at = _parse_timestamp(aweme.get("create_time"))

    # URL
    share_url = aweme.get("share_url", "")
    if not share_url:
        share_url = f"https://www.douyin.com/video/{aweme_id}"

    result: dict[str, Any] = {
        "platform": "douyin",
        "type": "video",
        "title": desc,
        "content": desc,
        "author": author,
        "tags": tags,
        "images": images,
    }
    if video_out:
        result["video"] = video_out
    result["stats"] = stats
    result["published_at"] = published_at
    result["url"] = share_url

    return result


# ---------------------------------------------------------------------------
# Profile aggregation
# ---------------------------------------------------------------------------

def _aggregate_posts(posts: list[dict]) -> dict:
    """Compute aggregate stats from a list of formatted post dicts."""
    if not posts:
        return {}

    total = len(posts)
    total_likes = sum(p.get("stats", {}).get("likes", 0) for p in posts)
    total_collects = sum(p.get("stats", {}).get("collects", 0) for p in posts)
    total_comments = sum(p.get("stats", {}).get("comments", 0) for p in posts)

    avg_likes = round(total_likes / total)
    avg_collects = round(total_collects / total)
    avg_comments = round(total_comments / total)

    # Top posts by likes
    sorted_by_likes = sorted(posts, key=lambda p: p.get("stats", {}).get("likes", 0), reverse=True)
    top_posts = [
        {"title": p.get("title", ""), "likes": p.get("stats", {}).get("likes", 0)}
        for p in sorted_by_likes[:5]
    ]

    # Tag frequency
    tag_counter: Counter[str] = Counter()
    for p in posts:
        for tag in p.get("tags", []):
            tag_counter[tag] += 1
    tag_frequency = dict(tag_counter.most_common(20))

    # Content type ratio
    type_counter: Counter[str] = Counter()
    for p in posts:
        if p.get("video"):
            type_counter["video"] += 1
        elif p.get("images"):
            type_counter["image"] += 1
        else:
            type_counter["text"] += 1
    content_type_ratio = dict(type_counter)

    # Posting frequency estimate
    timestamps = []
    for p in posts:
        ts = p.get("published_at")
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                timestamps.append(dt)
            except (ValueError, TypeError):
                pass

    posting_frequency = ""
    if len(timestamps) >= 2:
        timestamps.sort()
        span_days = (timestamps[-1] - timestamps[0]).total_seconds() / 86400
        if span_days > 0 and total > 1:
            days_per_post = span_days / (total - 1)
            if days_per_post < 1:
                posting_frequency = f"约每天{round(1 / days_per_post)}篇"
            else:
                posting_frequency = f"约每{round(days_per_post)}天1篇"

    return {
        "avg_likes": avg_likes,
        "avg_collects": avg_collects,
        "avg_comments": avg_comments,
        "top_posts": top_posts,
        "tag_frequency": tag_frequency,
        "content_type_ratio": content_type_ratio,
        "posting_frequency": posting_frequency,
    }


# ---------------------------------------------------------------------------
# Main handlers
# ---------------------------------------------------------------------------

async def handle_xhs_note(api: TikHubAPI, note_id: str) -> dict:
    """Fetch and format a single XHS note."""
    raw = await api.xhs_note_info(note_id)
    if not raw:
        return {"error": f"Note not found: {note_id}"}
    return _extract_xhs_note(raw)


async def handle_xhs_profile(api: TikHubAPI, user_id: str, max_posts: int) -> dict:
    """Fetch and aggregate an XHS user's posts."""
    user_info = await api.xhs_user_info(user_id)
    author = {
        "name": user_info.get("nickname") or user_info.get("nickName") or "",
        "id": user_id,
    }

    posts: list[dict] = []
    cursor = ""
    while len(posts) < max_posts:
        page = await api.xhs_user_notes(user_id, cursor=cursor)
        notes = page.get("notes", [])
        if not notes:
            break
        for note in notes:
            if len(posts) >= max_posts:
                break
            posts.append(_extract_xhs_note(note))
        if not page.get("has_more", False):
            break
        # Derive cursor from the last note's id for pagination
        last = notes[-1] if notes else {}
        cursor = last.get("id") or last.get("noteId") or ""
        if not cursor:
            break

    # Simplify posts for profile output
    simplified = []
    for p in posts:
        entry: dict[str, Any] = {"title": p.get("title", "")}
        entry.update(p.get("stats", {}))
        if p.get("published_at"):
            entry["published_at"] = p["published_at"]
        if p.get("url"):
            entry["url"] = p["url"]
        simplified.append(entry)

    return {
        "platform": "xiaohongshu",
        "type": "profile_analysis",
        "author": author,
        "total_fetched": len(posts),
        "posts": simplified,
        "aggregate": _aggregate_posts(posts),
    }


async def handle_douyin_video(api: TikHubAPI, aweme_id: str) -> dict:
    """Fetch and format a single Douyin video."""
    raw = await api.douyin_video(aweme_id)
    if not raw:
        return {"error": f"Video not found: {aweme_id}"}
    return _extract_douyin_video(raw)


async def handle_douyin_profile(api: TikHubAPI, sec_uid: str, max_posts: int) -> dict:
    """Fetch and aggregate a Douyin user's posts via search fallback.

    Note: TikHub doesn't have a direct user-posts endpoint for Douyin,
    so we use the user info from a video or search to gather posts.
    This is a best-effort approach using the search API.
    """
    # For Douyin profiles, we use search with the sec_uid as keyword
    # since there's no direct paginated user-posts endpoint in TikHub
    posts: list[dict] = []
    author = {"name": "", "id": sec_uid}

    # Try to fetch user info from the first available video
    result = await api.douyin_search(keyword=sec_uid, cursor=0)
    items = result.get("items", [])

    for aweme in items:
        if len(posts) >= max_posts:
            break
        formatted = _extract_douyin_video(aweme)
        if not author["name"] and formatted.get("author", {}).get("name"):
            author["name"] = formatted["author"]["name"]
        posts.append(formatted)

    # Simplify posts for profile output
    simplified = []
    for p in posts:
        entry: dict[str, Any] = {"title": p.get("title", "")}
        entry.update(p.get("stats", {}))
        if p.get("published_at"):
            entry["published_at"] = p["published_at"]
        if p.get("url"):
            entry["url"] = p["url"]
        simplified.append(entry)

    return {
        "platform": "douyin",
        "type": "profile_analysis",
        "author": author,
        "total_fetched": len(posts),
        "posts": simplified,
        "aggregate": _aggregate_posts(posts),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze Xiaohongshu/Douyin content via TikHub API",
        add_help=False,
    )
    parser.add_argument("url", nargs="?", default=None, help="URL to analyze")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX_POSTS, dest="max_posts",
                        help=f"Max posts for profile analysis (default: {DEFAULT_MAX_POSTS})")

    args = parser.parse_args()

    if not args.url:
        print(json.dumps({"error": "Usage: analyze.py <url> [--max N]"}))
        return

    # Parse the URL
    parsed = await parse_url(args.url)
    if not parsed:
        print(json.dumps({"error": f"Unrecognized URL: {args.url}"}))
        return

    # Load API token
    token = _load_api_token()
    if not token:
        print(json.dumps({"error": "TIKHUB_API_TOKEN not found in env or ~/.openclaw/openclaw.json"}))
        return

    api = TikHubAPI(token)
    try:
        if parsed.platform == "xiaohongshu":
            if parsed.kind == "note":
                result = await handle_xhs_note(api, parsed.identifier)
            else:
                result = await handle_xhs_profile(api, parsed.identifier, args.max_posts)
        elif parsed.platform == "douyin":
            if parsed.kind == "video":
                result = await handle_douyin_video(api, parsed.identifier)
            else:
                result = await handle_douyin_profile(api, parsed.identifier, args.max_posts)
        else:
            result = {"error": f"Unsupported platform: {parsed.platform}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))
    except httpx.HTTPStatusError as exc:
        print(json.dumps({
            "error": f"API error: {exc.response.status_code} {exc.response.text[:200]}"
        }))
    except httpx.HTTPError as exc:
        print(json.dumps({"error": f"HTTP error: {exc!s}"}))
    finally:
        await api.close()


if __name__ == "__main__":
    asyncio.run(main())
