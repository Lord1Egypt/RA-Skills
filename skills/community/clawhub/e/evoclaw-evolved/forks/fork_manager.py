# Fork Sessions — Fork 子代理机制
# 参考: claude-code src/core/sessions/fork.ts
#
# 设计:
#   fork_session() 创建分支 session，独立工作流
#   每个 fork 有独立 workspace（可用 worktree）
#   支持结果合并回主 session
#   TOCTOU 安全: worktree 目录存在性检查
#
# 与 Coordinator 的区别:
#   Coordinator: 一个主 agent 管多个子 agent，并行/串行协作
#   Fork: 用户主动分叉出一个独立分支，各自独立演进

from __future__ import annotations
import uuid
import time
import threading
import json
import os
import shutil
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from enum import Enum

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
FORKS_DIR = WORKSPACE / "evoclaw" / "forks"
FORKS_DIR.mkdir(parents=True, exist_ok=True)


# ─── Fork 状态 ──────────────────────────────────────────────────

class ForkState(str, Enum):
    ACTIVE = "active"
    MERGED = "merged"        # 结果已合并回父 session
    ABANDONED = "abandoned"  # 分支放弃
    FAILED = "failed"


# ─── Fork 记录 ──────────────────────────────────────────────────

@dataclass
class ForkRecord:
    fork_id: str
    parent_session_key: str
    label: str
    state: ForkState = ForkState.ACTIVE
    created_at: float = field(default_factory=time.time)
    merged_at: Optional[float] = None
    worktree_path: Optional[str] = None   # 独立工作树目录
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "fork_id": self.fork_id,
            "parent_session_key": self.parent_session_key,
            "label": self.label,
            "state": self.state.value,
            "created_at": self.created_at,
            "merged_at": self.merged_at,
            "worktree_path": self.worktree_path,
            "metadata": self.metadata,
        }


# ─── Fork Manager ───────────────────────────────────────────────

class ForkManager:
    """
    Fork session 管理.
    
    用法:
        fork = ForkManager.create(parent_session="main-001", label="尝试方案A")
        # 在 fork 上工作...
        ForkManager.merge(fork.fork_id)  # 合并结果
    """

    _forks: dict[str, ForkRecord] = {}
    _lock = threading.RLock()
    _index_file = FORKS_DIR / "forks_index.jsonl"

    @classmethod
    def _load(cls) -> None:
        if cls._index_file.exists():
            try:
                lines = cls._index_file.read_text(encoding="utf-8").strip().split("\n")
                with cls._lock:
                    cls._forks = {r["fork_id"]: r for r in (json.loads(l) for l in lines if l) if "fork_id" in r}
            except Exception:
                cls._forks = {}

    @classmethod
    def _save(cls) -> None:
        cls._index_file.parent.mkdir(parents=True, exist_ok=True)
        lines = ["\n".join(json.dumps(r, ensure_ascii=False) for r in cls._forks.values())]
        cls._index_file.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in cls._forks.values()) + "\n", encoding="utf-8")

    @classmethod
    def create(
        cls,
        parent_session_key: str,
        label: str,
        worktree: bool = False,
        metadata: Optional[dict] = None,
    ) -> ForkRecord:
        """
        创建 fork.
        
        Args:
            parent_session_key: 父 session key
            label: 分支标签
            worktree: 是否创建独立工作树目录
            metadata: 额外元数据
        """
        fork_id = str(uuid.uuid4())[:12]

        # 可选: 创建 worktree 目录
        worktree_path = None
        if worktree:
            worktree_path = str(FORKS_DIR / f"worktree_{fork_id}")
            try:
                Path(worktree_path).mkdir(parents=True, exist_ok=True)
            except Exception:
                worktree_path = None  # 失败不阻断

        record = ForkRecord(
            fork_id=fork_id,
            parent_session_key=parent_session_key,
            label=label,
            worktree_path=worktree_path,
            metadata=metadata or {},
        )

        with cls._lock:
            cls._forks[fork_id] = record.to_dict()
            cls._save()

        return record

    @classmethod
    def get(cls, fork_id: str) -> Optional[ForkRecord]:
        cls._load()
        with cls._lock:
            raw = cls._forks.get(fork_id)
            if raw:
                return ForkRecord(**raw)
            return None

    @classmethod
    def merge(cls, fork_id: str, result: Optional[dict] = None) -> dict:
        """
        合并 fork 结果回父 session.
        参考: claude-code fork merge 流程.
        """
        record = cls.get(fork_id)
        if not record:
            return {"error": f"Fork {fork_id} not found"}

        record.state = ForkState.MERGED
        record.merged_at = time.time()
        if result:
            record.metadata["merge_result"] = result

        with cls._lock:
            cls._forks[fork_id] = record.to_dict()
            cls._save()

        # 可选: 清理 worktree
        if record.worktree_path and Path(record.worktree_path).exists():
            try:
                shutil.rmtree(record.worktree_path)
            except Exception:
                pass  # 清理失败不阻断

        return {"fork_id": fork_id, "merged": True, "parent": record.parent_session_key}

    @classmethod
    def abandon(cls, fork_id: str) -> dict:
        """放弃 fork"""
        record = cls.get(fork_id)
        if not record:
            return {"error": f"Fork {fork_id} not found"}

        record.state = ForkState.ABANDONED

        with cls._lock:
            cls._forks[fork_id] = record.to_dict()
            cls._save()

        # 清理 worktree
        if record.worktree_path and Path(record.worktree_path).exists():
            try:
                shutil.rmtree(record.worktree_path)
            except Exception:
                pass

        return {"fork_id": fork_id, "abandoned": True}

    @classmethod
    def list_by_parent(cls, parent_session_key: str) -> list[ForkRecord]:
        """列出某 parent 的所有 forks"""
        cls._load()
        with cls._lock:
            return [
                ForkRecord(**r)
                for r in cls._forks.values()
                if r.get("parent_session_key") == parent_session_key
            ]

    @classmethod
    def list_active(cls) -> list[ForkRecord]:
        cls._load()
        with cls._lock:
            return [
                ForkRecord(**r)
                for r in cls._forks.values()
                if r.get("state") == ForkState.ACTIVE.value
            ]


# ─── Worktree 安全 ───────────────────────────────────────────────

def ensure_worktree_safe(path: str) -> bool:
    """
    检查 worktree 路径安全.
    参考: claude-code symlink realpath 检查.
    
    - 不允许 symlink 逃逸到 workspace 外
    - 不允许 /etc, /tmp 等危险路径
    """
    p = Path(path).resolve()
    
    # 允许的根目录
    allowed_roots = [WORKSPACE.resolve()]
    
    # 检查是否在允许范围内
    is_safe = any(str(p).startswith(str(root)) for root in allowed_roots)
    
    # 额外检查: 不允许危险路径
    dangerous = ["/etc", "/tmp", "/var", "/root", "/home"]
    is_safe = is_safe and not any(str(p).startswith(d) for d in dangerous)
    
    return is_safe


# ─── 便捷函数 ───────────────────────────────────────────────────

def fork_session(parent_session_key: str, label: str, worktree: bool = False) -> ForkRecord:
    """创建 fork"""
    return ForkManager.create(parent_session_key, label, worktree)


def merge_fork(fork_id: str, result: Optional[dict] = None) -> dict:
    """合并 fork"""
    return ForkManager.merge(fork_id, result)


if __name__ == "__main__":
    # Demo
    parent = "main-session-001"
    fork = fork_session(parent, "尝试方案A", worktree=True)
    print(f"✅ Fork created: {fork.fork_id}, worktree={fork.worktree_path}")

    active = ForkManager.list_by_parent(parent)
    print(f"   Active forks: {len(active)}")

    result = merge_fork(fork.fork_id, {"summary": "完成了登录功能"})
    print(f"   Merge result: {result}")
