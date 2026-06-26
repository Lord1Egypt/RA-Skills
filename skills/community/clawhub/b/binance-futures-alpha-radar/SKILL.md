---
name: binance-futures-strategy-analysis
description: Analyze Binance USDT-margined perpetual futures symbols with public futures market data only and return a structured market analysis report with a clear BUY, SELL, or HOLD recommendation without placing orders. Use when the user asks for buy/sell analysis, trade strategy, long/short judgment, setup review, support and resistance analysis, or detailed futures market commentary for symbols like BTC, ETH, SOL on Binance futures, explicitly wants contract data instead of spot data, or wants decisions generated under the repo's system-prompt trading rules.
---

# Binance Futures Strategy Analysis

## Overview

Use this skill to produce strategy decisions for Binance U-margined perpetual contracts from public market data only. Do not place orders, do not call any private API, and do not use spot market data.

## Workflow

1. Read the canonical strategy source at `../../../src/main/resources/system-prompt.txt`.
2. Read `references/system-prompt-coverage.md` before analysis. It mirrors the canonical rules in skill-friendly form and includes the analysis-only output adaptation.
3. Read `../../../docs/core-feature-spec.md` only if you need the project's original execution flow and field semantics.
4. Read `references/analysis-mode.md` before deciding, because this skill runs in analysis-only mode instead of live execution mode.
5. Normalize user input symbols to Binance USDT perpetual symbols:
   - `BTC` -> `BTCUSDT`
   - `ETH` -> `ETHUSDT`
   - `BTCUSDT` stays `BTCUSDT`
6. Run `python3 scripts/binance_futures_snapshot.py <SYMBOL...>` with the user symbols.
7. Use the script output as the only market data source unless the user gives additional account context.
8. Apply the strategy rules from `system-prompt.txt` exactly. Do not simplify the decision logic just because this skill is analysis-only.
9. Build the internal decision object in the canonical schema first, then render it as a human-readable structured report unless the user explicitly asks for raw JSON.

## Analysis Mode Rules

- Default to analysis-only assumptions when the user gives only symbols:
  - `equity_usdt = 10000`
  - `free_usdt = 10000`
  - `positions = []`
  - `cooldown_ok = true`
- Replace those defaults if the user provides account equity, free balance, cooldown status, or current positions.
- Because there is no live position context by default:
  - Use `BUY`, `SELL`, or `HOLD`.
  - Do not emit `ADD`, `REDUCE`, or `CLOSE` unless the user explicitly supplies an existing position.
- Still fill every required field from the canonical schema:
  - `ts`
  - `instId`
  - `action`
  - `position_mode`
  - `size_usdt`
  - `order_type`
  - `stop_loss_px`
  - `exit_plan`
  - `reason`
  - `confidence`
  - `leverage`
  - `cooldown_ok`
- Use `instId` in `BTC-USDT` style in the internal canonical decision. The script's `binance_symbol` is only for data fetching.
- Set `order_type` to `MARKET`.
- Keep `reason` in simplified Chinese and make it cite actual sequence evidence from the script output.
- Respect the canonical leverage ladder, confidence buckets, sizing rules, and exit-plan rules even when the final answer is prose.

## Default Output Format

Default to a structured Chinese analysis report, not raw JSON.

Include these sections in order unless the user explicitly asks for a different format:

1. `结论`
   - State the final recommended action: `BUY` / `SELL` / `HOLD`.
   - State whether the recommendation is immediate action or wait-for-confirmation.
2. `趋势判断`
   - Explain the 2H strategic direction.
   - Explain the 15m execution structure.
   - Mention 5m only as supporting context.
3. `关键理由`
   - Explain why the chosen action is valid.
   - Explain why the opposite direction is not preferred.
   - Explain why now is or is not the right timing.
4. `支撑与阻力`
   - List near support, key support, near resistance, and key resistance.
   - Distinguish short-term levels from higher-timeframe levels.
5. `触发条件`
   - Explain what price action would upgrade to `BUY`.
   - Explain what price action would upgrade to `SELL`.
   - Explain what invalidates the current bias.
6. `风控与计划`
   - Give stop-loss logic, target logic, and management logic in plain Chinese.
   - Mention if current risk/reward is insufficient.

If the user explicitly asks for JSON, return the canonical JSON array instead.

## How To Read The Script Output

Focus on these sections:

- `timeframes["2h"]`
  - Use for strategic trend class: `STRONG_UP`, `MODERATE_UP`, `MODERATE_DOWN`, `STRONG_DOWN`.
  - Check price structure, EMA alignment, MACD histogram, RSI, ADX, swing highs/lows, reversal candles, volume anomalies, and volume profile.
- `timeframes["15m"]`
  - Use for execution quality.
  - Check breakout confirmation, pullback hold, EMA21 behavior, ATR-based stop distance, recent swing levels, and risk/reward estimates.
- `timeframes["5m"]`
  - Use only as short-term context. Do not let it override the 2H strategic filter.
- `funding`
  - Use for cost evaluation.
- `depth`
  - Use spread and slippage estimates to judge whether execution cost is acceptable.
- `open_interest`
  - Use as supporting context, not as a standalone trigger.

## Decision Discipline

- Enforce the 2H directional filter first.
- Require confirmed 15m structure before any `BUY` or `SELL`.
- Prefer `HOLD` when confirmation is missing, risk/reward is poor, ATR expansion is too aggressive, or cost is unattractive.
- For counter-trend setups, allow only the weaker reconnaissance logic that the canonical prompt permits.
- Always produce an `exit_plan` with numeric `tp` and `sl`, plus a Chinese `inv` management rule.
- If the data is incomplete or inconsistent, output `HOLD`.
- Internally evaluate all canonical controls:
  - trend class
  - entry confirmation
  - counter-trend exception handling
  - leverage bucket
  - nominal size
  - worst-case risk
  - exit-plan priority
  - cooldown
  - simultaneous-position cap
  - confidence bucket

## Coverage Check

This skill is not allowed to rely on a partial summary anymore. Before answering, make sure your reasoning covers all canonical rule groups listed in `references/system-prompt-coverage.md`.

## Script

- Main helper: `scripts/binance_futures_snapshot.py`
- Purpose:
  - Fetch Binance U-margined perpetual public data
  - Compute the indicators and structural helpers required by the strategy
  - Output a compact JSON snapshot for one or more symbols

## Output Contract

- Default:
  - Return a structured Chinese market analysis report.
  - Include a single explicit final recommendation per symbol: `BUY`, `SELL`, or `HOLD`.
  - Include detailed reasons, support and resistance, invalidation conditions, and next-step triggers.
- If JSON is requested:
  - Return one decision object per requested symbol in a single JSON array.
  - Keep the field order exactly aligned with the canonical prompt.

If the user asks for `BTC ETH`, analyze both symbols separately in the same response.
