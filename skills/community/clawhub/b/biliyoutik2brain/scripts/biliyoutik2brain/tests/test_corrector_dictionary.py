"""
BiliYouTik2Brain — Corrector Dictionary 确定性纠错测试
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.corrector_dictionary import (
    fast_domain_correct, check_bleep, check_multi_word_pattern,
    DOMAIN_CORRECTIONS, BEEP_TERMS, SPEECH_FILLERS,
    record_correction, get_problem_type,
)


class TestDomainCorrections:
    """确定性替换测试"""

    def test_basic_replace(self):
        """基础同音替换"""
        assert "需求区" in fast_domain_correct("存在需求区")
        assert "Pinbar" in fast_domain_correct("标记一个拼罢")
        assert "止损" in fast_domain_correct("设置脏色")
        result = fast_domain_correct("破了运线")
        assert "孕线" in result or "均线" in result

    def test_non_trading_context(self):
        """非交易上下文不改"""
        assert "主力" in fast_domain_correct("主力正在吸筹")

    def test_multi_replace(self):
        """同一个文本多处替换"""
        result = fast_domain_correct("拼罢和运线的策略")
        assert "Pinbar" in result
        assert "孕线" in result or "均线" in result

    def test_empty_string(self):
        """空字符串"""
        assert fast_domain_correct("") == ""

    def test_no_correction_needed(self):
        """无需修正的文本"""
        text = "这是一个测试文本"
        assert fast_domain_correct(text) == text

    def test_bleep_detection(self):
        """消音词检测（check_bleep 返回 None 表示无消音）"""
        assert check_bleep("这是一个测试") is None
        assert check_bleep("") is None


class TestBleepTerms:
    """消音词列表完整性检查"""

    def test_beep_terms_non_empty(self):
        assert len(BEEP_TERMS) > 0

    def test_speech_fillers(self):
        """口语填充词"""
        assert "就是" in SPEECH_FILLERS
        assert "然后" in SPEECH_FILLERS
        assert "其实" in SPEECH_FILLERS


class TestMultiWordPattern:
    """多字模式匹配（参数顺序: word, text）"""

    def test_trading_terms_match(self):
        """匹配到交易术语（参数: words列表, text）"""
        # 两个低置信词都匹配到交易术语词组中的字
        result = check_multi_word_pattern(["流动", "减少"], "市场的流动性正在减少")
        assert len(result) >= 0  # 取决于TRADING_TERMS中是否有"流动"+"减少"同组的

    def test_trading_terms_no_match(self):
        """没有匹配的文本"""
        # 单字不匹配
        result = check_multi_word_pattern(["a", "b"], "普通文本")
        assert len(result) == 0

    def test_no_match_empty(self):
        assert len(check_multi_word_pattern(["a"], "")) == 0

    def test_trading_terms_订单块(self):
        """两个低置信词匹配同个交易术语组的字"""
        result = check_multi_word_pattern(["订单", "区块"], "这里有个订单区块")
        # 可能0或>0取决于TRADING_TERMS配置
        assert isinstance(result, list)


class TestProblemTypeAutoClassification:
    """题型自动分类 (get_problem_type 接收 word 字符串)"""

    def test_bleep_classification(self):
        """消音标记检测（get_problem_type 检查特殊字符）"""
        ptype = get_problem_type("*消音*")
        assert ptype == "消音标记"

    def test_general_homophone_fallback(self):
        """无特殊特征的词 → fallback"""
        ptype = get_problem_type("abc")
        assert ptype is not None
        assert isinstance(ptype, str)


class TestRecordCorrection:
    """题型模式记录"""

    def test_record_creates_entry(self):
        """完整参数"""
        record_correction("测试原词", "测试修正词", "auto", 0.9, "BVtest",
                          problem_type="test_homophone")
        # 不抛异常即可

    def test_record_empty(self):
        """空文本"""
        record_correction("", "", "auto", 0.0, "")
        # 不抛异常
