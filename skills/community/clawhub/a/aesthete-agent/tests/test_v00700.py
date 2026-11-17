# -*- coding: utf-8 -*-
"""test_v00700 — 0.7.0 回归:前端语域词典/跨语域方向 directions/证据卷宗 evidence/
候选回传句/数字一致性(文案色板数=实数,用户令:每版必核,机制永固)。"""
import json, os, re, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")
VARIANTS = os.path.join(ROOT, "scripts", "make_variants.py")
LIBRARY = os.path.join(ROOT, "palettes", "palettes.json")
PAL = "555B6E,89B0AE,BEE3DB,FAF9F9,FFD6BA"
TMP = tempfile.mkdtemp(prefix="t070_")


def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def palette_count():
    lib = json.load(open(LIBRARY, encoding="utf-8"))
    return len(lib["palettes"] if isinstance(lib, list) else lib["palettes"])


class TestCountConsistency(unittest.TestCase):
    """用户令(2026-10-19):文案里的色板数必须等于库内实数,每版发布链自动核对。"""

    COPY_SPEC = [
        ("SKILL.md", [r"(\d+)-palette evidence library"]),
        ("SKILL_ZH.md", [r"(\d+) 板实证库"]),
        ("README.md", [r"(\d+)%20curated", r"(\d+) curated palettes"]),
        ("README.zh-CN.md", [r"(\d+)%20curated", r"(\d+) 块精选色板"]),
    ]

    def test_copy_numbers_equal_library(self):
        n = palette_count()
        for fname, patterns in self.COPY_SPEC:
            text = open(os.path.join(ROOT, fname), encoding="utf-8").read()
            for pat in patterns:
                found = re.findall(pat, text)
                self.assertTrue(found, f"{fname} 未找到色板数句式: {pat}")
                for v in found:
                    self.assertEqual(int(v), n, f"{fname} 文案写 {v},库内实数 {n}")

    def test_no_stale_counts(self):
        n = palette_count()
        for fname, _ in self.COPY_SPEC:
            text = open(os.path.join(ROOT, fname), encoding="utf-8").read()
            for m in re.finditer(r"\b(\d{2,4})(?:-palette|%20curated| 板实证| curated palettes| 块精选色板)", text):
                self.assertEqual(int(m.group(1)), n, f"{fname} 残留旧数 {m.group(0)}")


class TestMatchRegisters(unittest.TestCase):
    """0.7.0 主菜:中文审美口语词 → 正确板族。"""

    CASES = [
        ("素雅耐看的落地页", "frontend_soft"),
        ("大气稳重的商务首页", "frontend_deep"),
        ("来一套鲜艳有活力的", "frontend_bold"),
        ("科技感的数据面板", "frontend_tech"),
        ("儿科教学查房课件", "medical_teaching"),
        ("母婴封面", "pediatric_cover"),
    ]

    def test_brief_hits_register(self):
        for brief, reg in self.CASES:
            r = run([ENGINE, "match", "--brief", brief, "--limit", "2"])
            self.assertEqual(r.returncode, 0, brief)
            self.assertIn(f"register={reg}", r.stdout, f"brief={brief!r} 未命中 {reg}")

    def test_soft_prefers_pastel_light(self):
        r = run([ENGINE, "match", "--brief", "素雅清新", "--limit", "5"])
        tops = r.stdout.splitlines()
        body = [ln for ln in tops if ln.startswith("*") or ln.startswith("new")]
        self.assertTrue(any(("pastel" in ln or "light" in ln) for ln in body[:3]),
                        "素雅语域前 3 应含 pastel/light 板")


class TestDirections(unittest.TestCase):
    def test_directions_end_to_end(self):
        out = os.path.join(TMP, "d1")
        r = run([ENGINE, "directions", "--brief", "素雅耐看的落地页", "--n", "3", "--out-dir", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        comp = os.path.join(out, "directions.html")
        self.assertTrue(os.path.exists(comp))
        self.assertIn("data-say", open(comp, encoding="utf-8").read())
        self.assertIn("60-30-10", open(comp, encoding="utf-8").read())
        pages = [f for f in os.listdir(out) if re.fullmatch(r"direction_[A-D]\.html", f)]
        self.assertGreaterEqual(len(pages), 2, "差异铁律:至少 2 个方向整页")

    def test_directions_differ(self):
        out = os.path.join(TMP, "d2")
        r = run([ENGINE, "directions", "--registers", "frontend_soft,frontend_deep", "--out-dir", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        hexsets = set(re.findall(r"\[([0-9A-F ]+)\]", r.stdout))
        self.assertGreaterEqual(len(hexsets), 2, "跨语域方向色板必须互不相同")

    def test_directions_needs_two(self):
        r = run([ENGINE, "directions", "--registers", "nosuchreg"])
        self.assertNotEqual(r.returncode, 0)


class TestVariantsCards(unittest.TestCase):
    def make_pages(self):
        paths = []
        for name, bg, ink in (("a", "FAF9F9", "3D405B"), ("b", "01161E", "EFF6E0")):
            p = os.path.join(TMP, name + ".html")
            open(p, "w", encoding="utf-8").write(
                f"<html><body style='background:#{bg};color:#{ink};font-size:14px'>"
                f"<p>{name} 页面正文样例,字号达标。</p></body></html>")
            paths.append(p)
        return paths

    def test_single_candidate_rejected(self):
        pages = self.make_pages()
        r = run([VARIANTS, pages[0]])
        self.assertEqual(r.returncode, 1)

    def test_cards_meta_and_echo(self):
        pages = self.make_pages()
        cards = os.path.join(TMP, "cards.json")
        json.dump([{"label": "素雅", "hexes": PAL.split(","), "tags": ["light", "pastel"]},
                   {"label": "Deep Pine", "hexes": ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"],
                    "tags": ["cool", "mid"]}], open(cards, "w", encoding="utf-8"))
        out = os.path.join(TMP, "compare.html")
        r = run([VARIANTS] + pages + ["--cards", cards, "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        html = open(out, encoding="utf-8").read()
        self.assertIn("data-say", html)
        self.assertIn("60-30-10", html)
        self.assertIn("#555B6E", html)


class TestEvidence(unittest.TestCase):
    def make_page(self):
        p = os.path.join(TMP, "good.html")
        open(p, "w", encoding="utf-8").write(
            "<html><head><style>body{background:#FAF9F9;font-family:system-ui}"
            ".card{background:#FFFFFF;color:#3D405B;font-size:15px;padding:18px}</style></head>"
            "<body><div class='card'><h1 style='font-size:24px;color:#3D405B'>素雅落地页样例</h1>"
            "<p>正文 15px,墨色对浅纸,四道闸应当全过。</p></div></body></html>")
        return p

    def test_evidence_pass(self):
        page = self.make_page()
        out = os.path.join(TMP, "good")
        r = run([ENGINE, "evidence", page, "--palette", PAL, "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ev = json.load(open(out + ".json", encoding="utf-8"))
        self.assertEqual(ev["verdict"], "PASS")
        self.assertIn("summary", ev["report"])           # 0.8.0 量化叙事
        self.assertEqual(ev["report"]["summary"]["gates_passed"], "4/4")
        self.assertRegex(ev["fingerprint"], r"^[0-9a-f]{64}$")  # 指纹绑定(零模型信任闸)
        self.assertRegex(ev["page_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn("gates", ev["report"])
        self.assertTrue(os.path.exists(out + ".html"))
        self.assertIn("四道机械闸", open(out + ".html", encoding="utf-8").read())

    def test_evidence_fail_blocked(self):
        page = os.path.join(TMP, "bad.html")
        open(page, "w", encoding="utf-8").write(
            "<html><body style='background:#7C3AED;color:#FFFFFF;font-size:15px'><p>紫渐变底板样例</p></body></html>")
        out = os.path.join(TMP, "bad")
        r = run([ENGINE, "evidence", page, "--palette", "8B5CF6,A855F7,7C3AED,6D28D9,5B21B6",
                 "--out", out])
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.load(open(out + ".json", encoding="utf-8"))["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
