# -*- coding: utf-8 -*-
"""
查询对话历史
支持 FTS5 MATCH（Python 3.9+）和 LIKE 降级（3.8）
"""
import os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import sqlite3
import sys
from pathlib import Path

SESSION_KEY_RE = __import__("re").compile(r"agent:main:(?:session:)?(?P<key>[^:]+)")


def get_db_path():
    ws_env = os.environ.get("OPENCLAW_WORKSPACE")
    if ws_env:
        return Path(ws_env) / "conversations.db"
    home = Path.home()
    # 优先找 workspace/conversations.db，不找 openclaw 根目录下的同名空文件
    for c in [home / ".openclaw" / "workspace", home / ".openclaw"]:
        db = c / "conversations.db"
        if db.exists() and db.stat().st_size > 0:
            return db
    return home / ".openclaw" / "conversations.db"


def detect_fts(conn):
    try:
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _q_test USING fts5(content)")
        conn.execute("DROP TABLE _q_test")
        return True
    except Exception:
        return False


def search(conn, query, limit=10, use_fts=False):
    pattern = f"%{query}%"
    # LIKE 始终可用，作为主要搜索或 fallback
    rows = conn.execute("""
        SELECT session_key, role, content, created_at
        FROM chunks
        WHERE content LIKE :pattern
        ORDER BY created_at DESC
        LIMIT :limit
    """, {"pattern": pattern, "limit": limit}).fetchall()
    # 如果 FTS 找到更多结果，可以合并
    if use_fts:
        try:
            fts_rows = conn.execute("""
                SELECT c.session_key, c.role, c.content, c.created_at
                FROM chunks c
                WHERE c.rowid IN (
                    SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH :q
                )
                ORDER BY c.created_at DESC
                LIMIT :limit
            """, {"q": query, "limit": limit}).fetchall()
            # 合并去重
            seen = {(r[0], r[2][:50]) for r in rows}
            for r in fts_rows:
                key = (r[0], r[2][:50])
                if key not in seen:
                    rows.append(r)
                    seen.add(key)
            rows.sort(key=lambda x: x[3], reverse=True)
            rows = rows[:limit]
        except Exception:
            pass
    return rows


def format_ts(ts_ms):
    import datetime
    if not ts_ms:
        return "unknown"
    try:
        return datetime.datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ts_ms)


def main(query=None, limit=10):
    if query is None:
        if len(sys.argv) < 2:
            print("用法: query_conversations.py <搜索内容> [limit]")
            return
        query = sys.argv[1]
        if len(sys.argv) >= 3:
            limit = int(sys.argv[2])

    db_path = get_db_path()
    if not db_path.exists():
        print(f"[!] 数据库不存在: {db_path}")
        print(f"    请先运行: python import_sessions.py")
        return

    conn = sqlite3.connect(db_path)
    use_fts = detect_fts(conn)

    rows = search(conn, query, limit=limit, use_fts=use_fts)

    if not rows:
        print("没有找到相关内容")
        conn.close()
        return

    print(f"找到 {len(rows)} 条结果:\n")
    for i, (session_key, role, content, created_at) in enumerate(rows, 1):
        ts = format_ts(created_at)
        key_match = SESSION_KEY_RE.search(session_key)
        key_short = key_match.group("key")[-8:] if key_match else session_key[-8:]
        print(f"--- [{i}] {ts} ({key_short}) ---")
        # 内容截断
        preview = content[:300] + ("..." if len(content) > 300 else "")
        print(preview)
        print()

    conn.close()


if __name__ == "__main__":
    main()
