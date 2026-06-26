"""专业回测引擎 - 复权/涨跌停/成交量约束/滑点模型/基准对比/T+1"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ===================== 交易成本模型 =====================

@dataclass
class CostModel:
    """交易成本模型"""
    commission_rate: float = 0.0003     # 佣金费率（双向）
    stamp_tax_rate: float = 0.001       # 印花税（卖出）
    min_commission: float = 5.0         # 最低佣金
    slippage_model: str = "percentage"  # fixed / percentage / volume
    slippage_value: float = 0.001       # 滑点值

    def buy_cost(self, price: float, shares: int, volume: float = 0) -> float:
        """买入成本"""
        amount = price * shares
        commission = max(amount * self.commission_rate, self.min_commission)
        slippage = self._calc_slippage(price, shares, volume)
        return amount + commission + slippage

    def sell_cost(self, price: float, shares: int, volume: float = 0) -> float:
        """卖出所得"""
        amount = price * shares
        commission = max(amount * self.commission_rate, self.min_commission)
        tax = amount * self.stamp_tax_rate
        slippage = self._calc_slippage(price, shares, volume)
        return amount - commission - tax - slippage

    def _calc_slippage(self, price: float, shares: int, volume: float) -> float:
        """计算滑点"""
        if self.slippage_model == "fixed":
            return self.slippage_value * shares
        elif self.slippage_model == "volume" and volume > 0:
            # 成交量冲击模型：参与率越高滑点越大
            participation = shares / volume
            impact = price * shares * participation * 0.1
            return impact
        else:
            return price * shares * self.slippage_value


# ===================== 复权处理 =====================

def adjust_prices(df: pd.DataFrame, adj_type: str = "qfq") -> pd.DataFrame:
    """复权处理

    Args:
        df: K线数据，需含 open/high/low/close/volume 和 adj_factor
        adj_type: qfq=前复权, hfq=后复权

    Returns:
        复权后的 DataFrame
    """
    df = df.copy()

    if "adj_factor" not in df.columns:
        # 没有复权因子，返回原数据
        return df

    factor = df["adj_factor"].astype(float)

    if adj_type == "qfq":
        # 前复权：最新价格不变
        latest_factor = factor.iloc[-1]
        adj_ratio = factor / latest_factor
    else:
        # 后复权：上市价格不变
        first_factor = factor.iloc[0]
        adj_ratio = factor / first_factor

    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df[col] = df[col].astype(float) * adj_ratio

    if "volume" in df.columns and adj_type == "hfq":
        df["volume"] = df["volume"].astype(float) / adj_ratio

    return df


# ===================== 涨跌停判断 =====================

def is_limit_up(close: float, prev_close: float, threshold: float = 0.095) -> bool:
    """判断是否涨停"""
    if prev_close <= 0:
        return False
    pct = (close - prev_close) / prev_close
    return pct >= threshold


def is_limit_down(close: float, prev_close: float, threshold: float = -0.095) -> bool:
    """判断是否跌停"""
    if prev_close <= 0:
        return False
    pct = (close - prev_close) / prev_close
    return pct <= threshold


def can_buy_at_limit(close: float, prev_close: float) -> bool:
    """涨停能否买入（简化：涨停封板不可买入）"""
    return not is_limit_up(close, prev_close, 0.095)


def can_sell_at_limit(close: float, prev_close: float) -> bool:
    """跌停能否卖出（简化：跌停封板不可卖出）"""
    return not is_limit_down(close, prev_close, -0.095)


# ===================== 订单类型 =====================

@dataclass
class Order:
    """订单"""
    code: str
    direction: str      # buy / sell
    price: float
    shares: int
    order_type: str = "market"  # market / limit
    status: str = "pending"     # pending / filled / rejected / cancelled
    fill_price: float = 0.0
    fill_shares: int = 0
    commission: float = 0.0
    slippage: float = 0.0
    reason: str = ""


@dataclass
class Position:
    """持仓"""
    code: str
    shares: int
    avg_cost: float
    market_value: float = 0.0
    unrealized_pnl: float = 0.0
    buy_date: str = ""
    can_sell_date: str = ""  # T+1 限制


@dataclass
class Portfolio:
    """投资组合"""
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)
    total_value: float = 0.0
    total_return: float = 0.0

    def update_market_value(self, prices: Dict[str, float]):
        """更新市值"""
        pos_value = 0
        for code, pos in self.positions.items():
            price = prices.get(code, pos.avg_cost)
            pos.market_value = price * pos.shares
            pos.unrealized_pnl = (price - pos.avg_cost) * pos.shares
            pos_value += pos.market_value
        self.total_value = self.cash + pos_value
        self.total_return = (self.total_value / (self.cash + pos_value)) - 1 if (self.cash + pos_value) > 0 else 0


# ===================== 基准对比 =====================

@dataclass
class BenchmarkResult:
    """基准对比结果"""
    benchmark_return: float
    excess_return: float
    alpha: float
    beta: float
    information_ratio: float
    tracking_error: float

    def summary(self) -> str:
        return (
            f"基准收益: {self.benchmark_return:+.2%} | "
            f"超额收益: {self.excess_return:+.2%} | "
            f"Alpha: {self.alpha:+.4f} | Beta: {self.beta:.2f} | "
            f"IR: {self.information_ratio:.2f} | 跟踪误差: {self.tracking_error:.2%}"
        )


# ===================== 回测引擎 =====================

@dataclass
class BacktestConfig:
    """回测配置"""
    initial_capital: float = 1_000_000
    max_single_position: float = 0.30
    max_total_position: float = 0.80
    cost_model: CostModel = field(default_factory=CostModel)
    enforce_t1: bool = True            # T+1 限制
    enforce_limit: bool = True          # 涨跌停限制
    enforce_volume: bool = True         # 成交量约束
    max_volume_participation: float = 0.1  # 最大成交量参与率
    adj_type: str = "qfq"              # 复权类型


@dataclass
class BacktestMetrics:
    """回测指标"""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    win_rate: float
    profit_factor: float
    avg_holding_days: float
    total_trades: int
    total_commission: float
    total_slippage: float
    benchmark: Optional[BenchmarkResult] = None

    def summary(self) -> str:
        lines = [
            f"总收益: {self.total_return:+.2%}",
            f"年化收益: {self.annual_return:+.2%}",
            f"最大回撤: {self.max_drawdown:.2%}",
            f"夏普比率: {self.sharpe_ratio:.2f}",
            f"索提诺比率: {self.sortino_ratio:.2f}",
            f"卡尔马比率: {self.calmar_ratio:.2f}",
            f"胜率: {self.win_rate:.0%}",
            f"盈亏比: {self.profit_factor:.2f}",
            f"平均持仓: {self.avg_holding_days:.1f}天",
            f"总交易: {self.total_trades}笔",
            f"总佣金: {self.total_commission:.0f}",
            f"总滑点: {self.total_slippage:.0f}",
        ]
        if self.benchmark:
            lines.append(self.benchmark.summary())
        return "\n".join(lines)


class BacktestEngine:
    """专业回测引擎"""

    def __init__(self, config: BacktestConfig | None = None):
        self.cfg = config or BacktestConfig()
        self.portfolio = Portfolio(cash=self.cfg.initial_capital)
        self.trades: List[Dict] = []
        self.daily_returns: List[float] = []
        self.daily_values: List[float] = []
        self.orders: List[Order] = []
        self._trade_dates: List[str] = []

    def run(
        self,
        stock_data: Dict[str, pd.DataFrame],
        signal_func,
        start_date: str | None = None,
        end_date: str | None = None,
        benchmark_data: pd.DataFrame | None = None,
    ) -> BacktestMetrics:
        """运行回测

        Args:
            stock_data: {code: DataFrame} 所有股票K线数据
            signal_func: 信号函数，签名 (code, df, portfolio, date) -> Optional[Order]
            start_date: 起始日期
            end_date: 结束日期
            benchmark_data: 基准K线数据
        """
        # 获取所有交易日
        all_dates = set()
        for df in stock_data.values():
            if "date" in df.columns:
                all_dates.update(df["date"].astype(str).tolist())
        trade_dates = sorted(all_dates)

        if start_date:
            trade_dates = [d for d in trade_dates if d >= start_date]
        if end_date:
            trade_dates = [d for d in trade_dates if d <= end_date]

        if not trade_dates:
            logger.warning("无交易日数据")
            return self._empty_metrics()

        self._trade_dates = trade_dates

        # 逐日回测
        prev_values = self.cfg.initial_capital

        for i, current_date in enumerate(trade_dates):
            # 1. 更新持仓市值
            prices = {}
            for code, df in stock_data.items():
                row = df[df["date"].astype(str) == current_date]
                if not row.empty:
                    prices[code] = float(row.iloc[0]["close"])
            self.portfolio.update_market_value(prices)

            # 2. 检查止损止盈（卖出信号）
            for code in list(self.portfolio.positions.keys()):
                pos = self.portfolio.positions[code]
                if not self._can_sell(code, current_date, trade_dates):
                    continue

                df = stock_data.get(code)
                if df is None:
                    continue

                sell_order = signal_func(code, df, self.portfolio, current_date, "sell")
                if sell_order and sell_order.direction == "sell":
                    self._execute_sell(sell_order, prices.get(code, 0), current_date)

            # 3. 生成买入信号
            for code, df in stock_data.items():
                if code in self.portfolio.positions:
                    continue

                buy_order = signal_func(code, df, self.portfolio, current_date, "buy")
                if buy_order and buy_order.direction == "buy":
                    self._execute_buy(buy_order, prices.get(buy_order.code, 0), current_date, df, current_date)

            # 4. 记录每日收益
            current_value = self.portfolio.total_value
            daily_ret = (current_value - prev_values) / prev_values if prev_values > 0 else 0
            self.daily_returns.append(daily_ret)
            self.daily_values.append(current_value)
            prev_values = current_value

        return self._calculate_metrics(benchmark_data, trade_dates)

    def _can_sell(self, code: str, current_date: str, trade_dates: list) -> bool:
        """检查是否可卖出（T+1）"""
        if not self.cfg.enforce_t1:
            return True
        pos = self.portfolio.positions.get(code)
        if pos and pos.can_sell_date:
            return current_date >= pos.can_sell_date
        return True

    def _execute_buy(self, order: Order, price: float, date: str, df: pd.DataFrame, current_date: str):
        """执行买入"""
        if self.cfg.enforce_limit:
            prev_rows = df[df["date"].astype(str) < date]
            if not prev_rows.empty:
                prev_close = float(prev_rows.iloc[-1]["close"])
                if not can_buy_at_limit(price, prev_close):
                    order.status = "rejected"
                    order.reason = "涨停封板无法买入"
                    return

        if self.cfg.enforce_volume:
            row = df[df["date"].astype(str) == date]
            if not row.empty:
                volume = float(row.iloc[0].get("volume", 0))
                max_shares = int(volume * self.cfg.max_volume_participation)
                if order.shares > max_shares:
                    order.shares = max_shares

        cost = self.cfg.cost_model.buy_cost(price, order.shares)
        if cost > self.portfolio.cash:
            order.status = "rejected"
            order.reason = "资金不足"
            return

        order.fill_price = price
        order.fill_shares = order.shares
        order.status = "filled"

        self.portfolio.cash -= cost

        if order.code in self.portfolio.positions:
            pos = self.portfolio.positions[order.code]
            total_shares = pos.shares + order.shares
            pos.avg_cost = (pos.avg_cost * pos.shares + price * order.shares) / total_shares
            pos.shares = total_shares
        else:
            can_sell = ""
            if self._trade_dates and date in self._trade_dates:
                idx = self._trade_dates.index(date)
                if idx + 1 < len(self._trade_dates):
                    can_sell = self._trade_dates[idx + 1]
            self.portfolio.positions[order.code] = Position(
                code=order.code,
                shares=order.shares,
                avg_cost=price,
                buy_date=date,
                can_sell_date=can_sell,
            )

        self.trades.append({
            "date": date, "code": order.code, "direction": "buy",
            "price": price, "shares": order.shares, "cost": cost,
        })

    def _execute_sell(self, order: Order, price: float, date: str):
        """执行卖出"""
        pos = self.portfolio.positions.get(order.code)
        if not pos or pos.shares <= 0:
            order.status = "rejected"
            order.reason = "无持仓"
            return

        sell_shares = min(order.shares, pos.shares)
        proceeds = self.cfg.cost_model.sell_cost(price, sell_shares)

        order.fill_price = price
        order.fill_shares = sell_shares
        order.status = "filled"

        self.portfolio.cash += proceeds
        pos.shares -= sell_shares

        if pos.shares <= 0:
            del self.portfolio.positions[order.code]

        self.trades.append({
            "date": date, "code": order.code, "direction": "sell",
            "price": price, "shares": sell_shares, "proceeds": proceeds,
        })

    def _calculate_metrics(
        self,
        benchmark_data: pd.DataFrame | None,
        trade_dates: list,
    ) -> BacktestMetrics:
        """计算回测指标"""
        if not self.daily_returns:
            return self._empty_metrics()

        returns = np.array(self.daily_returns)
        values = np.array(self.daily_values)

        # 总收益
        total_return = (values[-1] - values[0]) / values[0] if values[0] > 0 else 0

        # 年化收益
        n_days = len(returns)
        annual_return = (1 + total_return) ** (252 / max(n_days, 1)) - 1

        # 最大回撤
        peak = np.maximum.accumulate(values)
        drawdown = (peak - values) / peak
        max_drawdown = float(np.max(drawdown))

        # 夏普比率
        rf = 0.03 / 252  # 无风险利率
        excess = returns - rf
        sharpe = float(np.mean(excess) / np.std(excess) * np.sqrt(252)) if np.std(excess) > 0 else 0

        # 索提诺比率
        downside = returns[returns < 0]
        downside_std = float(np.std(downside)) if len(downside) > 0 else 1
        sortino = float((np.mean(returns) - rf) * np.sqrt(252) / downside_std) if downside_std > 0 else 0

        # 卡尔马比率
        calmar = annual_return / max_drawdown if max_drawdown > 0 else 0

        # 胜率和盈亏比
        wins = [t for t in self.trades if t["direction"] == "sell" and t.get("proceeds", 0) > 0]
        total_sells = [t for t in self.trades if t["direction"] == "sell"]
        win_rate = len(wins) / len(total_sells) if total_sells else 0

        buy_trades = [t for t in self.trades if t["direction"] == "buy"]
        sell_trades = [t for t in self.trades if t["direction"] == "sell"]
        total_commission = sum(t.get("cost", 0) for t in buy_trades) + sum(t.get("proceeds", 0) for t in sell_trades)

        # 基准对比
        benchmark_result = None
        if benchmark_data is not None and not benchmark_data.empty:
            benchmark_result = self._calc_benchmark(benchmark_data, returns, trade_dates)

        return BacktestMetrics(
            total_return=total_return,
            annual_return=annual_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            calmar_ratio=calmar,
            win_rate=win_rate,
            profit_factor=0,
            avg_holding_days=0,
            total_trades=len(self.trades),
            total_commission=total_commission,
            total_slippage=0,
            benchmark=benchmark_result,
        )

    def _calc_benchmark(
        self,
        benchmark_data: pd.DataFrame,
        returns: np.ndarray,
        trade_dates: list,
    ) -> BenchmarkResult:
        """计算基准对比"""
        bm_close = benchmark_data["close"].astype(float).values
        bm_returns = np.diff(bm_close) / bm_close[:-1]

        min_len = min(len(returns), len(bm_returns))
        port_ret = returns[:min_len]
        bm_ret = bm_returns[:min_len]

        bm_total = float((bm_close[-1] - bm_close[0]) / bm_close[0])
        excess = float(np.sum(port_ret) - np.sum(bm_ret))

        # Alpha / Beta
        if len(port_ret) > 2:
            cov = np.cov(port_ret, bm_ret)
            beta = float(cov[0, 1] / cov[1, 1]) if cov[1, 1] > 0 else 1
            alpha = float(np.mean(port_ret) - beta * np.mean(bm_ret)) * 252
        else:
            alpha, beta = 0, 1

        # 信息比率
        tracking_diff = port_ret - bm_ret
        tracking_error = float(np.std(tracking_diff) * np.sqrt(252))
        ir = float(np.mean(tracking_diff) * 252 / tracking_error) if tracking_error > 0 else 0

        return BenchmarkResult(
            benchmark_return=bm_total,
            excess_return=excess,
            alpha=alpha,
            beta=beta,
            information_ratio=ir,
            tracking_error=tracking_error,
        )

    def _empty_metrics(self) -> BacktestMetrics:
        return BacktestMetrics(
            total_return=0, annual_return=0, max_drawdown=0,
            sharpe_ratio=0, sortino_ratio=0, calmar_ratio=0,
            win_rate=0, profit_factor=0, avg_holding_days=0,
            total_trades=0, total_commission=0, total_slippage=0,
        )


# ===================== 滚动窗口回测 =====================

@dataclass
class RollingWindowResult:
    """单个窗口的回测结果"""
    window_id: int
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    best_params: Dict
    train_score: float
    test_metrics: BacktestMetrics

    def summary(self) -> str:
        return (
            f"窗口{self.window_id}: "
            f"训练[{self.train_start}~{self.train_end}] "
            f"测试[{self.test_start}~{self.test_end}] "
            f"夏普={self.test_metrics.sharpe_ratio:.2f} "
            f"胜率={self.test_metrics.win_rate:.0%} "
            f"回撤={self.test_metrics.max_drawdown:.2%}"
        )


@dataclass
class RollingBacktestResult:
    """滚动窗口回测汇总结果"""
    windows: List[RollingWindowResult]
    avg_sharpe: float
    avg_win_rate: float
    avg_return: float
    avg_max_drawdown: float
    sharpe_std: float
    win_rate_std: float
    drawdown_std: float
    best_window: Optional[RollingWindowResult] = None
    worst_window: Optional[RollingWindowResult] = None

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "滚动窗口回测结果",
            "=" * 60,
            f"窗口数量: {len(self.windows)}",
            "",
            "【绩效统计】",
            f"  平均夏普比率: {self.avg_sharpe:.2f} ± {self.sharpe_std:.2f}",
            f"  平均胜率: {self.avg_win_rate:.0%} ± {self.win_rate_std:.0%}",
            f"  平均收益: {self.avg_return:+.2%}",
            f"  平均最大回撤: {self.avg_max_drawdown:.2%} ± {self.drawdown_std:.2%}",
            "",
        ]

        if self.best_window:
            lines.append("【最佳窗口】")
            lines.append(f"  {self.best_window.summary()}")
            lines.append("")

        if self.worst_window:
            lines.append("【最差窗口】")
            lines.append(f"  {self.worst_window.summary()}")
            lines.append("")

        lines.append("【各窗口详情】")
        for w in self.windows:
            lines.append(f"  {w.summary()}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            "window_count": len(self.windows),
            "avg_sharpe": round(self.avg_sharpe, 4),
            "avg_win_rate": round(self.avg_win_rate, 4),
            "avg_return": round(self.avg_return, 4),
            "avg_max_drawdown": round(self.avg_max_drawdown, 4),
            "sharpe_std": round(self.sharpe_std, 4),
            "win_rate_std": round(self.win_rate_std, 4),
            "drawdown_std": round(self.drawdown_std, 4),
            "windows": [
                {
                    "id": w.window_id,
                    "train": f"{w.train_start}~{w.train_end}",
                    "test": f"{w.test_start}~{w.test_end}",
                    "sharpe": round(w.test_metrics.sharpe_ratio, 4),
                    "win_rate": round(w.test_metrics.win_rate, 4),
                    "return": round(w.test_metrics.total_return, 4),
                    "max_drawdown": round(w.test_metrics.max_drawdown, 4),
                }
                for w in self.windows
            ],
        }


class RollingBacktestEngine:
    """滚动窗口回测引擎

    实现 Walk-Forward 分析：
    1. 在训练窗口内优化策略参数
    2. 在测试窗口内验证策略表现
    3. 滚动推进，记录所有窗口的绩效

    Args:
        window_size_days: 训练窗口大小（交易日）
        step_days: 每次滚动步长（交易日）
        config: 回测配置
    """

    def __init__(
        self,
        window_size_days: int = 252,
        step_days: int = 21,
        config: BacktestConfig | None = None,
    ):
        self.window_size = window_size_days
        self.step_days = step_days
        self.cfg = config or BacktestConfig()

    def run(
        self,
        stock_data: Dict[str, pd.DataFrame],
        signal_func=None,
        param_optimizer=None,
        start_date: str | None = None,
        end_date: str | None = None,
        benchmark_data: pd.DataFrame | None = None,
    ) -> RollingBacktestResult:
        """运行滚动窗口回测

        Args:
            stock_data: {code: DataFrame} 股票K线数据
            signal_func: 信号函数，签名 (code, df, portfolio, date, side) -> Optional[Order]
            param_optimizer: 参数优化器，签名 (train_data) -> Dict[str, Any]
            start_date: 起始日期
            end_date: 结束日期
            benchmark_data: 基准K线数据

        Returns:
            RollingBacktestResult 汇总结果
        """
        # 获取所有交易日
        all_dates = set()
        for df in stock_data.values():
            if "date" in df.columns:
                all_dates.update(df["date"].astype(str).tolist())
        trade_dates = sorted(all_dates)

        if start_date:
            trade_dates = [d for d in trade_dates if d >= start_date]
        if end_date:
            trade_dates = [d for d in trade_dates if d <= end_date]

        if len(trade_dates) < self.window_size + self.step_days:
            logger.warning(f"数据不足：需要至少 {self.window_size + self.step_days} 个交易日")
            return self._empty_result()

        # 划分窗口
        windows = []
        window_id = 0
        i = 0

        while i + self.window_size + self.step_days <= len(trade_dates):
            train_start = trade_dates[i]
            train_end = trade_dates[i + self.window_size - 1]
            test_start = trade_dates[i + self.window_size]
            test_end_idx = min(i + self.window_size + self.step_days - 1, len(trade_dates) - 1)
            test_end = trade_dates[test_end_idx]

            windows.append({
                "id": window_id,
                "train_start": train_start,
                "train_end": train_end,
                "test_start": test_start,
                "test_end": test_end,
            })

            window_id += 1
            i += self.step_days

        logger.info(f"共 {len(windows)} 个滚动窗口，窗口大小={self.window_size}，步长={self.step_days}")

        # 逐窗口回测
        results = []

        for window in windows:
            logger.info(f"处理窗口 {window['id']}: 训练[{window['train_start']}~{window['train_end']}] "
                       f"测试[{window['test_start']}~{window['test_end']}]")

            # 1. 训练期：优化参数
            best_params = {}
            train_score = 0.0

            if param_optimizer:
                train_data = self._slice_data(stock_data, window["train_start"], window["train_end"])
                try:
                    best_params, train_score = param_optimizer(train_data)
                    logger.debug(f"  优化结果: params={best_params}, score={train_score:.4f}")
                except Exception as e:
                    logger.warning(f"  参数优化失败: {e}")

            # 2. 测试期：验证策略
            test_data = self._slice_data(stock_data, window["test_start"], window["test_end"])

            engine = BacktestEngine(self.cfg)
            test_metrics = engine.run(
                stock_data=test_data,
                signal_func=signal_func,
                start_date=window["test_start"],
                end_date=window["test_end"],
                benchmark_data=benchmark_data,
            )

            result = RollingWindowResult(
                window_id=window["id"],
                train_start=window["train_start"],
                train_end=window["train_end"],
                test_start=window["test_start"],
                test_end=window["test_end"],
                best_params=best_params,
                train_score=train_score,
                test_metrics=test_metrics,
            )

            results.append(result)
            logger.info(f"  {result.summary()}")

        # 3. 汇总统计
        return self._aggregate_results(results)

    def _slice_data(
        self,
        stock_data: Dict[str, pd.DataFrame],
        start_date: str,
        end_date: str,
    ) -> Dict[str, pd.DataFrame]:
        """切片数据"""
        sliced = {}
        for code, df in stock_data.items():
            if "date" not in df.columns:
                continue
            mask = (df["date"].astype(str) >= start_date) & (df["date"].astype(str) <= end_date)
            sliced_df = df[mask].reset_index(drop=True)
            if not sliced_df.empty:
                sliced[code] = sliced_df
        return sliced

    def _aggregate_results(
        self,
        results: List[RollingWindowResult],
    ) -> RollingBacktestResult:
        """汇总窗口结果"""
        if not results:
            return self._empty_result()

        sharpes = [r.test_metrics.sharpe_ratio for r in results]
        win_rates = [r.test_metrics.win_rate for r in results]
        returns = [r.test_metrics.total_return for r in results]
        drawdowns = [r.test_metrics.max_drawdown for r in results]

        avg_sharpe = float(np.mean(sharpes))
        avg_win_rate = float(np.mean(win_rates))
        avg_return = float(np.mean(returns))
        avg_max_drawdown = float(np.mean(drawdowns))

        sharpe_std = float(np.std(sharpes))
        win_rate_std = float(np.std(win_rates))
        drawdown_std = float(np.std(drawdowns))

        best_window = max(results, key=lambda r: r.test_metrics.sharpe_ratio)
        worst_window = min(results, key=lambda r: r.test_metrics.sharpe_ratio)

        return RollingBacktestResult(
            windows=results,
            avg_sharpe=avg_sharpe,
            avg_win_rate=avg_win_rate,
            avg_return=avg_return,
            avg_max_drawdown=avg_max_drawdown,
            sharpe_std=sharpe_std,
            win_rate_std=win_rate_std,
            drawdown_std=drawdown_std,
            best_window=best_window,
            worst_window=worst_window,
        )

    def _empty_result(self) -> RollingBacktestResult:
        return RollingBacktestResult(
            windows=[],
            avg_sharpe=0,
            avg_win_rate=0,
            avg_return=0,
            avg_max_drawdown=0,
            sharpe_std=0,
            win_rate_std=0,
            drawdown_std=0,
        )
