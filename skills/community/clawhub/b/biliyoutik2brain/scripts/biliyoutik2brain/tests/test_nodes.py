"""
BiliYouTik2Brain — 节点函数测试
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.node_transcribe import _smart_correct, _mark_low_confidence, _format_confidence_notes


class TestSmartCorrect:
    """确定性纠错测试"""

    def test_direct_replacement(self):
        assert _smart_correct("一贴") == "一单"

    def test_no_change(self):
        """无需修正的文本"""
        text = "价格突破阻力区"
        assert _smart_correct(text) == text

    def test_empty_text(self):
        assert _smart_correct("") == ""

    def test_multi_replacement(self):
        """多次替换"""
        text = "一贴一贴一贴"
        assert _smart_correct(text) == "一单一单一单"


class TestMarkLowConfidence:
    """低置信度词标记"""

    def test_single_word(self):
        text = "测试文本"
        low_words = [("测试", 0.3)]
        result = _mark_low_confidence(text, low_words)
        assert "【？测试】" in result

    def test_multi_word(self):
        text = "这是测试文本"
        low_words = [("这是", 0.2), ("测试", 0.4)]
        result = _mark_low_confidence(text, low_words)
        assert "【？这是】" in result
        assert "【？测试】" in result

    def test_empty_list(self):
        text = "测试文本"
        result = _mark_low_confidence(text, [])
        assert result == text

    def test_empty_text(self):
        assert _mark_low_confidence("", [("a", 0.5)]) == ""

    def test_short_word_skip(self):
        """单字不标记"""
        text = "我你他"
        low_words = [("我", 0.3), ("你", 0.2)]
        result = _mark_low_confidence(text, low_words)
        assert "【？我】" not in result


class TestFormatConfidenceNotes:
    """置信度说明格式化"""

    def test_format_notes(self):
        notes = _format_confidence_notes([("测试", 0.3), ("文本", 0.4)])
        assert "测试" in notes
        assert "0.3" in notes
        assert "文本" in notes

    def test_empty_notes(self):
        notes = _format_confidence_notes([])
        assert "置信度正常" in notes

    def test_max_15_items(self):
        words = [(f"word{i}", 0.3) for i in range(30)]
        notes = _format_confidence_notes(words)
        # 只显示前15个
        assert "word14" in notes
        assert "word15" not in notes  # 16个从0开始
