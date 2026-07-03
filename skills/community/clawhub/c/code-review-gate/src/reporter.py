"""报告生成器 — 将检查结果格式化为可读报告。"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.models import CheckResult, Finding, Severity


_SEVERITY_ICON: dict[Severity, str] = {
    "critical": "🔴",
    "important": "🟡",
    "minor": "⚪",
}
_SEVERITY_LABEL: dict[Severity, str] = {
    "critical": "Critical",
    "important": "Important",
    "minor": "Minor",
}
_SEVERITY_ORDER: dict[Severity, int] = {
    "critical": 0, "important": 1, "minor": 2
}


class Reporter:
    """将审查结果渲染为终端 / Markdown / JSON 格式。"""

    def __init__(
        self,
        results: list[CheckResult],
        base: str | None,
        head: str | None,
        files: list[str] | None,
        diff_stats: str,
        design_path: str | None,
        severity: str = "important",
    ):
        self.results = results
        self.base = base
        self.head = head
        self.files = files
        self.diff_stats = diff_stats
        self.design_path = design_path
        self.severity = severity
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def generate(self, fmt: str = "terminal") -> str:
        if fmt == "json":
            return self._json()
        if fmt == "markdown":
            return self._markdown()
        return self._terminal()

    def _group_findings(self) -> dict[Severity, list[Finding]]:
        grouped: dict[Severity, list[Finding]] = {
            "critical": [], "important": [], "minor": []
        }
        for r in self.results:
            for f in r.findings:
                if f.status == "fail":
                    grouped[f.severity].append(f)
        return grouped

    def _terminal(self) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("  CODE REVIEW GATE — 代码审查门禁")
        lines.append("=" * 60)
        lines.append(f"  Time:    {self.timestamp}")
        if self.base and self.head:
            lines.append(f"  Range:   {self.base}..{self.head}")
        if self.files:
            lines.append(f"  Files:   {', '.join(self.files)}")
        if self.design_path:
            lines.append(f"  Design:  {self.design_path}")
        lines.append(f"  Diff:    {self.diff_stats if self.diff_stats else '(no stats)'}")
        lines.append("")

        # 汇总
        total = sum(len(r.findings) for r in self.results)
        fail = sum(1 for r in self.results for f in r.findings if f.status == "fail")
        lines.append(f"  Checks:  {len(self.results)} dimensions | {total} items | {fail} issues found")
        lines.append("")

        # 各维度结果
        for r in self.results:
            icon = "PASS" if r.status == "pass" else "FAIL"
            lines.append(f"  [{icon}] {r.label}")

        lines.append("")
        lines.append("-" * 60)

        # 分级问题
        grouped = self._group_findings()
        for severity in ["critical", "important", "minor"]:
            findings = grouped[severity]  # type: ignore
            if not findings:
                continue
            icon = _SEVERITY_ICON[severity]  # type: ignore
            label = _SEVERITY_LABEL[severity]  # type: ignore
            lines.append(f"\n  {icon} {label} ({len(findings)} issues)")
            lines.append(f"  {'─' * 50}")
            for i, f in enumerate(findings, 1):
                lines.append(f"  {i}. {f.detail or f.question}")
                if f.file_ref:
                    lines.append(f"     File: {f.file_ref}")
                if f.risk:
                    lines.append(f"     Risk: {f.risk}")
                if f.fix:
                    lines.append(f"     Fix:  {f.fix}")
                lines.append("")

        # 裁决
        lines.append("=" * 60)
        critical_count = len(grouped["critical"])
        if critical_count > 0:
            lines.append(f"  GATE: BLOCKED — {critical_count} critical issue(s)")
            lines.append(f"  Fix critical issues before proceeding.")
        else:
            lines.append(f"  GATE: PASSED")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _markdown(self) -> str:
        lines = []
        lines.append(f"## Code Review Report — {self.timestamp}")
        lines.append("")
        lines.append(f"**Range:** {self.base or 'N/A'}..{self.head or 'N/A'}  ")
        if self.diff_stats:
            lines.append(f"**Diff:** {self.diff_stats}  ")
        if self.design_path:
            lines.append(f"**Design:** {self.design_path}  ")
        lines.append("")

        # 汇总表
        lines.append("### Results Summary")
        lines.append("")
        lines.append("| Dimension | Status | Issues |")
        lines.append("|-----------|--------|--------|")
        for r in self.results:
            fail_count = sum(1 for f in r.findings if f.status == "fail")
            status = "PASS" if r.status == "pass" else "FAIL"
            lines.append(f"| {r.label} | {status} | {fail_count} |")
        lines.append("")

        # 分级问题
        grouped = self._group_findings()
        for severity in ["critical", "important", "minor"]:
            findings = grouped[severity]  # type: ignore
            if not findings:
                continue
            icon = _SEVERITY_ICON[severity]  # type: ignore
            label = _SEVERITY_LABEL[severity]  # type: ignore
            lines.append(f"### {icon} {label} ({len(findings)} issues)")
            lines.append("")
            for i, f in enumerate(findings, 1):
                lines.append(f"**{i}. {f.detail or f.question}**")
                if f.file_ref:
                    lines.append(f"- File: `{f.file_ref}`")
                if f.risk:
                    lines.append(f"- Risk: {f.risk}")
                if f.fix:
                    lines.append(f"- Fix: {f.fix}")
                lines.append("")

        # 裁决
        critical_count = len(grouped["critical"])
        if critical_count > 0:
            lines.append(f"### Assessment: BLOCKED ({critical_count} critical)")
        else:
            lines.append("### Assessment: PASSED")

        return "\n".join(lines)

    def _json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp,
            "base": self.base,
            "head": self.head,
            "diff_stats": self.diff_stats,
            "results": [
                {
                    "category": r.category,
                    "label": r.label,
                    "status": r.status,
                    "findings": [
                        {
                            "check_id": f.check_id,
                            "severity": f.severity,
                            "status": f.status,
                            "file_ref": f.file_ref,
                            "detail": f.detail,
                            "risk": f.risk,
                            "fix": f.fix,
                        }
                        for f in r.findings
                    ],
                }
                for r in self.results
            ],
            "blocked": len(self._group_findings()["critical"]) > 0,
        }, indent=2, ensure_ascii=False)
