"""简版回测引擎 + 风险评估 - 支持网格/均线/布林带策略

用法:
    from scripts.backtest import run_backtest, assess_risk
    result = run_backtest(df, strategy="grid", initial_capital=100000)
    print(result.summary())

    risk = assess_risk(df["close"])
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List


@dataclass
class Trade:
    date: str
    action: str  # "buy" / "sell"
    price: float
    shares: float
    amount: float
    reason: str = ""


@dataclass
class BacktestResult:
    initial_capital: float
    final_value: float
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    annual_volatility: float
    trades: List[Trade] = field(default_factory=list)
    equity_curve: pd.Series = field(default_factory=pd.Series)

    def summary(self) -> str:
        lines = [
            "=" * 40,
            "          回测结果摘要",
            "=" * 40,
            f"  初始资金:     ¥{self.initial_capital:>12,.0f}",
            f"  最终权益:     ¥{self.final_value:>12,.0f}",
            f"  总收益率:     {self.total_return:>11.2%}",
            f"  最大回撤:     {self.max_drawdown:>11.2%}",
            f"  夏普比率:     {self.sharpe_ratio:>11.2f}",
            f"  年化波动率:   {self.annual_volatility:>11.2%}",
            f"  交易次数:     {len(self.trades):>11d}",
            "=" * 40,
        ]
        return "\n".join(lines)


def _calc_sharpe(returns: pd.Series, risk_free: float = 0.02) -> float:
    """计算年化夏普比率"""
    if len(returns) < 2 or returns.std() == 0:
        return 0.0
    excess = returns - risk_free / 252
    return np.sqrt(252) * excess.mean() / returns.std()


def _calc_max_drawdown(equity: pd.Series) -> float:
    """计算最大回撤"""
    peak = equity.expanding().max()
    dd = (equity - peak) / peak
    return abs(dd.min())


# --- 策略实现 ---

def _grid_signals(df: pd.DataFrame, grid_num: int = 10) -> pd.Series:
    """网格策略信号"""
    price_range = df["high"].max() - df["low"].min()
    if price_range == 0:
        return pd.Series(0, index=df.index)
    grid_size = price_range / grid_num
    base = df["low"].min()
    signals = pd.Series(0, index=df.index)

    for i in range(1, len(df)):
        level = (df["close"].iloc[i] - base) / grid_size
        prev_level = (df["close"].iloc[i - 1] - base) / grid_size
        # 跌破网格线 → 买入
        if int(level) < int(prev_level) and level > 0:
            signals.iloc[i] = 1
        # 涨破网格线 → 卖出
        elif int(level) > int(prev_level):
            signals.iloc[i] = -1
    return signals


def _ma_cross_signals(df: pd.DataFrame, short: int = 5, long: int = 20) -> pd.Series:
    """均线交叉策略信号"""
    ma_s = df["close"].rolling(short).mean()
    ma_l = df["close"].rolling(long).mean()
    signals = pd.Series(0, index=df.index)
    # 金叉买入
    signals[(ma_s > ma_l) & (ma_s.shift(1) <= ma_l.shift(1))] = 1
    # 死叉卖出
    signals[(ma_s < ma_l) & (ma_s.shift(1) >= ma_l.shift(1))] = -1
    return signals


def _bollinger_signals(df: pd.DataFrame, period: int = 20, num_std: float = 2.0) -> pd.Series:
    """布林带回归策略信号"""
    from scripts.technical_indicators import calc_bollinger
    upper, mid, lower = calc_bollinger(df["close"], period, num_std)
    signals = pd.Series(0, index=df.index)
    signals[df["close"] <= lower] = 1
    signals[df["close"] >= upper] = -1
    return signals


def run_backtest(
    df: pd.DataFrame,
    strategy: str = "grid",
    initial_capital: float = 100000,
    stop_loss: float = 0.05,
    take_profit: float = 0.10,
    **kwargs,
) -> BacktestResult:
    """运行回测。

    Args:
        df: 包含 date/open/high/low/close/volume 的日线数据
        strategy: "grid" / "ma_cross" / "bollinger"
        initial_capital: 初始资金
        stop_loss: 止损比例（0.05 = 5%）
        take_profit: 止盈比例（0.10 = 10%）
        **kwargs: 策略参数 grid_num, ma_short, ma_long, etc.
    """
    if "date" not in df.columns:
        df = df.reset_index()
        if "date" not in df.columns:
            df["date"] = pd.RangeIndex(len(df))

    # 生成信号
    if strategy == "grid":
        signals = _grid_signals(df, grid_num=kwargs.get("grid_num", 10))
    elif strategy == "ma_cross":
        signals = _ma_cross_signals(df, short=kwargs.get("ma_short", 5), long=kwargs.get("ma_long", 20))
    elif strategy == "bollinger":
        signals = _bollinger_signals(df)
    else:
        raise ValueError(f"未知策略: {strategy}")

    # 模拟交易
    cash = initial_capital
    shares = 0.0
    trades = []
    cost_price = 0.0
    equity_list = []

    for i in range(len(df)):
        price = df["close"].iloc[i]
        date = str(df["date"].iloc[i])[:10]
        signal = signals.iloc[i]

        # 止损/止盈检查
        if shares > 0 and cost_price > 0:
            pnl_pct = (price - cost_price) / cost_price
            if pnl_pct <= -stop_loss:
                amount = shares * price
                cash += amount
                trades.append(Trade(date, "sell", price, shares, amount, "止损"))
                shares = 0.0
                cost_price = 0.0
            elif pnl_pct >= take_profit:
                amount = shares * price
                cash += amount
                trades.append(Trade(date, "sell", price, shares, amount, "止盈"))
                shares = 0.0
                cost_price = 0.0

        # 执行信号
        if signal == 1 and shares == 0:
            buy_amount = cash * 0.9  # 用90%现金买入
            buy_shares = buy_amount / price
            cash -= buy_shares * price
            shares = buy_shares
            cost_price = price
            trades.append(Trade(date, "buy", price, buy_shares, buy_shares * price, "信号买入"))

        elif signal == -1 and shares > 0:
            sell_amount = shares * price
            cash += sell_amount
            trades.append(Trade(date, "sell", price, shares, sell_amount, "信号卖出"))
            shares = 0.0
            cost_price = 0.0

        equity = cash + shares * price
        equity_list.append(equity)

    equity_curve = pd.Series(equity_list, index=df.index if "date" not in df.columns else range(len(df)))
    final_value = cash + shares * df["close"].iloc[-1]
    total_return = (final_value - initial_capital) / initial_capital

    returns = equity_curve.pct_change().dropna()
    sharpe = _calc_sharpe(returns)
    max_dd = _calc_max_drawdown(equity_curve)
    annual_vol = returns.std() * np.sqrt(252) if len(returns) > 0 else 0.0

    return BacktestResult(
        initial_capital=initial_capital,
        final_value=final_value,
        total_return=total_return,
        max_drawdown=max_dd,
        sharpe_ratio=sharpe,
        annual_volatility=annual_vol,
        trades=trades,
        equity_curve=equity_curve,
    )


def assess_risk(prices: pd.Series, risk_free: float = 0.02) -> dict:
    """风险评估（无需回测，直接用价格序列计算）。

    Returns:
        dict: max_drawdown, sharpe_ratio, annual_volatility, calmar_ratio,
              annual_return, max_consecutive_loss_days
    """
    returns = prices.pct_change().dropna()
    equity = prices  # 假设持有1份

    max_dd = _calc_max_drawdown(equity)
    sharpe = _calc_sharpe(returns, risk_free)
    annual_vol = returns.std() * np.sqrt(252) if len(returns) > 0 else 0.0

    # 年化收益
    n_days = len(prices)
    total_ret = prices.iloc[-1] / prices.iloc[0] - 1 if prices.iloc[0] > 0 else 0
    annual_ret = (1 + total_ret) ** (252 / n_days) - 1 if n_days > 0 else 0

    # Calmar比率
    calmar = annual_ret / max_dd if max_dd > 0 else 0

    # 最大连续下跌天数
    neg_returns = (returns < 0).astype(int)
    max_consec = 0
    current = 0
    for v in neg_returns:
        if v == 1:
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 0

    return {
        "max_drawdown": round(max_dd, 4),
        "sharpe_ratio": round(sharpe, 2),
        "annual_volatility": round(annual_vol, 4),
        "calmar_ratio": round(calmar, 2),
        "annual_return": round(annual_ret, 4),
        "max_consecutive_loss_days": max_consec,
    }


if __name__ == "__main__":
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else "159915"
    strategy = sys.argv[2] if len(sys.argv) > 2 else "grid"

    from scripts.fetch_data import fetch_etf_daily
    df = fetch_etf_daily(code, "20250101", "20260301")
    if df.empty:
        print("无数据"); sys.exit(1)

    result = run_backtest(df, strategy=strategy)
    print(result.summary())
    print(f"\n最近5笔交易:")
    for t in result.trades[-5:]:
        print(f"  {t.date} {t.action:>4s} @ ¥{t.price:.3f} × {t.shares:.0f} ({t.reason})")
