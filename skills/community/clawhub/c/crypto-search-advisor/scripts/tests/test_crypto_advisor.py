#!/usr/bin/env python3
"""
crypto_advisor.py 自动化测试

测试覆盖：
- 币种分类（稳定币/Meme/主流/山寨/商品/股票）
- 冲突检测（low/medium/high）
- 截图质量评估
- 数据可信度评分
- 输出格式化
- 成交量方向感知（放量上涨/放量下跌/缩量）
- 时效性判定（真实时间差比对）
- Tokenomics 解析（FDV/MCap/解锁风险）
- 完整分析流程
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_advisor import (
    classify_coin,
    detect_conflict,
    assess_screenshot_quality,
    calculate_input_reliability,
    analyze,
    format_output
)


# ==================== TestClassifyCoin ====================

class TestClassifyCoin:
    """测试币种分类"""

    def test_stablecoin_exact_match(self):
        """精确匹配：稳定币"""
        result = classify_coin("USDT")
        assert result["category"] == "stable"

        result = classify_coin("USDC")
        assert result["category"] == "stable"

        result = classify_coin("DAI")
        assert result["category"] == "stable"

    def test_stablecoin_price_fallback(self):
        """价格回退：价格≈1，判定为稳定币"""
        result = classify_coin("UNKNOWN", price=1.001)
        assert result["category"] == "stable"

        result = classify_coin("UNKNOWN", price=0.98)
        assert result["category"] == "stable"

    def test_meme_exact_match(self):
        """精确匹配：Meme币"""
        result = classify_coin("DOGE")
        assert result["category"] == "meme"

        result = classify_coin("SHIB")
        assert result["category"] == "meme"

        result = classify_coin("PEPE")
        assert result["category"] == "meme"

    def test_meme_price_fallback(self):
        """价格回退：价格<0.01，判定为Meme币"""
        result = classify_coin("UNKNOWN", price=0.0001)
        assert result["category"] == "meme"

    def test_mainstream_default(self):
        """默认分类：主流币"""
        result = classify_coin("BTC")
        assert result["category"] == "mainstream"

        result = classify_coin("ETH")
        assert result["category"] == "mainstream"

        result = classify_coin("RANDOM")
        assert result["category"] == "altcoin"

    def test_chinese_names(self):
        """中文别名支持"""
        result = classify_coin("泰达币")
        assert result["category"] == "stable"

        result = classify_coin("比特币")
        assert result["category"] == "mainstream"

        result = classify_coin("狗狗币")
        assert result["category"] == "meme"


# ==================== TestDetectConflict ====================

class TestDetectConflict:
    """测试冲突检测"""

    def test_low_conflict(self):
        """低冲突：偏差<1%"""
        result = detect_conflict(100, 99, 101)
        assert result["conflict_level"] == "low"

    def test_medium_conflict(self):
        """中冲突：偏差1-3%"""
        result = detect_conflict(100, 97, 98)
        assert result["conflict_level"] == "medium"

    def test_high_conflict(self):
        """高冲突：偏差>3%"""
        result = detect_conflict(100, 90, 92)
        assert result["conflict_level"] == "high"

    def test_edge_case_exact_boundary(self):
        """边界值测试：1%边界"""
        result = detect_conflict(100, 99, 99)
        assert result["conflict_level"] in ["low", "medium"]


# ==================== TestAssessQuality ====================

class TestAssessQuality:
    """测试截图质量评估"""

    def test_quality_a(self):
        """A级质量"""
        result = assess_screenshot_quality(
            clarity="clear",
            confidence="high",
            missing=[]
        )
        assert result["usable_level"] == "A"
        assert result["trade_usable"] is True

    def test_quality_b(self):
        """B级质量"""
        result = assess_screenshot_quality(
            clarity="partial",
            confidence="medium",
            missing=["volume"]
        )
        assert result["usable_level"] == "B"
        assert result["trade_usable"] is True

    def test_quality_c(self):
        """C级质量"""
        result = assess_screenshot_quality(
            clarity="blurry",
            confidence="low",
            missing=["volume", "indicators", "price"]
        )
        assert result["usable_level"] == "C"
        assert result["trade_usable"] is False


# ==================== TestInputReliability ====================

class TestInputReliability:
    """测试数据可信度评分"""

    def test_high_score_no_conflict(self):
        """高评分：无冲突，高质量"""
        conflict = {"conflict_level": "low"}
        quality = {"usable_level": "A", "trade_usable": True}
        search_data = {"min": 100, "max": 101}

        result = calculate_input_reliability(
            category="mainstream",
            conflict=conflict,
            quality=quality,
            search_data=search_data
        )

        assert result["score"] >= 9.0
        assert result["grade"] in ["A", "A+"]

    def test_medium_score_with_conflict(self):
        """中等评分：有冲突"""
        conflict = {"conflict_level": "medium"}
        quality = {"usable_level": "B", "trade_usable": True}
        search_data = {"min": 100, "max": 101}

        result = calculate_input_reliability(
            category="mainstream",
            conflict=conflict,
            quality=quality,
            search_data=search_data
        )

        # 计算逻辑：quality=7.0-1.5=5.5, weighted=5.5*0.25=1.375
        # completeness=10, weighted=2.0
        # feasible=10, weighted=2.5
        # risk=7.0, weighted=1.4
        # freshness=10, weighted=1.0
        # total=8.275 → A
        assert 7.0 <= result["score"] <= 9.0
        assert result["grade"] in ["A", "B+", "B"]

    def test_low_score_high_conflict(self):
        """低评分：高冲突或低质量"""
        conflict = {"conflict_level": "high"}
        quality = {"usable_level": "C", "trade_usable": False}
        search_data = {"min": 100, "max": 101}

        result = calculate_input_reliability(
            category="mainstream",
            conflict=conflict,
            quality=quality,
            search_data=search_data
        )

        # 计算逻辑：quality=4.0-3.0=1.0, weighted=1.0*0.25=0.25
        # completeness=10, weighted=2.0
        # feasible=10, weighted=2.5
        # risk=4.0, weighted=0.8
        # freshness=10, weighted=1.0
        # total=6.55 → B
        assert result["score"] < 8.0
        assert result["grade"] in ["B", "C+", "C"]

    def test_output_has_transparency_fields(self):
        """测试输出包含透明度字段"""
        conflict = {"conflict_level": "low"}
        quality = {"usable_level": "A", "trade_usable": True}
        search_data = {"min": 100, "max": 101}

        result = calculate_input_reliability(
            category="mainstream",
            conflict=conflict,
            quality=quality,
            search_data=search_data
        )

        # 检查透明度字段
        assert "formula" in result
        assert "dimensions" in result
        assert "calculation_trace" in result
        assert "grade_boundaries" in result
        assert "score_sources" in result
        
        # 检查每个维度都有扣分明细
        for dim_name, dim_data in result["dimensions"].items():
            assert "raw_score" in dim_data
            assert "weight" in dim_data
            assert "deductions" in dim_data
            assert "calculation_type" in dim_data
            assert "weighted_contribution" in dim_data
    
    def test_deduction_details_structure(self):
        """测试扣分明细结构"""
        conflict = {"conflict_level": "medium"}
        quality = {"usable_level": "B", "trade_usable": True, "confidence": "medium"}
        search_data = {"min": 100, "max": 101}

        result = calculate_input_reliability(
            category="mainstream",
            conflict=conflict,
            quality=quality,
            search_data=search_data
        )

        # 检查有扣分的维度
        data_cred = result["dimensions"]["data_credibility"]
        assert len(data_cred["deductions"]) > 0
        
        # 检查扣分明细结构
        for deduction in data_cred["deductions"]:
            assert "reason" in deduction
            assert "deducted" in deduction
            assert "from" in deduction
            assert isinstance(deduction["deducted"], (int, float))
            assert deduction["deducted"] > 0


# ==================== TestFormatOutput ====================

class TestFormatOutput:
    """测试输出格式化"""

    def test_output_has_required_fields(self):
        """输出包含必需字段"""
        base_data = {
            "symbol": "BTC",
            "screenshot_price": "$78000",
            "search_price_range": "$78000-78500"
        }
        reliability_score = {
            "score": 9.0,
            "grade": "A+",
            "dimensions": {}
        }

        result = format_output(
            category="mainstream",
            base_data=base_data,
            reliability_score=reliability_score
        )

        # 必需字段检查
        assert "symbol" in result
        assert "category" in result
        assert "input_reliability" in result
        assert "disclaimer" in result

    def test_mainstream_mode_output(self):
        """主流币模式输出"""
        base_data = {"symbol": "BTC"}
        reliability_score = {"score": 9.0, "grade": "A+", "dimensions": {}}

        result = format_output(
            category="mainstream",
            base_data=base_data,
            reliability_score=reliability_score
        )

        assert result["category"] == "mainstream"

    def test_stablecoin_mode_output(self):
        """稳定币模式输出"""
        base_data = {"symbol": "USDT"}
        reliability_score = {"score": 10.0, "grade": "A+", "dimensions": {}}

        result = format_output(
            category="stable",
            base_data=base_data,
            reliability_score=reliability_score
        )

        assert result["category"] == "stable"

    def test_meme_mode_output(self):
        """Meme币模式输出"""
        base_data = {"symbol": "DOGE"}
        reliability_score = {"score": 8.0, "grade": "A", "dimensions": {}}

        result = format_output(
            category="meme",
            base_data=base_data,
            reliability_score=reliability_score
        )

        assert result["category"] == "meme"


# ==================== TestIntegration ====================

class TestIntegration:
    """集成测试：完整分析流程"""

    def test_full_analysis_mainstream(self, sample_screenshot_data, sample_search_data):
        """主流币完整流程"""
        result = analyze(
            symbol="BTC",
            screenshot_data=sample_screenshot_data,
            search_data=sample_search_data
        )

        assert result["symbol"] == "BTC"
        assert result["category"] == "mainstream"
        assert "input_reliability" in result
        assert "observation_plan" in result

    def test_full_analysis_stablecoin(self):
        """稳定币完整流程"""
        screenshot_data = {"price": 1.001, "clarity": "clear", "confidence": "high"}
        search_data = {"min": 1.00, "max": 1.002}

        result = analyze(
            symbol="USDT",
            screenshot_data=screenshot_data,
            search_data=search_data
        )

        assert result["symbol"] == "USDT"
        assert result["category"] == "stable"

    def test_full_analysis_meme(self):
        """Meme币完整流程"""
        screenshot_data = {
            "price": 0.1524,
            "clarity": "clear",
            "confidence": "high",
            "missing_elements": []
        }
        search_data = {"min": 0.149, "max": 0.155}

        result = analyze(
            symbol="DOGE",
            screenshot_data=screenshot_data,
            search_data=search_data
        )

        assert result["symbol"] == "DOGE"
        assert result["category"] == "meme"
        assert "risk_flags" in result

    def test_full_analysis_with_missing_search_data(self):
        """缺失搜索数据的分析"""
        screenshot_data = {"price": 100, "clarity": "clear", "confidence": "high"}
        search_data = {"min": None, "max": None}

        result = analyze(
            symbol="BTC",
            screenshot_data=screenshot_data,
            search_data=search_data
        )

        # 即使搜索数据缺失，也应该有输出
        assert result["symbol"] == "BTC"
        assert "input_reliability" in result


# ==================== TestVolumeDirection ====================

class TestVolumeDirection:
    """成交量方向感知测试"""

    def test_high_buying(self):
        """放量上涨"""
        from crypto_advisor import compute_indicator_signals
        ind = {'volume': {'current_bar': 10_000_000, 'current_bar_ma5': 5_000_000}, 'pct_change_24h': +5}
        vs = compute_indicator_signals(ind)['volume_status']
        assert vs['type'] == 'high_buying'
        assert '放量上涨' in vs['display']

    def test_high_selling(self):
        """放量下跌（CHIP场景）"""
        from crypto_advisor import compute_indicator_signals
        ind = {'volume': {'current_bar': 5_530_000_000, 'current_bar_ma5': 2_838_000_000}, 'pct_change_24h': -3.57}
        vs = compute_indicator_signals(ind)['volume_status']
        assert vs['type'] == 'high_selling'
        assert '放量下跌' in vs['display']

    def test_extremely_low(self):
        """极度缩量（XRP场景）"""
        from crypto_advisor import compute_indicator_signals
        ind = {'volume': {'current_bar': 506_000, 'current_bar_ma5': 12_600_000}, 'pct_change_24h': +0.01}
        vs = compute_indicator_signals(ind)['volume_status']
        assert vs['type'] == 'extremely_low'
        assert '极度缩量' in vs['display']

    def test_no_direction_defaults_to_high(self):
        """无价格方向时，高量比回退为'放量'"""
        from crypto_advisor import compute_indicator_signals
        ind = {'volume': {'current_bar': 10_000_000, 'current_bar_ma5': 5_000_000}}
        vs = compute_indicator_signals(ind)['volume_status']
        assert vs['type'] == 'high'


# ==================== TestFreshnessCheck ====================

class TestFreshnessCheck:
    """时效性判定测试"""

    def test_fresh_recent_screenshot(self):
        """1分钟前截图 → is_fresh=True"""
        from crypto_advisor import analyze
        from datetime import datetime, timezone, timedelta
        recent = (datetime.now(timezone(timedelta(hours=8))) - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
        r = analyze('CHIP',
            screenshot_data={'price': 0.06, 'time': recent, 'clarity': 'clear', 'confidence': 'high'},
            search_data={})
        assert r['freshness_check']['is_fresh'] is True

    def test_expired_screenshot(self):
        """60分钟前截图 → is_fresh=False（altcoin阈值15min）"""
        from crypto_advisor import analyze
        from datetime import datetime, timezone, timedelta
        old = (datetime.now(timezone(timedelta(hours=8))) - timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M')
        r = analyze('CHIP',
            screenshot_data={'price': 0.06, 'time': old, 'clarity': 'clear', 'confidence': 'high'},
            search_data={})
        assert r['freshness_check']['is_fresh'] is False

    def test_no_screenshot_time_still_fresh(self):
        """无截图时间 → is_fresh=True（回退）"""
        from crypto_advisor import analyze
        r = analyze('CHIP',
            screenshot_data={'price': 0.06, 'time': '', 'clarity': 'clear', 'confidence': 'high'},
            search_data={})
        assert r['freshness_check']['is_fresh'] is True


# ==================== TestTokenomics ====================

class TestTokenomics:
    """Tokenomics 解析测试"""

    def test_unlock_schedule_parsed(self):
        """解锁风险检测（CHIP：35个月至2029，5倍FDV/MCap）"""
        from crypto_advisor import analyze
        r = analyze('CHIP',
            screenshot_data={'price': 0.06, 'time': '2026-05-13 19:00', 'clarity': 'clear', 'confidence': 'high'},
            search_data={'min': 0.05, 'max': 0.07},
            search_text='CHIP连续35个月分批解锁至2029 FDV约9.43亿 MCap约1.89亿'
        )
        tok = r.get('tokenomics_risk', {})
        assert tok.get('unlock_risk') in ('高', '中', '低'), f"unlock_risk={tok.get('unlock_risk')}"
        assert tok.get('fdv_mcap_ratio') == pytest.approx(5.0, abs=0.1)
        assert '解锁' in tok.get('note', '')

    def test_fdv_mcap_ratio_parsed(self):
        """FDV/MCap 比率提取（5x左右）"""
        from crypto_advisor import analyze
        r = analyze('CHIP',
            screenshot_data={'price': 0.06, 'time': '2026-05-13 19:00', 'clarity': 'clear', 'confidence': 'high'},
            search_data={'min': 0.05, 'max': 0.07},
            search_text='FDV约9.43亿 MCap约1.89亿'
        )
        tok = r.get('tokenomics_risk', {})
        # fdv/mcap 为格式化字符串或数值
        assert tok.get('fdv_mcap_ratio') == pytest.approx(5.0, abs=0.1)
        assert 'fdv' in tok
        assert 'mcap' in tok


class TestDetermineBias:
    """组合信号矩阵 bias 判定"""

    def test_xrp_scenario_extreme_low_volume_death_cross(self):
        """XRP: 极度缩量+MACD死叉+价破均线 = neutral"""
        from crypto_advisor import determine_bias
        signals = {
            'ma_alignment': {'type': 'mixed'},
            'macd_signal': {'type': 'bearish'},
            'volume_status': {'type': 'low'},
            'price_vs_ma7': {'type': 'below_ma7'},
            'price_vs_ma25': {'type': 'below_ma25'},
            'price_vs_ma99': {'type': 'below_ma99'},
        }
        r = determine_bias(signals)
        assert r['bias'] == 'neutral'
        assert 'MACD空头' in r['logic']

    def test_mixed_signals_defaults_neutral(self):
        """混杂信号 + 无匹配矩阵行 → neutral"""
        from crypto_advisor import determine_bias
        signals = {
            'ma_alignment': {'type': 'unknown'},
            'macd_signal': {'type': 'unknown'},
            'volume_status': {'type': 'normal'},
        }
        r = determine_bias(signals)
        assert r['bias'] == 'neutral'
        assert '建议观望' in r['logic']

    def test_healthy_bullish_long(self):
        """多头排列+金叉+正常量 = long"""
        from crypto_advisor import determine_bias
        signals = {
            'ma_alignment': {'type': 'bullish'},
            'macd_signal': {'type': 'bullish'},
            'volume_status': {'type': 'normal'},
        }
        r = determine_bias(signals)
        assert r['bias'] == 'long'
        assert '趋势向上' in r['logic']

    def test_bearish_high_selling_short(self):
        """空头排列+放量下跌 = short"""
        from crypto_advisor import determine_bias
        signals = {
            'ma_alignment': {'type': 'bearish'},
            'macd_signal': {'type': 'bearish'},
            'volume_status': {'type': 'high_selling'},
        }
        r = determine_bias(signals)
        assert r['bias'] == 'short'
        assert '恐慌抛售' in r['logic']

    def test_bullish_low_volume_neutral(self):
        """多头排列+金叉+缩量 = neutral（缩量上涨）"""
        from crypto_advisor import determine_bias
        signals = {
            'ma_alignment': {'type': 'bullish'},
            'macd_signal': {'type': 'bullish'},
            'volume_status': {'type': 'low'},
        }
        r = determine_bias(signals)
        assert r['bias'] == 'neutral'
        assert '缩量上涨' in r['logic']


# ==================== Signal Reconciliation（v2.5）====================

class TestSignalReconciliation:
    """信号协调：S>A>B>C 多信息层权重覆盖"""

    def test_macro_override(self):
        """ETF巨量流入覆盖技术danger → warning"""
        from crypto_advisor import SignalReconciliation
        quick = {'risk_level': 'danger', 'triggered_by': ['trend_break']}
        deep = {'etf_netflow': 500_000_000, 'fear_greed_index': {'value': 50}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'context_adjusted'
        assert result['final_assessment'] == 'warning'
        assert result['dominant_layer'] == 'macro_flow'

    def test_confirmed(self):
        """无覆盖时确认原始信号"""
        from crypto_advisor import SignalReconciliation
        quick = {'risk_level': 'danger', 'triggered_by': ['panic_selling']}
        deep = {'etf_netflow': 0, 'fear_greed_index': {'value': 50}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'confirmed'
        assert result['overlays'] == []

    def test_onchain_override(self):
        """链上净流出覆盖缩量信号"""
        from crypto_advisor import SignalReconciliation
        quick = {'risk_level': 'warning', 'triggered_by': ['liquidity_dry']}
        deep = {'exchange_netflow': -5000, 'fear_greed_index': {'value': 50}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'context_adjusted'
        assert result['overlays'][0]['layer'] == 'onchain'

    def test_sentiment_fomo_fear(self):
        """FGI极度恐惧覆盖FOMO"""
        from crypto_advisor import SignalReconciliation
        quick = {'risk_level': 'danger', 'triggered_by': ['fomo_zone']}
        deep = {'etf_netflow': 0, 'fear_greed_index': {'value': 15}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'context_adjusted'
        assert result['overlays'][0]['layer'] == 'sentiment'

    def test_derive_danger_to_warning(self):
        """A级覆盖：danger → warning"""
        from crypto_advisor import SignalReconciliation
        quick = {'risk_level': 'danger', 'triggered_by': ['liquidity_dry']}
        deep = {'exchange_netflow': -5000, 'fear_greed_index': {'value': 50}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['final_assessment'] == 'warning'


# ==================== Confidence Engine v2.5 ====================

class TestConfidenceEngineV25:
    """完整版置信度引擎：指标自洽性校验"""

    def test_macd_inconsistency(self):
        """MACD柱与DIF/DEA不匹配"""
        from crypto_advisor import ConfidenceEngine
        indicators = {
            'ma': {'ma7': 100},
            'macd': {'dif': 1.0, 'dea': 0.5, 'macd': 999},
            'volume': {'current_bar': 1000, 'current_bar_ma5': 1000},
            'price_extremes': {'high': 110, 'low': 90},
            'current_price': 100
        }
        conf = ConfidenceEngine.calculate(
            {'clarity': 'clear', 'time': '2026-05-14', 'missing_elements': []},
            indicators, 'mainstream'
        )
        assert any('MACD' in d for d in conf['deductions'])

    def test_ma_price_divergence(self):
        """MA与价格偏离过大 → OCR警告"""
        from crypto_advisor import ConfidenceEngine
        indicators = {
            'ma': {'ma7': 1000},
            'macd': {'dif': 1, 'dea': 0.5, 'macd': 0.5},
            'volume': {'current_bar': 100, 'current_bar_ma5': 100},
            'price_extremes': {'high': 110, 'low': 90},
            'current_price': 100
        }
        conf = ConfidenceEngine.calculate(
            {'clarity': 'clear', 'time': '2026-05-14', 'missing_elements': []},
            indicators, 'mainstream'
        )
        assert any('偏离' in d for d in conf['deductions'])

    def test_volume_magnitude_error(self):
        """成交量数量级异常"""
        from crypto_advisor import ConfidenceEngine
        indicators = {
            'ma': {'ma7': 1},
            'macd': {'dif': 0, 'dea': 0, 'macd': 0},
            'volume': {'current_bar': 1_000_000, 'current_bar_ma5': 100},
            'price_extremes': {'high': 2, 'low': 0.5},
            'current_price': 1
        }
        conf = ConfidenceEngine.calculate(
            {'clarity': 'clear', 'time': '2026-05-14', 'missing_elements': []},
            indicators, 'mainstream'
        )
        assert any('数量级' in d for d in conf['deductions'])

    def test_all_clean_high_confidence(self):
        """指标自洽，高置信度"""
        from crypto_advisor import ConfidenceEngine
        indicators = {
            'ma': {'ma7': 100},
            'macd': {'dif': 1.0, 'dea': 0.5, 'macd': 0.5},  # 1-0.5=0.5 ✓
            'volume': {'current_bar': 1000, 'current_bar_ma5': 1000},
            'price_extremes': {'high': 110, 'low': 90},
            'current_price': 100
        }
        conf = ConfidenceEngine.calculate(
            {'clarity': 'clear', 'time': '2026-05-14', 'missing_elements': []},
            indicators, 'mainstream'
        )
        assert conf['level'] == 'high'
        assert conf['validation_details']['valid']


# ==================== neutral_bearish（v2.5）====================

class TestNeutralBearish:
    """结构偏空但无量确认档位"""

    def test_bearish_plus_normal_volume(self):
        """空头排列+死叉+正常量 = neutral_bearish"""
        signals = {
            'ma_alignment': {'type': 'bearish'},
            'macd_signal': {'type': 'bearish'},
            'volume_status': {'type': 'normal'},
            'volume_vs_ma5': 1.0
        }
        from crypto_advisor import _check_neutral_bearish
        assert _check_neutral_bearish(signals, {}) is True

    def test_bearish_plus_panic_not_nb(self):
        """空头排列+放量下跌 ≠ neutral_bearish"""
        signals = {
            'ma_alignment': {'type': 'bearish'},
            'macd_signal': {'type': 'bearish'},
            'volume_status': {'type': 'high_selling'},
            'volume_vs_ma5': 3.0
        }
        from crypto_advisor import _check_neutral_bearish
        assert _check_neutral_bearish(signals, {}) is False

    def test_warning_due_to_nb(self):
        """neutral_bearish 单独触发时降级为 warning"""
        from crypto_advisor import _determine_risk_state
        signals = {
            'ma_alignment': {'type': 'bearish'},
            'macd_signal': {'type': 'bearish'},
            'volume_status': {'type': 'normal'},
            'volume_vs_ma5': 1.0
        }
        risk = _determine_risk_state(signals, {'pct_change_24h': -2})
        # 死叉(2)+bearish_ma(1)+neutral_bearish(2)=5≥4 → danger
        # trend_break 优先于 neutral_bearish → bearish
        assert 'neutral_bearish' in risk['triggered_by']
        assert risk['risk_direction'] == 'bearish'

    def test_risk_direction_bearish(self):
        """恐慌抛售 → bearish"""
        from crypto_advisor import _determine_risk_state
        signals = {
            'volume_status': {'type': 'high_selling'},
            'macd_signal': {'type': 'bearish'},
            'ma_alignment': {'type': 'bearish'},
        }
        risk = _determine_risk_state(signals, {'pct_change_24h': -10})
        assert risk['risk_direction'] == 'bearish'

    def test_risk_direction_safe(self):
        """无触发器 → uncertain"""
        from crypto_advisor import _determine_risk_state
        signals = {
            'ma_alignment': {'type': 'bullish'},
            'macd_signal': {'type': 'bullish'},
            'volume_status': {'type': 'normal'},
        }
        risk = _determine_risk_state(signals, {'pct_change_24h': 1})
        assert risk['risk_level'] == 'safe'
        assert risk['risk_direction'] == 'uncertain'

    def test_structure_bearish_cautious(self):
        """空头排列+缩量 = cautious，不是 uncertain（GALA场景）"""
        from crypto_advisor import _derive_risk_direction
        triggered = [
            {'tag': 'structure_bearish', 'weight': 1, 'risk_desc': '均线空头排列', 'structure_impact': '中期趋势向下'},
            {'tag': 'liquidity_weak', 'weight': 1, 'risk_desc': '成交量萎缩', 'structure_impact': '流动性不足'},
        ]
        direction = _derive_risk_direction(triggered)
        assert direction == 'cautious', f"期望 cautious，实际 {direction}"

    def test_structure_bearish_with_trend_break_bearish(self):
        """空头排列+死叉 = bearish"""
        from crypto_advisor import _derive_risk_direction
        triggered = [
            {'tag': 'structure_bearish', 'weight': 1},
            {'tag': 'trend_break', 'weight': 2},
        ]
        direction = _derive_risk_direction(triggered)
        assert direction == 'bearish'

    def test_momentum_weak_cautious(self):
        """弱势金叉 = cautious"""
        from crypto_advisor import _derive_risk_direction
        triggered = [
            {'tag': 'momentum_weak', 'weight': 1, 'risk_desc': 'MACD弱势金叉', 'structure_impact': '动能不足'},
        ]
        direction = _derive_risk_direction(triggered)
        assert direction == 'cautious'


# ==================== 运行测试 ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
