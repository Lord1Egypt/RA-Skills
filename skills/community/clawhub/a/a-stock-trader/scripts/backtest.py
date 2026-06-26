#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略回测脚本 / Strategy Backtest Script

功能 / Function:
    - 均线策略回测 / MA strategy backtest
    - 动量策略回测 / Momentum strategy backtest
    - 收益计算 / Return calculation
    - 交易记录 / Trade recording
"""

import sqlite3
import os
import pandas as pd

# 数据库路径 / Database path
DB_PATH = os.path.expanduser("~/.openclaw/workspace/a-stock/data.db")

def load_data(code):
    """
    加载股票数据 / Load stock data
    从数据库读取历史K线 / Read historical K-line from database
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        f"SELECT * FROM daily_data WHERE code='{code}' ORDER BY date",
        conn
    )
    conn.close()
    return df

def ma_strategy(df, ma_short=5, ma_long=20):
    """
    均线策略 / Moving Average Strategy
    短期均线上穿长期均线买入 / Buy when short MA crosses above long MA
    短期均线下穿长期均线卖出 / Sell when short MA crosses below long MA
    
    参数 / Parameters:
        df: 数据框 (dataframe)
        ma_short: 短期均线周期 (short MA period)
        ma_long: 长期均线周期 (long MA period)
    """
    df = df.copy()
    df["ma_short"] = df["close"].rolling(ma_short).mean()
    df["ma_long"] = df["close"].rolling(ma_long).mean()
    
    # 信号 / Signals
    df["signal"] = 0
    df.loc[df["ma_short"] > df["ma_long"], "signal"] = 1  # 金叉 / Golden cross
    df.loc[df["ma_short"] <= df["ma_long"], "signal"] = -1  # 死叉 / Death cross
    
    return df

def momentum_strategy(df, threshold=0.05):
    """
    动量策略 / Momentum Strategy
    涨跌幅超过阈值买入/卖出 / Buy/sell when price change exceeds threshold
    
    参数 / Parameters:
        df: 数据框 (dataframe)
        threshold: 涨跌幅阈值 (threshold for price change)
    """
    df = df.copy()
    df["return"] = df["close"].pct_change()
    df["signal"] = 0
    df.loc[df["return"] > threshold, "signal"] = 1   # 买入 / Buy
    df.loc[df["return"] < -threshold, "signal"] = -1  # 卖出 / Sell
    return df

def run_backtest(code, strategy="ma", initial_capital=1000000):
    """
    运行回测 / Run backtest
    
    参数 / Parameters:
        code: 股票代码 (stock code)
        strategy: 策略名称 (strategy name)
        initial_capital: 初始资金 (initial capital)
    
    返回 / Returns:
        回测结果字典 (backtest result dict)
    """
    df = load_data(code)
    if df.empty:
        print(f"没有 {code} 的数据，请先运行 fetch_daily.py / No data for {code}, run fetch_daily.py first")
        return
    
    # 应用策略 / Apply strategy
    if strategy == "ma":
        df = ma_strategy(df)
    elif strategy == "momentum":
        df = momentum_strategy(df)
    
    # 模拟交易 / Simulate trading
    position = 0
    cash = initial_capital
    trades = []
    
    for i, row in df.iterrows():
        if row["signal"] == 1 and position == 0:
            # 买入 / Buy
            shares = int(cash / row["close"] / 100) * 100
            if shares > 0:
                cash -= shares * row["close"]
                position = shares
                trades.append({
                    "date": row["date"],
                    "type": "BUY",
                    "price": row["close"],
                    "shares": shares
                })
        elif row["signal"] == -1 and position > 0:
            # 卖出 / Sell
            cash += position * row["close"]
            pnl = position * (row["close"] - trades[-1]["price"])
            trades.append({
                "date": row["date"],
                "type": "SELL",
                "price": row["close"],
                "shares": position,
                "pnl": pnl
            })
            position = 0
    
    # 最终持仓 / Final position
    if position > 0:
        final_value = position * df.iloc[-1]["close"]
    else:
        final_value = cash
    
    # 收益 / Return
    total_return = (final_value - initial_capital) / initial_capital * 100
    
    print(f"\n{'='*40}")
    print(f"回测结果 / Backtest Result: {code} - {strategy}策略 / strategy")
    print(f"{'='*40}")
    print(f"初始资金 / Initial: ¥{initial_capital:,.0f}")
    print(f"最终价值 / Final: ¥{final_value:,.0f}")
    print(f"总收益 / Return: {total_return:.2f}%")
    print(f"交易次数 / Trades: {len(trades)}")
    print(f"{'='*40}")
    
    return {
        "code": code,
        "strategy": strategy,
        "initial_capital": initial_capital,
        "final_value": final_value,
        "total_return": total_return,
        "trades": trades
    }

def main():
    """
    主函数 / Main function
    命令行入口 / CLI entry point
    """
    import argparse
    parser = argparse.ArgumentParser(description='策略回测 / Strategy Backtest')
    parser.add_argument("--stock", default="600519", help="股票代码 / Stock code")
    parser.add_argument("--strategy", default="ma", choices=["ma", "momentum"], help="策略 / Strategy")
    parser.add_argument("--capital", type=int, default=1000000, help="初始资金 / Initial capital")
    args = parser.parse_args()
    
    run_backtest(args.stock, args.strategy, args.capital)

if __name__ == "__main__":
    main()
