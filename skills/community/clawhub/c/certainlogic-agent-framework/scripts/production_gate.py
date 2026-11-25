#!/usr/bin/env python3
"""
Production Gate — 7-point production readiness check.

Usage:
    python3 production_gate.py <project_dir>
    python3 production_gate.py <project_dir> --verbose

Returns exit 0 if all 7 checks pass, 1 otherwise.
"""
import argparse
import os
import sys
from pathlib import Path


CHECKS = [
    ("No file >300 lines in core", "max_line_length"),
    ("At least one test file", "has_tests"),
    ("Proper startup mechanism (systemd or equivalent)", "has_startup"),
    ("Structured logging (not bare print/echo)", "structured_logging"),
    ("Health check endpoint", "has_health"),
    ("No watchdog sprawl (≤1 watchdog script)", "watchdog_sprawl"),
    ("Error handling (try/except)", "error_handling"),
]


def check_max_line_length(project):
    """Check no Python file exceeds 300 lines."""
    for f in sorted(project.rglob("*.py")):
        if "test_" not in f.name and "archive" not in str(f):
            lines = f.read_text().count("\n")
            if lines > 300:
                return False, f"{f.relative_to(project)}: {lines} lines"
    return True, "All core files ≤300 lines"


def check_has_tests(project):
    """Check for at least one test file."""
    tests = list(project.rglob("test_*.py")) + list(project.rglob("*_test.py"))
    if tests:
        return True, f"Found {len(tests)} test file(s)"
    return False, "No test files found"


def check_has_startup(project):
    """Check for systemd unit, Dockerfile, or start script."""
    candidates = list(project.rglob("*.service")) + list(project.rglob("Dockerfile"))
    candidates += list(project.glob("start.sh")) + list(project.glob("start-*.sh"))
    if candidates:
        return True, f"Found startup mechanism: {candidates[0].name}"
    return False, "No startup mechanism found (systemd/Dockerfile/start.sh)"


def check_structured_logging(project):
    """Check for structured logging (logging module, not print)."""
    for f in project.rglob("*.py"):
        if "test_" not in f.name:
            content = f.read_text()
            if "import logging" in content or "logging." in content:
                return True, "Structured logging found"
    return False, "No structured logging (logging module) found"


def check_has_health(project):
    """Check for health check endpoint."""
    for f in project.rglob("*.py"):
        content = f.read_text()
        if "/health" in content or "health" in content.lower():
            return True, f"Health endpoint found in {f.name}"
    return False, "No health check endpoint found"


def check_watchdog_sprawl(project):
    """Check there's at most 1 watchdog script."""
    watchdogs = [f for f in project.glob("*watchdog*")] + \
                [f for f in project.rglob("*watchdog*.py")]
    if len(watchdogs) <= 1:
        return True, f"{len(watchdogs)} watchdog script(s)"
    return False, f"{len(watchdogs)} watchdog scripts (max 1 allowed)"


def check_error_handling(project):
    """Check for try/except in main source files."""
    for f in sorted(project.rglob("*.py")):
        if "test_" not in f.name and "archive" not in str(f):
            content = f.read_text()
            if "try:" in content and "except" in content:
                return True, f"Error handling found in {f.name}"
    return False, "No try/except error handling found in source files"


CHECK_FUNCS = {
    "max_line_length": check_max_line_length,
    "has_tests": check_has_tests,
    "has_startup": check_has_startup,
    "structured_logging": check_structured_logging,
    "has_health": check_has_health,
    "watchdog_sprawl": check_watchdog_sprawl,
    "error_handling": check_error_handling,
}


def main():
    parser = argparse.ArgumentParser(description="7-point production readiness check")
    parser.add_argument("project", help="Project directory to check")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    project = Path(args.project)
    if not project.is_dir():
        print(f"Error: {args.project} is not a directory")
        sys.exit(1)

    print(f"=== Production Gate: {project.resolve()} ===\n")

    passed = 0
    failed = 0
    for name, key in CHECKS:
        ok, msg = CHECK_FUNCS[key](project)
        status = "✅" if ok else "❌"
        print(f"  {status}  {name}")
        if args.verbose or not ok:
            print(f"       {msg}")
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n  {passed}/{passed + failed} checks passed", end="")
    if failed:
        print(f" — {failed} FAILED ❌")
        sys.exit(1)
    else:
        print(" — ALL PASSED ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()