---
name: commodities
description: "Fetch commodity prices for WTI (Crude Oil), Brent, Natural Gas, and Gold using Yahoo Finance (yfinance). Follow the same pattern as stock-price-checker-pro."
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"🛢️","requires":{"bins":["uv"]}}}
---

# Skill: Commodities

## When to use
- The user asks for current commodity prices (WTI, Brent, Natural Gas, Gold).
- The user wants daily change, percent change, recent high/low ranges, or recent headlines affecting these commodities.

## When NOT to use
- User wants equities, fundamentals, or portfolio-level analysis — use the stock skills instead.

## Authentication
- No API key required. Uses Yahoo Finance via `yfinance`.

## Commands

### Check a commodity price

```bash
uv run skills/commodities/src/main.py <SYMBOL>
```

### Examples

```bash
uv run skills/commodities/src/main.py CL=F   # WTI Crude Futures (WTI)
uv run skills/commodities/src/main.py BZ=F   # Brent Crude Futures (Brent)
uv run skills/commodities/src/main.py NG=F   # Natural Gas Futures (NG)
uv run skills/commodities/src/main.py GC=F   # Gold Futures (GC)
```

## Ticker Reference (Yahoo Finance)

| Commodity       | Yahoo Ticker |
|-----------------|--------------|
| WTI Crude Oil   | `CL=F`       |
| Brent Crude     | `BZ=F`       |
| Natural Gas     | `NG=F`       |
| Gold Futures    | `GC=F`       |

## Output
- Current price, daily change & % change
- Previous close
- Today's high / low
- 2W, 1M, 3M, 6M, 52W high / low ranges
- Recent headlines (when available)

## Notes
- `uv run` reads the inline `# /// script` dependency block in `main.py` and auto-installs `yfinance`.
- Do NOT use web search or curl for these prices — use this script for consistent formatting.
