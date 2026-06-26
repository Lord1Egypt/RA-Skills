---
name: agent-trading-bot
description: AI-powered trading bot framework for OpenClaw. Connects to crypto exchanges (Binance, Hyperliquid, Bluefin) and prediction markets (Polymarket, Kalshi) via API. Provides strategy templating, risk management (position sizing, stop-losses, max drawdown), paper trading mode, and live execution with kill-switch. Use when asked to "set up trading bot", "trade crypto", "connect to Binance", "prediction market bot", "automated trading", "trading strategy", "position sizing", "risk management for trading", "paper trading", "backtest strategy", "DCA bot", "grid trading", "funding rate arbitrage", or when building autonomous trading agents on OpenClaw.
---

# Agent Trading Bot

AI-powered trading framework for OpenClaw. Connect to exchanges, manage risk, execute strategies.

## Quick Start

```bash
# Check exchange connectivity (no trades)
python3 scripts/agent-trading-bot.py status

# Paper trade (simulated) with a strategy
python3 scripts/agent-trading-bot.py paper --strategy dca --pair BTC/USDT

# Live trade (requires API keys configured)
python3 scripts/agent-trading-bot.py trade --strategy dca --pair BTC/USDT --amount 100

# Risk dashboard — current positions, exposure, P&L
python3 scripts/agent-trading-bot.py risk

# Kill switch — close all positions immediately
python3 scripts/agent-trading-bot.py kill
```

## ⚠️ Safety First

**This skill includes multiple safety layers:**
1. Paper trading mode by default — no real money until explicitly enabled
2. Maximum position size limits (configurable)
3. Stop-loss on every position (default: 5%)
4. Maximum drawdown circuit breaker (default: 10% of portfolio)
5. Kill switch to close all positions instantly
6. API keys never stored in skill files — environment variables only

**The agent never trades without explicit user approval for live mode.**

## Commands

### `status` — Exchange Connectivity Check
Tests API connections without trading:
- Verifies API key validity
- Checks account balances
- Reports exchange status (maintenance, rate limits)
- Shows available trading pairs

### `paper` — Paper Trading (Simulated)
Runs strategy with fake money to test before going live:
- Simulates order execution at market prices
- Tracks P&L, win rate, Sharpe ratio
- Logs every trade decision with reasoning
- Options: `--strategy`, `--pair`, `--duration`, `--capital`

### `trade` — Live Trading
Executes strategy with real funds:
- Requires explicit `--live` flag (double confirmation)
- All safety limits enforced
- Every trade logged with timestamp, reasoning, and fills
- Options: `--strategy`, `--pair`, `--amount`, `--live`

### `risk` — Risk Dashboard
Real-time risk overview:
- Open positions with unrealized P&L
- Portfolio exposure by asset
- Current drawdown vs maximum allowed
- Margin utilization (for futures)
- Daily/weekly/monthly P&L

### `kill` — Emergency Kill Switch
Immediately closes all open positions:
- Market sells all spot positions
- Closes all futures positions
- Cancels all pending orders
- Logs everything
- Requires confirmation unless `--force` flag

### `backtest` — Strategy Backtesting
Test a strategy against historical data:
- Options: `--strategy`, `--pair`, `--start`, `--end`
- Reports: total return, max drawdown, Sharpe ratio, win rate

## Strategies

### Built-in Strategies

| Strategy | Description | Risk Level |
|----------|-------------|------------|
| `dca` | Dollar-Cost Average — buy fixed amount at intervals | Low |
| `grid` | Grid trading — buy low, sell high in a price range | Medium |
| `momentum` | Trend following with moving average crossovers | Medium |
| `funding` | Funding rate arbitrage (perpetual futures) | Medium |
| `mean-revert` | Buy oversold, sell overbought (RSI-based) | High |

See `references/strategies.md` for detailed strategy documentation.

### Custom Strategies
Create a strategy file at `strategies/<name>.json`:
```json
{
  "name": "my-strategy",
  "entry": { "indicator": "rsi", "condition": "below", "value": 30 },
  "exit": { "indicator": "rsi", "condition": "above", "value": 70 },
  "risk": { "stop_loss_pct": 3, "take_profit_pct": 9, "max_position_pct": 5 }
}
```

## Configuration

Set exchange API keys via environment variables:
```bash
export BINANCE_API_KEY="your-key"
export BINANCE_API_SECRET="your-secret"
export HYPERLIQUID_API_KEY="your-key"
export HYPERLIQUID_API_SECRET="your-secret"
```

Risk limits in `~/.openclaw/trading-config.json`:
```json
{
  "max_position_pct": 10,
  "max_drawdown_pct": 10,
  "default_stop_loss_pct": 5,
  "max_daily_trades": 20,
  "allowed_pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
}
```
