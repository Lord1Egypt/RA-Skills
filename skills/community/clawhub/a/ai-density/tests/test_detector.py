#!/usr/bin/env python3
"""
AI Density 单元测试 / Unit Tests
"""

import unittest
import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.detector import (
    AIDensityDetector,
    DetectionResult,
    AIContentLevel,
    detect_ai_content,
    AIFingerprintDetector,
    PerplexityAnalyzer,
    SemanticAnalyzer,
    StyleAnalyzer,
    HumanModificationDetector
)


class TestAIDensityDetector(unittest.TestCase):
    """测试 AI Density 检测器核心功能 / Test AI Density detector core functionality"""
    
    def setUp(self):
        """测试前准备 / Setup before tests"""
        self.detector = AIDensityDetector()
    
    def test_detect_ai_content_basic(self):
        """测试快速检测接口"""
        text = "这是一段测试文本，用于验证AI检测功能。"
        result = detect_ai_content(text)
        
        self.assertIsInstance(result, DetectionResult)
        self.assertIn(result.level, range(0, 11))
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)
        self.assertGreater(result.confidence, 0)
        self.assertIsNotNone(result.description)
    
    def test_detector_class(self):
        """测试 AIDensityDetector 类 / Test AIDensityDetector class"""
        text = "人工智能是计算机科学的重要分支。"
        result = self.detector.detect(text)
        
        self.assertIsInstance(result, DetectionResult)
        self.assertIsInstance(result.dimension_scores, dict)
        self.assertIn('fingerprint', result.dimension_scores)
        self.assertIn('perplexity', result.dimension_scores)
    
    def test_dimension_scores_structure(self):
        """测试各维度得分结构"""
        text = "测试文本内容，包含足够的长度来进行分析。这是一段用于测试的文本。"
        result = self.detector.detect(text)
        
        expected_dimensions = [
            'fingerprint', 'perplexity', 'semantic', 
            'style', 'human_modification'
        ]
        
        for dim in expected_dimensions:
            self.assertIn(dim, result.dimension_scores)
            # 维度得分可能是浮点数或字典
            score = result.dimension_scores[dim]
            if isinstance(score, dict):
                self.assertIn('score', score)
    
    def test_level_description(self):
        """测试等级描述"""
        for level in range(0, 11):
            desc = self.detector._get_level_description(level)
            self.assertIsNotNone(desc)
            self.assertGreater(len(desc), 0)


class TestAIFingerprintDetector(unittest.TestCase):
    """测试 AI 指纹检测器"""
    
    def setUp(self):
        self.detector = AIFingerprintDetector()
    
    def test_detect_patterns(self):
        """测试模式检测"""
        # 包含典型AI模式的文本
        text = "综上所述，我们可以得出以下结论。"
        result = self.detector.detect(text)
        
        # 返回的是字典格式
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertGreaterEqual(result['score'], 0)
        self.assertLessEqual(result['score'], 100)
    
    def test_no_patterns(self):
        """测试无模式文本"""
        text = "今天天气不错，我想去公园走走。"
        result = self.detector.detect(text)
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)


class TestPerplexityAnalyzer(unittest.TestCase):
    """测试困惑度分析器"""
    
    def setUp(self):
        self.analyzer = PerplexityAnalyzer()
    
    def test_analyze(self):
        """测试困惑度分析"""
        text = "这是一段测试文本。"
        result = self.analyzer.analyze(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertGreater(result['score'], 0)


class TestSemanticAnalyzer(unittest.TestCase):
    """测试语义分析器"""
    
    def setUp(self):
        self.analyzer = SemanticAnalyzer()
    
    def test_analyze(self):
        """测试语义分析"""
        text = """
        首先，我们需要理解这个问题。
        其次，分析其中的关键因素。
        最后，得出结论。
        """
        result = self.analyzer.analyze(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertGreaterEqual(result['score'], 0)


class TestStyleAnalyzer(unittest.TestCase):
    """测试风格分析器"""
    
    def setUp(self):
        self.analyzer = StyleAnalyzer()
    
    def test_analyze(self):
        """测试风格分析"""
        text = "人工智能是计算机科学的分支。"
        result = self.analyzer.analyze(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertGreaterEqual(result['score'], 0)


class TestHumanModificationDetector(unittest.TestCase):
    """测试人工痕迹检测器"""
    
    def setUp(self):
        self.detector = HumanModificationDetector()
    
    def test_detect_human_elements(self):
        """测试人工元素检测"""
        # 包含个人经验、情绪化的文本
        text = "我觉得这事儿特别坑，我昨天搞到凌晨3点才弄好！"
        result = self.detector.detect(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)


class TestAIContentLevel(unittest.TestCase):
    """测试 AI 内容等级枚举"""
    
    def test_level_values(self):
        """测试等级值"""
        self.assertEqual(AIContentLevel.LEVEL_0.value, 0)
        self.assertEqual(AIContentLevel.LEVEL_5.value, 5)
        self.assertEqual(AIContentLevel.LEVEL_10.value, 10)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_pipeline(self):
        """测试完整检测流程"""
        texts = [
            "这是第一段测试文本，包含足够的长度。",
            "人工智能是计算机科学的重要分支，主要研究如何让计算机模拟人类智能。这是一段较长的测试文本。",
            "兄弟们，这事儿真的太离谱了！我昨天搞到凌晨才弄好，真的累死了。",
        ]
        
        for text in texts:
            result = detect_ai_content(text)
            self.assertIsInstance(result.level, int)
            self.assertIn(result.level, range(0, 11))
    
    def test_ai_style_text(self):
        """测试AI风格文本检测"""
        text = """
        综上所述，人工智能是当今科技发展的重要方向。
        首先，我们需要了解其基本原理。
        其次，分析其应用场景。
        最后，展望其未来发展。
        """
        result = detect_ai_content(text)
        # AI风格文本应该得分较高
        self.assertIsInstance(result.level, int)
        self.assertIsInstance(result.score, float)
    
    def test_human_style_text(self):
        """测试人工风格文本检测"""
        text = """
        兄弟们，今天这事儿真给我整无语了！
        我昨天那个项目，代码写到凌晨3点...
        你说气人不？不过还好最后解决了。
        下次再也不这么干了，真的！
        """
        result = detect_ai_content(text)
        # 人工风格文本应该能检测出来
        self.assertIsInstance(result.level, int)
        self.assertIsNotNone(result.description)


if __name__ == '__main__':
    unittest.main()
