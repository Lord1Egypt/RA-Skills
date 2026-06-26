# -*- coding: utf-8 -*-
"""
上下文缓存管理器
基于Claude Code fork-safe设计和Context缓存机制实现

核心设计：
- fork时克隆system prompt cache
- 智能压缩冗余历史
- session快速恢复
- 内容替换状态隔离
"""

import json
import gzip
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

CACHE_DIR = Path.home() / ".openclaw" / "workspace" / "tmp" / "context-cache"
CACHE_INDEX_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "context-cache-index.json"
MAX_CACHE_AGE_HOURS = 24  # 缓存过期时间
MAX_HISTORY_LENGTH = 50   # 最大消息历史长度

class ContextState(Enum):
    """上下文状态"""
    ACTIVE = "active"           # 正在使用
    FORKED = "forked"          # 已fork，有子进程
    COMPACTED = "compacted"    # 已压缩
    ARCHIVED = "archived"      # 已归档

@dataclass
class ContextSnapshot:
    """上下文快照"""
    session_id: str
    system_prompt: str
    messages: List[dict]
    content_replacement_state: dict  # fork-safe关键字段
    rendered_system_prompt: str     # fork-safe关键字段
    created_at: str
    state: str
    size_chars: int
    compressed: bool

def ensure_cache_dir():
    """确保缓存目录存在"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR

def get_cache_path(session_id: str) -> Path:
    """生成缓存文件路径"""
    ensure_cache_dir()
    date_str = datetime.now().strftime("%Y%m%d")
    return CACHE_DIR / f"{session_id}-{date_str}.pkl.gz"

def compress_messages(messages: List[dict]) -> List[dict]:
    """
    智能压缩消息历史
    
    策略：
    1. 保留最近20条完整消息
    2. 更早的消息只保留key字段
    3. system消息始终完整保留
    """
    if len(messages) <= MAX_HISTORY_LENGTH:
        return messages
    
    # 保留最近20条
    recent = messages[-20:]
    
    # 旧消息压缩为摘要
    older = messages[:-20]
    summary = {
        "role": "system",
        "content": f"[Compressed {len(older)} older messages]",
        "_compressed": True,
        "_original_count": len(older)
    }
    
    # 查找并保留system消息
    system_msgs = [m for m in older if m.get("role") == "system"]
    
    return system_msgs + [summary] + recent

def create_snapshot(
    session_id: str,
    system_prompt: str,
    messages: List[dict],
    content_replacement_state: dict = None,
    rendered_system_prompt: str = None
) -> ContextSnapshot:
    """
    创建上下文快照（fork-safe）
    
    参考Claude Code的fork设计：
    - contentReplacementState必须克隆
    - renderedSystemPrompt必须克隆
    - messages必须克隆
    """
    # 压缩消息
    compressed_messages = compress_messages(messages)
    
    # fork-safe克隆
    snapshot = ContextSnapshot(
        session_id=session_id,
        system_prompt=system_prompt,
        messages=compressed_messages,
        content_replacement_state=content_replacement_state or {},
        rendered_system_prompt=rendered_system_prompt or system_prompt,
        created_at=datetime.now().isoformat(),
        state=ContextState.ACTIVE.value,
        size_chars=len(json.dumps(compressed_messages)),
        compressed=len(messages) > MAX_HISTORY_LENGTH
    )
    
    return snapshot

def save_snapshot(snapshot: ContextSnapshot) -> Path:
    """保存快照到磁盘"""
    cache_path = get_cache_path(snapshot.session_id)
    
    # pickle + gzip压缩
    with gzip.open(cache_path, 'wb') as f:
        pickle.dump(asdict(snapshot), f)
    
    # 更新索引
    update_cache_index(snapshot)
    
    return cache_path

def load_snapshot(session_id: str) -> Optional[ContextSnapshot]:
    """从磁盘加载快照"""
    cache_path = get_cache_path(session_id)
    
    # 查找可能的文件
    for file_path in CACHE_DIR.glob(f"{session_id}-*.pkl.gz"):
        try:
            with gzip.open(file_path, 'rb') as f:
                data = pickle.load(f)
                return ContextSnapshot(**data)
        except Exception:
            continue
    
    return None

def update_cache_index(snapshot: ContextSnapshot):
    """更新缓存索引"""
    index = {}
    if CACHE_INDEX_FILE.exists():
        try:
            with open(CACHE_INDEX_FILE, 'r', encoding='utf-8') as f:
                index = json.load(f)
        except:
            pass
    
    index[snapshot.session_id] = {
        "created_at": snapshot.created_at,
        "size_chars": snapshot.size_chars,
        "compressed": snapshot.compressed,
        "state": snapshot.state
    }
    
    CACHE_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def fork_context(
    parent_session_id: str,
    child_session_id: str
) -> Optional[ContextSnapshot]:
    """
    Fork上下文到新session
    
    关键：必须克隆父进程的三个关键字段
    """
    parent = load_snapshot(parent_session_id)
    if not parent:
        return None
    
    # 标记父状态为forked
    parent.state = ContextState.FORKED.value
    save_snapshot(parent)
    
    # 创建子快照（克隆所有关键字段）
    child = ContextSnapshot(
        session_id=child_session_id,
        system_prompt=parent.system_prompt,
        messages=parent.messages.copy(),  # 克隆消息
        content_replacement_state=parent.content_replacement_state.copy(),  # 克隆替换状态
        rendered_system_prompt=parent.rendered_system_prompt,  # 克隆rendered提示
        created_at=datetime.now().isoformat(),
        state=ContextState.ACTIVE.value,
        size_chars=parent.size_chars,
        compressed=parent.compressed
    )
    
    save_snapshot(child)
    return child

def cleanup_expired_cache(max_age_hours: int = MAX_CACHE_AGE_HOURS) -> int:
    """清理过期缓存"""
    if not CACHE_DIR.exists():
        return 0
    
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    deleted = 0
    
    for file_path in CACHE_DIR.glob("*.pkl.gz"):
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        if mtime < cutoff:
            file_path.unlink()
            deleted += 1
    
    return deleted

def get_cache_stats() -> dict:
    """获取缓存统计"""
    if not CACHE_DIR.exists():
        return {"total_files": 0, "total_size_bytes": 0}
    
    total_size = sum(f.stat().st_size for f in CACHE_DIR.glob("*.pkl.gz"))
    return {
        "total_files": len(list(CACHE_DIR.glob("*.pkl.gz"))),
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2)
    }

class ContextCacheManager:
    """
    上下文缓存管理器
    """
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id
        self.snapshot: Optional[ContextSnapshot] = None
    
    def capture(
        self,
        system_prompt: str,
        messages: List[dict],
        content_replacement_state: dict = None,
        rendered_system_prompt: str = None
    ) -> Path:
        """捕获当前上下文"""
        self.snapshot = create_snapshot(
            self.session_id,
            system_prompt,
            messages,
            content_replacement_state,
            rendered_system_prompt
        )
        return save_snapshot(self.snapshot)
    
    def restore(self) -> Optional[ContextSnapshot]:
        """恢复上下文"""
        self.snapshot = load_snapshot(self.session_id)
        return self.snapshot
    
    def fork(self, child_session_id: str) -> Optional[ContextSnapshot]:
        """Fork到新session"""
        return fork_context(self.session_id, child_session_id)

if __name__ == "__main__":
    # 测试
    print("Context Cache Manager")
    print(f"Cache dir: {ensure_cache_dir()}")
    
    # 创建测试snapshot
    manager = ContextCacheManager("test-session-001")
    path = manager.capture(
        system_prompt="You are a helpful assistant.",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
    )
    print(f"Snapshot saved: {path}")
    
    # 恢复
    restored = manager.restore()
    print(f"Restored: {restored.session_id}, messages: {len(restored.messages)}")
    
    # Fork
    forked = manager.fork("child-session-002")
    print(f"Forked: {forked.session_id if forked else 'failed'}")
    
    # 统计
    print(f"Cache stats: {get_cache_stats()}")
