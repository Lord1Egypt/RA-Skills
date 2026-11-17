#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""包级测试：跑夹具判不了的外壳属性（入口契约、零输入、埋点、骨架不出空壳）。"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
CHECK = PKG / "scripts" / "check_inquiry_letter.py"
OUTLINE = PKG / "scripts" / "make_outline.py"
GOOD = PKG / "scripts" / "fixtures" / "good-inquiry.md"


def run(args, env=None):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if env:
        e.update(env)
    return subprocess.run([sys.executable, "-B"] + [str(a) for a in args],
                          capture_output=True, text=True, env=e)


class TestEntryContract(unittest.TestCase):
    def test_help_exits_zero(self):
        for scr in (CHECK, OUTLINE):
            r = run([scr, "--help"])
            self.assertEqual(r.returncode, 0, "%s --help rc=%d" % (scr.name, r.returncode))

    def test_no_args_exits_two(self):
        for scr in (CHECK, OUTLINE):
            r = run([scr])
            self.assertEqual(r.returncode, 2, "%s 无参应 rc=2，实得 %d" % (scr.name, r.returncode))

    def test_missing_file_exits_three(self):
        r = run([CHECK, "/nonexistent/x.md"])
        self.assertEqual(r.returncode, 3)

    def test_empty_file_exits_three(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("")
            p = f.name
        try:
            self.assertEqual(run([CHECK, p]).returncode, 3)
        finally:
            os.unlink(p)


class TestSelftests(unittest.TestCase):
    def test_check_selftest_green(self):
        r = run([CHECK, "--selftest"])
        self.assertEqual(r.returncode, 0, r.stdout[-400:])
        self.assertIn("不合=0", r.stdout)

    def test_outline_selftest_green(self):
        r = run([OUTLINE, "--selftest"])
        self.assertEqual(r.returncode, 0, r.stdout[-400:])
        self.assertIn("不合=0", r.stdout)


class TestDemo(unittest.TestCase):
    def test_demo_needs_no_input_and_passes_own_checker(self):
        r = run([CHECK, "--demo"])
        self.assertEqual(r.returncode, 0)
        self.assertGreater(len(r.stdout), 500, "--demo 产出过短")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(r.stdout)
            p = f.name
        try:
            c = run([CHECK, p])
            self.assertEqual(c.returncode, 0, c.stdout[-500:])
            self.assertIn("六道全过", c.stdout)
        finally:
            os.unlink(p)

    def test_demo_is_byte_reproducible(self):
        a = run([CHECK, "--demo"]).stdout
        b = run([CHECK, "--demo"]).stdout
        self.assertEqual(a, b, "--demo 两次产出不一致")

    def test_demo_equals_good_fixture(self):
        """好样夹具必须逐字节等于 --demo 的产出——两份各自维护迟早漂移。"""
        demo = run([CHECK, "--demo"]).stdout
        self.assertEqual(demo, GOOD.read_text(encoding="utf-8"),
                         "fixtures/good-inquiry.md 与 --demo 产出不一致")


class TestOutlineBehaviour(unittest.TestCase):
    def test_empty_listing_exits_one_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            listing = Path(d) / "l.jsonl"
            listing.write_text("\n\n", encoding="utf-8")
            out = Path(d) / "o.md"
            r = run([OUTLINE, listing, out])
            self.assertEqual(r.returncode, 1)
            self.assertFalse(out.exists(), "空清单不该出空壳")

    def test_bad_lines_named_good_lines_kept(self):
        with tempfile.TemporaryDirectory() as d:
            listing = Path(d) / "l.jsonl"
            listing.write_text(
                '{"title": "好行", "url": "https://e.com/a", "asof": "2026-11-10"}\n'
                '{"title": "缺键"}\n', encoding="utf-8")
            out = Path(d) / "o.md"
            r = run([OUTLINE, listing, out])
            self.assertEqual(r.returncode, 1, "有坏行时退码应为 1")
            self.assertIn("坏行 第 2 行", r.stderr)
            self.assertTrue(out.exists(), "好行照收，骨架仍应写出")
            self.assertIn("好行", out.read_text(encoding="utf-8"))

    def test_skeleton_does_not_pass_the_checker(self):
        """骨架故意过不了机检，是设计不是待修。"""
        with tempfile.TemporaryDirectory() as d:
            listing = Path(d) / "l.jsonl"
            listing.write_text(
                '{"title": "回复公告", "url": "https://e.com/a", "asof": "2026-11-10"}\n',
                encoding="utf-8")
            out = Path(d) / "o.md"
            run([OUTLINE, listing, out])
            c = run([CHECK, out])
            self.assertEqual(c.returncode, 1, "骨架不该过机检")


class TestFirstRunMarker(unittest.TestCase):
    def test_marker_written(self):
        with tempfile.TemporaryDirectory() as home:
            r = run([CHECK, "--demo"], env={"HOME": home})
            self.assertEqual(r.returncode, 0)
            marks = list((Path(home) / ".cue-usage").glob("cue-cn-inquiry-letter-reply-*"))
            self.assertEqual(len(marks), 1, "埋点应落一枚")

    def test_marker_does_not_multiply_same_day(self):
        with tempfile.TemporaryDirectory() as home:
            for _ in range(3):
                run([CHECK, "--demo"], env={"HOME": home})
            marks = list((Path(home) / ".cue-usage").glob("cue-cn-inquiry-letter-reply-*"))
            self.assertEqual(len(marks), 1, "同日多次跑只留一枚")

    def test_marker_failure_is_silent(self):
        """家目录不可写时静默跳过：不报错、不改退码。"""
        with tempfile.TemporaryDirectory() as home:
            ro = Path(home) / ".cue-usage"
            ro.mkdir()
            ro.chmod(0o500)
            try:
                r = run([CHECK, "--demo"], env={"HOME": home})
                self.assertEqual(r.returncode, 0, "埋点失败不该改进程退码")
                self.assertEqual(r.stderr, "", "埋点失败不该吐杂音")
            finally:
                ro.chmod(0o700)

    def test_marker_without_home_is_silent(self):
        env = {k: v for k, v in os.environ.items() if k != "HOME"}
        e = dict(env, PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-B", str(CHECK), "--demo"],
                           capture_output=True, text=True, env=e)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
