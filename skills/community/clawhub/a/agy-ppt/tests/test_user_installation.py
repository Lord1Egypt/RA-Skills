#!/usr/bin/env python3
"""Regression tests for the lightweight user bootstrap path."""

from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path
import sys
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import codex_ppt_runtime as runtime  # noqa: E402


class LightweightBootstrapTests(unittest.TestCase):
    def test_bootstrap_installs_runtime_dependencies_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "runtime"
            python = home / ".venv" / "bin" / "python"
            python.parent.mkdir(parents=True)
            python.touch()
            args = argparse.Namespace(upgrade=False)
            with (
                mock.patch.object(runtime, "_runtime_home", return_value=home),
                mock.patch.object(runtime, "_venv_python", return_value=python),
                mock.patch.object(runtime.subprocess, "run") as run,
            ):
                self.assertEqual(runtime._bootstrap(args), 0)

        run.assert_called_once()
        command = run.call_args.args[0]
        self.assertEqual(command[:4], [str(python), "-m", "pip", "install"])
        self.assertIn("-r", command)
        rendered = " ".join(command).lower()
        for forbidden in ("unittest", "pytest", "qualification", "render", "tesseract"):
            self.assertNotIn(forbidden, rendered)

    def test_bootstrap_does_not_call_doctor_or_create_sample_deck(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "runtime"
            args = argparse.Namespace(upgrade=False)
            with (
                mock.patch.object(runtime, "_runtime_home", return_value=home),
                mock.patch.object(runtime.venv.EnvBuilder, "create"),
                mock.patch.object(runtime.subprocess, "run"),
                mock.patch.object(runtime, "_doctor") as doctor,
            ):
                runtime._bootstrap(args)
        doctor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
