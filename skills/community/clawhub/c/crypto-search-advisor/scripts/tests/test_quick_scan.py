#!/usr/bin/env python3
"""
Quick Scan v3 — 风险警报器范式 自动化测试
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quick_scan import (
    TRIGGER_REGISTRY,
    determine_risk_state,
    ConfidenceEngine,
    SignalReconciliation,
    quick_scan_v3,
    quick_scan_v2,
    quick_scan,
    FORBIDDEN_DIRECTION_WORDS,
    _check_below_all_ma,
    _check_fomo_extreme,
    _check_price_extension,
)


class TestTriggers:
    def test_panic_selling(self):
        s = {'volume_status': {'type': 'high_selling'}}
        assert TRIGGER_REGISTRY['panic_selling']['check'](s, {})

    def test_death_cross(self):
        s = {'macd_signal': {'type': 'bearish'}}
        assert TRIGGER_REGISTRY['death_cross']['check'](s, {})

    def test_extremely_low_volume(self):
        s = {'volume_status': {'type': 'extremely_low'}}
        assert TRIGGER_REGISTRY['extremely_low_volume']['check'](s, {})

    def test_low_volume(self):
        s = {'volume_status': {'type': 'low'}}
        assert TRIGGER_REGISTRY['low_volume']['check'](s, {})

    def test_below_ma7(self):
        s = {'price_vs_ma7': {'type': 'below_ma7'}}
        assert TRIGGER_REGISTRY['below_ma7']['check'](s, {})

    def test_below_all_ma(self):
        s = {
            'price_vs_ma7': {'type': 'below_ma7'},
            'price_vs_ma25': {'type': 'below_ma25'},
            'price_vs_ma99': {'type': 'below_ma99'},
        }
        assert _check_below_all_ma(s, {})

    def test_below_only_one_ma_not_all(self):
        s = {'price_vs_ma7': {'type': 'below_ma7'}}
        assert not _check_below_all_ma(s, {})

    def test_bearish_ma(self):
        s = {'ma_alignment': {'type': 'bearish'}}
        assert TRIGGER_REGISTRY['bearish_ma']['check'](s, {})

    def test_fomo(self):
        s = {'volume_vs_ma5': 3.0}
        d = {'pct_change_24h': 25}
        assert _check_fomo_extreme(s, d)

    def test_fomo_low_vol(self):
        s = {'volume_vs_ma5': 0.3}
        d = {'pct_change_24h': 18}
        assert _check_fomo_extreme(s, d)

    def test_fomo_no(self):
        s = {'volume_vs_ma5': 1.0}
        d = {'pct_change_24h': 5}
        assert not _check_fomo_extreme(s, d)

    def test_price_extension(self):
        d = {'price': 0.12, '_raw_indicators': {'ma': {'ma7': 0.10}}}
        assert _check_price_extension({}, d)


class TestConfidenceEngine:
    def test_high_perfect(self):
        d = {'clarity': 'clear', 'time': '2026-05-14', 'timeframe': '4h'}
        ind = {'ma': {}, 'macd': {}, 'volume': {}, 'price_extremes': {}}
        c = ConfidenceEngine.calculate(d, ind, 'mainstream')
        assert c['level'] == 'high'
        assert c['score'] == 100

    def test_low_blurry_missing(self):
        d = {'clarity': 'blurry', 'missing_elements': ['volume', 'macd']}
        ind = {}
        c = ConfidenceEngine.calculate(d, ind, 'meme')
        assert c['level'] == 'low'
        assert 'Meme币高波动' in c['deductions'][-1]

    def test_altcoin_discount(self):
        d = {'clarity': 'clear', 'time': 'today', 'timeframe': '1h'}
        ind = {'ma': {}, 'macd': {}, 'volume': {}, 'price_extremes': {}}
        c = ConfidenceEngine.calculate(d, ind, 'altcoin')
        assert '山寨币流动性差' in c['deductions'][0]
        assert c['score'] == 95

    def test_meme_discount(self):
        d = {'clarity': 'clear', 'time': 'today', 'timeframe': '1h'}
        ind = {'ma': {}, 'macd': {}, 'volume': {}, 'price_extremes': {}}
        c = ConfidenceEngine.calculate(d, ind, 'meme')
        assert 'Meme币高波动' in c['deductions'][0]
        assert c['score'] == 90

    def test_macd_inconsistency(self):
        d = {'clarity': 'clear', 'time': 'now', 'timeframe': '1h'}
        ind = {
            'ma': {'ma7': 100}, 'current_price': 100,
            'macd': {'dif': 5, 'dea': 2, 'macd': 10},  # 5-2=3 ≠ 10
            'volume': {'current_bar': 1000, 'current_bar_ma5': 1000},
            'price_extremes': {'high': 110, 'low': 90},
        }
        c = ConfidenceEngine.calculate(d, ind, 'mainstream')
        assert 'MACD柱与DIF/DEA计算不匹配' in c['deductions']

    def test_price_ma_divergence(self):
        d = {'clarity': 'clear', 'time': 'now', 'timeframe': '1h'}
        ind = {
            'ma': {'ma7': 10}, 'current_price': 100,
            'macd': {'dif': 1, 'dea': 0.5, 'macd': 0.5},
            'volume': {'current_bar': 1000, 'current_bar_ma5': 1000},
            'price_extremes': {'high': 110, 'low': 90},
        }
        c = ConfidenceEngine.calculate(d, ind, 'mainstream')
        assert '疑似OCR错误' in str(c['deductions'])


class TestRiskState:
    def test_safe(self):
        s = {
            'ma_alignment': {'type': 'bullish'},
            'macd_signal': {'type': 'bullish'},
            'volume_status': {'type': 'normal'},
            'price_vs_ma7': {'type': 'above_ma7'},
        }
        risk = determine_risk_state(s, {'price': 100, 'pct_change_24h': 1})
        assert risk['risk_level'] == 'safe'

    def test_warning(self):
        s = {
            'volume_status': {'type': 'low'},
            'price_vs_ma7': {'type': 'below_ma7'},
        }
        risk = determine_risk_state(s, {'price': 50, 'pct_change_24h': -1})
        assert risk['risk_level'] == 'warning'

    def test_danger(self):
        s = {
            'volume_status': {'type': 'high_selling'},
            'macd_signal': {'type': 'bearish'},
            # 3+2=5 → danger (≥4, <6)
        }
        risk = determine_risk_state(s, {'price': 100, 'pct_change_24h': -5})
        assert risk['risk_level'] == 'danger'

    def test_critical(self):
        s = {
            'volume_status': {'type': 'high_selling'},
            'macd_signal': {'type': 'bearish'},
            'ma_alignment': {'type': 'bearish'},
            'price_vs_ma7': {'type': 'below_ma7'},
            'price_vs_ma25': {'type': 'below_ma25'},
            'price_vs_ma99': {'type': 'below_ma99'},
        }
        risk = determine_risk_state(s, {'price': 10, 'pct_change_24h': -25})
        assert risk['risk_level'] == 'critical'


class TestSignalReconciliation:
    def test_macro_flow_overlay(self):
        quick = {'risk_level': 'danger', 'triggered_by': ['trend_break']}
        deep = {'etf_netflow': 500_000_000}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'context_adjusted'
        assert result['overlays'][0]['layer'] == 'macro_flow'
        assert result['overlays'][0]['weight'] == 'S'

    def test_onchain_overlay(self):
        quick = {'risk_level': 'warning', 'triggered_by': ['liquidity_dry']}
        deep = {'exchange_netflow': -5000}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'context_adjusted'
        assert result['overlays'][0]['layer'] == 'onchain'

    def test_sentiment_fomo_fear(self):
        quick = {'risk_level': 'danger', 'triggered_by': ['fomo_zone']}
        deep = {'fear_greed_index': {'value': 15}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'context_adjusted'
        assert result['overlays'][0]['layer'] == 'sentiment'

    def test_confirmed_no_overlays(self):
        quick = {'risk_level': 'safe', 'triggered_by': []}
        deep = {}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['status'] == 'confirmed'

    def test_s_first_when_multiple(self):
        quick = {'risk_level': 'danger', 'triggered_by': ['fomo_zone']}
        deep = {'etf_netflow': 500_000_000, 'exchange_netflow': -5000,
                'fear_greed_index': {'value': 15}}
        result = SignalReconciliation.reconcile(quick, deep)
        assert result['overlays'][0]['weight'] == 'S'
        assert result['dominant_layer'] == 'macro_flow'


class TestForbiddenWords:
    """v3 核心：禁止方向预测词汇"""

    def test_st_no_forbidden(self):
        ss = {
            'price': 0.080696, 'time': '2026-05-13 19:53',
            'timeframe': '4h', 'clarity': 'clear',
            'missing_elements': [], 'pct_change_24h': -3.57,
        }
        ind = {
            'ma': {'ma7': 0.080596, 'ma25': 0.080497, 'ma99': 0.080221},
            'macd': {'dif': 0.000069, 'dea': 0.000064, 'macd': 0.000005},
            'volume': {'current_bar': 1406759, 'current_bar_ma5': 1352753,
                       'current_bar_ma10': 1347958},
            'price_extremes': {'high_24h': 0.080700, 'low_24h': 0.079895},
            'current_price': 0.080696,
        }
        ss['_raw_indicators'] = ind
        text = quick_scan_v3('ST', 'altcoin', ss, ind)

        for word in FORBIDDEN_DIRECTION_WORDS:
            assert word not in text, f"禁止方向词汇: {word}"

    def test_btc_no_forbidden(self):
        ss = {
            'price': 79716, 'timeframe': '1h', 'clarity': 'clear',
            'missing_elements': [], 'pct_change_24h': -2.5,
        }
        ind = {
            'ma': {'ma7': 80448, 'ma25': 80645, 'ma99': 80918},
            'macd': {'dif': -201.8, 'dea': -66.5, 'macd': -135.3},
            'volume': {'current_bar': 1250000, 'current_bar_ma5': 1000000},
            'current_price': 79716,
        }
        ss['_raw_indicators'] = ind
        text = quick_scan_v3('BTC', 'mainstream', ss, ind)

        for word in FORBIDDEN_DIRECTION_WORDS:
            assert word not in text, f"禁止方向词汇: {word}"


class TestV3StructureContent:
    def test_required_sections(self):
        ss = {
            'price': 0.080696, 'time': '2026-05-13 19:53',
            'timeframe': '4h', 'clarity': 'clear',
            'missing_elements': [], 'pct_change_24h': -3.57,
        }
        ind = {
            'ma': {'ma7': 0.080596, 'ma25': 0.080497, 'ma99': 0.080221},
            'macd': {'dif': 0.000069, 'dea': 0.000064, 'macd': 0.000005},
            'volume': {'current_bar': 1406759, 'current_bar_ma5': 1352753},
            'price_extremes': {'high_24h': 0.080700, 'low_24h': 0.079895},
            'current_price': 0.080696,
        }
        ss['_raw_indicators'] = ind
        text = quick_scan_v3('ST', 'altcoin', ss, ind)

        assert '结构状态' in text
        assert '风险等级' in text
        assert '置信度' in text
        assert '不涉及宏观' in text
        assert '详细分析生成中' in text

    def test_btc_bearish_structure(self):
        ss = {
            'price': 79716, 'timeframe': '1h', 'clarity': 'clear',
            'missing_elements': [], 'pct_change_24h': -2.5,
        }
        ind = {
            'ma': {'ma7': 80448, 'ma25': 80645, 'ma99': 80918},
            'macd': {'dif': -201.8, 'dea': -66.5, 'macd': -135.3},
            'volume': {'current_bar': 1250000, 'current_bar_ma5': 1000000},
            'current_price': 79716,
        }
        ss['_raw_indicators'] = ind
        text = quick_scan_v3('BTC', 'mainstream', ss, ind)
        assert '空头排列' in text or '死叉' in text


class TestBackwardCompat:
    def test_quick_scan_v2(self):
        text = quick_scan_v2('ETH', 'mainstream', {'price': 3000, 'timeframe': '1d'}, {})
        assert 'ETH' in text

    def test_quick_scan_legacy(self):
        text = quick_scan('DOGE', {'price': 0.5, 'asset_type': 'meme'}, {})
        assert 'DOGE' in text

    def test_empty_crash(self):
        text = quick_scan_v3('X', 'altcoin', {'price': 1}, {})
        assert isinstance(text, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])