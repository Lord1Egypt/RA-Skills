#!/usr/bin/env python3
"""Tests for run-pipeline.py CLI defaults."""

import importlib.util
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"

spec = importlib.util.spec_from_file_location("run_pipeline", SCRIPTS_DIR / "run-pipeline.py")
run_pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_pipeline)


class TestRunPipelineDefaults(unittest.TestCase):
    def test_default_fetch_window_is_24_hours(self):
        parser = run_pipeline.build_parser()

        args = parser.parse_args([])

        self.assertEqual(args.hours, 24)


if __name__ == "__main__":
    unittest.main()
