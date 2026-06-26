"""Data models for BeautyPlus AI SDK."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    POLLING = "polling"


@dataclass
class UploadResult:
    """Result of a media upload operation."""
    url: str
    size: int
    media_type: str = ""
    bucket: str = ""
    key: str = ""


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: Optional[str] = None
    output_urls: List[str] = field(default_factory=list)
    primary_url: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    error: Optional[str] = None
    error_code: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    pipeline_trace: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        """Check if task completed successfully."""
        return self.status == TaskStatus.COMPLETED and not self.error

    @property
    def is_failed(self) -> bool:
        """Check if task failed."""
        return self.status == TaskStatus.FAILED or bool(self.error)


@dataclass
class TokenPolicy:
    """OSS/AI token policy configuration."""
    url: str
    bucket: str
    key: str
    credentials: Dict[str, str]
    data: Optional[Dict[str, Any]] = None
    ttl: int = 3600
    push_path: str = ""
    status_query: Dict[str, Any] = field(default_factory=dict)
    sync_timeout: int = 10


@dataclass
class ConsumeResult:
    """Result of quota consumption."""
    success: bool
    context: str = ""
    gid: Optional[str] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None
