#!/usr/bin/env python3
"""CLI entrypoint for anime_character_loader.

Phase B target: keep behavior compatible by delegating to legacy implementation.
"""

from __future__ import annotations

import runpy
from pathlib import Path


def _legacy_module_path() -> Path:
    return Path(__file__).resolve().parent / "legacy.py"


def main() -> int:
    """Run legacy CLI to preserve argument/behavior compatibility."""
    module_path = _legacy_module_path()
    if not module_path.exists():
        raise FileNotFoundError(f"Legacy module not found: {module_path}")

    runpy.run_path(str(module_path), run_name="__main__")
    return 0


if __name__ == "__main__":
    main()
