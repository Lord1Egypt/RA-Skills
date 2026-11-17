#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for scripts/setup.py（跨平台安装器；仅本地检测，不做网络/写操作）。

说明
----
- 纯 stdlib；不运行真实 pip 安装，避免依赖网络与污染 vendor；
- 覆盖 find_python_interpreter 能找到解释器、dry_run 输出平台/依赖清单；
- 不改变现有 setup.sh / install_vendor.sh 调用约定。
"""
from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import setup  # noqa: E402


class SetupDryRunTest(unittest.TestCase):
    def test_find_python_finds_something(self):
        py = setup.find_python_interpreter()
        self.assertTrue(py)
        self.assertTrue(Path(py).is_file() or py == "python")

    def test_dry_run_outputs_expected_fields(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            setup.dry_run()
        text = out.getvalue()
        for key in ("platform.os", "python", "vendor_dir", "packages", "mode"):
            self.assertIn(key, text)

    def test_min_version_field(self):
        self.assertGreaterEqual(setup.MIN_PY, (3, 10))

    def test_core_packages_nonempty(self):
        self.assertTrue(setup.CORE_PACKAGES)
        for pkg in setup.CORE_PACKAGES:
            self.assertTrue(any(x.lower().split("==")[0] == pkg.lower() for x in setup.PIP_PACKAGES), f"{pkg} not in {setup.PIP_PACKAGES}")


if __name__ == "__main__":
    unittest.main()
