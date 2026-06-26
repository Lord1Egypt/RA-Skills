"""
memory_core.py - 核心接口与数据模型

定义全系统的记忆条目结构、查询接口和核心抽象。
"""

from __future__ import annotations

import uuid
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


# =============================================================================
# 枚举定义
# =============================================================================

class MemoryType(Enum):
    """记忆类型"""
    FACT = "fact"              # 事实性记忆（知识、规则）
    EPISODE = "episode"        # 情景记忆（事件、任务）
    PROCEDURE = "procedure"    # 程序性记忆（流程、方法）
    PREFERENCE = "preference"  # 偏好记忆（设置、习惯）
    CONTEXT = "context"        # 上下文记忆（当前会话状态）


class MemoryScope(Enum):
    """记忆作用域"""
    PRIVATE = "private"        # Agent私有
    SHARED = "shared"          # 共享知识池
    SESSION = "session"        # 当前会话


class MemoryImportance(Enum):
    """记忆重要性等级"""
    CRITICAL = 5  # 核心决策、重大事件
    HIGH = 4      # 重要事实、偏好
    MEDIUM = 3    # 一般信息
    LOW = 2       # 临时状态
    EPHEMERAL = 1 # 瞬时上下文


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class MemoryEntry:
    """
    记忆条目 - 记忆系统的基本存储单元
    
    设计原则：
    - 每个条目有唯一ID，支持细粒度引用
    - importance 决定持久化策略（低等级自动过期）
    - tags 支持多维度检索
    - scope 决定可见性（私有/共享/会话）
    """
    content: str                          # 记忆内容（文本）
    memory_type: MemoryType               # 记忆类型
    scope: MemoryScope                     # 作用域
    importance: MemoryImportance = MemoryImportance.MEDIUM
    
    # 元数据
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""                     # 创建者Agent ID
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    accessed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # 检索字段
    tags: list[str] = field(default_factory=list)
    related_agent_ids: list[str] = field(default_factory=list)  # 关联Agent
    related_entry_ids: list[str] = field(default_factory=list)   # 关联记忆
    
    # 生命周期
    ttl_seconds: float = 3600.0            # 存活时间（秒）
    version: int = 1                       # 版本号（乐观锁）
    is_deleted: bool = False               # 软删除标记
    is_pinned: bool = False                # 置顶标记（不被自动清理）
    
    # 内容管理
    summary: str = ""                      # 自动摘要
    source: str = ""                       # 来源（user/system/agent）
    
    @property
    def content_hash(self) -> str:
        """内容的稳定哈希，用于去重检测"""
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]
    
    @property
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.is_pinned:
            return False
        elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(self.created_at)).total_seconds()
        return elapsed > self.ttl_seconds
    
    @property
    def age_seconds(self) -> float:
        """记忆年龄（秒）"""
        return (datetime.now(timezone.utc) - datetime.fromisoformat(self.created_at)).total_seconds()
    
    def touch(self):
        """更新访问时间"""
        self.accessed_at = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        """序列化"""
        return {
            "entry_id": self.entry_id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "scope": self.scope.value,
            "importance": self.importance.value,
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "accessed_at": self.accessed_at,
            "tags": self.tags,
            "related_agent_ids": self.related_agent_ids,
            "related_entry_ids": self.related_entry_ids,
            "ttl_seconds": self.ttl_seconds,
            "version": self.version,
            "is_deleted": self.is_deleted,
            "is_pinned": self.is_pinned,
            "summary": self.summary,
            "source": self.source,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> MemoryEntry:
        """反序列化"""
        return cls(
            entry_id=data["entry_id"],
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            scope=MemoryScope(data["scope"]),
            importance=MemoryImportance(data.get("importance", 3)),
            agent_id=data.get("agent_id", ""),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
            accessed_at=data.get("accessed_at", datetime.now(timezone.utc).isoformat()),
            tags=data.get("tags", []),
            related_agent_ids=data.get("related_agent_ids", []),
            related_entry_ids=data.get("related_entry_ids", []),
            ttl_seconds=data.get("ttl_seconds", 3600.0),
            version=data.get("version", 1),
            is_deleted=data.get("is_deleted", False),
            is_pinned=data.get("is_pinned", False),
            summary=data.get("summary", ""),
            source=data.get("source", ""),
        )


@dataclass
class MemoryQuery:
    """记忆查询条件"""
    # 检索词
    query_text: str = ""                   # 全文检索关键词
    tags: list[str] = field(default_factory=list)  # 标签过滤
    
    # 作用域过滤
    scope: Optional[MemoryScope] = None     # 指定作用域
    scopes: list[MemoryScope] = field(default_factory=list)  # 允许多作用域
    agent_id: Optional[str] = None          # 指定Agent
    caller_agent_id: str = ""               # 调用者Agent（用于权限判断）
    
    # 类型过滤
    memory_type: Optional[MemoryType] = None
    memory_types: list[MemoryType] = field(default_factory=list)
    
    # 重要性过滤
    min_importance: MemoryImportance = MemoryImportance.EPHEMERAL
    
    # 时间范围
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    # 分页
    limit: int = 20
    offset: int = 0
    
    # 排序
    sort_by: str = "importance"  # importance | created_at | accessed_at
    descending: bool = True
    
    def is_visible_to(self, entry: MemoryEntry) -> bool:
        """判断记忆条目对调用者是否可见"""
        # 已删除
        if entry.is_deleted:
            return False
        # 已过期（非置顶）
        if entry.is_expired:
            return False
        # 作用域权限
        if entry.scope == MemoryScope.PRIVATE:
            return entry.agent_id == self.caller_agent_id
        if entry.scope == MemoryScope.SESSION:
            return True
        # SHARED 对所有Agent可见
        return True


@dataclass
class MemoryResult:
    """记忆查询结果"""
    entries: list[MemoryEntry] = field(default_factory=list)
    total: int = 0
    query: Optional[MemoryQuery] = None
    
    # 统计信息
    scope_breakdown: dict[str, int] = field(default_factory=dict)
    type_breakdown: dict[str, int] = field(default_factory=dict)
    
    # 聚合信息
    top_tags: list[tuple[str, int]] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "entries": [e.to_dict() for e in self.entries],
            "total": self.total,
            "scope_breakdown": self.scope_breakdown,
            "type_breakdown": self.type_breakdown,
            "top_tags": self.top_tags,
        }


# =============================================================================
# 核心接口
# =============================================================================

class MemoryCore:
    """
    记忆核心接口 - 所有记忆组件的基类
    
    定义统一的记忆读写接口，子类实现具体存储逻辑。
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
    
    # --- 写入接口 ---
    
    def store(self, entry: MemoryEntry) -> str:
        """
        存储记忆条目
        Returns: entry_id
        """
        raise NotImplementedError
    
    def update(self, entry_id: str, content: str, **kwargs) -> bool:
        """更新记忆"""
        raise NotImplementedError
    
    def delete(self, entry_id: str, soft: bool = True) -> bool:
        """删除记忆"""
        raise NotImplementedError
    
    # --- 读取接口 ---
    
    def query(self, q: MemoryQuery) -> MemoryResult:
        """查询记忆"""
        raise NotImplementedError
    
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取单条记忆"""
        raise NotImplementedError
    
    def get_recent(self, limit: int = 10, scope: Optional[MemoryScope] = None) -> list[MemoryEntry]:
        """获取最近的记忆"""
        raise NotImplementedError
    
    # --- 生命周期管理 ---
    
    def prune_expired(self) -> int:
        """清理过期记忆，返回清理数量"""
        raise NotImplementedError
    
    def get_stats(self) -> dict[str, Any]:
        """获取记忆统计"""
        raise NotImplementedError
