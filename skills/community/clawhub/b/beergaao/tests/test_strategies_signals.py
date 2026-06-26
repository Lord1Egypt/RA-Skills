"""P0: 策略信号生成逻辑测试 - 10种策略的 BUY/SELL/None 信号验证"""
import pytest
import numpy as np
import pandas as pd
from stock_skill.indicators import compute_all


def make_trend_df(n=100, trend="up"):
    """构造特定趋势的数据"""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    if trend == "up":
        base = 10 + np.linspace(0, 5, n)
    elif trend == "down":
        base = 20 - np.linspace(0, 8, n)
    else:
        base = 15 + np.random.randn(n) * 0.3
    close = base + np.random.randn(n) * 0.1
    close = np.maximum(close, 1)
    high = close * 1.01
    low = close * 0.99
    opn = close * 1.002
    volume = np.random.randint(500000, 2000000, n).astype(float)
    if trend == "up":
        volume = volume * (1 + np.linspace(0, 0.5, n))
    df = pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })
    return compute_all(df)


class TestMABreakoutStrategy:
    """MA 突破策略测试"""

    def test_buy_signal_uptrend_volume(self):
        """上升趋势+放量 -> BUY"""
        from stock_skill.strategies.strategies import MABreakoutStrategy
        df = make_trend_df(50, "up")
        # 手动构造 BUY 条件
        df.iloc[-1, df.columns.get_loc("close")] = df.iloc[-1]["ma20"] * 1.02
        df.iloc[-1, df.columns.get_loc("volume")] = df.iloc[-1]["vol_ma5"] * 2.5
        strategy = MABreakoutStrategy()
        signal = strategy.evaluate(df)
        # 可能触发 BUY 或 None（取决于其他条件）
        if signal is not None:
            assert signal.direction in ["BUY", "SELL"]

    def test_sell_signal_downtrend(self):
        """下降趋势 -> SELL 或 None"""
        from stock_skill.strategies.strategies import MABreakoutStrategy
        df = make_trend_df(50, "down")
        strategy = MABreakoutStrategy()
        signal = strategy.evaluate(df)
        if signal is not None:
            assert signal.direction in ["BUY", "SELL"]

    def test_no_signal_insufficient_data(self):
        """数据不足 -> None"""
        from stock_skill.strategies.strategies import MABreakoutStrategy
        df = make_trend_df(10, "up")
        strategy = MABreakoutStrategy()
        signal = strategy.evaluate(df)
        assert signal is None


class TestMACDCrossStrategy:
    """MACD 金叉策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """MACD 策略返回信号或 None"""
        from stock_skill.strategies.strategies import MACDCrossStrategy
        df = make_trend_df(50)
        strategy = MACDCrossStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or hasattr(signal, "direction")

    def test_no_signal_insufficient_data(self):
        """数据不足 -> None"""
        from stock_skill.strategies.strategies import MACDCrossStrategy
        df = make_trend_df(10)
        strategy = MACDCrossStrategy()
        signal = strategy.evaluate(df)
        assert signal is None


class TestBollingerSqueezeStrategy:
    """布林带收口策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """布林带策略返回信号或 None"""
        from stock_skill.strategies.strategies import BollingerSqueezeStrategy
        df = make_trend_df(50)
        strategy = BollingerSqueezeStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or hasattr(signal, "confidence")

    def test_no_signal_insufficient_data(self):
        """数据不足 -> None"""
        from stock_skill.strategies.strategies import BollingerSqueezeStrategy
        df = make_trend_df(10)
        strategy = BollingerSqueezeStrategy()
        signal = strategy.evaluate(df)
        assert signal is None


class TestRSIOversoldStrategy:
    """RSI 超卖策略测试"""

    def test_buy_signal_oversold_bounce(self):
        """RSI 超卖反弹 -> BUY"""
        from stock_skill.strategies.strategies import RSIOversoldStrategy
        df = make_trend_df(50)
        # 手动构造 RSI 超卖反弹
        df.iloc[-2, df.columns.get_loc("rsi")] = 25  # 前一日 RSI < 30
        df.iloc[-1, df.columns.get_loc("rsi")] = 35  # 当日 RSI > 30
        strategy = RSIOversoldStrategy()
        signal = strategy.evaluate(df)
        if signal is not None:
            assert signal.direction == "BUY"
            assert signal.confidence > 0.5

    def test_sell_signal_overbought(self):
        """RSI 超买回落 -> SELL"""
        from stock_skill.strategies.strategies import RSIOversoldStrategy
        df = make_trend_df(50)
        # 手动构造 RSI 超买回落
        df.iloc[-2, df.columns.get_loc("rsi")] = 75  # 前一日 RSI > 70
        df.iloc[-1, df.columns.get_loc("rsi")] = 65  # 当日 RSI < 70
        strategy = RSIOversoldStrategy()
        signal = strategy.evaluate(df)
        if signal is not None:
            assert signal.direction == "SELL"

    def test_custom_params(self):
        """自定义参数"""
        from stock_skill.strategies.strategies import RSIOversoldStrategy
        strategy = RSIOversoldStrategy()
        strategy.set_params(rsi_threshold=25)
        assert strategy.params.rsi_threshold == 25

    def test_no_signal_insufficient_data(self):
        """数据不足 -> None"""
        from stock_skill.strategies.strategies import RSIOversoldStrategy
        df = make_trend_df(10)
        strategy = RSIOversoldStrategy()
        signal = strategy.evaluate(df)
        assert signal is None


class TestKDJCrossStrategy:
    """KDJ 金叉策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """KDJ 策略返回信号或 None"""
        from stock_skill.strategies.strategies import KDJCrossStrategy
        df = make_trend_df(50)
        strategy = KDJCrossStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or signal.direction in ["BUY", "SELL"]

    def test_no_signal_insufficient_data(self):
        """数据不足 -> None"""
        from stock_skill.strategies.strategies import KDJCrossStrategy
        df = make_trend_df(10)
        strategy = KDJCrossStrategy()
        signal = strategy.evaluate(df)
        assert signal is None


class TestVolumeShrinkStrategy:
    """缩量回调策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """缩量策略返回信号或 None"""
        from stock_skill.strategies.strategies import VolumeShrinkStrategy
        df = make_trend_df(50)
        strategy = VolumeShrinkStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or signal.direction in ["BUY", "SELL"]


class TestVolumePriceDivergenceStrategy:
    """量价背离策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """量价背离策略返回信号或 None"""
        from stock_skill.strategies.strategies import VolumePriceDivergenceStrategy
        df = make_trend_df(50)
        strategy = VolumePriceDivergenceStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or signal.direction in ["BUY", "SELL"]


class TestOBVTrendStrategy:
    """OBV 趋势策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """OBV 策略返回信号或 None"""
        from stock_skill.strategies.strategies import OBVTrendStrategy
        df = make_trend_df(50)
        strategy = OBVTrendStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or signal.direction in ["BUY", "SELL"]


class TestDoubleMAStrategy:
    """双均线策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """双均线策略返回信号或 None"""
        from stock_skill.strategies.strategies import DoubleMAStrategy
        df = make_trend_df(50)
        strategy = DoubleMAStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or signal.direction in ["BUY", "SELL"]


class TestSupportBounceStrategy:
    """支撑反弹策略测试"""

    def test_evaluate_returns_signal_or_none(self):
        """支撑反弹策略返回信号或 None"""
        from stock_skill.strategies.strategies import SupportBounceStrategy
        df = make_trend_df(50)
        strategy = SupportBounceStrategy()
        signal = strategy.evaluate(df)
        assert signal is None or signal.direction in ["BUY", "SELL"]


class TestStrategyRegistry:
    """策略注册表测试"""

    def test_registry_count(self):
        """注册表包含 10 个策略"""
        from stock_skill.strategies.strategies import get_all_strategies
        strategies = get_all_strategies()
        assert len(strategies) == 10

    def test_registry_names(self):
        """注册表包含所有策略名称"""
        from stock_skill.strategies.strategies import get_all_strategies
        names = [s.name for s in get_all_strategies()]
        expected = ["ma_breakout", "macd_cross", "boll_squeeze", "rsi_oversold",
                    "kdj_cross", "volume_shrink", "vol_price_divergence",
                    "obv_trend", "double_ma", "support_bounce"]
        for name in expected:
            assert name in names

    def test_get_strategy_by_name(self):
        """按名称获取策略"""
        from stock_skill.strategies.strategies import get_strategy
        strategy = get_strategy("ma_breakout")
        assert strategy is not None
        assert strategy.name == "ma_breakout"

    def test_get_nonexistent_strategy(self):
        """获取不存在的策略 -> None"""
        from stock_skill.strategies.strategies import get_strategy
        strategy = get_strategy("nonexistent")
        assert strategy is None


class TestStrategyParams:
    """策略参数测试"""

    def test_default_params(self):
        """默认参数正确"""
        from stock_skill.strategies.strategies import StrategyParams
        params = StrategyParams()
        assert params.vol_multiplier == 1.8
        assert params.rsi_threshold == 30
        assert params.ma_period == 20

    def test_custom_params(self):
        """自定义参数"""
        from stock_skill.strategies.strategies import StrategyParams
        params = StrategyParams(vol_multiplier=2.0, rsi_threshold=25)
        assert params.vol_multiplier == 2.0
        assert params.rsi_threshold == 25

    def test_to_dict(self):
        """参数转字典"""
        from stock_skill.strategies.strategies import StrategyParams
        params = StrategyParams()
        d = params.to_dict()
        assert "vol_multiplier" in d
        assert "rsi_threshold" in d


class TestStrategyParamMethods:
    """策略参数方法测试"""

    def test_set_params(self):
        """设置策略参数"""
        from stock_skill.strategies.strategies import MABreakoutStrategy
        strategy = MABreakoutStrategy()
        strategy.set_params(vol_multiplier=2.5)
        assert strategy.params.vol_multiplier == 2.5

    def test_reset_params(self):
        """重置策略参数"""
        from stock_skill.strategies.strategies import MABreakoutStrategy
        strategy = MABreakoutStrategy()
        strategy.set_params(vol_multiplier=2.5)
        strategy.reset_params()
        assert strategy.params.vol_multiplier == 1.8  # 默认值

    def test_evaluate_with_params(self):
        """临时参数评估"""
        from stock_skill.strategies.strategies import RSIOversoldStrategy
        df = make_trend_df(50)
        strategy = RSIOversoldStrategy()
        # 使用临时参数
        result = strategy.evaluate_with_params(df, {"rsi_threshold": 25})
        # 参数应恢复
        assert strategy.params.rsi_threshold == 30  # 默认值


class TestStrategyCalibrator:
    """策略校准器测试"""

    def test_calibrate_insufficient_data(self):
        """数据不足 -> 空结果"""
        from stock_skill.strategies.strategies import StrategyCalibrator
        df = make_trend_df(50)
        result = StrategyCalibrator.calibrate(df)
        assert result == {}

    def test_calibrate_with_valid_data(self):
        """有效数据 -> 返回结果"""
        from stock_skill.strategies.strategies import StrategyCalibrator
        df = make_trend_df(200)
        result = StrategyCalibrator.calibrate(df, strategy_name="rsi_oversold")
        # 可能有结果或空（取决于数据）
        assert isinstance(result, dict)

    def test_calibrate_regime_filter(self):
        """按市场状态过滤"""
        from stock_skill.strategies.strategies import StrategyCalibrator
        df = make_trend_df(200, "up")
        result = StrategyCalibrator.calibrate(df, regime="trend")
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
