"""
Bilibili API Client
- Fetches video metadata, subtitle URLs, danmaku data
- Implements rate limiting (1s min interval) and exponential backoff retry (max 3)
- Local cache with 24h TTL
"""
import json
import time
import hashlib
import logging
import os
from typing import Optional, Dict, Any
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Rate limiting state
_last_request_time: float = 0.0
_MIN_INTERVAL = 1.0  # seconds

# Cache config
CACHE_DIR = os.path.expanduser("~/.openclaw/data/bilibili-digest/cache")
CACHE_TTL_HOURS = 24

# User-Agent to mimic browser
_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bilibili.com/",
}

# API Endpoints
API_VIDEO_INFO = "https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
API_VIDEO_INFO_AV = "https://api.bilibili.com/x/web-interface/view?aid={aid}"
API_PLAYER_WBI = "https://api.bilibili.com/x/player/v2?bvid={bvid}"
API_DANMAKU = "https://api.bilibili.com/x/v1/dm/list.so?oid={oid}"
API_SUBTITLE = "https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}"


def _rate_limit():
    """Ensure minimum interval between API calls."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _last_request_time = time.time()


def _cache_key(url: str) -> str:
    """Generate a cache key from URL."""
    return hashlib.md5(url.encode()).hexdigest()


def _get_cache_path(key: str) -> str:
    """Get the cache file path for a given key."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{key}.json")


def _check_cache(url: str) -> Optional[Dict]:
    """Check if a cached response exists and is still valid."""
    key = _cache_key(url)
    cache_path = _get_cache_path(key)
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, "r") as f:
            data = json.load(f)
        cached_time = datetime.fromisoformat(data.get("_cached_at", "2000-01-01"))
        if datetime.now() - cached_time < timedelta(hours=CACHE_TTL_HOURS):
            logger.debug("Cache hit for %s", url)
            return data.get("response")
        else:
            logger.debug("Cache expired for %s", url)
            return None
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def _write_cache(url: str, response: Dict):
    """Write response to cache."""
    try:
        key = _cache_key(url)
        cache_path = _get_cache_path(key)
        data = {"_cached_at": datetime.now().isoformat(), "response": response}
        with open(cache_path, "w") as f:
            json.dump(data, f, ensure_ascii=False)
    except OSError as e:
        logger.warning("Failed to write cache: %s", e)


def _api_request(url: str, max_retries: int = 3, use_cache: bool = True) -> Optional[Dict]:
    """
    Make an HTTP request to a Bilibili API endpoint with rate limiting and retry.
    
    Args:
        url: API endpoint URL.
        max_retries: Maximum number of retry attempts (default 3).
        use_cache: Whether to check/write cache (default True).
        
    Returns:
        Parsed JSON response dict, or None on failure.
    """
    # Check cache first
    if use_cache:
        cached = _check_cache(url)
        if cached:
            return cached

    last_error = None
    for attempt in range(max_retries):
        try:
            _rate_limit()
            req = Request(url, headers=_DEFAULT_HEADERS)
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            if data.get("code") == 0:
                response = data.get("data", {})
                if use_cache:
                    _write_cache(url, response)
                return response
            else:
                logger.warning("API returned error code %s: %s (attempt %d/%d)",
                               data.get("code"), data.get("message", ""), attempt + 1, max_retries)
                # Non-retryable errors
                if data.get("code") in (-404, -403, -412):
                    return None
                last_error = f"API code {data.get('code')}: {data.get('message', '')}"
                
        except HTTPError as e:
            last_error = f"HTTP {e.code}"
            logger.warning("HTTP error on attempt %d/%d: %s", attempt + 1, max_retries, e.code)
            if e.code in (403, 404):
                return None
        except (URLError, TimeoutError, OSError) as e:
            last_error = str(e)
            logger.warning("Request error on attempt %d/%d: %s", attempt + 1, max_retries, e)
        
        if attempt < max_retries - 1:
            # Exponential backoff: 1s, 2s, 4s
            time.sleep(2 ** attempt)
    
    logger.error("All %d retries exhausted for %s: %s", max_retries, url, last_error)
    return None


def get_video_info(bvid: Optional[str] = None, avid: Optional[str] = None) -> Optional[Dict]:
    """
    Get video metadata including title, author, duration, view count, tags.
    
    Args:
        bvid: BV ID (e.g., "BV1xx411c7mD")
        avid: AV ID (e.g., "123456")
        
    Returns:
        Video info dict with keys: title, author, duration, etc.
    """
    if bvid:
        url = API_VIDEO_INFO.format(bvid=bvid)
    elif avid:
        url = API_VIDEO_INFO_AV.format(aid=avid)
    else:
        logger.error("Either bvid or avid must be provided")
        return None
    
    data = _api_request(url)
    if not data:
        return None
    
    return {
        "title": data.get("title", ""),
        "author": data.get("owner", {}).get("name", ""),
        "author_mid": data.get("owner", {}).get("mid", 0),
        "duration_seconds": data.get("duration", 0),
        "publish_date": data.get("pubdate", 0),
        "view_count": data.get("stat", {}).get("view", 0),
        "like_count": data.get("stat", {}).get("like", 0),
        "danmaku_count": data.get("stat", {}).get("danmaku", 0),
        "category": data.get("tname", ""),
        "cover_url": data.get("pic", ""),
        "description": data.get("desc", ""),
        "tags": [t.get("tag_name", "") for t in (data.get("tags") or [])],
        "has_cc": False,  # Will be updated by subtitle check
        "cid": data.get("cid", 0),
    }


def get_subtitle(bvid: str, cid: int) -> Optional[Dict]:
    """
    Fetch CC subtitle data for a video.
    
    Args:
        bvid: BV ID.
        cid: The CID (chapter ID) for the video.
        
    Returns:
        Subtitle data dict with segments, or None if unavailable.
    """
    url = API_SUBTITLE.format(bvid=bvid, cid=cid)
    data = _api_request(url)
    if not data:
        return None
    
    subtitle_info = data.get("subtitle", {})
    if not subtitle_info:
        return None
    
    subtitle_urls = subtitle_info.get("subtitles", [])
    if not subtitle_urls:
        return None
    
    # Prefer Chinese subtitles
    preferred_lan = "zh-CN"
    subtitle_url = None
    for sub in subtitle_urls:
        if sub.get("lan_doc", "").startswith("中文"):
            subtitle_url = sub.get("subtitle_url", "")
            break
    
    if not subtitle_url:
        subtitle_url = subtitle_urls[0].get("subtitle_url", "")
    
    if not subtitle_url:
        return None
    
    # Ensure full URL
    if subtitle_url.startswith("//"):
        subtitle_url = "https:" + subtitle_url
    elif subtitle_url.startswith("/"):
        subtitle_url = "https:" + subtitle_url
    
    # Fetch actual subtitle content
    sub_data = _api_request(subtitle_url)
    return sub_data


def get_danmaku(oid: int, segment_num: int = 1) -> Optional[list]:
    """
    Fetch danmaku (bullet comments) for a video segment.
    
    Args:
        oid: The object ID (usually CID) for danmaku.
        segment_num: Danmaku segment number (1 = first 6 min).
        
    Returns:
        List of danmaku entries with time and content, or None.
    """
    url = API_DANMAKU.format(oid=oid)
    data = _api_request(url, use_cache=True)
    if data and isinstance(data, dict):
        return data.get("dm", [])
    return None


def clean_cache(max_age_hours: int = 72):
    """Remove cache files older than max_age_hours."""
    if not os.path.exists(CACHE_DIR):
        return
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    for fname in os.listdir(CACHE_DIR):
        fpath = os.path.join(CACHE_DIR, fname)
        mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
        if mtime < cutoff:
            os.remove(fpath)
            logger.debug("Removed expired cache: %s", fname)
