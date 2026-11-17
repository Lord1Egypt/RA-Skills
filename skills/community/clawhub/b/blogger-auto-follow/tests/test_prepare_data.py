# -*- coding: utf-8 -*-
"""
单元测试: 数据准备与文本解析转换工具 (prepare_data.py)
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.prepare_data import parse_raw_text, validate_json_file


class TestPrepareData(unittest.TestCase):
    def test_parse_numbered_list(self):
        """测试带序号与括号/连字符的多行文本解析"""
        raw_text = """
        1. 极客湾Geekerwan - 数码评测 (350万粉)
        2、 影视飓风 -- 影视视效 (500w)
        3. 差评君 ｜ 科技资讯
        4 - 半佛仙人 (商业认知)
        """
        results = parse_raw_text(raw_text)
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "极客湾Geekerwan")
        self.assertEqual(results[0]["fans"], "350万粉")
        self.assertEqual(results[0]["category"], "数码评测")

        self.assertEqual(results[1]["name"], "影视飓风")
        self.assertEqual(results[1]["fans"], "500w")

        self.assertEqual(results[2]["name"], "差评君")
        self.assertEqual(results[2]["category"], "科技资讯")

        self.assertEqual(results[3]["name"], "半佛仙人")
        self.assertEqual(results[3]["category"], "商业认知")

    def test_parse_comma_separated_text(self):
        """测试逗号和顿号分隔的单行博主名"""
        raw_text = "李开复, 罗永浩、 稚晖君, 何同学"
        results = parse_raw_text(raw_text)
        self.assertEqual(len(results), 4)
        names = [r["name"] for r in results]
        self.assertIn("李开复", names)
        self.assertIn("罗永浩", names)
        self.assertIn("稚晖君", names)
        self.assertIn("何同学", names)

    def test_validate_json_file(self):
        """测试 JSON 格式校验函数"""
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tf:
            tf.write('[{"id": 1, "name": "测试博主", "industry": "科技 · 数码 · 编程"}]')
            tf_path = tf.name

        try:
            self.assertTrue(validate_json_file(tf_path))
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)


if __name__ == "__main__":
    unittest.main()
