#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner for lint_research_output.py — validates test fixtures against
expected pass/fail outcomes.

Usage:
    python scripts/run_lint_tests.py

Exit code 0 = all tests passed; 1 = at least one test failed.
"""

import json
import sys
from pathlib import Path

# Ensure the lint module is importable
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from lint_research_output import lint_file, LintReport


# ── Test Cases ───────────────────────────────────────────────────────────────

TEST_CASES = [
    {
        "name": "valid-evidence-ledger",
        "file": "test-fixtures/valid-evidence-ledger.json",
        "expect_errors": False,
        "description": "Valid evidence ledger should produce zero errors",
    },
    {
        "name": "invalid-evidence-ledger",
        "file": "test-fixtures/invalid-evidence-ledger.json",
        "expect_errors": True,
        "min_errors": 5,
        "description": "Invalid ledger should catch duplicate ID, bad status, bad source_type, bad reliability, missing fields, confirmed_fact without source",
    },
    {
        "name": "valid-cycle-report",
        "file": "test-fixtures/valid-cycle-report.json",
        "expect_errors": False,
        "description": "Valid ResearchCycleReport with correct state transitions",
    },
    {
        "name": "invalid-state-machine",
        "file": "test-fixtures/invalid-state-machine.json",
        "expect_errors": True,
        "min_errors": 4,
        "description": "Should catch: accepted without passed, retrying without retry_patch, max_cycles not escalated, bad transition",
    },
    {
        "name": "valid-verification-report",
        "file": "test-fixtures/valid-verification-report.json",
        "expect_errors": False,
        "description": "Valid verification report with pass verdict and all dimensions passing",
    },
    {
        "name": "invalid-verification-report",
        "file": "test-fixtures/invalid-verification-report.json",
        "expect_errors": True,
        "min_errors": 2,
        "description": "Should catch: fail without retry_patch, evidence ID in both confirmed and rejected",
    },
    {
        "name": "valid-conflict-resolution",
        "file": "test-fixtures/valid-conflict-resolution.json",
        "expect_errors": False,
        "description": "Valid conflict resolution report with proper resolution strategies",
    },
    {
        "name": "valid-research-brief-md",
        "file": "test-fixtures/valid-research-brief.md",
        "expect_errors": False,
        "description": "Valid Markdown research brief with evidence IDs, confidence, evidence window, and reversal conditions",
    },
    {
        "name": "invalid-decision-brief-md",
        "file": "test-fixtures/invalid-decision-brief.md",
        "expect_errors": True,
        "min_errors": 1,
        "description": "Invalid Markdown decision brief: missing reversal conditions, empty phrases, no evidence IDs, no sources, no evidence window",
    },
]


# ── Runner ───────────────────────────────────────────────────────────────────


def run_tests() -> int:
    """Run all test cases and report results."""
    passed = 0
    failed = 0
    total = len(TEST_CASES)

    print(f"Running {total} lint test cases...\n")

    for tc in TEST_CASES:
        file_path = str(SCRIPT_DIR / tc["file"])

        # Ensure file exists
        if not Path(file_path).exists():
            print(f"  FAIL  {tc['name']}: fixture file not found: {file_path}")
            failed += 1
            continue

        report = lint_file(file_path)
        has_errors = report.has_errors

        # Check expectations
        ok = True
        reasons = []

        if tc["expect_errors"] and not has_errors:
            ok = False
            reasons.append("expected errors but got none")
        elif not tc["expect_errors"] and has_errors:
            ok = False
            reasons.append(f"expected no errors but got {len(report.errors)}")
            for e in report.errors:
                reasons.append(f"  -> {e['code']}: {e['message']}")
        elif tc.get("min_errors") and len(report.errors) < tc["min_errors"]:
            ok = False
            reasons.append(
                f"expected at least {tc['min_errors']} errors but got {len(report.errors)}"
            )

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        print(f"  {status}  {tc['name']} ({len(report.errors)} err, {len(report.warnings)} warn)")
        if not ok:
            for reason in reasons:
                print(f"       {reason}")
        # Show warnings for visibility
        for w in report.warnings:
            print(f"       WARN {w['code']}: {w['message']}")

    print(f"\nResults: {passed}/{total} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
