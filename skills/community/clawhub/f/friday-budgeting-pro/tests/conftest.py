"""
tests/conftest.py — Shared pytest fixtures for the Friday Budgeting Pro test suite.

Key fixture
-----------
_isolated_app_dir (autouse=True)
    Ensures *every* test sees a fresh, isolated FRIDAY_BP_APP_DIR — the
    production ~/.friday-bp/ directory is never touched.

    The fixture:
      1. Creates a temporary directory via pytest's ``tmp_path``.
      2. Monkeypatches the ``FRIDAY_BP_APP_DIR`` environment variable.
      3. Reloads ``server.paths`` (if already imported) so that the
         module-level constants (APP_DIR, DB_PATH, …) resolve to the temp dir.
      4. Also patches the constants directly on the already-imported module so
         that any code that imported the names before the fixture ran still
         gets the right values.

This is the safety net — even tests that forget to set up their own DB
fixture are automatically isolated.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolated_app_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect every test to a fresh temp dir — never ~/.friday-bp/."""
    test_dir = tmp_path / "friday_bp_test"
    test_dir.mkdir(exist_ok=True)

    monkeypatch.setenv("FRIDAY_BP_APP_DIR", str(test_dir))

    # Also patch module-level constants so code that imported paths early
    # still sees the temp dir.
    if "server.paths" in sys.modules:
        paths_mod = sys.modules["server.paths"]
        monkeypatch.setattr(paths_mod, "APP_DIR", test_dir, raising=False)
        monkeypatch.setattr(paths_mod, "DB_PATH", test_dir / "data.db", raising=False)
        monkeypatch.setattr(
            paths_mod,
            "SYNC_LOCK_PATH",
            test_dir / "sync.lock",
            raising=False,
        )
        monkeypatch.setattr(
            paths_mod,
            "EXPORTS_DIR",
            test_dir / "exports",
            raising=False,
        )

    yield test_dir
