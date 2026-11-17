#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn-segment-report-cn —— 包级测试（零网络、零凭据、零外部依赖）。

跑法：
    python3 tests/test_segment.py
    python3 tests/test_segment.py -v

退码：0 全过 / 1 有不合。

与 scripts/fixtures/run_fixtures.sh 的分工：那支跑三档判据夹具（判据行为），
本支跑**入口契约**——退码、--demo、埋点、零输入可跑。这些是脚本外壳的属性，
夹具判不了，但用户第一次上手撞到的正是它们。
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
CHECK = PKG / "scripts" / "check_segment.py"
SLUG = "cue-cn-segment-report-cn"


def run(*args, env=None, cwd=None):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if env:
        e.update(env)
    return subprocess.run([sys.executable, "-B", str(args[0]), *map(str, args[1:])],
                          capture_output=True, text=True, env=e, cwd=str(cwd or PKG))


class EntryContract(unittest.TestCase):
    """入口脚本的外壳契约：每个用户第一次跑就会撞到的东西。"""

    def test_help_exits_zero(self):
        r = run(CHECK, "--help")
        self.assertEqual(r.returncode, 0, f"--help rc={r.returncode}")
        self.assertIn("usage", r.stdout.lower())

    def test_usage_error_exits_two(self):
        r = run(CHECK)
        self.assertEqual(r.returncode, 2, f"无参 rc={r.returncode}")

    def test_missing_file_exits_three(self):
        self.assertEqual(run(CHECK, "/nonexistent/x.md").returncode, 3)

    def test_empty_file_exits_three(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "empty.md"
            p.write_text("", encoding="utf-8")
            self.assertEqual(run(CHECK, p).returncode, 3)

    def test_selftest_green(self):
        self.assertEqual(run(CHECK, "--selftest").returncode, 0)


class ZeroInput(unittest.TestCase):
    """零输入可跑：不给任何数据文件也能跑出可判对错的产物。"""

    def test_demo_runs_without_input(self):
        r = run(CHECK, "--demo")
        self.assertEqual(r.returncode, 0)
        self.assertGreater(len(r.stdout), 1000, "样例太短，不足以当成品看")

    def test_demo_output_passes_its_own_checker(self):
        demo = run(CHECK, "--demo").stdout
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "demo.md"
            p.write_text(demo, encoding="utf-8")
            r = run(CHECK, p)
            self.assertEqual(r.returncode, 0, f"样例自身过不了机检：{r.stdout[-400:]}")
            self.assertIn("零发条", r.stdout)

    def test_demo_is_deterministic(self):
        self.assertEqual(run(CHECK, "--demo").stdout, run(CHECK, "--demo").stdout,
                         "样例每次跑出的字节不同——用户在别处对照会看不懂")

    def test_demo_equals_good_fixture(self):
        """样例与 good 夹具必须同源：两份各自维护迟早漂移，用户看到的成品就与自测不同。"""
        demo = run(CHECK, "--demo").stdout
        fixture = (PKG / "scripts" / "fixtures" / "good-segment.md").read_text(encoding="utf-8")
        self.assertEqual(demo, fixture)


class GateBehaviour(unittest.TestCase):
    """坏样必须五道齐发——这是「尺子不是恒真」的最小证据。"""

    def test_bad_fixture_fires_all_five(self):
        r = run(CHECK, PKG / "scripts" / "fixtures" / "bad-segment.md")
        self.assertEqual(r.returncode, 1)
        for code in ("SG-STRUCT", "SG-QUOTE", "SG-NOSELF", "SG-GAP", "SG-LINE"):
            self.assertIn(code, r.stdout, f"坏样没发 {code}")

    def test_good_fixture_stays_clean(self):
        r = run(CHECK, PKG / "scripts" / "fixtures" / "good-segment.md")
        self.assertEqual(r.returncode, 0, r.stdout[-400:])


class FirstRunBeacon(unittest.TestCase):
    """首次运行埋点：落一枚空文件，且失败时绝不拖垮主流程。"""

    def test_beacon_written_on_first_run(self):
        with tempfile.TemporaryDirectory() as td:
            r = run(CHECK, "--demo", env={"HOME": td})
            self.assertEqual(r.returncode, 0, "埋点失败不许影响主流程")
            hits = list((Path(td) / ".cue-usage").glob(f"{SLUG}-*"))
            self.assertEqual(len(hits), 1, f"应恰落一枚埋点，实得 {hits}")
            self.assertEqual(hits[0].stat().st_size, 0, "埋点须是空文件")

    def test_beacon_does_not_multiply_same_day(self):
        with tempfile.TemporaryDirectory() as td:
            for _ in range(3):
                run(CHECK, "--demo", env={"HOME": td})
            hits = list((Path(td) / ".cue-usage").glob(f"{SLUG}-*"))
            self.assertEqual(len(hits), 1, f"同一天跑三次应只留一枚，实得 {len(hits)}")

    def test_beacon_failure_is_silent(self):
        with tempfile.TemporaryDirectory() as td:
            os.chmod(td, 0o500)                 # 家目录做成只读
            try:
                r = run(CHECK, "--demo", env={"HOME": td})
                self.assertEqual(r.returncode, 0)
                self.assertEqual(r.stderr, "", f"埋点失败不许吐杂音：{r.stderr[:200]}")
            finally:
                os.chmod(td, 0o700)

    def test_no_home_is_silent(self):
        e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        e.pop("HOME", None)
        r = subprocess.run([sys.executable, "-B", str(CHECK), "--demo"],
                           capture_output=True, text=True, env=e, cwd=str(PKG))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "", f"无 HOME 不许吐杂音：{r.stderr[:200]}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
