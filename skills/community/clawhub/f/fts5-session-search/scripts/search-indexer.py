#!/usr/bin/env python3
"""
FTS5 Session Search Indexer for OpenClaw

Indexes OpenClaw session logs into SQLite FTS5 for instant full-text search.

Usage:
    python3 search-indexer.py index      — index new sessions since last run
    python3 search-indexer.py status     — show indexed session count, last indexed, db size
    python3 search-indexer.py reindex    — drop and rebuild entire index from scratch
"""

import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "search.db"
SESSIONS_ROOT = Path(os.environ.get("SESSIONS_ROOT", os.path.expanduser("~/.openclaw/agents")))

# Agents to index
AGENTS = os.environ.get("SEARCH_AGENTS", "main,mario,lilo,felix,peter,wazowski,woody,jarvis").split(",")

# Max content length per message (prevent enormous tool results from bloating index)
MAX_CONTENT_LENGTH = 10000


def get_db():
    """Get database connection with FTS5 tables created."""
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA synchronous=NORMAL")
    db.execute("PRAGMA cache_size=-8000")  # 8MB cache
    
    # Create FTS5 virtual table
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS conversations USING fts5(
            session_id,
            agent,
            timestamp,
            role,
            content,
            topic,
            tokenize='porter unicode61'
        )
    """)
    
    # Create metadata table
    db.execute("""
        CREATE TABLE IF NOT EXISTS session_meta (
            session_id TEXT PRIMARY KEY,
            agent TEXT,
            start_time TEXT,
            end_time TEXT,
            message_count INTEGER,
            topics TEXT,
            total_tokens INTEGER DEFAULT 0,
            indexed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index tracking table
    db.execute("""
        CREATE TABLE IF NOT EXISTS index_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    
    # Index for fast time lookups
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_session_meta_time ON session_meta(start_time)
    """)
    
    db.commit()
    return db


def extract_text_from_content(content_list):
    """Extract readable text from a message content array."""
    texts = []
    for item in content_list:
        if not isinstance(item, dict):
            continue
        content_type = item.get("type", "")
        if content_type == "text":
            text = item.get("text", "")
            if text:
                texts.append(text)
        elif content_type == "thinking":
            thinking = item.get("thinking", "")
            if thinking:
                texts.append(f"[thinking] {thinking}")
    return "\n".join(texts)


def extract_topics(text):
    """Extract simple topics/keywords from text."""
    if not text:
        return ""
    # Extract meaningful words (3+ chars, not common stop words)
    stop_words = {
        "the", "and", "for", "are", "but", "not", "you", "all", "can", "had",
        "her", "was", "one", "our", "out", "has", "have", "been", "from",
        "this", "that", "with", "they", "will", "what", "about", "would",
        "there", "their", "which", "could", "other", "into", "more", "some",
        "than", "its", "also", "just", "like", "then", "make", "being",
        "over", "only", "most", "very", "after", "before", "between",
    }
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    # Count word frequency
    word_freq = {}
    for w in words:
        if w not in stop_words:
            word_freq[w] = word_freq.get(w, 0) + 1
    # Top 10 most frequent meaningful words
    topics = sorted(word_freq.items(), key=lambda x: -x[1])[:10]
    return ", ".join(t[0] for t in topics)


def estimate_tokens(text):
    """Rough estimate of token count (chars / 4)."""
    return len(text) // 4 if text else 0


def parse_session_file(filepath, agent_name):
    """Parse a session JSONL file and return messages."""
    messages = []
    session_id = None
    start_time = None
    end_time = None
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                entry_type = obj.get("type", "")
                
                if entry_type == "session":
                    session_id = obj.get("id", "")
                    start_time = obj.get("timestamp", "")
                    continue
                
                if entry_type == "message":
                    msg = obj.get("message", {})
                    role = msg.get("role", "")
                    content = msg.get("content", [])
                    timestamp = obj.get("timestamp", msg.get("timestamp", ""))
                    
                    # Only index user and assistant messages (not toolResult for FTS)
                    if role not in ("user", "assistant", "system"):
                        continue
                    
                    text = extract_text_from_content(content)
                    if not text:
                        continue
                    
                    # Truncate overly long content
                    if len(text) > MAX_CONTENT_LENGTH:
                        text = text[:MAX_CONTENT_LENGTH] + "...[truncated]"
                    
                    end_time = timestamp
                    messages.append({
                        "role": role,
                        "content": text,
                        "timestamp": timestamp,
                    })
    except Exception as e:
        print(f"  Warning: Error reading {filepath}: {e}", file=sys.stderr)
        return None, []
    
    if not session_id:
        # Extract session ID from filename
        session_id = Path(filepath).stem.split(".")[0]
    
    meta = {
        "session_id": session_id,
        "agent": agent_name,
        "start_time": start_time or "",
        "end_time": end_time or "",
        "message_count": len(messages),
    }
    
    return meta, messages


def index_session(db, meta, messages):
    """Index a single session's messages into FTS5."""
    session_id = meta["session_id"]
    
    # Check if already indexed
    existing = db.execute(
        "SELECT 1 FROM session_meta WHERE session_id = ?",
        (session_id,)
    ).fetchone()
    if existing:
        return False  # Already indexed
    
    # Calculate topics from all messages combined
    all_text = " ".join(m["content"] for m in messages)
    topics = extract_topics(all_text)
    
    # Calculate total tokens
    total_tokens = sum(estimate_tokens(m["content"]) for m in messages)
    
    # Insert messages into FTS5
    for msg in messages:
        db.execute(
            """INSERT INTO conversations 
               (session_id, agent, timestamp, role, content, topic) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, meta["agent"], msg["timestamp"], msg["role"], msg["content"], topics)
        )
    
    # Insert metadata
    db.execute(
        """INSERT INTO session_meta 
           (session_id, agent, start_time, end_time, message_count, topics, total_tokens) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (session_id, meta["agent"], meta["start_time"], meta["end_time"], 
         meta["message_count"], topics, total_tokens)
    )
    
    return True


def discover_sessions():
    """Discover all session JSONL files across all agents."""
    sessions = []
    for agent in AGENTS:
        agent_dir = SESSIONS_ROOT / agent / "sessions"
        if not agent_dir.is_dir():
            continue
        
        for f in sorted(agent_dir.iterdir()):
            # Only primary session files (not trajectory, checkpoint, bak, reset)
            if f.suffix != ".jsonl":
                continue
            name = f.stem
            # Skip non-primary files
            if any(skip in name for skip in [".checkpoint", ".trajectory", ".bak", ".reset"]):
                continue
            # Skip files with dots in name (these are bak/checkpoint variants)
            if "." in name and not name.count(".") == 0:
                # e.g., "714b215d..." is fine, "714b215d...checkpoint.abc" is not
                base = name.split(".")[0]
                if len(base) != 36:  # UUID format
                    continue
            sessions.append((agent, str(f)))
    
    return sessions


def cmd_index(db):
    """Index new sessions since last run."""
    print("🔍 Discovering session files...")
    sessions = discover_sessions()
    print(f"   Found {len(sessions)} session files across all agents")
    
    # Get already indexed sessions
    indexed = set()
    for row in db.execute("SELECT session_id FROM session_meta"):
        indexed.add(row[0])
    
    new_count = 0
    skipped = 0
    errors = 0
    start_time = time.time()
    
    for agent, filepath in sessions:
        # Extract session_id from filename
        session_id = Path(filepath).stem.split(".")[0]
        
        if session_id in indexed:
            skipped += 1
            continue
        
        meta, messages = parse_session_file(filepath, agent)
        if meta is None or not messages:
            skipped += 1
            continue
        
        try:
            if index_session(db, meta, messages):
                new_count += 1
                db.commit()
                if new_count % 10 == 0:
                    print(f"   Indexed {new_count} sessions...")
        except Exception as e:
            print(f"  Error indexing {filepath}: {e}", file=sys.stderr)
            db.rollback()
            errors += 1
    
    db.commit()
    elapsed = time.time() - start_time
    
    # Update last indexed timestamp
    db.execute(
        "INSERT OR REPLACE INTO index_state (key, value) VALUES (?, ?)",
        ("last_index", datetime.now(timezone.utc).isoformat())
    )
    db.commit()
    
    print(f"\n✅ Indexing complete:")
    print(f"   New sessions indexed: {new_count}")
    print(f"   Already indexed (skipped): {skipped}")
    print(f"   Errors: {errors}")
    print(f"   Time: {elapsed:.1f}s")
    
    return new_count


def cmd_reindex(db):
    """Drop and rebuild entire index from scratch."""
    print("🗑️  Dropping existing index...")
    db.execute("DROP TABLE IF EXISTS conversations")
    db.execute("DROP TABLE IF EXISTS session_meta")
    db.execute("DROP TABLE IF EXISTS index_state")
    db.commit()
    
    # Recreate tables
    db.close()
    db = get_db()
    
    print("🔄 Rebuilding index from scratch...")
    return cmd_index(db), db


def cmd_status(db):
    """Show indexed session count, last indexed, db size."""
    # Session count
    session_count = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
    
    # Message count
    msg_count = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    
    # Total tokens
    total_tokens = db.execute("SELECT SUM(total_tokens) FROM session_meta").fetchone()[0] or 0
    
    # Last indexed
    last_indexed = db.execute(
        "SELECT value FROM index_state WHERE key = 'last_index'"
    ).fetchone()
    last_indexed = last_indexed[0] if last_indexed else "Never"
    
    # Date range
    date_range = db.execute(
        "SELECT MIN(start_time), MAX(start_time) FROM session_meta WHERE start_time != ''"
    ).fetchone()
    
    # DB size
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    
    # Per-agent stats
    agent_stats = db.execute(
        "SELECT agent, COUNT(*), SUM(message_count) FROM session_meta GROUP BY agent ORDER BY agent"
    ).fetchall()
    
    print("📊 Search Index Status")
    print(f"   Sessions indexed: {session_count}")
    print(f"   Messages indexed: {msg_count}")
    print(f"   Est. total tokens: {total_tokens:,}")
    print(f"   Last indexed: {last_indexed}")
    print(f"   Date range: {date_range[0] or 'N/A'} → {date_range[1] or 'N/A'}")
    print(f"   Database size: {db_size / 1024:.1f} KB ({db_size / 1024 / 1024:.2f} MB)")
    print(f"\n   Per-agent breakdown:")
    for agent, sessions, msgs in agent_stats:
        print(f"     {agent}: {sessions} sessions, {msgs} messages")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    db = get_db()
    
    try:
        if command == "index":
            cmd_index(db)
        elif command == "status":
            cmd_status(db)
        elif command == "reindex":
            _, db = cmd_reindex(db)
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()