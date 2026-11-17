#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布前脱敏守护的行为测试：抓得住工程量，也不得误伤版本号和耗时。"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import cad_release_scrub as scrub  # noqa: E402

DIRTY = """# 台账说明

- 首层参考量 274.446 m3，CAD 覆盖 273.2436 m3。
- 标高 -1.060~2.810 对应首层。
- 源图摘要 35a1519576792ec46bdbb4711cd1a0eb。
- 结果见 outputs/阶段四十九-首层混凝土分标号台账含节点区.json。
- 介质路径 /Volumes/办公/项目/图纸.dwg。
"""

CLEAN = """# 能力说明

- 内置解析库 ezdwg 0.12.6（旧版 0.11.0）、ezdxf 1.4.4。
- 全套 8 张 94MB → 11.8s / 峰值 98MB，单张 0.2–1.5 秒。
- 构件计数 42 块，容差 5 mm 以内算对齐。
- 统一报告 `cad-quantity-report/v0.21` 增 7 键、1 门槛，接口版本 v0.20 -> v0.21。
- 置信度 ≥ 0.90，推断项 0.50–0.89；示例参数 --thickness-m 0.10。
- 规则权重：direct_label 0.92、pattern_match 0.78；高强螺栓 10.9S / 8.8S。
- 图例规则权重 confidence_base 0.88、0.84、0.86。
"""


class ReleaseScrubTest(unittest.TestCase):
    def _write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_project_results_are_flagged(self):
        with tempfile.TemporaryDirectory() as temp:
            findings = scrub.scan([self._write(Path(temp), "a.md", DIRTY)])
        kinds = {tuple(item[2]) for item in findings}
        self.assertTrue(any("结果数值" in kind for kind in kinds))
        self.assertTrue(any("标高数值" in kind for kind in kinds))
        self.assertTrue(any("文件摘要" in kind for kind in kinds))
        self.assertTrue(any("阶段产物名" in kind for kind in kinds))
        self.assertTrue(any("绝对路径" in kind for kind in kinds))
        self.assertGreaterEqual(len(findings), 5)

    def test_versions_and_benchmarks_are_not_flagged(self):
        with tempfile.TemporaryDirectory() as temp:
            findings = scrub.scan([self._write(Path(temp), "b.md", CLEAN)])
        self.assertEqual(findings, [])

    def test_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self._write(Path(temp), "c.md", DIRTY)
            first = path.read_text(encoding="utf-8")
            for pattern, repl in scrub.REDACTIONS:
                first = pattern.sub(repl, first)
            path.write_text(first, encoding="utf-8")
            second = first
            for pattern, repl in scrub.REDACTIONS:
                second = pattern.sub(repl, second)
            self.assertEqual(first, second)
            self.assertNotIn("274.446", first)
            self.assertIn("〈实测〉", first)
            self.assertIn("<介质路径>", first)


if __name__ == "__main__":
    unittest.main()
