"""测试覆盖检查器 — 检测测试代码是否存在和被更新。"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class TestingChecker(BaseChecker):
    category = "testing"
    label = "测试覆盖 (Testing)"
    severity = "critical"

    def run(self) -> list[CheckResult]:
        ext = self._get_file_extensions()
        code_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php"}
        if not ext & code_exts and ext:
            self._finding("test-skip", "测试检查", "critical", "skipped",
                          detail="非代码文件，跳过测试检查")
            return [self._result(self.label)]

        self._check_tests_exist()
        self._check_test_assertions()
        self._check_test_isolation()

        return [self._result(self.label)]

    def _check_tests_exist(self) -> None:
        """检查是否有对应测试文件变更。"""
        # 检测新增的公开函数/方法
        new_funcs = re.findall(
            r"^\+\s*def\s+(?!_)(\w+)\s*\([^)]*\)\s*:", self.diff, re.MULTILINE
        )
        new_classes = re.findall(
            r"^\+\s*class\s+(\w+)", self.diff, re.MULTILINE
        )

        changed_files = self._parse_file_refs()
        test_files = [f for f in changed_files if "test" in f.lower() or f.endswith("_test.py") or "_test." in f]

        public_funcs = [f for f in new_funcs if not f.startswith("_")]
        if public_funcs and not test_files:
            self._finding(
                check_id="test-exist",
                question="是否有相应的单元测试？",
                severity="critical",
                status="fail",
                detail=f"新增公开函数 {public_funcs[:3]}{'...' if len(public_funcs) > 3 else ''}，但未检测到测试文件变更",
                risk="未测试的代码可能在后续变更中无感知地引入 bug",
                fix="为新增功能编写单元测试",
            )

        # 文件被修改但无对应测试修改
        if changed_files and not test_files:
            self._finding(
                check_id="test-exist",
                question="是否有相应的单元测试？",
                severity="critical",
                status="fail",
                detail=f"修改了 {len(changed_files)} 个文件，但未发现测试文件更新",
                risk="修改可能破坏现有行为且未被测试捕获",
                fix="更新相关测试或确认无需测试（请在审查中说明理由）",
            )

    def _check_test_assertions(self) -> None:
        """检查测试断言是否清晰。"""
        # 检查测试文件中是否有断言
        if "test" in self.diff.lower():
            # 无断言的测试
            for match in re.finditer(
                r"^\+\s*def\s+test_\w+.*\n(?:\+.*\n){0,20}",
                self.diff, re.MULTILINE
            ):
                block = match.group(0)
                if "assert" not in block:
                    line = self.diff[:match.start()].count("\n") + 1
                    self._finding(
                        check_id="test-assert",
                        question="测试断言是否清晰？",
                        severity="critical",
                        status="fail",
                        file_ref=f"line ~{line}",
                        detail="测试函数似乎缺少 assert 断言",
                        risk="无断言的测试无法验证功能正确性",
                        fix="添加有明确失败信息的 assert 语句",
                    )

    def _check_test_isolation(self) -> None:
        """检查测试隔离性。"""
        # 检测全局状态修改
        isolation_patterns = [
            (r"globals\(\)\[", "测试中修改全局变量 (测试隔离性问题)"),
            (r"os\.environ\[", "测试中修改环境变量 (可能影响其他测试)"),
            (r"(?:monkeypatch|mock|unittest\.mock)", "使用 mock (确认 mock 已正确还原)"),
        ]
        for pattern, detail in isolation_patterns:
            for match in re.finditer(pattern, self.diff):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="test-isolation",
                    question="测试是否可重复且独立？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="非隔离测试可能导致测试结果不稳定",
                    fix="使用 setUp/tearDown 或 fixture 确保状态清理",
                )
