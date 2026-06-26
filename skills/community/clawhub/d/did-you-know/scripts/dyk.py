#!/usr/bin/env python3
"""Backwards-compatible entry point — delegates to serve_hook.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from serve_hook import main  # noqa: F401

if __name__ == "__main__":
    raise SystemExit(main())
