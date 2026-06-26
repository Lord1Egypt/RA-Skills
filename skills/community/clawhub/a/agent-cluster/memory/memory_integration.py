"""
memory_integration.py - 集成到现有 M-A3 Agent 系统

将记忆层无缝集成到 agent-cluster 的编排层和执行层：
1. Orchestrator 集成 - 任务编排时自动记忆
2. Agent 集成 - 每个专业Agent配备私有记忆
3. 会话恢复 - 断点续传时恢复记忆上下文
4. 协同记忆 - 多Agent协作时自动同步
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from .memory_core import MemoryImportance, MemoryQuery, MemoryScope, MemoryType
from .memory_router import MemoryRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 全局单例
# =============================================================================

_memory_router: MemoryRouter | None = None


def get_memory_router(db_path: str | None = None) -> MemoryRouter:
    """获取全局记忆路由单例"""
    global _memory_router
    if _memory_router is None:
        _memory_router = MemoryRouter(db_path=db_path)
        logger.info("MemoryRouter initialized (singleton)")
    return _memory_router


# =============================================================================
# Orchestrator 集成
# =============================================================================

class OrchestratorMemoryMixin:
    """
    Orchestrator 记忆集成混入类
    
    使用方式（在 orchestrator 中继承）：
    
        class OrchestratorWithMemory(OrchestratorMemoryMixin, BaseOrchestrator):
            pass
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._memory = get_memory_router()
    
    def memorize_task_outcome(
        self,
        task: str,
        agent_id: str,
        outcome: str,
        success: bool,
        related_agents: list[str] | None = None,
    ):
        """记忆任务执行结果（供后续参考）"""
        importance = MemoryImportance.HIGH if success else MemoryImportance.CRITICAL
        content = f"任务：{task}\n结果：{outcome}\n执行Agent：{agent_id}\n状态：{'成功' if success else '失败'}"
        
        entry_id = self._memory.memorize(
            content=content,
            agent_id=agent_id,
            scope=MemoryScope.SHARED,
            memory_type=MemoryType.EPISODE,
            importance=importance,
            tags=["task_outcome", "success" if success else "failed", agent_id],
            related_agent_ids=related_agents or [],
            summary=f"{'✓' if success else '✗'} {task[:50]}",
        )
        
        logger.info(f"Task outcome memorized: [{agent_id}] {task[:30]} → {success}")
        return entry_id
    
    def memorize_decision(
        self,
        decision: str,
        reason: str,
        agent_id: str,
        session_id: str | None = None,
    ):
        """记忆关键决策"""
        content = f"决策：{decision}\n原因：{reason}"
        
        return self._memory.memorize(
            content=content,
            agent_id=agent_id,
            scope=MemoryScope.SHARED,
            memory_type=MemoryType.PROCEDURE,
            importance=MemoryImportance.HIGH,
            tags=["decision", agent_id],
            summary=decision[:80],
            session_id=session_id,
        )
    
    def memorize_learning(
        self,
        learning: str,
        agent_id: str,
        category: str = "general",
    ):
        """
        记忆经验教训（自动提升为全局知识）
        
        使用场景：
        - 从失败中学习：某个策略失效
        - 从成功中提炼：某个方法特别有效
        """
        return self._memory.memorize(
            content=learning,
            agent_id=agent_id,
            scope=MemoryScope.SHARED,
            memory_type=MemoryType.PROCEDURE,
            importance=MemoryImportance.HIGH,
            tags=["learning", category, agent_id],
            ttl_seconds=365 * 86400,  # 永久保留
            summary=learning[:80],
        )
    
    def get_task_history(
        self,
        task_keywords: str = "",
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """查询历史任务执行情况"""
        result = self._memory.recall(
            agent_id="orchestrator",
            query_text=task_keywords,
            scope="shared",
            tags=["task_outcome"],
            limit=limit,
        )
        return [e.to_dict() for e in result.entries]


# =============================================================================
# Agent 记忆胶水（为每个专业 Agent 提供即插即用的记忆能力）
# =============================================================================

class AgentMemoryGlue:
    """
    Agent 记忆胶水 - 为专业 Agent 提供即插即用的记忆装饰器
    
    使用方式：
    
        memory = AgentMemoryGlue(agent_id="inventory")
        
        @memory.memorize_outcome
        def process_task(task_result):
            ...
            return {"status": "success", "data": result}
    
    或者在 Agent 类中组合使用：
    
        class InventoryAgent(AgentMemoryGlue):
            def __init__(self):
                super().__init__("inventory")
    """
    
    def __init__(self, agent_id: str, db_path: str | None = None):
        self.agent_id = agent_id
        self._memory = get_memory_router(db_path=db_path)
        self._private = self._memory.get_private(agent_id)
    
    # -------------------------------------------------------------------------
    # 装饰器
    # -------------------------------------------------------------------------
    
    def memorize_outcome(self, func):
        """
        装饰器：自动记忆任务执行结果
        
        用法：
            @memory.memorize_outcome
            def query_inventory(sku):
                return db.query(sku)
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            task_name = func.__name__
            success = isinstance(result, dict) and result.get("status") != "failed"
            outcome = str(result)[:200]
            
            self.remember_task(
                task_name=task_name,
                outcome=outcome,
                success=success,
                params=str(args)[:100],
            )
            
            return result
        
        wrapper.__name__ = func.__name__
        return wrapper
    
    # -------------------------------------------------------------------------
    # 快捷方法
    # -------------------------------------------------------------------------
    
    def remember_preference(
        self,
        key: str,
        value: str,
        importance: MemoryImportance = MemoryImportance.HIGH,
    ):
        """记忆偏好设置"""
        return self._private.memorize_preference(
            content=f"{key}: {value}",
            importance=importance,
        )
    
    def recall_preferences(self) -> list:
        """召回所有偏好"""
        return self._private.recall_preferences()
    
    def remember_knowledge(
        self,
        content: str,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        tags: list[str] | None = None,
    ):
        """记忆知识"""
        return self._private.memorize_knowledge(
            content=content,
            importance=importance,
            tags=tags,
        )
    
    def recall_knowledge(self, query: str = "") -> list:
        """召回知识"""
        return self._private.recall_knowledge(query=query)
    
    def remember_rule(
        self,
        rule: str,
        reason: str = "",
    ):
        """提炼并记忆规则"""
        return self._private.memorize_rule(rule=rule, reason=reason)
    
    def recall_rules(self) -> list:
        """召回提炼的规则"""
        return self._private.recall_rules()
    
    def remember_task(
        self,
        task_name: str,
        outcome: str,
        success: bool,
        params: str = "",
    ):
        """记忆任务执行"""
        importance = MemoryImportance.HIGH if success else MemoryImportance.CRITICAL
        content = f"[{task_name}]\n参数：{params}\n结果：{outcome}"
        self._private.memorize(
            content=content,
            memory_type=MemoryType.EPISODE,
            importance=importance,
            tags=["task", task_name],
            summary=f"{'✓' if success else '✗'} {task_name}",
        )
    
    def remember_context(
        self,
        task_id: str,
        context: str,
        stage: str = "in_progress",
    ):
        """记忆任务上下文"""
        return self._private.memorize_task_context(
            task_id=task_id,
            context=context,
            stage=stage,
        )
    
    def recall_context(self, task_id: str) -> list:
        """召回任务上下文"""
        return self._private.recall_task_context(task_id=task_id)
    
    def recall(self, query_text: str = "", limit: int = 20) -> list:
        """通用召回"""
        result = self._private.recall(query_text=query_text, limit=limit)
        return result.entries
    
    def forget(self, entry_id: str) -> bool:
        """遗忘"""
        return self._private.forget(entry_id)
    
    def build_context(self, task_description: str = "") -> str:
        """构建任务相关上下文"""
        return self._private.build_context_for_task(task_description)
    
    # -------------------------------------------------------------------------
    # 跨Agent协同
    # -------------------------------------------------------------------------
    
    def share_with(
        self,
        content: str,
        target_agent_ids: list[str],
        reason: str = "",
        session_id: str | None = None,
    ):
        """与其他Agent共享知识"""
        return self._memory.sync_across_agents(
            content=content,
            from_agent_id=self.agent_id,
            to_agent_ids=target_agent_ids,
            reason=reason,
            session_id=session_id,
        )
    
    def publish_to_pool(
        self,
        content: str,
        pool_type: str = "knowledge",
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        summary: str = "",
    ) -> str:
        """发布到共享知识池"""
        if pool_type == "fact":
            return self._memory.shared.publish_fact(
                content=content,
                author_agent_id=self.agent_id,
                importance=importance,
                summary=summary,
            )
        elif pool_type == "rule":
            return self._memory.shared.publish_rule(
                content=content,
                author_agent_id=self.agent_id,
                importance=importance,
            )
        else:
            return self._memory.shared.publish_knowledge(
                content=content,
                author_agent_id=self.agent_id,
                importance=importance,
                summary=summary,
            )


# =============================================================================
# 会话恢复集成
# =============================================================================

class SessionRecovery:
    """
    会话恢复胶水 - 断点续传时恢复Agent上下文
    
    使用场景：
    - Agent 崩溃重启 → 恢复私有记忆和任务状态
    - 用户重新开始对话 → 加载相关历史上下文
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._memory = get_memory_router()
        self._private = self._memory.get_private(agent_id)
    
    def save_checkpoint(
        self,
        session_id: str,
        task_state: dict[str, Any],
        current_task: str,
        stage: str = "in_progress",
    ) -> str:
        """保存会话检查点"""
        import json
        content = json.dumps(task_state, ensure_ascii=False, indent=2)
        
        entry_id = self._memory.memorize(
            content=content,
            agent_id=self.agent_id,
            scope=MemoryScope.SESSION,
            memory_type=MemoryType.CONTEXT,
            importance=MemoryImportance.HIGH,
            tags=["checkpoint", session_id, stage],
            ttl_seconds=86400.0 * 7,  # 7天
            summary=f"检查点: {current_task[:50]}",
            session_id=session_id,
        )
        
        logger.info(f"Checkpoint saved: session={session_id}, task={current_task[:30]}")
        return entry_id
    
    def load_checkpoint(
        self,
        session_id: str,
    ) -> dict[str, Any] | None:
        """加载会话检查点"""
        # 直接查询 SESSION scope（检查点存在 SESSION scope）
        q = MemoryQuery(
            tags=["checkpoint", session_id],
            scope=MemoryScope.SESSION,
            caller_agent_id=self.agent_id,
            min_importance=MemoryImportance.HIGH,
            limit=5,
        )
        entries = self._memory._store.query(q).entries
        
        # 找最新且有 checkpoint 标签的
        for e in sorted(entries, key=lambda x: x.created_at, reverse=True):
            if "checkpoint" in e.tags and session_id in e.tags:
                import json
                try:
                    return json.loads(e.content)
                except json.JSONDecodeError:
                    return {"content": e.content}
        
        return None
    
    def recover_session(
        self,
        session_id: str,
        requester_agent_id: str,
    ) -> dict[str, Any]:
        """完整会话恢复"""
        return self._memory.session.recover_session(session_id, requester_agent_id)
    
    def get_agent_recent_history(self, limit: int = 20) -> list[dict[str, Any]]:
        """获取Agent近期历史（用于恢复时参考）"""
        entries = self._memory._store.get_recent(
            limit=limit,
            scope=MemoryScope.PRIVATE,
            agent_id=self.agent_id,
        )
        return [e.to_dict() for e in entries]


# =============================================================================
# 协同记忆集成
# =============================================================================

class CollaborationMemory:
    """
    协同记忆助手 - 帮助多个Agent协同时管理共享记忆
    
    使用场景：
    - 多Agent并行执行子任务 → 共享中间结果
    - 采购+财务协作 → 共享成本分析
    - 跨团队知识同步 → 定时推送更新
    """
    
    def __init__(self, primary_agent_id: str):
        self.primary_agent_id = primary_agent_id
        self._memory = get_memory_router()
    
    def start_collaboration(
        self,
        task_id: str,
        participants: list[str],
        title: str = "",
    ) -> str:
        """启动协作会话"""
        session = self._memory.session.create_session(
            task_id=task_id,
            root_agent_id=self.primary_agent_id,
            title=title,
            participants=participants,
        )
        
        # 自动发布协作启动公告
        self._memory.memorize(
            content=f"协作开始：{title}\n参与者：{', '.join(participants)}",
            agent_id=self.primary_agent_id,
            scope=MemoryScope.SHARED,
            memory_type=MemoryType.EPISODE,
            importance=MemoryImportance.HIGH,
            tags=["collaboration_start", task_id] + participants,
            session_id=session.session_id,
            summary=f"协作启动: {title[:50]}",
        )
        
        return session.session_id
    
    def share_intermediate_result(
        self,
        session_id: str,
        agent_id: str,
        result: str,
        next_agent_id: str,
    ):
        """共享中间结果给下游Agent"""
        return self._memory.session.store_session_knowledge(
            session_id=session_id,
            agent_id=agent_id,
            content=f"[{agent_id} → {next_agent_id}]\n{result}",
            knowledge_type="intermediate_result",
            importance=MemoryImportance.HIGH,
        )
    
    def record_collaboration_decision(
        self,
        session_id: str,
        decision: str,
        decided_by: str,
        participants: list[str],
    ):
        """记录协作决策"""
        entry_id = self._memory.session.broadcast_decision(
            session_id=session_id,
            agent_id=decided_by,
            decision=decision,
            reason=f"由 {decided_by} 决定，参与者: {', '.join(participants)}",
        )
        
        # 提炼为全局规则候选
        self._memory.memorize(
            content=f"[协作规则候选]\n{decision}",
            agent_id=decided_by,
            scope=MemoryScope.SHARED,
            memory_type=MemoryType.PROCEDURE,
            importance=MemoryImportance.MEDIUM,
            tags=["rule_candidate", "collaboration", decided_by],
            summary=decision[:60],
        )
        
        return entry_id
    
    def get_collaboration_history(
        self,
        session_id: str,
        agent_id: str,
    ) -> dict[str, Any]:
        """获取协作历史"""
        return self._memory.session.recover_session(session_id, agent_id)
