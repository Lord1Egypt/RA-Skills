"""数据模型定义"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class MemoryLevel(str, Enum):
    """记忆层级"""
    L1_HOT = "l1_hot"       # 热存储 - Redis
    L2_WARM = "l2_warm"     # 温存储 - SQLite
    L3_COLD = "l3_cold"     # 冷存储 - Markdown文件
    L4_ARCHIVE = "l4_archive"  # 归档 - FAISS+压缩


class EventType(str, Enum):
    """事件类型"""
    DECISION = "decision"       # 决策
    ERROR = "error"             # 错误
    LESSON = "lesson"           # 学到的内容
    COMPLETION = "completion"   # 完成
    IMPORTANT = "important"     # 重要信息
    QUESTION = "question"       # 问题
    RELATIONSHIP = "relationship"  # 关系约定
    SYSTEM = "system"           # 系统架构/健康


class MemoryItem(BaseModel):
    """记忆条目"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key: str
    content: str
    level: MemoryLevel = MemoryLevel.L1_HOT
    importance: int = Field(default=0, ge=0, le=100)  # 重要性评分 0-100
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None  # 向量嵌入
    tags: List[str] = Field(default_factory=list)
    
    # 时间戳
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    
    # 统计
    access_count: int = 0
    reference_count: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "key": "session_20260207",
                "content": "重要的决策内容...",
                "level": "l1_hot",
                "importance": 75,
                "tags": ["决策", "重要"]
            }
        }


class Event(BaseModel):
    """检测到的事件"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: EventType
    category: str  # 事件分类
    content: str
    confidence: float = Field(ge=0.0, le=1.0)  # 置信度
    matches: List[str] = Field(default_factory=list)  # 匹配的关键词
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_memory_id: Optional[str] = None


class DailySummary(BaseModel):
    """每日摘要"""
    date: str  # YYYY-MM-DD
    overview: str
    activities: List[Dict[str, Any]] = Field(default_factory=list)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    lessons: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class SearchResult(BaseModel):
    """搜索结果"""
    id: str
    key: str
    content: str
    similarity: float  # 相似度分数
    level: MemoryLevel
    metadata: Dict[str, Any]
    created_at: datetime


class StorageStats(BaseModel):
    """存储统计"""
    l1_entries: int = 0
    l1_size_bytes: int = 0
    l2_entries: int = 0
    l3_files: int = 0
    l4_vectors: int = 0
    total_memory_mb: float = 0.0
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class PersistenceConfig(BaseModel):
    """沉淀配置"""
    immediate_threshold: int = 70    # 立即沉淀阈值
    daily_threshold: int = 40        # 每日摘要阈值
    archive_days: int = 90           # 归档天数
    l1_max_size_mb: int = 100        # L1最大容量
    l2_max_entries: int = 10000      # L2最大条目数


# API请求/响应模型
class SetMemoryRequest(BaseModel):
    """存储记忆请求"""
    key: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    importance: Optional[int] = None  # 可选，自动计算
    tags: List[str] = Field(default_factory=list)


class SetMemoryResponse(BaseModel):
    """存储记忆响应"""
    success: bool
    item: MemoryItem
    persisted_level: MemoryLevel
    importance_score: int


class GetMemoryResponse(BaseModel):
    """获取记忆响应"""
    found: bool
    item: Optional[MemoryItem] = None
    from_level: Optional[MemoryLevel] = None


class SearchRequest(BaseModel):
    """搜索请求"""
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    levels: List[MemoryLevel] = Field(default_factory=list)  # 指定搜索层级
    min_similarity: float = Field(default=0.5, ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """搜索响应"""
    query: str
    total_results: int
    results: List[SearchResult]
    search_time_ms: float


class AnalyzeRequest(BaseModel):
    """分析内容请求"""
    content: str
    context: Dict[str, Any] = Field(default_factory=dict)


class AnalyzeResponse(BaseModel):
    """分析内容响应"""
    importance: int
    events: List[Event]
    is_sensitive: bool
    should_persist: bool
    suggested_level: MemoryLevel
