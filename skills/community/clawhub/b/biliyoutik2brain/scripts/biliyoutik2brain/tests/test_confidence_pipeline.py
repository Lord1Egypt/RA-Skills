"""
BiliYouTik2Brain — 置信度驱动管线测试
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.asr import ASRResult
from core.confidence_pipeline import process, scan_low_confidence_regions


class TestConfidencePipeline:
    """置信度驱动管线 — 核心流程测试"""

    def test_empty_text_returns(self):
        """空文本应直接返回"""
        r = ASRResult(full_text="")
        result = process(r)
        assert result.full_text == ""
        assert result.original_text == ""

    def test_basic_flow(self):
        """基本流程：有文本无线索时走分类+分析"""
        r = ASRResult(
            full_text="支撑位和阻力位是交易中的重要概念",
            engine="faster_whisper",
            has_token_confidence=True,
        )
        result = process(r)
        # 即使没有 LLM（离线），也应返回有文本的结果
        assert result.full_text or result.original_text
        # 至少应产出 chunk 或 full_text
        assert result.full_text or result.chunks

    def test_no_token_confidence(self):
        """无 token 置信度时也应正常返回"""
        r = ASRResult(
            full_text="测试文本",
            engine="bailian",
            has_token_confidence=False,
        )
        result = process(r)
        assert result.full_text or result.original_text


class TestLowConfidenceScan:
    """低置信区域扫描测试"""

    def test_empty_regions(self):
        r = ASRResult(full_text="test")
        regions = scan_low_confidence_regions(r)
        assert isinstance(regions, list)

    def test_high_confidence_no_regions(self):
        r = ASRResult(
            full_text="test",
            has_token_confidence=True,
            low_confidence_regions=[],
        )
        regions = scan_low_confidence_regions(r, threshold=0.6)
        assert isinstance(regions, list)
