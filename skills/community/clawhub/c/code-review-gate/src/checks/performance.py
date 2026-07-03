"""性能检查器 — 检测复杂度、资源泄漏、效率问题。"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class PerformanceChecker(BaseChecker):
    category = "performance"
    label = "性能 (Performance)"
    severity = "important"

    def run(self) -> list[CheckResult]:
        ext = self._get_file_extensions()
        code_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php"}
        if not ext & code_exts and ext:
            self._finding("perf-skip", "性能检查", "important", "skipped",
                          detail="非代码文件，跳过性能检查")
            return [self._result(self.label)]

        self._check_quadratic_complexity()
        self._check_n_plus_1()
        self._check_regex_backtracking()
        self._check_resource_leaks()
        self._check_large_collections()

        return [self._result(self.label)]

    def _check_quadratic_complexity(self) -> None:
        """检测嵌套循环 (O(n²) 风险)。"""
        lines = self.diff.split("\n")
        in_loop_depth = 0
        for i, line in enumerate(lines):
            if not line.startswith("+"):
                continue
            stripped = line[1:].strip()
            if re.match(r"(for|while)\s+", stripped):
                in_loop_depth += 1
                if in_loop_depth >= 2:
                    self._finding(
                        check_id="perf-complexity",
                        question="是否存在 O(n²) 或更高级别复杂度？",
                        severity="important",
                        status="fail",
                        file_ref=f"line ~{i + 1}",
                        detail="检测到嵌套循环 (可能的 O(n²) 复杂度)",
                        risk="大数据量时性能严重退化",
                        fix="考虑使用哈希表、排序后双指针或分批处理",
                    )
            if in_loop_depth > 0 and stripped == "":
                pass  # 循环体可能结束
            # 简单启发式：缩进减少表示循环结束
            if stripped != "" and not stripped.startswith((" ", "\t")) and in_loop_depth > 0:
                # 不是精确检测，简化处理
                pass

    def _check_n_plus_1(self) -> None:
        """检测 N+1 查询模式。"""
        patterns = [
            (r"for\s+\w+\s+in\s+.+:\s*\n\s*\w+\.(?:filter|get|query|execute)", "循环内数据库查询 (N+1 问题)"),
            (r"\.map\(.*\.(?:fetch|query|find)", "map 内查询调用 (N+1 问题)"),
            (r"forEach.*\.(?:find|findOne|query)", "forEach 内查询调用 (N+1 问题)"),
        ]
        for pattern, detail in patterns:
            for match in re.finditer(pattern, self.diff, re.MULTILINE | re.DOTALL):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="perf-n1",
                    question="是否存在 N+1 查询问题？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="数据库查询次数随数据量线性增长",
                    fix="使用 JOIN、批量查询或预加载 (eager loading)",
                )

    def _check_regex_backtracking(self) -> None:
        """检测灾难性回溯的正则模式。"""
        dangerous = [
            (r"\(\.\*\)\+", "(. *)+ 模式 (灾难性回溯风险)"),
            (r"\(\.\+\)\+", "(.+)+ 模式 (灾难性回溯风险)"),
            (r"\(\?:\.\|[\s\S]\)\*", "嵌套量词 (灾难性回溯风险)"),
        ]
        for pattern, detail in dangerous:
            for match in re.finditer(pattern, self.diff):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="perf-regex",
                    question="正则表达式是否安全？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="恶意输入可导致 CPU 100% (ReDoS 攻击)",
                    fix="重写正则，避免嵌套量词；或使用非回溯引擎如 re2",
                )

    def _check_resource_leaks(self) -> None:
        """检测资源泄漏（文件、连接等未关闭）。"""
        for match in re.finditer(r"open\([^)]+\)(?!.*with)", self.diff):
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="perf-resource",
                question="资源使用是否高效？",
                severity="important",
                status="fail",
                file_ref=f"line ~{line}",
                detail="open() 未使用 with 语句 (文件可能未关闭)",
                risk="文件句柄泄漏，长时间运行可耗尽系统资源",
                fix="使用 with open(...) as f: 确保自动关闭",
            )

    def _check_large_collections(self) -> None:
        """检测大数据量场景下的内存问题。"""
        patterns = [
            (r"\.(?:readlines|read)\(\)", "读取整个文件到内存", "如有大文件风险，使用迭代器逐行读取"),
            (r"list\(.*\.keys\(\)\)", "list(.keys()) 创建完整列表", "直接迭代 .keys() 或使用生成器"),
        ]
        for pattern, detail, fix in patterns:
            for match in re.finditer(pattern, self.diff):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="perf-memory",
                    question="大数据量下内存使用是否可控？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="大文件/大数据量可能导致 OOM",
                    fix=fix,
                )
