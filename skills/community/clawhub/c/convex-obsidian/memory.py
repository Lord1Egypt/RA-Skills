#!/usr/bin/env python3
"""
Hybrid Memory Search: Convex (Hot) + Obsidian (Deep)
HTTP API version - no Convex CLI needed
"""

import os
import sys
import json
import re
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class MemoryResult:
    source: str
    content: str
    timestamp: float
    relevance: float
    metadata: Dict[str, Any]
    path: Optional[str] = None

def get_convex_url() -> str:
    """Get Convex deployment URL."""
    return os.getenv(
        "CONVEX_DEPLOYMENT_URL",
        "https://gallant-jackal-80.convex.cloud"
    )

def convex_query(action: str, args: Dict) -> Any:
    """Query Convex via HTTP API."""
    url = f"{get_convex_url()}/api/query"
    headers = {"Content-Type": "application/json"}
    payload = {
        "path": action,
        "args": args
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("value")
    except Exception as e:
        print(f"Convex API error: {e}")
        return None

def convex_mutation(action: str, args: Dict) -> Any:
    """Run Convex mutation via HTTP API."""
    url = f"{get_convex_url()}/api/mutation"
    headers = {"Content-Type": "application/json"}
    payload = {
        "path": action,
        "args": args
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("value")
    except Exception as e:
        print(f"Convex API error: {e}")
        return None

def search_convex(query: str, limit: int = 10, session_id: Optional[str] = None) -> List[MemoryResult]:
    """Search recent memories in Convex."""
    results = convex_query("memory:searchMemories", {
        "query": query,
        "limit": limit,
        **({"sessionId": session_id} if session_id else {})
    })
    
    if not results:
        return []
    
    memories = []
    for r in results:
        memories.append(MemoryResult(
            source="convex",
            content=r.get("content", ""),
            timestamp=r.get("timestamp", 0) / 1000,
            relevance=r.get("score", 1.0),
            metadata={
                "tags": r.get("tags", []),
                "importance": r.get("importance", 5),
                "sessionId": r.get("sessionId"),
            }
        ))
    
    return memories

def search_obsidian(query: str, limit: int = 10, vault_path: str = "~/Vault") -> List[MemoryResult]:
    """Search Obsidian vault."""
    vault = Path(vault_path).expanduser()
    
    if not vault.exists():
        return []
    
    results = []
    query_terms = query.lower().split()
    
    for md_file in vault.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            score = 0
            for term in query_terms:
                if term in content_lower:
                    score += content_lower.count(term)
            
            if score > 0:
                mtime = md_file.stat().st_mtime
                preview = content[:500].replace('\n', ' ')
                
                results.append(MemoryResult(
                    source="obsidian",
                    content=preview,
                    timestamp=mtime,
                    relevance=score,
                    metadata={
                        "full_path": str(md_file),
                        "filename": md_file.name,
                    },
                    path=str(md_file.relative_to(vault))
                ))
        except Exception:
            continue
    
    results.sort(key=lambda x: x.relevance, reverse=True)
    return results[:limit]

def hybrid_search(
    query: str,
    limit: int = 10,
    session_id: Optional[str] = None,
    vault_path: str = "~/Vault",
    convex_weight: float = 0.6,
    obsidian_weight: float = 0.4
) -> List[MemoryResult]:
    """Hybrid search: Convex + Obsidian."""
    convex_results = search_convex(query, limit=limit, session_id=session_id)
    obsidian_results = search_obsidian(query, limit=limit, vault_path=vault_path)
    
    # Normalize scores
    if convex_results:
        max_conv = max(r.relevance for r in convex_results) or 1
        for r in convex_results:
            r.relevance = (r.relevance / max_conv) * convex_weight
    
    if obsidian_results:
        max_obs = max(r.relevance for r in obsidian_results) or 1
        for r in obsidian_results:
            r.relevance = (r.relevance / max_obs) * obsidian_weight
    
    combined = convex_results + obsidian_results
    combined.sort(key=lambda x: x.relevance, reverse=True)
    
    return combined[:limit]

def save_to_convex(
    content: str,
    session_id: str,
    source: str = "conversation",
    tags: List[str] = None,
    importance: int = 5,
    metadata: Dict = None
) -> str:
    """Save a memory to Convex."""
    result = convex_mutation("memory:saveMemory", {
        "sessionId": session_id,
        "content": content,
        "source": source,
        "tags": tags or [],
        "importance": importance,
        "metadata": metadata or {}
    })
    
    return result or "error"

def save_to_obsidian(
    content: str,
    title: str,
    folder: str = "01-Inbox",
    tags: List[str] = None,
    vault_path: str = "~/Vault"
) -> str:
    """Save a note to Obsidian vault."""
    vault = Path(vault_path).expanduser()
    target_dir = vault / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')
    filename = f"{date_str}-{safe_title}.md"
    filepath = target_dir / filename
    
    tags_str = ' '.join(f'#{tag}' for tag in (tags or []))
    note = f"""# {title}

{tags_str}

Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

{content}
"""
    
    filepath.write_text(note, encoding='utf-8')
    return str(filepath)

def get_stats() -> Dict:
    """Get memory statistics."""
    return convex_query("memory:stats", {}) or {}

def format_result(r: MemoryResult, index: int) -> str:
    """Format a search result for display."""
    date_str = datetime.fromtimestamp(r.timestamp).strftime("%Y-%m-%d %H:%M")
    source_icon = "🔥" if r.source == "convex" else "📚"
    
    lines = [
        f"{index}. {source_icon} [{r.source.upper()}] (relevance: {r.relevance:.2f})",
        f"   Date: {date_str}",
    ]
    
    if r.path:
        lines.append(f"   File: {r.path}")
    
    if r.metadata.get("tags"):
        lines.append(f"   Tags: {', '.join(r.metadata['tags'])}")
    
    content = r.content.replace('\n', ' ')[:200]
    lines.append(f"   {content}...")
    lines.append("")
    
    return '\n'.join(lines)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Hybrid Memory Search")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-n", "--limit", type=int, default=10)
    search_parser.add_argument("--session", help="Session ID filter")
    search_parser.add_argument("--vault", default="~/Vault", help="Vault path")
    
    save_parser = subparsers.add_parser("save", help="Save memory")
    save_parser.add_argument("content", help="Content to save")
    save_parser.add_argument("--session", required=True, help="Session ID")
    save_parser.add_argument("--source", default="conversation")
    save_parser.add_argument("--tags", nargs="+", default=[])
    save_parser.add_argument("--importance", type=int, default=5)
    
    save_obs_parser = subparsers.add_parser("save-obsidian", help="Save to Obsidian")
    save_obs_parser.add_argument("content", help="Content to save")
    save_obs_parser.add_argument("--title", required=True)
    save_obs_parser.add_argument("--folder", default="01-Inbox")
    save_obs_parser.add_argument("--tags", nargs="+", default=[])
    
    subparsers.add_parser("stats", help="Show statistics")
    
    args = parser.parse_args()
    
    if args.command == "search":
        results = hybrid_search(
            args.query,
            limit=args.limit,
            session_id=args.session,
            vault_path=args.vault
        )
        
        if not results:
            print("No results found.")
            sys.exit(0)
        
        print(f"\n🔍 Search results for: '{args.query}'\n")
        for i, r in enumerate(results, 1):
            print(format_result(r, i))
    
    elif args.command == "save":
        result = save_to_convex(
            args.content,
            args.session,
            source=args.source,
            tags=args.tags,
            importance=args.importance
        )
        print(f"✅ Saved to Convex: {result}")
    
    elif args.command == "save-obsidian":
        filepath = save_to_obsidian(
            args.content,
            args.title,
            folder=args.folder,
            tags=args.tags
        )
        print(f"✅ Saved to Obsidian: {filepath}")
    
    elif args.command == "stats":
        stats = get_stats()
        print("\n📊 Memory Statistics\n")
        if stats:
            print(f"Total memories: {stats.get('totalMemories', 0)}")
            print(f"Recent (30d): {stats.get('recentMemories', 0)}")
            print(f"Search entries: {stats.get('totalSearchEntries', 0)}")
            print(f"Avg importance: {stats.get('avgImportance', 0):.2f}")
        else:
            print("Could not fetch stats. Is Convex deployed?")
    
    else:
        parser.print_help()
