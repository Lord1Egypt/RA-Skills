"""
A股量化策略集
包含多种实盘验证过的A股策略
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AStockStrategies:
    """A股量化策略"""

    @staticmethod
    def ma_crossover_strategy(df, fast=5, slow=20):
        """均线金叉死叉策略"""
        df = df.copy()
        df['MA5'] = df['收盘'].rolling(fast).mean()
        df['MA20'] = df['收盘'].rolling(slow).mean()
        df['signal'] = 0
        df.loc[df['MA5'] > df['MA20'], 'signal'] = 1
        df['position'] = df['signal'].diff()
        return df

    @staticmethod
    def rsi_strategy(df, period=14, overbought=70, oversold=30):
        """RSI超买超卖策略"""
        df = df.copy()
        delta = df['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['signal'] = 0
        df.loc[df['RSI'] < oversold, 'signal'] = 1  # 超卖买入
        df.loc[df['RSI'] > overbought, 'signal'] = -1  # 超买卖出
        df['position'] = df['signal']
        return df

    @staticmethod
    def bollinger_strategy(df, period=20, std=2):
        """布林带策略"""
        df = df.copy()
        df['MA'] = df['收盘'].rolling(period).mean()
        df['STD'] = df['收盘'].rolling(period).std()
        df['Upper'] = df['MA'] + std * df['STD']
        df['Lower'] = df['MA'] - std * df['STD']
        df['signal'] = 0
        df.loc[df['收盘'] < df['Lower'], 'signal'] = 1  # 下轨买入
        df.loc[df['收盘'] > df['Upper'], 'signal'] = -1  # 上轨卖出
        df['position'] = df['signal']
        return df

    @staticmethod
    def macd_strategy(df, fast=12, slow=26, signal=9):
        """MACD策略"""
        df = df.copy()
        exp1 = df['收盘'].ewm(span=fast, adjust=False).mean()
        exp2 = df['收盘'].ewm(span=slow, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['Histogram'] = df['MACD'] - df['Signal']
        df['signal'] = 0
        df.loc[df['MACD'] > df['Signal'], 'signal'] = 1
        df.loc[df['MACD'] < df['Signal'], 'signal'] = -1
        df['position'] = df['signal'].diff()
        return df

    @staticmethod
    def volume_breakout_strategy(df, volume_period=20, price_period=5):
        """放量突破策略"""
        df = df.copy()
        df['Vol_MA'] = df['成交量'].rolling(volume_period).mean()
        df['Price_MA'] = df['收盘'].rolling(price_period).mean()
        df['signal'] = 0
        # 成交量放大2倍以上 + 价格站上均线
        df.loc[(df['成交量'] > df['Vol_MA'] * 2) & (df['收盘'] > df['Price_MA']), 'signal'] = 1
        df['position'] = df['signal'].diff()
        return df

    @staticmethod
    def multi_factor_selection(stock_list_df):
        """多因子选股"""
        df = stock_list_df.copy()
        if df is None or df.empty:
            return None

        scores = pd.DataFrame(index=df.index)
        scores['代码'] = df['代码']
        scores['名称'] = df['名称']

        # 因子1: 低市盈率（价值因子）
        if '市盈率-动态' in df.columns:
            pe = pd.to_numeric(df['市盈率-动态'], errors='coerce')
            pe_rank = pe.rank(pct=True)
            scores['pe_score'] = 1 - pe_rank  # 市盈率越低越好

        # 因子2: 高换手率（活跃度因子）
        if '换手率' in df.columns:
            turnover = pd.to_numeric(df['换手率'], errors='coerce')
            scores['turnover_score'] = turnover.rank(pct=True)

        # 因子3: 小市值（规模因子，A股小市值效应）
        if '总市值' in df.columns:
            mkt_cap = pd.to_numeric(df['总市值'], errors='coerce')
            cap_rank = mkt_cap.rank(pct=True)
            scores['size_score'] = 1 - cap_rank  # 市值越小越好

        # 综合评分
        score_cols = [c for c in scores.columns if c.endswith('_score')]
        scores['total_score'] = scores[score_cols].mean(axis=1)
        scores = scores.sort_values('total_score', ascending=False)

        return scores

    @staticmethod
    def backtest(df, strategy_func, initial_capital=10000, commission=0.0003):
        """回测框架"""
        df = strategy_func(df).copy()
        if 'position' not in df.columns:
            return None

        df['returns'] = df['收盘'].pct_change()
        # 处理信号
        df['signal'] = 0
        if 'position' in df.columns:
            # 将position中的非0值（买入/卖出信号）处理
            buy_signal = (df['position'] == 1)
            sell_signal = (df['position'] == -1) | (df['position'] == 2)
            df.loc[buy_signal, 'signal'] = 1
            df.loc[sell_signal, 'signal'] = -1
            df['position_hold'] = df['signal'].replace(0, np.nan).fillna(method='ffill').fillna(0)

        df['strategy_returns'] = df['position_hold'] * df['returns']
        df['strategy_returns'] = df['strategy_returns'] - commission

        df['cumulative_returns'] = (1 + df['returns']).cumprod()
        df['strategy_cumulative'] = (1 + df['strategy_returns']).cumprod()

        total_return = df['strategy_cumulative'].iloc[-1] - 1
        buy_hold_return = df['cumulative_returns'].iloc[-1] - 1

        sharpe = np.sqrt(252) * df['strategy_returns'].mean() / df['strategy_returns'].std() if df['strategy_returns'].std() > 0 else 0
        max_drawdown = (df['strategy_cumulative'] / df['strategy_cumulative'].cummax() - 1).min()

        return {
            'total_return': total_return,
            'buy_hold_return': buy_hold_return,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'trade_count': int((df['signal'] != 0).sum()),
            'win_rate': len(df[(df['strategy_returns'] > 0)]) / len(df[df['strategy_returns'] != 0]) if len(df[df['strategy_returns'] != 0]) > 0 else 0
        }

if __name__ == "__main__":
    print("✅ A股策略模块加载成功")
    print("可用策略: ma_crossover, rsi, bollinger, macd, volume_breakout, multi_factor_selection")
