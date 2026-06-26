"""Tests for --fail-on-breaking exit code behavior."""

import sys
from unittest.mock import patch, MagicMock


def _run_depradar(argv):
    """Run depradar.run() with given argv and return exit code."""
    import importlib
    import importlib.util
    import os

    scripts_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
    spec = importlib.util.spec_from_file_location(
        "depradar_main",
        os.path.join(scripts_dir, "depradar.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.run(argv)


class TestFailOnBreaking:
    def test_mock_no_fail_by_default(self):
        """--mock without --fail-on-breaking should exit 0."""
        code = _run_depradar(["--mock", "--no-community"])
        assert code == 0

    def test_mock_fail_on_breaking_exits_1(self):
        """--mock --fail-on-breaking should exit 1 (mock has breaking changes)."""
        code = _run_depradar(["--mock", "--fail-on-breaking", "--no-community"])
        assert code == 1

    def test_mock_fail_on_breaking_with_no_breaking(self):
        """Filter to a package that's minor-only: exit 0."""
        # axios and express are minor in mock — filter to them
        code = _run_depradar(
            ["--mock", "--fail-on-breaking", "--no-community", "axios", "express"]
        )
        assert code == 0

    def test_version_flag(self):
        """--version should exit 0."""
        code = _run_depradar(["--version"])
        assert code == 0

    def test_help_flag(self):
        """--help should exit 0."""
        code = _run_depradar(["--help"])
        assert code == 0
