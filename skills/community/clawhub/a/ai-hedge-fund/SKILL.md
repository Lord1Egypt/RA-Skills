---
name: ai-hedge-fund
description: Run an AI-powered hedge fund simulation with 16+ legendary investor agents. Each agent analyzes stocks from their unique investment philosophy. Auto-detects model from current OpenClaw session, no hardcoding. Uses yfinance for free financial data. Based on github.com/virattt/ai-hedge-fund.
---

# AI Hedge Fund Skill

Multi-agent investment analysis using legendary investor personas.

**Project:** https://github.com/virattt/ai-hedge-fund

## Setup (first time)

```bash
# Clone project
git clone https://github.com/virattt/ai-hedge-fund /data/workspace/ai-hedge-fund

# Install
pip install -e /data/workspace/ai-hedge-fund --break-system-packages --quiet
pip install yfinance --break-system-packages --quiet
```

## Run

Via skill script (auto-detects model):

```bash
python3 /data/workspace/skills/skills/ai-hedge-fund/scripts/run.py \
  --tickers NVDA \
  --analysts-all \
  --show-reasoning
```

Or direct CLI:

```bash
cd /data/workspace/ai-hedge-fund
python3 src/main.py \
  --tickers NVDA \
  --start-date 2026-01-01 \
  --end-date 2026-04-12 \
  --model "minimax/minimax-m2.5:free" \
  --analysts-all \
  --show-reasoning
```

## Model Auto-Detection

**Not hardcoded.** The run.py script auto-detects from:

1. `$OPENCLAW_LLM_MODEL` environment variable
2. OpenClaw config (`/root/.openclaw/openclaw.json`)
3. Default: `minimax/minimax-m2.5:free`

You can also specify manually via `--model` flag.

## Available Models

Any model from `src/llm/api_models.json`, e.g.:

- `minimax/minimax-m2.5:free` (default, free)
- `qwen/qwen3.6-plus:free` (free)
- `gpt-4.1` (OpenAI)
- `claude-sonnet-4-6` (Anthropic)

## All 16+ Agents

| Agent | Philosophy |
|-------|------------|
| Warren Buffett | Wonderful business at fair price |
| Charlie Munger | Only wonderful businesses |
| Ben Graham | Margin of safety |
| Michael Burry | Contrarian deep value |
| Cathie Wood | Innovation & disruption |
| Bill Ackman | Activist investor |
| Peter Lynch | Ten-baggers |
| Phil Fisher | Scuttlebutt |
| Stanley Druckenmiller | Macro asymmetric |
| Nassim Taleb | Antifragility |
| Mohnish Pabrai | Dhandho |
| Rakesh Jhunjhunwala | Big Bull |
| Aswath Damodaran | Valuation |
| + Quant agents | Fundamentals, Technical, Valuation, Sentiment |

## Output

Each agent outputs: signal (bullish/bearish/neutral), confidence %, reasoning.
Portfolio Manager aggregates into final BUY/SELL/HOLD.

## Data Source

yfinance (free, no API key needed)