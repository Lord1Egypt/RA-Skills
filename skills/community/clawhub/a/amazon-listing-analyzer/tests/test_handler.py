#!/usr/bin/env python3
"""
Amazon Listing Analyzer - test_handler.py
至少3个测试用例，验证核心功能正确性。
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handler import (
    analyze,
    score_title,
    score_bullets,
    score_description,
    score_keywords,
    score_compliance,
    health_score,
    keyword_analysis,
    competitor_benchmark,
    full_optimization,
)


class TestAmazonListingAnalyzer(unittest.TestCase):

    def test_health_score_valid_input(self):
        """测试用例1：健康度评分 - 有效输入"""
        data = {
            "intent": "health_score",
            "product_title": "Premium Wireless Bluetooth Headphones with Noise Cancellation",
            "bullet_points": [
                "High quality sound",
                "30-hour battery life",
                "Comfortable fit",
                "Fast charging",
                "Foldable design",
            ],
            "product_description": "Experience music like never before with our premium headphones.",
            "search_terms": "wireless headphones bluetooth noise cancellation",
        }
        result = analyze(data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["module"], "health_score")
        self.assertIn("health_score", result["result"])
        hs = result["result"]["health_score"]
        self.assertIn("total", hs)
        self.assertIn("dimensions", hs)
        self.assertIn("summary", hs)
        self.assertIsInstance(hs["total"], int)
        self.assertGreaterEqual(hs["total"], 0)
        self.assertLessEqual(hs["total"], 100)

    def test_keyword_analysis(self):
        """测试用例2：关键词分析"""
        data = {
            "intent": "keyword_analysis",
            "product_category": "Electronics > Headphones",
            "product_features": ["wireless", "noise cancellation", "bluetooth", "long battery life"],
        }
        result = analyze(data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["module"], "keyword_analysis")
        self.assertIn("keyword_analysis", result["result"])
        ka = result["result"]["keyword_analysis"]
        self.assertIn("matrix", ka)
        self.assertIn("priority_keywords", ka)
        self.assertIn("long_tail_keywords", ka)
        self.assertIsInstance(ka["matrix"], list)
        self.assertIsInstance(ka["priority_keywords"], list)
        self.assertIsInstance(ka["long_tail_keywords"], list)

    def test_competitor_benchmark(self):
        """测试用例3：竞品对标分析"""
        data = {
            "intent": "competitor_benchmark",
            "competitor_asin": "B00XXXXXXXX",
            "product_title": "Generic Brand Wireless Headphones",
            "bullet_points": ["Good sound", "10hr battery", "Lightweight", "Sweat resistant", "Foldable"],
        }
        result = analyze(data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["module"], "competitor_benchmark")
        self.assertIn("competitor_benchmark", result["result"])
        cb = result["result"]["competitor_benchmark"]
        self.assertIn("comparisons", cb)
        self.assertIn("gaps", cb)
        self.assertIsInstance(cb["comparisons"], list)
        self.assertGreater(len(cb["comparisons"]), 0)

    def test_full_optimization(self):
        """测试用例4：完整优化建议包"""
        data = {
            "intent": "full_optimization",
            "product_title": "Wireless Headphones",
            "bullet_points": ["Good sound", "10hr battery"],
            "product_description": "Great headphones for daily use.",
            "search_terms": "headphones",
            "product_features": ["wireless", "bluetooth"],
        }
        result = analyze(data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["module"], "full_optimization")
        self.assertIn("optimization_package", result["result"])
        op = result["result"]["optimization_package"]
        self.assertIn("title", op)
        self.assertIn("bullets", op)
        self.assertIn("description", op)
        self.assertIn("keywords", op)

    def test_input_too_long(self):
        """测试用例5：输入超长校验"""
        data = {
            "intent": "health_score",
            "product_title": "x" * 15000,
        }
        result = analyze(data)
        self.assertEqual(result["status"], "error")
        self.assertIn("errors", result)
        self.assertTrue(any("超过10000字符" in e for e in result["errors"]))

    def test_score_title_edge_cases(self):
        """测试用例6：标题评分边界情况"""
        # 空标题
        r = score_title("")
        self.assertEqual(r["score"], 0)
        self.assertIn("标题为空", r["issues"])
        # 正常标题
        r = score_title("Sony WH-1000XM5 Wireless Noise Cancelling Headphones")
        self.assertGreater(r["score"], 0)
        # 标题缺少核心词
        r = score_title("Best Product Ever")
        self.assertIn("headphone", r["issues"][-1].lower() if r["issues"] else "")

    def test_score_bullets_edge_cases(self):
        """测试用例7：五点描述评分边界"""
        # 空
        r = score_bullets([])
        self.assertEqual(r["score"], 0)
        # 少于5条
        r = score_bullets(["Only one bullet point here"])
        self.assertLess(r["score"], 80)

    def test_score_compliance_forbidden_words(self):
        """测试用例8：合规检查禁止词"""
        r = score_compliance(
            "Fake Replica Headphones",
            ["Best product ever", "Miracle cure for headaches"],
            "This product is number 1 top rated",
        )
        self.assertLess(r["score"], 100)
        self.assertTrue(any("fake" in issue.lower() for issue in r["issues"]))

    def test_unknown_intent_defaults_to_health_score(self):
        """测试用例9：未知intent默认走健康度评分"""
        data = {"intent": "unknown_intent"}
        result = analyze(data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["module"], "health_score")


if __name__ == "__main__":
    unittest.main(verbosity=2)
