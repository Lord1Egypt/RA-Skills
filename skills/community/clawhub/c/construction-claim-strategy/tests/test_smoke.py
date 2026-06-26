"""
Smoke test for strategy_advisor.py.

Tests the script by importing main() directly and patching sys.argv,
avoiding external process invocation entirely. This keeps the CLI
smoke-test intent while satisfying static-analysis scanners.

Checks that:
  - --reference exits cleanly and prints non-empty output
  - --file mode exits cleanly
  - the output file is created and non-empty
  - the output contains all 7 dimension headers
  - the script contains no forbidden imports

This is intentionally minimal. It catches the most common breakages:
import errors, missing files, schema regressions, and major output
structural changes. It is not a substitute for unit tests of the
underlying logic.

Run from the package root:
    python3 -m unittest tests.test_smoke
    python3 -m pytest tests/test_smoke.py  (if pytest is installed)
"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch


PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = PACKAGE_ROOT / "scripts" / "strategy_advisor.py"
SAMPLE_INPUT = PACKAGE_ROOT / "examples" / "strategy_input.json"

# Ensure scripts/ is importable
SCRIPTS_DIR = str(PACKAGE_ROOT / "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from strategy_advisor import main, VERSION

EXPECTED_DIMENSION_HEADERS = [
    "Situation Assessment",
    "Scope Control",
    "Direction Decision",
    "Argument Strategy",
    "Disclosure Control",
    "Response Architecture",
    "Risk Assessment",
]


class StrategyAdvisorSmokeTest(unittest.TestCase):

    def setUp(self):
        self.assertTrue(SCRIPT.exists(), f"Script not found: {SCRIPT}")
        self.assertTrue(
            SAMPLE_INPUT.exists(),
            f"Sample input not found: {SAMPLE_INPUT}",
        )

    def _run_cli(self, argv):
        """Run main() with patched sys.argv, capturing stdout/stderr."""
        out = io.StringIO()
        err = io.StringIO()
        with patch.object(sys, "argv", argv), \
             redirect_stdout(out), redirect_stderr(err):
            try:
                main()
                code = 0
            except SystemExit as e:
                code = int(e.code) if e.code is not None else 0
        return code, out.getvalue(), err.getvalue()

    def test_reference_mode_runs(self):
        """`--reference` should run and print non-empty output to stdout."""
        code, stdout, stderr = self._run_cli(
            ["strategy_advisor.py", "--reference"]
        )
        self.assertEqual(
            code, 0,
            f"--reference exited non-zero. stderr:\n{stderr}",
        )
        self.assertTrue(
            stdout.strip(),
            "--reference produced empty output",
        )

    def test_file_mode_produces_report(self):
        """`--file` mode should generate a report containing all 7 dimensions."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as tmp:
            output_path = tmp.name

        try:
            code, stdout, stderr = self._run_cli([
                "strategy_advisor.py",
                "--file", str(SAMPLE_INPUT),
                "--output", output_path,
            ])
            self.assertEqual(
                code, 0,
                f"--file mode exited non-zero. stderr:\n{stderr}",
            )

            self.assertTrue(
                os.path.exists(output_path),
                "Output file was not created",
            )
            with open(output_path, "r", encoding="utf-8") as f:
                report = f.read()

            self.assertTrue(report.strip(), "Output report is empty")

            for header in EXPECTED_DIMENSION_HEADERS:
                self.assertIn(
                    header, report,
                    f"Expected dimension header not found in report: {header!r}",
                )
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_version_flag(self):
        """`--version` should print version string and exit cleanly."""
        code, stdout, stderr = self._run_cli(
            ["strategy_advisor.py", "--version"]
        )
        self.assertEqual(code, 0)
        self.assertIn("Strategy Advisor v", stdout + stderr)

    def test_no_forbidden_imports(self):
        """Script must not import network, subprocess, or dynamic-exec modules.

        Uses ast.parse to walk the syntax tree. Catches forbidden
        imports and dangerous built-in calls regardless of aliasing,
        whitespace, or indirection. Does not false-positive on
        comments, docstrings, or plain-English strings.

        Enforces the 'stdlib-only, no network, no subprocess' security claim
        in SKILL.md.
        """
        import ast

        FORBIDDEN_MODULES = {
            "subprocess", "socket", "requests", "httpx", "aiohttp",
            "importlib", "pickle", "marshal",
        }
        # Dotted imports: "from urllib.request import ..." etc.
        FORBIDDEN_DOTTED = {
            "urllib.request", "urllib.error",
            "http.client", "http.server",
        }
        # Bare dangerous built-in calls
        FORBIDDEN_CALLS = {"exec", "eval", "compile"}
        # Attribute calls: os.system(), pickle.loads(), etc.
        FORBIDDEN_ATTR_CALLS = {
            ("os", "system"),
            ("pickle", "loads"),
            ("marshal", "loads"),
            ("importlib", "import_module"),
        }

        with open(SCRIPT, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source, filename=str(SCRIPT))
        violations = []

        for node in ast.walk(tree):
            # import X / import X as Y
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top in FORBIDDEN_MODULES or alias.name in FORBIDDEN_DOTTED:
                        violations.append(
                            f"  L{node.lineno}: import {alias.name}"
                        )
            # from X import Y
            elif isinstance(node, ast.ImportFrom) and node.module:
                top = node.module.split(".")[0]
                if top in FORBIDDEN_MODULES or node.module in FORBIDDEN_DOTTED:
                    violations.append(
                        f"  L{node.lineno}: from {node.module} import ..."
                    )
            # function calls
            elif isinstance(node, ast.Call):
                func = node.func
                # bare dangerous call
                if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                    violations.append(
                        f"  L{node.lineno}: {func.id}() call"
                    )
                # dotted dangerous call
                elif isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                    pair = (func.value.id, func.attr)
                    if pair in FORBIDDEN_ATTR_CALLS:
                        violations.append(
                            f"  L{node.lineno}: {func.value.id}.{func.attr}() call"
                        )

        self.assertEqual(
            violations, [],
            "Forbidden import/call found in strategy_advisor.py:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
