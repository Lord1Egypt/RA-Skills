# -*- coding: utf-8 -*-
"""test_v00300 — v0.3.0 新特性回归(主题包/矩阵APCA/语义数据色/critique/doctor/w3c/context)。"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")
THEMES = os.path.join(ROOT, "palettes", "themes.json")
PAL = "264653,2A9D8F,E9C46A,F4A261,E76F51"
TMP = tempfile.mkdtemp(prefix="viz_test_")

def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)

class TestThemes(unittest.TestCase):
    def test_8_packs_valid(self):
        d = json.load(open(THEMES, encoding="utf-8"))
        self.assertGreaterEqual(len(d["themes"]), 8)
        for t in d["themes"]:
            self.assertIn("colors", t); self.assertIn("fonts", t); self.assertIn("voice", t)
    def test_apply_glm(self):
        r = run([ENGINE, "theme", "GLM黄蓝", "--format", "css"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("--c-evidence: #70A0D0", r.stdout)

class TestMatrixSemantic(unittest.TestCase):
    def test_matrix_apca_recommend(self):
        r = run([ENGINE, "matrix", "--palette", PAL, "--method", "apca", "--recommend"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("推荐", r.stdout)
    def test_semantic_cb_safe(self):
        r = run([ENGINE, "semantic", "--count", "6", "--base", "2A9D8F"])
        self.assertEqual(r.returncode, 0)
        self.assertIn(">=0.08", r.stdout)
        hexes = r.stdout.splitlines()[0].split()
        self.assertEqual(len(hexes), 6)

class TestCritiqueDoctor(unittest.TestCase):
    def test_critique_report(self):
        fd, ev = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"theme": "light", "bodyBg": "F7F4EC", "minFont": 13,
                       "colors": [{"hex": "3D405B", "areaRatio": 0.2}],
                       "worstPairs": [{"fg": "8A6A1F", "bg": "F7F4EC", "ratio": 4.6}]}, f)
        out = os.path.join(tempfile.gettempdir(), "crit_v00300.md")
        r = run([ENGINE, "critique", "--palette", PAL, "--evidence", ev, "--out", out])
        self.assertEqual(r.returncode, 0)
        self.assertIn("finding ledger", open(out, encoding="utf-8").read())
        os.unlink(out); os.unlink(ev)
    def test_doctor_green(self):
        r = run([ENGINE, "doctor"])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])

class TestFutureTech(unittest.TestCase):
    def test_apca_slate_on_paper(self):
        r = run([ENGINE, "contrast", "--fg", "3D405B", "--bg", "F7F4EC", "--method", "apca"])
        self.assertIn("正文理想", r.stdout)
    def test_w3c_export(self):
        r = run([ENGINE, "export", "--palette", PAL, "--format", "w3c"])
        d = json.loads(r.stdout)
        self.assertEqual(d["color"]["palette-1"]["$type"], "color")
    def test_context_export(self):
        r = run([ENGINE, "export", "--palette", PAL, "--format", "context"])
        self.assertIn("Guardrails", r.stdout)
        self.assertIn("60-30-10", r.stdout)

class TestVisualizer(unittest.TestCase):
    def test_visualize_six_scenes(self):
        out = os.path.join(TMP, "viz_light.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--name", "T", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
        html = open(out, encoding="utf-8").read()
        for scene in ("Mobile App", "Landing", "Dashboard", "Branding", "Typography", "Pattern",
                      "Data Chart", "E-commerce", "Email", "Editorial"):
            self.assertIn(scene, html)
        os.unlink(out)
    def test_visualize_dark_runs(self):
        out = os.path.join(TMP, "viz_dark.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--theme", "dark", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
        os.unlink(out)
    def test_visualize_variants(self):
        out = os.path.join(TMP, "viz_var.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--variants", "3", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
        html = open(out, encoding="utf-8").read()
        self.assertEqual(html.count("Variant "), 3)
        self.assertEqual(html.count("Mobile App"), 3)
        os.unlink(out)
    def test_visualize_ten_scenes_ladder(self):
        out = os.path.join(TMP, "viz_10.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
        html = open(out, encoding="utf-8").read()
        self.assertIn("Caption", html)
        self.assertIn("Placeholder", html)
        os.unlink(out)
    def test_svg_shuffle_grid(self):
        svg = os.path.join(TMP, "sh.svg")
        open(svg, "w", encoding="utf-8").write(
            '<svg xmlns="http://www.w3.org/2000/svg"><rect fill="#E8E4F8"/>'
            '<circle fill="#7C6BD4"/><rect fill="#3A3160"/><path fill="#FFFFFF"/>'
            '<line stroke="#000000"/></svg>')
        out = os.path.join(TMP, "viz_sh.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--svg", svg, "--shuffle", "3", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
        for f in (svg.replace(".svg", ".recolored.svg"),
                  svg.replace(".svg", ".recolor-2.svg"),
                  svg.replace(".svg", ".recolor-3.svg"),
                  svg.replace(".svg", ".recolor-grid.html")):
            self.assertTrue(os.path.exists(f), f)
        rec = open(svg.replace(".svg", ".recolor-2.svg"), encoding="utf-8").read()
        self.assertIn("#FFFFFF", rec)
        self.assertIn("#000000", rec)
        os.unlink(svg)
        for f in (svg.replace(".svg", ".recolored.svg"), svg.replace(".svg", ".recolor-2.svg"),
                  svg.replace(".svg", ".recolor-3.svg"), svg.replace(".svg", ".recolor-grid.html")):
            if os.path.exists(f):
                os.unlink(f)
        os.unlink(out)
    def test_svg_recolor_keeps_pure_bw(self):
        svg = os.path.join(TMP, "in.svg")
        open(svg, "w", encoding="utf-8").write(
            '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10" '
            'fill="#E8E4F8"/><circle fill="#7C6BD4"/><path fill="#FFFFFF"/>'
            '<line stroke="#000000"/></svg>')
        out = os.path.join(TMP, "viz_svg.html")
        r = run([ENGINE, "visualize", "--palette", PAL, "--svg", svg, "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout[-300:])
        rec = open(svg.replace(".svg", ".recolored.svg"), encoding="utf-8").read()
        self.assertIn("#FFFFFF", rec)
        self.assertIn("#000000", rec)
        self.assertNotIn("#7C6BD4", rec)
        self.assertNotIn("#E8E4F8", rec)
        os.unlink(svg); os.unlink(svg.replace(".svg", ".recolored.svg")); os.unlink(out)

if __name__ == "__main__":
    unittest.main()
