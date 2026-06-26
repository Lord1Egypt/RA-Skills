#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
WORKSPACE = SKILL_ROOT.parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from lib.audit import (  # noqa: E402
    ai_review,
    analyze_target,
    build_report,
    build_text_target,
    combine_results,
    fetch_url,
    load_file,
    load_policy,
    reports_dir,
    write_report,
)


def _target_from_args(args: argparse.Namespace, policy: dict) -> object:
    max_chars = int(policy.get("size_limits", {}).get("max_text_chars", 30000))
    if args.command == "scan-url":
        return fetch_url(args.url, max_chars)
    if args.command == "scan-file":
        return load_file(Path(args.path).resolve(), max_chars)
    return build_text_target(args.title or "inline-text", args.text, source="inline")


def print_summary(report: dict, report_path: Path) -> None:
    decision = report["decision"]
    print("=" * 72)
    print(f"[{decision['recommendation']}] {report['target']['title']} | risk={decision['risk_score']}")
    print(report["summary"]["summary"])
    metrics = report["static_analysis"]["metrics"]
    print(
        "metrics: "
        f"words={metrics['word_count']} "
        f"brand_mentions={metrics['brand_mentions']} "
        f"brand_density={metrics['brand_density_per_1k_words']} "
        f"domain_status={metrics['domain_status']}"
    )
    signals = report["static_analysis"].get("signals", [])
    if signals:
        print("signals:")
        for signal in signals[:8]:
            evidence = "; ".join(signal.get("evidence", [])[:3])
            print(f"- {signal['id']}: {signal['summary']} :: {evidence}")
    ai = report.get("ai_review") or {}
    if ai.get("summary"):
        print(f"ai: {ai['summary']}")
    print(f"report: {report_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect GEO / SEO soft articles and recommendation pollution")
    parser.add_argument("--policy", help="Custom policy path")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--with-ai", action="store_true", help="Enable optional AI review for the target")

    subparsers = parser.add_subparsers(dest="command", required=True)

    url_parser = subparsers.add_parser("scan-url", help="Scan a URL")
    url_parser.add_argument("url")

    file_parser = subparsers.add_parser("scan-file", help="Scan a local file")
    file_parser.add_argument("path")

    text_parser = subparsers.add_parser("scan-text", help="Scan raw text")
    text_parser.add_argument("--title", default="inline-text")
    text_parser.add_argument("--text", required=True)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    policy = load_policy(SKILL_ROOT, args.policy)
    target = _target_from_args(args, policy)
    static_result = analyze_target(target, policy)
    ai_result = ai_review(target, static_result) if args.with_ai else None
    decision = combine_results(static_result, ai_result, policy)
    report = build_report(target, static_result, ai_result, decision, policy)
    report_path = write_report(report, reports_dir(policy, WORKSPACE))

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_summary(report, report_path)

    return 1 if decision["recommendation"] == "BLOCK" else 0


if __name__ == "__main__":
    sys.exit(main())
