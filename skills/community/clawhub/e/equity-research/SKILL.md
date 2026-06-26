---
name: equity-research
description: "Run a full equity research report on a stock by executing three local scripts with uv run. Read this skill file for exact commands. Do NOT use sessions_spawn or web search."
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":["uv"]}}}
---

# Skill: Equity Research

## When to use
- The user wants a full breakdown or deep dive on a stock.
- The user wants to make a buy/sell/hold decision and needs all signals in one place.
- The user asks "tell me everything about [ticker]" or "give me a full report on [company]".
- The user wants comprehensive equity research combining price, fundamentals, and market sentiment.

## When NOT to use
- The user only wants the current price or daily movement → use `stock-price-checker-pro`
- The user only wants fundamentals (P/E, EPS, margins) → use `stock-fundamentals`
- The user only wants recent news headlines → use `market-news-brief`

## Commands

This skill orchestrates three sub-skills. Run all three commands for the same ticker, then synthesize the results into a unified report.

### Step 1 — Current price, ranges, and upcoming events

```bash
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py <TICKER>
```

### Step 2 — Fundamentals (valuation, profitability, balance sheet)

```bash
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>
```

### Step 3 — Broad market news and sentiment

```bash
# For US-listed stocks
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py US

# For German/European stocks (e.g. RHM.DE, SAP.DE, ASML.AS)
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py EUROPE

# For Japanese stocks (e.g. 7203.T)
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py JAPAN

# For Korean stocks (e.g. 005930.KS)
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py SOUTH_KOREA
```

> ⚠️ `market-news-brief` takes a **market scope word** (`US`, `EUROPE`, `ASIA`, `GLOBAL`, `UK`, `GERMANY`, `NETHERLANDS`, `JAPAN`, `SOUTH_KOREA`).
> Do NOT pass a bare company ticker like `AAPL` or `RHM.DE` — it will error.
> Use `US` for US-listed equities, `EUROPE` for European stocks, `GLOBAL` for a worldwide macro backdrop.

### Full example — Apple (US)

```bash
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py AAPL
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py AAPL
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py US
```

### Full example — Rheinmetall (Germany)

```bash
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py RHM.DE
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py RHM.DE
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py EUROPE
```

### Full example — NVIDIA (US)

```bash
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py NVDA
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py NVDA
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py US
```

## Report Structure

After running all three commands, synthesize the results into a structured report:

1. **Price Snapshot** — current price, daily change, volume, 52W range, upcoming events
2. **Fundamentals Summary** — valuation multiples, profitability margins, debt profile, analyst target
3. **Market Context** — macro tone for the relevant region, dominant themes, key headlines
4. **Overall Take** — a brief synthesized assessment combining all three signals (bullish / neutral / bearish and why)

## Notes

- Always run all three sub-skills before writing the report — partial data leads to incomplete conclusions.
- Each sub-skill uses `uv run` internally — no manual pip install or environment setup needed.
- Do NOT attempt to fetch any of this data via web search or curl — always use the commands above.
- Do NOT use the `.sh` wrapper scripts — call `uv run src/main.py` directly as shown in the examples.
- `uv run` reads the inline `# /// script` dependency block in each `main.py` and auto-installs `yfinance` — no pip or venv setup needed.
- Ticker symbols must be valid Yahoo Finance tickers. See TOOLS.md for the full ticker format reference by exchange.