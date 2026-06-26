"""核心记忆服务"""
import time
from datetime import datetime
from typing import Dict, List, Optional

from app.config import settings
from app.core.l1_storage import get_l1_storage
from app.core.l2_storage import get_l2_storage
from app.core.l3_storage import get_l3_storage
from app.core.l4_storage import get_l4_storage
from app.models import (
    DailySummary, GetMemoryResponse, MemoryItem, MemoryLevel,
    SearchRequest, SearchResponse, SearchResult, SetMemoryRequest,
    SetMemoryResponse, StorageStats
)
from app.services.embedding import get_embedding_service
from app.services.event_detector import get_event_detector


class MemoryService:
    """核心记忆服务 - 管理L1-L4四层存储"""
    
    def __init__(self):
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.l4 = None
        self.embedder = None
        self.detector = None
    
    async def init(self):
        """初始化所有存储层"""
        print("[MemoryService] Initializing...")
        
        self.l1 = await get_l1_storage()
        self.l2 = await get_l2_storage()
        self.l3 = await get_l3_storage()
        self.l4 = await get_l4_storage()
        
        self.embedder = get_embedding_service()
        self.detector = get_event_detector()
        
        print("[MemoryService] All levels initialized")
    
    async def set(self, request: SetMemoryRequest) -> SetMemoryResponse:
        """
        存储记忆
        
        流程：
        1. 分析内容重要性
        2. 生成向量嵌入
        3. 根据重要性决定存储层级
        4. 异步沉淀到其他层级
        """
        start_time = time.time()
        
        # 分析内容
        context = {
            "reference_count": request.metadata.get("reference_count", 0),
            "task_active": request.metadata.get("task_active", True)
        }
        
        importance, events, is_sensitive = self.detector.analyze(
            request.content, context
        )
        
        # 如果提供了重要性，使用提供的值
        if request.importance is not None:
            importance = request.importance
        
        # 生成向量嵌入（用于L4）
        try:
            embedding = self.embedder.encode(request.content)
            # 修复：确保 embedding 是单层列表，不是嵌套列表
            if embedding and isinstance(embedding[0], list):
                embedding = embedding[0]
        except Exception as e:
            print(f"[Embedding] Error: {e}")
            embedding = None
        
        # 创建记忆项
        item = MemoryItem(
            key=request.key,
            content=request.content,
            importance=importance,
            metadata=request.metadata,
            tags=request.tags,
            embedding=embedding
        )
        
        # 存储到L1（总是）
        await self.l1.set(request.key, item)
        
        # 根据重要性决定后续处理
        persisted_level = MemoryLevel.L1_HOT
        
        if importance >= settings.IMPORTANCE_IMMEDIATE:
            # 立即沉淀到L3
            item.level = MemoryLevel.L3_COLD
            await self.l3.append_to_memory(item, section="decisions" if any(
                e.type.value == "decision" for e in events
            ) else "general")
            
            # 同时存储到L2用于查询
            await self.l2.set(item)
            
            # 添加到L4向量索引
            if embedding:
                await self.l4.add(item, embedding)
            
            persisted_level = MemoryLevel.L3_COLD
            
        elif importance >= settings.IMPORTANCE_DAILY:
            # 存储到L2，等待每日沉淀
            item.level = MemoryLevel.L2_WARM
            item.metadata["_queued_for_summary"] = True
            await self.l2.set(item)
            persisted_level = MemoryLevel.L2_WARM
        
        elapsed = (time.time() - start_time) * 1000
        print(f"[Set] {request.key} in {elapsed:.2f}ms, importance={importance}, level={persisted_level}")
        
        return SetMemoryResponse(
            success=True,
            item=item,
            persisted_level=persisted_level,
            importance_score=importance
        )
    
    async def get(self, key: str) -> GetMemoryResponse:
        """
        获取记忆
        
        流程：
        1. 先查L1
        2. 未命中则查L2
        3. 找到后提升到L1
        """
        # L1
        item = await self.l1.get(key)
        if item:
            item.access_count += 1
            item.last_accessed = datetime.utcnow()
            await self.l1.set(key, item)  # 更新访问统计
            return GetMemoryResponse(found=True, item=item, from_level=MemoryLevel.L1_HOT)
        
        # L2
        item = await self.l2.get(key)
        if item:
            # 提升到L1
            await self.l1.set(key, item)
            return GetMemoryResponse(found=True, item=item, from_level=MemoryLevel.L2_WARM)
        
        return GetMemoryResponse(found=False)
    
    async def search(self, request: SearchRequest) -> SearchResponse:
        """
        搜索记忆
        
        支持：
        1. 文本搜索（L1, L2, L3）
        2. 语义搜索（L4向量索引）
        """
        start_time = time.time()
        results: List[SearchResult] = []
        
        # 1. 向量语义搜索（L4）
        try:
            query_embedding = self.embedder.encode(request.query)
            vector_results = await self.l4.search(query_embedding, top_k=request.top_k)
            
            for r in vector_results:
                if r.similarity >= request.min_similarity:
                    results.append(r)
        except Exception as e:
            print(f"[Search] Vector search error: {e}")
        
        # 2. 文本搜索L1
        l1_keys = await self.l1.keys("*")
        for key in l1_keys[:50]:  # 限制数量
            if len(results) >= request.top_k:
                break
            
            item = await self.l1.get(key)
            if item and request.query.lower() in item.content.lower():
                results.append(SearchResult(
                    id=item.id,
                    key=item.key,
                    content=item.content[:200],
                    similarity=0.7,  # 文本匹配默认相似度
                    level=MemoryLevel.L1_HOT,
                    metadata=item.metadata,
                    created_at=item.created_at
                ))
        
        # 3. 文本搜索L3（最近的）
        if len(results) < request.top_k:
            l3_results = await self.l3.search_content(request.query, days=30)
            for r in l3_results:
                if len(results) >= request.top_k:
                    break
                
                results.append(SearchResult(
                    id=f"l3_{r['date']}",
                    key=r["date"],
                    content=r["preview"],
                    similarity=0.6,
                    level=MemoryLevel.L3_COLD,
                    metadata={"file": r["file"]},
                    created_at=datetime.strptime(r["date"], "%Y-%m-%d")
                ))
        
        # 按相似度排序
        results.sort(key=lambda x: x.similarity, reverse=True)
        results = results[:request.top_k]
        
        elapsed = (time.time() - start_time) * 1000
        
        return SearchResponse(
            query=request.query,
            total_results=len(results),
            results=results,
            search_time_ms=elapsed
        )
    
    async def run_daily_persistence(self):
        """运行每日沉淀任务"""
        print("[DailyPersistence] Starting...")
        
        # 1. 从L2获取待沉淀的记忆
        items = await self.l2.get_for_daily_summary()
        
        if not items:
            print("[DailyPersistence] No items to persist")
            return
        
        # 2. 生成每日摘要
        summary = DailySummary(
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            overview=f"今日共沉淀 {len(items)} 条记忆",
            activities=[],
            decisions=[],
            lessons=[]
        )
        
        for item in items:
            # 分类
            score = item.importance
            
            summary.activities.append({
                "time": item.created_at.strftime("%H:%M"),
                "description": item.key,
                "importance": score
            })
            
            if score >= 70:
                summary.decisions.append({
                    "topic": item.key,
                    "conclusion": item.content[:100],
                    "timestamp": item.created_at.isoformat()
                })
            elif any(t in ["lesson", "learned"] for t in item.tags):
                summary.lessons.append({
                    "content": item.content[:200]
                })
        
        # 3. 保存到L3
        await self.l3.save_daily_summary(summary)
        
        print(f"[DailyPersistence] Completed, {len(items)} items persisted")
    
    async def run_weekly_archive(self):
        """运行每周归档任务"""
        print("[WeeklyArchive] Starting...")
        await self.l4.archive_old_memories(days=settings.ARCHIVE_DAYS)
        print("[WeeklyArchive] Completed")
    
    async def get_stats(self) -> StorageStats:
        """获取存储统计"""
        l1_stats = await self.l1.stats()
        l2_stats = await self.l2.stats()
        l3_stats = await self.l3.stats()
        l4_stats = await self.l4.get_stats()
        
        total_mb = (
            l1_stats.get("size_bytes", 0) +
            l4_stats.get("index_size", 0)
        ) / 1024 / 1024
        
        return StorageStats(
            l1_entries=l1_stats.get("entries", 0),
            l1_size_bytes=l1_stats.get("size_bytes", 0),
            l2_entries=l2_stats.get("entries", 0),
            l3_files=l3_stats.get("total_files", 0),
            l4_vectors=l4_stats.get("total_vectors", 0),
            total_memory_mb=round(total_mb, 2)
        )


# 单例
_memory_service: Optional[MemoryService] = None


async def get_memory_service() -> MemoryService:
    """获取记忆服务单例"""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
        await _memory_service.init()
    return _memory_service
