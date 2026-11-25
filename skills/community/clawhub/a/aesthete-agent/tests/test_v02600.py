# -*- coding: utf-8 -*-
"""test_v02600 — 0.26.0 回归:文档即代码(docgen)+闸门诚实(跳过即点名,绝不静默)。"""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SCRIPTS = os.path.join(ROOT, "scripts")
ENGINE = os.path.join(SCRIPTS, "palette_forge.py")
DOC = os.path.join(ROOT, "docs", "COMMANDS.md")
TMP = tempfile.mkdtemp(prefix="t260_")
PAL = "EFF6E0,E0E6D3,01161E,2E7D5B"


def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


class TestDocgen(unittest.TestCase):
    """文档即代码:COMMANDS.md 来源=各命令 --help 实跑,新鲜度可机械校验。"""

    def test_fresh_check_passes(self):
        r = run([os.path.join(SCRIPTS, "docgen.py"), "--check"])
        self.assertEqual(r.returncode, 0, (r.stdout + r.stderr)[:600])
        self.assertIn("文档新鲜", r.stdout)

    def test_discover_covered_by_when(self):
        sys.path.insert(0, SCRIPTS)
        import docgen
        subs = docgen.discover()
        missing = [c for c in subs if c not in docgen.WHEN]
        self.assertEqual(missing, [], "WHEN 导读缺词条: %s" % missing)
        self.assertGreaterEqual(len(subs), 38)

    def test_commands_md_exists_and_sections(self):
        self.assertTrue(os.path.exists(DOC))
        txt = open(DOC, encoding="utf-8").read()
        self.assertIn("docgen.py 生成", txt)          # 生成标记
        self.assertGreaterEqual(txt.count("\n## "), 40)


class TestGateHonesty(unittest.TestCase):
    """闸门诚实:闸的数据不可读 → 跳过必须记 P1(默认严=红),绝不静默。"""

    PAGE = ("<html><head><style>body{background:#EFF6E0;color:#01161E}"
            "p{font-size:13px}</style></head><body><p>t</p></body></html>")

    def _lint_with_profile(self, profile_path):
        sys.path.insert(0, SCRIPTS)
        import lint_page
        p = os.path.join(TMP, "hp.html")
        open(p, "w", encoding="utf-8").write(self.PAGE)
        lint_page.PROFILE = profile_path
        buf_out, buf_err = io.StringIO(), io.StringIO()
        old_argv = sys.argv
        sys.argv = ["lint_page.py", p, "--palette", PAL]
        code = None
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                lint_page.main()
        except SystemExit as e:
            code = e.code
        finally:
            sys.argv = old_argv
            del sys.modules["lint_page"]
        return code, buf_out.getvalue()

    def test_profile_unreadable_banned_gate_p1(self):
        code, out = self._lint_with_profile(os.path.join(TMP, "nope.json"))
        self.assertEqual(code, 1, out)
        self.assertIn("黑名单族闸跳过", out)
        self.assertIn("P1", out)

    def test_profile_unreadable_render_gate_p1(self):
        # ev.json 存在(剂量闸有数据),但 profile 不可读 => 档案闸跳过点名
        ev = os.path.join(TMP, "ev.json")
        open(ev, "w", encoding="utf-8").write(
            '{"url":"x","theme":"light","bodyBg":"#EFF6E0","minFont":13,'
            '"colors":[{"hex":"2E7D5B","areaRatio":0.05}],"worstPairs":[],"zones":[]}')
        sys.path.insert(0, SCRIPTS)
        import lint_page
        p = os.path.join(TMP, "hr.html")
        open(p, "w", encoding="utf-8").write(self.PAGE)
        lint_page.PROFILE = os.path.join(TMP, "nope.json")
        buf_out = io.StringIO()
        old_argv = sys.argv
        sys.argv = ["lint_page.py", p, "--palette", PAL, "--render", ev]
        code = None
        try:
            with contextlib.redirect_stdout(buf_out):
                lint_page.main()
        except SystemExit as e:
            code = e.code
        finally:
            sys.argv = old_argv
            del sys.modules["lint_page"]
        self.assertEqual(code, 1, buf_out.getvalue())
        self.assertIn("档案闸跳过", buf_out.getvalue())

    def test_healthy_profile_still_green(self):
        code, out = self._lint_with_profile(os.path.join(ROOT, "profile.json"))
        self.assertEqual(code, 0, out)
        self.assertNotIn("闸跳过", out)

    def test_evidence_render_missing_fails_fast(self):
        page = os.path.join(TMP, "er.html")
        open(page, "w", encoding="utf-8").write(self.PAGE)
        r = run([ENGINE, "evidence", page, "--palette", PAL,
                 "--render", os.path.join(TMP, "ghost.json"), "--out", os.path.join(TMP, "er")])
        self.assertEqual(r.returncode, 2, (r.stdout + r.stderr)[:400])
        self.assertIn("--render 文件不存在", r.stderr)

    def test_evidence_render_garbage_fails_fast(self):
        page = os.path.join(TMP, "eg.html")
        open(page, "w", encoding="utf-8").write(self.PAGE)
        bad = os.path.join(TMP, "bad.json")
        open(bad, "w", encoding="utf-8").write("{not json")
        r = run([ENGINE, "evidence", page, "--palette", PAL, "--render", bad,
                 "--out", os.path.join(TMP, "eg")])
        self.assertEqual(r.returncode, 2, (r.stdout + r.stderr)[:400])
        self.assertIn("--render 文件不可解析", r.stderr)


if __name__ == "__main__":
    unittest.main()
