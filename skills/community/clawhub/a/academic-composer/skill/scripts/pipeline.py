#!/usr/bin/env python3
"""
Academic Composer — writing style analysis engine.

Runs local quantitative analysis on essay text using bundled measure.py,
which scores 24 AI stylistic patterns, syntactic complexity (MDD/ADD),
and semantic density (TTR, content-word ratio) against human-corpus baselines.

Style analysis scripts run locally and do not call external services.
Essay text is passed via file path or stdin to avoid exposing content
in process listings or shell history.

Usage:
  python pipeline.py --file essay.txt [--json]
  echo "ESSAY TEXT" | python pipeline.py --stdin [--max-iters 3] [--json]
  python pipeline.py --file essay.txt --measure-only --json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

_MEASURE_SCRIPT = Path(__file__).parent / "measure.py"


def run_measurement(essay_text: str) -> Dict[str, Any]:
    """Run measure.py, passing essay via stdin to avoid CLI arg exposure."""
    if not _MEASURE_SCRIPT.exists():
        raise FileNotFoundError(
            f"measure.py not found at {_MEASURE_SCRIPT}. "
            "Ensure the academic-composer skill is installed correctly."
        )
    result = subprocess.run(
        [sys.executable, str(_MEASURE_SCRIPT), "--stdin", "--json"],
        input=essay_text,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"measure.py error: {result.stderr.strip()}")
    return json.loads(result.stdout)


def build_style_feedback(report: Dict[str, Any], pass_num: int) -> str:
    issues = report.get("top_issues", [])
    mdd = report.get("mdd_mean", 0)
    ttr = report.get("ttr", 0)
    score = report.get("ai_pattern_score", 0)

    lines = [f"[PASS {pass_num}] Style quality score: {score:.1f}/100 (target <= 15)"]

    if pass_num == 1:
        if issues:
            lines.append("Priority fixes:")
            for iss in issues[:4]:
                lines.append(f"  - {iss}")
    elif pass_num == 2:
        lines.append(f"MDD mean: {mdd:.2f} (human baseline: 2.4-3.1)")
        if mdd > 3.1:
            lines.append("  -> Shorten sentence dependency chains; break up long noun phrases.")
        elif mdd < 2.4:
            lines.append("  -> Add some complex sentences for variety.")
        if issues:
            lines.append("Remaining pattern issues:")
            for iss in issues[:3]:
                lines.append(f"  - {iss}")
    else:
        lines.append(f"TTR: {ttr:.2f} (human baseline: 0.50-0.70)")
        if ttr < 0.50:
            lines.append("  -> Increase vocabulary variety; avoid repeating the same key terms.")
        if issues:
            lines.append("Remaining issues:")
            for iss in issues[:2]:
                lines.append(f"  - {iss}")

    lines.append("\nIMPORTANT: Do NOT alter any in-text citations or reference list entries.")
    return "\n".join(lines)


def run_style_review(
    essay: str,
    max_passes: int = 3,
    score_threshold: float = 15.0,
) -> Dict[str, Any]:
    history: List[Dict[str, Any]] = []

    for i in range(1, max_passes + 1):
        report = run_measurement(essay)
        record = {
            "pass": i,
            "ai_pattern_score": report.get("ai_pattern_score"),
            "mdd_mean": report.get("mdd_mean"),
            "mdd_variance": report.get("mdd_variance"),
            "ttr": report.get("ttr"),
            "passes": report.get("passes", False),
            "top_issues": report.get("top_issues", []),
        }
        history.append(record)

        print(f"[PASS {i}] Style score: {record['ai_pattern_score']}/100", file=sys.stderr)

        if report.get("passes", False):
            return {
                "final_essay": essay,
                "history": history,
                "converged": True,
                "total_passes": i,
            }

        feedback = build_style_feedback(report, i)
        return {
            "final_essay": essay,
            "history": history,
            "converged": False,
            "total_passes": i,
            "pending_feedback": feedback,
        }

    return {
        "final_essay": essay,
        "history": history,
        "converged": False,
        "total_passes": max_passes,
    }


def format_style_table(result: Dict[str, Any]) -> str:
    lines = [
        "| Pass | Style Score | MDD Mean | MDD Var | TTR  | Status |",
        "|------|-------------|----------|---------|------|--------|",
    ]
    for rec in result["history"]:
        p = rec.get("pass", "?")
        sc = f"{rec['ai_pattern_score']:.1f}" if isinstance(rec.get("ai_pattern_score"), float) else "N/A"
        mdd = f"{rec['mdd_mean']:.2f}" if isinstance(rec.get("mdd_mean"), float) else "N/A"
        var = f"{rec['mdd_variance']:.2f}" if isinstance(rec.get("mdd_variance"), float) else "N/A"
        ttr = f"{rec['ttr']:.2f}" if isinstance(rec.get("ttr"), float) else "N/A"
        status = "PASS" if rec.get("passes") else "FAIL"
        lines.append(f"| {p:>4} | {sc:>11} | {mdd:>8} | {var:>7} | {ttr:>4} | {status:>6} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Academic Composer — local writing style analysis (no external services)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to essay text file")
    group.add_argument("--stdin", action="store_true", help="Read essay from stdin (avoids CLI arg exposure)")
    parser.add_argument("--max-iters", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=15.0)
    parser.add_argument("--measure-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    if args.measure_only:
        report = run_measurement(text)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(f"Style score : {report.get('ai_pattern_score', 'N/A')}/100")
            print(f"MDD mean    : {report.get('mdd_mean', 'N/A')}")
            print(f"TTR         : {report.get('ttr', 'N/A')}")
            print(f"Passes      : {report.get('passes', False)}")
        return

    result = run_style_review(essay=text, max_passes=args.max_iters, score_threshold=args.threshold)

    if args.json:
        summary = {k: v for k, v in result.items() if k != "final_essay"}
        summary["final_essay_length"] = len(result["final_essay"])
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(format_style_table(result))
        if result.get("pending_feedback"):
            print(f"\n{result['pending_feedback']}")


if __name__ == "__main__":
    main()
