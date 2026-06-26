# Analysis Mode

This skill reuses the repository's live-trading strategy, but it does not execute trades.

## Canonical Sources

- Primary rule source: `../../../src/main/resources/system-prompt.txt`
- Execution-field semantics: `../../../docs/core-feature-spec.md`

Use this file only for the analysis-only adaptations below.

## Analysis-Only Defaults

When the user only gives symbol codes such as `BTC` or `ETH`, use:

- `equity_usdt = 10000`
- `free_usdt = 10000`
- `positions = []`
- `cooldown_ok = true`

If the user provides real account values, replace these defaults.

## Action Restrictions

Without explicit position context:

- Allow `BUY`
- Allow `SELL`
- Allow `HOLD`
- Do not use `ADD`
- Do not use `REDUCE`
- Do not use `CLOSE`

If the user provides a current position, then `ADD`, `REDUCE`, and `CLOSE` become available, but they must still follow the canonical strategy.

## Symbol Mapping

Use Binance public futures data from U-margined perpetual contracts:

- Fetch with `BTCUSDT`, `ETHUSDT`, `SOLUSDT`
- Output with `BTC-USDT`, `ETH-USDT`, `SOL-USDT`

Do not use spot endpoints and do not switch to coin-margined contracts.

## Required Output

Default to a structured Chinese analysis report.

Only return a JSON array when the user explicitly asks for JSON.

Internally keep the canonical decision object with this exact field order:

1. `ts`
2. `instId`
3. `action`
4. `position_mode`
5. `size_usdt`
6. `order_type`
7. `stop_loss_px`
8. `exit_plan`
9. `reason`
10. `confidence`
11. `leverage`
12. `cooldown_ok`

In prose mode, surface at least:

- final action
- trend judgment
- detailed rationale
- support and resistance
- invalidation conditions
- stop-loss and target logic

## Sizing

In analysis mode, keep the same sizing logic:

- `NEW`: `free_usdt * 30% * leverage`
- If 15m is range or counter-trend bounce, halve the nominal size
- If no valid entry exists, use `HOLD` and set `size_usdt = 0`

## When To Prefer HOLD

Prefer `HOLD` when any of these are true:

- 2H direction and 15m trigger disagree
- 15m has no confirmed breakout or pullback hold
- Expected R is below the canonical threshold
- Funding, spread, or slippage materially weakens the setup
- ATR expansion makes the stop too wide
- The structure is noisy or ambiguous
