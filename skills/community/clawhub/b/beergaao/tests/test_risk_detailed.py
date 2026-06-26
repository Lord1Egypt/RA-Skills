"""P0: 风控熔断完整测试 - 仓位管理、止损止盈、熔断机制、相关性检查"""
import pytest
import numpy as np
from stock_skill.risk import RiskManager, PositionResult, TrailingStop
from stock_skill.models import MarketAnalysis, MarketTrend, TradeSignal, SignalType


class TestCircuitBreaker:
    """熔断机制测试"""

    def test_circuit_breaker_limit_down(self):
        """跌停潮触发熔断：limit_down > 30"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.STRONG_DOWN, score=5.0,
            up_count=100, down_count=1900, total_count=2000,
            limit_up=0, limit_down=35
        )
        triggered, triggers = rm.circuit_breaker(market)
        assert triggered is True
        assert any("跌停潮" in t for t in triggers)

    def test_circuit_breaker_low_score(self):
        """极端弱势触发熔断：score < 2"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.STRONG_DOWN, score=1.5,
            up_count=200, down_count=1800, total_count=2000,
            limit_up=0, limit_down=10
        )
        triggered, triggers = rm.circuit_breaker(market)
        assert triggered is True
        assert any("极端弱势" in t for t in triggers)

    def test_circuit_breaker_plunge(self):
        """普跌触发熔断：down/total > 0.9"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.STRONG_DOWN, score=3.0,
            up_count=50, down_count=1950, total_count=2000,
            limit_up=0, limit_down=10
        )
        triggered, triggers = rm.circuit_breaker(market)
        assert triggered is True
        assert any("普跌" in t for t in triggers)

    def test_circuit_breaker_normal_market(self):
        """正常市场不触发熔断"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.SIDEWAYS, score=6.0,
            up_count=1000, down_count=1000, total_count=2000,
            limit_up=5, limit_down=5
        )
        triggered, triggers = rm.circuit_breaker(market)
        assert triggered is False
        assert triggers == []

    def test_circuit_breaker_multiple_triggers(self):
        """多条件同时满足 -> 全部原因"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.STRONG_DOWN, score=1.0,
            up_count=100, down_count=1900, total_count=2000,
            limit_up=0, limit_down=50
        )
        triggered, triggers = rm.circuit_breaker(market)
        assert triggered is True
        assert len(triggers) == 3  # 跌停潮 + 极端弱势 + 普跌

    @pytest.mark.parametrize("limit_down,score,down_ratio,expected", [
        (31, 5.0, 0.5, True),   # 仅跌停潮
        (10, 1.5, 0.5, True),   # 仅极端弱势
        (10, 5.0, 0.95, True),  # 仅普跌
        (29, 2.0, 0.89, False), # 全部不满足
    ])
    def test_circuit_breaker_boundary(self, limit_down, score, down_ratio, expected):
        """边界值测试"""
        rm = RiskManager()
        total = 2000
        down = int(total * down_ratio)
        market = MarketAnalysis(
            trend=MarketTrend.STRONG_DOWN, score=score,
            up_count=total - down, down_count=down, total_count=total,
            limit_up=0, limit_down=limit_down
        )
        triggered, _ = rm.circuit_breaker(market)
        assert triggered == expected


class TestPositionCalculation:
    """仓位计算测试"""

    def test_position_high_confidence_high_market(self):
        """高置信+高市场评分 -> 仓位接近上限"""
        rm = RiskManager()
        result = rm.calculate_position(
            confidence=0.9, market_score=9, signal_count=1
        )
        assert result.position_pct >= 0.25
        assert result.position_pct <= rm.max_single

    def test_position_low_confidence_low_market(self):
        """低置信+低市场评分 -> 仓位接近 5%"""
        rm = RiskManager()
        result = rm.calculate_position(
            confidence=0.3, market_score=1, signal_count=3
        )
        assert result.position_pct == pytest.approx(0.05, abs=0.02)

    def test_position_high_atr(self):
        """高 ATR -> atr_factor=0.7"""
        rm = RiskManager()
        # ATR 5% of price
        result = rm.calculate_position(
            confidence=0.7, market_score=6, signal_count=1,
            atr=0.5, current_price=10.0
        )
        result_normal = rm.calculate_position(
            confidence=0.7, market_score=6, signal_count=1,
            atr=0.0, current_price=10.0
        )
        assert result.position_pct < result_normal.position_pct

    def test_position_medium_atr(self):
        """中等 ATR -> atr_factor=0.85"""
        rm = RiskManager()
        # ATR 3.5% of price
        result = rm.calculate_position(
            confidence=0.7, market_score=6, signal_count=1,
            atr=0.35, current_price=10.0
        )
        result_high = rm.calculate_position(
            confidence=0.7, market_score=6, signal_count=1,
            atr=0.5, current_price=10.0
        )
        assert result.position_pct > result_high.position_pct

    def test_position_multiple_signals(self):
        """多信号分摊仓位"""
        rm = RiskManager()
        result1 = rm.calculate_position(confidence=0.7, market_score=6, signal_count=1)
        result2 = rm.calculate_position(confidence=0.7, market_score=6, signal_count=2)
        assert result2.position_pct < result1.position_pct

    def test_position_clamp_bounds(self):
        """仓位上下限约束"""
        rm = RiskManager()
        # 最大仓位
        result_max = rm.calculate_position(confidence=1.0, market_score=10, signal_count=1)
        assert result_max.position_pct <= rm.max_single
        # 最小仓位
        result_min = rm.calculate_position(confidence=0.1, market_score=0, signal_count=10)
        assert result_min.position_pct >= 0.05


class TestStopLoss:
    """止损计算测试"""

    def test_stop_loss_fixed(self):
        """固定止损"""
        rm = RiskManager()
        stop = rm.calculate_stop_loss(10.0)
        assert stop == pytest.approx(10.0 * (1 + rm.stop_loss_rate), abs=0.01)

    def test_stop_loss_atr_optimal(self):
        """ATR 止损最优"""
        rm = RiskManager()
        # 大 ATR -> 止损位更高
        stop = rm.calculate_stop_loss(10.0, atr=1.0)
        fixed_stop = 10.0 * (1 + rm.stop_loss_rate)
        assert stop > fixed_stop

    def test_stop_loss_support_optimal(self):
        """支撑位止损最优"""
        rm = RiskManager()
        # 支撑位接近价格
        stop = rm.calculate_stop_loss(10.0, support=9.8)
        fixed_stop = 10.0 * (1 + rm.stop_loss_rate)
        assert stop > fixed_stop

    def test_stop_loss_combined(self):
        """综合止损（取最高值）"""
        rm = RiskManager()
        stop = rm.calculate_stop_loss(10.0, atr=0.5, support=9.5)
        fixed_stop = 10.0 * (1 + rm.stop_loss_rate)
        atr_stop = 10.0 - 2 * 0.5
        support_stop = 9.5 * 0.98
        assert stop == pytest.approx(max(fixed_stop, atr_stop, support_stop), abs=0.01)


class TestTargetCalculation:
    """止盈计算测试"""

    def test_target_fixed(self):
        """固定止盈"""
        rm = RiskManager()
        target = rm.calculate_target(10.0)
        assert target == pytest.approx(10.0 * (1 + rm.target_rate), abs=0.01)

    def test_target_atr_optimal(self):
        """ATR 止盈最优"""
        rm = RiskManager()
        target = rm.calculate_target(10.0, atr=0.5)
        fixed_target = 10.0 * (1 + rm.target_rate)
        assert target <= fixed_target

    def test_target_resistance_optimal(self):
        """阻力位止盈最优"""
        rm = RiskManager()
        target = rm.calculate_target(10.0, resistance=10.3)
        fixed_target = 10.0 * (1 + rm.target_rate)
        assert target == pytest.approx(10.3, abs=0.01)


class TestTrailingStop:
    """移动止损测试"""

    def test_trailing_stop_initial(self):
        """初始止损设置正确"""
        rm = RiskManager()
        ts = rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        assert ts.code == "TEST.SH"
        assert ts.entry_price == 10.0
        assert ts.highest_price == 10.0
        assert ts.atr == 0.5

    def test_trailing_stop_move_up(self):
        """价格创新高 -> 止损上移"""
        rm = RiskManager()
        ts = rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        initial_stop = ts.current_stop
        # 价格上涨
        ts.update(11.0)
        assert ts.highest_price == 11.0
        assert ts.current_stop > initial_stop

    def test_trailing_stop_no_move_down(self):
        """价格下跌 -> 止损不回落"""
        rm = RiskManager()
        ts = rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        # 先上涨
        ts.update(11.0)
        stop_after_up = ts.current_stop
        # 再下跌
        ts.update(10.5)
        assert ts.current_stop == stop_after_up  # 止损位不变

    def test_trailing_stop_trigger(self):
        """价格跌破止损 -> 触发"""
        rm = RiskManager()
        ts = rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        # 价格跌破止损位
        assert ts.is_triggered(ts.current_stop - 0.1) is True

    def test_trailing_stop_not_trigger(self):
        """价格高于止损 -> 不触发"""
        rm = RiskManager()
        ts = rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        assert ts.is_triggered(10.0) is False

    def test_update_trailing_stop_integration(self):
        """RiskManager.update_trailing_stop 集成测试"""
        rm = RiskManager()
        rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        # 价格上涨
        result1 = rm.update_trailing_stop("TEST.SH", 11.0)
        assert result1 is None  # 未触发
        # 价格暴跌
        result2 = rm.update_trailing_stop("TEST.SH", 8.0)
        assert result2 is not None  # 触发止损

    def test_remove_trailing_stop(self):
        """移除移动止损"""
        rm = RiskManager()
        rm.init_trailing_stop("TEST.SH", 10.0, 0.5)
        rm.remove_trailing_stop("TEST.SH")
        result = rm.update_trailing_stop("TEST.SH", 11.0)
        assert result is None

    def test_update_nonexistent_trailing_stop(self):
        """更新不存在的移动止损"""
        rm = RiskManager()
        result = rm.update_trailing_stop("NONEXISTENT.SH", 10.0)
        assert result is None


class TestCorrelationCheck:
    """相关性检查测试"""

    def test_correlation_high(self):
        """高相关序列 -> warning"""
        rm = RiskManager()
        np.random.seed(42)
        returns = np.random.randn(100)
        returns_dict = {
            "STOCK_A.SH": returns,
            "STOCK_B.SH": returns + np.random.randn(100) * 0.01  # 几乎完全相关
        }
        warnings, corr_matrix = rm.check_portfolio_correlation(returns_dict)
        assert len(warnings) > 0
        assert "相关性" in warnings[0]

    def test_correlation_low(self):
        """低相关序列 -> 无 warning"""
        rm = RiskManager()
        np.random.seed(42)
        returns_dict = {
            "STOCK_A.SH": np.random.randn(100),
            "STOCK_B.SH": np.random.randn(100)
        }
        warnings, _ = rm.check_portfolio_correlation(returns_dict)
        # 随机序列相关性通常较低
        assert len(warnings) == 0

    def test_correlation_single_stock(self):
        """只有 1 只股票 -> 无 warning"""
        rm = RiskManager()
        returns_dict = {"STOCK_A.SH": np.random.randn(100)}
        warnings, _ = rm.check_portfolio_correlation(returns_dict)
        assert warnings == []

    def test_correlation_empty(self):
        """空数据 -> 无 warning"""
        rm = RiskManager()
        warnings, _ = rm.check_portfolio_correlation({})
        assert warnings == []


class TestShouldOpen:
    """开仓条件测试"""

    def test_should_open_above_threshold(self):
        """市场评分 >= 阈值 -> 允许开仓"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.WEAK_UP, score=rm.min_market_score + 1,
            up_count=1000, down_count=1000, total_count=2000
        )
        assert rm.should_open(market) is True

    def test_should_open_below_threshold(self):
        """市场评分 < 阈值 -> 不允许开仓"""
        rm = RiskManager()
        market = MarketAnalysis(
            trend=MarketTrend.WEAK_DOWN, score=rm.min_market_score - 1,
            up_count=1000, down_count=1000, total_count=2000
        )
        assert rm.should_open(market) is False


class TestAdjustConfidence:
    """置信度调整测试"""

    def test_adjust_confidence_high_bt_wr(self):
        """高回测胜率 -> 置信度提升"""
        rm = RiskManager()
        adjusted = rm.adjust_confidence(0.6, bt_wr=0.7, n_strats=2)
        assert adjusted > 0.6

    def test_adjust_confidence_low_bt_wr(self):
        """低回测胜率 -> 置信度降低"""
        rm = RiskManager()
        adjusted = rm.adjust_confidence(0.6, bt_wr=0.3, n_strats=2)
        assert adjusted < 0.6

    def test_adjust_confidence_resonance(self):
        """多策略共振 -> 置信度提升"""
        rm = RiskManager()
        adj1 = rm.adjust_confidence(0.6, bt_wr=0.5, n_strats=1)
        adj3 = rm.adjust_confidence(0.6, bt_wr=0.5, n_strats=3)
        assert adj3 > adj1

    def test_adjust_confidence_clamp(self):
        """置信度限制在 [0, 1]"""
        rm = RiskManager()
        assert rm.adjust_confidence(1.0, bt_wr=1.0, n_strats=10) <= 1.0
        assert rm.adjust_confidence(0.0, bt_wr=0.0, n_strats=1) >= 0.0


class TestRiskCheck:
    """总仓位检查测试"""

    def test_risk_check_within_limit(self):
        """总仓位在限制内 -> 无 warning"""
        rm = RiskManager()
        signals = [
            TradeSignal(code="A.SH", name="A", signal_type=SignalType.BUY,
                       price=10, support=9, resistance=11, stop_loss=9.5,
                       target_price=11, position_pct=0.3, confidence=0.7, reason="test"),
            TradeSignal(code="B.SH", name="B", signal_type=SignalType.BUY,
                       price=20, support=18, resistance=22, stop_loss=19,
                       target_price=22, position_pct=0.3, confidence=0.7, reason="test"),
        ]
        warnings = rm.risk_check(signals)
        assert len(warnings) == 0

    def test_risk_check_exceed_limit(self):
        """总仓位超限 -> warning"""
        rm = RiskManager()
        signals = [
            TradeSignal(code="A.SH", name="A", signal_type=SignalType.BUY,
                       price=10, support=9, resistance=11, stop_loss=9.5,
                       target_price=11, position_pct=0.5, confidence=0.7, reason="test"),
            TradeSignal(code="B.SH", name="B", signal_type=SignalType.BUY,
                       price=20, support=18, resistance=22, stop_loss=19,
                       target_price=22, position_pct=0.5, confidence=0.7, reason="test"),
        ]
        warnings = rm.risk_check(signals)
        assert len(warnings) > 0
        assert "总仓位" in warnings[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
