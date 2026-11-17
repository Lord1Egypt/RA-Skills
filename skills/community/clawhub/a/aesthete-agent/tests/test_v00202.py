# -*- coding: utf-8 -*-
"""test_v00202 — v0.2.2 六模块改进回归(desc 需求词前置/能力×边界/slop 退出码/selftest)。"""
import json, os, re, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")
LINT = os.path.join(ROOT, "scripts", "lint_page.py")
SKILL = os.path.join(ROOT, "SKILL.md")
SKILL_ZH = os.path.join(ROOT, "SKILL_ZH.md")
PALETTE = "F4F1DE,E07A5F,3D405B,81B29A,F2CC8F"

def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)

class TestDescZH(unittest.TestCase):
    def setUp(self):
        self.fm = open(SKILL_ZH, encoding="utf-8").read().split("---")[1]
        self.desc = re.search(r"description: (.*)", self.fm).group(1)
    def test_len_le_1024(self):
        self.assertLessEqual(len(self.desc), 1024)
    def test_demand_words_in_first_120(self):
        head = self.desc[:120]
        for w in ("配色生成", "调色板", "前端美学"):
            self.assertIn(w, head, f"需求词 {w} 不在头 120 字符")
    def test_brand_not_in_first_60(self):
        self.assertNotIn("Aesthete", self.desc[:60], "品牌词不得在首 60 字符")
    def test_skip_when_present(self):
        self.assertIn("Skip when", self.desc)
        for w in ("翻译", "润色"):
            self.assertIn(w, self.desc.split("Skip when", 1)[1])
    def test_version_not_decreased(self):
        v = float(re.search(r"version: ([\d.]+)", self.fm).group(1).rsplit(".", 1)[0].replace(".", ""))
        self.assertGreaterEqual(v, 2.2, "版本只增不减")

class TestDescEN(unittest.TestCase):
    def setUp(self):
        self.fm = open(SKILL, encoding="utf-8").read().split("---")[1]
        self.desc = re.search(r"description: (.*)", self.fm).group(1)
    def test_len_le_1024(self):
        self.assertLessEqual(len(self.desc), 1024)
    def test_demand_words_in_first_120(self):
        head = self.desc[:120]
        for w in ("Color palette generation", "frontend aesthetics", "UI color schemes"):
            self.assertIn(w, head, f"demand word {w} not in first 120 chars")
    def test_brand_not_in_first_60(self):
        self.assertNotIn("Aesthete", self.desc[:60], "brand word must not appear in first 60 chars")
    def test_skip_when_present(self):
        self.assertIn("Skip when", self.desc)
    def test_body_english_anchors(self):
        s = open(SKILL, encoding="utf-8").read()
        self.assertIn("Capability × Boundary Quick Reference", s)
        self.assertIn("30-second routing", s)
        self.assertNotIn("配色生成、调色板方案", s.split("---")[2][:500], "英文主文件正文不得残留中文版 desc")

class TestEngine(unittest.TestCase):
    def test_wcag_boundaries(self):
        r = run([ENGINE, "contrast", "--fg", "767676", "--bg", "FFFFFF"])
        self.assertIn("AA PASS", r.stdout)
        r2 = run([ENGINE, "contrast", "--fg", "777777", "--bg", "FFFFFF"])
        self.assertIn("AA FAIL", r2.stdout)
    def test_slop_exit_nonzero_on_hit(self):
        r = run([ENGINE, "slop", "--palette", "3B82F6,8B5CF6,EC4899"])
        self.assertEqual(r.returncode, 1)
        self.assertIn("MEDIAN-TRAP", r.stdout)
    def test_selftest_green(self):
        r = run([ENGINE, "selftest"])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
    def test_match_reports_register(self):
        r = run([ENGINE, "match", "--brief", "儿科临床教学页", "--limit", "3"])
        self.assertIn("register=", r.stdout)
    def test_house_and_slop_in_help(self):
        r = run([ENGINE, "--help"])
        self.assertIn("house", r.stdout)
        self.assertIn("slop", r.stdout)

class TestLint(unittest.TestCase):
    def test_bad_fixture_flags(self):
        fd, bad = tempfile.mkstemp(suffix=".html")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write('<html><style>.x{color:#3B82F6;font-size:9px}'
                        '.y{background:linear-gradient(90deg,#8B5CF6,#A855F7)}</style>'
                        '<p class="x">t</p></html>')
            r = run([LINT, bad, "--palette", PALETTE])
            self.assertEqual(r.returncode, 1)
            self.assertIn("P0", r.stdout)
        finally:
            os.unlink(bad)

class TestCapabilityBoundaryDoc(unittest.TestCase):
    def test_table_present(self):
        s = open(SKILL_ZH, encoding="utf-8").read()
        self.assertIn("能力×边界速查", s)
        self.assertIn("非目标", s)
    def test_routing_table_present(self):
        s = open(SKILL_ZH, encoding="utf-8").read()
        self.assertIn("30 秒路由", s)

if __name__ == "__main__":
    unittest.main()
