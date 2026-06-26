#!/usr/bin/env python3
"""Run the repo-root Atlas CLI from a skill checkout.

Resolves `core/atlas_cli.py` using:
1. `ATLAS_AGENT_REPO` — absolute path to this monorepo root (recommended if you copy only `skills/` elsewhere), or
2. Default: three parents above this file (`skills/atlas-avatar/scripts/` → repo root).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    override = os.environ.get("ATLAS_AGENT_REPO", "").strip()
    if override:
        root = Path(override).expanduser().resolve()
    else:
        root = Path(__file__).resolve().parents[3]
    cli = root / "core" / "atlas_cli.py"
    if not cli.is_file():
        print(
            "Could not find core/atlas_cli.py.\n"
            "Clone the full monorepo (with core/ + skills/) or set ATLAS_AGENT_REPO "
            "to the repository root.",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(subprocess.call([sys.executable, str(cli), *sys.argv[1:]]))


if __name__ == "__main__":
    main()
