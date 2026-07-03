from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_user_info(
    mid: int
) -> Dict[str, Any]:
    """
    Get information about a Bilibili user
    
    Args:
        mid: User's numeric ID
    
    Returns:
        
    """
    arguments = {
        "mid": mid
    }
    
    return call_api("1777316659451907", "get_user_info", arguments)

def get_video_info(
    bvid: str
) -> Dict[str, Any]:
    """
    Get detailed information about a Bilibili video
    
    Args:
        bvid: Bilibili video ID (BVID)
    
    Returns:
        
    """
    arguments = {
        "bvid": bvid
    }
    
    return call_api("1777316659451907", "get_video_info", arguments)

def search_videos(
    keyword: str,
    page: Optional[int] = 1.0,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Search for videos on Bilibili
    
    Args:
        keyword: Keyword to search for
        page: Page number, defaults to 1
        count: Number of results to return, default 10, maximum 20
    
    Returns:
        
    """
    arguments = {
        "keyword": keyword,
        "page": page,
        "count": count
    }
    
    return call_api("1777316659451907", "search_videos", arguments)

