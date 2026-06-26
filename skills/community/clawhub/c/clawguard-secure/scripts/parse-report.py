#!/usr/bin/env python3
"""
ClawGuard report parser — extracts key statistics from an exported JSON report.
Reduces token usage by summarizing large reports before loading into context.

Usage:
    python3 parse-report.py <path-to-report.json>
"""

import json
import sys
from collections import Counter
from pathlib import Path


def parse_report(path: str) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"Error: Cannot read file: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON file. Check that the file is valid JSON.", file=sys.stderr)
        sys.exit(1)

    # Normalize camelCase / snake_case
    findings = data.get("findings", [])
    score = data.get("score", 0)
    scan_level = data.get("scan_level") or data.get("scanLevel", "unknown")
    created_at = data.get("created_at") or data.get("createdAt", "unknown")
    rulepack_version = data.get("rulepack_version") or data.get("rulesVersion", "unknown")

    # Severity breakdown
    sev_fail = Counter()
    sev_warn = Counter()
    sev_pass = Counter()
    category_counts = data.get("category_summary") or data.get("categorySummary", {})
    statuses = Counter()

    for f in findings:
        sev = f.get("severity", "UNKNOWN")
        status = f.get("status", "unknown")
        statuses[status] += 1
        if status == "fail":
            sev_fail[sev] += 1
        elif status == "warn":
            sev_warn[sev] += 1
        elif status == "pass":
            sev_pass[sev] += 1

    # Immediate attention: fail + CRITICAL/HIGH
    urgent = [
        {"rule_id": f.get("rule_id") or f.get("ruleId"), "title": f.get("title"), "severity": f.get("severity")}
        for f in findings
        if f.get("status") == "fail" and f.get("severity") in ("CRITICAL", "HIGH")
    ]

    # Grade
    grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 60 else "D" if score >= 40 else "F"

    return {
        "score": score,
        "grade": grade,
        "scan_level": scan_level,
        "created_at": created_at,
        "rulepack_version": rulepack_version,
        "total_findings": len(findings),
        "status_counts": dict(statuses),
        "severity_fail": dict(sev_fail),
        "severity_warn": dict(sev_warn),
        "severity_pass": dict(sev_pass),
        "category_counts": dict(category_counts),
        "urgent": urgent,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <report.json>", file=sys.stderr)
        sys.exit(1)
    result = parse_report(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
