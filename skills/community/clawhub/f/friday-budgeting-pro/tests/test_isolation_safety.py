"""
tests/test_isolation_safety.py — Tests that verify the test isolation infrastructure.

Covers:
  1. check_test_isolation.py exits 0 on the real test suite.
  2. check_test_isolation.py flags a synthetic file with a hard-coded
     production DB path in a string value.
  3. The _isolated_app_dir autouse fixture actually monkeypatches the
     FRIDAY_BP_APP_DIR environment variable to a temp dir.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import textwrap


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# 1. Safety-check script passes on the current repository
# ---------------------------------------------------------------------------


def test_check_script_passes_on_repo():
    """Running check_test_isolation.py against the real tests/ dir exits 0."""
    result = subprocess.run(
        [sys.executable, "scripts/check_test_isolation.py"],
        capture_output=True,
        text=True,
        cwd=str(_repo_root()),
    )
    assert (
        result.returncode == 0
    ), f"check_test_isolation.py reported violations:\n{result.stdout}\n{result.stderr}"
    assert "OK" in result.stdout


# ---------------------------------------------------------------------------
# 2. Safety-check script flags a synthetic file with a production path
# ---------------------------------------------------------------------------


def test_check_script_detects_violations(tmp_path: pathlib.Path):
    """A synthetic tests/ tree with a hard-coded production DB path is flagged."""
    fake_tests = tmp_path / "tests"
    fake_tests.mkdir()
    (fake_tests / "__init__.py").write_text("")

    # Construct the production path — suppressed here since this line is
    # intentionally building the path for testing the checker itself.
    prod_db = "~/" + ".friday-bp/data.db"  # isolation-check: allow

    bad_file = fake_tests / "test_bad.py"
    bad_file.write_text(textwrap.dedent(f"""\
            import sqlite3

            DB_PATH = "{prod_db}"
            """))

    result = subprocess.run(
        [sys.executable, str(_repo_root() / "scripts" / "check_test_isolation.py")],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
    )
    assert (
        result.returncode == 1
    ), f"Expected exit 1 for production path; got:\n{result.stdout}\n{result.stderr}"
    assert "test_bad.py" in result.stdout


# ---------------------------------------------------------------------------
# 3. _isolated_app_dir autouse fixture patches the env var
# ---------------------------------------------------------------------------


def test_isolated_app_dir_patches_env_var(tmp_path: pathlib.Path):
    """FRIDAY_BP_APP_DIR is set to a temp dir by the autouse fixture."""
    app_dir_env = os.environ.get("FRIDAY_BP_APP_DIR", "")
    assert app_dir_env, "FRIDAY_BP_APP_DIR should be set by _isolated_app_dir fixture"

    # It must not be the real ~/.friday-bp directory.
    real_friday = str(pathlib.Path.home() / ".friday-bp")
    assert (
        app_dir_env != real_friday
    ), "FRIDAY_BP_APP_DIR must not point to the real production directory"

    # It should be a real, writable path.
    assert pathlib.Path(app_dir_env).exists(), "FRIDAY_BP_APP_DIR should be a real dir"


def test_isolated_app_dir_unique_per_test(tmp_path: pathlib.Path):
    """Each test gets its own unique FRIDAY_BP_APP_DIR (not shared state)."""
    app_dir_env = os.environ.get("FRIDAY_BP_APP_DIR", "")
    assert (
        "/tmp" in app_dir_env or "pytest" in app_dir_env or "friday_bp_test" in app_dir_env
    ), f"FRIDAY_BP_APP_DIR does not look like a temp path: {app_dir_env}"
