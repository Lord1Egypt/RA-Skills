#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for scripts/doctor.py（三平台 status/fix 分支）。

说明
----
- 纯 stdlib + unittest，不要求外部后端存在；
- 通过 ``platform_hint`` 显式模拟 darwin / linux / win，断言 build_report 的
  ``os`` / ``suggest`` 字段、六档能力分档与 fix 命令的平台分支；
- ``_fix_templates`` 直接覆盖 brew（mac）/ apt-dnf（linux）/ winget-choco（win）
  三套安装指令，不依赖本机已装软件。
"""

from __future__ import annotations

import json
import subprocess
import sys
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
DOCTOR = SKILL_DIR / "scripts" / "doctor.py"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import doctor  # noqa: E402

ALLOWED = set(doctor.STATUSES)
BUS_STATES = ("已安装", "未装", "禁用（SKILLBUS_DISABLE=1）")  # lis_skill_bus 探测口径
ALLOWED = ALLOWED.union(BUS_STATES)
CAPABILITIES = ("dxf", "dwg", "pdf_vector", "pdf_raster_ocr", "measure", "qto_linkage", "lis_skill_bus")


class DoctorPlatformBranchTest(unittest.TestCase):
    def _report(self, hint: str) -> dict:
        return doctor.build_report(SKILL_DIR, platform_hint=hint)

    def test_fix_templates_three_platforms(self):
        darwin = doctor._fix_templates("darwin")
        linux = doctor._fix_templates("linux")
        win = doctor._fix_templates("win")
        self.assertIn("brew", darwin["libredwg"])
        self.assertIn("brew", darwin["poppler"])
        self.assertIn("libredwg-tools", linux["libredwg"])
        self.assertIn("poppler-utils", linux["poppler"])
        self.assertIn("apt-get", linux["poppler"])
        self.assertIn("dnf", linux["poppler"])
        self.assertIn("winget", win["libredwg"])
        self.assertIn("winget", win["poppler"])
        self.assertIn("choco", win["poppler"])
        self.assertIn("ODAFileConverter", win["libredwg"])
        self.assertNotIn("brew", linux["poppler"])
        self.assertNotIn("brew", win["poppler"])
        self.assertNotIn("brew", linux["setup"])
        self.assertNotIn("brew", win["setup"])

    def test_report_has_os_and_six_caps_for_each_platform(self):
        for hint in ("darwin", "linux", "win"):
            with self.subTest(platform=hint):
                rep = self._report(hint)
                self.assertEqual(rep["os"], hint)
                self.assertEqual(len(rep["tier0"]["capabilities"]), 7)
                self.assertEqual(
                    sorted(rep["tier0"]["capabilities"].keys()), sorted(CAPABILITIES)
                )
                for cap in rep["tier0"]["capabilities"].values():
                    self.assertIn(cap["status"], ALLOWED)
                self.assertIsInstance(rep["suggest"], dict)
                self.assertEqual(rep["schema"], "cad-file-reader/doctor-v1")

    def test_fix_and_suggest_fields_present_in_tier1(self):
        for hint in ("darwin", "linux", "win"):
            with self.subTest(platform=hint):
                rep = self._report(hint)
                for f in rep["tier1"]["fixes"]:
                    self.assertIsInstance(f["command"], str)
                    self.assertIsInstance(f.get("suggest", ""), str)
                    self.assertIn(f["capability"], CAPABILITIES)
                for key, suggest in rep["suggest"].items():
                    self.assertIsInstance(suggest, str)

    def test_platform_templates_are_pairwise_different(self):
        for key in ("poppler", "libredwg", "setup"):
            darwin = doctor._fix_templates("darwin")[key]
            linux = doctor._fix_templates("linux")[key]
            win = doctor._fix_templates("win")[key]
            self.assertNotEqual(darwin, linux, f"{key} darwin==linux")
            self.assertNotEqual(linux, win, f"{key} linux==win")
            self.assertNotEqual(darwin, win, f"{key} darwin==win")

    def test_json_only_includes_os_and_suggest(self):
        with tempfile.TemporaryDirectory(prefix="cad-doctor-plat-") as td:
            tmp = Path(td)
            proc = subprocess.run(
                [sys.executable, str(DOCTOR), "--json-only"], capture_output=True, text=True,
                timeout=90, cwd=str(tmp),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            rep = json.loads(proc.stdout)
            self.assertIn("os", rep)
            self.assertIn("suggest", rep)
            self.assertEqual(len(rep["tier0"]["capabilities"]), 7)
            self.assertEqual(rep["schema"], "cad-file-reader/doctor-v1")


if __name__ == "__main__":
    unittest.main()
