#!/usr/bin/env python3
"""
Supply-chain guard for GitHub Actions workflows (ROADMAP T0.6).

A tag like `@v4` can be moved to point at different code; a full commit SHA
can't. Every action and reusable workflow, first-party `and3rn3t/.github` ones
included, is pinned by SHA with a `# vX` comment. Renovate keeps the pins fresh.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = sorted((REPO_ROOT / ".github" / "workflows").glob("*.y*ml"))

USES = re.compile(r"^\s*(?:-\s*)?uses:\s*(?P<ref>[^\s#]+)(?:\s*#\s*(?P<comment>.*))?$")
SHA = re.compile(r"^[0-9a-f]{40}$")


def uses_lines():
    for path in WORKFLOWS:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = USES.match(line)
            if match:
                yield path.name, lineno, match["ref"], match["comment"]


def test_workflows_found():
    assert WORKFLOWS
    assert any(True for _ in uses_lines())


def test_actions_pinned_by_sha():
    unpinned = []
    for name, lineno, ref, comment in uses_lines():
        if ref.startswith(("./", "docker://")):
            continue
        _, _, version = ref.partition("@")
        if not SHA.match(version) or not (comment and comment.startswith("v")):
            unpinned.append(f"{name}:{lineno}: {ref}")
    assert not unpinned, "Pin actions as `owner/repo@<40-hex sha> # vX`:\n" + "\n".join(unpinned)
