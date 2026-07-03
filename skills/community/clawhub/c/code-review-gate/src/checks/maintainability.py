"""可维护性检查器 — SOLID 原则、依赖管理、配置外部化、日志规范。"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class MaintainabilityChecker(BaseChecker):
    category = "maintainability"
    label = "可维护性 (Maintainability)"
    severity = "important"

    def run(self) -> list[CheckResult]:
        ext = self._get_file_extensions()
        code_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php"}
        if not ext & code_exts and ext:
            self._finding("maint-skip", "可维护性检查", "important", "skipped",
                          detail="非代码文件，跳过可维护性检查")
            return [self._result(self.label)]

        self._check_hardcoded_config()
        self._check_circular_dependency()
        self._check_logging()
        self._check_duplication()

        return [self._result(self.label)]

    def _check_hardcoded_config(self) -> None:
        """检测硬编码配置值。"""
        patterns = [
            (r"(?:host|port|url|endpoint)\s*=\s*[\"'](?:http|https|\d)", "URL/端点硬编码", "使用配置文件或环境变量"),
            (r"(?:timeout|retry|max_\w+|min_\w+)\s*=\s*\d+", "超时/阈值硬编码", "使用配置文件，便于调整"),
            (r"(?:path|dir|folder|directory)\s*=\s*[\"']/", "路径硬编码", "使用相对于项目根目录的路径或配置"),
        ]
        for pattern, detail, fix in patterns:
            for match in re.finditer(pattern, self.diff, re.IGNORECASE):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="maint-config",
                    question="配置是否外部化？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="硬编码值不利于环境切换和维护",
                    fix=fix,
                )

    def _check_circular_dependency(self) -> None:
        """检测可能的循环依赖。"""
        imported = set(re.findall(r"(?:from|import)\s+(\S+)", self.diff))
        if len(imported) > 0:
            # 简化：检查是否导入了自身模块
            files = self._parse_file_refs()
            for f in files:
                module_name = f.replace("/", ".").replace(".py", "").replace(".ts", "").replace(".js", "")
                for imp in imported:
                    if module_name.endswith(imp) or imp.endswith(module_name.split(".")[-1]):
                        if imp != module_name:
                            self._finding(
                                check_id="maint-circular",
                                question="依赖关系是否合理？",
                                severity="important",
                                status="fail",
                                file_ref=f,
                                detail=f"可能循环依赖: {f} 导入了模块 {imp}",
                                risk="循环依赖导致初始化错误和维护困难",
                                fix="重构代码，提取共享逻辑到独立模块",
                            )

    def _check_logging(self) -> None:
        """检查日志规范。"""
        # print 语句用于调试
        for match in re.finditer(r"print\([^)]*\)", self.diff):
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="maint-log",
                question="日志是否适当？",
                severity="important",
                status="fail",
                file_ref=f"line ~{line}",
                detail="使用 print() 而非 logging 模块",
                risk="print 无法分级、无法重定向、不适合生产环境",
                fix="使用 logging.debug() / .info() / .warning() / .error()",
            )

        # 敏感信息在日志中
        for match in re.finditer(
            r"(?:log|print)\(.*(?:password|secret|token|api_key|private)",
            self.diff, re.IGNORECASE
        ):
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="maint-log-secret",
                question="日志是否适当？",
                severity="critical",
                status="fail",
                file_ref=f"line ~{line}",
                detail="日志中可能包含敏感信息",
                risk="敏感信息泄露到日志文件",
                fix="对敏感字段做脱敏处理",
            )

    def _check_duplication(self) -> None:
        """检测重复代码块。"""
        # 简化启发式：连续 5 行以上相同内容
        lines = self.diff.split("\n")
        added_lines = [l[1:] for l in lines if l.startswith("+")]

        seen_blocks: dict[str, int] = {}
        for i in range(len(added_lines) - 3):
            block = "\n".join(added_lines[i:i + 5])
            if len(block) > 50:  # 忽略太短的块
                if block in seen_blocks and (i - seen_blocks[block]) > 5:
                    self._finding(
                        check_id="maint-duplicate",
                        question="是否存在重复代码？",
                        severity="important",
                        status="fail",
                        detail="检测到重复的代码块（可能违反 DRY 原则）",
                        risk="重复代码增加维护成本和 bug 风险",
                        fix="提取为公共函数或模块",
                    )
                    break
                seen_blocks[block] = i
