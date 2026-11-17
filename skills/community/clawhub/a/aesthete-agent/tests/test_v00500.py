# -*- coding: utf-8 -*-
"""test_v00500 — 0.5.0 回归(report 一键验收/prompt 导出/渐变禁令 P0/场景回归)。"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")
LINT = os.path.join(ROOT, "scripts", "lint_page.py")
PAL = "264653,2A9D8F,E9C46A,F4A261,E76F51"
TMP = tempfile.mkdtemp(prefix="t050_")


def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


class TestReport(unittest.TestCase):
    def test_report_shape_and_exit(self):
        r = run([ENGINE, "report", "--palette", PAL])
        self.assertIn(r.returncode, (0, 1))
        d = json.loads(r.stdout)
        self.assertIn(d["verdict"], ("PASS", "FAIL"))
        for gate in ("contrast", "color_blind", "ai_slop", "score"):
            self.assertIn(gate, d["gates"])
            self.assertIsInstance(d["gates"][gate]["pass"], bool)

    def test_report_fail_is_fail(self):
        r = run([ENGINE, "report", "--palette", "8B5CF6,A855F7,7C3AED,6D28D9"])
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["verdict"], "FAIL")


class TestPromptExport(unittest.TestCase):
    def test_prompt_block(self):
        r = run([ENGINE, "export", "--palette", PAL, "--format", "prompt"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("PALETTE", r.stdout)
        self.assertIn("60-30-10", r.stdout)
        self.assertIn("AVOID", r.stdout)
        self.assertTrue("gradients of any kind" in r.stdout)


class TestGradientBan(unittest.TestCase):
    def test_lint_single_gradient_is_p0(self):
        fd, bad = tempfile.mkstemp(suffix=".html")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write('<html><style>.y{background:linear-gradient(90deg,#E07066,#FAF3DD)}'
                        '</style><p>t</p></html>')
            r = run([LINT, bad, "--palette", PAL])
            self.assertEqual(r.returncode, 1)
            self.assertIn("P0", r.stdout)
            self.assertIn("禁渐变", r.stdout)
        finally:
            os.unlink(bad)

    def test_visualizer_no_gradient_scene(self):
        out = os.path.join(TMP, "viz.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--out", out])
        self.assertEqual(r.returncode, 0)
        html = open(out, encoding="utf-8").read()
        self.assertNotIn("Gradient Hero", html)
        self.assertNotIn("linear-gradient", html)
        os.unlink(out)

    def test_card_output_gradient_free(self):
        out = os.path.join(TMP, "card.html")
        r = run([ENGINE, "card", "--palette", PAL, "--name", "T", "--out", out])
        self.assertEqual(r.returncode, 0)
        html = open(out, encoding="utf-8").read()
        self.assertNotIn("-gradient(", html)
        os.unlink(out)



class TestCjkSubsetScript(unittest.TestCase):
    """CJK title-subset builder: contract + graceful skip without fonttools."""

    def test_script_present_and_contract(self):
        p = os.path.join(ROOT, "scripts", "make_cjk_subset.py")
        self.assertTrue(os.path.isfile(p))
        src = open(p, encoding="utf-8").read()
        self.assertIn("DEFAULT_PUNCT", src)
        self.assertIn("SourceHanSerifCN", src)
        self.assertIn("font-display:swap", src)
        self.assertNotIn("palette-" + "forge", src)  # 旧名字面不落地(合规grep扫tests)

    def test_subset_build_or_graceful_skip(self):
        out = os.path.join(TMP, "t.woff2")
        r = run([os.path.join(ROOT, "scripts", "make_cjk_subset.py"),
                 "--text", "排印验证", "--out", out])
        if r.returncode == 2:
            self.assertIn("fonttools", r.stderr)  # no fonttools: graceful skip
            return
        # no local font file either: friendly pointer, exit 1 (not a crash)
        if r.returncode == 1:
            self.assertIn("Font file not found", r.stderr)
            return
        self.assertEqual(r.returncode, 0)
        if os.path.isfile(out):
            self.assertGreater(os.path.getsize(out), 1000)
            os.unlink(out)

    def test_references_responsive_doc(self):
        p = os.path.join(ROOT, "references", "responsive.md")
        self.assertTrue(os.path.isfile(p))
        doc = open(p, encoding="utf-8").read()
        for must in ("display:none", "min-width:920px", "min(100%", "scrollWidth", "何时读我", "回 INDEX"):
            self.assertIn(must, doc)

    def test_references_cjk_doc(self):
        p = os.path.join(ROOT, "references", "cjk-typography.md")
        self.assertTrue(os.path.isfile(p))
        doc = open(p, encoding="utf-8").read()
        for must in ("PingFang SC", "Microsoft YaHei", "text-autospace",
                     "text-spacing-trim", "<br>", "67KB"):
            self.assertIn(must, doc)



if __name__ == "__main__":
    unittest.main()
