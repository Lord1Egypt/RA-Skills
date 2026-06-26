"""Test configuration for the dont-starve-skill memory script."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# conftest.py lives at <skill-root>/tests/conftest.py.
# parents[1] is the skill root (dont-starve-skill/).
_SKILL_ROOT = Path(__file__).resolve().parents[1]
_MEMORY_PY = _SKILL_ROOT / "scripts" / "memory.py"


def _import_memory():
    spec = importlib.util.spec_from_file_location("memory", str(_MEMORY_PY))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["memory"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def memory():
    """Import memory.py after the implementation exists."""
    return _import_memory()


@pytest.fixture(autouse=True)
def isolated_memory_dir(tmp_path):
    """Redirect memory storage to a temporary directory for every test."""
    env_dir = tmp_path / "memory"
    env_dir.mkdir()
    with patch.dict(os.environ, {"DONTSTARVE_MEMORY_DIR": str(env_dir)}):
        yield env_dir
