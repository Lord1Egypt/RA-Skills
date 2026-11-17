#!/usr/bin/env python3
"""Compatibility entry point delegating to the packaged llm_wiki CLI."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(PROJECT_ROOT / "src"), str(PROJECT_ROOT)]

try:
    from llm_wiki import cli as _cli
except ImportError:
    from src.llm_wiki import cli as _cli

globals().update(
    {key: value for key, value in vars(_cli).items() if not key.startswith("__")}
)

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(_cli.main())
