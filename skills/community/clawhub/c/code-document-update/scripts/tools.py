from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def resolve_library_id(
    libraryName: str
) -> Dict[str, Any]:
    """
    Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries.

You MUST call this function before 'get-library-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

Selection Process:
1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
- Name similarity to the query (exact matches prioritized)
- Description relevance to the query's intent
- Documentation coverage (prioritize libraries with higher Code Snippet counts)
- Source reputation (consider libraries with High or Medium reputation more authoritative)
- Benchmark Score: Quality indicator (100 is the highest score)

Response Format:
- Return the selected library ID in a clearly marked section
- Provide a brief explanation for why this library was chosen
- If multiple good matches exist, acknowledge this but proceed with the most relevant one
- If no good matches exist, clearly state this and suggest query refinements

For ambiguous queries, request clarification before proceeding with a best-guess match.
    
    Args:
        libraryName: Library name to search for and retrieve a Context7-compatible library ID.
    
    Returns:
        
    """
    arguments = {
        "libraryName": libraryName
    }
    
    return call_api("1777316659576835", "resolve_library_id", arguments)

def get_library_docs(
    context7CompatibleLibraryID: str,
    mode: Optional[str] = "code",
    topic: Optional[str] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    Fetches up-to-date documentation for a library. You must call 'resolve-library-id' first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query. Use mode='code' (default) for API references and code examples, or mode='info' for conceptual guides, narrative information, and architectural questions.
    
    Args:
        context7CompatibleLibraryID: Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') retrieved from 'resolve-library-id' or directly from user query in the format '/org/project' or '/org/project/version'.
        mode: Documentation mode: 'code' for API references and code examples (default), 'info' for conceptual guides, narrative information, and architectural questions.
        topic: Topic to focus documentation on (e.g., 'hooks', 'routing').
        page: Page number for pagination (start: 1, default: 1). If the context is not sufficient, try page=2, page=3, page=4, etc. with the same topic.
    
    Returns:
        
    """
    arguments = {
        "context7CompatibleLibraryID": context7CompatibleLibraryID,
        "mode": mode,
        "topic": topic,
        "page": page
    }
    
    return call_api("1777316659576835", "get_library_docs", arguments)

