#!/usr/bin/env python3
"""Unit tests for scripts/check_tools.py.

Stdlib only (unittest). No network. Mock shutil.which and subprocess.run
to test verdict calculation without depending on the actual environment.

Run via:
    python -m unittest evals.test_check_tools -v
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Make scripts/ importable when run from repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from check_tools import (  # noqa: E402
    TOOL_REGISTRY,
    check_tool,
    detect_platform,
    get_extended_path,
    main,
)


class TestCheckToolUnit(unittest.TestCase):
    """Direct calls to check_tool() with mocked shutil.which."""

    def test_tool_available(self):
        """A tool on PATH returns available=True with version info."""
        with patch("check_tools.shutil.which", return_value="/usr/bin/curl"):
            with patch("check_tools.subprocess.run") as mock_run:
                mock_run.return_value.stdout = "curl 8.4.0\n"
                mock_run.return_value.stderr = ""
                r = check_tool("curl", "linux")
                self.assertTrue(r["available"])
                self.assertEqual(r["path"], "/usr/bin/curl")
                self.assertEqual(r["version"], "curl 8.4.0")

    def test_tool_missing(self):
        """A tool not on PATH returns available=False with install_hint."""
        with patch("check_tools.shutil.which", return_value=None):
            r = check_tool("aria2c", "windows")
            self.assertFalse(r["available"])
            self.assertIsNone(r["path"])
            self.assertIsNone(r["version"])
            self.assertIn("install_hint", r)
            self.assertIn("windows", r["install_hint"])
            self.assertIn("linux", r["install_hint"])
            self.assertIn("macos", r["install_hint"])

    def test_tool_with_exe_suffix_windows(self):
        """Windows: also tries <name>.exe."""
        calls = []
        def fake_which(name):
            calls.append(name)
            if name.endswith(".exe"):
                return "C:\\Tools\\yt-dlp.exe"
            return None
        with patch("check_tools.shutil.which", side_effect=fake_which):
            with patch("check_tools.subprocess.run") as mock_run:
                mock_run.return_value.stdout = "2024.09.06\n"
                mock_run.return_value.stderr = ""
                r = check_tool("yt-dlp", "windows")
                self.assertTrue(r["available"])
                self.assertIn(".exe", r["path"])
                self.assertEqual(calls, ["yt-dlp", "yt-dlp.exe"])

    def test_tool_version_timeout(self):
        """Version command timeout → still available but version=None."""
        with patch("check_tools.shutil.which", return_value="/usr/bin/yt-dlp"):
            with patch("check_tools.subprocess.run",
                       side_effect=subprocess.TimeoutExpired(cmd="yt-dlp", timeout=3)):
                r = check_tool("yt-dlp", "linux")
                self.assertTrue(r["available"])
                self.assertIsNone(r["version"])


class TestPlatformDetection(unittest.TestCase):
    """detect_platform() and get_extended_path() basic behavior."""

    def test_platform_returns_valid_value(self):
        self.assertIn(detect_platform(), {"windows", "linux", "macos"})

    def test_extended_path_wins_aria2c(self):
        """Windows PATH extension adds %LOCALAPPDATA%\\.local\\bin."""
        dirs, extended = get_extended_path("windows")
        self.assertTrue(extended)
        # Should contain a .local/bin path (exact form varies by OS)
        self.assertTrue(any(".local" in d.lower() for d in dirs))


class TestVerdictCalculation(unittest.TestCase):
    """Main() verdict calculation under mocked environment."""

    def _run_main(self, argv, available_tools):
        """Run main() with mocked which/run, return parsed JSON."""
        import io
        import contextlib
        buf = io.StringIO()
        # Mock shutil.which to return path only for available_tools
        def fake_which(name):
            return f"/fake/{name}" if name in available_tools else None
        with patch("check_tools.shutil.which", side_effect=fake_which):
            with patch("check_tools.subprocess.run") as mock_run:
                mock_run.return_value.stdout = "1.0.0\n"
                mock_run.return_value.stderr = ""
                with contextlib.redirect_stdout(buf):
                    rc = main(argv)
        self.assertEqual(rc, 0)
        return json.loads(buf.getvalue())

    def test_all_available_no_required_verdict_partial(self):
        """When no --required and all present → verdict=pass."""
        d = self._run_main(["--json"], {"curl", "yt-dlp", "aria2c"})
        self.assertEqual(d["verdict"], "pass")
        self.assertEqual(d["missing"], [])

    def test_missing_tool_no_required_verdict_partial(self):
        """Missing tool without --required → verdict=partial."""
        d = self._run_main(["--json"], {"curl"})  # only curl available
        self.assertEqual(d["verdict"], "partial")
        self.assertIn("yt-dlp", d["missing"])
        self.assertIn("aria2c", d["missing"])

    def test_required_all_present_verdict_pass(self):
        """--required yt-dlp with yt-dlp available → verdict=pass."""
        d = self._run_main(["--required", "yt-dlp"], {"curl", "yt-dlp"})
        self.assertEqual(d["verdict"], "pass")
        self.assertEqual(d["missing_required"], [])

    def test_required_missing_verdict_fail(self):
        """--required yt-dlp with yt-dlp missing → verdict=fail."""
        d = self._run_main(["--required", "yt-dlp"], {"curl"})
        self.assertEqual(d["verdict"], "fail")
        self.assertEqual(d["missing_required"], ["yt-dlp"])

    def test_single_tool_check(self):
        """--tool curl only checks curl."""
        d = self._run_main(["--tool", "curl", "--json"], {"curl"})
        self.assertEqual(list(d["tools"].keys()), ["curl"])


class TestToolRegistryIntegrity(unittest.TestCase):
    """Verify TOOL_REGISTRY schema is consistent."""

    def test_all_tools_have_required_fields(self):
        for name, meta in TOOL_REGISTRY.items():
            self.assertIn("required_for", meta, f"{name} missing required_for")
            self.assertIn("version_cmd", meta, f"{name} missing version_cmd")
            self.assertIn("expected_version_regex", meta, f"{name} missing version_regex")
            if name in ("yt-dlp", "aria2c"):
                self.assertIn("install_hint", meta, f"{name} missing install_hint")
                for plat in ("windows", "linux", "macos"):
                    self.assertIn(plat, meta["install_hint"],
                                  f"{name} missing {plat} install hint")
                self.assertIn("expected_size_mb", meta, f"{name} missing size_mb")


if __name__ == "__main__":
    unittest.main(verbosity=2)
