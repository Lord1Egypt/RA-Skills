"""
test_pipeline.py - 教学流水线单元测试（7 项）

覆盖：
  17. select_knowledge.extract_keywords 关键词提取
  18. select_knowledge.score_segment 片段打分
  19. select_knowledge.select_candidates 候选选择
  20. compose_lesson.render_markdown Markdown 课件渲染
  21. compose_lesson.render_assessment 评估题渲染
  22. analyze_courseware.mock_analyze_segment mock 推理
  23. skill_runtime.python_version_supported Python 版本检测
"""
import sys
import os
import unittest

_scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, _scripts_dir)

from select_knowledge import extract_keywords, score_segment, select_candidates
from compose_lesson import render_markdown, render_assessment
from analyze_courseware import mock_analyze_segment
from skill_runtime import python_version_supported, min_python_display


class TestExtractKeywords(unittest.TestCase):
    """测试关键词提取。"""

    def test_chinese_bigram(self):
        """中文主题应提取 bigram 关键词。"""
        kws = extract_keywords("机器学习入门")
        self.assertIn("机器", kws)
        self.assertIn("器学", kws)
        self.assertIn("学习", kws)

    def test_english_keyword(self):
        """英文 token 应整体作为关键词。"""
        kws = extract_keywords("AI 基础")
        self.assertIn("ai", kws)


class TestScoreSegment(unittest.TestCase):
    """测试片段打分。"""

    def test_keyword_match_positive_score(self):
        """关键词命中应得正分。"""
        seg = {"seg_text": "机器学习是AI的核心", "knowledge_tags": ["机器学习"], "difficulty": 2}
        kws = extract_keywords("机器学习")
        score = score_segment(seg, kws)
        self.assertGreater(score, 0)

    def test_negative_word_penalty(self):
        """负面词应扣分。"""
        seg = {"seg_text": "这段内容已废弃不相关", "knowledge_tags": [], "difficulty": 2}
        kws = extract_keywords("机器学习")
        score = score_segment(seg, kws)
        self.assertLess(score, 0)


class TestSelectCandidates(unittest.TestCase):
    """测试候选知识点选择。"""

    def test_select_returns_candidates(self):
        """应返回指定数量的候选知识点。"""
        segments = [
            {"seg_id": 0, "source_file": "a.md", "source_filename": "a.md",
             "seg_text": "机器学习基础", "knowledge_tags": ["机器学习"], "difficulty": 2,
             "pedagogy_suggestion": "建议讲授式"},
            {"seg_id": 1, "source_file": "b.md", "source_filename": "b.md",
             "seg_text": "深度学习进阶", "knowledge_tags": ["深度学习"], "difficulty": 3,
             "pedagogy_suggestion": "建议PBL"},
        ]
        candidates = select_candidates(segments, "机器学习", min_knowledge=2)
        self.assertEqual(len(candidates), 2)
        self.assertIn("theme_score", candidates[0])


class TestRenderMarkdown(unittest.TestCase):
    """测试 Markdown 课件渲染。"""

    def test_render_contains_title_and_objectives(self):
        """渲染结果应包含标题和教学目标。"""
        plan = {
            "lesson_title": "AI 通识课第一节",
            "pedagogy_method": "讲授式",
            "learning_objectives": ["了解AI基础", "理解机器学习概念"],
            "knowledge_points": ["AI", "机器学习"],
            "clips": [
                {"knowledge_point": "AI", "difficulty": 1, "duration_sec": 120,
                 "voiceover": {"text": "AI是人工智能的简称"}},
            ],
            "assessment": {"questions": [
                {"question": "Q1", "answer": "A1"},
            ]},
        }
        md = render_markdown(plan)
        self.assertIn("# AI 通识课第一节", md)
        self.assertIn("了解AI基础", md)
        self.assertIn("讲授式", md)
        self.assertIn("v8-aipc", md)  # 验证版本号已升级 V8-AIPC


class TestRenderAssessment(unittest.TestCase):
    """测试评估题渲染。"""

    def test_render_assessment_structure(self):
        """评估题应包含标准化结构。"""
        plan = {
            "assessment": {
                "questions": [
                    {"id": "Q1", "type": "choice", "question": "什么是AI？",
                     "options": ["A", "B"], "answer": "A", "difficulty": 1},
                    {"id": "Q2", "type": "short_answer", "question": "解释ML",
                     "answer": "机器学习", "difficulty": 2},
                ],
            },
        }
        result = render_assessment(plan)
        self.assertEqual(result["total_questions"], 2)
        self.assertEqual(result["questions"][0]["id"], "Q1")
        self.assertEqual(result["questions"][1]["answer"], "机器学习")


class TestMockAnalyzeSegment(unittest.TestCase):
    """测试 mock 推理。"""

    def test_mock_analyze_returns_tags(self):
        """mock 推理应返回知识点标签和难度。"""
        result = mock_analyze_segment("机器学习是人工智能的核心技术", "机器学习")
        self.assertIn("knowledge_tags", result)
        self.assertGreater(len(result["knowledge_tags"]), 0)
        self.assertIn("difficulty", result)
        self.assertGreaterEqual(result["difficulty"], 1)
        self.assertLessEqual(result["difficulty"], 5)


class TestPythonVersionSupported(unittest.TestCase):
    """测试 Python 版本检测。"""

    def test_supported_version(self):
        """>= 3.10 应返回 True。"""
        self.assertTrue(python_version_supported((3, 10)))
        self.assertTrue(python_version_supported((3, 12)))

    def test_unsupported_version(self):
        """< 3.10 应返回 False。"""
        self.assertFalse(python_version_supported((3, 9)))
        self.assertFalse(python_version_supported((3, 8)))


if __name__ == "__main__":
    unittest.main()
