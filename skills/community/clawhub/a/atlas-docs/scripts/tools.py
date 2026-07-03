from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_docs(
) -> Dict[str, Any]:
    """
    Lists all available documentation libraries and frameworks. Use this as your first step to discover available documentation sets. Returns name, description and source url for each documentation set. Required before using other documentation tools since you need the docName.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659387395", "list_docs", arguments)

def search_docs(
    docName: str,
    query: str
) -> Dict[str, Any]:
    """
    Searches a documentation set for specific content. Use this to find pages containing particular keywords, concepts, or topics. Returns matching pages ranked by relevance with their paths and descriptions. Follow up with get_docs_page to get full content.
    
    Args:
        docName: Name of the documentation set
        query: Search query to find relevant pages within the documentation set
    
    Returns:
        
    """
    arguments = {
        "docName": docName,
        "query": query
    }
    
    return call_api("1777316659387395", "search_docs", arguments)

def get_docs_index(
    docName: str
) -> Dict[str, Any]:
    """
    Retrieves a condensed, LLM-friendly index of the pages in a documentation set. Use this for initial exploration to understand what's covered and identify relevant pages. Returns a markdown page with a list of available pages. Follow up with get_docs_page to get full content.
    
    Args:
        docName: Name of the documentation set
    
    Returns:
        
    """
    arguments = {
        "docName": docName
    }
    
    return call_api("1777316659387395", "get_docs_index", arguments)

def get_docs_page(
    docName: str,
    pagePath: str
) -> Dict[str, Any]:
    """
    Retrieves a specific documentation page's content using its relative path. Use this to get detailed information about a known topic, after identifying the relevant page through get_docs_index or search_docs. Returns the complete content of a single documentation page.
    
    Args:
        docName: Name of the documentation set
        pagePath: The root-relative path of the specific documentation page (e.g., '/guides/getting-started', '/api/authentication')
    
    Returns:
        
    """
    arguments = {
        "docName": docName,
        "pagePath": pagePath
    }
    
    return call_api("1777316659387395", "get_docs_page", arguments)

def get_docs_full(
    docName: str
) -> Dict[str, Any]:
    """
    Retrieves the complete documentation content in a single consolidated file. Use this when you need comprehensive knowledge or need to analyze the full documentation context. Returns a large volume of text - consider using get_docs_page or search_docs for targeted information.
    
    Args:
        docName: Name of the documentation set
    
    Returns:
        
    """
    arguments = {
        "docName": docName
    }
    
    return call_api("1777316659387395", "get_docs_full", arguments)

