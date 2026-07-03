"""Code Review Gate — 代码审查门禁核心引擎。

扫描 git diff，按 7 个维度执行静态分析，输出结构化审查报告。

用法:
    python gate.py --base HEAD~1 --head HEAD
    python gate.py --files "src/api/*.py" --design design.md
    python gate.py --base main --head feature-x --format json
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

# 确保从 skills 根目录运行时也能找到模块
_sys_path_root = str(Path(__file__).resolve().parent.parent)
if _sys_path_root not in sys.path:
    sys.path.insert(0, _sys_path_root)

from src.checks import (
    FunctionalChecker,
    SecurityChecker,
    PerformanceChecker,
    ReadabilityChecker,
    MaintainabilityChecker,
    TestingChecker,
    DocumentationChecker,
)
from src.reporter import Reporter


class CodeReviewGate:
    """门禁主控制器：调度各维度检查器，汇总结果，决定通过/阻塞。"""

    CHECKERS = [
        FunctionalChecker,
        SecurityChecker,
        PerformanceChecker,
        ReadabilityChecker,
        MaintainabilityChecker,
        TestingChecker,
        DocumentationChecker,
    ]

    def __init__(
        self,
        base: str | None = None,
        head: str | None = None,
        files: list[str] | None = None,
        design_path: str | None = None,
        severity: str = "important",
        max_lines: int = 1000,
    ):
        self.base = base
        self.head = head
        self.files = files
        self.design_path = design_path
        self.severity = severity
        self.max_lines = max_lines

    def get_diff(self) -> str:
        """获取 git diff 内容。"""
        if self.files:
            # 审查当前工作区指定文件
            cmd = ["git", "diff", "--", *self.files]
        elif self.base and self.head:
            cmd = ["git", "diff", f"{self.base}..{self.head}"]
        else:
            # 默认审查未暂存的改动
            cmd = ["git", "diff"]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            print("Error: git diff timed out", file=sys.stderr)
            sys.exit(2)
        except FileNotFoundError:
            print("Error: git not found. Is git installed?", file=sys.stderr)
            sys.exit(2)

    def get_diff_stats(self) -> str:
        """获取 diff 统计信息。"""
        if self.files:
            cmd = ["git", "diff", "--stat", "--", *self.files]
        elif self.base and self.head:
            cmd = ["git", "diff", "--stat", f"{self.base}..{self.head}"]
        else:
            cmd = ["git", "diff", "--stat"]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
            )
            return result.stdout.strip()
        except Exception:
            return "(stats unavailable)"

    def load_design_doc(self) -> str | None:
        """加载设计文档内容。"""
        if not self.design_path:
            return None
        path = Path(self.design_path)
        if not path.exists():
            print(f"Warning: design doc not found at {self.design_path}", file=sys.stderr)
            return None
        return path.read_text(encoding="utf-8")

    def should_skip(self) -> bool:
        """判断是否应该跳过审查。"""
        diff = self.get_diff()
        if not diff.strip():
            print("No changes detected. Skipping review.")
            return True
        line_count = diff.count("\n")
        if line_count > self.max_lines:
            print(
                f"Diff too large ({line_count} lines > {self.max_lines} max). "
                "Please split into smaller changes or increase --max-lines.",
                file=sys.stderr,
            )
            return True
        return False

    def run(self) -> int:
        """执行门禁检查，返回退出码。"""
        if self.should_skip():
            return 3  # 跳过

        diff = self.get_diff()
        diff_stats = self.get_diff_stats()
        design_doc = self.load_design_doc()

        # 实例化检查器
        checkers = [
            cls(diff, diff_stats, design_doc)
            for cls in self.CHECKERS
        ]

        # 运行所有检查
        results = []
        for checker in checkers:
            results.extend(checker.run())

        # 生成报告
        reporter = Reporter(
            results=results,
            base=self.base,
            head=self.head,
            files=self.files,
            diff_stats=diff_stats,
            design_path=self.design_path,
            severity=self.severity,
        )
        report = reporter.generate()

        # 输出报告
        print(report)

        # 判断门禁结果
        critical_count = sum(
            1 for r in results
            if r.severity == "critical" and r.status == "fail"
        )
        if critical_count > 0:
            return 1  # 阻塞
        return 0  # 通过


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Code Review Gate — AI 代码审查门禁",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python gate.py --base HEAD~1 --head HEAD
  python gate.py --files "src/api/*.py" --design design.md --format json
  python gate.py --base main --head feature-x --severity critical
        """,
    )
    parser.add_argument("--base", help="Git diff 基准 commit/branch")
    parser.add_argument("--head", help="Git diff 目标 commit/branch")
    parser.add_argument("--files", nargs="*", help="限定审查的文件路径")
    parser.add_argument("--design", help="设计文档路径")
    parser.add_argument(
        "--severity",
        choices=["critical", "important", "minor"],
        default="important",
        help="最低报告级别 (默认: important)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "terminal"],
        default="terminal",
        help="输出格式 (默认: terminal)",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=1000,
        help="单次审查最大行数 (默认: 1000)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.base and not args.head and not args.files:
        print("Warning: No --base/--head or --files specified. Reviewing unstaged changes.")

    gate = CodeReviewGate(
        base=args.base,
        head=args.head,
        files=args.files,
        design_path=args.design,
        severity=args.severity,
        max_lines=args.max_lines,
    )
    exit_code = gate.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
