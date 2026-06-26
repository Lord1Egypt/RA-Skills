---
name: crypto-arb-cn
description: "加密货币套利监控 | Cryptocurrency Arbitrage Monitor. 支持币安、OKX、Gate.io、火币 | Supports Binance, OKX, Gate.io, Huobi. 实时价格监控、利润计算、Telegram通知 | Real-time price monitoring, profit calculation, Telegram alerts. 触发词：套利、arbitrage、加密货币、crypto、价格差. Find arbitrage opportunities across Chinese-accessible exchanges."
---

# Crypto Arbitrage CN

Monitor cryptocurrency prices across Chinese-accessible exchanges and find arbitrage opportunities.

## Quick Start

```bash
# Single check for opportunities
python scripts/arbitrage_monitor.py --once

# Continuous monitoring (every 30 seconds)
python scripts/arbitrage_monitor.py
```

## Supported Exchanges

| Exchange | Fee | API |
|----------|-----|-----|
| Binance | 0.1% | ✅ |
| OKX | 0.08% | ✅ |
| Gate.io | 0.2% | ✅ |
| Huobi | 0.2% | ✅ |

## Configuration

Edit these variables in `scripts/arbitrage_monitor.py`:

```python
# Trading pairs to monitor
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]

# Minimum profit threshold (after fees)
MIN_PROFIT_PERCENT = 0.5  # 0.5%

# Check interval (for continuous mode)
INTERVAL = 30  # seconds
```

## Output Format

When opportunities are found:

```
💰 BTCUSDT | 币安 → OKX | 利润: 0.65%
   买入: ¥485,230 (币安)
   卖出: ¥488,380 (OKX)
   预计利润: ¥3,150 (每 BTC)
```

## Usage Examples

**Check once:**
```
用户: 帮我看看现在有没有套利机会
→ Run: python scripts/arbitrage_monitor.py --once
```

**Start monitoring:**
```
用户: 开始监控套利机会
→ Run: python scripts/arbitrage_monitor.py
```

**Add Telegram notification:**
```
用户: 有机会发 Telegram 给我
→ Set up TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

## Important Notes

1. **Fees matter**: Always calculate profit after trading fees (0.1-0.2% per trade)
2. **Transfer time**: Cross-exchange arbitrage requires crypto transfer (10-60 min)
3. **Price volatility**: Prices change fast, opportunities may disappear
4. **Risk warning**: Arbitrage involves risk, user discretion advised

## References

- See [references/exchanges.md](references/exchanges.md) for detailed exchange API documentation
