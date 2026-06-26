---
name: boeingchoco-polymarket-ai-divergence
description: "Find markets where Simmer's AI consensus diverges from the real market price, then trade on the mispriced side using calibration-shrunk Kelly sizing. Scans for divergence, applies AI-overconfidence shrinkage, liquidity / spread / time-to-resolution safeguards, and executes trades on zero-fee markets with sufficient surviving edge."
metadata:
  author: Simmer (@simmer_markets)
  version: "2.6.1"
  displayName: Polymarket AI Divergence
  difficulty: intermediate
  openclaw:
    emoji: "🔮"
    primaryEnv: SIMMER_API_KEY
    requires:
      anyBins:
        - python3
        - python
      env:
        - SIMMER_API_KEY
    install:
      - id: uv-simmer-sdk
        kind: uv
        package: "simmer-sdk>=0.11.1"
        label: "Install Simmer SDK (uv)"
---
# Polymarket AI Divergence Trader

Find markets where Simmer's AI consensus diverges from the real market price, then trade the edge — defensively.

> **This is a template.** v2.6 defaults trade when the **calibrated** edge survives 3% (raw divergence × source/adaptive shrinkage − fees − 1% slippage buffer − optional longshot penalty), on zero-fee Polymarket markets with ≥ $1k liquidity, ≥ $500 24h volume, ≥ 6h to resolution, ≤ 180d to resolution, top-of-book depth ≥ $250, and where the half-spread eats < 50% of the edge. Position size is fractional Kelly (cap 0.20), capped at 5% of market liquidity and 20% of top-of-book depth, scaled by `sqrt(days_to_resolve / 30)`, then adjusted by category-aware Kelly multipliers. Remix any of these (see *Configuration*). The skill handles plumbing — your agent provides the alpha.

## What's new in v2.6 (category-aware sizing)

v2.6 adds a **category-aware Kelly multiplier**. Research (Kalshibench, QuantPedia 2025) shows AI consensus alpha is heterogeneous across Polymarket categories:

- **Politics & crypto** are dominated by professional bot flow → AI edge is small but cleaner → multiplier **0.60**
- **Sports** has more retail noise → AI edge is larger and less compressed → multiplier **0.85**
- **Niche / long-tail** (default bucket) is where AI most outperforms market consensus → multiplier **0.75**

Set `category_multipliers_csv` to remix, e.g. `"politics=0.5,crypto=0.5,sports=0.9,weather=1.0,default=0.7"`. Disable with `SIMMER_DIVERGENCE_ENABLE_CATEGORY_MULTIPLIER=0`.

Also in v2.6: the structured automaton report now includes a `skip_reason_counts` histogram so operators can tell which safeguard is doing most of the filtering and tune the right knob.

## What's new in v2.5 (research-backed)

v2.5 adds **source-aware and adaptive calibration shrinkage** on top of v2.4. Instead of using one fixed shrinkage for every market, the strategy now starts with a signal-source-specific shrinkage (`oracle_shrinkage=0.65`, `crowd_shrinkage=0.80`) and then shrinks edge harder in stress regimes:

- high 1-day price-move markets (`one_day_price_change`) where short-term volatility and narrative whipsaw are elevated
- thinner-liquidity markets near the floor where executable alpha is less reliable
- low-probability contracts where favorite-longshot bias is structurally expensive
- thin top-of-book markets where fills are likely to move the price

This is controlled by:
- `oracle_shrinkage` (default `0.65`)
- `crowd_shrinkage` (default `0.80`)
- `enable_adaptive_shrinkage` (default `1`)
- `adaptive_shrinkage_vol_mult` (default `1.25`)
- `longshot_threshold` (default `0.15`)
- `longshot_penalty_bps` (default `75`)
- `slippage_buffer_pct` (default `0.01`)
- `min_top_book_depth_usd` (default `250`)

The goal is simple: **fewer false positives, higher realized edge per executed trade**.

## What changed in v2.4 (research-backed)

Independent research showed AI forecasters are systematically overconfident (Kalshibench: even Claude Opus shows ECE ≈ 0.12) and that 87% of Polymarket wallets lose money primarily to **position-size mistakes**, not bad predictions. v2.4 adds seven safeguards designed to address those failure modes:

1. **AI calibration shrinkage** — multiply the raw AI − market divergence by `ai_shrinkage` (default 0.70) before treating it as edge.
2. **Liquidity floor** — skip Polymarket markets with on-book liquidity below `min_liquidity_usd` (default $1k).
3. **Volume floor** — skip markets with 24h volume below `min_volume_24h_usd` (default $500) to avoid stale prices.
4. **Time-to-resolution band** — skip markets resolving in less than `min_hours_to_resolve` (default 6h, terminal-volatility / oracle risk) or more than `max_days_to_resolve` (default 180d, capital opportunity cost).
5. **Extreme-divergence sanity cap** — skip divergences above `max_divergence_sanity` (default 40%) as likely stale data or broken oracles.
6. **CLOB spread check** — fetch the YES/NO orderbook from `clob.polymarket.com` and skip if the half-spread exceeds `max_spread_pct_of_edge` (default 50%) of the calibrated edge. Use the crossing price (not the stale external price) for Kelly sizing.
7. **Liquidity / depth-aware position cap** — position is capped at `max_position_pct_liquidity` × on-book liquidity (default 5%) and 20% of top-of-book depth.
8. **Time-decay sizing** — multiply final position by `sqrt(days_to_resolve / 30)`, capped at 1.0, so a 7-day market takes ~48% of a 30-day-equivalent position.

9. **Tradable-price band** — skip markets with crossing price outside `min_price`..`max_price` (defaults 3%..97%) to avoid favorite/longshot tails where calibration degrades.
10. **Minimum expected edge in dollars** — require `position_size × edge >= min_expected_profit_usd` (default $0.10) so tiny, noisy bets are skipped.

Together these typically cut trade count by 30–60% but raise per-trade expected value materially. All knobs can be tuned or turned off (`SIMMER_DIVERGENCE_ENABLE_SPREAD_CHECK=0`, etc.) for traders who want v2.3 behavior.

## What's new in v2.5 (execution + calibration upgrade)

9. **Source-aware calibration** — distinct shrinkage per signal source (`oracle_shrinkage=0.65`, `crowd_shrinkage=0.80`) because AI-oracle and crowd-flow signals have different error profiles.
10. **Longshot-bias penalty** — optional additional edge haircut on low-probability contracts (`longshot_threshold=0.15`, `longshot_penalty_bps=75`) to avoid structurally expensive tails.

## What It Does

1. **Scans** all active markets for AI vs market price divergence
2. **Calibrates** by shrinking raw divergence toward zero to correct for AI overconfidence
3. **Filters** to markets with calibrated edge above threshold (default 3%), zero fees, sufficient liquidity / volume, and a reasonable time-to-resolution band
4. **Checks** safeguards (flip-flop detection, existing positions, spread, top-of-book depth, sanity caps)
5. **Sizes** using fractional Kelly (cap 0.20), capped at 5% of liquidity & 20% of top-of-book, time-decayed by `√(days/30)`
6. **Executes** trades on the mispriced side using the actual orderbook crossing price (YES when AI is bullish, NO when bearish)

## Setup Flow

When user asks to install or configure this skill:

1. **Install the Simmer SDK**
   ```bash
   python -m pip install "simmer-sdk>=0.11.1"
   ```

2. **Ask for Simmer API key**
   - They can get it from simmer.markets/dashboard → SDK tab
   - Store in environment as `SIMMER_API_KEY`

3. **Ask for wallet private key** (only for external-wallet self-custody trading)
   - This is the private key for their Polymarket wallet (the wallet that holds USDC)
   - Store in environment as `WALLET_PRIVATE_KEY`
   - The SDK uses this to sign orders client-side automatically — no manual signing needed
   - Not needed for managed wallets or $SIM paper trading on the Simmer venue

## Quick Commands

```bash
# Scan only (dry run, no trades)
python ai_divergence.py

# Scan + execute trades
python ai_divergence.py --live

# Only show bullish divergences
python ai_divergence.py --bullish

# Only >15% divergence
python ai_divergence.py --min 15

# JSON output
python ai_divergence.py --json

# Cron mode (quiet, trades only)
python ai_divergence.py --live --quiet

# Show config
python ai_divergence.py --config

# Update config
python ai_divergence.py --set max_bet_usd=10
```

## Configuration

| Key | Env Var | Default | Description |
|-----|---------|---------|-------------|
| `min_divergence` | `SIMMER_DIVERGENCE_MIN` | 5.0 | Min divergence % for scanner display |
| `min_edge` | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.03 | Min calibrated edge to trade after shrinkage + fees |
| `max_bet_usd` | `SIMMER_DIVERGENCE_MAX_BET_USD` | 5.0 | Max bet per trade |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES_PER_RUN` | 3 | Max trades per cycle |
| `kelly_cap` | `SIMMER_DIVERGENCE_KELLY_CAP` | 0.20 | Fractional Kelly cap |
| `daily_budget` | `SIMMER_DIVERGENCE_DAILY_BUDGET_USD` | 25.0 | Daily spend limit |
| `default_direction` | `SIMMER_DIVERGENCE_DIRECTION_FILTER` | (both) | Filter: "bullish" or "bearish" |
| `ai_shrinkage` | `SIMMER_DIVERGENCE_AI_SHRINKAGE` | 0.70 | Multiplier on raw AI − market divergence |
| `min_liquidity_usd` | `SIMMER_DIVERGENCE_MIN_LIQUIDITY_USD` | 1000 | Min Polymarket on-book liquidity (USD) |
| `min_volume_24h_usd` | `SIMMER_DIVERGENCE_MIN_VOLUME_24H_USD` | 500 | Min 24h volume (USD) |
| `max_position_pct_liquidity` | `SIMMER_DIVERGENCE_MAX_POS_PCT_LIQ` | 0.05 | Max position as fraction of market liquidity |
| `min_hours_to_resolve` | `SIMMER_DIVERGENCE_MIN_HOURS_TO_RESOLVE` | 6 | Skip markets resolving within this many hours |
| `max_days_to_resolve` | `SIMMER_DIVERGENCE_MAX_DAYS_TO_RESOLVE` | 180 | Skip markets beyond this many days |
| `max_divergence_sanity` | `SIMMER_DIVERGENCE_MAX_DIV_SANITY` | 0.40 | Skip suspiciously extreme divergences |
| `max_spread_pct_of_edge` | `SIMMER_DIVERGENCE_MAX_SPREAD_PCT_EDGE` | 0.50 | Skip if half-spread > this share of edge |
| `enable_spread_check` | `SIMMER_DIVERGENCE_ENABLE_SPREAD_CHECK` | 1 | 1 = check CLOB spread; 0 = skip |
| `enable_time_decay` | `SIMMER_DIVERGENCE_ENABLE_TIME_DECAY` | 1 | 1 = sqrt(days/30) sizing; 0 = constant |
| `min_price` | `SIMMER_DIVERGENCE_MIN_PRICE` | 0.03 | Skip trades below this crossing price (longshot tail) |
| `max_price` | `SIMMER_DIVERGENCE_MAX_PRICE` | 0.97 | Skip trades above this crossing price (favorite tail) |
| `min_expected_profit_usd` | `SIMMER_DIVERGENCE_MIN_EXPECTED_PROFIT_USD` | 0.10 | Minimum `size × edge` before a trade is allowed |
| `enable_adaptive_shrinkage` | `SIMMER_DIVERGENCE_ENABLE_ADAPTIVE_SHRINKAGE` | 1 | 1 = volatility/liquidity-aware shrinkage of AI edge |
| `adaptive_shrinkage_vol_mult` | `SIMMER_DIVERGENCE_ADAPTIVE_SHRINK_VOL_MULT` | 1.25 | Liquidity stress multiplier used by adaptive shrinkage |
| `oracle_shrinkage` | `SIMMER_DIVERGENCE_ORACLE_SHRINKAGE` | 0.65 | Shrinkage for `signal_source=oracle` |
| `crowd_shrinkage` | `SIMMER_DIVERGENCE_CROWD_SHRINKAGE` | 0.80 | Shrinkage for `signal_source=crowd` |
| `longshot_threshold` | `SIMMER_DIVERGENCE_LONGSHOT_THRESHOLD` | 0.15 | Contracts below this price are treated as longshots |
| `longshot_penalty_bps` | `SIMMER_DIVERGENCE_LONGSHOT_PENALTY_BPS` | 75 | Extra edge haircut for longshots (bps) |
| `slippage_buffer_pct` | `SIMMER_DIVERGENCE_SLIPPAGE_BUFFER_PCT` | 0.01 | Conservative execution-cost buffer subtracted from edge before Kelly |
| `min_top_book_depth_usd` | `SIMMER_DIVERGENCE_MIN_TOP_BOOK_DEPTH_USD` | 250 | Skip when top-of-book depth is too thin for reliable fills |
| `category_multipliers_csv` | `SIMMER_DIVERGENCE_CATEGORY_MULTIPLIERS` | `politics=0.60,crypto=0.60,sports=0.85,default=0.75` | Per-category Kelly multipliers |
| `enable_category_multiplier` | `SIMMER_DIVERGENCE_ENABLE_CATEGORY_MULTIPLIER` | 1 | 1 = apply category multipliers; 0 = treat all the same |

Update via CLI: `python ai_divergence.py --set max_bet_usd=10`

## How It Works

### Divergence Signal

Each imported market has two prices:
- **AI consensus** (`current_probability`) — Simmer's AI consensus price, derived from multi-model ensemble forecasting
- **External price** (`external_price_yes`) — Real market price on Polymarket/Kalshi

```
raw_divergence  = AI consensus - external price
source_shrink   = oracle_shrinkage | crowd_shrinkage | ai_shrinkage
effective_shrink= source_shrink × adaptive market-quality multipliers
calibrated_edge = raw_divergence × effective_shrink
tradeable_edge  = calibrated_edge − fee_pct − slippage_buffer_pct − optional_longshot_penalty
```
We trade only when `|tradeable_edge| ≥ min_edge` (default 3%).

When calibrated edge > 0 → buy YES. When calibrated edge < 0 → buy NO.

### Kelly Sizing

Position size uses the fractional Kelly criterion on the calibrated edge:
```
kelly_fraction = tradeable_edge / (1 - crossing_price)
size           = clamp(kelly_fraction, 0, kelly_cap) * max_bet_usd
size           = min(size,
                     max_position_pct_liquidity * gamma_liquidity,
                     0.20 * top_of_book_depth_usd)
size          *= sqrt(days_to_resolve / 30)              # capped at 1.0
```
Capped at `kelly_cap` (default 0.20). Research consistently shows that full Kelly fails under estimation error — quarter / fifth Kelly is industry standard for AI-driven strategies.

### Fee Filtering

75% of Polymarket markets have 0% fees. The remaining 25% charge 10% (short-duration crypto/sports). The skill subtracts the fee from the calibrated edge and skips trades where the residual falls below `min_edge`, so fee-heavy markets are filtered automatically.

### Safeguards (v2.5)

- **Fee + slippage check**: Skips when calibrated edge − fee − slippage buffer < `min_edge`
- **Flip-flop detection**: Uses SDK's context API to detect contradictory trades
- **Position check**: Skips markets where you already hold a position
- **Daily budget**: Stops trading when daily spend limit is reached
- **Source/adaptive calibration shrinkage**: Multiplies raw divergence by source and market-quality shrinkage to correct for systematic AI overconfidence
- **Longshot penalty**: Haircuts low-price contracts before Kelly sizing
- **Liquidity + volume floors**: Skips polymarket-sourced markets below thresholds (stale prices, no execution)
- **Time-to-resolution band**: Skips < 6h (terminal volatility / oracle risk) and > 180d (capital lock-up)
- **Sanity divergence cap**: Skips raw divergences > 40% (almost always stale data / broken oracle)
- **CLOB spread guard**: Skips when half-spread > 50% of edge; uses real crossing price for Kelly
- **Top-of-book depth floor + depth-aware sizing**: Requires sufficient depth, then caps at 5% of book liquidity and 20% of top-of-book depth
- **Time-decay sizing**: `position × sqrt(days_to_resolve / 30)` so near-term bets shrink automatically

## API Endpoints Used

- `GET /api/sdk/markets/opportunities` — Divergence-ranked market list
- `GET /api/sdk/context/{market_id}` — Fee rate and safeguards per market
- `POST /api/sdk/trade` — Trade execution (via SDK client)
- `GET /api/sdk/positions` — Current portfolio positions

## Troubleshooting

**"No markets above min edge threshold"**
→ All divergences are below the `min_edge` setting. Lower it with `--set min_edge=0.01` or wait for larger divergences.

**"Daily budget exhausted"**
→ The skill has hit its daily spend limit. Adjust with `--set daily_budget=50`.

**All markets skipped for fees**
→ Only zero-fee markets are traded. If all available divergence opportunities have fees, no trades execute. This is by design.

**"context fetch failed"**
→ The SDK context endpoint is rate-limited (18 req/min). If running frequently, reduce `max_trades_per_run`.
