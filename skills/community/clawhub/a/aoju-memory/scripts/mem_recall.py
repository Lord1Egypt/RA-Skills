#!/usr/bin/env python3
"""
mem_recall.py — Search long-term memory for relevant context

Usage:
  python3 mem_recall.py "<query>" [--limit 5]

Returns memories, learnings, and past decisions relevant to the query.
Uses keyword + context matching (no embeddings required).
"""
import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"


def search_file(path: Path, query: str, limit: int = 5) -> list[dict]:
    """Search a single file for query matches."""
    if not path.exists():
        return []
    
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    
    query_words = query.lower().split()
    lines = content.split("\n")
    scored_lines = []
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        # Skip headers and empty lines
        if not line.strip() or line.startswith("#"):
            continue
        
        score = 0
        matched_words = 0
        for word in query_words:
            if word in line_lower:
                score += 1
                matched_words += 1
                # Exact phrase match bonus
                if query.lower() in line_lower:
                    score += 3
        
        if matched_words > 0:
            # Context: include surrounding lines
            context_start = max(0, i - 1)
            context_end = min(len(lines), i + 3)
            context = "\n".join(lines[context_start:context_end])
            scored_lines.append({
                "score": score,
                "line": line.strip(),
                "context": context.strip(),
                "file": str(path),
            })
    
    # Sort by score descending, return top matches
    scored_lines.sort(key=lambda x: x["score"], reverse=True)
    return scored_lines[:limit]


def search_memory(query: str, limit: int = 5) -> list[dict]:
    """Search all memory sources."""
    results = []
    
    # Search MEMORY.md
    results.extend(search_file(MEMORY_FILE, query, limit))
    
    # Search recent daily logs (last 7 days)
    if MEMORY_DIR.exists():
        today = datetime.now()
        for days_ago in range(7):
            date = today - timedelta(days=days_ago)
            daily_file = MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md"
            results.extend(search_file(daily_file, query, limit // 2 + 1))
    
    # Search learnings
    if LEARNINGS_DIR.exists():
        for learning_file in sorted(LEARNINGS_DIR.glob("*.md"), reverse=True)[:10]:
            results.extend(search_file(learning_file, query, 2))
    
    # Dedupe by context, sort by score
    seen = set()
    deduped = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        ctx_key = r["context"][:100]
        if ctx_key not in seen:
            seen.add(ctx_key)
            deduped.append(r)
    
    return deduped[:limit]


def format_results(results: list[dict], query: str) -> str:
    if not results:
        return f"No memories found for: {query}"
    
    output = [f"## Memory Search: {query}\n"]
    output.append(f"Found {len(results)} relevant memories:\n")
    
    for i, r in enumerate(results, 1):
        rel_path = r["file"].replace(str(WORKSPACE) + "/", "")
        output.append(f"---")
        output.append(f"[{rel_path}] (score: {r['score']})")
        output.append(r["context"])
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search memory")
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--format", default="text", choices=["text", "json"])
    args = parser.parse_args()
    
    if not args.query:
        print("Usage: mem_recall.py <query>")
        sys.exit(1)
    
    results = search_memory(args.query, args.limit)
    
    if args.format == "json":
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_results(results, args.query))
