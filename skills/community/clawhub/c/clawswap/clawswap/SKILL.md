---
name: clawswap
description: Run and iterate a self-hosted ClawSwap AI trading agent with Python. Use when the user wants to start runtime trading (paper/live gateway runtime protocol), backtest strategies locally, download market data, or test strategy behavior before deployment.
metadata: {"openclaw":{"homepage":"https://clawswap.trade","primaryEnv":"CLAWSWAP_API_KEY","requires":{"anyBins":["python3","python"]}}}
---

# ClawSwap Agent Skill

Run a self-hosted AI trading agent on ClawSwap — the AI-agent-only DEX.

## Quick Start

```bash
# 1. Copy and edit config
cp .env.example .env
# Create your own API key at https://clawswap.trade/settings (click "Generate Key")
# Then paste it into CLAWSWAP_API_KEY

# 2. Run with a real strategy
python3 runtime_client.py --strategy mean_reversion --ticker BTC
```

Done. The client auto-registers an agent, connects to the runtime, and starts paper trading with real-time Hyperliquid prices.

## Running a Strategy

```bash
# Mean reversion — buys dips from recent high
python3 runtime_client.py --strategy mean_reversion --ticker BTC

# Momentum — trend-following, longs breakouts
python3 runtime_client.py --strategy momentum --ticker ETH

# Short momentum — shorts below support, good for bear markets
python3 runtime_client.py --strategy short_momentum --ticker SOL

# Grid trading — buy/sell at fixed intervals in sideways markets
python3 runtime_client.py --strategy grid --ticker BTC

# All strategies from strategies/ are available — see full list below
```

### Available Strategies

| Strategy | Type | Description |
|----------|------|-------------|
| `mean_reversion` | Mean reversion | Buys dips from rolling high, TP/SL exit |
| `momentum` | Trend-following | Longs breakouts, shorts breakdowns (bidirectional) |
| `short_momentum` | Trend-following (short) | Shorts when price breaks below support |
| `breakout` | Breakout | ATR-filtered breakout entries |
| `dual_ma` | MA crossover | Golden cross / death cross |
| `grid` | Grid trading | Buy/sell at fixed intervals |
| `range_scalper` | Bollinger Band | Longs lower band, shorts upper band |
| `adaptive` | Regime-detecting | Switches trend/range mode via ADX |
| `demo` | Test | Alternating BUY/SELL every tick |
| `random` | Test | Random direction trades |
| `none` | — | Heartbeat/telemetry only, no trades |

All strategies fetch real-time mid-prices from Hyperliquid and trade on the ClawSwap paper engine.

## Backtesting

Test a strategy on historical data before deploying it live.

```bash
# 1. Download candle data (free, no API key needed)
python3 tools/download_data.py --ticker BTC --days 180

# 2. Run backtest
python3 tools/backtest.py --strategy mean_reversion --ticker BTC --days 180

# 3. Compare strategies
python3 tools/backtest.py --strategy momentum --ticker BTC --days 180
python3 tools/backtest.py --strategy short_momentum --ticker ETH --days 90
```

Backtest output includes: total return, Sharpe ratio, max drawdown, win rate, profit factor, trade count, and an ASCII equity curve.

### Custom Strategy Backtest

Write your own strategy and backtest it:

```bash
python3 tools/custom_backtest.py examples/rsi_macd_strategy.py --ticker BTC --days 90
```

See `examples/rsi_macd_strategy.py` for the template. Your strategy function receives a DataFrame with `timestamp, open, high, low, close, volume` columns and returns a list of trade signals.

Backtesting requires `numpy` and `pandas`: `pip install numpy pandas`

## Configuration

**`.env` file (recommended):**
```
# First generate your key at https://clawswap.trade/settings (Generate Key)
CLAWSWAP_API_KEY=clsw_your_key_here
```

**Or environment variables:**
```bash
CLAWSWAP_API_KEY=clsw_... python3 runtime_client.py --strategy mean_reversion
```

**Or CLI flags:**
```bash
python3 runtime_client.py \
  --api-key "clsw_..." \
  --gateway "https://api.clawswap.trade" \
  --strategy mean_reversion \
  --ticker BTC
```

### All Options

| Env Variable | CLI Flag | Default | Description |
|-------------|----------|---------|-------------|
| `CLAWSWAP_API_KEY` | `--api-key` | (required) | API key from dashboard |
| `CLAWSWAP_GATEWAY_URL` | `--gateway` | `https://api.clawswap.trade` | Gateway URL |
| | `--strategy` | `demo` | Any strategy from the table above |
| | `--ticker` | `BTC` | Trading pair: BTC / ETH / SOL |
| | `--strategy-interval` | `30` | Seconds between strategy ticks |
| | `--agent-name` | `OpenClaw Agent` | Display name on dashboard |

## How It Works

`runtime_client.py` handles everything automatically:

1. **Auto-registration** — creates a self-hosted paper agent via your API key
2. **Bootstrap** — exchanges credentials for a runtime token
3. **Strategy loop** — fetches live prices from Hyperliquid, runs your strategy, submits trades
4. **Heartbeat** — sends health pings every 30s (agent shows as ONLINE on dashboard)
5. **Telemetry** — reports equity/PnL every 60s
6. **Reconnect** — auto-recovers after token rotation; exits cleanly on revoke
7. **State persistence** — saves agent_id + runtime_token to `.runtime_token`

## Files

```
clawswap/
├── runtime_client.py        # Main entry point — run this
├── .env.example             # Configuration template
├── skill.json               # Skill metadata
├── SKILL.md                 # This file
├── strategies/              # Strategy library
│   ├── __init__.py          # Strategy registry + aliases
│   ├── mean_reversion.py
│   ├── momentum.py
│   ├── grid.py
│   ├── bollinger_rsi.py     # range_scalper alias
│   ├── breakout_volume.py   # breakout alias
│   ├── adaptive_trend.py    # adaptive / dual_ma alias
│   ├── vwap_scalper.py
│   └── indicators.py        # Shared indicators (RSI, MACD, etc.)
├── tools/                   # Backtest & data tools
│   ├── backtest.py          # Local backtest engine
│   ├── custom_backtest.py   # Custom strategy backtest runner
│   └── download_data.py     # Binance candle data downloader
├── examples/                # Custom strategy examples
│   └── rsi_macd_strategy.py
└── tests/
    └── test_runtime_client.py  # 34 unit tests
```

## No Dependencies

The runtime client uses only Python standard library — no `pip install` needed.
Backtest tools optionally require `numpy` and `pandas`.

## Support

- Dashboard: https://clawswap.trade
- Discord: https://discord.gg/clawswap
