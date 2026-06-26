"""Backtrader 回测引擎 - 专业级回测框架集成"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

import backtrader as bt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ===================== 数据适配器 =====================

class BeerGaaoDataFeed(bt.feeds.PandasData):
    """将 BeerGaao 的 K 线数据适配为 Backtrader 可消费的格式"""

    params = (
        ('datetime', None),  # 若 DataFrame 有 datetime 索引则自动识别
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None),
    )

    # 支持的列名映射
    datafields = [
        'datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest'
    ]


# ===================== 策略适配器 =====================

class StrategyAdapter(bt.Strategy):
    """将 BeerGaao 原策略引擎生成的信号适配为 Backtrader 策略"""

    params = (
        ('signal_func', None),  # 信号函数
        ('risk_manager', None),  # 风控管理器
        ('stop_loss_pct', 0.04),  # 止损百分比
        ('take_profit_pct', 0.06),  # 止盈百分比
        ('max_position_pct', 0.3),  # 最大仓位比例
    )

    def __init__(self):
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.signal_history = []

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
                logger.debug(f"买入成交: 价格={order.executed.price}, 数量={order.executed.size}")
            else:
                logger.debug(f"卖出成交: 价格={order.executed.price}, 数量={order.executed.size}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.warning(f"订单被拒绝/取消: {order.status}")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        logger.debug(f"交易利润: 毛利={trade.pnl:.2f}, 净利={trade.pnlcomm:.2f}")

    def next(self):
        if self.order:
            return

        if not self.position:
            # 无持仓，检查买入信号
            if self.p.signal_func:
                signal = self.p.signal_func(self.data)
                if signal and signal.get('action') == 'BUY':
                    # 计算仓位
                    size = self._calculate_position_size()
                    if size > 0:
                        self.order = self.buy(size=size)
        else:
            # 有持仓，检查止损止盈
            current_price = self.data.close[0]
            if self.buy_price:
                pnl_pct = (current_price - self.buy_price) / self.buy_price

                # 止损
                if pnl_pct <= -self.p.stop_loss_pct:
                    self.order = self.sell(size=self.position.size)
                    logger.debug(f"触发止损: 亏损 {pnl_pct:.2%}")

                # 止盈
                elif pnl_pct >= self.p.take_profit_pct:
                    self.order = self.sell(size=self.position.size)
                    logger.debug(f"触发止盈: 盈利 {pnl_pct:.2%}")

                # 卖出信号
                elif self.p.signal_func:
                    signal = self.p.signal_func(self.data)
                    if signal and signal.get('action') == 'SELL':
                        self.order = self.sell(size=self.position.size)

    def _calculate_position_size(self) -> int:
        """计算仓位大小"""
        cash = self.broker.getcash()
        total_value = self.broker.getvalue()
        max_position_value = total_value * self.p.max_position_pct
        current_price = self.data.close[0]

        if current_price <= 0:
            return 0

        # 计算可买数量（100 股整数倍）
        max_shares = int(min(cash, max_position_value) / current_price)
        max_shares = (max_shares // 100) * 100

        return max_shares


# ===================== 分析器 =====================

class BeerGaaoAnalyzer(bt.Analyzer):
    """BeerGaao 标准分析器"""

    def __init__(self):
        self.trades = []
        self.portfolio_values = []

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades.append({
                'pnl': trade.pnl,
                'pnlcomm': trade.pnlcomm,
                'size': trade.size,
                'price': trade.price,
                'value': trade.value,
            })

    def next(self):
        self.portfolio_values.append(self.strategy.broker.getvalue())

    def get_analysis(self):
        return {
            'trades': self.trades,
            'portfolio_values': self.portfolio_values,
        }


# ===================== 回测引擎封装 =====================

@dataclass
class BacktraderConfig:
    """Backtrader 回测配置"""
    initial_capital: float = 1_000_000
    commission: float = 0.0003
    slippage_perc: float = 0.001
    stop_loss_pct: float = 0.04
    take_profit_pct: float = 0.06
    max_position_pct: float = 0.30


class BacktraderBacktest:
    """Backtrader 回测引擎封装，与现有回测引擎 API 对齐"""

    def __init__(self, config: Optional[BacktraderConfig] = None):
        self.config = config or BacktraderConfig()
        self.cerebro = bt.Cerebro()
        self._configure_broker()
        self._data_loaded = False

    def _configure_broker(self):
        """配置经纪商参数"""
        self.cerebro.broker.setcash(self.config.initial_capital)
        self.cerebro.broker.setcommission(commission=self.config.commission)

        # 设置滑点
        self.cerebro.broker.set_slippage_perc(self.config.slippage_perc)

    def load_data(self, df: pd.DataFrame, name: str = 'stock') -> None:
        """加载数据，df 需包含 open/high/low/close/volume 列

        Args:
            df: DataFrame with columns [open, high, low, close, volume]
            name: 数据名称
        """
        if df.empty:
            raise ValueError("数据为空")

        # 确保有 datetime 索引
        if 'date' in df.columns:
            df = df.copy()
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

        # 确保列名正确
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"缺少必需列: {col}")

        data = BeerGaaoDataFeed(dataname=df, name=name)
        self.cerebro.adddata(data)
        self._data_loaded = True

    def add_strategy(self, strategy_class: Type[bt.Strategy], **kwargs) -> None:
        """添加策略"""
        self.cerebro.addstrategy(strategy_class, **kwargs)

    def add_signal_strategy(self, signal_func, **kwargs) -> None:
        """添加信号驱动策略

        Args:
            signal_func: 信号函数，接收 data 参数，返回 {'action': 'BUY'/'SELL', ...}
        """
        self.cerebro.addstrategy(
            StrategyAdapter,
            signal_func=signal_func,
            stop_loss_pct=self.config.stop_loss_pct,
            take_profit_pct=self.config.take_profit_pct,
            max_position_pct=self.config.max_position_pct,
            **kwargs
        )

    def add_default_analyzers(self) -> None:
        """添加默认分析器"""
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe',
                                timeframe=bt.TimeFrame.Days, compression=1)
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(BeerGaaoAnalyzer, _name='beergaao')

    def add_analyzer(self, analyzer_class: Type[bt.Analyzer], **kwargs) -> None:
        """添加分析器"""
        self.cerebro.addanalyzer(analyzer_class, **kwargs)

    def run(self) -> Dict[str, Any]:
        """运行回测，返回标准化结果

        Returns:
            Dict with keys: total_return, annual_return, max_drawdown, sharpe_ratio,
                          win_rate, profit_factor, trades, portfolio_values
        """
        if not self._data_loaded:
            raise RuntimeError("请先加载数据")

        # 运行回测
        results = self.cerebro.run()
        strategy = results[0]

        # 提取分析器结果
        return self._extract_results(strategy)

    def _extract_results(self, strategy) -> Dict[str, Any]:
        """提取分析器结果并转换为 BeerGaao 标准格式"""
        final_value = self.cerebro.broker.getvalue()
        initial_value = self.config.initial_capital
        total_return = (final_value - initial_value) / initial_value

        # 交易统计
        trades_analysis = strategy.analyzers.trades.get_analysis()
        total_trades = trades_analysis.get('total', {}).get('total', 0)
        won_trades = trades_analysis.get('won', {}).get('total', 0)
        lost_trades = trades_analysis.get('lost', {}).get('total', 0)

        # 胜率
        win_rate = won_trades / total_trades if total_trades > 0 else 0

        # 盈亏比
        avg_won = trades_analysis.get('won', {}).get('pnl', {}).get('average', 0)
        avg_lost = abs(trades_analysis.get('lost', {}).get('pnl', {}).get('average', 1))
        profit_factor = avg_won / avg_lost if avg_lost > 0 else 0

        # 夏普比率
        sharpe_analysis = strategy.analyzers.sharpe.get_analysis()
        sharpe_ratio = sharpe_analysis.get('sharperatio', 0) or 0

        # 最大回撤
        drawdown_analysis = strategy.analyzers.drawdown.get_analysis()
        max_drawdown = drawdown_analysis.get('max', {}).get('drawdown', 0) / 100

        # 年化收益
        returns_analysis = strategy.analyzers.returns.get_analysis()
        annual_return = returns_analysis.get('rnorm100', 0) / 100

        # BeerGaao 分析器数据
        beergaao_analysis = strategy.analyzers.beergaao.get_analysis()

        return {
            'initial_capital': initial_value,
            'final_capital': final_value,
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_trades': total_trades,
            'won_trades': won_trades,
            'lost_trades': lost_trades,
            'trades': beergaao_analysis.get('trades', []),
            'portfolio_values': beergaao_analysis.get('portfolio_values', []),
        }

    def plot(self, **kwargs) -> None:
        """绘制回测结果图表"""
        try:
            self.cerebro.plot(**kwargs)
        except Exception as e:
            logger.warning(f"绘图失败: {e}")


# ===================== 便捷函数 =====================

def run_backtest(
    df: pd.DataFrame,
    strategy_class: Optional[Type[bt.Strategy]] = None,
    signal_func=None,
    config: Optional[BacktraderConfig] = None,
    plot: bool = False,
) -> Dict[str, Any]:
    """便捷回测函数

    Args:
        df: K线数据
        strategy_class: Backtrader 策略类
        signal_func: 信号函数（与 strategy_class 二选一）
        config: 回测配置
        plot: 是否绘图

    Returns:
        回测结果字典
    """
    engine = BacktraderBacktest(config)
    engine.load_data(df)

    if strategy_class:
        engine.add_strategy(strategy_class)
    elif signal_func:
        engine.add_signal_strategy(signal_func)
    else:
        raise ValueError("必须提供 strategy_class 或 signal_func")

    engine.add_default_analyzers()
    results = engine.run()

    if plot:
        engine.plot()

    return results
