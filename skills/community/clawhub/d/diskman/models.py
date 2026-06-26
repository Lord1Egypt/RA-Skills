"""Shared data models for diskman."""

from dataclasses import dataclass, field
from enum import Enum


class LinkType(Enum):
    """Type of file system link."""

    NORMAL = "normal"
    SYMBOLIC_LINK = "symbolic_link"
    JUNCTION = "junction"
    NOT_FOUND = "not_found"


class RiskLevel(Enum):
    """Risk level for operations."""

    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DirectoryType(Enum):
    """Type of directory content."""

    CACHE = "cache"
    DEPENDENCY = "dependency"
    BUILD = "build"
    TEMP = "temp"
    LOG = "log"
    CONFIG = "config"
    DATA = "data"
    PROJECT = "project"
    SYSTEM = "system"
    MIGRATED = "migrated"  # 已迁移的目录
    UNKNOWN = "unknown"


class RecommendedAction(Enum):
    """Recommended action for a directory."""

    CAN_DELETE = "can_delete"
    CAN_MOVE = "can_move"
    KEEP = "keep"
    REVIEW = "review"


@dataclass
class FileInfo:
    """Information about a file."""

    path: str
    name: str
    size_bytes: int = 0
    modified_time: float | None = None

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / 1024 / 1024, 2)

    @property
    def size_gb(self) -> float:
        return round(self.size_bytes / 1024 / 1024 / 1024, 2)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "name": self.name,
            "size_bytes": self.size_bytes,
            "size_mb": self.size_mb,
            "size_gb": self.size_gb,
            "modified_time": self.modified_time,
        }


@dataclass
class DirectoryInfo:
    """Information about a directory."""

    path: str
    size_bytes: int = 0
    link_type: LinkType = LinkType.NORMAL
    link_target: str | None = None
    file_types: dict[str, int] = field(default_factory=dict)
    file_count: int = 0

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / 1024 / 1024, 2)

    @property
    def size_gb(self) -> float:
        return round(self.size_bytes / 1024 / 1024 / 1024, 2)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "size_bytes": self.size_bytes,
            "size_mb": self.size_mb,
            "size_gb": self.size_gb,
            "link_type": self.link_type.value,
            "link_target": self.link_target,
            "file_types": self.file_types,
            "file_count": self.file_count,
        }


@dataclass
class AnalysisResult:
    """Result of directory analysis."""

    path: str
    directory_type: DirectoryType
    risk_level: RiskLevel
    recommended_action: RecommendedAction
    reason: str
    confidence: float = 0.5
    dependencies: list[str] = field(default_factory=list)
    target_path: str | None = None

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "type": self.directory_type.value,
            "risk": self.risk_level.value,
            "action": self.recommended_action.value,
            "reason": self.reason,
            "confidence": self.confidence,
            "dependencies": self.dependencies,
            "target_path": self.target_path,
        }


@dataclass
class ScanResult:
    """Result of a scan operation."""

    directories: list[DirectoryInfo] = field(default_factory=list)
    files: list[FileInfo] = field(default_factory=list)
    total_size_bytes: int = 0
    scan_path: str = ""

    @property
    def total_size_mb(self) -> float:
        return round(self.total_size_bytes / 1024 / 1024, 2)

    @property
    def total_size_gb(self) -> float:
        return round(self.total_size_bytes / 1024 / 1024 / 1024, 2)

    def to_dict(self) -> dict:
        return {
            "scan_path": self.scan_path,
            "dir_count": len(self.directories),
            "file_count": len(self.files),
            "total_size_mb": self.total_size_mb,
            "total_size_gb": self.total_size_gb,
            "directories": [d.to_dict() for d in self.directories],
            "files": [f.to_dict() for f in self.files],
        }


@dataclass
class MigrationResult:
    """Result of a migration operation."""

    success: bool
    source: str
    target: str
    link_type: str | None = None
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "source": self.source,
            "target": self.target,
            "link_type": self.link_type,
            "error": self.error,
        }


@dataclass
class CleanResult:
    """Result of a clean operation."""

    success: bool
    path: str
    freed_bytes: int = 0
    dry_run: bool = False
    error: str | None = None

    @property
    def freed_mb(self) -> float:
        return round(self.freed_bytes / 1024 / 1024, 2)

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "path": self.path,
            "freed_mb": self.freed_mb,
            "freed_bytes": self.freed_bytes,
            "dry_run": self.dry_run,
            "error": self.error,
        }


@dataclass
class AnalysisContext:
    """Context for directory analysis."""

    user_type: str | None = None
    project_type: str | None = None
    intent: str | None = None
    target_drive: str | None = None
