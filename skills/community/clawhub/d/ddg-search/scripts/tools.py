from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search(
    query: str,
    max_results: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
Search DuckDuckGo and return formatted results.

Args:
    query: The search query string
    max_results: Maximum number of results to return (default: 10)
    ctx: MCP context for logging

    
    Args:
        query: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "max_results": max_results
    }
    
    return call_api("1777419062294531", "search", arguments)

def fetch_content(
    url: str
) -> Dict[str, Any]:
    """
    
Fetch and parse content from a webpage URL.

Args:
    url: The webpage URL to fetch content from
    ctx: MCP context for logging

    
    Args:
        url: null
    
    Returns:
        null
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777419062294531", "fetch_content", arguments)

