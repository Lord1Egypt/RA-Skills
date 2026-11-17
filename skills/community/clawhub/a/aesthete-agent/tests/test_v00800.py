# -*- coding: utf-8 -*-
"""test_v00800 — 0.8.0 回归:一键图片验收 check-image/主题包 10/语域词表扩容/量化叙事。"""
import io, json, os, re, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")
TMP = tempfile.mkdtemp(prefix="t080_")


def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def make_image(path, cols):
    from PIL import Image
    w = 100
    im = Image.new("RGB", (w * len(cols), 100))
    for i, c in enumerate(cols):
        for x in range(i * w, (i + 1) * w):
            for y in range(100):
                im.putpixel((x, y), c)
    im.save(path)


class TestCheckImage(unittest.TestCase):
    PAL_COLS = [(85, 91, 110), (137, 176, 174), (190, 227, 219), (250, 249, 249), (255, 214, 186)]

    def setUp(self):
        try:
            import PIL  # noqa: F401
            self.have_pil = True
        except ImportError:
            self.have_pil = False

    def test_check_image_pass(self):
        if not self.have_pil:
            self.skipTest("Pillow 未安装")
        img = os.path.join(TMP, "multi.png")
        make_image(img, self.PAL_COLS)
        r = run([ENGINE, "check-image", img])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["verdict"], "PASS")
        self.assertGreaterEqual(len(d["palette"]), 3)
        self.assertRegex(d["image_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(d["report"]["summary"]["gates_passed"], "4/4")

    def test_check_image_missing_file(self):
        r = run([ENGINE, "check-image", os.path.join(TMP, "nope.png")])
        self.assertEqual(r.returncode, 2)


class TestThemes(unittest.TestCase):
    def test_ten_themes_with_new_packs(self):
        d = json.load(open(os.path.join(ROOT, "palettes", "themes.json"), encoding="utf-8"))
        themes = d["themes"] if isinstance(d, dict) else d
        self.assertGreaterEqual(len(themes), 11)
        names_en = {t.get("name_en") for t in themes}
        self.assertIn("Deep Pine", names_en)      # 用户点名板升主题包
        self.assertIn("Morning Pastel", names_en)  # 素雅标杆升主题包
        for t in themes:
            for k in ("name", "use_when", "colors", "fonts", "voice"):
                self.assertIn(k, t, f"主题缺字段 {k}: {t.get('name_en')}")


class TestLexiconExpansion(unittest.TestCase):
    """0.8.0 语域词表扩容:口语审美词第二轮。"""

    CASES = [
        ("奶油莫兰迪风的博客", "frontend_soft"),
        ("轻奢质感的品牌首页", "frontend_deep"),
        ("元气明快的活动页", "frontend_bold"),
        ("赛博科幻感的控制台", "frontend_tech"),
    ]

    def test_expanded_words_hit_registers(self):
        for brief, reg in self.CASES:
            r = run([ENGINE, "match", "--brief", brief, "--limit", "2"])
            self.assertEqual(r.returncode, 0, brief)
            self.assertIn(f"register={reg}", r.stdout, f"brief={brief!r} 未命中 {reg}")


class TestScaffold(unittest.TestCase):
    def test_scaffold_theme_end_to_end(self):
        out = os.path.join(TMP, "scaffold-test.html")
        r = run([ENGINE, "scaffold", "--theme", "Deep Pine",
                 "--recipe", "DARK-FOUR-ACT",
                 "--brand", "测试木作", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(out))
        html = io.open(out, encoding="utf-8").read()
        self.assertIn("night-hero", html)
        self.assertNotIn("linear-gradient", html)
        self.assertIn("测试木作", html)
        # 产出自身过闸:lint 零 P0(声明色板从 stdout 取)
        pal = re.search(r"主题色板\(声明\): ([0-9A-F,]+)", r.stdout).group(1)
        lint = run([os.path.join(ROOT, "scripts", "lint_page.py"), out, "--palette", pal])
        self.assertEqual(lint.returncode, 0, lint.stdout)

    def test_scaffold_unknown_theme(self):
        r = run([ENGINE, "scaffold", "--theme", "Nope"])
        self.assertEqual(r.returncode, 2)


class TestScene(unittest.TestCase):
    PAL = "01161E,EFF6E0,124559,AEC3B0,52636E"

    def test_scene_wallet_end_to_end(self):
        out = os.path.join(TMP, "scene-wallet.html")
        r = run([ENGINE, "scene", "--kind", "wallet", "--theme", "Deep Pine",
                 "--palette", self.PAL, "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        html = io.open(out, encoding="utf-8").read()
        self.assertIn("p-balance", html)          # 钱包场景结构
        self.assertNotIn("linear-gradient", html)  # 零渐变
        pal = re.search(r"主题色板\(声明\): ([0-9A-F,]+)", r.stdout).group(1)
        lint = run([os.path.join(ROOT, "scripts", "lint_page.py"), out,
                    "--palette", pal, "--floor", "9"])   # 设备 mockup 微字豁免
        self.assertEqual(lint.returncode, 0, lint.stdout)

    def test_scene_purple_guard(self):
        out = os.path.join(TMP, "scene-purple.html")
        r = run([ENGINE, "scene", "--kind", "landing", "--palette",
                 "7C3AED,A855F7,DDD6FE,1E1B4B", "--out", out])
        self.assertEqual(r.returncode, 1)
        self.assertIn("AI 默认紫守门", r.stderr)

    def test_scene_unknown_kind(self):
        r = run([ENGINE, "scene", "--kind", "nope", "--palette", "555B6E,89B0AE,BEE3DB"])
        self.assertEqual(r.returncode, 2)


class TestQuantifiedVerdict(unittest.TestCase):
    def test_fail_summary_counts_findings(self):
        r = run([ENGINE, "report", "--palette", "8B5CF6,A855F7,7C3AED"])
        d = json.loads(r.stdout)
        self.assertEqual(d["verdict"], "FAIL")
        self.assertIn("summary", d)
        self.assertGreater(d["summary"]["issues_caught"], 0)
        self.assertIn("fingerprint", d)


if __name__ == "__main__":
    unittest.main()
