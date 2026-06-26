"""
Base CMS Connector - Abstract interface for all CMS platforms.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)


class OperationType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    PUBLISH = "publish"
    DRAFT = "draft"


class OperationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class CMSCredential:
    """CMS连接凭证"""
    url: str
    username: str = ""
    api_key: str = ""
    app_password: str = ""  # WordPress App Password
    timeout: int = 30

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if v}


@dataclass
class ContentPayload:
    """内容发布载荷"""
    title: str
    content: str
    status: str = "draft"  # draft | publish | pending | private
    excerpt: str = ""
    author: int = 1
    categories: List[int] = field(default_factory=list)
    tags: List[int] = field(default_factory=list)
    featured_media: int = 0
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationRecord:
    """操作记录（用于回滚和审计）"""
    id: str
    timestamp: datetime
    operation: OperationType
    entity_type: str  # post | page | media
    entity_id: Optional[int]
    payload: Dict[str, Any]
    response: Optional[Dict[str, Any]]
    status: OperationStatus
    error_message: str = ""
    executor: str = "system"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "operation": self.operation.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "payload": self.payload,
            "response": self.response,
            "status": self.status.value,
            "error_message": self.error_message,
            "executor": self.executor,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OperationRecord":
        d["timestamp"] = datetime.fromisoformat(d["timestamp"])
        d["operation"] = OperationType(d["operation"])
        d["status"] = OperationStatus(d["status"])
        return cls(**d)


class BaseCMSConnector(ABC):
    """
    抽象CMS连接器基类。
    所有平台连接器（WordPress/Shopify/Strapi等）必须继承此类。
    """

    def __init__(self, credential: CMSCredential, storage_path: str = "./cms_history.json"):
        self.credential = credential
        self.storage_path = storage_path
        self._history: List[OperationRecord] = []
        self._load_history()

    # ── 认证 ──────────────────────────────────────────────
    @abstractmethod
    def authenticate(self) -> bool:
        """验证凭证有效性"""
        pass

    # ── 内容操作 ───────────────────────────────────────────
    @abstractmethod
    def create_content(self, payload: ContentPayload) -> Dict[str, Any]:
        """创建内容"""
        pass

    @abstractmethod
    def update_content(self, content_id: int, payload: ContentPayload) -> Dict[str, Any]:
        """更新内容"""
        pass

    @abstractmethod
    def delete_content(self, content_id: int, force: bool = False) -> Dict[str, Any]:
        """删除内容"""
        pass

    @abstractmethod
    def get_content(self, content_id: int) -> Dict[str, Any]:
        """获取单条内容"""
        pass

    @abstractmethod
    def list_content(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """列出内容"""
        pass

    # ── 辅助方法 ───────────────────────────────────────────
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())[:8]

    def _save_record(self, record: OperationRecord) -> None:
        """持久化操作记录"""
        self._history.append(record)
        self._persist_history()

    def _persist_history(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self._history], f, ensure_ascii=False, indent=2)

    def _load_history(self) -> None:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._history = [OperationRecord.from_dict(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self._history = []

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._history[-limit:]]

    def rollback_operation(self, record_id: str) -> bool:
        """根据操作记录ID执行回滚"""
        for record in reversed(self._history):
            if record.id == record_id:
                return self._do_rollback(record)
        return False

    @abstractmethod
    def _do_rollback(self, record: OperationRecord) -> bool:
        """子类实现具体回滚逻辑"""
        pass

    def close(self) -> None:
        """关闭连接，清理资源"""
        self._persist_history()
