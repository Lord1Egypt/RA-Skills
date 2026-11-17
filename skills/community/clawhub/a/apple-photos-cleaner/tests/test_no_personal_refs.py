#!/usr/bin/env python3
"""
Guard against personal references in published files (ROADMAP T0.2).

ClawHub publishes the whole repository, so examples, fixtures and docs must use
neutral placeholder names. Real family names and machine names once leaked into
SKILL.md examples; this keeps them out.
"""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
THIS_FILE = Path(__file__).resolve()

# Matched case-insensitively on word boundaries
DENYLIST = [
    "Jonah",
    "Silas",
    "Matt's",
    "Mac mini",
]

DENY_PATTERN = re.compile(r"\b(?:" + "|".join(re.escape(term) for term in DENYLIST) + r")\b", re.IGNORECASE)


def tracked_text_files() -> list[Path]:
    """Every tracked file except binaries (NUL byte) and this denylist itself."""
    if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
        pytest.skip("not a git checkout")
    output = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    paths = [REPO_ROOT / line for line in output.splitlines()]
    return [p for p in paths if p.is_file() and p.resolve() != THIS_FILE and b"\0" not in p.read_bytes()]


def test_no_personal_references():
    hits = []
    for path in tracked_text_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            match = DENY_PATTERN.search(line)
            if match:
                hits.append(f"{path.relative_to(REPO_ROOT)}:{lineno}: {match.group(0)!r}")
    assert not hits, "Personal references found (use neutral names like Alex/Sam):\n" + "\n".join(hits)
