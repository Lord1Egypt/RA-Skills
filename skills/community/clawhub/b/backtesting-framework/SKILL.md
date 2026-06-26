---
name: backtesting-framework
description: Strategy backtesting framework for futures and stocks. Supports moving average crossovers, RSI mean reversion, Bollinger Bands breakout, and custom strategies. Generates performance reports with Sharpe, max drawdown, win rate.
emoji: 🔬
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Backtesting Framework — 策略回测框架

Pure Python backtesting engine for futures and stock strategies. No external dependencies beyond NumPy.

## Quick Start

```python
import numpy as np

# Sample price data (close prices)
prices = np.array([100, 102, 101, 105, 107, 106, 110, 108, 112, 115])

def ma_crossover(prices, fast=3, slow=5):
    """Moving Average Crossover Strategy"""
    fast_ma = np.convolve(prices, np.ones(fast)/fast, mode='valid')
    slow_ma = np.convolve(prices, np.ones(slow)/slow, mode='valid')
    
    # Align arrays
    min_len = min(len(fast_ma), len(slow_ma))
    fast_ma = fast_ma[-min_len:]
    slow_ma = slow_ma[-min_len:]
    
    # Generate signals: 1 = buy, -1 = sell, 0 = hold
    signals = np.zeros(min_len)
    signals[1:] = np.where(fast_ma[1:] > slow_ma[1:], 1, -1)
    
    return signals

def backtest(prices, signals, initial_capital=10000):
    """Run a backtest and return performance metrics."""
    # Pad signals to match prices
    pad = len(prices) - len(signals)
    signals = np.pad(signals, (pad, 0), 'constant', constant_values=0)
    
    # Calculate returns
    returns = np.diff(prices) / prices[:-1]
    strategy_returns = signals[:-1] * returns
    
    # Performance metrics
    total_return = np.prod(1 + strategy_returns) - 1
    sharpe = np.mean(strategy_returns) / np.std(strategy_returns) * np.sqrt(252) if np.std(strategy_returns) > 0 else 0
    win_rate = np.sum(strategy_returns > 0) / np.sum(strategy_returns != 0) if np.sum(strategy_returns != 0) > 0 else 0
    
    # Max drawdown
    cumulative = np.cumprod(1 + strategy_returns)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_dd = np.min(drawdown)
    
    return {
        "total_return": total_return,
        "sharpe_ratio": sharpe,
        "win_rate": win_rate,
        "max_drawdown": max_dd,
        "final_capital": initial_capital * (1 + total_return)
    }
```

## Built-in Strategies

### 1. Moving Average Crossover (均线金叉死叉)

```python
def ma_strategy(prices, fast=5, slow=20):
    fast_ma = np.convolve(prices, np.ones(fast)/fast, mode='valid')
    slow_ma = np.convolve(prices, np.ones(slow)/slow, mode='valid')
    min_len = min(len(fast_ma), len(slow_ma))
    signals = np.zeros(min_len)
    signals[1:] = np.where(fast_ma[1:min_len] > slow_ma[1:min_len], 1, -1)
    return signals
```

### 2. RSI Mean Reversion (RSI均值回归)

```python
def rsi_strategy(prices, period=14, oversold=30, overbought=70):
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.convolve(gains, np.ones(period)/period, mode='valid')
    avg_loss = np.convolve(losses, np.ones(period)/period, mode='valid')
    rs = avg_gain / np.where(avg_loss == 0, 0.001, avg_loss)
    rsi = 100 - (100 / (1 + rs))
    signals = np.zeros(len(rsi))
    signals[rsi < oversold] = 1
    signals[rsi > overbought] = -1
    return signals
```

### 3. Bollinger Bands Breakout (布林带突破)

```python
def bb_strategy(prices, period=20, std_dev=2):
    sma = np.convolve(prices, np.ones(period)/period, mode='valid')
    rolling_std = np.array([np.std(prices[i:i+period]) for i in range(len(prices)-period+1)])
    upper = sma + std_dev * rolling_std
    lower = sma - std_dev * rolling_std
    
    signals = np.zeros(len(sma))
    price_aligned = prices[period-1:]
    signals[price_aligned > upper] = -1  # Short at upper band
    signals[price_aligned < lower] = 1   # Long at lower band
    return signals
```

## Output Format

```
🔬 策略回测报告

策略: MA Crossover (5, 20)
品种: IF2606 (沪深300)
时间: 2026-01-01 ~ 2026-05-21

📊 绩效指标
• 总收益率:    +15.3%
• 年化收益:    +38.2%
• 夏普比率:    1.45  🟢
• 胜率:        42.5%
• 最大回撤:    -8.7%
• 交易次数:    42次

📈 资金曲线
期初: ¥10,000
期末: ¥11,530

⚠️ 回测表现不代表未来收益
```

## Notes

- All strategies use only NumPy for calculations
- Backtest results are hypothetical and do not account for: slippage, commissions, liquidity
- Always forward-test (paper trade) before going live
- Overfitting is the #1 enemy — keep strategies simple
- Use multiple timeframes to validate strategy robustness
