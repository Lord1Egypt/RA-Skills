#!/usr/bin/env python3
"""
Eidolon Search - Simple Search

Usage:
  python scripts/search.py "query" [limit]
  DB_PATH=./memory.db python scripts/search.py "query"
"""

import sys
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get('DB_PATH', './memory.db')

def search(query, limit=10):
    """메모리 검색"""
    if not Path(DB_PATH).exists():
        print(f"❌ Database not found: {DB_PATH}")
        print(f"Run: python scripts/build-index.py")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    results = c.execute("""
    SELECT 
      path,
      snippet(memory_fts, 1, '[', ']', '...', 30) as snippet,
      rank
    FROM memory_fts
    WHERE memory_fts MATCH ?
    ORDER BY rank
    LIMIT ?
    """, (query, limit)).fetchall()
    
    conn.close()
    
    print(f"🔍 Search: {query}")
    print("=" * 60)
    
    if not results:
        print("No results found.")
    else:
        for i, (path, snippet, rank) in enumerate(results, 1):
            print(f"\n{i}. {path}")
            print(f"   {snippet}")
    
    print("\n✅ Done")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/search.py 'query' [limit]")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    search(query, limit)

if __name__ == "__main__":
    main()
