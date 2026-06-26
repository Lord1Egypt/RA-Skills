#!/usr/bin/env python3
"""CLI entrypoint for the Dida365 OpenAPI public skill."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dida365_lib.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
