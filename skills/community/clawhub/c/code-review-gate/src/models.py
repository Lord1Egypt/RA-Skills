"""门禁结果数据模型。"""

from dataclasses import dataclass, field
from typing import Literal


Severity = Literal["critical", "important", "minor"]
Status = Literal["pass", "fail", "skipped"]
Category = Literal[
    "functional",
    "security",
    "performance",
    "readability",
    "maintainability",
    "testing",
    "documentation",
]


@dataclass
class Finding:
    """单个检查发现。"""

    category: Category
    check_id: str
    question: str
    severity: Severity
    status: Status
    file_ref: str | None = None   # 如 "src/api/users.py:45"
    detail: str | None = None     # 问题描述
    risk: str | None = None       # 风险说明
    fix: str | None = None        # 修复建议


@dataclass
class CheckResult:
    """单个检查器运行结果。"""

    category: Category
    label: str
    severity: Severity
    status: Status              # 整体状态: all pass → "pass", any fail → "fail"
    findings: list[Finding] = field(default_factory=list)
    summary: str = ""           # 简要总结


@dataclass
class ReviewReport:
    """完整审查报告。"""

    base: str | None
    head: str | None
    files: list[str] | None
    diff_stats: str
    design_path: str | None

    results: list[CheckResult]
    strengths: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    design_consistency: list[str] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(
            1 for r in self.results
            for f in r.findings
            if f.severity == "critical" and f.status == "fail"
        )

    @property
    def important_count(self) -> int:
        return sum(
            1 for r in self.results
            for f in r.findings
            if f.severity == "important" and f.status == "fail"
        )

    @property
    def minor_count(self) -> int:
        return sum(
            1 for r in self.results
            for f in r.findings
            if f.severity == "minor" and f.status == "fail"
        )

    @property
    def blocked(self) -> bool:
        return self.critical_count > 0
