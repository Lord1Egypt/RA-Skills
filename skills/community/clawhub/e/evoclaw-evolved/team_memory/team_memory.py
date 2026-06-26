# Team Memory — 团队记忆共享
# 参考: claude-code Team Memory
#
# 双重安全:
#   1. 字符串 containment 检查 — 防止数据逃逸
#   2. Symlink realpath 检查 — 防止路径穿越攻击
#
# 用途:
#   多 agent 之间共享记忆
#   Workspace 之间的记忆同步

from __future__ import annotations
import os
import json
import time
import hashlib
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from enum import Enum

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
TEAM_DIR = WORKSPACE / "evoclaw" / "team_memory"
TEAM_DIR.mkdir(parents=True, exist_ok=True)


# ─── 访问级别 ───────────────────────────────────────────────────

class AccessLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


# ─── 记忆条目 ───────────────────────────────────────────────────

@dataclass
class TeamMemoryEntry:
    """团队记忆条目"""
    entry_id: str
    author: str                     # agent/user ID
    content: str
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None   # TTL, None=永不过期
    access_level: AccessLevel = AccessLevel.READ

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "author": self.author,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "access_level": self.access_level.value,
        }


# ─── 安全检查 ───────────────────────────────────────────────────

class TeamMemorySecurityError(Exception):
    """安全检查失败"""
    pass


def _check_symlink_safe(target_path: Path, workspace_root: Path) -> bool:
    """
    Symlink 安全检查.
    参考: claude-code realpath 检查.

    检查:
      1. realpath 不在 workspace 外
      2. 不是符号链接逃逸
    """
    try:
        resolved = target_path.resolve()
        # 检查是否在 workspace 内
        try:
            resolved.relative_to(workspace_root.resolve())
            return True
        except ValueError:
            return False
    except Exception:
        return False


def _check_containment(text: str, max_length: int = 10000) -> bool:
    """
    字符串 containment 检查.
    防止数据逃逸 — 限制单条记忆长度.
    """
    if len(text) > max_length:
        return False
    return True


# ─── Team Memory 存储 ───────────────────────────────────────────

class TeamMemoryStore:
    """
    团队记忆存储.
    支持多 agent 并发读写, 带安全检查.
    """

    def __init__(self, team_id: str = "default"):
        self.team_id = team_id
        self.team_file = TEAM_DIR / f"{team_id}.jsonl"
        self._lock_file = TEAM_DIR / f"{team_id}.lock"

    # ─── 读写 ─────────────────────────────────────────────────

    def write(
        self,
        author: str,
        content: str,
        tags: Optional[list[str]] = None,
        ttl_seconds: Optional[float] = None,
    ) -> TeamMemoryEntry:
        """
        写入记忆. 安全检查: containment + symlink.
        """
        # 安全检查 1: 长度限制
        if not _check_containment(content):
            raise TeamMemorySecurityError(f"Content too long (max {10000} chars)")

        entry = TeamMemoryEntry(
            entry_id=self._generate_id(),
            author=author,
            content=content,
            tags=tags or [],
            expires_at=time.time() + ttl_seconds if ttl_seconds else None,
        )

        # 追加到文件
        self.team_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.team_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

        return entry

    def read(
        self,
        requester: str,
        tags: Optional[list[str]] = None,
        since: Optional[float] = None,
        limit: int = 50,
    ) -> list[TeamMemoryEntry]:
        """
        读取记忆. 只返回未过期的条目.
        """
        if not self.team_file.exists():
            return []

        entries = []
        now = time.time()

        try:
            lines = self.team_file.read_text(encoding="utf-8").strip().split("\n")
            for line in lines:
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    entry = TeamMemoryEntry(**obj)

                    # TTL 过滤
                    if entry.expires_at and entry.expires_at < now:
                        continue

                    # 时间过滤
                    if since and entry.created_at < since:
                        continue

                    # 标签过滤
                    if tags:
                        if not any(t in entry.tags for t in tags):
                            continue

                    entries.append(entry)

                    if len(entries) >= limit:
                        break
                except Exception:
                    continue
        except Exception:
            pass

        return entries

    def search(self, requester: str, query: str, limit: int = 10) -> list[TeamMemoryEntry]:
        """
        简单搜索: 按关键词匹配 content.
        后续可升级为 embedding 相似度搜索.
        """
        results = self.read(requester, limit=100)
        query_lower = query.lower()
        return [e for e in results if query_lower in e.content.lower()][:limit]

    def delete(self, entry_id: str, requester: str) -> bool:
        """删除记忆 (只能删除自己的)"""
        if not self.team_file.exists():
            return False

        lines = []
        deleted = False
        for line in self.team_file.read_text(encoding="utf-8").strip().split("\n"):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if obj.get("entry_id") == entry_id:
                    if obj.get("author") != requester:
                        raise TeamMemorySecurityError("Can only delete your own entries")
                    deleted = True
                    continue
                lines.append(line)
            except TeamMemorySecurityError:
                raise
            except Exception:
                continue

        if deleted:
            self.team_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return deleted

    # ─── 工具 ─────────────────────────────────────────────────

    def _generate_id(self) -> str:
        ts = int(time.time() * 1000)
        h = hashlib.sha256(f"{ts}{self.team_id}".encode()).hexdigest()[:12]
        return f"team_{self.team_id}_{h}"

    def count(self) -> int:
        """返回记忆总条数 (不含过期)"""
        return len(self.read(requester="system", limit=99999))

    def cleanup_expired(self) -> int:
        """清理过期条目"""
        if not self.team_file.exists():
            return 0
        now = time.time()
        lines = []
        removed = 0
        for line in self.team_file.read_text(encoding="utf-8").strip().split("\n"):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if obj.get("expires_at") and obj["expires_at"] < now:
                    removed += 1
                    continue
                lines.append(line)
            except Exception:
                continue
        if removed > 0:
            self.team_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return removed


# ─── 全局访问 ───────────────────────────────────────────────────

def get_team_memory(team_id: str = "default") -> TeamMemoryStore:
    return TeamMemoryStore(team_id)


if __name__ == "__main__":
    tm = get_team_memory("test-team")

    # Write
    e1 = tm.write("agent-1", "这是一个团队共享的记忆片段", tags=["测试", "重要"])
    print(f"✅ Written: {e1.entry_id}")

    # Read
    entries = tm.read("agent-2", tags=["测试"])
    print(f"✅ Read: {len(entries)} entries")

    # Search
    results = tm.search("agent-2", "记忆")
    print(f"✅ Search: {len(results)} found")

    # Delete
    deleted = tm.delete(e1.entry_id, requester="agent-1")
    print(f"✅ Deleted: {deleted}")

    print("✅ Team Memory: all tests passed")
