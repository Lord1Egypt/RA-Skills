---
name: defi-trading-engine
description: DeFi Trading Engine - Autonomous DeFi trading bot with self-improving review system for OpenClaw agents. Use when setting up DeFi trading, crypto trading bot, automated trading, Base chain trading, Bankr integration, trading engine, self-improving bot, or trading strategy execution.
---

# DeFi Trading Engine

Autonomous DeFi trading bot with self-improving review system. Scans for opportunities, executes trades, logs performance, and learns from mistakes.

## When to Use

Apply this skill when:
- Setting up automated crypto trading on Base or other EVM chains
- Building a self-improving trading system
- Implementing systematic DeFi trading strategies
- Executing DCA, momentum, or mean reversion strategies
- Reviewing and optimizing trading performance
- Managing trading risk (position sizing, drawdown limits)
- Integrating with Bankr CLI or other DEX tools

## Architecture

**Self-Improvement Loop:**

```
scan → evaluate → execute → log → review → patch params → repeat
```

**Components:**
1. **Token Scanner** (`scan-tokens.py`) — Finds trading opportunities
2. **Risk Manager** (`risk-manager.py`) — Enforces position limits and risk rules
3. **Trade Executor** (`trade-executor.py`) — Executes trades via Bankr CLI
4. **Daily Review** (`daily-review.py`) — Analyzes performance and suggests improvements
5. **Config File** (`trading-config.json`) — Central configuration for all parameters

## Quick Start

### 1. Setup

Create workspace:

```bash
mkdir -p ~/trading-bot/{trades,reviews}
cd ~/trading-bot
```

Copy skill scripts:

```bash
cp ~/.openclaw/skills/defi-trading-engine/scripts/* .
```

### 2. Configure

Create `trading-config.json`:

```json
{
  "risk": {
    "max_position_size_usd": 40,
    "take_profit_pct": 4,
    "stop_loss_pct": 8,
    "max_active_positions": 5,
    "max_daily_trades": 8,
    "cooldown_minutes": 30,
    "max_drawdown_pct": 15
  },
  "strategy": {
    "type": "momentum_swing",
    "entry_signal": "volume_spike_and_price_up",
    "exit_signal": "take_profit_or_stop_loss",
    "timeframe": "15min"
  },
  "bankr": {
    "chain": "base",
    "wallet": "trading-wallet",
    "slippage_pct": 1.5
  },
  "data_sources": {
    "use_coingecko_trending": true,
    "use_dexscreener": true,
    "min_liquidity_usd": 50000,
    "min_volume_24h_usd": 100000
  }
}
```

### 3. Setup Bankr (if needed)

See `references/bankr-setup.md` for Bankr CLI setup.

### 4. Run the Trading Loop

**Manual execution:**

```bash
# 1. Scan for opportunities
python3 scan-tokens.py --output candidates.json

# 2. Review candidates
cat candidates.json

# 3. Execute a trade (after risk check)
python3 trade-executor.py --symbol SOL --action buy --amount 40

# 4. Run daily review
python3 daily-review.py
```

**Automated loop (cron):**

```bash
# Run scanner every 30 minutes
*/30 * * * * cd ~/trading-bot && python3 scan-tokens.py --output candidates.json

# Run daily review at 23:00
0 23 * * * cd ~/trading-bot && python3 daily-review.py
```

## Core Scripts

### scan-tokens.py

Scans for trading opportunities using free APIs.

**Data Sources:**
- CoinGecko trending coins
- Volume spikes (24h volume vs 7d average)
- Price momentum (1h, 4h, 24h trends)
- Liquidity and market cap filters

**Output (`candidates.json`):**
```json
[
  {
    "symbol": "SOL",
    "name": "Solana",
    "price": 145.5,
    "volume_24h": 2800000000,
    "volume_spike_ratio": 1.8,
    "price_change_1h_pct": 2.5,
    "price_change_24h_pct": 5.2,
    "liquidity_usd": 850000000,
    "score": 8.5,
    "signals": ["trending", "volume_spike", "momentum_up"]
  }
]
```

**Usage:**
```bash
python3 scan-tokens.py --output candidates.json --min-score 7.0
```

---

### risk-manager.py

Enforces risk limits before every trade. Acts as the gatekeeper.

**Checks:**
- Position size within limit
- Max active positions not exceeded
- Daily trade limit not exceeded
- Cooldown period respected
- Max drawdown not breached

**Usage:**
```bash
python3 risk-manager.py --action check --symbol SOL --amount 40
```

**Exit Codes:**
- `0` — Trade approved
- `1` — Trade denied (prints reason)

**Example Output:**
```
✅ Risk check passed
  - Position size: $40 (limit: $40)
  - Active positions: 3 (limit: 5)
  - Daily trades: 5 (limit: 8)
  - Cooldown: OK (35 minutes since last trade)
  - Drawdown: 8.5% (limit: 15%)
```

---

### trade-executor.py

Executes trades via Bankr CLI (or generic DEX interface).

**Supported Actions:**
- `buy` — Market buy
- `sell` — Market sell
- `limit_buy` — Limit order buy
- `limit_sell` — Limit order sell
- `set_stop_loss` — Stop-loss order
- `set_take_profit` — Take-profit order

**Usage:**
```bash
# Market buy
python3 trade-executor.py --symbol SOL --action buy --amount 40

# Sell with stop-loss
python3 trade-executor.py --symbol SOL --action sell --stop-loss-pct 8
```

**Trade Log (`trades/YYYY-MM-DD.json`):**
```json
[
  {
    "timestamp": "2026-03-13T15:45:00Z",
    "symbol": "SOL",
    "action": "buy",
    "amount_usd": 40,
    "price": 145.5,
    "quantity": 0.275,
    "tx_hash": "0xabc123...",
    "status": "success",
    "take_profit_price": 151.32,
    "stop_loss_price": 133.86
  }
]
```

---

### daily-review.py

Analyzes trade history, calculates P&L, identifies weaknesses, and suggests parameter adjustments.

**Metrics Calculated:**
- Total P&L (realized + unrealized)
- Win rate (% of profitable trades)
- Average win vs average loss
- Sharpe ratio (if enough data)
- Max drawdown
- Best/worst trades

**Output (`reviews/review-YYYY-MM-DD.md`):**

````markdown
# Trading Review — 2026-03-13

## Performance Summary
- **Total P&L:** +$42.50 (+5.3%)
- **Trades:** 8 (6 wins, 2 losses)
- **Win Rate:** 75%
- **Avg Win:** $9.20
- **Avg Loss:** -$5.80
- **Max Drawdown:** 8.5%

## Top Performers
1. SOL: +$18.50 (+12.7%)
2. LINK: +$12.20 (+8.1%)

## Worst Performers
1. UNI: -$8.50 (-5.7%)

## Pattern Analysis
- ✅ Momentum trades (4/5 profitable)
- ⚠️ Low liquidity tokens (1/3 profitable)
- ❌ Entries during high volatility (0/2 profitable)

## Recommended Adjustments
1. Increase `min_liquidity_usd` from $50k to $100k (low liquidity trades underperformed)
2. Add volatility filter (skip trades when VIX > 30)
3. Tighten stop-loss to 6% (avg loss exceeds target)

## Next Actions
- [ ] Update `trading-config.json` with new parameters
- [ ] Backtest on last 30 days with new rules
- [ ] Monitor performance for 1 week before further changes
````

**Usage:**
```bash
python3 daily-review.py --start-date 2026-03-01 --end-date 2026-03-13
```

---

## Configuration Reference

### Risk Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `max_position_size_usd` | 40 | Max $ per trade |
| `take_profit_pct` | 4 | Exit when +4% gain |
| `stop_loss_pct` | 8 | Exit when -8% loss |
| `max_active_positions` | 5 | Max concurrent positions |
| `max_daily_trades` | 8 | Max trades per day |
| `cooldown_minutes` | 30 | Wait time between trades |
| `max_drawdown_pct` | 15 | Stop trading if down 15% |

### Strategy Parameters

| Parameter | Options | Purpose |
|-----------|---------|---------|
| `type` | `momentum_swing`, `mean_reversion`, `dca`, `asymmetric` | Strategy type |
| `entry_signal` | `volume_spike_and_price_up`, `oversold`, `breakout` | Entry condition |
| `exit_signal` | `take_profit_or_stop_loss`, `reversal`, `time_based` | Exit condition |
| `timeframe` | `5min`, `15min`, `1h`, `4h` | Trading timeframe |

### Bankr Integration

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `chain` | `base` | EVM chain (base, ethereum, polygon) |
| `wallet` | `trading-wallet` | Bankr wallet name |
| `slippage_pct` | 1.5 | Max acceptable slippage |

---

## Strategy Templates

See `references/strategies.md` for detailed strategy implementations:

1. **DCA (Dollar-Cost Averaging)** — Buy fixed amount on schedule
2. **Momentum Swing** — Ride short-term momentum with tight stops
3. **Mean Reversion** — Buy dips, sell rallies
4. **Asymmetric Bets** — Small positions on high-upside opportunities

---

## Risk Management Rules

The risk manager enforces these rules:

### Position Sizing
```
Position size ≤ max_position_size_usd
```

### Active Position Limit
```
count(open_positions) < max_active_positions
```

### Daily Trade Limit
```
count(trades_today) < max_daily_trades
```

### Cooldown Period
```
time_since_last_trade ≥ cooldown_minutes
```

### Max Drawdown Circuit Breaker
```
if current_drawdown ≥ max_drawdown_pct:
  halt_all_trading()
  send_alert()
```

When max drawdown is hit, **all trading stops** until manually reset.

---

## Self-Improvement Process

The bot learns from performance:

**1. Daily Review**
Run `daily-review.py` to analyze trades.

**2. Pattern Recognition**
Identify which setups worked:
- Entry conditions with >70% win rate
- Tokens with consistent performance
- Timeframes with best risk/reward

**3. Parameter Adjustment**
Update `trading-config.json` based on findings:
- Tighten filters if win rate < 60%
- Adjust position size if drawdown too high
- Change timeframe if signals lag

**4. Backtest Changes**
Test new parameters on historical data (manual or automated).

**5. Monitor**
Run new parameters for 7 days, then review again.

**Cycle:** Weekly reviews → Parameter tweaks → Monitor → Repeat

---

## Safety Features

✅ **DO:**
- Start with small position sizes ($40 default)
- Use stop-losses on every trade
- Respect cooldown periods (avoid overtrading)
- Run daily reviews to catch bad patterns early
- Keep max drawdown limit low (15% default)
- Paper trade first (simulate without real funds)

❌ **DON'T:**
- Disable risk manager checks
- Increase position size without testing
- Remove stop-losses ("this time is different")
- Trade during network congestion (high gas fees)
- Ignore max drawdown signals
- Use leverage (this engine is spot-only by design)

---

## Monitoring & Alerts

Track bot health:

**Check active positions:**
```bash
jq '.[] | select(.status == "open")' trades/*.json
```

**Check today's P&L:**
```bash
python3 daily-review.py --start-date $(date +%Y-%m-%d) --end-date $(date +%Y-%m-%d)
```

**Alert on max drawdown:**
```bash
# Add to cron (every hour)
python3 risk-manager.py --action check_drawdown && echo "Trading halted: max drawdown exceeded"
```

---

## Troubleshooting

**Problem:** Risk manager denies all trades

**Solution:** Check `trading-config.json` limits. May have hit daily trade limit or max drawdown.

---

**Problem:** Trades execute but P&L is negative

**Solution:** Run `daily-review.py` to identify losing patterns. Tighten entry filters or adjust stop-loss.

---

**Problem:** Bankr CLI errors

**Solution:** Check wallet balance, network connection, and gas fees. See `references/bankr-setup.md`.

---

**Problem:** Scanner returns no candidates

**Solution:** Lower `min_score` threshold or relax liquidity filters.

---

## Advanced Features

### Paper Trading Mode

Test strategies without real funds:

```json
{
  "mode": "paper",
  "paper_balance_usd": 1000
}
```

All trades simulate execution, no real transactions.

### Multi-Strategy Support

Run multiple strategies in parallel:

```json
{
  "strategies": [
    {
      "name": "momentum",
      "allocation_pct": 60,
      "config": { ... }
    },
    {
      "name": "mean_reversion",
      "allocation_pct": 40,
      "config": { ... }
    }
  ]
}
```

### Backtesting

Test parameters on historical data (requires historical price data):

```bash
python3 backtest.py --start 2026-01-01 --end 2026-03-01 --config trading-config.json
```

*(Backtest script not included — implement based on your data source)*

---

## Resources

- **Bankr Setup:** `references/bankr-setup.md`
- **Strategy Templates:** `references/strategies.md`
- **CoinGecko API:** https://www.coingecko.com/en/api/documentation
- **Base Chain Docs:** https://docs.base.org

---

**Version:** 1.0
**Last Updated:** 2026-03-13
**Security Note:** Store API keys and wallet private keys securely. Never commit to Git.
