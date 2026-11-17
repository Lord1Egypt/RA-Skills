#!/usr/bin/env python3
"""Check a competitive-intelligence report for minimum delivery evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


REQUIRED_CONCEPTS = {
    "research date": (r"\b20\d{2}-\d{2}-\d{2}\b",),
    "sources": (r"https?://", r"\[[^]]+\]\(https?://"),
    "confidence": (r"\bconfidence\b", r"置信度"),
    "limitations": (r"\blimitations?\b", r"局限", r"证据缺口", r"未知"),
    "recommendations": (r"\brecommendations?\b", r"建议"),
}


def validate(text: str) -> list[str]:
    failures = []
    for concept, patterns in REQUIRED_CONCEPTS.items():
        if not any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            failures.append(f"missing {concept}")
    if len(re.findall(r"https?://", text)) < 2:
        failures.append("fewer than two source URLs")
    if not re.search(r"\b(inference|unknown)\b|推断|未知|未找到", text, flags=re.IGNORECASE):
        failures.append("facts are not distinguished from inference or unknowns")
    return failures


def validate_structured(report: dict[str, Any]) -> list[str]:
    failures = []
    evidence = report.get("evidence") or []
    findings = report.get("findings") or []
    evidence_ids = {item.get("evidence_id") for item in evidence}
    if not report.get("research_date"):
        failures.append("missing research date")
    if not evidence:
        failures.append("missing evidence")
    for item in evidence:
        content = item.get("content") or {}
        source = item.get("source") or {}
        if not content.get("raw_path") or not content.get("sha256"):
            failures.append(f'incomplete evidence trace: {item.get("evidence_id")}')
        if not source.get("url") and not source.get("query"):
            failures.append(f'missing evidence source: {item.get("evidence_id")}')
    for finding in findings:
        linked = set(finding.get("evidence_ids") or [])
        if not linked:
            failures.append(f'finding has no evidence: {finding.get("finding_id")}')
        dangling = linked - evidence_ids
        if dangling:
            failures.append(f'finding has dangling evidence: {finding.get("finding_id")}: {sorted(dangling)}')
        if finding.get("confidence") not in {"high", "medium", "low"}:
            failures.append(f'finding has invalid confidence: {finding.get("finding_id")}')
        for field in ("fact", "inference", "recommendation", "priority"):
            if not finding.get(field):
                failures.append(f'finding is missing {field}: {finding.get("finding_id")}')
    if report.get("status") != "complete":
        failures.append("report analysis is not complete")
    elif not findings:
        failures.append("complete report has no findings")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    text = args.report.read_text(encoding="utf-8")
    failures = validate_structured(json.loads(text)) if args.report.suffix.lower() == ".json" else validate(text)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("OK: report passes minimum competitive-intelligence checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
