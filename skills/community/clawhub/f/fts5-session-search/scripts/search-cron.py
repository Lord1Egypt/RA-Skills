#!/usr/bin/env python3
"""
FTS5 Search Index Cron — Designed to be called from heartbeats.

Lightweight wrapper that:
- Checks if there are new sessions to index
- Indexes only new sessions
- Logs stats: sessions indexed, time taken, db size

Usage:
    python3 search-cron.py
"""

import sys
import time
import importlib.util
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "search.db"

# Load module with hyphenated filename
spec = importlib.util.spec_from_file_location('search_indexer', SCRIPT_DIR / 'search-indexer.py')
search_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_indexer)

get_db = search_indexer.get_db
cmd_index = search_indexer.cmd_index
cmd_status = search_indexer.cmd_status


def main():
    """Run incremental index and report stats."""
    print("🔄 FTS5 Search Index Cron")
    print("=" * 40)
    
    if not DB_PATH.exists():
        print("   Database not found. Running initial index...")
        db = get_db()
    else:
        db = get_db()
    
    # Check current state before indexing
    before_sessions = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
    
    # Run incremental index
    new_count = cmd_index(db)
    
    # Get after state
    after_sessions = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
    
    db.close()
    
    # Report
    print(f"\n📈 Cron Summary:")
    print(f"   Sessions before: {before_sessions}")
    print(f"   New sessions: {new_count}")
    print(f"   Sessions after: {after_sessions}")
    print(f"   DB size: {DB_PATH.stat().st_size / 1024:.1f} KB")
    
    if new_count > 0:
        print("✅ New sessions indexed successfully")
    else:
        print("✅ No new sessions to index")
    
    return new_count


if __name__ == "__main__":
    main()