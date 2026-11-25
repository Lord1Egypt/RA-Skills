#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn-borrowing-cost-cn —— 包级测试（零网络、零凭据、零外部依赖）。

跑法：
    python3 tests/test_borrowing_cost.py
    python3 tests/test_borrowing_cost.py -v

退码：0 全过 / 1 有不合。

与 scripts/fixtures/run_fixtures.sh 的分工：那支跑三档判据夹具（判据行为），
本支跑**入口契约**——退码、--demo、零输入可跑、样例与好样夹具同源。
这些是脚本外壳的属性，夹具判不了，但用户第一次上手撞到的正是它们。
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
CHECK = PKG / "scripts" / "check_borrowing_cost.py"
FIX = PKG / "scripts" / "fixtures"


def run(*args, env=None):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if env:
        e.update(env)
    return subprocess.run([sys.executable, "-B", str(args[0]), *map(str, args[1:])],
                          capture_output=True, text=True, env=e, cwd=str(PKG))


class EntryContract(unittest.TestCase):
    """入口脚本的外壳契约：每个用户第一次跑就会撞到的东西。"""

    def test_no_args_exits_two(self):
        r = run(CHECK)
        self.assertEqual(r.returncode, 2, f"无参 rc={r.returncode}")
        self.assertIn("用法", r.stdout)

    def test_missing_file_exits_three(self):
        self.assertEqual(run(CHECK, "/nonexistent/x.md").returncode, 3)

    def test_empty_file_exits_three(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "empty.md"
            p.write_text("", encoding="utf-8")
            self.assertEqual(run(CHECK, p).returncode, 3)

    def test_selftest_green(self):
        r = run(CHECK, "--selftest")
        self.assertEqual(r.returncode, 0, r.stdout[-500:])
        self.assertIn("不合=0", r.stdout)
        self.assertIn("不可判=0", r.stdout)


class ZeroInput(unittest.TestCase):
    """零输入可跑：不给任何数据文件也能跑出可判对错的产物。"""

    def test_demo_runs_without_input(self):
        r = run(CHECK, "--demo")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        self.assertGreater(len(r.stdout), 1000, "样例太短，不足以当成品看")

    def test_demo_output_passes_its_own_checker(self):
        demo = run(CHECK, "--demo").stdout
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "demo.md"
            p.write_text(demo, encoding="utf-8")
            r = run(CHECK, p)
            self.assertEqual(r.returncode, 0, f"样例自身过不了机检：{r.stdout[-400:]}")
            self.assertIn("五道全过", r.stdout)

    def test_demo_is_deterministic(self):
        self.assertEqual(run(CHECK, "--demo").stdout, run(CHECK, "--demo").stdout,
                         "样例每次跑出的字节不同——用户在别处对照会看不懂")

    def test_demo_equals_good_fixture(self):
        """样例与 good 夹具必须同源：两份各自维护迟早漂移，用户看到的成品就与自测不同。"""
        demo = run(CHECK, "--demo").stdout
        fixture = (FIX / "good-borrowing.md").read_text(encoding="utf-8")
        self.assertEqual(demo, fixture)


class GateBehaviour(unittest.TestCase):
    """坏样必须五道齐发——这是「尺子不是恒真」的最小证据。"""

    def test_bad_fixture_fires_all_five(self):
        r = run(CHECK, FIX / "bad-borrowing.md")
        self.assertEqual(r.returncode, 1)
        for code in ("BC-STRUCT", "BC-QUOTE", "BC-CAP", "BC-SPLIT", "BC-LINE"):
            self.assertIn(code, r.stdout, f"坏样没发 {code}")

    def test_good_fixture_stays_clean(self):
        r = run(CHECK, FIX / "good-borrowing.md")
        self.assertEqual(r.returncode, 0, r.stdout[-400:])
        self.assertIn("五道全过", r.stdout)


class DeclaredGapIsSilent(unittest.TestCase):
    """缺口两边都声明了 ⇒ 恒等与两分静默跳过，不重复报「缺失」。

    这是续拍 C 的设计冲突所在：旧实现把「整条跳过」写成一条发条，字面通、语义反，
    会让合规稿被判红。本档钉住它。
    """

    def test_declared_rate_gap_produces_no_finding(self):
        demo = run(CHECK, "--demo").stdout
        line = ("- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」"
                "〔锚：2025 年年报·第 231 页·借款费用〕[S1]")
        self.assertIn(line, demo, "夹具已改形，本档的注入点失效")
        t = demo.replace(line, "- 未取到：一般借款资本化率", 1)
        t = t.replace("- 未取到：无", "- 未取到：一般借款资本化率", 1)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "gap.md"
            p.write_text(t, encoding="utf-8")
            r = run(CHECK, p)
            self.assertEqual(r.returncode, 0, f"已声明的缺口被当成违规：{r.stdout[-400:]}")
            self.assertNotIn("BC-CAP", r.stdout)
            self.assertNotIn("BC-SPLIT", r.stdout)


class RedlineScope(unittest.TestCase):
    """红线只判本件自己写下的字：引文与〔锚／口径／自算〕标签槽是原文与出处。"""

    def test_anchor_subject_name_is_not_a_judgement(self):
        demo = run(CHECK, "--demo").stdout
        t = demo.replace("第 231 页·借款费用", "第 231 页·预计负债", 1)
        self.assertNotEqual(t, demo, "夹具已改形，本档的注入点失效")
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "anchor.md"
            p.write_text(t, encoding="utf-8")
            r = run(CHECK, p)
            self.assertEqual(r.returncode, 0,
                             f"锚里的科目名被判成红线：{r.stdout[-400:]}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
