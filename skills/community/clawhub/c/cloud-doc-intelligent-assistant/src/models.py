"""数据模型定义"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ChangeType(Enum):
    """变更类型枚举"""
    MINOR = "minor"  # 小改动
    MAJOR = "major"  # 大改动
    STRUCTURAL = "structural"  # 结构性变化


@dataclass
class Document:
    """文档数据模型"""
    url: str
    title: str
    content: str
    content_hash: str
    last_modified: Optional[datetime] = None
    crawled_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentChange:
    """文档变更数据模型"""
    document: Document
    old_content_hash: str
    new_content_hash: str
    diff: str
    change_type: ChangeType


@dataclass
class ChangeReport:
    """变更报告数据模型"""
    added: List[Document] = field(default_factory=list)
    modified: List[DocumentChange] = field(default_factory=list)
    deleted: List[Document] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Notification:
    """通知数据模型"""
    title: str
    summary: str
    changes: List[DocumentChange]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
