#!/usr/bin/env python3
"""
ClawShield Lite — Security scanner for AI skill code.
Reads code from stdin, scans for risky patterns, and outputs a JSON risk report.
"""

import json
import sys
import os


def load_rules(rules_path: str = None) -> dict:
    """Load pattern rules from rules.json."""
    if rules_path is None:
        rules_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.json")
    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": "rules.json not found"}), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"error": "rules.json contains invalid JSON"}), file=sys.stderr)
        sys.exit(1)


def scan_code(code: str, rules: dict) -> dict:
    """
    Scan the provided code string against loaded rules.
    Returns a report dict with risk_level and a list of issues.
    """
    issues: list[dict] = []

    # Check dangerous patterns (severity: high)
    for pattern, explanation in rules.get("dangerous", {}).items():
        if pattern in code:
            issues.append({
                "pattern": pattern,
                "severity": "high",
                "explanation": explanation,
            })

    # Check suspicious patterns (severity: medium)
    for pattern, explanation in rules.get("suspicious", {}).items():
        if pattern in code:
            issues.append({
                "pattern": pattern,
                "severity": "medium",
                "explanation": explanation,
            })

    # Determine overall risk level
    high_count = sum(1 for i in issues if i["severity"] == "high")
    total = len(issues)

    if total == 0:
        risk_level = "SAFE"
    elif high_count >= 3 or total >= 3:
        risk_level = "HIGH RISK"
    else:
        risk_level = "MEDIUM RISK"

    return {"risk_level": risk_level, "issues": issues}


def main() -> None:
    """Entry point — read stdin, scan, and print JSON report."""
    if sys.stdin.isatty():
        print(
            json.dumps({"error": "No input provided. Pipe code via stdin."}),
            file=sys.stderr,
        )
        sys.exit(1)

    code = sys.stdin.read()
    if not code.strip():
        print(
            json.dumps({"error": "Empty input received."}),
            file=sys.stderr,
        )
        sys.exit(1)

    rules = load_rules()
    report = scan_code(code, rules)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
