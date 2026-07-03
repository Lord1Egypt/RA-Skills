"""检查器基类。"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path

from src.models import Category, Severity, Status, Finding, CheckResult


class BaseChecker(ABC):
    """所有检查器的抽象基类。"""

    category: Category
    label: str
    severity: Severity

    def __init__(self, diff: str, diff_stats: str, design_doc: str | None):
        self.diff = diff
        self.diff_stats = diff_stats
        self.design_doc = design_doc
        self.findings: list[Finding] = []

    @abstractmethod
    def run(self) -> list[CheckResult]:
        """执行检查，返回检查结果列表。"""

    def _finding(
        self,
        check_id: str,
        question: str,
        severity: Severity,
        status: Status,
        file_ref: str | None = None,
        detail: str | None = None,
        risk: str | None = None,
        fix: str | None = None,
    ) -> Finding:
        f = Finding(
            category=self.category,
            check_id=check_id,
            question=question,
            severity=severity,
            status=status,
            file_ref=file_ref,
            detail=detail,
            risk=risk,
            fix=fix,
        )
        self.findings.append(f)
        return f

    def _result(self, label: str) -> CheckResult:
        """生成该检查器的汇总结果。"""
        all_pass = all(
            f.status == "pass" or f.status == "skipped"
            for f in self.findings
        )
        return CheckResult(
            category=self.category,
            label=label,
            severity=self.severity,
            status="pass" if all_pass else "fail",
            findings=list(self.findings),
        )

    def _parse_file_refs(self) -> list[str]:
        """从 diff 中提取变更文件列表。"""
        files: list[str] = []
        for line in self.diff.split("\n"):
            m = re.match(r"^\+\+\+ b/(.+)$", line)
            if m:
                files.append(m.group(1))
        return files

    def _get_file_extensions(self) -> set[str]:
        """获取变更文件的扩展名集合。"""
        exts: set[str] = set()
        for f in self._parse_file_refs():
            ext = Path(f).suffix.lower()
            if ext:
                exts.add(ext)
        return exts
