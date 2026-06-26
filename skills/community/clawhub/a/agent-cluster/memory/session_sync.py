"""
session_sync.py - 会话记忆同步

支持同一会话内多个 Agent 的记忆同步，实现：
- 会话上下文自动同步
- 跨 Agent 任务状态广播
- 会话快照保存与恢复
- 会话级临时知识池
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

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


# =============================================================================
# 会话数据模型
# =============================================================================

@dataclass
class SessionContext:
    """会话上下文"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    title: str = ""
    
    # 参与者
    participants: list[str] = field(default_factory=list)  # Agent ID 列表
    
    # 时间
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_active: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # 状态
    status: str = "active"  # active | completed | aborted
    root_agent_id: str = ""  # 发起会话的Agent
    
    # 会话元信息
    metadata: dict[str, Any] = field(default_factory=dict)
    
    # 摘要（自动生成）
    summary: str = ""
    
    def touch(self):
        self.last_active = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "task_id": self.task_id,
            "title": self.title,
            "participants": self.participants,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "status": self.status,
            "root_agent_id": self.root_agent_id,
            "metadata": self.metadata,
            "summary": self.summary,
        }


@dataclass
class SessionEvent:
    """会话事件"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    agent_id: str = ""
    event_type: str = ""   # message | decision | task_start | task_complete | context_share
    content: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    related_entry_ids: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "event_type": self.event_type,
            "content": self.content,
            "timestamp": self.timestamp,
            "related_entry_ids": self.related_entry_ids,
            "tags": self.tags,
        }


# =============================================================================
# 会话同步器
# =============================================================================

class SessionSync:
    """
    会话记忆同步器
    
    功能：
    1. 会话生命周期管理（创建/保存/恢复）
    2. 事件流记录（跨Agent消息、决策、状态变更）
    3. 上下文广播（让所有参与者感知会话状态）
    4. 会话级临时知识池（Session Scope 记忆）
    5. 会话快照（自动摘要 + 手动关键节点快照）
    """
    
    def __init__(
        self,
        store: Optional[PersistentStore] = None,
        db_path: str | None = None,
    ):
        self.store = store or PersistentStore(db_path=db_path or str(self._default_db()))
        self._sessions: dict[str, SessionContext] = {}  # 内存缓存
        self._event_log_path = str(self._default_db().parent / "session_events.jsonl")
        self._init_event_log()
    
    @staticmethod
    def _default_db() -> Any:
        from pathlib import Path
        return Path(__file__).parent.parent / "data" / "memory" / "sessions.db"
    
    def _init_event_log(self):
        """初始化事件日志"""
        Path(self._event_log_path).parent.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # 会话生命周期管理
    # -------------------------------------------------------------------------
    
    def create_session(
        self,
        task_id: str,
        root_agent_id: str,
        title: str = "",
        participants: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SessionContext:
        """创建新会话"""
        session = SessionContext(
            task_id=task_id,
            title=title or f"Task-{task_id}",
            participants=participants or [root_agent_id],
            root_agent_id=root_agent_id,
            metadata=metadata or {},
        )
        
        # 持久化到 store
        entry = MemoryEntry(
            content=json.dumps(session.to_dict(), ensure_ascii=False),
            memory_type=MemoryType.CONTEXT,
            scope=MemoryScope.SESSION,
            importance=MemoryImportance.MEDIUM,
            agent_id=root_agent_id,
            tags=["session", "meta", task_id],
            ttl_seconds=86400.0,  # 1天
            summary=f"会话: {session.title}",
            source="system",
        )
        entry_id = self.store.store(entry)
        session.metadata["entry_id"] = entry_id
        
        self._sessions[session.session_id] = session
        self.log_event(session.session_id, root_agent_id, "session_create", f"创建会话: {title}")
        
        logger.info(f"Session created: {session.session_id} by {root_agent_id}")
        return session
    
    def join_session(self, session_id: str, agent_id: str) -> bool:
        """Agent 加入会话"""
        session = self._get_session(session_id)
        if session is None:
            return False
        if agent_id not in session.participants:
            session.participants.append(agent_id)
            self._sync_session(session)
            self.log_event(session_id, agent_id, "agent_join", f"Agent {agent_id} 加入会话")
        return True
    
    def complete_session(self, session_id: str, summary: str = "") -> bool:
        """完成会话"""
        session = self._get_session(session_id)
        if session is None:
            return False
        
        session.status = "completed"
        session.summary = summary or self._auto_summary(session_id)
        self._sync_session(session)
        
        # 将会话事件归档
        self._archive_session_events(session_id)
        
        self.log_event(session_id, "system", "session_complete", session.summary)
        logger.info(f"Session completed: {session_id}")
        return True
    
    def _get_session(self, session_id: str) -> Optional[SessionContext]:
        """从缓存或存储获取会话"""
        if session_id in self._sessions:
            return self._sessions[session_id]
        
        # 从存储恢复
        q = MemoryQuery(
            tags=["session", "meta"],
            scope=MemoryScope.SESSION,
            limit=1,
        )
        # 简单恢复逻辑（实际需要按 session_id 查询）
        with get_cursor(self.store.db_path) as cur:
            cur.execute("""
                SELECT * FROM memory_entries
                WHERE scope='session' AND is_deleted=0
                AND content LIKE ?
                ORDER BY created_at DESC LIMIT 10
            """, (f'%{session_id}%',))
            
            for row in cur.fetchall():
                data = json.loads(row["content"])
                if data.get("session_id") == session_id:
                    session = SessionContext(**{k: v for k, v in data.items() if k in SessionContext.__dataclass_fields__})
                    self._sessions[session_id] = session
                    return session
        return None
    
    def _sync_session(self, session: SessionContext):
        """同步会话到存储"""
        session.touch()
        entry_id = session.metadata.get("entry_id", "")
        if entry_id:
            self.store.update(entry_id, content=json.dumps(session.to_dict(), ensure_ascii=False))
    
    # -------------------------------------------------------------------------
    # 事件流
    # -------------------------------------------------------------------------
    
    def log_event(
        self,
        session_id: str,
        agent_id: str,
        event_type: str,
        content: str,
        related_entry_ids: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """记录会话事件"""
        event = SessionEvent(
            session_id=session_id,
            agent_id=agent_id,
            event_type=event_type,
            content=content,
            related_entry_ids=related_entry_ids or [],
            tags=tags or [],
        )
        
        # 追加到事件日志（JSONL 格式）
        with open(self._event_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        
        # 同时存储为 Session Scope 记忆
        entry = MemoryEntry(
            content=json.dumps(event.to_dict(), ensure_ascii=False),
            memory_type=MemoryType.EPISODE,
            scope=MemoryScope.SESSION,
            importance=MemoryImportance.MEDIUM if event_type in ("decision", "task_complete") else MemoryImportance.LOW,
            agent_id=agent_id,
            tags=["event", event_type, session_id] + (tags or []),
            related_entry_ids=related_entry_ids or [],
            ttl_seconds=86400.0,
            summary=f"[{event_type}] {content[:60]}",
            source="system",
        )
        entry_id = self.store.store(entry)
        
        # 更新会话活跃时间
        session = self._get_session(session_id)
        if session:
            session.touch()
        
        return event.event_id
    
    def get_events(
        self,
        session_id: str,
        event_type: str | None = None,
        agent_id: str | None = None,
        limit: int = 50,
    ) -> list[SessionEvent]:
        """获取会话事件流"""
        # 从事件日志读取
        events = []
        try:
            with open(self._event_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    event_data = json.loads(line)
                    if event_data.get("session_id") != session_id:
                        continue
                    if event_type and event_data.get("event_type") != event_type:
                        continue
                    if agent_id and event_data.get("agent_id") != agent_id:
                        continue
                    events.append(SessionEvent(**event_data))
        except FileNotFoundError:
            pass
        
        events.sort(key=lambda e: e.timestamp, reverse=True)
        return events[:limit]
    
    def _archive_session_events(self, session_id: str):
        """归档会话事件（压缩到会话摘要）"""
        events = self.get_events(session_id, limit=500)
        if not events:
            return
        
        # 生成归档摘要
        event_summary = {
            "total_events": len(events),
            "participants": list(set(e.agent_id for e in events)),
            "event_types": list(set(e.event_type for e in events)),
            "first_event": events[-1].timestamp,
            "last_event": events[0].timestamp,
        }
        
        # 存储为永久会话归档
        entry = MemoryEntry(
            content=json.dumps(event_summary, ensure_ascii=False),
            memory_type=MemoryType.EPISODE,
            scope=MemoryScope.SHARED,
            importance=MemoryImportance.MEDIUM,
            agent_id="system",
            tags=["session_archive", session_id],
            ttl_seconds=365 * 86400,
            summary=f"会话归档: {len(events)}个事件",
            source="system",
        )
        self.store.store(entry)
    
    # -------------------------------------------------------------------------
    # 会话级临时知识池
    # -------------------------------------------------------------------------
    
    def store_session_knowledge(
        self,
        session_id: str,
        agent_id: str,
        content: str,
        knowledge_type: str = "context",
        importance: MemoryImportance = MemoryImportance.MEDIUM,
    ) -> str:
        """
        存储会话级临时知识（仅会话参与者可见，会话结束后过期）
        
        使用场景：
        - 跨Agent中间结果共享
        - 任务分步状态的临时记录
        - 会话内决策备忘
        """
        entry = MemoryEntry(
            content=content,
            memory_type=MemoryType.CONTEXT,
            scope=MemoryScope.SESSION,
            importance=importance,
            agent_id=agent_id,
            tags=["session_knowledge", session_id, knowledge_type],
            ttl_seconds=86400.0,  # 会话结束后1天过期
            summary=content[:80],
            source="agent",
        )
        entry_id = self.store.store(entry)
        
        # 广播事件
        self.log_event(
            session_id, agent_id, "context_share",
            f"共享: {content[:60]}",
            related_entry_ids=[entry_id],
        )
        return entry_id
    
    def get_session_context(
        self,
        session_id: str,
        caller_agent_id: str,
        query: str = "",
    ) -> MemoryResult:
        """获取会话上下文（供任意参与者查询）"""
        q = MemoryQuery(
            query_text=query,
            tags=[session_id],
            scope=MemoryScope.SESSION,
            caller_agent_id=caller_agent_id,
            min_importance=MemoryImportance.LOW,
            limit=30,
        )
        return self.store.query(q)
    
    def broadcast_decision(
        self,
        session_id: str,
        agent_id: str,
        decision: str,
        reason: str = "",
    ) -> str:
        """
        广播决策（特殊事件类型，会自动同步给所有参与者）
        
        决策会被标记为高优先级，且会被自动提炼为全局规则候选
        """
        content = decision
        if reason:
            content = f"{decision}\n\n原因：{reason}"
        
        entry_id = self.store_session_knowledge(
            session_id=session_id,
            agent_id=agent_id,
            content=content,
            knowledge_type="decision",
            importance=MemoryImportance.HIGH,
        )
        
        self.log_event(
            session_id, agent_id, "decision",
            decision[:100],
            related_entry_ids=[entry_id],
            tags=["decision"],
        )
        
        # 标记为规则候选（供后续评审）
        self._propose_as_rule_candidate(session_id, decision, agent_id)
        
        return entry_id
    
    def _propose_as_rule_candidate(self, session_id: str, decision: str, agent_id: str):
        """将重要决策提议为全局规则候选"""
        entry = MemoryEntry(
            content=f"[规则候选 - 来自会话 {session_id}]\n{decision}",
            memory_type=MemoryType.PROCEDURE,
            scope=MemoryScope.SHARED,
            importance=MemoryImportance.HIGH,
            agent_id=agent_id,
            tags=["rule_candidate", "pending_review", session_id],
            ttl_seconds=7 * 86400,  # 7天评审期
            summary=f"规则候选: {decision[:60]}",
            source="agent",
        )
        self.store.store(entry)
    
    # -------------------------------------------------------------------------
    # 会话恢复
    # -------------------------------------------------------------------------
    
    def recover_session(
        self,
        session_id: str,
        requester_agent_id: str,
    ) -> dict[str, Any]:
        """
        恢复会话完整上下文
        
        返回：
        - session: 会话元信息
        - events: 事件流
        - shared_knowledge: 共享知识
        - decisions: 决策列表
        """
        session = self._get_session(session_id)
        if session is None:
            return {"error": "Session not found"}
        
        # 检查参与者权限
        if requester_agent_id not in session.participants and requester_agent_id != "orchestrator":
            return {"error": "Unauthorized"}
        
        events = self.get_events(session_id, limit=100)
        context_result = self.get_session_context(session_id, requester_agent_id)
        
        return {
            "session": session.to_dict(),
            "events": [e.to_dict() for e in events],
            "shared_knowledge": [e.to_dict() for e in context_result.entries],
            "decisions": [
                e.to_dict() for e in events
                if e.event_type == "decision"
            ],
            "participants": session.participants,
        }
    
    # -------------------------------------------------------------------------
    # 辅助方法
    # -------------------------------------------------------------------------
    
    def _auto_summary(self, session_id: str) -> str:
        """自动生成会话摘要"""
        events = self.get_events(session_id, limit=50)
        if not events:
            return "会话完成（无事件记录）"
        
        decision_count = sum(1 for e in events if e.event_type == "decision")
        task_completes = sum(1 for e in events if e.event_type == "task_complete")
        participants = list(set(e.agent_id for e in events))
        
        return f"会话完成：{len(events)}个事件，{decision_count}个决策，{task_completes}个任务完成，{len(participants)}个参与者参与"
    
    def get_active_sessions(self, agent_id: str) -> list[SessionContext]:
        """获取某Agent参与的活动会话"""
        active = []
        for session in self._sessions.values():
            if session.status == "active" and agent_id in session.participants:
                active.append(session)
        return active
    
    def get_session_stats(self) -> dict[str, Any]:
        """获取会话统计"""
        active = len([s for s in self._sessions.values() if s.status == "active"])
        completed = len([s for s in self._sessions.values() if s.status == "completed"])
        return {
            "active_sessions": active,
            "completed_sessions": completed,
            "total_cached": len(self._sessions),
        }
