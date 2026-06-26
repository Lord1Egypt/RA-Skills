"""L2 温存储 - SQLite实现"""
import json
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Column, DateTime, Integer, JSON, String, Text, create_engine, select, delete
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings
from app.models import MemoryItem, MemoryLevel

Base = declarative_base()


class MemoryRecord(Base):
    """记忆记录表"""
    __tablename__ = "memories"
    
    id = Column(String(36), primary_key=True)
    key = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    level = Column(String(20), default="l2_warm")
    importance = Column(Integer, default=0)
    meta_data = Column(JSON, default=dict)
    tags = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_accessed = Column(DateTime, nullable=True)
    access_count = Column(Integer, default=0)


class L2WarmStorage:
    """L2温存储 - SQLite实现"""
    
    def __init__(self):
        self.engine = None
        self.async_session = None
    
    async def init(self):
        """初始化数据库"""
        # 确保目录存在
        settings.SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建异步引擎
        db_url = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"
        self.engine = create_async_engine(db_url, echo=False)
        
        # 创建表
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # 创建会话工厂
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        
        print(f"[L2] SQLite initialized: {settings.SQLITE_PATH}")
    
    async def get(self, key: str) -> Optional[MemoryItem]:
        """获取记忆"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            result = await session.execute(
                select(MemoryRecord).where(MemoryRecord.key == key)
            )
            record = result.scalar_one_or_none()
            
            if not record:
                return None
            
            # 更新访问统计
            record.access_count += 1
            record.last_accessed = datetime.utcnow()
            await session.commit()
            
            return self._record_to_item(record)
    
    async def set(self, item: MemoryItem) -> bool:
        """存储记忆"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            # 检查是否已存在
            result = await session.execute(
                select(MemoryRecord).where(MemoryRecord.id == item.id)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                # 更新
                existing.content = item.content
                existing.importance = item.importance
                existing.metadata = item.metadata
                existing.tags = item.tags
                existing.updated_at = datetime.utcnow()
            else:
                # 新建
                record = MemoryRecord(
                    id=item.id,
                    key=item.key,
                    content=item.content,
                    level=item.level.value,
                    importance=item.importance,
                    metadata=item.metadata,
                    tags=item.tags,
                    created_at=item.created_at,
                    updated_at=item.updated_at
                )
                session.add(record)
            
            await session.commit()
            return True
    
    async def delete(self, key: str) -> bool:
        """删除记忆"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            result = await session.execute(
                delete(MemoryRecord).where(MemoryRecord.key == key)
            )
            await session.commit()
            return result.rowcount > 0
    
    async def list_all(self, limit: int = 1000) -> List[MemoryItem]:
        """列出所有记忆"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            result = await session.execute(
                select(MemoryRecord).limit(limit)
            )
            records = result.scalars().all()
            return [self._record_to_item(r) for r in records]
    
    async def get_for_daily_summary(self) -> List[MemoryItem]:
        """获取需要每日摘要的记忆"""
        if not self.async_session:
            await self.init()
        
        # 获取今天创建且重要性>=40的记忆
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        async with self.async_session() as session:
            result = await session.execute(
                select(MemoryRecord)
                .where(MemoryRecord.created_at >= today)
                .where(MemoryRecord.importance >= settings.IMPORTANCE_DAILY)
            )
            records = result.scalars().all()
            return [self._record_to_item(r) for r in records]
    
    async def get_oldest(self, limit: int = 100) -> List[MemoryItem]:
        """获取最旧的记忆（用于淘汰）"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            result = await session.execute(
                select(MemoryRecord)
                .order_by(MemoryRecord.last_accessed.asc().nullsfirst())
                .limit(limit)
            )
            records = result.scalars().all()
            return [self._record_to_item(r) for r in records]
    
    async def stats(self) -> dict:
        """获取统计信息"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            from sqlalchemy import func
            
            result = await session.execute(select(func.count()).select_from(MemoryRecord))
            count = result.scalar()
            
            return {
                "entries": count
            }
    
    def _record_to_item(self, record: MemoryRecord) -> MemoryItem:
        """数据库记录转模型"""
        return MemoryItem(
            id=record.id,
            key=record.key,
            content=record.content,
            level=MemoryLevel(record.level),
            importance=record.importance,
            metadata=record.metadata or {},
            tags=record.tags or [],
            created_at=record.created_at,
            updated_at=record.updated_at,
            last_accessed=record.last_accessed,
            access_count=record.access_count
        )
    
    async def close(self):
        """关闭连接"""
        if self.engine:
            await self.engine.dispose()


# 单例
_l2_storage: Optional[L2WarmStorage] = None


async def get_l2_storage() -> L2WarmStorage:
    """获取L2存储单例"""
    global _l2_storage
    if _l2_storage is None:
        _l2_storage = L2WarmStorage()
        await _l2_storage.init()
    return _l2_storage
