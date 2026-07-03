"""可读性检查器 — 命名规范、函数职责、注释质量。"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class ReadabilityChecker(BaseChecker):
    category = "readability"
    label = "可读性 (Readability)"
    severity = "important"

    # 不良命名模式
    BAD_NAME_PATTERNS = [
        (r"\b(tmp|temp|foo|bar|baz|xxx|test\d*)\b", "使用无意义变量名"),
        (r"\b(data|info|obj|thing|stuff)\b", "使用过于泛化的变量名"),
        (r"\b(a|b|c|x|y|z)\s*=", "单字母变量名（非迭代器上下文）"),
    ]

    def run(self) -> list[CheckResult]:
        ext = self._get_file_extensions()
        code_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php"}
        if not ext & code_exts and ext:
            self._finding("read-skip", "可读性检查", "important", "skipped",
                          detail="非代码文件，跳过可读性检查")
            return [self._result(self.label)]

        self._check_naming()
        self._check_function_length()
        self._check_commented_code()
        self._check_nesting_depth()

        return [self._result(self.label)]

    def _check_naming(self) -> None:
        """检查命名规范。"""
        for pattern, detail in self.BAD_NAME_PATTERNS:
            for match in re.finditer(pattern, self.diff):
                # 只对新增行 (+ ) 检查
                context_start = max(0, match.start() - 1)
                prefix = self.diff[context_start:match.start()]
                if not prefix.endswith("+"):
                    continue
                line = self.diff[:match.start()].count("\n") + 1
                name = match.group(0)
                self._finding(
                    check_id="read-name",
                    question="命名是否清晰有意义？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=f"{detail}: '{name}'",
                    risk="降低代码可读性和可维护性",
                    fix="使用描述性的名称，如 'user_id'、'config_path' 等",
                )

    def _check_function_length(self) -> None:
        """检查函数是否过长。"""
        lines = self.diff.split("\n")
        current_func_start = None
        func_line_count = 0
        in_func = False

        for i, line in enumerate(lines):
            if not line.startswith("+"):
                continue
            stripped = line[1:].strip()
            if re.match(r"^\s*def\s+", stripped):
                current_func_start = i + 1
                func_line_count = 0
                in_func = True
            elif in_func:
                func_line_count += 1
                if func_line_count > 100:
                    self._finding(
                        check_id="read-func-len",
                        question="函数/类职责是否单一？",
                        severity="important",
                        status="fail",
                        file_ref=f"line ~{current_func_start}",
                        detail=f"函数长度超过 100 行 (当前 {func_line_count}+ 行)",
                        risk="长函数难以理解、测试和维护",
                        fix="拆分为多个职责单一的小函数",
                    )
                    in_func = False  # 只报告一次

    def _check_commented_code(self) -> None:
        """检测被注释掉的代码。"""
        commented = re.finditer(
            r"^\+\s*(?:#|//|--|/\*)\s*(?:def|function|class|if|for|while|return|const|let|var|import)",
            self.diff, re.MULTILINE
        )
        for match in commented:
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="read-commented",
                question="代码是否简洁明了？",
                severity="minor",
                status="fail",
                file_ref=f"line ~{line}",
                detail="检测到被注释掉的代码块",
                risk="注释掉的代码会造成混淆，应在版本历史中查看",
                fix="删除注释掉的代码，依赖 Git 历史追溯",
            )

    def _check_nesting_depth(self) -> None:
        """检查嵌套深度。"""
        lines = self.diff.split("\n")
        for i, line in enumerate(lines):
            if not line.startswith("+"):
                continue
            indent = len(line[1:]) - len(line[1:].lstrip(" "))
            if indent >= 16:  # 4层缩进 (4 * 4)
                self._finding(
                    check_id="read-nesting",
                    question="代码是否简洁明了？",
                    severity="important",
                    status="fail",
                    file_ref=f"line ~{i + 1}",
                    detail=f"嵌套深度过深 (缩进 >= 16 字符, 约 {indent // 4} 层)",
                    risk="深层嵌套降低可读性",
                    fix="使用提前返回 (early return) 或提取子函数减少嵌套",
                )
                break  # 只报告第一处
