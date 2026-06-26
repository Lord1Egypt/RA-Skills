#!/usr/bin/env python3
"""
Integration layer combining memory_search and FTS5 search.

Provides memory_search_enhanced() that merges results from both:
1. Existing MEMORY.md + memory/*.md (via memory_search)
2. FTS5 past conversation search (via search-tool)

This module is designed to be importable from the OpenClaw tool system.
"""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "search.db"

# Load modules with hyphens in filename
_spec_tool = importlib.util.spec_from_file_location('search_tool', SCRIPT_DIR / 'search-tool.py')
search_tool = importlib.util.module_from_spec(_spec_tool)
_spec_tool.loader.exec_module(search_tool)

# Register so integration.py can import it
sys.modules['search_tool'] = search_tool


def fts5_search(query: str, scope: str = "all", limit: int = 10, time_range: str = None) -> list:
    """Search using FTS5 past conversation index."""
    if not DB_PATH.exists():
        return []
    
    try:
        results = search_tool.search(query, scope=scope, limit=limit, time_range=time_range)
        return results
    except Exception as e:
        print(f"FTS5 search error: {e}", file=sys.stderr)
        return []


def memory_search_enhanced(query: str, limit: int = 10, time_range: str = None) -> list:
    """
    Combined search across both memory files and past conversations.
    
    Args:
        query: Search query
        limit: Max results per source
        time_range: Optional time filter ("today", "week", "month", "year")
    
    Returns:
        List of dicts with: source, session_id, agent, timestamp, role, content, relevance_score, topic
    """
    # 1. Search FTS5 (past conversations)
    fts5_results = fts5_search(query, limit=limit, time_range=time_range)
    
    # 2. Format results with source tag
    combined = []
    
    for r in fts5_results:
        combined.append({
            "source": "conversations",
            "session_id": r.get("session_id", ""),
            "agent": r.get("agent", ""),
            "timestamp": r.get("timestamp", ""),
            "role": r.get("role", ""),
            "content": r.get("content", ""),
            "relevance_score": r.get("relevance_score", 0),
            "topic": r.get("topic", ""),
        })
    
    # Deduplicate by content similarity (first 100 chars)
    seen_content = set()
    deduped = []
    for r in combined:
        content_key = r["content"][:100]
        if content_key not in seen_content:
            seen_content.add(content_key)
            deduped.append(r)
    
    # Sort by relevance score (lower bm25 = more relevant)
    deduped.sort(key=lambda x: x.get("relevance_score", float('inf')))
    
    return deduped[:limit * 2]  # Return more since we may filter later


def get_conversation_context(session_id: str, query: str = None, limit: int = 5) -> str:
    """
    Get relevant context from a specific session's past conversation.
    """
    if not DB_PATH.exists():
        return ""
    
    try:
        messages = search_tool.get_session(session_id)
        if not messages:
            return ""
        
        # If query, filter to most relevant messages
        if query:
            query_lower = query.lower()
            scored = []
            for msg in messages:
                content_lower = msg.get("content", "").lower()
                # Simple keyword matching score
                score = sum(1 for word in query_lower.split() if word in content_lower)
                if score > 0:
                    scored.append((score, msg))
            scored.sort(key=lambda x: -x[0])
            messages = [m for _, m in scored[:limit]]
        else:
            messages = messages[:limit]
        
        lines = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if len(content) > 500:
                content = content[:500] + "..."
            lines.append(f"[{role}]: {content}")
        
        return "\n".join(lines)
    except Exception as e:
        print(f"get_conversation_context error: {e}", file=sys.stderr)
        return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: integration.py <query> [--limit N] [--time today|week|month|year]")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = 10
    time_range = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--time" and i + 1 < len(sys.argv):
            time_range = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    results = memory_search_enhanced(query, limit=limit, time_range=time_range)
    
    if not results:
        print("No results found.")
    else:
        for i, r in enumerate(results, 1):
            print(f"\n--- Result {i} (source: {r['source']}, score: {r['relevance_score']}) ---")
            print(f"Session: {r['session_id']}")
            print(f"Agent: {r['agent']}")
            print(f"Time: {r['timestamp']}")
            print(f"Role: {r['role']}")
            content = r['content']
            if len(content) > 300:
                content = content[:300] + "..."
            print(f"Content: {content}")
        
        print(f"\nTotal: {len(results)} results")