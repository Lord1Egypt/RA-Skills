from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_subtitles(
    url: str
) -> Dict[str, Any]:
    """
    获取B站视频的字幕内容

Args:
    url: B站视频链接，例如 https://www.bilibili.com/video/BV1x341177NN
    
Returns:
    列表形式的字幕内容，按语言分组

    
    Args:
        url: null
    
    Returns:
        
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777419074164739", "get_subtitles", arguments)

def get_danmaku(
    url: str
) -> Dict[str, Any]:
    """
    获取B站视频的弹幕内容

Args:
    url: B站视频链接，例如 https://www.bilibili.com/video/BV1x341177NN
    
Returns:
    列表形式的弹幕内容

    
    Args:
        url: null
    
    Returns:
        
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777419074164739", "get_danmaku", arguments)

def get_comments(
    url: str
) -> Dict[str, Any]:
    """
    获取B站视频的热门评论

Args:
    url: B站视频链接，例如 https://www.bilibili.com/video/BV1x341177NN
    
Returns:
    列表形式的热门评论

    
    Args:
        url: null
    
    Returns:
        
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777419074164739", "get_comments", arguments)

