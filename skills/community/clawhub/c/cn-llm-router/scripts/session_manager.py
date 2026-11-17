"""多轮会话管理（v2.6 新增）。

chat --session ID 调用时自动维护对话上下文：
- SQLite 持久化会话表（会话 ID / 消息历史 / 所用模型 / 创建时间）
- 后续调用自动携带上下文
- 支持会话内切换模型（历史以摘要压缩注入）
- 超出上下文窗口时自动摘要压缩历史

设计：纯标准库 sqlite3，零依赖；存储在 ~/.cn_llm_router/sessions.db
"""

import json
import os
import sqlite3
import time

DB_PATH = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "sessions.db")


def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        messages TEXT NOT NULL DEFAULT '[]',
        model TEXT,
        provider TEXT,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL
    )""")
    c.commit()
    return c


def get_session(session_id):
    """获取会话历史。返回 {id, messages, model, provider, created_at, updated_at} 或 None。"""
    c = _conn()
    try:
        row = c.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "messages": json.loads(row["messages"]),
            "model": row["model"],
            "provider": row["provider"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
    finally:
        c.close()


def create_session(session_id=None):
    """创建新会话。返回 session_id。"""
    import uuid
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
    now = time.time()
    c = _conn()
    try:
        c.execute(
            "INSERT OR IGNORE INTO sessions (id, messages, created_at, updated_at) VALUES (?, '[]', ?, ?)",
            (session_id, now, now)
        )
        c.commit()
    finally:
        c.close()
    return session_id


def append_message(session_id, role, content, model=None, provider=None):
    """向会话追加一条消息。"""
    c = _conn()
    try:
        row = c.execute("SELECT messages FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not row:
            create_session(session_id)
            messages = []
        else:
            messages = json.loads(row["messages"])
        messages.append({"role": role, "content": content, "ts": time.time()})
        c.execute(
            "UPDATE sessions SET messages=?, model=?, provider=?, updated_at=? WHERE id=?",
            (json.dumps(messages, ensure_ascii=False), model, provider, time.time(), session_id)
        )
        c.commit()
    finally:
        c.close()


def list_sessions(limit=10):
    """列出最近活跃会话。"""
    c = _conn()
    try:
        rows = c.execute(
            "SELECT id, model, provider, created_at, updated_at FROM sessions ORDER BY updated_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        c.close()


def delete_session(session_id):
    """删除会话。"""
    c = _conn()
    try:
        cur = c.execute("DELETE FROM sessions WHERE id=?", (session_id,))
        c.commit()
        return cur.rowcount > 0
    finally:
        c.close()


def compress_history(messages, max_chars=4000):
    """摘要压缩历史消息：保留最近 N 条，更早的合并为摘要占位。

    简单策略：保留 system 消息 + 最近 6 条；更早消息替换为摘要占位符。
    后续版本可调用模型做真正摘要，当前避免额外 API 调用。"""
    if len(messages) <= 6:
        return messages
    system_msgs = [m for m in messages if m.get("role") == "system"]
    recent = messages[-6:]
    older_count = len(messages) - 6 - len(system_msgs)
    if older_count > 0:
        placeholder = {
            "role": "system",
            "content": "[历史摘要] 前面 %d 条对话已压缩，仅保留最近 6 条" % older_count
        }
        return system_msgs + [placeholder] + recent
    return messages


def build_messages_with_history(session_id, current_prompt, system=None, max_history_chars=8000):
    """构建带上下文的消息列表。

    返回 (messages, history_model, history_provider)。
    当前上下文超 max_history_chars 时自动摘要压缩。
    """
    session = get_session(session_id)
    if not session:
        create_session(session_id)
        messages = []
        history_model = None
        history_provider = None
    else:
        messages = session["messages"]
        history_model = session["model"]
        history_provider = session["provider"]

    # 添加 system 提示
    if system and not any(m.get("role") == "system" for m in messages):
        messages.insert(0, {"role": "system", "content": system})

    # 追加当前用户消息
    messages.append({"role": "user", "content": current_prompt})

    # 超长时压缩
    total_chars = sum(len(m.get("content", "")) for m in messages)
    if total_chars > max_history_chars:
        messages = compress_history(messages)

    return messages, history_model, history_provider
