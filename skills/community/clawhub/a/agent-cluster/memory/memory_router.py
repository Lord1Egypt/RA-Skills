"""
memory_router.py - 记忆访问路由

作为统一的记忆访问网关：
- 自动判断作用域（Private / Shared / Session）
- Agent 权限校验
- 路由到正确的底层组件
- 提供统一的读写 API
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from .memory_core import (
    MemoryEntry,
    MemoryImportance,
    MemoryQuery,
    MemoryResult,
    MemoryScope,
    MemoryType,
)
from .persistent_store import PersistentStore
from .private_memory import PrivateMemory
from .shared_knowledge import SharedKnowledgePool
from .session_sync import SessionSync
from .memory_index import MemoryIndex

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryRouter:
    """
    记忆访问路由 - 统一入口
    
    接收 Agent 的记忆请求，自动路由到正确的存储层。
    
    路由策略：
    - scope='private'     → PrivateMemory（隔离存储）
    - scope='shared'      → SharedKnowledgePool（跨Agent共享）
    - scope='session'     → SessionSync（会话级临时）
    - scope=None (auto)   → 根据权限和内容类型自动判断
    
    权限矩阵：
    ┌─────────────┬─────────┬──────────┬─────────┐
    │ Agent       │ Private │ Shared   │ Session │
    ├─────────────┼─────────┼──────────┼─────────┤
    │ self        │ RW      │ R        │ RW      │
    │ other       │ -       │ R/W*     │ -       │
    │ orchestrator│ R       │ RW       │ RW      │
    └─────────────┴─────────┴──────────┴─────────┘
    (* 需满足特定条件，如参与协作或高权限)
    """

    def __init__(
        self,
        db_path: str | None = None,
        default_agent_id: str = "orchestrator",
    ):
        self.default_agent_id = default_agent_id
        self.db_path = db_path
        
        # 初始化各层组件（共享同一 db_path）
        self._store = PersistentStore(db_path=db_path or str(self._default_db()))
        self._private: dict[str, PrivateMemory] = {}  # 每个Agent独立实例
        self._shared = SharedKnowledgePool(store=self._store)
        self._session = SessionSync(store=self._store)
        self._index = MemoryIndex(store=self._store)
    
    @staticmethod
    def _default_db() -> Any:
        from pathlib import Path
        return Path(__file__).parent.parent / "data" / "memory" / "memory.db"
    
    # -------------------------------------------------------------------------
    # 组件访问器（延迟初始化）
    # -------------------------------------------------------------------------
    
    def get_private(self, agent_id: str) -> PrivateMemory:
        """获取指定Agent的私有记忆实例"""
        if agent_id not in self._private:
            self._private[agent_id] = PrivateMemory(agent_id=agent_id, store=self._store)
        return self._private[agent_id]
    
    @property
    def shared(self) -> SharedKnowledgePool:
        return self._shared
    
    @property
    def session(self) -> SessionSync:
        return self._session
    
    @property
    def index(self) -> MemoryIndex:
        return self._index
    
    # -------------------------------------------------------------------------
    # 统一写入 API
    # -------------------------------------------------------------------------
    
    def memorize(
        self,
        content: str,
        agent_id: str,
        scope: MemoryScope | str = "auto",
        memory_type: MemoryType | str = MemoryType.EPISODE,
        importance: MemoryImportance | int = MemoryImportance.MEDIUM,
        tags: list[str] | None = None,
        ttl_seconds: float = 86400.0,
        summary: str = "",
        related_agent_ids: list[str] | None = None,
        source: str = "agent",
        session_id: str | None = None,
    ) -> str:
        """
        统一记忆存储入口
        
        Args:
            content: 记忆内容
            agent_id: 写入Agent ID
            scope: 作用域（auto/priority/shared/session/private）
            memory_type: 记忆类型
            importance: 重要性（1-5）
            tags: 标签
            ttl_seconds: 存活时间
            summary: 摘要
            related_agent_ids: 关联Agent列表（用于Shared）
            source: 来源
            session_id: 会话ID（Session Scope 必填）
            
        Returns:
            entry_id
        """
        # 解析 scope
        if isinstance(scope, str):
            scope = self._resolve_scope(scope, agent_id, session_id)
        
        if isinstance(memory_type, str):
            memory_type = MemoryType(memory_type)
        
        if isinstance(importance, int):
            importance = MemoryImportance(importance)
        
        # 路由分发
        if scope == MemoryScope.PRIVATE:
            return self.get_private(agent_id).memorize(
                content=content,
                memory_type=memory_type,
                importance=importance,
                tags=tags,
                ttl_seconds=ttl_seconds,
                summary=summary,
                source=source,
            )
        
        elif scope == MemoryScope.SHARED:
            return self._shared.publish_knowledge(
                content=content,
                author_agent_id=agent_id,
                category=tags[0] if tags else "general",
                importance=importance,
                tags=tags,
                summary=summary,
            )
        
        elif scope == MemoryScope.SESSION:
            if not session_id:
                raise ValueError("session_id is required for SESSION scope")
            return self._session.store_session_knowledge(
                session_id=session_id,
                agent_id=agent_id,
                content=content,
                knowledge_type=tags[0] if tags else "context",
                importance=importance,
            )
        
        else:
            # 兜底：存到私有记忆
            return self.get_private(agent_id).memorize(
                content=content,
                memory_type=memory_type,
                importance=importance,
                tags=tags,
                ttl_seconds=ttl_seconds,
                summary=summary,
                source=source,
            )
    
    def _resolve_scope(
        self,
        scope: str,
        agent_id: str,
        session_id: str | None,
    ) -> MemoryScope:
        """根据关键词自动解析 scope"""
        scope_map = {
            "private": MemoryScope.PRIVATE,
            "shared": MemoryScope.SHARED,
            "session": MemoryScope.SESSION,
            "auto": None,
        }
        
        resolved = scope_map.get(scope)
        if resolved is not None:
            return resolved
        
        # auto 模式：根据内容类型判断
        if scope == "auto":
            if session_id:
                return MemoryScope.SESSION
            return MemoryScope.PRIVATE
        
        return MemoryScope.PRIVATE
    
    # -------------------------------------------------------------------------
    # 统一读取 API
    # -------------------------------------------------------------------------
    
    def recall(
        self,
        agent_id: str,
        query_text: str = "",
        scope: MemoryScope | str = "all",
        memory_type: str | None = None,
        tags: list[str] | None = None,
        session_id: str | None = None,
        limit: int = 20,
    ) -> MemoryResult:
        """
        统一记忆查询入口
        
        Args:
            agent_id: 调用者Agent ID
            query_text: 检索关键词
            scope: 查询作用域
            memory_type: 记忆类型过滤
            tags: 标签过滤
            session_id: 会话ID（查询SESSION时必填）
            limit: 返回数量限制
        """
        # 解析 scope
        if isinstance(scope, str):
            scopes = self._resolve_scopes(scope, session_id)
        else:
            scopes = [scope]
        
        # 类型解析
        from .memory_core import MemoryType as MT
        types = [MT(t) for t in (memory_type or "").split(",") if t]
        
        q = MemoryQuery(
            query_text=query_text,
            tags=tags or [],
            scopes=scopes,
            caller_agent_id=agent_id,
            memory_types=types,
            limit=limit,
        )
        
        # 路由到 index 进行加权检索
        if scopes == [MemoryScope.SESSION] and session_id:
            return self._session.get_session_context(session_id, agent_id, query_text)
        
        return self._index.search(
            query_text=query_text,
            agent_id="",  # 不限Agent（允许读其他人的SHARED）
            scopes=scopes,
            memory_types=[t.value for t in types] if types else None,
            tags=tags,
            caller_agent_id=agent_id,
            limit=limit,
        )
    
    def _resolve_scopes(self, scope: str, session_id: str | None) -> list[MemoryScope]:
        """解析 scope 字符串到作用域列表"""
        if scope == "all":
            return [MemoryScope.PRIVATE, MemoryScope.SHARED]
        if scope == "private":
            return [MemoryScope.PRIVATE]
        if scope == "shared":
            return [MemoryScope.SHARED]
        if scope == "session":
            return [MemoryScope.SESSION]
        return [MemoryScope.PRIVATE]
    
    # -------------------------------------------------------------------------
    # 高级 API
    # -------------------------------------------------------------------------
    
    def memorize_and_link(
        self,
        content: str,
        agent_id: str,
        related_agent_ids: list[str],
        scope: MemoryScope = MemoryScope.SHARED,
        memory_type: MemoryType = MemoryType.FACT,
    ) -> str:
        """
        存储记忆并自动建立关联
        
        自动：
        1. 存储记忆
        2. 关联到指定Agent
        3. 发布到共享知识池（同时给所有相关Agent发通知）
        """
        entry = MemoryEntry(
            content=content,
            memory_type=memory_type,
            scope=scope,
            importance=MemoryImportance.HIGH,
            agent_id=agent_id,
            related_agent_ids=related_agent_ids,
            tags=["linked", "collaboration"] + related_agent_ids,
            ttl_seconds=90 * 86400,
            source="agent",
        )
        entry_id = self._store.store(entry)
        
        # 触发关联Agent的通知（通过事件日志）
        if scope == MemoryScope.SHARED:
            logger.info(
                f"[{agent_id}] linked memory {entry_id} with agents: {related_agent_ids}"
            )
        
        return entry_id
    
    def build_agent_context(
        self,
        agent_id: str,
        task_query: str = "",
        include_shared: bool = True,
    ) -> str:
        """
        为指定Agent构建完整上下文
        
        包含：
        1. 私有知识（相关知识 + 规则）
        2. 共享知识（相关事实 + 规则）
        3. 最近会话
        """
        parts = []
        
        # 1. 私有知识
        private = self.get_private(agent_id)
        knowledge_context = private.build_context_for_task(task_query, max_entries=8)
        if knowledge_context:
            parts.append("【你的私人知识库】\n" + knowledge_context)
        
        # 2. 规则
        rules = private.recall_rules()
        if rules:
            parts.append("【你提炼的规则】")
            for r in rules[:5]:
                parts.append(f"- {r.content[:120]}")
        
        # 3. 共享知识
        if include_shared:
            shared_result = self._shared.query_knowledge(
                query_text=task_query,
                caller_agent_id=agent_id,
                importance=MemoryImportance.MEDIUM,
                limit=10,
            )
            if shared_result.entries:
                parts.append("【共享知识】")
                for e in shared_result.entries[:5]:
                    parts.append(f"- [{e.agent_id}] {e.summary or e.content[:80]}")
        
        # 4. 全局规则
        global_rules = self._shared.get_global_rules(caller_agent_id=agent_id)
        if global_rules:
            parts.append("【全局协作规则】")
            for r in global_rules[:3]:
                parts.append(f"- {r.content[:100]}")
        
        return "\n\n".join(parts) if parts else ""
    
    def sync_across_agents(
        self,
        content: str,
        from_agent_id: str,
        to_agent_ids: list[str],
        reason: str = "",
        session_id: str | None = None,
    ) -> dict[str, str]:
        """
        跨Agent同步知识
        
        使用场景：
        - Inventory Agent 发现库存异常 → 通知 Finance + Procurement
        - 某个Agent提炼了可复用的规则 → 同步给所有相关Agent
        
        Returns: {agent_id: entry_id} 映射
        """
        result = {}
        
        # 发布到共享知识池
        artifact_id = self._shared.publish_artifact(
            content=f"[来自 {from_agent_id} 的同步]\n{content}",
            author_agent_id=from_agent_id,
            related_agent_ids=to_agent_ids,
            artifact_type="cross_agent_sync",
            importance=MemoryImportance.HIGH,
            summary=reason or content[:60],
        )
        result["shared"] = artifact_id
        
        # 如果有会话上下文，额外存入会话
        if session_id:
            session_entry_id = self._session.store_session_knowledge(
                session_id=session_id,
                agent_id=from_agent_id,
                content=f"[跨Agent同步 → {', '.join(to_agent_ids)}]\n{content}",
                knowledge_type="cross_agent_sync",
                importance=MemoryImportance.HIGH,
            )
            result["session"] = session_entry_id
            
            # 广播事件
            self._session.log_event(
                session_id=session_id,
                agent_id=from_agent_id,
                event_type="context_share",
                content=f"同步知识给: {', '.join(to_agent_ids)}",
                related_entry_ids=[artifact_id, session_entry_id],
            )
        
        for agent_id in to_agent_ids:
            logger.info(f"[{from_agent_id}] → [{agent_id}]: {content[:50]}")
        
        return result
    
    # -------------------------------------------------------------------------
    # 管理 API
    # -------------------------------------------------------------------------
    
    def prune_all(self) -> int:
        """清理所有过期记忆"""
        return self._store.prune_expired()
    
    def get_system_stats(self) -> dict[str, Any]:
        """获取全系统记忆统计"""
        store_stats = self._store.get_stats()
        session_stats = self._session.get_session_stats()
        hot_tags = self._index.get_hot_tags(top_n=10)
        
        return {
            "store": store_stats,
            "session": session_stats,
            "hot_tags": hot_tags,
            "registered_agents": list(self._private.keys()),
        }
    
    def delete_agent_memories(self, agent_id: str) -> int:
        """删除某Agent的所有记忆（管理操作）"""
        return self._store.soft_delete_by_agent(agent_id)
