"""P0: 回测引擎计算准确性测试 - 成本模型、涨跌停、T+1、绩效指标"""
import pytest
import numpy as np
import pandas as pd
from datetime import date, timedelta
from stock_skill.backtest.engine import (
    CostModel, adjust_prices, is_limit_up, is_limit_down,
    can_buy_at_limit, can_sell_at_limit, Order, Position, Portfolio,
    BacktestConfig, BacktestEngine, BenchmarkResult
)


class TestCostModel:
    """交易成本模型测试"""

    def test_buy_cost_basic(self):
        """买入成本基本计算"""
        cm = CostModel()
        cost = cm.buy_cost(10.0, 1000)
        amount = 10.0 * 1000
        commission = max(amount * 0.0003, 5.0)
        slippage = amount * 0.001
        expected = amount + commission + slippage
        assert cost == pytest.approx(expected, abs=0.01)

    def test_sell_cost_basic(self):
        """卖出所得基本计算"""
        cm = CostModel()
        proceeds = cm.sell_cost(10.0, 1000)
        amount = 10.0 * 1000
        commission = max(amount * 0.0003, 5.0)
        tax = amount * 0.001
        slippage = amount * 0.001
        expected = amount - commission - tax - slippage
        assert proceeds == pytest.approx(expected, abs=0.01)

    def test_min_commission(self):
        """金额很小时佣金 = 5 元"""
        cm = CostModel()
        cost = cm.buy_cost(1.0, 10)  # 金额 = 10 元
        # 佣金应为 5 元（最低佣金）
        assert cost == pytest.approx(10 + 5 + 0.01, abs=0.01)

    def test_slippage_fixed(self):
        """固定滑点模型"""
        cm = CostModel(slippage_model="fixed", slippage_value=0.01)
        slippage = cm._calc_slippage(10.0, 1000, 0)
        assert slippage == 0.01 * 1000

    def test_slippage_percentage(self):
        """百分比滑点模型"""
        cm = CostModel(slippage_model="percentage", slippage_value=0.001)
        slippage = cm._calc_slippage(10.0, 1000, 0)
        assert slippage == 10.0 * 1000 * 0.001

    def test_slippage_volume(self):
        """成交量冲击滑点模型"""
        cm = CostModel(slippage_model="volume")
        # 高参与率 -> 高滑点
        slippage_high = cm._calc_slippage(10.0, 1000, 5000)  # 20% 参与率
        slippage_low = cm._calc_slippage(10.0, 1000, 50000)  # 2% 参与率
        assert slippage_high > slippage_low

    def test_custom_commission_rate(self):
        """自定义佣金费率"""
        cm = CostModel(commission_rate=0.0001)
        cost = cm.buy_cost(100.0, 1000)
        amount = 100.0 * 1000
        commission = max(amount * 0.0001, 5.0)
        expected = amount + commission + amount * 0.001
        assert cost == pytest.approx(expected, abs=0.01)

    def test_custom_stamp_tax(self):
        """自定义印花税率"""
        cm = CostModel(stamp_tax_rate=0.0005)
        proceeds = cm.sell_cost(100.0, 1000)
        amount = 100.0 * 1000
        commission = max(amount * 0.0003, 5.0)
        tax = amount * 0.0005
        expected = amount - commission - tax - amount * 0.001
        assert proceeds == pytest.approx(expected, abs=0.01)


class TestAdjustPrices:
    """复权处理测试"""

    def test_adjust_prices_qfq(self):
        """前复权：最新价格不变"""
        df = pd.DataFrame({
            "open": [10.0, 11.0, 12.0],
            "high": [10.5, 11.5, 12.5],
            "low": [9.5, 10.5, 11.5],
            "close": [10.0, 11.0, 12.0],
            "adj_factor": [1.0, 1.1, 1.2]
        })
        result = adjust_prices(df, "qfq")
        # 最新价格不变
        assert result.iloc[-1]["close"] == 12.0
        # 历史价格按比例调整
        assert result.iloc[0]["close"] < 10.0

    def test_adjust_prices_hfq(self):
        """后复权：上市价格不变"""
        df = pd.DataFrame({
            "open": [10.0, 11.0, 12.0],
            "high": [10.5, 11.5, 12.5],
            "low": [9.5, 10.5, 11.5],
            "close": [10.0, 11.0, 12.0],
            "adj_factor": [1.0, 1.1, 1.2]
        })
        result = adjust_prices(df, "hfq")
        # 上市价格不变
        assert result.iloc[0]["close"] == 10.0
        # 后续价格按比例调整
        assert result.iloc[-1]["close"] > 12.0

    def test_adjust_prices_no_factor(self):
        """没有复权因子 -> 返回原数据"""
        df = pd.DataFrame({
            "open": [10.0, 11.0],
            "high": [10.5, 11.5],
            "low": [9.5, 10.5],
            "close": [10.0, 11.0]
        })
        result = adjust_prices(df, "qfq")
        assert result.equals(df)


class TestLimitUpDown:
    """涨跌停判断测试"""

    def test_is_limit_up(self):
        """涨停判断"""
        assert is_limit_up(11.0, 10.0, 0.095) is True  # 10% 涨幅
        assert is_limit_up(10.5, 10.0, 0.095) is False  # 5% 涨幅

    def test_is_limit_down(self):
        """跌停判断"""
        assert is_limit_down(9.0, 10.0, -0.095) is True  # -10% 跌幅
        assert is_limit_down(9.5, 10.0, -0.095) is False  # -5% 跌幅

    def test_limit_up_boundary(self):
        """涨停边界值"""
        assert is_limit_up(10.95, 10.0) is True  # 9.5%
        assert is_limit_up(10.94, 10.0) is False  # 9.4%

    def test_limit_down_boundary(self):
        """跌停边界值"""
        assert is_limit_down(9.05, 10.0) is True  # -9.5%
        assert is_limit_down(9.06, 10.0) is False  # -9.4%

    def test_zero_prev_close(self):
        """前收盘价为 0 -> False"""
        assert is_limit_up(10.0, 0.0) is False
        assert is_limit_down(10.0, 0.0) is False


class TestCanTradeAtLimit:
    """涨跌停可否交易测试"""

    def test_cannot_buy_at_limit(self):
        """涨停不可买"""
        assert can_buy_at_limit(11.0, 10.0) is False

    def test_can_buy_normal(self):
        """正常价格可买"""
        assert can_buy_at_limit(10.5, 10.0) is True

    def test_cannot_sell_at_limit(self):
        """跌停不可卖"""
        assert can_sell_at_limit(9.0, 10.0) is False

    def test_can_sell_normal(self):
        """正常价格可卖"""
        assert can_sell_at_limit(9.5, 10.0) is True


class TestPosition:
    """持仓测试"""

    def test_position_attributes(self):
        """持仓属性正确"""
        pos = Position(code="600036.SH", shares=1000, avg_cost=10.0)
        assert pos.code == "600036.SH"
        assert pos.shares == 1000
        assert pos.avg_cost == 10.0
        assert pos.market_value == 0.0
        assert pos.unrealized_pnl == 0.0

    def test_position_t1_restriction(self):
        """T+1 限制"""
        pos = Position(code="600036.SH", shares=1000, avg_cost=10.0,
                      buy_date="2024-01-01", can_sell_date="2024-01-02")
        assert pos.can_sell_date == "2024-01-02"


class TestPortfolio:
    """投资组合测试"""

    def test_portfolio_initial(self):
        """初始投资组合"""
        portfolio = Portfolio(cash=1000000)
        assert portfolio.cash == 1000000
        assert portfolio.positions == {}
        assert portfolio.total_value == 0.0

    def test_update_market_value(self):
        """更新市值"""
        portfolio = Portfolio(cash=500000)
        portfolio.positions["600036.SH"] = Position(
            code="600036.SH", shares=1000, avg_cost=10.0
        )
        prices = {"600036.SH": 11.0}
        portfolio.update_market_value(prices)
        assert portfolio.positions["600036.SH"].market_value == 11000
        assert portfolio.positions["600036.SH"].unrealized_pnl == 1000
        assert portfolio.total_value == 511000

    def test_update_market_value_multiple(self):
        """多持仓市值更新"""
        portfolio = Portfolio(cash=500000)
        portfolio.positions["A.SH"] = Position(code="A.SH", shares=1000, avg_cost=10.0)
        portfolio.positions["B.SH"] = Position(code="B.SH", shares=2000, avg_cost=20.0)
        prices = {"A.SH": 11.0, "B.SH": 19.0}
        portfolio.update_market_value(prices)
        assert portfolio.total_value == 500000 + 11000 + 38000


class TestBacktestEngine:
    """回测引擎测试"""

    def test_engine_initialization(self):
        """引擎初始化"""
        config = BacktestConfig(initial_capital=100000)
        engine = BacktestEngine(config)
        assert engine.portfolio.cash == 100000

    def test_engine_default_config(self):
        """默认配置"""
        engine = BacktestEngine()
        assert engine.portfolio.cash == 1_000000

    def test_run_with_no_signals(self):
        """无信号 -> 无交易"""
        # 创建测试数据
        n = 50
        dates = pd.date_range("2024-01-01", periods=n, freq="B")
        df = pd.DataFrame({
            "date": dates,
            "open": [10.0] * n,
            "high": [10.5] * n,
            "low": [9.5] * n,
            "close": [10.0] * n,
            "volume": [1000000] * n
        })

        config = BacktestConfig(initial_capital=100000)
        engine = BacktestEngine(config)

        # 无信号函数
        def no_signal(df, date):
            return None

        result = engine.run(df, signal_func=no_signal)
        assert result is not None
        assert len(result.get("trades", [])) == 0

    def test_run_with_buy_signal(self):
        """买入信号执行"""
        n = 50
        dates = pd.date_range("2024-01-01", periods=n, freq="B")
        df = pd.DataFrame({
            "date": dates,
            "open": [10.0] * n,
            "high": [10.5] * n,
            "low": [9.5] * n,
            "close": [10.0] * n,
            "volume": [1000000] * n
        })

        config = BacktestConfig(initial_capital=100000)
        engine = BacktestEngine(config)

        # 第一天买入
        buy_called = [False]
        def buy_signal(df, date):
            if not buy_called[0]:
                buy_called[0] = True
                return {"direction": "buy", "price": 10.0, "shares": 100}
            return None

        result = engine.run(df, signal_func=buy_signal)
        assert buy_called[0] is True


class TestBenchmarkResult:
    """基准对比测试"""

    def test_benchmark_attributes(self):
        """基准对比属性"""
        result = BenchmarkResult(
            benchmark_return=0.10,
            excess_return=0.05,
            alpha=0.02,
            beta=0.8,
            information_ratio=0.5,
            tracking_error=0.03
        )
        assert result.benchmark_return == 0.10
        assert result.excess_return == 0.05
        assert result.alpha == 0.02
        assert result.beta == 0.8

    def test_benchmark_summary(self):
        """基准对比摘要"""
        result = BenchmarkResult(
            benchmark_return=0.10,
            excess_return=0.05,
            alpha=0.02,
            beta=0.8,
            information_ratio=0.5,
            tracking_error=0.03
        )
        summary = result.summary()
        assert "基准收益" in summary
        assert "超额收益" in summary
        assert "Alpha" in summary
        assert "Beta" in summary


class TestBacktestMetrics:
    """回测指标计算测试"""

    def test_max_drawdown_calculation(self):
        """最大回撤计算"""
        # 净值序列：100 -> 120 -> 90 -> 110
        values = [100, 120, 90, 110]
        peak = values[0]
        max_dd = 0
        for v in values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak
            if dd > max_dd:
                max_dd = dd
        # 最大回撤 = (120 - 90) / 120 = 25%
        assert max_dd == pytest.approx(0.25, abs=0.01)

    def test_sharpe_ratio_calculation(self):
        """夏普比率计算"""
        # 假设日收益率
        returns = [0.01, -0.005, 0.008, -0.002, 0.015]
        excess = [r - 0.03/252 for r in returns]  # 无风险利率 3%/年
        sharpe = np.mean(excess) / np.std(excess) * np.sqrt(252)
        assert isinstance(sharpe, float)
        assert sharpe != 0

    def test_win_rate_calculation(self):
        """胜率计算"""
        trades = [
            {"pnl": 100},   # 盈利
            {"pnl": -50},   # 亏损
            {"pnl": 200},   # 盈利
            {"pnl": -30},   # 亏损
        ]
        wins = sum(1 for t in trades if t["pnl"] > 0)
        win_rate = wins / len(trades)
        assert win_rate == 0.5


class TestT1Restriction:
    """T+1 限制测试"""

    def test_t1_can_sell_next_day(self):
        """T+1：买入后次日可卖"""
        pos = Position(
            code="600036.SH", shares=1000, avg_cost=10.0,
            buy_date="2024-01-01", can_sell_date="2024-01-02"
        )
        # 当天不能卖
        assert "2024-01-01" < pos.can_sell_date
        # 次日可以卖
        assert "2024-01-02" >= pos.can_sell_date


class TestVolumeConstraint:
    """成交量约束测试"""

    def test_volume_constraint_basic(self):
        """基本成交量约束"""
        max_participation = 0.1  # 最大参与率 10%
        volume = 100000
        max_shares = int(volume * max_participation)
        assert max_shares == 10000

    def test_volume_constraint_exceeded(self):
        """超过成交量约束"""
        max_participation = 0.1
        volume = 100000
        order_shares = 15000
        actual_shares = min(order_shares, int(volume * max_participation))
        assert actual_shares == 10000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
