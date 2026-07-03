from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_help(
    query: str,
    max_suggestions: Optional[int] = 3.0
) -> Dict[str, Any]:
    """
    Find ANSYS Fluent documentation URLs for your query.

This tool helps you navigate to the right online documentation.
Use WebFetch to retrieve the actual content from the returned URLs.

Args:
    query: Search term (e.g., "flamelet model", "read case", "turbulence")
    max_suggestions: Maximum manual section suggestions to return (default: 3)

Returns:
    URLs and navigation hints for finding the documentation
    
    Args:
        query: null
        max_suggestions: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "max_suggestions": max_suggestions
    }
    
    return call_api("1777419075828739", "search_help", arguments)

def list_topics(
) -> Dict[str, Any]:
    """
    List common Fluent topics with quick documentation links.

Returns:
    List of pre-mapped topics for faster navigation
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419075828739", "list_topics", arguments)

def get_manual_link(
    manual: str,
    section: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get direct link to a specific Fluent manual or section.

Args:
    manual: Manual name (user_guide, tui, theory, udf)
    section: Optional section path (e.g., "turbulence", "file/read-case")

Returns:
    Direct URL to the manual or section
    
    Args:
        manual: null
        section: null
    
    Returns:
        null
    """
    arguments = {
        "manual": manual,
        "section": section
    }
    
    return call_api("1777419075828739", "get_manual_link", arguments)

