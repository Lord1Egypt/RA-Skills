"""Builder Agent 데이터 모델"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Complexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class DiscoverySource(Enum):
    GITHUB_TRENDING = "github_trending"
    CVE_DATABASE = "cve_database"
    SECURITY_NEWS = "security_news"


class PipelineStage(Enum):
    IDLE = "idle"
    DISCOVERING = "discovering"
    QUEUING = "queuing"
    BUILDING = "building"
    TESTING = "testing"
    FIXING = "fixing"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ProjectIdea:
    title: str
    description: str
    source: str  # DiscoverySource value
    priority: str = "medium"
    complexity: str = "medium"
    url: Optional[str] = None
    tech_stack: List[str] = field(default_factory=list)
    score: float = 0.0
    discovered_at: str = ""
    notion_page_id: Optional[str] = None
    # CVE 전용
    cve_id: Optional[str] = None
    severity: Optional[str] = None
    cvss_score: Optional[float] = None
    # 메타
    keyword: Optional[str] = None

    def __post_init__(self):
        if not self.discovered_at:
            self.discovered_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectIdea':
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class ErrorAnalysis:
    error_type: str  # 'type_error', 'import_error', 'missing_method', 'test_failure', 'unknown'
    raw_output: str
    fix_suggestion: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    fixed: bool = False

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class BuildResult:
    success: bool
    project_path: str
    retry_count: int
    errors: List[ErrorAnalysis] = field(default_factory=list)
    test_output: str = ""
    mode: str = "direct"

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'project_path': self.project_path,
            'retry_count': self.retry_count,
            'errors': [e.to_dict() for e in self.errors],
            'test_output': self.test_output,
            'mode': self.mode,
        }


@dataclass
class PipelineState:
    stage: str = "idle"
    current_project: Optional[str] = None
    started_at: Optional[str] = None
    last_checkpoint: Optional[str] = None
    errors: List[str] = field(default_factory=list)

    def set_stage(self, stage: str):
        self.stage = stage
        self.last_checkpoint = datetime.now().isoformat()
