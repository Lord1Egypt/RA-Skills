import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import writer_bridge  # noqa: E402
from content_gate import check  # noqa: E402

CLEAN = ("周末下午我们两个人过来，等位 15 分钟。我点了脏脏拿铁 32 元，奶味重但不腻。"
         "你们去三圣乡一般喝咖啡还是喝茶？")
WRITER = writer_bridge.find_writer_dir()


def get(results, name):
    return next(r for r in results if r["check"] == name)


def fake_writer(version: str) -> Path:
    d = Path(tempfile.mkdtemp()) / writer_bridge.WRITER_SLUG
    (d / "scripts").mkdir(parents=True)
    for name in writer_bridge.REQUIRED:
        (d / "scripts" / name).write_text("print('{}')\n", encoding="utf-8")
    (d / "_meta.json").write_text(json.dumps({"version": version}), encoding="utf-8")
    return d


class DependencyTest(unittest.TestCase):
    def test_missing_writer_blocks(self):
        with mock.patch.object(writer_bridge, "_candidates", lambda explicit=None: iter([Path("/nonexistent")])):
            res = writer_bridge.writer_checks(CLEAN)
        dep = get(res, "写作规范依赖")
        self.assertFalse(dep["pass"])
        self.assertEqual(dep["level"], "block")
        self.assertIn("clawhub install hekouwang-writer-skill", dep["detail"])

    def test_old_writer_blocks(self):
        d = fake_writer("1.0.0")
        res = writer_bridge.writer_checks(CLEAN, writer_dir=str(d))
        self.assertFalse(get(res, "写作规范依赖")["pass"])
        self.assertIn(">= 1.1.0", get(res, "写作规范依赖")["detail"])

    def test_missing_writer_fails_gate(self):
        with mock.patch.object(writer_bridge, "_candidates", lambda explicit=None: iter([Path("/nonexistent")])):
            self.assertFalse(check("", CLEAN, "review", None)["pass"])

    def test_version_parse(self):
        self.assertEqual(writer_bridge._parse_version("1.10.2"), (1, 10, 2))
        self.assertEqual(writer_bridge._parse_version("2"), (2, 0, 0))


@unittest.skipIf(WRITER is None, "未安装 hekouwang-writer-skill")
class WriterRulesTest(unittest.TestCase):
    def test_clean_text_passes(self):
        res = writer_bridge.writer_checks(CLEAN)
        self.assertTrue(all(r["pass"] for r in res if r["level"] == "block"), res)

    def test_sawdust_over_density_blocks(self):
        r = get(writer_bridge.writer_checks(CLEAN + "其实非常好喝。"), "写作规范·锯末词")
        self.assertFalse(r["pass"])
        self.assertEqual(r["level"], "block")

    def test_long_sentence_blocks(self):
        long_sent = ("我们觉得下午三点以后去比较合适因为中午的时候人太多了而且没有座位还要等很久很久"
                     "才能轮到我们点单所以千万别在中午的时候过去排队浪费时间。")
        r = get(writer_bridge.writer_checks(CLEAN + long_sent), "写作规范·必拆长句")
        self.assertFalse(r["pass"])

    def test_mobile_blocks(self):
        r = get(writer_bridge.writer_checks(CLEAN + "老板电话 13812345678。"), "写作规范·敏感信息")
        self.assertFalse(r["pass"])

    def test_semicolon_only_warns(self):
        r = get(writer_bridge.writer_checks("奶味重；不腻。" + CLEAN), "写作规范·分号")
        self.assertFalse(r["pass"])
        self.assertEqual(r["level"], "warn")


if __name__ == "__main__":
    unittest.main()
