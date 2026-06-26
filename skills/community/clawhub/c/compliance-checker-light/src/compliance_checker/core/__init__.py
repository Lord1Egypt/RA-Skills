"""
核心组件模块

包含数据模型、检查器基类和注册表。
注意：get_initialized_registry 已移至 application.bootstrap

Core 层设计原则：
- 零依赖：不依赖任何其他层
- 纯粹性：只包含数据模型、抽象接口、异常定义
- 稳定性：变更频率最低，所有上层都依赖它
"""

from .document import Document, PageContent, DocumentMetadata, DocumentType, ParseResult
from .checklist_model import (
    Checklist,
    RequiredDocument,
    CompliancePoint,
    ValidityRule,
    ProjectPeriod,
    CheckMethod,
    SupportedFileType,
    ChecklistSummary,
    DocumentCheck,
)
from .result_model import (
    FullCheckResult,
    CheckSummary,
    IssueItem,
    CompletenessResult,
    TimelinessResult,
    TimelinessDetail,
    ComplianceResult,
    DocumentCompliance,
    ComplianceCheckItem,
    DocumentMatch,
    MatchType,
)
from .checker_base import CheckStatus, CheckResult, BaseChecker, UnavailableChecker
from .checker_registry import CheckerRegistry
from .exceptions import (
    ComplianceCheckerError,
    ChecklistError,
    DocumentParseError,
    CheckExecutionError,
)
from .interfaces import (
    SemanticMatcherProtocol,
    DocumentParserProtocol,
    VisualCheckerProtocol,
    LLMClientProtocol,
    OCREngineProtocol,
)
from .yaml_compat import safe_load, simple_yaml_load

__all__ = [
    # 文档模型
    "Document",
    "PageContent",
    "DocumentMetadata",
    "DocumentType",
    "ParseResult",
    # 清单模型
    "Checklist",
    "RequiredDocument",
    "CompliancePoint",
    "ValidityRule",
    "ProjectPeriod",
    "CheckMethod",
    "SupportedFileType",
    "ChecklistSummary",
    "DocumentCheck",
    # 检查结果模型
    "CheckStatus",
    "CheckResult",
    "FullCheckResult",
    "CheckSummary",
    "IssueItem",
    "CompletenessResult",
    "TimelinessResult",
    "TimelinessDetail",
    "ComplianceResult",
    "DocumentCompliance",
    "ComplianceCheckItem",
    "DocumentMatch",
    "MatchType",
    # 检查器基类
    "BaseChecker",
    "UnavailableChecker",
    # 注册表
    "CheckerRegistry",
    # 异常
    "ComplianceCheckerError",
    "ChecklistError",
    "DocumentParseError",
    "CheckExecutionError",
    # 接口协议
    "SemanticMatcherProtocol",
    "DocumentParserProtocol",
    "VisualCheckerProtocol",
    "LLMClientProtocol",
    "OCREngineProtocol",
    # YAML 兼容层
    "safe_load",
    "simple_yaml_load",
]
