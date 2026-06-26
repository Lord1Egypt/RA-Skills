#!/usr/bin/env python3
"""
Tests for AI Annotator Module
测试 AI 标注器功能
"""

import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from annotator import AIAnnotator, FeatureExtractor


def test_feature_extractor_basic():
    """测试特征提取器基本功能"""
    extractor = FeatureExtractor()
    text = "这是一个测试文本。他说道：\"你好吗？\"她微笑着回答。"

    features = extractor.extract_features(text)

    assert "char_count" in features
    assert "sentence_count" in features
    assert "dialogue_ratio" in features
    assert "emotion_scores" in features
    assert "scene_scores" in features
    assert features["char_count"] > 0
    print("✅ test_feature_extractor_basic passed")


def test_feature_extractor_emotion():
    """测试情绪特征提取"""
    extractor = FeatureExtractor()
    text = "他感到非常紧张，周围充满了危险的气息。"

    features = extractor.extract_features(text)

    assert "紧张" in features["emotion_scores"]
    assert features["emotion_scores"]["紧张"] > 0
    print("✅ test_feature_extractor_emotion passed")


def test_feature_extractor_scene():
    """测试场景特征提取"""
    extractor = FeatureExtractor()
    text = "他拔出剑，发动了攻击，灵力在经脉中运转。"

    features = extractor.extract_features(text)

    assert "打斗" in features["scene_scores"]
    assert "修炼" in features["scene_scores"]
    print("✅ test_feature_extractor_scene passed")


def test_predict_preliminary_tags():
    """测试初步标签预测"""
    extractor = FeatureExtractor()
    text = "这是一段很长的测试文本。" * 100

    features = extractor.extract_features(text)
    tags = extractor.predict_preliminary_tags(features)

    assert "字数区间" in tags
    assert "节奏" in tags
    assert "主情绪" in tags
    assert "主场景" in tags
    assert "对话比例" in tags
    print("✅ test_predict_preliminary_tags passed")


def test_ai_annotator_init():
    """测试 AI 标注器初始化"""
    annotator = AIAnnotator(model="dashscope-coding/qwen3.5-plus")

    assert annotator.model == "dashscope-coding/qwen3.5-plus"
    print("✅ test_ai_annotator_init passed")


def test_fallback_annotation():
    """测试降级标注"""
    annotator = AIAnnotator()
    text = "这是一个测试文本片段。"

    # 测试降级标注（不调用 LLM）
    annotation = annotator._fallback_annotation(text)

    assert "scene_type" in annotation
    assert "emotion" in annotation
    assert "pace" in annotation
    assert annotation["fallback"] is True
    print("✅ test_fallback_annotation passed")


def test_annotation_structure():
    """测试标注数据结构"""
    extractor = FeatureExtractor()
    text = "他怒吼着冲了上去，剑光闪烁。"

    features = extractor.extract_features(text)
    tags = extractor.predict_preliminary_tags(features)

    assert "主场景" in tags
    assert "主情绪" in tags
    print("✅ test_annotation_structure passed")


if __name__ == "__main__":
    print("Running AI Annotator Tests...\n")

    test_feature_extractor_basic()
    test_feature_extractor_emotion()
    test_feature_extractor_scene()
    test_predict_preliminary_tags()
    test_ai_annotator_init()
    test_fallback_annotation()
    test_annotation_structure()

    print("\n✅ All AI Annotator tests passed!")
