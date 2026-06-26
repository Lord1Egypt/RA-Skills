#!/usr/bin/env python3
"""
FTS5 Session Search Tool for OpenClaw

Provides search, topic search, time-range search, session retrieval, and stats.

Usage:
    python3 search-tool.py search "query" [--scope all|user|assistant] [--limit 10] [--time today|week|month|year]
    python3 search-tool.py topic "topic name" [--limit 10]
    python3 search-tool.py time "2026-05-01" "2026-05-22" [--limit 10]
    python3 search-tool.py session <session_id>
    python3 search-tool.py stats
"""

import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "search.db"

# Time range mappings
TIME_RANGES = {
    "today": timedelta(days=0),
    "week": timedelta(weeks=1),
    "month": timedelta(days=30),
    "year": timedelta(days=365),
}


def get_db():
    """Get database connection."""
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA cache_size=-4000")
    return db


def search(query: str, scope: str = "all", limit: int = 10, time_range: str = None) -> list:
    """
    Search across all indexed conversations.
    
    Args:
        query: Natural language search query
        scope: "all", "user", "assistant", "system"
        limit: Max results to return
        time_range: "today", "week", "month", "year", or None
    
    Returns:
        List of dicts with: session_id, agent, timestamp, role, content, relevance_score, topic
    """
    db = get_db()
    try:
        # Build WHERE clause for scope
        scope_clause = ""
        if scope in ("user", "assistant", "system"):
            scope_clause = f"AND role = '{scope}'"
        
        # Build time filter
        time_clause = ""
        if time_range and time_range in TIME_RANGES:
            cutoff = (datetime.now(timezone.utc) - TIME_RANGES[time_range]).isoformat()
            time_clause = f"AND timestamp >= '{cutoff}'"
        
        # Use FTS5 MATCH with bm25 ranking
        # Handle negation: convert "term -negated" to "term NOT negated"
        safe_query = query.replace('"', '""')
        # FTS5 uses NOT instead of -
        # But - can work as NOT in column filters, so we convert
        safe_query = re.sub(r'\s+-(\w+)', r' NOT \1', safe_query)
        
        sql = f"""
            SELECT 
                session_id,
                agent,
                timestamp,
                role,
                content,
                topic,
                bm25(conversations) as relevance_score
            FROM conversations
            WHERE conversations MATCH ? {scope_clause} {time_clause}
            ORDER BY relevance_score
            LIMIT ?
        """
        
        results = []
        for row in db.execute(sql, (safe_query, limit)):
            results.append({
                "session_id": row[0],
                "agent": row[1],
                "timestamp": row[2],
                "role": row[3],
                "content": row[4],
                "topic": row[5],
                "relevance_score": round(row[6], 4),
            })
        
        return results
    finally:
        db.close()


def search_by_topic(topic: str, limit: int = 10) -> list:
    """Search for all conversations about a specific topic."""
    db = get_db()
    try:
        # Search in the topic column specifically
        safe_topic = topic.replace('"', '""')
        
        # First try exact topic column match
        sql = """
            SELECT 
                session_id,
                agent,
                timestamp,
                role,
                content,
                topic,
                bm25(conversations) as relevance_score
            FROM conversations
            WHERE topic MATCH ?
            ORDER BY relevance_score
            LIMIT ?
        """
        
        results = []
        for row in db.execute(sql, (safe_topic, limit)):
            results.append({
                "session_id": row[0],
                "agent": row[1],
                "timestamp": row[2],
                "role": row[3],
                "content": row[4],
                "topic": row[5],
                "relevance_score": round(row[6], 4),
            })
        
        # If no results, fall back to general search
        if not results:
            results = search(topic, limit=limit)
        
        return results
    finally:
        db.close()


def search_by_time(start: str, end: str, limit: int = 10) -> list:
    """Search conversations within a time range."""
    db = get_db()
    try:
        sql = """
            SELECT 
                session_id,
                agent,
                timestamp,
                role,
                content,
                topic,
                0 as relevance_score
            FROM conversations
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        
        results = []
        for row in db.execute(sql, (start, end, limit)):
            results.append({
                "session_id": row[0],
                "agent": row[1],
                "timestamp": row[2],
                "role": row[3],
                "content": row[4],
                "topic": row[5],
                "relevance_score": row[6],
            })
        
        return results
    finally:
        db.close()


def get_session(session_id: str) -> list:
    """Get full conversation for a session."""
    db = get_db()
    try:
        sql = """
            SELECT session_id, agent, timestamp, role, content, topic
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp
        """
        
        results = []
        for row in db.execute(sql, (session_id,)):
            results.append({
                "session_id": row[0],
                "agent": row[1],
                "timestamp": row[2],
                "role": row[3],
                "content": row[4],
                "topic": row[5],
            })
        
        return results
    finally:
        db.close()


def stats() -> dict:
    """Return search index statistics."""
    db = get_db()
    try:
        session_count = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
        msg_count = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        total_tokens = db.execute("SELECT SUM(total_tokens) FROM session_meta").fetchone()[0] or 0
        last_indexed = db.execute(
            "SELECT value FROM index_state WHERE key = 'last_index'"
        ).fetchone()
        date_range = db.execute(
            "SELECT MIN(start_time), MAX(start_time) FROM session_meta WHERE start_time != ''"
        ).fetchone()
        db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
        
        # Per-agent stats
        agent_stats = {}
        for row in db.execute(
            "SELECT agent, COUNT(*), SUM(message_count), SUM(total_tokens) FROM session_meta GROUP BY agent"
        ):
            agent_stats[row[0]] = {
                "sessions": row[1],
                "messages": row[2] or 0,
                "tokens": row[3] or 0,
            }
        
        return {
            "sessions_indexed": session_count,
            "messages_indexed": msg_count,
            "total_tokens": total_tokens,
            "last_indexed": last_indexed[0] if last_indexed else "Never",
            "date_range": {
                "start": date_range[0] or "N/A",
                "end": date_range[1] or "N/A",
            },
            "db_size_bytes": db_size,
            "db_size_mb": round(db_size / 1024 / 1024, 2),
            "agents": agent_stats,
        }
    finally:
        db.close()


def format_results(results, show_content=True):
    """Format search results for display."""
    if not results:
        print("No results found.")
        return
    
    for i, r in enumerate(results, 1):
        print(f"\n{'='*60}")
        print(f"  Result {i} | Score: {r.get('relevance_score', 'N/A')}")
        print(f"  Session: {r['session_id']}")
        print(f"  Agent: {r.get('agent', 'N/A')}")
        print(f"  Time: {r['timestamp']}")
        print(f"  Role: {r['role']}")
        if r.get('topic'):
            print(f"  Topic: {r['topic'][:80]}")
        if show_content:
            content = r['content']
            if len(content) > 300:
                content = content[:300] + "..."
            print(f"\n  {content}")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(results)} results")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "search":
        if len(sys.argv) < 3:
            print("Usage: search-tool.py search <query> [--scope all|user|assistant] [--limit N] [--time today|week|month|year]")
            sys.exit(1)
        
        query = sys.argv[2]
        scope = "all"
        limit = 10
        time_range = None
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--scope" and i + 1 < len(sys.argv):
                scope = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--time" and i + 1 < len(sys.argv):
                time_range = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        start = time.time()
        results = search(query, scope=scope, limit=limit, time_range=time_range)
        elapsed = time.time() - start
        
        format_results(results)
        print(f"\nSearch took {elapsed*1000:.1f}ms")
    
    elif command == "topic":
        if len(sys.argv) < 3:
            print("Usage: search-tool.py topic <topic> [--limit N]")
            sys.exit(1)
        
        topic = sys.argv[2]
        limit = 10
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        results = search_by_topic(topic, limit=limit)
        format_results(results)
    
    elif command == "time":
        if len(sys.argv) < 4:
            print("Usage: search-tool.py time <start_date> <end_date> [--limit N]")
            sys.exit(1)
        
        start_date = sys.argv[2]
        end_date = sys.argv[3]
        limit = 10
        
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        results = search_by_time(start_date, end_date, limit=limit)
        format_results(results)
    
    elif command == "session":
        if len(sys.argv) < 3:
            print("Usage: search-tool.py session <session_id>")
            sys.exit(1)
        
        session_id = sys.argv[2]
        results = get_session(session_id)
        format_results(results, show_content=True)
    
    elif command == "stats":
        s = stats()
        print("📊 Search Index Statistics")
        print(f"   Sessions indexed: {s['sessions_indexed']}")
        print(f"   Messages indexed: {s['messages_indexed']}")
        print(f"   Total tokens (est): {s['total_tokens']:,}")
        print(f"   Last indexed: {s['last_indexed']}")
        print(f"   Date range: {s['date_range']['start']} → {s['date_range']['end']}")
        print(f"   Database size: {s['db_size_mb']} MB")
        print(f"\n   Per-agent breakdown:")
        for agent, astat in sorted(s['agents'].items()):
            print(f"     {agent}: {astat['sessions']} sessions, {astat['messages']} messages, {astat['tokens']:,} tokens")
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()