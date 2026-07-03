"""文档检查器 — 检测文档同步和 API 文档完整性。"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class DocumentationChecker(BaseChecker):
    category = "documentation"
    label = "文档同步 (Documentation)"
    severity = "minor"

    def run(self) -> list[CheckResult]:
        self._check_docstrings()
        self._check_todo_fixme()
        self._check_comments_quality()

        return [self._result(self.label)]

    def _check_docstrings(self) -> None:
        """检查公共函数是否有文档字符串。"""
        # 检测新增的公开函数
        for match in re.finditer(
            r"^\+\s*def\s+(?!_)(\w+)\s*\([^)]*\)\s*:", self.diff, re.MULTILINE
        ):
            func_name = match.group(1)
            # 检查后续几行是否有 docstring
            end = match.end()
            after = self.diff[end:end + 200]
            has_docstring = bool(re.search(r'"""', after)) or bool(re.search(r"'''", after))

            if not has_docstring:
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="doc-docstring",
                    question="公共 API 是否有文档？",
                    severity="minor",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=f"公开函数 {func_name}() 缺少文档字符串",
                    risk="使用者无法了解函数功能、参数和返回值",
                    fix='添加 """简短描述\n\nArgs:\n    ...\nReturns:\n    ..."""',
                )

    def _check_todo_fixme(self) -> None:
        """检测 TODO/FIXME 是否有处理计划。"""
        todo_patterns = [
            (r"TODO\s*[:(]?", "TODO"),
            (r"FIXME\s*[:(]?", "FIXME"),
            (r"HACK\s*[:(]?", "HACK"),
            (r"XXX\s*[:(]?", "XXX"),
        ]
        for pattern, label in todo_patterns:
            for match in re.finditer(pattern, self.diff):
                line = self.diff[:match.start()].count("\n") + 1
                context = self.diff[match.start():match.start() + 80].replace("\n", " ")
                self._finding(
                    check_id="doc-todo",
                    question="TODO/FIXME 是否有明确的处理计划？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=f"{label}: {context.strip()[:60]}",
                    risk="未解决的 TODO/FIXME 可能在发布后被遗忘",
                    fix="关联 issue 编号或添加负责人和截止日期",
                )

    def _check_comments_quality(self) -> None:
        """检查注释质量。"""
        # 检测"是什么"而非"为什么"的低质量注释
        for match in re.finditer(
            r"\+\s*#\s*(?:set|get|create|update|delete|add|remove)\s+\w+", self.diff
        ):
            line = self.diff[:match.start()].count("\n") + 1
            comment = match.group(0).strip()
            self._finding(
                check_id="doc-quality",
                question="注释是否有价值？",
                severity="minor",
                status="fail",
                file_ref=f"line ~{line}",
                detail=f"注释描述'是什么'而非'为什么': {comment}",
                risk="冗余注释增加维护负担",
                fix="解释业务原因、设计决策或非显而易见的逻辑",
            )
