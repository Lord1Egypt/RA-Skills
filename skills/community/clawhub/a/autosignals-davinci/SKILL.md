---
id: 'autosignals'
name: 'AutoSignals - Autonomous Trading Signal Optimization'
description: 'Monitors and controls the AutoSignals autonomous research loop.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# AutoSignals - Autonomous Trading Signal Optimization

Monitors and controls the AutoSignals autonomous research loop.

## What It Is

AutoSignals is an adaptation of Karpathy's autoresearch pattern for trading signal optimization. An autonomous loop runs continuously, spawning sub-agents to modify `signals.py`, backtesting changes, and keeping improvements.

**Architecture:**
- `signals.py` — The ONE file agents can modify (factor weights, thresholds, indicators, scoring)
- `backtest.py` — Fixed evaluation engine (5-year backtest, composite score metric)
- `prepare.py` — Data download (S&P 500 + held tickers)
- `program.md` — Instructions for research agents
- `run.py` — Autonomous loop controller
- `experiments.jsonl` — Full experiment log

**Location:** `/Users/clawdiri/Projects/autosignals/`

## How to Use

### Check Status

```bash
bash /Users/clawdiri/Projects/autosignals/status.sh
```

Shows:
- Running status (PID, uptime)
- Best composite score achieved
- Total experiments run
- Last 10 experiments with outcomes
- Score trend (last 20)
- Any errors

### Start the Loop

```bash
bash /Users/clawdiri/Projects/autosignals/start.sh
```

Starts the autonomous loop in the background. Runs forever until stopped.

### Stop the Loop

```bash
kill $(cat /Users/clawdiri/Projects/autosignals/autosignals.pid)
```

### View Logs

```bash
tail -f /Users/clawdiri/Projects/autosignals/logs/autosignals.log
```

### View Best Signals

```bash
cat /Users/clawdiri/Projects/autosignals/best_score.json
```

Then read the corresponding commit:

```bash
cd /Users/clawdiri/Projects/autosignals
git show <commit_hash>:signals.py
```

### Monitoring Script (for DaVinci heartbeats)

```bash
bash /Users/clawdiri/Projects/autosignals/monitor.sh
```

Returns JSON with:
- `running`: bool
- `experiment_count`: int
- `best_score`: float
- `best_commit`: str
- `trend`: "improving" | "declining" | "flat"
- `errors`: list of recent errors

## Evaluation Metric

```
composite_score = (0.35 * sharpe_normalized) + 
                  (0.25 * (1 - max_drawdown)) + 
                  (0.20 * win_rate) + 
                  (0.20 * profit_factor_normalized)
```

All components normalized to [0, 1].

**Baseline targets:**
- Sharpe: 1.57 / 1.46 / 1.24
- Starting weights: 40% Insider / 35% Earnings / 25% Sector Rotation

**Good:** Beat baseline
**Great:** Sharpe > 2.0, drawdown < 15%
**Exceptional:** Sharpe > 2.5, drawdown < 10%

## Data

- **Price data:** 5 years daily OHLCV for S&P 500 + META, GOOG, AMZN, TSLA, BTC-USD, IAU
- **Factor data:** Currently mock (insider, earnings, sector). Can be enhanced with real API data.
- **Cache:** `/Users/clawdiri/Projects/autosignals/data/prices.parquet`

Refresh data:

```bash
cd /Users/clawdiri/Projects/autosignals
source .venv/bin/activate
python prepare.py
```

## Design Principles (from Karpathy)

1. **Single modifiable file** — agents only edit `signals.py`
2. **Fixed evaluation** — `backtest.py` is immutable truth
3. **Self-contained** — no external API calls during backtest (cached data only)
4. **Git-tracked progress** — every improvement is a commit
5. **Resilient loop** — individual failures don't stop the system

## Alert Conditions (for DaVinci)

- Loop stopped unexpectedly → WhatsApp alert
- No experiments in last 30 minutes (if running) → check logs
- Error rate > 50% (last 10 experiments) → investigate
- New best score achieved → celebrate 🎉

## When to Intervene

**Hands-off:**
- Normal operation (experiments running, mix of keep/discard)
- Gradual improvement trend
- Low error rate

**Check it out:**
- All experiments failing (agent spawn issues? data corruption?)
- Score trend declining over 20+ experiments (overfitting? bad hypothesis?)
- Loop stopped (crash? resource exhaustion?)

**Celebrate:**
- New all-time best score
- Sharpe > 2.0 achieved
- Major breakthrough (e.g., 10%+ score improvement)

## Future Enhancements

- Real factor data integration (Finnhub insider API, FMP earnings, sector ETF momentum)
- Multi-ticker portfolio optimization (vs current single-ticker signals)
- Walk-forward validation (rolling window backtest to prevent overfitting)
- Ensemble signals (combine multiple top-performing signal variants)
- Risk-adjusted position sizing (Kelly criterion, volatility targeting)
- Live paper trading integration (Alpaca API)
