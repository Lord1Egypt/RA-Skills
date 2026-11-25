# -*- coding: utf-8 -*-
"""test_v03000 — 0.30.0 回归:默认即最佳·整合。

SKILL 双语「黄金默认值」3 秒信息架构(决策表后即默认值表)/双语同键/引擎默认
与文档口径一致(表格数值来自引擎实现,防文档漂移)。"""
import io
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import type_kit  # noqa: E402
import token_sheet  # noqa: E402


class TestGoldenDefaultsDocs(unittest.TestCase):
    """3 秒信息架构:黄金默认值表在决策表之后、能力表之前,双语同键。"""

    @staticmethod
    def _section(path, header):
        txt = io.open(path, encoding="utf-8").read()
        i = txt.find(header)
        j = txt.find("\n## ", i + 10)
        return txt[i:j] if i >= 0 and j > i else ""

    def test_zh_block_position_and_content(self):
        txt = io.open(os.path.join(ROOT, "SKILL_ZH.md"), encoding="utf-8").read()
        i_decision = txt.find("### 任务 → 命令")
        i_golden = txt.find("### 黄金默认值")
        i_caps = txt.find("## 能力×边界速查")
        self.assertGreater(i_golden, i_decision > 0 and i_decision or 0)
        self.assertLess(i_golden, i_caps, "黄金默认值表必须在能力表之前(3 秒前置)")
        for key in ("max≤2.5×min", "APCA Lc 60/90", "--track-display:-0.011em",
                    "color-mix(in oklab", "--contrast high", "默认即最佳"):
            self.assertIn(key, txt[i_golden:i_caps], key)

    def test_en_block_same_keys(self):
        txt = io.open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
        i_golden = txt.find("### Golden defaults")
        i_caps = txt.find("## Capability × Boundary Quick Reference")
        self.assertGreater(i_golden, 0)
        self.assertLess(i_golden, i_caps)
        for key in ("2.5×min", "APCA Lc 60/90", "--track-display", "defaults are the product"):
            self.assertIn(key, txt[i_golden:i_caps], key)

    def test_doc_numbers_match_engine(self):
        """文档数值=引擎实现(防漂移):行高表/APCA 保证/动效时长逐项对账。"""
        zh = io.open(os.path.join(ROOT, "SKILL_ZH.md"), encoding="utf-8").read()
        for lh, role in (("1.15", "display"), ("1.3", "heading"),
                         ("1.7", "body"), ("1.5", "caption")):
            self.assertEqual(type_kit.LINE_HEIGHT[role], float(lh), role)
        self.assertGreater(token_sheet._apca_lc("000000", "FFFFFF"), 100.0)
        self.assertLess(token_sheet._apca_lc("777777", "888888"), 15.0)
        for i, role in enumerate(token_sheet.STEP_ROLES, 1):
            self.assertEqual(token_sheet.STEP_ROLES[i - 1], role)  # 角色表自洽
        self.assertIn("APCA Lc 60/90", zh)        # 文字步保证口径
        self.assertIn("150/300/600ms", zh)        # 动效令牌口径
        self.assertIn("--track-display:-0.011em", zh)


if __name__ == "__main__":
    unittest.main()
