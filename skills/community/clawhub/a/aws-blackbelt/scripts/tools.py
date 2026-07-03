from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_seminars(
    query: str,
    sort_order: Optional[str] = "desc",
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Search AWS Black Belt seminars by keyword.

Args:
    ctx: Context to access MCP features
    query: Search keyword (e.g., "machine learning", "lambda", "s3")
    sort_order: Sort order by published date - "desc" (newest first) or "asc" (oldest first)
    limit: Maximum number of results to return (default: 10, max: 50)

Returns:
    List of seminar information including title, date, PDF and YouTube links
    
    Args:
        query: Search keyword
        sort_order: Sort order
        limit: Max results
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "sort_order": sort_order,
        "limit": limit
    }
    
    return call_api("1777419068962819", "search_seminars", arguments)

def get_seminar_transcript(
    youtube_url: str,
    language: Optional[str] = "ja"
) -> Dict[str, Any]:
    """
    Get transcript from seminar video. Note: Supported only in Japanese.

Args:
    ctx: Context to access MCP features
    youtube_url: YouTube video URL
    language: Language code for transcript (default: "ja" for Japanese)

Returns:
    Seminar transcript
    
    Args:
        youtube_url: YouTube video URL
        language: Language code for transcript (e.g., 'ja')
    
    Returns:
        
    """
    arguments = {
        "youtube_url": youtube_url,
        "language": language
    }
    
    return call_api("1777419068962819", "get_seminar_transcript", arguments)

