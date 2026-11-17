#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 3 步可靠性：快速失败预检 + 超时/加密/不支持版本翻译 + cad_scan 快速失败。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from cad_preflight import preflight_file  # noqa: E402
from cad_batch import rc_reason, classify_input, input_fail_reason  # noqa: E402

SAMPLE = SKILL_DIR / "examples" / "sample_room.dxf"


class CadPreflightTest(unittest.TestCase):
    def test_empty_and_tiny_and_bad_magic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty = root / "empty.dxf"
            empty.write_bytes(b"")
            tiny = root / "tiny.dxf"
            tiny.write_bytes(b"x" * 100)
            bad = root / "bad.dxf"
            bad.write_bytes(b"This is definitely not cad content\n" * 120)
            self.assertEqual(preflight_file(empty)["kind"], "empty")
            self.assertEqual(preflight_file(tiny)["kind"], "tiny")
            r = preflight_file(bad)
            self.assertEqual(r["kind"], "bad_magic")
            self.assertTrue(r["reason"])

    def test_sample_dxf_and_dwg_header_ok(self):
        r = preflight_file(SAMPLE)
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["format"], "DXF")
        with tempfile.TemporaryDirectory() as tmp:
            dwg = Path(tmp) / "x.dwg"
            dwg.write_bytes(b"AC1015" + b"\x00" * 3000)
            r2 = preflight_file(dwg)
            self.assertTrue(r2["ok"], r2)
            self.assertEqual(r2["format"], "DWG")
            self.assertEqual(r2.get("version"), "1015")

    def test_unsupported_version_is_fast_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            dwg = Path(tmp) / "v.dwg"
            dwg.write_bytes(b"AC9999" + b"\x00" * 4000)
            r = preflight_file(dwg)
            self.assertEqual(r["kind"], "unsupported_version")
            self.assertIn("不支持的 DWG 版本", r["reason"])

    def test_cad_scan_fast_fails_without_pretending_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.dxf"
            bad.write_bytes(b"definitely-not-cad\n" * 120)
            t0 = time.time()
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "cad_scan.py"), str(bad), "--format", "json"],
                capture_output=True, text=True, timeout=30,
            )
            elapsed = time.time() - t0
            self.assertLess(elapsed, 5.0, f"快速失败必须 <5 秒，实际 {elapsed:.2f}s")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout or "{}")
            self.assertTrue(data.get("notes") and any("快速失败" in x for x in data["notes"]),
                             data.get("notes"))
            self.assertFalse(data.get("files"))

    def test_batch_classify_and_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty = root / "empty.dxf"
            empty.write_bytes(b"")
            bad = root / "bad.dxf"
            bad.write_bytes(b"not-cad\n" * 200)
            self.assertEqual(classify_input(empty), "缺输入")
            self.assertEqual(classify_input(bad), "失败跳过")
            self.assertTrue("魔数" in input_fail_reason(bad))

    def test_rc_reason_translates_timeout_encrypt_unsupported_memory(self):
        self.assertIn("超时终止", rc_reason(124, "boom", 45))
        self.assertIn("加密 DWG", rc_reason(1, "file is encrypted, password required", 45))
        self.assertIn("不支持的 DWG 版本", rc_reason(1, "unsupported DWG version AC9999", 45))
        self.assertIn("内存看门狗终止", rc_reason(-9, "cad_scan内存闸 峰值内存 5000MB 已超上限", 45))


if __name__ == "__main__":
    unittest.main()
