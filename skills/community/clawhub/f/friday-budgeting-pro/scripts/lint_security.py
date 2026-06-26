#!/usr/bin/env python3
"""
lint_security.py — Forbidden-pattern security linter.

Walks *.py files under server/, ui/, scripts/ (excluding tests/, .venv/, venv/,
__pycache__/) and fails if any forbidden pattern is found.

Exit codes:
  0 — clean
  1 — one or more violations found
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Forbidden patterns
# ---------------------------------------------------------------------------
PATTERNS = [
    (
        re.compile(r"\b0\.0\.0\.0\b"),
        "hardcoded all-interfaces bind address",
    ),
    (
        re.compile(
            r"""(?:app|uvicorn)\.run\s*\([^)]*host\s*=\s*["\']?(?!127\.0\.0\.1|localhost)[^\s"',)]+"""
        ),
        "HTTP server bound to non-localhost host",
    ),
    (
        re.compile(r"""requests\.get\([^)]*\b(ngrok|tunnel|cloudflared?)\b"""),
        "public-tunnel reference in requests.get()",
    ),
    (
        re.compile(r"""Fernet\(open\("""),
        "Fernet key loaded from file (use keyring instead)",
    ),
    (
        re.compile(r"""PLAID_SECRET\s*=\s*["'][0-9a-f]{30,}["']"""),
        "hardcoded Plaid production secret",
    ),
    (
        re.compile(r"""PLAID_CLIENT_ID\s*=\s*["'][0-9a-f]{20,}["']"""),
        "hardcoded Plaid production client_id",
    ),
]

# ---------------------------------------------------------------------------
# Directories to scan / skip
# ---------------------------------------------------------------------------
SCAN_DIRS = ["server", "ui", "scripts"]
SKIP_DIRS = {"tests", ".venv", "venv", "__pycache__"}


def iter_python_files(root: Path):
    for scan_dir in SCAN_DIRS:
        base = root / scan_dir
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            # Skip any path component that matches a skip dir
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            yield path


def check_file(path: Path):
    violations = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"WARNING: could not read {path}: {exc}", file=sys.stderr)
        return violations

    for lineno, line in enumerate(lines, start=1):
        for pattern, description in PATTERNS:
            if pattern.search(line):
                violations.append(f"{path}:{lineno}: {description} — {line.strip()}")
    return violations


def main():
    root = Path(__file__).parent.parent.resolve()
    all_violations = []
    for py_file in sorted(iter_python_files(root)):
        all_violations.extend(check_file(py_file))

    if all_violations:
        for v in all_violations:
            print(v)
        sys.exit(1)

    print("lint_security: no violations found.")
    sys.exit(0)


if __name__ == "__main__":
    main()
