#!/usr/bin/env python3
"""
Session Indexer — scan OpenClaw session .jsonl files and index into SQLite FTS5.
Usage: python index-sessions.py [--agent main] [--incremental] [--all-agents]
"""
import sqlite3
import json
import glob
import os
import sys
import argparse
from datetime import datetime

# Configurable paths via env vars
AGENTS_DIR = os.environ.get("OPENCLAW_AGENTS_DIR", os.path.expanduser("~/.openclaw/agents"))
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.environ.get("SESSION_SEARCH_DB_DIR", os.path.join(SKILL_DIR, "db"))
DB_PATH = os.path.join(DB_DIR, "sessions.db")

def get_session_files(agent_id="main"):
    """Get all .jsonl session files for an agent."""
    session_dir = os.path.join(AGENTS_DIR, agent_id, "sessions")
    if not os.path.isdir(session_dir):
        return []
    return sorted(glob.glob(f"{session_dir}/*.jsonl"), key=os.path.getmtime, reverse=True)

def get_all_agent_ids():
    """Discover all agent IDs from agents directory."""
    if not os.path.isdir(AGENTS_DIR):
        return []
    return [d for d in os.listdir(AGENTS_DIR)
            if os.path.isdir(os.path.join(AGENTS_DIR, d, "sessions"))]

def extract_messages(jsonl_path):
    """Extract user/assistant messages from a session file."""
    messages = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if d.get("type") != "message":
                    continue

                msg = d.get("message", {})
                role = msg.get("role", "?")
                if role not in ("user", "assistant"):
                    continue

                content = msg.get("content", [])
                texts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            t = block.get("text", "").strip()
                            if t:
                                texts.append(t)
                        elif block.get("type") == "toolCall":
                            tc = block.get("name", "?")
                            args = block.get("arguments", {})
                            if isinstance(args, dict):
                                cmd = args.get("command", "")[:100]
                                texts.append(f"[tool: {tc}] {cmd}")
                            else:
                                texts.append(f"[tool: {tc}]")

                full_text = "\n".join(texts)
                if not full_text:
                    continue

                messages.append({
                    "message_id": d.get("id", ""),
                    "role": role,
                    "text": full_text,
                    "timestamp": msg.get("timestamp", d.get("timestamp", "")),
                })
    except Exception as e:
        print(f"  ⚠️  Failed to read {jsonl_path}: {e}", file=sys.stderr)
    return messages

def init_db():
    """Create SQLite FTS5 tables."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
            session_id, message_id, role, text, timestamp,
            tokenize='unicode61 remove_diacritics 2'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS index_meta (
            session_file TEXT PRIMARY KEY,
            last_modified TEXT,
            entries_indexed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn

def index_agent(agent_id, conn, incremental=False):
    """Index sessions for one agent."""
    session_files = get_session_files(agent_id)
    if not session_files:
        return 0, 0

    total_indexed = 0
    files_processed = 0

    for sf in session_files:
        sf_abs = os.path.abspath(sf)
        mtime = datetime.fromtimestamp(os.path.getmtime(sf_abs)).isoformat()

        if incremental:
            c = conn.cursor()
            c.execute("SELECT last_modified FROM index_meta WHERE session_file = ?", (sf_abs,))
            row = c.fetchone()
            if row and row[0] == mtime:
                continue

        messages = extract_messages(sf_abs)
        if not messages:
            continue

        session_id = os.path.basename(sf_abs).replace(".jsonl", "")

        if incremental:
            conn.execute("DELETE FROM sessions_fts WHERE session_id = ?", (session_id,))

        entries = [
            (session_id, m["message_id"], m["role"], m["text"], m["timestamp"])
            for m in messages
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO sessions_fts VALUES (?, ?, ?, ?, ?)",
            entries
        )
        conn.execute(
            "INSERT OR REPLACE INTO index_meta VALUES (?, ?, ?)",
            (sf_abs, mtime, len(messages))
        )

        total_indexed += len(messages)
        files_processed += 1

    return total_indexed, files_processed

def main():
    parser = argparse.ArgumentParser(description="Index OpenClaw session files into FTS5")
    parser.add_argument("--agent", default="main", help="Agent ID (default: main)")
    parser.add_argument("--all-agents", action="store_true", help="Index all agents found in agents dir")
    parser.add_argument("--incremental", action="store_true", help="Skip files not modified since last index")
    args = parser.parse_args()

    conn = init_db()
    grand_total = 0
    grand_files = 0

    if args.all_agents:
        for agent_id in get_all_agent_ids():
            print(f"\n📁 Indexing agent: {agent_id}")
            n, f = index_agent(agent_id, conn, incremental=args.incremental)
            print(f"   {'+' if n else '  '}{f} files, {n} messages")
            grand_total += n
            grand_files += f
    else:
        print(f"📁 Indexing agent: {args.agent}")
        grand_total, grand_files = index_agent(args.agent, conn, incremental=args.incremental)
        print(f"   {'+' if grand_total else '  '}{grand_files} files, {grand_total} messages")

    conn.commit()
    conn.close()

    print(f"\n✅ Done — {grand_files} files, {grand_total} messages indexed")
    print(f"   DB: {DB_PATH}")

if __name__ == "__main__":
    main()
