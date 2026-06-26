---
name: akquant-backtest
description: A-share quantitative trading backtesting using AKQuant (Rust engine) and AKShare data. Use when user asks to "backtest a stock strategy", "test trading algorithm on Chinese stocks", "analyze stock performance", "run double MA strategy", or "optimize trading parameters". Supports double MA, RSI, and custom strategies for A-shares.
---

# AKQuant A-Share Backtesting

High-performance quantitative backtesting for Chinese stocks using Rust-powered AKQuant framework.

## When to Use This Skill

Use this skill when you need to:
- **Backtest trading strategies** - "Backtest double MA strategy on 平安银行"
- **Analyze stock performance** - "How would a momentum strategy perform on 茅台?"
- **Optimize trading parameters** - "Find best MA periods for 宁德时代"
- **Validate trading ideas** - "Test if RSI works on Chinese tech stocks"
- **Compare strategies** - "Which performs better: MA crossover or RSI?"

## Quick Examples

### Example 1: Quick Backtest
**User says:** "Backtest double MA strategy on 贵州茅台"

**Actions:**
```bash
python3 scripts/run_backtest.py 600519 10 30
```

**Result:** Returns total return, trade count, equity curve

### Example 2: Strategy Comparison
**User says:** "Compare 5-day vs 20-day MA on 平安银行"

**Actions:**
```bash
# Fast MA = 5, Slow MA = 20
python3 scripts/run_backtest.py 000001 5 20

# Compare with default 10/30
python3 scripts/run_backtest.py 000001 10 30
```

**Result:** Compare returns to find optimal parameters

### Example 3: Research Workflow
**User says:** "Analyze which tech stocks performed best with momentum strategy in 2024"

**Actions:**
1. Test on multiple stocks: `python3 scripts/run_backtest.py 300750 10 30` (宁德时代)
2. Test: `python3 scripts/run_backtest.py 002594 10 30` (比亚迪)
3. Compare results and identify patterns

## Step-by-Step Instructions

### Step 1: Choose Stock Symbol

**Common A-Share Symbols:**
| Symbol | Company | Sector |
|--------|---------|--------|
| 600519 | 贵州茅台 | 消费 |
| 000001 | 平安银行 | 金融 |
| 300750 | 宁德时代 | 新能源 |
| 002594 | 比亚迪 | 汽车 |
| 000858 | 五粮液 | 消费 |

**Find symbol:** Use AKShare or search "股票代码 + 公司名称"

### Step 2: Select Strategy Parameters

**Double MA Strategy (金叉买入，死叉卖出):**
```bash
python3 scripts/run_backtest.py <symbol> <fast_period> <slow_period>
```

**Recommended combinations:**
- Conservative: 20 / 60 (fewer trades, longer trends)
- Balanced: 10 / 30 (moderate frequency)
- Aggressive: 5 / 20 (more trades, shorter trends)

### Step 3: Analyze Results

**Key metrics to review:**
- **总收益率** - Overall strategy performance
- **交易次数** - Frequency (lower = less commission)
- **最大回撤** - Risk measure (if implemented)
- **胜率** - % of profitable trades

**Interpretation:**
```
Return > 0%    → Strategy beats buy-and-hold
Return < 0%    → Strategy underperforms
Trade count > 20 → Consider commission impact
```

## Available Strategies

### Built-in Strategy: Double MA
**Logic:** Fast MA crosses above slow MA → Buy; Crosses below → Sell

**Code example:**
```python
from double_ma_strategy import run_double_ma_backtest

result = run_double_ma_backtest(
    symbol="000001",
    fast_period=10,
    slow_period=30,
    initial_capital=100000,
    start_date="20240101",
    end_date="20241231"
)

print(f"Return: {result['return_pct']:.2f}%")
print(f"Trades: {len(result['trades'])}")
```

### Custom Strategy Development

**RSI Strategy Template:**
```python
import akquant as aq

class RsiStrategy:
    def __init__(self, period=14, oversold=30, overbought=70):
        self.rsi = aq.RSI(period)
        self.oversold = oversold
        self.overbought = overbought
        
    def on_bar(self, bar):
        self.rsi.update(bar['close'])
        
        if self.rsi.value < self.oversold:
            return 'BUY'  # 超卖买入
        elif self.rsi.value > self.overbought:
            return 'SELL'  # 超买卖出
        return 'HOLD'
```

## Technical Indicators Reference

| Indicator | Usage | Signal |
|-----------|-------|--------|
| `aq.SMA(n)` | Trend following | Price > SMA → uptrend |
| `aq.EMA(n)` | Faster trend | More responsive than SMA |
| `aq.RSI(n)` | Momentum | <30 oversold, >70 overbought |
| `aq.MACD()` | Trend + momentum | Crossover signals |
| `aq.BollingerBands(n, k)` | Volatility | Price touches bands |
| `aq.ATR(n)` | Risk sizing | Position sizing based on volatility |

**Example:**
```python
import akquant as aq

# Multi-indicator strategy
sma = aq.SMA(20)
rsi = aq.RSI(14)

for price in prices:
    sma.update(price)
    rsi.update(price)
    
    # Buy: Price > SMA AND RSI < 40 (uptrend but not overbought)
    if price > sma.value and rsi.value < 40:
        signal = 'BUY'
```

## Data Access via AKShare

### Stock Historical Data
```python
import akshare as ak

# Daily price data (qfq = 前复权)
df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq"
)

# Columns: 日期, 开盘, 收盘, 最高, 最低, 成交量
```

### Real-time Quote
```python
# Current prices
df = ak.stock_zh_a_spot_em()
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'akquant'"
**Cause:** Dependencies not installed
**Solution:**
```bash
source /root/.openclaw/venv/bin/activate
pip install akquant akshare pandas numpy
```

### Error: "Stock symbol not found"
**Cause:** Wrong symbol format
**Solution:**
- A-shares use 6-digit codes: 000001 (SZ), 600519 (SH), 300750 (创业板)
- Don't include exchange prefix (use `000001` not `SZ000001`)

### Error: "No data returned"
**Causes:**
1. **Invalid date range** - Check `start_date` < `end_date`
2. **Stock suspended** - Some stocks have trading halts
3. **Delisted stock** - Verify stock is still trading
4. **Network issue** - AKShare requires internet connection

### Strategy returns -100% (total loss)
**Causes:**
1. **Wrong parameter order** - `fast_period` should be < `slow_period`
   ```bash
   # Wrong: fast > slow
   python3 scripts/run_backtest.py 000001 30 10
   
   # Correct: fast < slow
   python3 scripts/run_backtest.py 000001 10 30
   ```
2. **Too many trades** - High commission costs
3. **Wrong signal logic** - Check buy/sell conditions

### Slow performance
**Solutions:**
- Reduce date range (test 3 months instead of 1 year)
- Use `fast_period` >= 5 to reduce calculation
- AKQuant is Rust-based and fast; slowness usually comes from data fetching

### Results inconsistent between runs
**Cause:** AKShare data updates (recent days)
**Solution:**
- Use fixed date ranges for reproducibility
- Cache data locally if needed

## Best Practices

### Strategy Development Workflow
1. **Start simple** - Test MA crossover before complex strategies
2. **Visualize** - Plot equity curve if possible
3. **Walk-forward test** - Train on 2023, test on 2024
4. **Transaction costs** - Include 0.1% commission + 0.1% slippage
5. **Risk management** - Add stop-loss logic

### Parameter Optimization
```bash
# Test multiple combinations
for fast in 5 10 15; do
  for slow in 20 30 60; do
    echo "Testing $fast/$slow:"
    python3 scripts/run_backtest.py 000001 $fast $slow
  done
done
```

### Avoid Overfitting
- Don't optimize too many parameters
- Test on out-of-sample data
- Simple strategies often outperform complex ones

## Limitations & Warnings

- **Data delay:** AKShare has 15-minute delay - for backtesting only, not live trading
- **Historical bias:** Past performance ≠ future results
- **Execution:** Real-world fills may differ from backtest assumptions
- **Survivorship:** Delisted stocks not in current data
- **Dividends:** Adjusted prices used, but dividend timing affects returns

## References

- [AKQuant Cheat Sheet](references/akquant_cheatsheet.md) - Quick API reference
- [AKShare Documentation](https://www.akshare.xyz/) - Data sources
- [AKQuant GitHub](https://github.com/akfamily/akquant) - Official docs
