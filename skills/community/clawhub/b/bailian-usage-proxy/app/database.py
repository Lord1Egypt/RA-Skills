"""
数据库连接和操作
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, and_
from contextlib import asynccontextmanager

from .config import get_settings
from .models import Base, User, UsageLog, DailyStats


class Database:
    """数据库管理类"""
    
    def __init__(self):
        self.settings = get_settings()
        self.engine = None
        self.async_session = None
    
    async def init(self):
        """初始化数据库连接"""
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.debug,
            pool_pre_ping=True,
        )
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        
        # 创建表
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @asynccontextmanager
    async def get_session(self):
        """获取数据库会话"""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    # 用户相关操作
    async def create_user(self, user: User) -> User:
        """创建用户"""
        async with self.get_session() as session:
            session.add(user)
            await session.flush()
            return user
    
    async def get_user_by_api_key(self, api_key: str) -> Optional[User]:
        """通过API Key获取用户"""
        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.api_key == api_key, User.is_active == 1)
            )
            return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """通过ID获取用户"""
        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
    
    async def list_users(self, department: Optional[str] = None) -> List[User]:
        """列出用户"""
        async with self.get_session() as session:
            query = select(User).where(User.is_active == 1)
            if department:
                query = query.where(User.department == department)
            result = await session.execute(query)
            return result.scalars().all()
    
    # 用量日志相关
    async def log_usage(self, log: UsageLog) -> UsageLog:
        """记录用量"""
        async with self.get_session() as session:
            session.add(log)
            await session.flush()
            return log
    
    async def get_user_daily_usage(self, user_id: str, date: str) -> int:
        """获取用户当日用量"""
        async with self.get_session() as session:
            result = await session.execute(
                select(func.sum(UsageLog.total_tokens)).where(
                    and_(
                        UsageLog.user_id == user_id,
                        UsageLog.request_date == date
                    )
                )
            )
            total = result.scalar()
            return total or 0
    
    async def query_usage_logs(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> List[UsageLog]:
        """查询用量日志"""
        async with self.get_session() as session:
            query = select(UsageLog)
            
            if user_id:
                query = query.where(UsageLog.user_id == user_id)
            if start_date:
                query = query.where(UsageLog.request_date >= start_date)
            if end_date:
                query = query.where(UsageLog.request_date <= end_date)
            
            query = query.order_by(UsageLog.created_at.desc()).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
    
    # 统计相关
    async def get_daily_stats(self, user_id: str, stats_date: str) -> Optional[DailyStats]:
        """获取每日统计"""
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyStats).where(
                    and_(
                        DailyStats.user_id == user_id,
                        DailyStats.stats_date == stats_date
                    )
                )
            )
            return result.scalar_one_or_none()
    
    async def update_daily_stats(self, user_id: str, stats_date: str, **kwargs):
        """更新每日统计"""
        async with self.get_session() as session:
            stats = await self.get_daily_stats(user_id, stats_date)
            if stats:
                for key, value in kwargs.items():
                    setattr(stats, key, value)
                stats.updated_at = datetime.utcnow()
            else:
                stats = DailyStats(
                    id=f"stats_{user_id}_{stats_date}",
                    user_id=user_id,
                    stats_date=stats_date,
                    **kwargs
                )
                session.add(stats)
            await session.flush()


# 全局数据库实例
db = Database()
