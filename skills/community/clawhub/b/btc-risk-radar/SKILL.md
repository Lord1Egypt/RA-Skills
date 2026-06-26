---
name: btc-risk-radar
description: Professional BTC risk radar using public options, perp, and spot data. Use when the user wants a clear Bitcoin risk snapshot with volatility/skew context, panic or black-swan validation, timestamped evidence, confidence scoring, and explicit caveats for traders or advanced observers.
---

# BTC Risk Radar

Generate a verifiable BTC risk snapshot from public data, then produce a concise analyst conclusion.

This skill is a **read-only heuristic risk-state framework**, not a full institutional analytics stack. Several fields are deliberate **proxies / approximations** and must be presented as such.

## Workflow

1. Run `scripts/btc_risk_radar.py` to collect current public data and compute metrics.
2. Read JSON output first; treat it as the source of truth.
3. Explain conclusions with explicit confidence, caveats, and data gaps.
4. Avoid deterministic predictions; present risk state (GREEN/AMBER/RED) and trigger reasons.
5. If venue coverage is partial, keep going and surface degraded confidence rather than pretending coverage is complete.

## Quick Audit Path

For a fast review:

1. Run `python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --sources`
2. Run `python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --json`
3. Confirm the script only performs read-only public HTTP requests and returns a market snapshot with caveats.
4. Verify that proxy metrics and partial-data conditions are explicitly disclosed in output.

## Commands

```bash
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --json
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --sources
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --version
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --prompt "用户问题"
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --lang en
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --lang zh
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --horizon-hours 72
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --event-mode high-alert
python3 skills/btc-risk-radar/scripts/btc_risk_radar.py --audience beginner --lang zh
```

## Safety / Scope Boundary

- Read-only skill: query public market APIs only.
- Use no authentication, cookies, API keys, private accounts, or wallet access.
- Execute no trades, place no orders, and mutate no exchange state.
- Write no files and send no external messages as part of normal use.
- Produce analysis only; not investment advice.

## Output Policy

- Default language behavior: `auto`.
- If `--lang auto` and the prompt contains Chinese, switch final narrative to Chinese.
- If `--lang auto` and no Chinese is detected, use English.
- `--json` output is language-neutral.
- Always include:
  - `as_of_utc`
  - key metrics (ATM IV, RR25, RR15, put-volume proxy, funding, basis)
  - `availability`
  - `data_gaps`
  - `degraded_mode`
  - 72h validation matrix (`validation_72h`)
  - confidence (`confidence.score`, `confidence.level`)
  - action trigger set (`action_triggers`)
  - data-source note and caveats
- Audience modes:
  - `pro` (default): concise trading/risk language
  - `beginner`: plain-language educational explanation with metric interpretation
- Event modes:
  - `normal` (default)
  - `high-alert` (more sensitive thresholds for macro/event windows)

## Interpretation Guardrails

- `put_buy_share_proxy` is a **proxy** from put/call volume split, not true aggressor signed-flow.
- RR and ATM IV are computed from front-expiry delta-nearest options; this is robust but may differ from proprietary dashboards.
- Funding regime is an aggregated public snapshot, not a full term-structure model.
- RED means elevated downside risk pricing, not guaranteed crash.
- Partial venue failure should lower confidence, not silently disappear from the narrative.

## Data Sources (public)

- Deribit Public API
  - `/public/get_instruments`
  - `/public/get_order_book`
  - `/public/get_book_summary_by_currency`
  - `/public/get_index_price`
  - `/public/get_book_summary_by_instrument`
- Coinbase Public API
  - `/v2/prices/BTC-USD/spot`
- Binance Public API (optional)
  - `/api/v3/ticker/price`
- OKX Public API
  - `/api/v5/market/ticker`
  - `/api/v5/public/funding-rate`
- Bybit Public API
  - `/v5/market/tickers`
