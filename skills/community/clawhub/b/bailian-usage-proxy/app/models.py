"""
数据模型
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(String(32), primary_key=True, comment="用户ID")
    name = Column(String(100), nullable=False, comment="用户名称")
    department = Column(String(100), nullable=True, comment="部门")
    api_key = Column(String(64), unique=True, nullable=False, comment="API Key")
    daily_limit = Column(Integer, default=1000000, comment="日限额(tokens)")
    monthly_limit = Column(Integer, default=10000000, comment="月限额(tokens)")
    is_active = Column(Integer, default=1, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    __table_args__ = (
        Index('idx_api_key', 'api_key'),
        Index('idx_department', 'department'),
    )


class UsageLog(Base):
    """用量日志表"""
    __tablename__ = "usage_logs"
    
    id = Column(String(32), primary_key=True, comment="记录ID")
    user_id = Column(String(32), nullable=False, comment="用户ID")
    request_id = Column(String(64), nullable=False, comment="请求ID")
    model = Column(String(50), nullable=False, comment="模型名称")
    
    # Token统计
    input_tokens = Column(Integer, default=0, comment="输入token数")
    output_tokens = Column(Integer, default=0, comment="输出token数")
    total_tokens = Column(Integer, default=0, comment="总token数")
    
    # 请求信息
    request_type = Column(String(20), nullable=False, comment="请求类型: chat/completion/embedding")
    status_code = Column(Integer, comment="HTTP状态码")
    response_time_ms = Column(Integer, comment="响应时间(ms)")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    request_date = Column(String(10), nullable=False, comment="请求日期(YYYY-MM-DD)")
    
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'request_date'),
        Index('idx_model', 'model'),
        Index('idx_created_at', 'created_at'),
    )


class DailyStats(Base):
    """每日统计表"""
    __tablename__ = "daily_stats"
    
    id = Column(String(32), primary_key=True, comment="记录ID")
    user_id = Column(String(32), nullable=False, comment="用户ID")
    stats_date = Column(String(10), nullable=False, comment="统计日期")
    
    # 用量统计
    total_requests = Column(Integer, default=0, comment="总请求数")
    total_input_tokens = Column(Integer, default=0, comment="总输入token")
    total_output_tokens = Column(Integer, default=0, comment="总输出token")
    total_tokens = Column(Integer, default=0, comment="总token数")
    
    # 模型分布(JSON格式)
    model_distribution = Column(Text, comment="模型使用分布")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    __table_args__ = (
        Index('idx_user_stats_date', 'user_id', 'stats_date', unique=True),
    )


# Pydantic模型
class UserCreate(BaseModel):
    """创建用户请求"""
    name: str = Field(..., min_length=1, max_length=100, description="用户名称")
    department: Optional[str] = Field(None, max_length=100, description="部门")
    daily_limit: int = Field(default=1000000, ge=0, description="日限额")
    monthly_limit: int = Field(default=10000000, ge=0, description="月限额")


class UserResponse(BaseModel):
    """用户响应"""
    id: str
    name: str
    department: Optional[str]
    api_key: str
    daily_limit: int
    monthly_limit: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UsageQuery(BaseModel):
    """用量查询请求"""
    user_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    model: Optional[str] = None


class UsageReport(BaseModel):
    """用量报表"""
    user_id: str
    user_name: str
    period: str
    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    model_breakdown: dict
    daily_trend: list
