"""
shared_knowledge.py - 共享知识池

跨 Agent 共享的知识库，支持：
- 共享事实（Shared Facts）
- 协作成果（Collaboration Artifacts）
- 组织知识（Organization Knowledge）
- 全局规则（Global Rules）
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


class SharedKnowledgePool:
    """
    共享知识池 - 所有 Agent 可读，授权 Agent 可写
    
    层级结构：
    1. facts     : 共享事实（事实性知识，任何Agent可读，高权限Agent可写）
    2. artifacts : 协作成果（多Agent协作产生的成果，如分析报告、决策）
    3. org_knowledge: 组织知识（公司政策、业务规则、行业知识）
    4. rules     : 全局规则（跨Agent协作协议、标准流程）
    """
    
    # 共享知识池子类型
    class PoolType:
        FACTS = "shared_facts"
        ARTIFACTS = "collaboration_artifacts"
        ORG_KNOWLEDGE = "org_knowledge"
        RULES = "global_rules"
    
    # 写入权限矩阵（agent_id -> 可写类型）
    WRITE_PERMISSIONS = {
        "orchestrator": ["shared_facts", "collaboration_artifacts", "org_knowledge", "global_rules"],
        "admin": ["shared_facts", "collaboration_artifacts", "org_knowledge", "global_rules"],
    }
    
    def __init__(self, store: Optional[PersistentStore] = None):
        self.store = store or PersistentStore()
    
    def _get_writable_types(self, agent_id: str) -> list[str]:
        """获取某 Agent 可写的池子类型"""
        return self.WRITE_PERMISSIONS.get(agent_id, [])
    
    # -------------------------------------------------------------------------
    # 写入操作
    # -------------------------------------------------------------------------
    
    def publish_fact(
        self,
        content: str,
        author_agent_id: str,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        tags: list[str] | None = None,
        summary: str = "",
    ) -> str:
        """
        发布共享事实
        
        使用场景：
        - 库存智能体发布：{"SKU001": {"qty": 100, "warehouse": "A"}}
        - 物流智能体发布：{"order_123": {"status": "shipped", "carrier": "SF"}}
        """
        entry = MemoryEntry(
            content=content,
            memory_type=MemoryType.FACT,
            scope=MemoryScope.SHARED,
            importance=importance,
            agent_id=author_agent_id,
            tags=["shared_fact"] + (tags or []),
            ttl_seconds=90 * 86400,  # 默认90天
            summary=summary,
            source="agent",
        )
        return self.store.store(entry)
    
    def publish_artifact(
        self,
        content: str,
        author_agent_id: str,
        related_agent_ids: list[str],
        artifact_type: str = "report",
        importance: MemoryImportance = MemoryImportance.HIGH,
        summary: str = "",
    ) -> str:
        """
        发布协作成果
        
        使用场景：
        - 财务+采购协作：成本分析报告
        - 多Agent协作：战略规划文档
        """
        entry = MemoryEntry(
            content=content,
            memory_type=MemoryType.FACT,  # 成果也是一种事实
            scope=MemoryScope.SHARED,
            importance=importance,
            agent_id=author_agent_id,
            related_agent_ids=related_agent_ids,
            tags=["artifact", artifact_type, "collaboration"] + related_agent_ids,
            ttl_seconds=180 * 86400,  # 半年
            summary=summary or content[:100],
            source="agent",
        )
        return self.store.store(entry)
    
    def publish_rule(
        self,
        content: str,
        author_agent_id: str,
        rule_type: str = "protocol",
        importance: MemoryImportance = MemoryImportance.HIGH,
    ) -> str:
        """发布全局规则/协议"""
        entry = MemoryEntry(
            content=content,
            memory_type=MemoryType.PROCEDURE,
            scope=MemoryScope.SHARED,
            importance=importance,
            agent_id=author_agent_id,
            tags=["global_rule", rule_type],
            ttl_seconds=365 * 86400,  # 永久
            source="agent",
        )
        return self.store.store(entry)
    
    def publish_knowledge(
        self,
        content: str,
        author_agent_id: str,
        category: str = "general",
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        tags: list[str] | None = None,
        summary: str = "",
    ) -> str:
        """发布组织知识"""
        entry = MemoryEntry(
            content=content,
            memory_type=MemoryType.FACT,
            scope=MemoryScope.SHARED,
            importance=importance,
            agent_id=author_agent_id,
            tags=["org_knowledge", category] + (tags or []),
            ttl_seconds=180 * 86400,
            summary=summary,
            source="agent",
        )
        return self.store.store(entry)
    
    # -------------------------------------------------------------------------
    # 读取操作
    # -------------------------------------------------------------------------
    
    def query_knowledge(
        self,
        query_text: str = "",
        tags: list[str] | None = None,
        caller_agent_id: str = "",
        importance: MemoryImportance = MemoryImportance.LOW,
        limit: int = 30,
    ) -> MemoryResult:
        """查询共享知识"""
        q = MemoryQuery(
            query_text=query_text,
            tags=tags or [],
            scope=MemoryScope.SHARED,
            caller_agent_id=caller_agent_id,
            min_importance=importance,
            limit=limit,
        )
        return self.store.query(q)
    
    def query_by_pool_type(
        self,
        pool_type: str,
        caller_agent_id: str = "",
        limit: int = 20,
    ) -> list[MemoryEntry]:
        """按池子类型查询"""
        q = MemoryQuery(
            tags=[pool_type],
            scope=MemoryScope.SHARED,
            caller_agent_id=caller_agent_id,
            limit=limit,
        )
        return self.store.query(q).entries
    
    def get_latest_facts(
        self,
        caller_agent_id: str = "",
        limit: int = 20,
    ) -> list[MemoryEntry]:
        """获取最新共享事实"""
        q = MemoryQuery(
            tags=["shared_fact"],
            scope=MemoryScope.SHARED,
            caller_agent_id=caller_agent_id,
            limit=limit,
            sort_by="created_at",
        )
        return self.store.query(q).entries
    
    def get_artifacts(
        self,
        caller_agent_id: str = "",
        related_agent_id: str = "",
        limit: int = 10,
    ) -> list[MemoryEntry]:
        """获取协作成果"""
        q = MemoryQuery(
            tags=["artifact"],
            scope=MemoryScope.SHARED,
            caller_agent_id=caller_agent_id,
            limit=limit,
            sort_by="created_at",
        )
        result = self.store.query(q)
        
        # 额外过滤：按关联Agent
        if related_agent_id:
            return [e for e in result.entries if related_agent_id in e.related_agent_ids]
        return result.entries
    
    def get_global_rules(
        self,
        caller_agent_id: str = "",
    ) -> list[MemoryEntry]:
        """获取全局规则（所有Agent可用）"""
        q = MemoryQuery(
            tags=["global_rule"],
            scope=MemoryScope.SHARED,
            caller_agent_id=caller_agent_id,
            limit=50,
            min_importance=MemoryImportance.HIGH,
        )
        return self.store.query(q).entries
    
    def get_recent_collaboration(
        self,
        agent_id: str,
        other_agent_id: str,
        limit: int = 10,
    ) -> list[MemoryEntry]:
        """获取两个Agent之间的协作历史"""
        q = MemoryQuery(
            scope=MemoryScope.SHARED,
            tags=["artifact"],
            caller_agent_id=agent_id,
            limit=50,
            sort_by="created_at",
        )
        result = self.store.query(q)
        
        # 筛选：任一相关Agent匹配
        return [
            e for e in result.entries
            if (agent_id in e.related_agent_ids or agent_id == e.agent_id)
            and (other_agent_id in e.related_agent_ids or other_agent_id == e.agent_id)
        ][:limit]
    
    # -------------------------------------------------------------------------
    # 删除与权限
    # -------------------------------------------------------------------------
    
    def retract(self, entry_id: str, agent_id: str) -> bool:
        """撤回/删除共享知识（仅原作者或orchestrator可操作）"""
        entry = self.store.get(entry_id)
        if entry is None:
            return False
        if entry.agent_id != agent_id and agent_id not in ("orchestrator", "admin"):
            logger.warning(f"[{agent_id}] Unauthorized retract attempt: {entry_id}")
            return False
        return self.store.delete(entry_id)
    
    def update_artifact(
        self,
        entry_id: str,
        new_content: str,
        agent_id: str,
    ) -> bool:
        """更新协作成果（仅原作者或orchestrator可操作）"""
        entry = self.store.get(entry_id)
        if entry is None:
            return False
        if entry.agent_id != agent_id and agent_id not in ("orchestrator", "admin"):
            return False
        return self.store.update(entry_id, content=new_content)
    
    # -------------------------------------------------------------------------
    # 统计与报告
    # -------------------------------------------------------------------------
    
    def get_pool_stats(self) -> dict[str, Any]:
        """获取知识池统计"""
        stats = self.store.get_stats()
        
        # 按池子类型统计
        with get_cursor(self.store.db_path) as cur:
            pool_stats = {}
            for pool_type in ["shared_fact", "artifact", "org_knowledge", "global_rule"]:
                cur.execute("""
                    SELECT COUNT(*) as c FROM memory_entries
                    WHERE is_deleted=0 AND scope='shared'
                    AND tags LIKE ?
                """, (f'%"{pool_type}"%',))
                pool_stats[pool_type] = cur.fetchone()["c"]
            
            # 活跃协作者统计
            cur.execute("""
                SELECT DISTINCT agent_id FROM memory_entries
                WHERE scope='shared' AND is_deleted=0 AND agent_id != ''
            """)
            pool_stats["active_agents"] = [row["agent_id"] for row in cur.fetchall()]
            
            stats["pool_breakdown"] = pool_stats
        
        return stats
