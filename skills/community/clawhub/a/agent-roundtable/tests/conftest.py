"""Pytest conftest — ensures src/ is on sys.path."""

import sys
from pathlib import Path

src = Path(__file__).resolve().parent.parent / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))
