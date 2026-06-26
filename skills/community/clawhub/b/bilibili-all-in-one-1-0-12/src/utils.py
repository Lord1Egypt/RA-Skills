"""Shared utility functions for the Bilibili All-in-One skill."""

import re
import os
import json
import time
import hashlib
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs


# Bilibili API endpoints
API_BASE = "https://api.bilibili.com"
API_HOT = f"{API_BASE}/x/web-interface/popular"
API_TRENDING = f"{API_BASE}/x/web-interface/popular/series/list"
API_WEEKLY = f"{API_BASE}/x/web-interface/popular/series/one"
API_RANK = f"{API_BASE}/x/web-interface/ranking/v2"
API_VIDEO_INFO = f"{API_BASE}/x/web-interface/view"
API_VIDEO_DETAIL = f"{API_BASE}/x/web-interface/view/detail"
API_PLAY_URL = f"{API_BASE}/x/player/playurl"
API_DANMAKU = f"{API_BASE}/x/v1/dm/list.so"
API_SUBTITLE = f"{API_BASE}/x/player/v2"
API_STAT = f"{API_BASE}/x/relation/stat"
API_SEARCH = f"{API_BASE}/x/web-interface/search/type"

# Video quality mapping
QUALITY_MAP = {
    "360p": 16,
    "480p": 32,
    "720p": 64,
    "1080p": 80,
    "1080p+": 112,
    "4k": 120,
}

# Category TID mapping
CATEGORY_TID = {
    "all": 0,
    "anime": 1,
    "music": 3,
    "dance": 129,
    "game": 4,
    "tech": 188,
    "life": 160,
    "food": 211,
    "car": 223,
    "fashion": 155,
    "entertainment": 5,
    "movie": 23,
    "tv": 11,
}

# Default headers
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Origin": "https://www.bilibili.com",
}


def extract_bvid(url_or_bvid: str) -> Optional[str]:
    """Extract BV ID from a Bilibili URL or return it directly if already a BV ID.

    Args:
        url_or_bvid: Bilibili video URL or BV number.

    Returns:
        The extracted BV ID, or None if extraction fails.
    """
    if not url_or_bvid:
        return None

    # Already a BV ID
    bv_match = re.match(r"^(BV[a-zA-Z0-9]+)$", url_or_bvid.strip())
    if bv_match:
        return bv_match.group(1)

    # Extract from URL
    patterns = [
        r"bilibili\.com/video/(BV[a-zA-Z0-9]+)",
        r"b23\.tv/(BV[a-zA-Z0-9]+)",
        r"bilibili\.com/bangumi/play/(BV[a-zA-Z0-9]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_bvid)
        if match:
            return match.group(1)

    return None


def extract_aid(url_or_aid: str) -> Optional[int]:
    """Extract AV ID from a Bilibili URL or return it directly.

    Args:
        url_or_aid: Bilibili video URL or AV number.

    Returns:
        The extracted AV ID as integer, or None if extraction fails.
    """
    if not url_or_aid:
        return None

    # Already an AV ID
    av_match = re.match(r"^av(\d+)$", url_or_aid.strip(), re.IGNORECASE)
    if av_match:
        return int(av_match.group(1))

    # Extract from URL
    match = re.search(r"bilibili\.com/video/av(\d+)", url_or_aid)
    if match:
        return int(match.group(1))

    return None


def format_duration(seconds: int) -> str:
    """Format duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted duration string (e.g., '1:23:45' or '12:34').
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_number(num: int) -> str:
    """Format a large number to a human-readable string.

    Args:
        num: The number to format.

    Returns:
        Formatted number string (e.g., '1.2万', '3.4亿').
    """
    if num >= 100_000_000:
        return f"{num / 100_000_000:.1f}亿"
    if num >= 10_000:
        return f"{num / 10_000:.1f}万"
    return str(num)


def ensure_dir(directory: str) -> str:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Path to the directory.

    Returns:
        The absolute path to the directory.
    """
    abs_path = os.path.abspath(directory)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def sanitize_filename(filename: str) -> str:
    """Sanitize a string for use as a filename.

    Args:
        filename: The original filename.

    Returns:
        Sanitized filename safe for all operating systems.
    """
    # Remove or replace invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    sanitized = re.sub(invalid_chars, "_", filename)
    # Remove trailing dots and spaces
    sanitized = sanitized.strip(". ")
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    return sanitized or "untitled"


def generate_wbi_sign(params: Dict[str, Any], img_key: str, sub_key: str) -> Dict[str, Any]:
    """Generate WBI signature for Bilibili API requests.

    Args:
        params: Request parameters.
        img_key: WBI img key.
        sub_key: WBI sub key.

    Returns:
        Parameters dict with wts and w_rid added.
    """
    mixin_key_enc_tab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
        27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
        37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
        22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
    ]

    raw_key = img_key + sub_key
    mixin_key = "".join(raw_key[i] for i in mixin_key_enc_tab)[:32]

    params["wts"] = int(time.time())
    # Sort parameters
    sorted_params = dict(sorted(params.items()))
    query = "&".join(f"{k}={v}" for k, v in sorted_params.items())
    wbi_sign = hashlib.md5((query + mixin_key).encode()).hexdigest()
    params["w_rid"] = wbi_sign

    return params


def parse_video_url(url: str) -> Dict[str, Any]:
    """Parse a video URL and extract platform and identifier.

    Args:
        url: Video URL (supports Bilibili and YouTube).

    Returns:
        Dict with 'platform' and 'id' keys.
    """
    parsed = urlparse(url)

    # Bilibili
    if "bilibili.com" in parsed.hostname or "b23.tv" in parsed.hostname:
        bvid = extract_bvid(url)
        aid = extract_aid(url)
        return {
            "platform": "bilibili",
            "bvid": bvid,
            "aid": aid,
            "url": url,
        }

    # YouTube
    if "youtube.com" in parsed.hostname or "youtu.be" in parsed.hostname:
        if "youtu.be" in parsed.hostname:
            video_id = parsed.path.strip("/")
        else:
            qs = parse_qs(parsed.query)
            video_id = qs.get("v", [None])[0]
        return {
            "platform": "youtube",
            "video_id": video_id,
            "url": url,
        }

    return {"platform": "unknown", "url": url}
