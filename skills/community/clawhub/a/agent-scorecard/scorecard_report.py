#!/usr/bin/env python3
"""
Agent Scorecard — Report Generation
=====================================
Generate markdown or JSON reports from evaluation results and history.

Usage:
    from scorecard_report import Reporter
    reporter = Reporter(config)
    md = reporter.single_report(eval_result)
    md = reporter.history_report(tracker, last_n=20)

CLI:
    python3 scorecard_report.py --config scorecard_config.json --history scorecard_history.jsonl
    python3 scorecard_report.py --config scorecard_config.json --result result.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _load_config(path: str) -> Any:
    """Load configuration from a JSON file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config not found: {path}")
    if not path.endswith(".json"):
        raise ValueError(f"Config must be a .json file: {path}")
    if os.path.getsize(path) > 1_000_000:
        raise ValueError(f"Config file too large (>1MB): {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _get(cfg: Any, name: str, default: Any = None) -> Any:
    if isinstance(cfg, dict):
        return cfg.get(name, default)
    return getattr(cfg, name, default)


class Reporter:
    """Generate evaluation reports."""

    def __init__(self, config: Any):
        self.include_details = _get(config, "INCLUDE_CHECK_DETAILS", True)
        self.include_rubric = _get(config, "INCLUDE_RUBRIC", True)
        self.include_sparklines = _get(config, "INCLUDE_TREND_SPARKLINES", True)
        self.output_dir = _get(config, "REPORT_OUTPUT_DIR", "reports")
        self.precision = _get(config, "SCORE_PRECISION", 2)
        self.dimensions_cfg = {
            d["name"]: d for d in _get(config, "DIMENSIONS", [])
        }

    def single_report_md(self, result: dict) -> str:
        """Generate a markdown report for a single evaluation result dict."""
        lines: list[str] = []
        passed = result.get("overall_passed", False)
        score = result.get("overall_score", 0)

        lines.append("# Agent Scorecard — Evaluation Report")
        lines.append("")
        lines.append(f"**Date:** {result.get('timestamp', 'N/A')}")
        lines.append(f"**Agent:** {result.get('agent', 'N/A')}")
        lines.append(f"**Task Type:** {result.get('task_type', 'N/A')}")
        lines.append(f"**Text Length:** {result.get('text_length', 'N/A')} chars")
        lines.append(f"**Method:** {result.get('aggregate_method', 'N/A')}")
        lines.append("")
        lines.append(f"## Overall Score: {score}/5 {'✅ PASS' if passed else '❌ FAIL'}")
        lines.append("")

        lines.append("## Dimension Scores")
        lines.append("")
        lines.append("| Dimension | Score | Threshold | Status | Source |")
        lines.append("|-----------|-------|-----------|--------|--------|")

        for dim in result.get("dimensions", []):
            status = "✅" if dim.get("passed") else "❌"
            lines.append(
                f"| {dim.get('label', dim.get('name'))} "
                f"| {dim.get('score')}/5 "
                f"| {dim.get('threshold')} "
                f"| {status} "
                f"| {dim.get('source', 'N/A')} |"
            )

        lines.append("")

        # Detail sections
        if self.include_details:
            lines.append("## Automated Check Details")
            lines.append("")
            for dim in result.get("dimensions", []):
                details = dim.get("auto_details", {})
                if details:
                    lines.append(f"### {dim.get('label', dim.get('name'))}")
                    for check_name, info in details.items():
                        if isinstance(info, dict):
                            lines.append(f"- **{check_name}:** score={info.get('score')}, {info.get('detail')}")
                        else:
                            lines.append(f"- **{check_name}:** {info}")
                    lines.append("")

        if self.include_rubric:
            lines.append("## Rubric Reference")
            lines.append("")
            for dim in result.get("dimensions", []):
                name = dim.get("name")
                cfg = self.dimensions_cfg.get(name, {})
                rubric = cfg.get("rubric", {})
                if rubric:
                    lines.append(f"### {dim.get('label', name)}")
                    for level in sorted(rubric.keys()):
                        marker = "→" if level == round(dim.get("score", 0)) else " "
                        lines.append(f"  {marker} **{level}:** {rubric[level]}")
                    lines.append("")

        return "\n".join(lines)

    def history_report_md(self, records: List[dict], title: str = "History Report") -> str:
        """Generate a markdown report summarising multiple evaluations."""
        lines: list[str] = []
        lines.append(f"# Agent Scorecard — {title}")
        lines.append("")
        lines.append(f"**Evaluations:** {len(records)}")

        if not records:
            lines.append("\nNo records found.")
            return "\n".join(lines)

        # Overall stats
        overall_scores = [r["overall_score"] for r in records if "overall_score" in r]
        if overall_scores:
            mean = sum(overall_scores) / len(overall_scores)
            passed = sum(1 for r in records if r.get("overall_passed"))
            lines.append(f"**Mean Overall Score:** {mean:.{self.precision}f}/5")
            lines.append(f"**Pass Rate:** {passed}/{len(records)} ({100*passed/len(records):.0f}%)")
            lines.append("")

            if self.include_sparklines and len(overall_scores) > 1:
                lines.append(f"**Trend:** {self._sparkline(overall_scores)}")
                lines.append("")

        # Per-dimension summary
        dim_scores: Dict[str, List[float]] = {}
        for rec in records:
            for d in rec.get("dimensions", []):
                dim_scores.setdefault(d["name"], []).append(d["score"])

        if dim_scores:
            lines.append("## Per-Dimension Summary")
            lines.append("")
            lines.append("| Dimension | Mean | Min | Max | Trend |")
            lines.append("|-----------|------|-----|-----|-------|")
            for name, scores in dim_scores.items():
                mean = sum(scores) / len(scores)
                spark = self._sparkline(scores) if self.include_sparklines else ""
                lines.append(
                    f"| {name} | {mean:.{self.precision}f} "
                    f"| {min(scores):.1f} | {max(scores):.1f} | {spark} |"
                )
            lines.append("")

        # Recent evaluations table
        recent = records[-10:]
        lines.append("## Recent Evaluations")
        lines.append("")
        lines.append("| # | Date | Agent | Score | Status |")
        lines.append("|---|------|-------|-------|--------|")
        for i, rec in enumerate(recent, len(records) - len(recent) + 1):
            ts = rec.get("timestamp", "")[:19]
            status = "✅" if rec.get("overall_passed") else "❌"
            lines.append(
                f"| {i} | {ts} | {rec.get('agent', '')} "
                f"| {rec.get('overall_score', '')}/5 | {status} |"
            )
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _sparkline(values: List[float]) -> str:
        if not values:
            return ""
        blocks = " ▁▂▃▄▅▆▇█"
        mn, mx = min(values), max(values)
        rng = mx - mn if mx != mn else 1
        return "".join(
            blocks[min(len(blocks) - 1, int((v - mn) / rng * (len(blocks) - 1)))]
            for v in values
        )

    def save_report(self, content: str, filename: str) -> str:
        """Save report to output directory. Returns the file path."""
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path


# ── CLI ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Scorecard — report generation")
    parser.add_argument("--config", required=True, help="Path to config .json file")
    parser.add_argument("--result", default=None, help="Single result JSON file")
    parser.add_argument("--history", default=None, help="JSONL history file")
    parser.add_argument("--last", type=int, default=None, help="Use only last N records")
    parser.add_argument("--agent", default=None, help="Filter by agent")
    parser.add_argument("--task", default=None, help="Filter by task type")
    parser.add_argument("--output", default=None, help="Output file (default: stdout)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        cfg = _load_config(args.config)
    except Exception as exc:
        print(f"Error loading config: {exc}", file=sys.stderr)
        sys.exit(1)

    reporter = Reporter(cfg)

    if args.result:
        try:
            with open(args.result, "r", encoding="utf-8") as f:
                result = json.load(f)
        except Exception as exc:
            print(f"Error reading result: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.format == "json":
            content = json.dumps(result, indent=2)
        else:
            content = reporter.single_report_md(result)

    elif args.history:
        records: list[dict] = []
        try:
            with open(args.history, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            records.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except Exception as exc:
            print(f"Error reading history: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.agent:
            records = [r for r in records if r.get("agent") == args.agent]
        if args.task:
            records = [r for r in records if r.get("task_type") == args.task]
        if args.last:
            records = records[-args.last:]

        if args.format == "json":
            content = json.dumps(records, indent=2)
        else:
            content = reporter.history_report_md(records)
    else:
        parser.print_help()
        return

    if args.output:
        path = reporter.save_report(content, args.output)
        print(f"Report saved to {path}")
    else:
        print(content)


if __name__ == "__main__":
    main()
