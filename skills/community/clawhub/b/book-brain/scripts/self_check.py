#!/usr/bin/env python3
"""Self-check: skill bundle files only (no network)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "references/SECURITY.md",
    "references/AGENT_CONTRACT.md",
    "references/MEMORY_LAYOUT.md",
    "references/LATTICE_INTEGRATION.md",
    "scripts/scaffold_haven.py",
    "scripts/write_ref_stub.py",
    "templates/memory_index.seed.json",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (ROOT / r).is_file()]
    if missing:
        print("MISSING:", ", ".join(missing), file=sys.stderr)
        return 1
    print("OK book-brain self_check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())