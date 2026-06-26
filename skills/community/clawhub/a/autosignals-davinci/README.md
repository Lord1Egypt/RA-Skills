# AutoSignals - Autonomous Trading Signal Optimization

Autonomous research loop that continuously optimizes trading signal algorithms through agent-driven experimentation.

## Description

AutoSignals is an adaptation of Andrej Karpathy's autoresearch pattern for trading signal optimization. An autonomous loop runs continuously, spawning agents to modify signal logic in `signals.py`, backtesting changes against 5 years of S&P 500 data, and keeping improvements. The system maintains a single modifiable file (signals.py) while using a fixed evaluation engine to prevent overfitting.

## Key Features

- **Autonomous loop** - Runs continuously, spawning agents for each experiment
- **Single modification point** - Agents can only edit `signals.py` (factor weights, thresholds, indicators)
- **Fixed evaluation** - `backtest.py` remains constant to ensure fair comparison
- **Composite scoring** - Balances Sharpe ratio, max drawdown, win rate, CAGR
- **Experiment logging** - Full JSONL log of all attempts, outcomes, and code changes
- **Status monitoring** - Real-time view of best score, experiment count, recent performance
- **Automatic rollback** - Bad experiments are discarded, only improvements persist

## Quick Start

```bash
# Check loop status
bash /Users/clawdiri/Projects/autosignals/status.sh

# Start autonomous loop
bash /Users/clawdiri/Projects/autosignals/start.sh

# Stop the loop
kill $(cat /Users/clawdiri/Projects/autosignals/autosignals.pid)

# View recent experiments
tail -20 /Users/clawdiri/Projects/autosignals/experiments.jsonl

# View best-performing signal version
cat /Users/clawdiri/Projects/autosignals/signals.py
```

**Status output shows:**
- Current running state (PID, uptime)
- Best composite score achieved
- Total experiments run
- Last 10 experiments with accept/reject status
- Score trend (last 20 experiments)

## Architecture

- **signals.py** - Modifiable signal logic (agents edit this)
- **backtest.py** - Fixed evaluation engine (5-year S&P 500 backtest)
- **prepare.py** - Data download and preprocessing
- **program.md** - Instructions for research agents
- **run.py** - Autonomous loop controller
- **experiments.jsonl** - Complete experiment history

## What It Does NOT Do

- Does NOT execute live trades (research environment only)
- Does NOT guarantee profitable signals (experimental optimization)
- Does NOT prevent overfitting without proper out-of-sample validation
- Does NOT work with options, futures, or crypto (equity-focused)
- Does NOT run without agent access (requires LLM or code generation capability)

## Requirements

- Python 3.9+
- pandas, yfinance, numpy, scipy
- Agent access (OpenAI, Anthropic, or local code generation)
- Sufficient compute for continuous backtesting

## License

MIT
