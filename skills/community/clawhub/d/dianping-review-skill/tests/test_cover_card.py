import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import cover_card as cover  # noqa: E402

FACTS = {"notes": ["6km", "3h", "陶罐2个100元"]}


class ValidateCoverTest(unittest.TestCase):
    def spec(self, **kw):
        base = {"title": "<大邑 · 赵公山东线>",
                "lines": ["起点：赵公山游客中心", "距离：约 6km（往返）", "用时：3h",
                          "亮点：森林氧吧、道观群、溪水相伴、入门级登山。"]}
        base.update(kw)
        return base

    def test_normalizes_brackets_and_default_picks(self):
        out = cover.validate_cover(self.spec(title="大邑 · 赵公山东线"), 4, FACTS)
        self.assertEqual(out["title"], "<大邑 · 赵公山东线>")
        self.assertEqual(out["picks"], [0, 1, 2])

    def test_orphan_number_blocked(self):
        with self.assertRaises(cover.CoverError):
            cover.validate_cover(self.spec(lines=["用时：9h", "亮点：溪水相伴"]), 1, FACTS)

    def test_needs_dot_and_two_lines(self):
        with self.assertRaises(cover.CoverError):
            cover.validate_cover(self.spec(title="<赵公山>"), 1, FACTS)
        with self.assertRaises(cover.CoverError):
            cover.validate_cover(self.spec(lines=["只有一行：溪水"]), 1, FACTS)

    def test_paint_three_up(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            paths = []
            for i, color in enumerate(((80, 140, 200), (30, 80, 40), (140, 100, 60))):
                p = tmp / f"{i}.jpg"
                Image.new("RGB", (800, 500), color).save(p, quality=85)
                paths.append(p)
            spec = cover.validate_cover(self.spec(), 3, FACTS)
            out = tmp / "01-封面.jpg"
            cover.paint_cover(paths, spec, out)
            im = Image.open(out).convert("RGB")
            self.assertEqual(im.size, (1080, 1440))
            band = list(im.crop((36, 480, 1040, 1100)).get_flattened_data())
            whites = sum(1 for r, g, b in band if r > 240 and g > 240 and b > 240)
            golds = sum(1 for r, g, b in band if r > 180 and g > 160 and b < 160 and r > b + 40)
            self.assertGreater(whites, 80)
            self.assertGreater(golds, 80)


if __name__ == "__main__":
    unittest.main()
