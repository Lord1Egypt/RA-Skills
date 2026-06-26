"""
memory_api.py - 记忆层 REST API

提供 FastAPI 风格的 HTTP 接口，供 Agent 系统调用。
"""

from __future__ import annotations

import logging
from typing import Any

from .memory_core import MemoryImportance, MemoryScope, MemoryType
from .memory_router import MemoryRouter

logger = logging.getLogger(__name__)


# =============================================================================
# FastAPI App（可选，按需启用）
# =============================================================================

def create_api(router: MemoryRouter | None = None) -> Any:
    """
    创建记忆层 API（FastAPI App）
    
    使用方式：
        from agent_cluster.memory.api import create_api
        app = create_api(memory_router)
        # uvicorn.run(app, host="0.0.0.0", port=8081)
    """
    try:
        from fastapi import FastAPI, HTTPException, Query
        from pydantic import BaseModel
    except ImportError:
        logger.warning("FastAPI not installed. API not available.")
        return None
    
    app = FastAPI(title="M-A3 Memory Layer API", version="1.0.0")
    mr = router or MemoryRouter()
    
    # -------------------------------------------------------------------------
    # 请求模型
    # -------------------------------------------------------------------------
    
    class MemorizeRequest(BaseModel):
        content: str
        agent_id: str
        scope: str = "auto"
        memory_type: str = "episode"
        importance: int = 3
        tags: list[str] | None = None
        ttl_seconds: float = 86400.0
        summary: str = ""
        related_agent_ids: list[str] | None = None
        session_id: str | None = None
    
    class RecallRequest(BaseModel):
        agent_id: str
        query_text: str = ""
        scope: str = "all"
        memory_type: str | None = None
        tags: list[str] | None = None
        session_id: str | None = None
        limit: int = 20
    
    class LinkRequest(BaseModel):
        content: str
        agent_id: str
        related_agent_ids: list[str]
        scope: str = "shared"
        memory_type: str = "fact"
    
    class SyncRequest(BaseModel):
        content: str
        from_agent_id: str
        to_agent_ids: list[str]
        reason: str = ""
        session_id: str | None = None
    
    class SessionCreateRequest(BaseModel):
        task_id: str
        root_agent_id: str
        title: str = ""
        participants: list[str] | None = None
        metadata: dict[str, Any] | None = None
    
    # -------------------------------------------------------------------------
    # 写入接口
    # -------------------------------------------------------------------------
    
    @app.post("/memory/memorize", summary="存储记忆")
    async def memorize(req: MemorizeRequest) -> dict[str, Any]:
        try:
            entry_id = mr.memorize(
                content=req.content,
                agent_id=req.agent_id,
                scope=req.scope,
                memory_type=req.memory_type,
                importance=MemoryImportance(req.importance),
                tags=req.tags,
                ttl_seconds=req.ttl_seconds,
                summary=req.summary,
                related_agent_ids=req.related_agent_ids,
                session_id=req.session_id,
            )
            return {"success": True, "entry_id": entry_id}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"memorize error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/memory/link", summary="存储并建立关联")
    async def memorize_and_link(req: LinkRequest) -> dict[str, Any]:
        entry_id = mr.memorize_and_link(
            content=req.content,
            agent_id=req.agent_id,
            related_agent_ids=req.related_agent_ids,
            scope=MemoryScope(req.scope),
            memory_type=MemoryType(req.memory_type),
        )
        return {"success": True, "entry_id": entry_id}
    
    # -------------------------------------------------------------------------
    # 读取接口
    # -------------------------------------------------------------------------
    
    @app.post("/memory/recall", summary="查询记忆")
    async def recall(req: RecallRequest) -> dict[str, Any]:
        result = mr.recall(
            agent_id=req.agent_id,
            query_text=req.query_text,
            scope=req.scope,
            memory_type=req.memory_type,
            tags=req.tags,
            session_id=req.session_id,
            limit=req.limit,
        )
        return result.to_dict()
    
    @app.get("/memory/{entry_id}", summary="获取单条记忆")
    async def get_entry(entry_id: str) -> dict[str, Any]:
        entry = mr._store.get(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry.to_dict()
    
    # -------------------------------------------------------------------------
    # 共享知识池接口
    # -------------------------------------------------------------------------
    
    @app.post("/knowledge/publish", summary="发布共享知识")
    async def publish_knowledge(req: MemorizeRequest) -> dict[str, Any]:
        entry_id = mr.shared.publish_knowledge(
            content=req.content,
            author_agent_id=req.agent_id,
            category=req.tags[0] if req.tags else "general",
            importance=MemoryImportance(req.importance),
            tags=req.tags,
            summary=req.summary,
        )
        return {"success": True, "entry_id": entry_id}
    
    @app.get("/knowledge/query", summary="查询共享知识")
    async def query_knowledge(
        q: str = Query(""),
        agent_id: str = Query(""),
        limit: int = Query(20),
    ) -> dict[str, Any]:
        result = mr.shared.query_knowledge(
            query_text=q,
            caller_agent_id=agent_id,
            limit=limit,
        )
        return result.to_dict()
    
    @app.get("/knowledge/artifacts", summary="获取协作成果")
    async def get_artifacts(
        agent_id: str = Query(""),
        related_agent: str = Query(""),
        limit: int = Query(10),
    ) -> dict[str, Any]:
        artifacts = mr.shared.get_artifacts(
            caller_agent_id=agent_id,
            related_agent_id=related_agent,
            limit=limit,
        )
        return {
            "artifacts": [a.to_dict() for a in artifacts],
            "total": len(artifacts),
        }
    
    # -------------------------------------------------------------------------
    # 会话接口
    # -------------------------------------------------------------------------
    
    @app.post("/session/create", summary="创建会话")
    async def create_session(req: SessionCreateRequest) -> dict[str, Any]:
        session = mr.session.create_session(
            task_id=req.task_id,
            root_agent_id=req.root_agent_id,
            title=req.title,
            participants=req.participants,
            metadata=req.metadata,
        )
        return session.to_dict()
    
    @app.get("/session/{session_id}", summary="获取会话")
    async def get_session(session_id: str) -> dict[str, Any]:
        session = mr.session._get_session(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return session.to_dict()
    
    @app.post("/session/{session_id}/recover", summary="恢复会话")
    async def recover_session(
        session_id: str,
        agent_id: str = Query(""),
    ) -> dict[str, Any]:
        return mr.session.recover_session(session_id, agent_id)
    
    @app.post("/session/{session_id}/broadcast", summary="广播决策")
    async def broadcast_decision(
        session_id: str,
        agent_id: str = Query(""),
        decision: str = Query(""),
        reason: str = Query(""),
    ) -> dict[str, Any]:
        entry_id = mr.session.broadcast_decision(
            session_id=session_id,
            agent_id=agent_id,
            decision=decision,
            reason=reason,
        )
        return {"success": True, "entry_id": entry_id}
    
    @app.get("/session/{session_id}/events", summary="获取会话事件流")
    async def get_events(
        session_id: str,
        event_type: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        events = mr.session.get_events(
            session_id=session_id,
            event_type=event_type,
            limit=limit,
        )
        return {
            "events": [e.to_dict() for e in events],
            "total": len(events),
        }
    
    # -------------------------------------------------------------------------
    # 高级接口
    # -------------------------------------------------------------------------
    
    @app.post("/sync", summary="跨Agent同步")
    async def sync_across_agents(req: SyncRequest) -> dict[str, Any]:
        result = mr.sync_across_agents(
            content=req.content,
            from_agent_id=req.from_agent_id,
            to_agent_ids=req.to_agent_ids,
            reason=req.reason,
            session_id=req.session_id,
        )
        return {"success": True, "results": result}
    
    @app.get("/context/{agent_id}", summary="构建Agent上下文")
    async def build_context(
        agent_id: str,
        task: str = Query(""),
    ) -> dict[str, str]:
        context = mr.build_agent_context(
            agent_id=agent_id,
            task_query=task,
        )
        return {"context": context}
    
    # -------------------------------------------------------------------------
    # 管理接口
    # -------------------------------------------------------------------------
    
    @app.get("/stats", summary="全系统统计")
    async def get_stats() -> dict[str, Any]:
        return mr.get_system_stats()
    
    @app.post("/prune", summary="清理过期记忆")
    async def prune() -> dict[str, int]:
        count = mr.prune_all()
        return {"pruned": count}
    
    @app.get("/tags/hot", summary="热门标签")
    async def get_hot_tags(top_n: int = 20) -> dict[str, Any]:
        tags = mr.index.get_hot_tags(top_n=top_n)
        return {"hot_tags": [{"tag": t, "count": c} for t, c in tags]}
    
    @app.get("/health", summary="健康检查")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "memory-layer"}
    
    return app
