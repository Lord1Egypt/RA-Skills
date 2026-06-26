# Session Store — Session 元数据持久化
# 参考: claude-code/src/core/session.ts processResumedConversation()
#       claude-code/src/core/session/persistence.ts
#
# 设计:
#   每个 session 独立 JSONL 文件, 存储:
#     - model, channel, mode
#     - active_tasks (运行中的任务)
#     - cron_state (定时任务状态)
#     - custom_prompt, append_prompt
#     - created_at, updated_at
#   恢复时完整重建状态

from __future__ import annotations
import os
import json
import time
import hashlib
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
SESSIONS_DIR = WORKSPACE / "evoclaw" / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class SessionMetadata:
    """Session 元数据"""
    session_key: str
    model: str = "unknown"
    channel: str = "unknown"
    mode: str = "normal"          # normal | coordinator | auto
    agent_id: Optional[str] = None
    custom_system_prompt: str = ""
    append_system_prompt: str = ""
    active_tasks: list[str] = field(default_factory=list)   # task_id 列表
    cron_running: list[str] = field(default_factory=list)   # 运行中的 cron 任务
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    last_message_at: float = field(default_factory=time.time)
    message_count: int = 0
    pinned_messages: list[str] = field(default_factory=list)  # message_id 列表
    worktree: Optional[str] = None   # 当前工作树目录 (用于 crash 恢复)
    metadata: dict = field(default_factory=dict)  # 扩展元数据

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "SessionMetadata":
        return cls(**d)

    def save(self) -> None:
        """保存到 JSONL 文件 (sessions_index.jsonl)"""
        self.updated_at = time.time()
        records = self._read_all()
        # 更新或追加
        found = False
        new_records = []
        for rec in records:
            if rec.get("session_key") == self.session_key:
                new_records.append(self.to_dict())
                found = True
            else:
                new_records.append(rec)
        if not found:
            new_records.append(self.to_dict())
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        index_file = SESSIONS_DIR / "sessions_index.jsonl"
        index_file.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in new_records) + "\n",
            encoding="utf-8"
        )

    @classmethod
    def _read_all(cls) -> list[dict]:
        """读取所有 session 元数据"""
        index = SESSIONS_DIR / "sessions_index.jsonl"
        if not index.exists():
            return []
        try:
            lines = index.read_text(encoding="utf-8").strip().split("\n")
            return [json.loads(line) for line in lines if line.strip()]
        except Exception:
            return []

    def remove(self) -> None:
        """删除 session 元数据"""
        index_records = [r for r in self._read_all() if r.get("session_key") != self.session_key]
        index = SESSIONS_DIR / "sessions_index.jsonl"
        if index.exists():
            index.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False) for r in index_records) + "\n",
                encoding="utf-8"
            )


class SessionStore:
    """
    Session 元数据存储.
    
    用法:
        store = SessionStore()
        meta = store.get("session-key-123")
        meta.message_count += 1
        meta.save()
    """

    @staticmethod
    def get(session_key: str) -> SessionMetadata:
        """获取 session 元数据, 不存在则创建新的"""
        records = SessionMetadata._read_all()
        for rec in records:
            if rec.get("session_key") == session_key:
                return SessionMetadata.from_dict(rec)
        # 不存在 → 创建新记录
        meta = SessionMetadata(session_key=session_key)
        meta.save()
        return meta

    @staticmethod
    def save(meta: SessionMetadata) -> None:
        """保存 session 元数据"""
        meta.save()

    @staticmethod
    def touch(session_key: str) -> SessionMetadata:
        """
        更新 last_message_at 时间戳 (轻量操作, 每条消息调用).
        内部缓冲: 最多每 30s 实际写一次磁盘.
        """
        meta = SessionStore.get(session_key)
        now = time.time()
        if now - meta.last_message_at > 30:
            meta.last_message_at = now
            meta.message_count += 1
            meta.save()
        else:
            # 只更新时间戳, 不写盘
            meta.last_message_at = now
        return meta

    @staticmethod
    def list_all() -> list[SessionMetadata]:
        """列出所有 session"""
        return [SessionMetadata.from_dict(r) for r in SessionMetadata._read_all()]

    @staticmethod
    def cleanup_old(days: int = 30) -> int:
        """删除 N 天前的 inactive session"""
        cutoff = time.time() - days * 86400
        records = SessionMetadata._read_all()
        remaining = [r for r in records if r.get("last_message_at", 0) > cutoff]
        removed = len(records) - len(remaining)
        index = SESSIONS_DIR / "sessions_index.jsonl"
        if index.exists():
            index.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False) for r in remaining) + "\n",
                encoding="utf-8"
            )
        return removed


# ─── Session 恢复 ─────────────────────────────────────────────────

def load_session_state(session_key: str) -> Optional[SessionMetadata]:
    """
    恢复 session 状态.
    参考: claude-code processResumedConversation() — 不仅恢复消息, 还恢复:
      - model, channel, mode
      - agent settings
      - worktree 目录
    """
    return SessionStore.get(session_key)


def snapshot_session(session_key: str, **kwargs) -> SessionMetadata:
    """
    快照当前 session 状态.
    在重要节点调用 (如: 心跳结束、任务完成、模式切换).
    """
    meta = SessionStore.get(session_key)
    for key, value in kwargs.items():
        if hasattr(meta, key):
            setattr(meta, key, value)
    meta.save()
    return meta


if __name__ == "__main__":
    # Demo
    meta = SessionStore.get("demo-session-001")
    meta.model = "minimax-portal/MiniMax-M2.7"
    meta.channel = "openclaw-weixin"
    meta.mode = "normal"
    meta.message_count = 42
    meta.save()
    print(f"Saved: {meta.session_key}, messages={meta.message_count}")

    loaded = SessionStore.get("demo-session-001")
    print(f"Loaded: model={loaded.model}, channel={loaded.channel}")

    removed = SessionStore.cleanup_old(days=0)
    print(f"Cleaned up: {removed} old sessions")
