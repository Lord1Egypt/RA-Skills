"""
APP 数据模型 - 榜单记录
"""

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class AppRecord(Base):
    """应用榜单记录"""
    __tablename__ = "app_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_date = Column(Date, nullable=False, index=True)  # 记录日期
    
    # 应用信息
    app_id = Column(String(50), nullable=False, index=True)  # App Store ID
    bundle_id = Column(String(200))  # Bundle ID
    app_name = Column(String(200), nullable=False)  # 应用名称
    developer = Column(String(200))  # 开发者
    
    # 榜单信息
    chart_type = Column(String(50), nullable=False)  # 榜单类型：top_free/top_paid/new_free/new_paid
    genre = Column(Integer, default=0)  # 分类 ID（0 表示总榜）
    rank = Column(Integer)  # 排名
    
    # 应用详情
    category = Column(String(100))  # 分类名称
    price = Column(String(20))  # 价格
    icon_url = Column(Text)  # 图标 URL
    
    # 追踪信息
    is_new = Column(Boolean, default=False)  # 是否新上架
    first_seen = Column(String(50))  # 首次发现日期
    last_seen = Column(String(50))  # 最后发现日期
    updated_at = Column(String(50), default=lambda: datetime.now().isoformat())
    
    def __repr__(self):
        return f"<AppRecord(app_id={self.app_id}, name='{self.app_name}', rank={self.rank}, date={self.record_date})>"
