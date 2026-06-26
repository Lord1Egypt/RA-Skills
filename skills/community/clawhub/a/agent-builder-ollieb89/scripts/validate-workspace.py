#!/usr/bin/env python3
"""validate_workspace.py

Static checks for an OpenClaw workspace. Exits non-zero if missing key guardrails.

Usage:
  python3 scripts/validate-workspace.py [workspace_dir]
"""

from __future__ import annotations
import sys
from pathlib import Path

REQ_FILES = [
    "AGENTS.md","SOUL.md","TOOLS.md","IDENTITY.md","USER.md","HEARTBEAT.md","BOOTSTRAP.md"
]

GUARDRAIL_SNIPPETS = {
    "ask-before-destructive": ["ask before destructive", "trash over rm", "prefer trash"],
    "ask-before-outbound": ["ask before outbound", "never send", "explicit approval"],
    "stop-on-cli-error": ["stop on cli", "--help", "unknown flag"],
    "no-secrets": ["never store credentials", "no secrets", "do not commit secrets", "credentials"],
    "sub-agent-note": ["sub-agent", "sub agents", "subagents"],
}

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    missing = [f for f in REQ_FILES if not (root / f).exists()]
    if missing:
        print("Missing required files:")
        for f in missing:
            print(f" - {f}")
        return 2

    agents = (root / "AGENTS.md").read_text(encoding="utf-8", errors="ignore").lower()

    failures = []
    for name, needles in GUARDRAIL_SNIPPETS.items():
        if not any(n in agents for n in needles):
            failures.append(name)

    if failures:
        print("AGENTS.md is missing guardrail(s):")
        for f in failures:
            print(f" - {f}")
        return 3

    print("✅ Workspace looks sane.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
