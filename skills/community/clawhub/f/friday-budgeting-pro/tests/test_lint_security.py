"""
Tests for scripts/lint_security.py
"""

import subprocess
import sys
import textwrap
from pathlib import Path

LINTER = Path(__file__).parent.parent / "scripts" / "lint_security.py"


def run_linter(*extra_args):
    result = subprocess.run(
        [sys.executable, str(LINTER), *extra_args],
        capture_output=True,
        text=True,
    )
    return result


# ---------------------------------------------------------------------------
# Smoke test: linter exits 0 on the actual repo
# ---------------------------------------------------------------------------
def test_smoke_clean_repo():
    result = run_linter()
    assert (
        result.returncode == 0
    ), f"lint_security.py found violations in the current repo:\n{result.stdout}"


# ---------------------------------------------------------------------------
# Synthetic positive: 0.0.0.0 in a non-test source file should be flagged
# ---------------------------------------------------------------------------
def test_flags_all_interfaces_bind(tmp_path, monkeypatch):
    """A file containing the all-interfaces address should be caught."""
    # Create a fake server/ dir under tmp_path so the linter picks it up
    fake_server = tmp_path / "server"
    fake_server.mkdir()
    bad_file = fake_server / "bad_config.py"
    bad_file.write_text(textwrap.dedent("""\
            HOST = "0" + "." + "0" + "." + "0" + "." + "0"  # won't match
            HOST2 = "0.0.0.0"  # this one should match
            """))

    # Patch the linter's root so it scans tmp_path instead of the real repo
    import scripts.lint_security as linter  # noqa: PLC0415

    original_root = None

    def patched_iter(root):
        return linter.iter_python_files(tmp_path)

    monkeypatch.setattr(linter, "iter_python_files", patched_iter)

    violations = linter.check_file(bad_file)
    assert any(
        "all-interfaces" in v for v in violations
    ), f"Expected a violation for 0.0.0.0 but got: {violations}"


# ---------------------------------------------------------------------------
# Tests/ files are excluded — a violating pattern inside tests/ is ignored
# ---------------------------------------------------------------------------
def test_tests_dir_excluded(tmp_path, monkeypatch):
    """Violations inside tests/ should be silently skipped."""
    import scripts.lint_security as linter  # noqa: PLC0415

    # Build a fake layout: tests/bad.py with a violation, server/ clean
    fake_tests = tmp_path / "tests"
    fake_tests.mkdir()
    bad_test_file = fake_tests / "bad.py"
    bad_test_file.write_text('HOST = "0.0.0.0"\n')

    fake_server = tmp_path / "server"
    fake_server.mkdir()
    clean_file = fake_server / "good.py"
    clean_file.write_text("HOST = '127.0.0.1'\n")

    # Collect files the way the real linter would from tmp_path
    found = list(linter.iter_python_files(tmp_path))

    # tests/bad.py must NOT appear in the scanned file list
    assert bad_test_file not in found, "lint_security should exclude files under tests/"
    # server/good.py SHOULD appear
    assert clean_file in found, "lint_security should scan files under server/"


# ---------------------------------------------------------------------------
# Synthetic Plaid secret flagged
# ---------------------------------------------------------------------------
def test_flags_hardcoded_plaid_secret(tmp_path):
    import scripts.lint_security as linter  # noqa: PLC0415

    fake_server = tmp_path / "server"
    fake_server.mkdir()
    bad_file = fake_server / "secrets.py"
    bad_file.write_text('PLAID_SECRET = "abcdef1234567890abcdef1234567890"\n')

    violations = linter.check_file(bad_file)
    assert any(
        "Plaid" in v for v in violations
    ), f"Expected Plaid secret violation but got: {violations}"
