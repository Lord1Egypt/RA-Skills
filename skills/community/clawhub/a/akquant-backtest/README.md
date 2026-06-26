# AKQuant A-Share Backtesting

High-performance quantitative backtesting for Chinese stocks using Rust-powered AKQuant framework.

## Features

- **Double MA Strategy** - Golden cross buy, death cross sell
- **Custom Strategies** - Build your own trading logic
- **AKShare Data** - Real-time A-share market data
- **Performance Metrics** - Returns, trade count, equity curve
- **Parameter Optimization** - Test different MA periods

## Installation

```bash
clawhub install akquant-backtest
```

## Quick Start

### Basic Backtest
```bash
python3 scripts/run_backtest.py 600519 10 30
```

This runs a double MA strategy on 贵州茅台 (600519) with 10-day fast MA and 30-day slow MA.

## Requirements

- Python 3.8+
- akquant
- akshare
- pandas
- numpy

## Setup

```bash
source /root/.openclaw/venv/bin/activate
pip install akquant akshare pandas numpy
```

## Usage Examples

### Quick Backtest
```bash
# Default 10/30 MA on 平安银行
python3 scripts/run_backtest.py 000001

# Custom parameters on 贵州茅台
python3 scripts/run_backtest.py 600519 5 20
```

### Common Stock Symbols
| Symbol | Company | Sector |
|--------|---------|--------|
| 600519 | 贵州茅台 | 消费 |
| 000001 | 平安银行 | 金融 |
| 300750 | 宁德时代 | 新能源 |
| 002594 | 比亚迪 | 汽车 |

### Strategy Comparison
```bash
# Test different MA combinations
for fast in 5 10 15; do
  for slow in 20 30 60; do
    echo "Testing $fast/$slow:"
    python3 scripts/run_backtest.py 000001 $fast $slow
  done
done
```

## Python API

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

## Custom Strategy Development

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
            return 'BUY'
        elif self.rsi.value > self.overbought:
            return 'SELL'
        return 'HOLD'
```

## Troubleshooting

- **ModuleNotFoundError**: Install dependencies with pip
- **Stock symbol not found**: Use 6-digit codes (000001, 600519)
- **No data returned**: Check date range and stock status
- **Negative returns**: Verify fast_period < slow_period

## Best Practices

1. **Start simple** - Test MA crossover before complex strategies
2. **Include costs** - Account for 0.1% commission + slippage
3. **Avoid overfitting** - Test on out-of-sample data
4. **Risk management** - Add stop-loss logic

## Limitations

- Data has 15-minute delay (backtesting only, not live trading)
- Past performance ≠ future results
- Delisted stocks not in historical data

## License

MIT-0

## References

- [AKQuant GitHub](https://github.com/akfamily/akquant)
- [AKShare Documentation](https://www.akshare.xyz/)
