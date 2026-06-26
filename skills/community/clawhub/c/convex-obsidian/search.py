#!/usr/bin/env python3
"""
Enhanced Memory Search - Combina Convex (hot) + Arquivos locais (deep)
Substitui/estende memory_search para incluir Convex
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import List, Dict, Any

CONVEX_URL = os.getenv("CONVEX_DEPLOYMENT_URL", "https://energized-goshawk-977.convex.cloud")
MEMORY_DIR = "/home/andrey/.openclaw/workspace/memory"

def search_convex(query: str, limit: int = 5) -> List[Dict]:
    """Busca memórias no Convex."""
    try:
        resp = requests.post(
            f"{CONVEX_URL}/api/query",
            json={"path": "memory:searchMemories", "args": {"query": query, "limit": limit}},
            timeout=10
        )
        if resp.status_code == 200:
            results = resp.json().get("value", [])
            formatted = []
            for r in results:
                formatted.append({
                    "path": f"convex://{r.get('_id', 'memory')}",
                    "startLine": 1,
                    "endLine": 1,
                    "score": r.get("score", 0.5),
                    "snippet": f"[CONVEX - {r.get('source', 'unknown')}] {r.get('content', '')[:300]}...",
                    "source": "convex",
                    "timestamp": r.get("timestamp"),
                    "tags": r.get("tags", [])
                })
            return formatted
    except Exception as e:
        print(f"Convex search error: {e}", file=sys.stderr)
    return []

def search_local_files(query: str, limit: int = 5) -> List[Dict]:
    """Busca simples nos arquivos de memória locais."""
    results = []
    query_lower = query.lower()
    
    memory_path = Path(MEMORY_DIR)
    if not memory_path.exists():
        return results
    
    for md_file in sorted(memory_path.glob("*.md"), reverse=True):
        try:
            content = md_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            if query_lower in content_lower:
                # Find line numbers
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        start = max(0, i - 2)
                        end = min(len(lines), i + 5)
                        snippet = '\n'.join(lines[start:end])
                        
                        results.append({
                            "path": str(md_file),
                            "startLine": start + 1,
                            "endLine": end,
                            "score": 0.7,
                            "snippet": snippet[:500],
                            "source": "local"
                        })
                        break
                
                if len(results) >= limit:
                    break
        except:
            continue
    
    return results[:limit]

def hybrid_search(query: str, limit: int = 10) -> Dict:
    """Busca híbrida: Convex + Arquivos locais."""
    convex_results = search_convex(query, limit=limit // 2)
    local_results = search_local_files(query, limit=limit // 2)
    
    # Combina e ordena por score
    combined = convex_results + local_results
    combined.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    return {
        "results": combined[:limit],
        "sources": {
            "convex": len(convex_results),
            "local": len(local_results)
        }
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", "-n", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    results = hybrid_search(args.query, limit=args.limit)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"🔍 Resultados para: '{args.query}'")
        print(f"   Fontes: {results['sources']['convex']} Convex + {results['sources']['local']} local\n")
        
        for i, r in enumerate(results["results"], 1):
            source_icon = "🔥" if r.get("source") == "convex" else "📄"
            print(f"{i}. {source_icon} {r['path']} (score: {r.get('score', 0):.2f})")
            print(f"   {r['snippet'][:200]}...")
            print()
