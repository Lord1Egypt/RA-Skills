#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/self_test.py 统一闭环不变量测试。

只测轻量且稳定快的部分：schema 原生校验器的正/负向约束、
self_test CLI 在跳过重量级步骤时仍能快速跑通并输出正确报告。
不重复跑全量 unittest（它对 201 项用例已由 run_preflight 统一跑）。
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = SKILL_DIR / "scripts"
PYTHON = sys.executable


def _load_script():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    import self_test as st  # noqa: E402
    return st


class SchemaValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.st = _load_script()

    def _sample(self, schema_name: str) -> dict:
        schema_path = SKILL_DIR / "schemas" / schema_name
        samples = self.st._sample_for_schema(schema_path)
        self.assertTrue(samples, f"{schema_name} 没有匹配样例")
        return json.loads(samples[0].read_text(encoding="utf-8"))

    def test_candidate_schema_positive_and_negative(self):
        st = self.st
        schema_path = SKILL_DIR / "schemas" / "candidate-v0.schema.json"
        ok, errors = st.validate_schema_file(self._sample("candidate-v0.schema.json"), schema_path)
        self.assertTrue(ok, errors)
        negatives = st._negative_samples(schema_path)
        self.assertGreaterEqual(len(negatives), 3)
        for bad in negatives:
            payload = {k: v for k, v in bad.items() if k != "_label"}
            ok, _ = st.validate_schema_file(payload, schema_path)
            self.assertFalse(ok, f"负向样例应被拦截: {bad['_label']}")

    def test_qto_schema_positive_and_negative(self):
        st = self.st
        schema_path = SKILL_DIR / "schemas" / "qto-project-v1.schema.json"
        ok, errors = st.validate_schema_file(self._sample("qto-project-v1.schema.json"), schema_path)
        self.assertTrue(ok, errors)
        negatives = st._negative_samples(schema_path)
        self.assertGreaterEqual(len(negatives), 3)
        for bad in negatives:
            payload = {k: v for k, v in bad.items() if k != "_label"}
            ok, _ = st.validate_schema_file(payload, schema_path)
            self.assertFalse(ok, f"负向样例应被拦截: {bad['_label']}")


class SelfTestCliTest(unittest.TestCase):
    def test_fast_skip_cli_passes(self):
        with tempfile.TemporaryDirectory(prefix="cad-selftest-cli-") as tmpd:
            tmp = Path(tmpd)
            proc = subprocess.run(
                [PYTHON, str(SCRIPTS_DIR / "self_test.py"), "--out-dir", str(tmp),
                 "--skip-doctor", "--skip-unit", "--skip-schema", "--skip-sample", "--json-only"],
                cwd=str(SKILL_DIR), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            data = json.loads(proc.stdout)
            self.assertEqual(data["tool"], "cad-file-reader-self-test")
            self.assertEqual(data["schema"], "cad-file-reader/self-test/v1")
            for key in ("doctor", "unit_tests", "schema_contract", "sample_dxf"):
                self.assertEqual(data[key]["status"], "skipped", key)
            self.assertTrue(data["bad_file_invariants"]["ok"])
            self.assertEqual(data["real_dwg_regression"]["status"], "skipped")
            self.assertTrue(data["summary"]["ok"])

    def test_manifest_missing_reports_skipped_regression(self):
        with tempfile.TemporaryDirectory(prefix="cad-selftest-mfx-") as tmpd:
            tmp = Path(tmpd)
            missing = tmp / "missing.json"
            proc = subprocess.run(
                [PYTHON, str(SCRIPTS_DIR / "self_test.py"), "--manifest", str(missing),
                 "--skip-doctor", "--skip-unit", "--skip-schema", "--skip-sample", "--report-json", str(tmp / "r.json")],
                cwd=str(SKILL_DIR), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            report = json.loads((tmp / "r.json").read_text(encoding="utf-8"))
            self.assertEqual(report["real_dwg_regression"]["status"], "skipped")
            self.assertTrue(report["summary"]["ok"])


if __name__ == "__main__":
    unittest.main()
