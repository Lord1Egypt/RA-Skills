# -*- coding: utf-8 -*-
"""
导入 sessions JSONL 文件到本地 SQLite
支持 FTS5 全文搜索（Python 3.9+），降级到 LIKE 搜索（3.8）
"""
import os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import re
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime

SESSION_KEY_RE = re.compile(r"agent:main:(?:session:)?(?P<key>[^:]+)")


def get_workspace():
    """推断 openclaw 根目录，用于拼接 sessions 路径"""
    ws = os.environ.get("OPENCLAW_WORKSPACE")
    if ws:
        return Path(ws)
    home = Path.home()
    candidates = [home / ".openclaw", home / ".openclaw" / "workspace"]
    for c in candidates:
        if (c / "agents" / "main" / "sessions").exists():
            return c
    return home / ".openclaw"


def get_db_workspace():
    """推断 workspace 目录，优先找有 conversations.db 的目录"""
    ws = os.environ.get("OPENCLAW_WORKSPACE")
    if ws:
        p = Path(ws)
        if (p / "conversations.db").exists():
            return p
    home = Path.home()
    for c in [home / ".openclaw" / "workspace", home / ".openclaw"]:
        db = c / "conversations.db"
        if db.exists() and db.stat().st_size > 0:
            return c
    return home / ".openclaw"


def get_db_path():
    """数据库路径，默认在 workspace/conversations.db"""
    ws = get_db_workspace()
    default = ws / "conversations.db"
    return Path(os.environ.get("CONVERSATIONS_DB", default))


def get_sessions_dir():
    ws = get_workspace()
    default = ws / "agents" / "main" / "sessions"
    return Path(os.environ.get("SESSIONS_DIR", default))


def detect_fts_support(conn):
    """检测 FTS5 是否可用"""
    try:
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _test_fts USING fts5(content)")
        conn.execute("DROP TABLE _test_fts")
        return True
    except Exception:
        return False


def init_db(conn, use_fts):
    """初始化数据库 schema"""
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            session_key TEXT,
            turn_id TEXT,
            role TEXT,
            content TEXT,
            created_at INTEGER,
            content_hash TEXT UNIQUE
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_session ON chunks(session_key)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_created ON chunks(created_at)")
    if use_fts:
        c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(content, content_rowid=rowid, content=chunks)")
        c.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, content) VALUES (new.rowid, new.content);
            END
        """)
        c.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content) VALUES('delete', old.rowid, old.content);
            END
        """)
        c.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content) VALUES('delete', old.rowid, old.content);
                INSERT INTO chunks_fts(rowid, content) VALUES (new.rowid, new.content);
            END
        """)


def parse_session_file(filepath):
    """解析单个 session JSONL 文件"""
    name = Path(filepath).name
    uuid_part = name.replace(".jsonl", "").split(".reset")[0].split(".deleted")[0]
    session_key = f"agent:main:session:{uuid_part}"
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("type") == "message":
                    role = record.get("role", "unknown")
                    content = extract_text_content(record.get("content", []))
                    if not content:
                        continue
                    ts = record.get("timestamp", "")
                    try:
                        created_at = int(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp() * 1000)
                    except Exception:
                        created_at = 0
                    seq = record.get("seq", 0)
                    turn_id = make_turn_id(int(created_at), role, seq)
                    content_hash = make_content_hash(content)
                    yield {
                        "session_key": session_key,
                        "turn_id": turn_id,
                        "role": role,
                        "content": content,
                        "created_at": created_at,
                        "content_hash": content_hash,
                    }
    except Exception as e:
        print(f"  [!] 解析失败 {filepath}: {e}")


def extract_text_content(content):
    """从 content 字段提取纯文本"""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    texts.append(block.get("text", ""))
                elif block.get("type") == "thinking":
                    pass
        return "\n".join(texts).strip()
    return ""


def make_turn_id(timestamp_ms: int, role: str, seq: int) -> str:
    return f"{timestamp_ms}_{role}_{seq}"


def make_content_hash(content: str) -> str:
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def main(dry_run=False):
    db_path = get_db_path()
    sessions_dir = get_sessions_dir()
    use_fts = True

    print(f"数据库: {db_path}")
    print(f"会话目录: {sessions_dir}")

    if not sessions_dir.exists():
        print(f"[!] sessions 目录不存在: {sessions_dir}")
        return

    conn = sqlite3.connect(db_path)
    use_fts = detect_fts_support(conn)
    print(f"FTS5 支持: {'是' if use_fts else '否（降级到 LIKE）'}")
    init_db(conn, use_fts)

    # 获取已有 hash
    existing = set(row[0] for row in conn.execute("SELECT content_hash FROM chunks"))
    print(f"现有记录: {len(existing)} 条")

    # 扫描 sessions
    jsonl_files = sorted(sessions_dir.glob("*.jsonl"))
    print(f"发现 session 文件: {len(jsonl_files)} 个")

    # 重建 FTS 索引（如果之前用的是降级模式）
    if use_fts:
        try:
            conn.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
        except Exception:
            pass

    imported = 0
    skipped = 0

    for filepath in jsonl_files:
        records = list(parse_session_file(filepath))
        if not records:
            skipped += 1
            continue

        for rec in records:
            if rec["content_hash"] in existing:
                continue
            if dry_run:
                print(f"  [DRY] {rec['session_key'][-8:]}: {rec['content'][:40]}...")
                continue
            conn.execute("""
                INSERT OR IGNORE INTO chunks (session_key, turn_id, role, content, created_at, content_hash)
                VALUES (:session_key, :turn_id, :role, :content, :created_at, :content_hash)
            """, rec)
            existing.add(rec["content_hash"])
            imported += 1

    if not dry_run:
        conn.commit()

    print(f"\n导入完成: {imported} 条新记录，{skipped} 个空文件")
    conn.close()


if __name__ == "__main__":
    import sys
    main(dry_run="--dry" in sys.argv or os.environ.get("DRY_RUN", "").lower() == "true")
