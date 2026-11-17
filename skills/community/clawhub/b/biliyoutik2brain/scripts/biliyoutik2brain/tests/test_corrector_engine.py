"""
BiliYouTik2Brain — Corrector Engine L1~L5 + Exit 测试
"""

import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.corrector_engine import correct_transcription
from core.corrector_engine.exit import (
    regression_check, check_exit, filter_by_confidence,
    handle_gotchas, needs_regression_check, get_remaining_words,
)


class TestExitCriteria:
    """退出条件 + 置信度过滤 + 回归检查"""

    def test_filter_no_low_confidence(self):
        """无低置信度 → 全部保留"""
        unfiltered = [
            {"original": "拼罢", "corrected": "Pinbar", "confidence": 0.9},
            {"original": "运线", "corrected": "孕线", "confidence": 0.95},
        ]
        filtered = filter_by_confidence(unfiltered)
        assert len(filtered) == 2

    def test_filter_low_confidence(self):
        """低置信度 → 过滤"""
        unfiltered = [
            {"original": "拼罢", "corrected": "Pinbar", "confidence": 0.3},
            {"original": "运线", "corrected": "孕线", "confidence": 0.9},
        ]
        filtered = filter_by_confidence(unfiltered)
        assert len(filtered) == 1
        assert filtered[0]["original"] == "运线"

    def test_filter_empty(self):
        assert filter_by_confidence([]) == []

    def test_regression_same_text(self):
        """回归检查：修正前后相同 → 通过"""
        ok, issues = regression_check("测试文本", "测试文本")
        assert ok is True
        assert len(issues) == 0

    def test_regression_empty_corrected(self):
        """回归检查：修正后为空 → 不通过"""
        ok, issues = regression_check("测试文本", "")
        assert ok is False
        assert len(issues) > 0

    def test_regression_too_short(self):
        """回归检查：修正后长度<原文本10% → 不通过"""
        ok, issues = regression_check("这是一段较长的测试文本", "短")
        assert ok is False
        assert len(issues) > 0

    def test_regression_good(self):
        """合理的修正（中译英，长度变化大但合理）→ 通过"""
        ok, issues = regression_check("[拼罢]", "Pinbar")
        assert ok is True

    def test_gotchas_low_confidence(self):
        """Gotchas：低置信度也会返回，但标记含evidence"""
        result = handle_gotchas("原始文本", "修正文本", 0.3)
        assert "corrected" in result
        assert result["confidence"] == 0.3

    def test_gotchas_high_confidence(self):
        """高置信度 → 正常"""
        result = handle_gotchas("原始文本", "修正文本", 0.95)
        assert result["confidence"] == 0.95

    def test_needs_regression_few(self):
        """少量修正→不需要回归检查"""
        assert needs_regression_check(1, 100) is False

    def test_needs_regression_many(self):
        """大量修正→需要回归检查"""
        assert needs_regression_check(20, 50) is True

    def test_check_exit_no_low_conf(self):
        """无低置信度词+无已应用修正 → 应退出（返回True）"""
        should_exit = check_exit([], {})
        assert should_exit is True

    def test_check_exit_has_low_conf(self):
        """有未修正的低置信度词 → 不应退出（返回False）"""
        should_exit = check_exit([("测试", 0.3)], {})
        assert should_exit is False

    def test_get_remaining_words_with_corrections(self):
        """获取仍未解决的低置信度词"""
        words = get_remaining_words([("a", 0.3), ("b", 0.8)], {"a": {"confidence": 0.9}})
        assert len(words) > 0
        # 'a' 被修正，'b' 仍然需要处理
        assert "a" not in words


class TestCorrectTranscriptionIntegration:
    """correct_transcription 集成测试"""

    def test_empty_text(self):
        """空文本 → 直接返回"""
        result = correct_transcription("")
        assert isinstance(result, dict)
        assert "corrected_text" in result

    def test_deterministic_no_low_conf(self):
        """无低置信词时保持原文（fast_domain_correct 在管线外）"""
        result = correct_transcription("标记一个拼罢")
        # corrector_engine 只修改低置信度词，没有低置信词时不修改
        assert result.get("corrected_text") == "标记一个拼罢"
        assert result.get("final_confidence", 0) >= 0.9
