"""
BiliYouTik2Brain — ASR 抽象层测试
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.asr import ASRResult, TokenInfo, ConfidenceRegion, estimate_confidence


class TestASRResult:
    """ASR 结果数据结构测试"""

    def test_empty_result(self):
        r = ASRResult(full_text="")
        assert r.full_text == ""
        assert r.has_token_confidence is False
        assert r.engine == "unknown"

    def test_with_text(self):
        r = ASRResult(full_text="测试文本", engine="faster_whisper")
        assert r.full_text == "测试文本"
        assert r.engine == "faster_whisper"

    def test_with_token_confidence(self):
        r = ASRResult(
            full_text="MACD金叉",
            engine="faster_whisper",
            has_token_confidence=True,
        )
        assert r.has_token_confidence is True

    def test_low_confidence_regions_default(self):
        r = ASRResult(full_text="test")
        assert r.low_confidence_regions == []


class TestTokenInfo:
    """Token 信息数据结构测试"""

    def test_token_info_creation(self):
        t = TokenInfo(word="MACD", confidence=0.95, start=1.0, end=1.5)
        assert t.word == "MACD"
        assert t.confidence == 0.95
        assert t.start == 1.0

    def test_low_confidence_token(self):
        t = TokenInfo(word="模糊", confidence=0.3, start=2.0, end=2.5)
        assert t.confidence < 0.6  # 低置信阈值


class TestConfidenceRegion:
    """置信区域数据结构测试"""

    def test_region_creation(self):
        r = ConfidenceRegion(
            char_start=0, char_end=10,
            text="测试低置信文本",
            avg_confidence=0.4,
            token_indices=[0, 1, 2],
        )
        assert r.avg_confidence < 0.6
        assert r.char_start == 0
        assert len(r.token_indices) == 3


class TestEstimateConfidence:
    """B方案置信度估算测试"""

    def test_estimate_on_empty(self):
        r = ASRResult(full_text="")
        result = estimate_confidence(r)
        assert isinstance(result, ASRResult)
        assert result.overall_confidence >= 0.0

    def test_estimate_on_normal_text(self):
        r = ASRResult(
            full_text="这是正常文本",
            segments=[],
        )
        result = estimate_confidence(r)
        assert 0.0 <= result.overall_confidence <= 1.0
