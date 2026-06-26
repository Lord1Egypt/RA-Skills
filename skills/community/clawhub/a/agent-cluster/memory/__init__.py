"""
M-A3 Multi-Agent Memory Layer
多智能体记忆层 - 跨Agent知识共享与协同记忆系统

核心组件：
- memory_core    : 核心接口与数据模型
- private_memory : Agent私有记忆（隔离）
- shared_knowledge: 共享知识池
- session_sync   : 会话记忆同步
- persistent_store: SQLite持久化
- memory_index    : 全文检索索引
- memory_router   : 记忆访问路由
"""

from .memory_core import (
    MemoryEntry,
    MemoryType,
    MemoryScope,
    MemoryImportance,
    MemoryResult,
    MemoryQuery,
    MemoryCore,
)

from .private_memory import PrivateMemory
from .shared_knowledge import SharedKnowledgePool
from .session_sync import SessionSync
from .persistent_store import PersistentStore
from .memory_index import MemoryIndex
from .memory_router import MemoryRouter

__all__ = [
    # Core models
    "MemoryEntry",
    "MemoryType",
    "MemoryScope",
    "MemoryImportance",
    "MemoryResult",
    "MemoryQuery",
    "MemoryCore",
    # Components
    "PrivateMemory",
    "SharedKnowledgePool",
    "SessionSync",
    "PersistentStore",
    "MemoryIndex",
    "MemoryRouter",
]
