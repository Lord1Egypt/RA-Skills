"""
private_memory.py - Agent 私有记忆隔离

每个 Agent 拥有独立的私有记忆空间，支持：
- 完全隔离的读写权限
- 按 Agent ID 自动路由
- 私有偏好记忆存储
- 任务上下文快照
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Optional

from .memory_core import (
    MemoryEntry,
    MemoryImportance,
    MemoryQuery,
    MemoryResult,
    MemoryScope,
    MemoryType,
)
from .persistent_store import PersistentStore, get_cursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrivateMemory:
    """
    Agent 私有记忆
    
    设计原则：
    - 每个 Agent 只有自己能看到自己的私有记忆
    - 存储内容：Agent个人偏好、工作习惯、专用知识、任务中间状态
    - 与 SharedKnowledgePool 完全隔离
    """
    
    def __init__(
        self,
        agent_id: str,
        store: Optional[PersistentStore] = None,
    ):
        self.agent_id = agent_id
        self.store = store or PersistentStore()
    
    # -------------------------------------------------------------------------
    # 写入操作
    # -------------------------------------------------------------------------
    
    def memorize(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.EPISODE,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        tags: list[str] | None = None,
        ttl_seconds: float = 86400.0,
        summary: str = "",
        source: str = "agent",
    ) -> str:
        """
        记忆存储 - Agent 私有记忆的核心写入接口
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性等级（决定保留时长）
            tags: 标签列表
            ttl_seconds: 存活时间
            summary: 自动摘要
            source: 来源
            
        Returns:
            entry_id
        """
        # 重要性决定默认 TTL
        importance_ttl_map = {
            MemoryImportance.CRITICAL: 365 * 86400,  # 1年
            MemoryImportance.HIGH: 90 * 86400,        # 90天
            MemoryImportance.MEDIUM: 30 * 86400,      # 30天
            MemoryImportance.LOW: 7 * 86400,           # 7天
            MemoryImportance.EPHEMERAL: 3600,          # 1小时
        }
        effective_ttl = max(ttl_seconds, importance_ttl_map.get(importance, 86400.0))
        
        entry = MemoryEntry(
            content=content,
            memory_type=memory_type,
            scope=MemoryScope.PRIVATE,
            importance=importance,
            agent_id=self.agent_id,
            tags=tags or [],
            ttl_seconds=effective_ttl,
            summary=summary,
            source=source,
        )
        
        entry_id = self.store.store(entry)
        logger.debug(f"[{self.agent_id}] memorized: {entry_id} ({memory_type.value})")
        return entry_id
    
    def memorize_preference(
        self,
        content: str,
        importance: MemoryImportance = MemoryImportance.HIGH,
    ) -> str:
        """存储 Agent 偏好记忆（快捷方法）"""
        return self.memorize(
            content=content,
            memory_type=MemoryType.PREFERENCE,
            importance=importance,
            tags=["preference", "personal"],
            ttl_seconds=180 * 86400,  # 半年
        )
    
    def memorize_knowledge(
        self,
        content: str,
        importance: MemoryImportance = MemoryImportance.HIGH,
        tags: list[str] | None = None,
    ) -> str:
        """存储 Agent 专用知识（快捷方法）"""
        return self.memorize(
            content=content,
            memory_type=MemoryType.FACT,
            importance=importance,
            tags=["knowledge", "personal"] + (tags or []),
            ttl_seconds=180 * 86400,
        )
    
    def memorize_task_context(
        self,
        task_id: str,
        context: str,
        stage: str = "in_progress",
    ) -> str:
        """存储任务上下文快照（快捷方法）"""
        return self.memorize(
            content=f"[Task {task_id}] {context}",
            memory_type=MemoryType.CONTEXT,
            importance=MemoryImportance.MEDIUM,
            tags=["task", task_id, stage],
            ttl_seconds=7200.0,  # 2小时
        )
    
    def memorize_rule(
        self,
        rule: str,
        reason: str = "",
    ) -> str:
        """存储从经验中提炼的规则（快捷方法）"""
        content = rule
        if reason:
            content += f"\n\n原因：{reason}"
        return self.memorize(
            content=content,
            memory_type=MemoryType.PROCEDURE,
            importance=MemoryImportance.HIGH,
            tags=["rule", "learned"],
            ttl_seconds=365 * 86400,
        )
    
    # -------------------------------------------------------------------------
    # 读取操作
    # -------------------------------------------------------------------------
    
    def recall(
        self,
        query_text: str = "",
        memory_type: MemoryType | None = None,
        tags: list[str] | None = None,
        limit: int = 20,
    ) -> MemoryResult:
        """召回记忆"""
        q = MemoryQuery(
            query_text=query_text,
            memory_type=memory_type,
            tags=tags or [],
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,        # 只查自己的
            caller_agent_id=self.agent_id, # 自己是调用者，有权限看
            limit=limit,
        )
        return self.store.query(q)
    
    def recall_preferences(self) -> list[MemoryEntry]:
        """召回所有偏好记忆"""
        q = MemoryQuery(
            memory_type=MemoryType.PREFERENCE,
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
            caller_agent_id=self.agent_id,
            limit=50,
        )
        result = self.store.query(q)
        return result.entries
    
    def recall_knowledge(self, query: str = "") -> list[MemoryEntry]:
        """召回知识记忆"""
        q = MemoryQuery(
            query_text=query,
            memory_type=MemoryType.FACT,
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
            caller_agent_id=self.agent_id,
            limit=30,
        )
        return self.store.query(q).entries
    
    def recall_rules(self) -> list[MemoryEntry]:
        """召回所有提炼规则"""
        q = MemoryQuery(
            memory_type=MemoryType.PROCEDURE,
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
            caller_agent_id=self.agent_id,
            limit=50,
        )
        return self.store.query(q).entries
    
    def recall_task_context(self, task_id: str) -> list[MemoryEntry]:
        """召回特定任务的上下文"""
        q = MemoryQuery(
            tags=[task_id],
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
            caller_agent_id=self.agent_id,
            limit=20,
        )
        return self.store.query(q).entries
    
    # -------------------------------------------------------------------------
    # 更新与删除
    # -------------------------------------------------------------------------
    
    def forget(self, entry_id: str, soft: bool = True) -> bool:
        """遗忘（删除）记忆"""
        # 验证权限：只能删除自己的
        entry = self.store.get(entry_id)
        if entry is None:
            return False
        if entry.agent_id != self.agent_id:
            logger.warning(f"[{self.agent_id}] Unauthorized delete attempt: {entry_id}")
            return False
        return self.store.delete(entry_id, soft=soft)
    
    def refine(self, entry_id: str, new_content: str) -> bool:
        """精化记忆"""
        entry = self.store.get(entry_id)
        if entry is None or entry.agent_id != self.agent_id:
            return False
        return self.store.update(entry_id, content=new_content)
    
    def pin(self, entry_id: str) -> bool:
        """置顶记忆"""
        entry = self.store.get(entry_id)
        if entry is None or entry.agent_id != self.agent_id:
            return False
        return self.store.update(entry_id, is_pinned=True)
    
    # -------------------------------------------------------------------------
    # 上下文构建
    # -------------------------------------------------------------------------
    
    def build_context_for_task(
        self,
        task_description: str,
        max_entries: int = 10,
    ) -> str:
        """
        为任务构建相关记忆上下文
        
        检索与任务相关的私有记忆，生成结构化上下文字符串。
        """
        # 并行检索：知识 + 规则 + 近期记忆
        knowledge_q = MemoryQuery(
            query_text=task_description,
            memory_type=MemoryType.FACT,
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
            caller_agent_id=self.agent_id,
            min_importance=MemoryImportance.MEDIUM,
            limit=max_entries,
        )
        
        rules_q = MemoryQuery(
            query_text=task_description,
            memory_type=MemoryType.PROCEDURE,
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
            caller_agent_id=self.agent_id,
            limit=max_entries,
        )
        
        k_result = self.store.query(knowledge_q)
        r_result = self.store.query(rules_q)
        
        context_parts = []
        
        if k_result.entries:
            context_parts.append("【相关知识】")
            for e in k_result.entries[:5]:
                context_parts.append(f"- {e.summary or e.content[:100]}")
        
        if r_result.entries:
            context_parts.append("【相关规则】")
            for e in r_result.entries[:5]:
                context_parts.append(f"- {e.content[:150]}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def get_stats(self) -> dict[str, Any]:
        """获取该 Agent 的私有记忆统计"""
        stats = self.store.get_stats()
        with get_cursor(self.store.db_path) as cur:
            cur.execute(
                "SELECT COUNT(*) as c FROM memory_entries WHERE agent_id=? AND scope='private' AND is_deleted=0",
                (self.agent_id,),
            )
            stats["agent_private_count"] = cur.fetchone()["c"]
        return stats
