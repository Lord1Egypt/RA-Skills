#!/usr/bin/env python3
"""
TDD 实践：优化趋势过滤器
目标：添加三重过滤器（MA20 斜率 + ADX + 突破确认）解决震荡市频繁止损问题
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 工具函数 ====================

def generate_sideways_price_data(days=180, range_pct=0.05, base_price=100):
    """
    生成震荡市价格数据（价格在区间内波动）
    
    Args:
        days: 天数
        range_pct: 波动范围（如 0.05 表示±5%）
        base_price: 基准价格
    
    Returns:
        DataFrame with 'close' prices
    """
    np.random.seed(42)  # 可重复性
    
    # 生成随机游走但限制在区间内
    prices = [base_price]
    for i in range(days - 1):
        # 随机波动
        change = np.random.uniform(-range_pct/2, range_pct/2)
        new_price = prices[-1] * (1 + change)
        
        # 限制在区间内
        min_price = base_price * (1 - range_pct)
        max_price = base_price * (1 + range_pct)
        new_price = np.clip(new_price, min_price, max_price)
        
        prices.append(new_price)
    
    return pd.DataFrame({
        'timestamp': pd.date_range(start=datetime.now() - timedelta(days=days), periods=days),
        'close': prices,
        'open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
        'high': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        'volume': np.random.randint(100000, 500000, days)
    })


def generate_trending_price_data(days=180, trend_pct=0.3, base_price=100):
    """
    生成趋势市价格数据（价格持续上涨/下跌）
    
    Args:
        days: 天数
        trend_pct: 总趋势幅度（如 0.3 表示 30% 涨幅）
        base_price: 基准价格
    
    Returns:
        DataFrame with 'close' prices
    """
    np.random.seed(42)  # 可重复性
    
    # 计算每日平均趋势
    daily_trend = trend_pct / days
    
    prices = [base_price]
    for i in range(days - 1):
        # 趋势 + 噪音
        noise = np.random.uniform(-0.005, 0.01)  # 轻微向上偏斜
        new_price = prices[-1] * (1 + daily_trend + noise)
        prices.append(new_price)
    
    return pd.DataFrame({
        'timestamp': pd.date_range(start=datetime.now() - timedelta(days=days), periods=days),
        'close': prices,
        'open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
        'high': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        'volume': np.random.randint(100000, 500000, days)
    })


def calculate_ma(prices, period):
    """计算移动平均线"""
    return prices.rolling(window=period).mean()


def calculate_ma20_slope(prices, lookback=5):
    """
    计算 MA20 的斜率（过去 lookback 天的变化率）
    
    Args:
        prices: 价格序列
        lookback: 回溯天数
    
    Returns:
        斜率（变化率）
    """
    ma20 = calculate_ma(prices, 20)
    
    if len(ma20) < lookback + 19:  # 需要足够的数据
        return 0
    
    current_ma = ma20.iloc[-1]
    past_ma = ma20.iloc[-lookback]
    
    if pd.isna(current_ma) or pd.isna(past_ma):
        return 0
    
    slope = (current_ma - past_ma) / past_ma
    return slope


def calculate_adx(prices, period=14):
    """
    计算 ADX (Average Directional Index)
    ADX > 25 表示强趋势，ADX < 20 表示震荡市
    
    Args:
        prices: 价格 DataFrame（需要 high, low, close）
        period: ADX 周期
    
    Returns:
        ADX 值
    """
    if len(prices) < period * 2:
        return 0
    
    high = prices['high']
    low = prices['low']
    close = prices['close']
    
    # 计算 +DM 和 -DM
    plus_dm = high.diff()
    minus_dm = -low.diff()
    
    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)
    
    # 计算 TR (True Range)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # 平滑处理
    atr = tr.rolling(window=period).mean()
    plus_di = 100 * pd.Series(plus_dm).rolling(window=period).mean() / atr
    minus_di = 100 * pd.Series(minus_dm).rolling(window=period).mean() / atr
    
    # 计算 DX 和 ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di).replace(0, np.nan)
    adx = dx.rolling(window=period).mean()
    
    return adx.iloc[-1] if not pd.isna(adx.iloc[-1]) else 0


# ==================== 策略实现 ====================

class TrendFilterStrategy:
    """
    带三重过滤器的趋势策略
    过滤器：MA20 斜率 + ADX + 突破确认
    """
    
    def __init__(self, fast_period=5, slow_period=20, 
                 ma20_slope_threshold=0.01, 
                 adx_threshold=20,
                 breakout_confirmation=True):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma20_slope_threshold = ma20_slope_threshold
        self.adx_threshold = adx_threshold
        self.breakout_confirmation = breakout_confirmation
        self.position = 0
        self.prices_history = []
    
    def should_trade(self, signal, prices_df):
        """
        三重过滤器决策
        
        过滤器 1: MA20 斜率（趋势方向）
        过滤器 2: ADX（趋势强度）
        过滤器 3: 突破确认（价格突破）
        """
        # 需要足够数据来计算 ADX(14) 和 MA20
        min_bars = self.slow_period + 14
        if len(prices_df) < min_bars:
            return False
        
        # 过滤器 1: MA20 斜率
        ma20_slope = calculate_ma20_slope(prices_df['close'])
        
        # 过滤器 2: ADX
        adx = calculate_adx(prices_df)
        
        # 过滤器 3: 突破确认（价格是否突破前 N 天的高点）
        if self.breakout_confirmation:
            # 突破前 fast_period 天之前的高点（避免看最近几天）
            lookback_start = -(self.fast_period * 2)
            lookback_end = -self.fast_period
            if len(prices_df) > abs(lookback_start):
                prev_high = prices_df['high'].iloc[lookback_start:lookback_end].max()
                current_price = prices_df['close'].iloc[-1]
                breakout = current_price > prev_high
            else:
                breakout = True
        else:
            breakout = True
        
        if signal == 'BUY':
            # 三重过滤：只在上升趋势 + 强趋势 + 突破时做多
            if (ma20_slope > self.ma20_slope_threshold and 
                adx > self.adx_threshold and 
                breakout):
                return True
        
        elif signal == 'SELL':
            # 卖出信号：趋势反转或过滤器失效
            if ma20_slope < -self.ma20_slope_threshold or adx < 15:
                return True
        
        return False
    
    def on_bar(self, bar, prices_df):
        """
        K 线事件处理
        
        Args:
            bar: 当前 K 线
            prices_df: 历史价格 DataFrame
        
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        self.prices_history.append(bar)
        
        # 需要足够数据来计算所有指标
        min_bars = self.slow_period + 14  # MA20 + ADX(14)
        if len(prices_df) < min_bars:
            return 'HOLD'
        
        # 计算双均线信号
        fast_ma = calculate_ma(prices_df['close'], self.fast_period).iloc[-1]
        slow_ma = calculate_ma(prices_df['close'], self.slow_period).iloc[-1]
        
        if pd.isna(fast_ma) or pd.isna(slow_ma):
            return 'HOLD'
        
        # 基础信号
        if fast_ma > slow_ma and self.position <= 0:
            signal = 'BUY'
        elif fast_ma < slow_ma and self.position > 0:
            signal = 'SELL'
        else:
            signal = 'HOLD'
        
        # 应用过滤器
        if signal == 'BUY':
            if self.should_trade(signal, prices_df):
                self.position = 1
                return 'BUY'
            else:
                return 'HOLD'
        
        elif signal == 'SELL':
            if self.should_trade(signal, prices_df):
                self.position = 0
                return 'SELL'
            else:
                return 'HOLD'
        
        return 'HOLD'


def run_strategy(prices_df, strategy=None):
    """
    运行策略回测
    
    Args:
        prices_df: 价格 DataFrame
        strategy: 策略实例（可选）
    
    Returns:
        回测结果对象
    """
    if strategy is None:
        strategy = TrendFilterStrategy()
    
    trades = []
    position = 0
    cash = 100000
    shares = 0
    
    for idx in range(len(prices_df)):
        bar = {
            'timestamp': prices_df.iloc[idx]['timestamp'],
            'close': prices_df.iloc[idx]['close'],
            'open': prices_df.iloc[idx]['open'],
            'high': prices_df.iloc[idx]['high'],
            'low': prices_df.iloc[idx]['low'],
            'volume': prices_df.iloc[idx]['volume']
        }
        
        # 获取到当前的价格历史
        current_prices = prices_df.iloc[:idx+1].copy()
        
        # 获取交易信号
        signal = strategy.on_bar(bar, current_prices)
        
        price = bar['close']
        
        # 执行交易
        if signal == 'BUY' and position == 0:
            shares = int(cash / price / 100) * 100
            if shares > 0:
                cost = shares * price
                cash -= cost
                position = 1
                trades.append({
                    'type': 'BUY',
                    'date': bar['timestamp'],
                    'price': price,
                    'shares': shares
                })
        
        elif signal == 'SELL' and position == 1:
            revenue = shares * price
            cash += revenue
            trades.append({
                'type': 'SELL',
                'date': bar['timestamp'],
                'price': price,
                'shares': shares
            })
            shares = 0
            position = 0
    
    # 计算最终结果
    final_value = cash + shares * prices_df['close'].iloc[-1]
    total_return = (final_value - 100000) / 100000
    
    class Result:
        def __init__(self, trades, final_value, total_return, position, num_trades):
            self.trades = trades
            self.final_value = final_value
            self.total_return = total_return
            self.position = position
            self.num_trades = num_trades
    
    return Result(
        trades=trades,
        final_value=final_value,
        total_return=total_return,
        position=position,
        num_trades=len(trades)
    )


# ==================== TDD 测试 ====================

def test_sideways_market_should_not_trade():
    """
    RED 1: 震荡市条件下，策略应该空仓
    期望：交易次数很少或为空
    """
    print("\n" + "="*60)
    print("测试 1: 震荡市应该空仓")
    print("="*60)
    
    # 生成震荡市数据
    prices = generate_sideways_price_data(days=180, range_pct=0.05)
    
    # 运行策略
    result = run_strategy(prices)
    
    print(f"交易次数：{result.num_trades}")
    print(f"最终仓位：{result.position}")
    print(f"总收益率：{result.total_return:.2%}")
    
    # 断言：交易次数很少或为空
    try:
        assert result.num_trades < 5 or result.position == 0, \
            f"震荡市交易过于频繁：{result.num_trades} 次"
        print("✅ 测试通过：震荡市空仓")
        return True
    except AssertionError as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_trending_market_should_trade():
    """
    RED 2: 趋势市条件下，策略应该交易
    期望：有交易，且盈利
    """
    print("\n" + "="*60)
    print("测试 2: 趋势市应该交易")
    print("="*60)
    
    # 生成趋势市数据
    prices = generate_trending_price_data(days=180, trend_pct=0.3)
    
    # 运行策略
    strategy = TrendFilterStrategy()
    result = run_strategy(prices, strategy)
    
    print(f"交易次数：{result.num_trades}")
    print(f"最终仓位：{result.position}")
    print(f"总收益率：{result.total_return:.2%}")
    
    # 断言：有交易且盈利
    try:
        assert result.num_trades > 0, "趋势市没有交易"
        assert result.total_return > 0, f"趋势市未盈利：{result.total_return:.2%}"
        print("✅ 测试通过：趋势市交易")
        return True
    except AssertionError as e:
        print(f"❌ 测试失败：{e}")
        return False


def run_all_tests():
    """运行所有 TDD 测试"""
    print("\n" + "="*60)
    print("TDD 实践：趋势过滤器优化")
    print("="*60)
    
    results = {
        'sideways': test_sideways_market_should_not_trade(),
        'trending': test_trending_market_should_trade()
    }
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    print(f"震荡市测试：{'✅ 通过' if results['sideways'] else '❌ 失败'}")
    print(f"趋势市测试：{'✅ 通过' if results['trending'] else '❌ 失败'}")
    
    return results


if __name__ == '__main__':
    run_all_tests()
