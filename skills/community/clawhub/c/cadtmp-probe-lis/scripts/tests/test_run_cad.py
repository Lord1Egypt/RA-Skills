#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for scripts/run_cad.py（Python 统一入口分发层）。

说明
----
- 纯 stdlib + unittest，不真正运行解析业务（避免依赖 vendor）；
- 覆盖 --list 清单、未知子命令 exit 2、--help、全局 flag 透传；
- 不改变任何业务 .py / .sh 的调用约定。
"""

from __future__ import annotations

import contextlib
import io
import sys

import unittest
from unittest import mock
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import run_cad  # noqa: E402


class RunCadEntryTest(unittest.TestCase):
    def test_list_includes_cad_scan(self):
        with contextlib.redirect_stdout(io.StringIO()):
            got = run_cad.main(["--list"])
        self.assertEqual(got, 0)
        commands = run_cad.list_subcommands()
        self.assertIn("cad_scan", commands)
        self.assertIn("read_cad", commands)

    def test_help_returns_zero(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_cad.main(["--help"]), 0)

    def test_unknown_subcommand_returns_two(self):
        with mock.patch.object(run_cad, "_prefer_runtime_python", return_value=None), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_cad.main(["this_cmd_does_not_exist"]), 2)

    def test_global_concise_flag_translates_env(self):
        old = dict(run_cad.os.environ.get("CAD_CONCISE", "")) if "CAD_CONCISE" in run_cad.os.environ else None
        try:
            # 需要一个不存在的子命令来快速命中“未知并 exit 2”，同时验证 flag 已翻译。
            with mock.patch.object(run_cad, "_prefer_runtime_python", return_value=None):
                rc = run_cad.main(["--concise", "this_cmd_does_not_exist"])
            self.assertEqual(rc, 2)
            self.assertEqual(run_cad.os.environ.get("CAD_CONCISE"), "1")
        finally:
            if old is not None:
                run_cad.os.environ["CAD_CONCISE"] = old
            else:
                run_cad.os.environ.pop("CAD_CONCISE", None)

    def test_full_and_with_evidence_translate_env(self):
        for flag in ("--full", "--with-evidence"):
            try:
                with mock.patch.object(run_cad, "_prefer_runtime_python", return_value=None), \
                        contextlib.redirect_stdout(io.StringIO()):
                    run_cad.main([flag, "this_cmd_does_not_exist"])
                self.assertEqual(run_cad.os.environ.get("CAD_CONCISE"), "0")
            finally:
                run_cad.os.environ.pop("CAD_CONCISE", None)


if __name__ == "__main__":
    unittest.main()
