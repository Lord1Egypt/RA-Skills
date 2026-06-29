"""
Bilibili URL Parser
- Extracts BV/AV/CV IDs from various Bilibili URL formats
- Resolves b23.tv short links to canonical URLs
"""
import re
import logging
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)

# BV号正则: BV + 10位字母数字 (不含IO)
BV_PATTERN = re.compile(r'[Bb][Vv][0-9A-Za-z]{10,}')
# AV号正则: av + 纯数字
AV_PATTERN = re.compile(r'[Aa][Vv](\d{1,12})')
# CV号正则 (专栏): cv + 纯数字
CV_PATTERN = re.compile(r'[Cc][Vv](\d{1,12})')
# 短链接短ID
SHORT_ID_PATTERN = re.compile(r'b23\.tv/([A-Za-z0-9]+)')
# 合集/播放列表
ML_PATTERN = re.compile(r'[Mm][Ll](\d{1,12})')
# 系列
SERIES_PATTERN = re.compile(r'series/(\d{1,12})')

SUPPORTED_DOMAINS = ("bilibili.com", "b23.tv", "www.bilibili.com")


class ParseResult:
    """Result of parsing a Bilibili URL."""
    
    def __init__(self, url: str, media_type: str, media_id: str,
                 raw_id: Optional[str] = None, is_short_link: bool = False):
        self.original_url = url
        self.media_type = media_type  # "video", "column", "playlist", "series"
        self.media_id = media_id      # normalized ID (BV1xx..., cv123, av123)
        self.raw_id = raw_id or media_id
        self.is_short_link = is_short_link

    def to_dict(self) -> Dict:
        return {
            "original_url": self.original_url,
            "media_type": self.media_type,
            "media_id": self.media_id,
            "is_short_link": self.is_short_link,
        }

    @property
    def api_type(self) -> str:
        """Return the type string used in Bilibili API endpoints."""
        return {"video": "video", "column": "article"}.get(self.media_type, self.media_type)


def parse_url(url: str) -> Optional[ParseResult]:
    """
    Parse a Bilibili URL and extract media type + ID.
    
    Supported formats:
    - https://www.bilibili.com/video/BV1xx411c7mD
    - https://b23.tv/BV1xx411c7mD
    - https://b23.tv/abc123 (short link)
    - https://www.bilibili.com/read/cv123456
    - https://www.bilibili.com/video/av123456
    - https://www.bilibili.com/medialist/play/ml123456
    - https://www.bilibili.com/series/123456
    
    Args:
        url: Bilibili URL string.
        
    Returns:
        ParseResult if successfully parsed, None otherwise.
    """
    if not url:
        return None

    # Strip whitespace and normalize
    url = url.strip()
    
    # Check if it's a b23.tv short link
    short_match = SHORT_ID_PATTERN.search(url)
    is_short = short_match is not None
    
    # Try BV pattern (most common for videos)
    bv_match = BV_PATTERN.search(url)
    if bv_match:
        return ParseResult(
            url=url, media_type="video", media_id=bv_match.group(0).upper(),
            is_short_link=is_short
        )
    
    # Try AV pattern
    av_match = AV_PATTERN.search(url)
    if av_match:
        return ParseResult(
            url=url, media_type="video", media_id=f"av{av_match.group(1)}",
            is_short_link=is_short
        )
    
    # Try CV pattern (columns/articles)
    cv_match = CV_PATTERN.search(url)
    if cv_match:
        return ParseResult(
            url=url, media_type="column", media_id=f"cv{cv_match.group(1)}",
            is_short_link=is_short
        )
    
    # Try medialist / playlist
    ml_match = ML_PATTERN.search(url)
    if ml_match:
        return ParseResult(
            url=url, media_type="playlist", media_id=ml_match.group(0),
            is_short_link=is_short
        )
    
    # Try series
    series_match = SERIES_PATTERN.search(url)
    if series_match:
        return ParseResult(
            url=url, media_type="series", media_id=series_match.group(1),
            is_short_link=is_short
        )
    
    # Fallback: check if it's a b23.tv short link
    short_match = re.search(r"b23\.tv/([A-Za-z0-9]+)", url)
    if short_match:
        return ParseResult(
            url=url, media_type="shortlink", media_id=short_match.group(1),
            is_short_link=True
        )
    
    logger.warning("Could not parse URL: %s", url)
    return None


def is_valid_bilibili_url(url: str) -> bool:
    """Quick check if a URL is a valid Bilibili link."""
    return any(domain in url for domain in SUPPORTED_DOMAINS) or "b23.tv" in url


def batch_parse(urls: list) -> list:
    """Parse multiple URLs and return results. Skips invalid ones."""
    results = []
    for url in urls:
        result = parse_url(url)
        if result:
            results.append(result)
    return results


def get_video_id_parts(media_id: str) -> Tuple[str, str]:
    """
    Split a media ID into type prefix and numeric/id part.
    Returns ("bv", "BV1xx...") or ("av", "123456") etc.
    """
    if media_id.upper().startswith("BV"):
        return ("bv", media_id)
    if media_id.lower().startswith("av"):
        return ("av", media_id[2:])
    if media_id.lower().startswith("cv"):
        return ("cv", media_id[2:])
    return ("unknown", media_id)
