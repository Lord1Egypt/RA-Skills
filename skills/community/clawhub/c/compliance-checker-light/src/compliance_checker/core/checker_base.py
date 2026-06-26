"""
检查器基类模块

定义所有检查器的抽象基类和通用接口。
注意：此文件只包含类型定义和抽象方法签名，不包含具体实现逻辑。
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class CheckStatus(str, Enum):
    """检查结果状态"""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    INCOMPLETE = "incomplete"
    HAS_ISSUES = "has_issues"
    UNCLEAR = "unclear"
    MISSING = "missing"
    EXPIRED = "expired"
    VALID = "valid"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


@dataclass
class CheckResult:
    """检查结果数据类"""

    check_type: str
    status: CheckStatus
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "check_type": self.check_type,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "issues": self.issues,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CheckResult":
        """从字典创建"""
        return cls(
            check_type=data.get("check_type", ""),
            status=CheckStatus(data.get("status", "error")),
            message=data.get("message", ""),
            details=data.get("details", {}),
            issues=data.get("issues", []),
        )


class BaseChecker(ABC):
    """
    所有检查器的抽象基类

    子类必须实现:
    - name: 检查器唯一标识
    - description: 检查器描述
    - check: 执行检查的核心方法
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """检查器唯一标识，如 'completeness', 'visual'"""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """检查器描述"""
        ...

    @property
    def version(self) -> str:
        """检查器版本"""
        return "1.0.0"

    @abstractmethod
    async def check(
        self,
        documents: List["Document"],
        checklist: Optional["Checklist"],
        doc_checks: Dict[str, Any],
    ) -> CheckResult:
        """
        执行检查

        Args:
            documents: 已解析的文档列表
            checklist: 审核清单
            doc_checks: 检查配置（来自清单的 checks 配置）

        Returns:
            CheckResult: 检查结果
        """
        ...

    def is_available(self) -> bool:
        """检查器是否可用（依赖是否安装等）"""
        return True

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """
        验证检查配置是否合法

        Args:
            config: 检查配置

        Returns:
            (是否合法, 错误信息)
        """
        return True, ""


class UnavailableChecker(BaseChecker):
    """
    占位检查器 - 用于未实现的功能

    当清单中配置了某个检查类型，但该检查器尚未实现时，
    使用此类返回友好的提示信息，而不是报错。
    """

    def __init__(self, check_type: str):
        self._name = check_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"[{self._name}] 检查器尚未实现"

    async def check(
        self,
        documents: List["Document"],
        checklist: Optional["Checklist"],
        doc_checks: Dict[str, Any],
    ) -> CheckResult:
        """返回未实现的提示"""
        return CheckResult(
            check_type=self._name,
            status=CheckStatus.UNAVAILABLE,
            message=f"查不了这块，去联系项目负责人。功能 '{self._name}' 正在开发中...",
            details={
                "contact": "项目负责人",
                "status": "开发中",
                "suggestion": "如需此功能，请联系开发团队添加该检查器",
            },
        )

    def is_available(self) -> bool:
        return False


class AliasCheckerWrapper(BaseChecker):
    """
    检查器别名包装器

    用于为同一个检查器实例注册多个名称（别名）。
    例如：VisualChecker 的 name 是 "compliance"，但清单中可能使用 "visual" 类型。
    使用此类可以将 "visual" 映射到同一个检查器实例。
    """

    def __init__(self, wrapped_checker: BaseChecker, alias_name: str):
        """
        初始化别名包装器

        Args:
            wrapped_checker: 被包装的实际检查器实例
            alias_name: 别名（注册表中使用的名称）
        """
        self._wrapped = wrapped_checker
        self._alias_name = alias_name

    @property
    def name(self) -> str:
        """返回别名"""
        return self._alias_name

    @property
    def description(self) -> str:
        """返回被包装检查器的描述"""
        return self._wrapped.description

    @property
    def version(self) -> str:
        """返回被包装检查器的版本"""
        return self._wrapped.version

    async def check(
        self,
        documents: List["Document"],
        checklist: Optional["Checklist"],
        doc_checks: Dict[str, Any],
    ) -> CheckResult:
        """委托给被包装的检查器执行"""
        return await self._wrapped.check(documents, checklist, doc_checks)

    def is_available(self) -> bool:
        """返回被包装检查器的可用状态"""
        return self._wrapped.is_available()

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """委托给被包装的检查器验证配置"""
        return self._wrapped.validate_config(config)
