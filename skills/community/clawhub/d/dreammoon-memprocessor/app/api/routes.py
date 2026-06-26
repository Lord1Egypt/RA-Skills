"""FastAPI路由"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.models import (
    AnalyzeRequest, AnalyzeResponse, GetMemoryResponse,
    SearchRequest, SearchResponse, SetMemoryRequest,
    SetMemoryResponse, StorageStats
)
from app.services.event_detector import get_event_detector
from app.services.memory_service import MemoryService, get_memory_service

router = APIRouter(prefix="/api/v1", tags=["memory"])


@router.post("/memory", response_model=SetMemoryResponse)
async def set_memory(
    request: SetMemoryRequest,
    service: MemoryService = Depends(get_memory_service)
):
    """存储记忆"""
    try:
        return await service.set(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory/{key}", response_model=GetMemoryResponse)
async def get_memory(
    key: str,
    service: MemoryService = Depends(get_memory_service)
):
    """获取记忆"""
    try:
        return await service.get(key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memory/{key}")
async def delete_memory(
    key: str,
    service: MemoryService = Depends(get_memory_service)
):
    """删除记忆"""
    # TODO: 实现删除逻辑
    return {"success": True, "key": key}


@router.post("/search", response_model=SearchResponse)
async def search_memory(
    request: SearchRequest,
    service: MemoryService = Depends(get_memory_service)
):
    """搜索记忆"""
    try:
        return await service.search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_memory_get(
    q: str = Query(..., description="搜索关键词"),
    top_k: int = Query(default=5, ge=1, le=50),
    min_similarity: float = Query(default=0.5, ge=0.0, le=1.0),
    service: MemoryService = Depends(get_memory_service)
):
    """搜索记忆 (GET方式)"""
    request = SearchRequest(
        query=q,
        top_k=top_k,
        min_similarity=min_similarity
    )
    return await service.search(request)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_content(request: AnalyzeRequest):
    """分析内容重要性"""
    detector = get_event_detector()
    
    importance, events, is_sensitive = detector.analyze(
        request.content,
        request.context
    )
    
    # 决定建议层级
    from app.config import settings
    from app.models import MemoryLevel
    
    if importance >= settings.IMPORTANCE_IMMEDIATE:
        suggested_level = MemoryLevel.L3_COLD
    elif importance >= settings.IMPORTANCE_DAILY:
        suggested_level = MemoryLevel.L2_WARM
    else:
        suggested_level = MemoryLevel.L1_HOT
    
    return AnalyzeResponse(
        importance=importance,
        events=events,
        is_sensitive=is_sensitive,
        should_persist=importance >= settings.IMPORTANCE_DAILY and not is_sensitive,
        suggested_level=suggested_level
    )


@router.get("/stats", response_model=StorageStats)
async def get_stats(
    service: MemoryService = Depends(get_memory_service)
):
    """获取存储统计"""
    return await service.get_stats()


@router.post("/tasks/daily")
async def run_daily_persistence(
    service: MemoryService = Depends(get_memory_service)
):
    """手动触发每日沉淀任务"""
    await service.run_daily_persistence()
    return {"success": True, "task": "daily_persistence"}


@router.post("/tasks/weekly")
async def run_weekly_archive(
    service: MemoryService = Depends(get_memory_service)
):
    """手动触发每周归档任务"""
    await service.run_weekly_archive()
    return {"success": True, "task": "weekly_archive"}
