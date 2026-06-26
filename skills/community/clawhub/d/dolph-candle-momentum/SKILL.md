---
name: polymarket-candle-momentum
description: Trade Polymarket 5-minute crypto fast markets using 1-minute candle body analysis and volume surge detection from Binance. Scans BTC, ETH, SOL, XRP, BNB simultaneously and picks the strongest signal each cycle. Enters when the last candle has a strong body (>60% of range) confirmed by a volume spike (>1.5x average). Backtested at 86%+ win rate over 3 months.
metadata:
  author: "Mibayy"
  version: "1.6.4"
  displayName: "Polymarket Candle Momentum"
  difficulty: "intermediate"
---

# Polymarket Candle Momentum

Trade Polymarket 5-minute crypto fast markets using **candle body analysis** and **volume surge detection** from Binance. A stronger, data-driven alternative to simple momentum signals.

> **This is a template.** The default signal uses Binance 1-minute candle structure (body/range ratio + volume surge). Remix it with your own thresholds, additional indicators, or alternative data sources. The skill handles all the plumbing (market discovery, import, trade execution). Your agent provides the alpha.

> Fast markets carry Polymarket's 10% fee (`is_paid: true`). The default thresholds are calibrated to maintain edge after fees.

## The Signal

Most fast-market skills use simple price momentum (did price go up or down?). This skill looks at **how** price moved:

1. **Candle Body Ratio** - Measures the last 1-minute candle's body size relative to its full range. A body ratio > 60% means a decisive move with minimal wicks (strong conviction, not noise).

2. **Volume Surge** - Confirms the move with volume. The last candle's volume must be > 1.5x the average of the previous 3 candles. High volume + strong body = real move, not a fake-out.

3. **Direction Alignment** - Body direction (bullish/bearish) must align with the 5-minute momentum direction.

### Why This Works Better

Simple momentum catches every wiggle. Candle body analysis filters for **quality** moves:
- A 0.5% move on a doji candle (long wicks, tiny body) = noise. Skip.
- A 0.3% move on a marubozu candle (90% body, no wicks) = conviction. Trade.

Backtested on BTC/ETH/SOL/XRP/BNB (3 months, 6131 five-minute slots):
- `body > 65% + volume > 1.5x`: **86.3% win rate** (N=292)
- `body > 60% + volume > 1.5x`: **84.7% win rate** (N=333)

## Setup

**pip dependencies:** `simmer-sdk`, `requests`

**Environment variables:**
- `SIMMER_API_KEY` (required) - get from simmer.markets/dashboard

No other credentials needed. The script only reads `SIMMER_API_KEY` from the environment. All trades go through `SimmerClient.trade()` - no wallet private key, no direct CLOB access.

```bash
export SIMMER_API_KEY="your_key_here"

# Dry run (default, no trades placed)
python candle_momentum.py

# Live trading via SimmerClient
python candle_momentum.py --live

# Quiet mode for cron
python candle_momentum.py --live --quiet
```

## How to Run on a Loop

The script runs one cycle. Set up a cron (every 2 min recommended for 5min markets):

```bash
*/2 * * * * cd /path/to/skill && SIMMER_API_KEY=your_key python candle_momentum.py --live --quiet
```

## Security Notes

- Only `SIMMER_API_KEY` is read from environment. Nothing else.
- No host files are read. No logs written outside the script's own stdout.
- `automaton.managed` is `false` - the skill does not auto-execute.
- Dry-run by default. `--live` must be passed explicitly.

## Trade Execution Path

1. Fetches Binance public klines (no auth) for BTC, ETH, SOL, XRP, BNB
2. Scans all 5 assets, picks strongest signal (body_ratio x vol_surge score)
3. Finds matching Polymarket fast market via `SimmerClient`
4. If `--live`: calls `SimmerClient.trade()` with side, amount, reasoning
5. If dry-run: logs the signal, no trade placed

## Configuration

Via environment variables only (no local file persistence):

```bash
python candle_momentum.py --set body_threshold=0.65
python candle_momentum.py --set asset=ETH
python candle_momentum.py --set vol_threshold=2.0
```

### Settings

| Setting | Default | Env Var | Description |
|---|---|---|---|
| `body_threshold` | 0.60 | `CM_BODY_THRESHOLD` | Min candle body/range ratio (0-1) |
| `vol_threshold` | 1.5 | `CM_VOL_THRESHOLD` | Min volume surge vs 3-candle average |
| `max_position` | 5.0 | `CM_MAX_POSITION` | Max USD per trade |
| `assets` | BTC,ETH,SOL,XRP,BNB | - | Assets to scan (picks best signal) |
| `asset` | BTC | `CM_ASSET` | Single asset override (ignores `assets`) |
| `window` | 5m | `CM_WINDOW` | Market window (5m or 15m) |
| `min_time_remaining` | 60 | `CM_MIN_TIME` | Skip markets with less time (seconds) |
| `lookback_candles` | 3 | `CM_LOOKBACK` | Candles for volume average |
| `entry_threshold` | 0.05 | `CM_ENTRY_THRESHOLD` | Min price divergence from 50c |

## CLI Options

```bash
python candle_momentum.py                    # Dry run
python candle_momentum.py --live             # Real trades
python candle_momentum.py --live --quiet     # Silent mode
python candle_momentum.py --positions        # Show open positions
python candle_momentum.py --config           # Show config
python candle_momentum.py --set KEY=VALUE    # Update config
```

## Remix Ideas

The candle body + volume signal is just the starting point. Ideas:

- **Multi-timeframe**: Confirm 1m signal with 5m candle structure
- **Wick analysis**: Filter out candles with long upper wicks (rejection)
- **RSI filter**: Skip overbought/oversold conditions
- **Multi-exchange**: Compare candle patterns across Binance + Coinbase
- **Order flow**: Add Polymarket CLOB depth as confirmation

To customize, edit `get_candle_signal()` in `candle_momentum.py`.

## Example Output

```
  Polymarket Candle Momentum Trader
==================================================
  [DRY RUN] Use --live to enable trading.

  Configuration:
  Asset:           BTC
  Body threshold:  0.60 (min candle body ratio)
  Vol threshold:   1.5x (min volume surge)
  Max position:    $5.00

  Discovering BTC fast markets...
  Found 3 active fast markets

  Selected: Bitcoin Up or Down - Mar 19, 10:30-10:35AM ET
  Expires in: 210s
  Current YES price: $0.490

  Fetching BTC candle data (binance)...
  Last candle: O=84250 H=84312 L=84245 C=84305
  Body ratio: 0.90 (strong!)
  Direction: BULLISH
  Volume surge: 2.3x avg

  Signal: BUY YES (body=0.90, vol=2.3x, direction=UP)
  Divergence: 5c (YES at 0.49, expected ~0.54)

  [DRY RUN] Would buy $5.00 YES
```

## Source

All trades tagged with `source: "sdk:candle-momentum"` for portfolio tracking.
