"""功能正确性检查器 — 检测逻辑错误、边界条件、错误处理。"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class FunctionalChecker(BaseChecker):
    category = "functional"
    label = "功能正确性 (Functional)"
    severity = "critical"

    def run(self) -> list[CheckResult]:
        ext = self._get_file_extensions()
        code_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php"}
        if not ext & code_exts and ext:
            self._finding("func-skip", "功能检查", "critical", "skipped",
                          detail="非代码文件，跳过功能检查")
            return [self._result(self.label)]

        self._check_exception_handling()
        self._check_boundary_conditions()
        self._check_concurrency()
        self._check_return_values()

        return [self._result(self.label)]

    def _check_exception_handling(self) -> None:
        """检查错误处理是否完善。"""
        # 裸 except 块
        for match in re.finditer(r"except\s*:", self.diff):
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="func-except",
                question="错误处理是否完善？",
                severity="critical",
                status="fail",
                file_ref=f"line ~{line}",
                detail="裸 except 语句（会捕获 KeyboardInterrupt 等系统异常）",
                risk="可能隐藏非预期异常，导致调试困难",
                fix="捕获具体异常类型: except SpecificError as e:",
            )

        # try 块内无 except
        try_blocks = re.finditer(r"^\+\s*try\s*:", self.diff, re.MULTILINE)
        for match in try_blocks:
            # 简单启发式：检查后续 10 行内是否有 except
            after = self.diff[match.end():match.end() + 500]
            if "except" not in after:
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="func-except",
                    question="错误处理是否完善？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail="try 块似乎缺少 except 子句",
                    risk="异常未被捕获，可能导致程序崩溃",
                    fix="添加 except 块处理预期异常",
                )

        # pass 在 except 块中 (吞掉异常)
        for match in re.finditer(r"except[^:]*:\s*\n\s*pass", self.diff):
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="func-except",
                question="错误处理是否完善？",
                severity="critical",
                status="fail",
                file_ref=f"line ~{line}",
                detail="except 块中只写 pass，吞掉了异常",
                risk="异常被静默忽略，导致后续逻辑基于错误状态运行",
                fix="至少记录日志: except SomeError as e: logger.error(f'...: {e}')",
            )

    def _check_boundary_conditions(self) -> None:
        """检查边界条件处理。"""
        # 只检查新增代码行（+ 开头），排除 diff 头部的文件路径
        for match in re.finditer(r"^\+\s*(\w+)\[(\d+)\]", self.diff, re.MULTILINE):
            if int(match.group(2)) == 0:
                continue  # 索引 0 通常是安全的
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="func-boundary",
                question="边界条件是否已处理？",
                severity="critical",
                status="fail",
                file_ref=f"line ~{line}",
                detail=f"硬编码索引访问 {match.group(1)}[{match.group(2)}]，无越界检查",
                risk="可能导致 IndexError/ArrayIndexOutOfBounds",
                fix="使用 .get() (dict) 或在访问前检查 len()",
            )

        # 除法无零检查 — 仅匹配新增代码行
        for match in re.finditer(r"^\+\s*.*(\w+)\s*/\s*\w+", self.diff, re.MULTILINE):
            # 排除注释行和 diff 头
            line_text = match.group(0)
            if line_text.startswith("+++") or line_text.startswith("---"):
                continue
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="func-boundary",
                question="边界条件是否已处理？",
                severity="critical",
                status="fail",
                file_ref=f"line ~{line}",
                detail=f"除法运算可能除零: {match.group(0).strip('+ ')[:60]}",
                risk="可能导致 ZeroDivisionError",
                fix="在除法前检查分母不为零",
            )

    def _check_concurrency(self) -> None:
        """检查并发问题。"""
        # 检测未加锁的共享变量修改
        thread_patterns = [
            (r"threading\.(?:Thread|start)", "创建线程", "确认共享资源已加锁"),
            (r"(?:asyncio\.)?Lock\(\)", "使用了 Lock", "确认锁作用域正确，无死锁风险"),
        ]
        for pattern, detail, fix in thread_patterns:
            for match in re.finditer(pattern, self.diff):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="func-concurrent",
                    question="并发问题是否已考虑？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="并发问题可能导致数据竞态或死锁",
                    fix=fix,
                )

    def _check_return_values(self) -> None:
        """检查返回值一致性。"""
        # 函数可能返回 None 但调用者未检查
        patterns = [
            (r"(\.get\(|\.pop\()", "调用 .get()/.pop() 的返回值可能为 None"),
        ]
        for pattern, detail in patterns:
            for match in re.finditer(pattern, self.diff):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="func-return",
                    question="返回值是否被正确处理？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="None 值传入下游逻辑可能导致 AttributeError",
                    fix="在使用返回值前检查 is not None",
                )
