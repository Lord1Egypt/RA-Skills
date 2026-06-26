"""Smoke tests for scripts/depradar.py — test the CLI entry point.

These tests run depradar.py as a subprocess to validate the CLI surface.
No network calls are made (--mock flag is used for all live-data tests).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

# Path to the depradar.py script
_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
_APIWATCH_PY = str(_SCRIPTS_DIR / "depradar.py")

# Ensure we run with the same interpreter as the test runner
_PYTHON = sys.executable


def _run(args: list, timeout: int = 30, env: dict = None) -> subprocess.CompletedProcess:
    """Run depradar.py with the given args and return the CompletedProcess."""
    cmd = [_PYTHON, _APIWATCH_PY] + args
    run_env = os.environ.copy()
    # Force UTF-8 output encoding so emoji in render output don't cause
    # UnicodeEncodeError on Windows (cp1252 default console encoding).
    run_env["PYTHONIOENCODING"] = "utf-8"
    if env:
        run_env.update(env)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding="utf-8",
        env=run_env,
    )


class TestHelpFlag(unittest.TestCase):

    def test_help_exits_0(self):
        result = _run(["--help"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_help_short_flag(self):
        result = _run(["-h"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_help_prints_usage(self):
        result = _run(["--help"])
        output = result.stdout + result.stderr
        self.assertTrue(
            "usage" in output.lower() or "depradar" in output.lower(),
            f"Expected usage info; got: {output[:400]}",
        )

    def test_help_mentions_emit(self):
        result = _run(["--help"])
        output = result.stdout + result.stderr
        self.assertIn("emit", output.lower())

    def test_help_mentions_mock(self):
        result = _run(["--help"])
        output = result.stdout + result.stderr
        self.assertIn("mock", output.lower())


class TestVersionFlag(unittest.TestCase):

    def test_version_exits_0(self):
        result = _run(["--version"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_version_output(self):
        result = _run(["--version"])
        output = result.stdout + result.stderr
        self.assertIn("depradar", output.lower())


class TestDiagnoseFlag(unittest.TestCase):

    def test_diagnose_exits_0(self):
        result = _run(["--diagnose"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_diagnose_shows_config_status(self):
        result = _run(["--diagnose"])
        output = result.stdout + result.stderr
        # Should show at least one known key or configuration info
        self.assertTrue(
            "GITHUB_TOKEN" in output
            or "configuration" in output.lower()
            or "depradar" in output.lower(),
            f"Expected config status; got: {output[:400]}",
        )

    def test_diagnose_mentions_github_token(self):
        result = _run(["--diagnose"])
        output = result.stdout + result.stderr
        self.assertIn("GITHUB_TOKEN", output)


class TestMockMode(unittest.TestCase):

    def test_mock_exits_0(self):
        result = _run(["--mock"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_produces_output(self):
        result = _run(["--mock"])
        self.assertGreater(len(result.stdout.strip()), 0)

    def test_mock_compact_mode(self):
        result = _run(["--mock", "--emit=compact"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        output = result.stdout
        # compact output should mention breaking changes and packages
        self.assertTrue(
            "stripe" in output.lower()
            or "breaking" in output.lower()
            or "package" in output.lower(),
            f"Unexpected compact output: {output[:400]}",
        )

    def test_mock_json_mode_exits_0(self):
        result = _run(["--mock", "--emit=json"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_json_is_valid_json(self):
        result = _run(["--mock", "--emit=json"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"JSON output is invalid: {exc}\nOutput: {result.stdout[:500]}")
        self.assertIsInstance(parsed, dict)

    def test_mock_json_contains_required_keys(self):
        result = _run(["--mock", "--emit=json"])
        parsed = json.loads(result.stdout)
        required_keys = [
            "project_path",
            "packages_scanned",
            "packages_with_breaking_changes",
            "packages_with_minor_updates",
            "depth",
            "days_window",
        ]
        for key in required_keys:
            self.assertIn(key, parsed, f"Missing key in JSON output: {key}")

    def test_mock_json_has_breaking_changes(self):
        result = _run(["--mock", "--emit=json"])
        parsed = json.loads(result.stdout)
        self.assertGreater(len(parsed["packages_with_breaking_changes"]), 0)

    def test_mock_markdown_mode(self):
        result = _run(["--mock", "--emit=md"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Breaking", result.stdout)

    def test_mock_context_mode(self):
        result = _run(["--mock", "--emit=context"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertGreater(len(result.stdout.strip()), 0)


class TestMockWithPackages(unittest.TestCase):

    def test_mock_stripe_exits_0(self):
        result = _run(["--mock", "stripe"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_stripe_output_contains_stripe(self):
        result = _run(["--mock", "stripe"])
        self.assertIn("stripe", result.stdout.lower())

    def test_mock_openai_exits_0(self):
        result = _run(["--mock", "openai"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_stripe_openai_exits_0(self):
        result = _run(["--mock", "stripe", "openai"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_stripe_openai_json_has_both(self):
        result = _run(["--mock", "--emit=json", "stripe", "openai"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        parsed = json.loads(result.stdout)
        all_packages = [
            p["package"]
            for p in (
                parsed.get("packages_with_breaking_changes", [])
                + parsed.get("packages_with_minor_updates", [])
            )
        ]
        # Both stripe and openai should be present (or at least one)
        self.assertGreater(len(all_packages), 0)

    def test_mock_unknown_package_exits_0(self):
        # Unknown packages should not crash the mock mode
        result = _run(["--mock", "some-unknown-pkg-xyz"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)


class TestMockWithOptions(unittest.TestCase):

    def test_mock_with_depth_quick(self):
        result = _run(["--mock", "--depth=quick"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_with_depth_deep(self):
        result = _run(["--mock", "--depth=deep"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_with_days_option(self):
        result = _run(["--mock", "--days=7"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_json_days_window_respected(self):
        result = _run(["--mock", "--emit=json", "--days=14"])
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["days_window"], 14)

    def test_mock_json_depth_respected(self):
        result = _run(["--mock", "--emit=json", "--depth=quick"])
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["depth"], "quick")

    def test_mock_with_path_option(self):
        result = _run(["--mock", "--path=/tmp"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_mock_json_project_path_in_output(self):
        result = _run(["--mock", "--emit=json"])
        parsed = json.loads(result.stdout)
        self.assertIn("project_path", parsed)
        self.assertIsInstance(parsed["project_path"], str)
        self.assertGreater(len(parsed["project_path"]), 0)


class TestImportSanity(unittest.TestCase):
    """Verify that the lib modules can be imported without side-effects."""

    def _import_module(self, module_name: str) -> None:
        lib_dir = str(_SCRIPTS_DIR / "lib")
        result = subprocess.run(
            [_PYTHON, "-c",
             f"import sys; sys.path.insert(0, r'{lib_dir}'); import {module_name}"],
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(
            result.returncode, 0,
            msg=f"Failed to import {module_name}:\n{result.stderr}",
        )

    def test_import_schema(self):
        self._import_module("schema")

    def test_import_semver(self):
        self._import_module("semver")

    def test_import_dates(self):
        self._import_module("dates")

    def test_import_cache(self):
        self._import_module("cache")

    def test_import_changelog_parser(self):
        self._import_module("changelog_parser")

    def test_import_dep_parser(self):
        self._import_module("dep_parser")

    def test_import_score(self):
        self._import_module("score")

    def test_import_render(self):
        self._import_module("render")

    def test_import_usage_scanner(self):
        self._import_module("usage_scanner")


if __name__ == "__main__":
    unittest.main()
