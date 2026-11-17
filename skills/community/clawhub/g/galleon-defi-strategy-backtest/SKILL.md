---
name: galleon-defi-strategy-backtest
description: Test daily long-only buy-and-hold, funded DCA or moving-average rules with costs, cash flows, drawdown and a benchmark. Use when validating a frozen crypto strategy on a held-out period, comparing cost sensitivity or checking a backtest for timing and accounting errors.
license: MIT
compatibility: Portable agent instructions. Bundled offline backtest requires Node.js 20+ and local JSON files. The pure ESM engine also runs in browsers. No provider account, wallet, signer, trading engine or scheduler is bundled.
metadata:
  author: Galleon Labs
  version: "0.2.0"
---

# Daily strategy research

Turn a supported rule into a reproducible experiment whose result can be checked. Keep historical fit, unseen-period behavior, paper observation and live trading as separate evidence.

## Define the experiment

Resolve the requested asset to its provider identity, data period and price type. Write entry/exit logic, cash budget, any positive contributions, fees and adverse slippage before evaluating performance. Reuse the user's terms and tools. State assumptions for missing research parameters; do not silently translate unsupported leverage, funding, intraday stops or portfolio rotation into this daily spot model.

The bundled engine supports:

- **Buy-and-hold:** invest available cash at the next observation, including subsequent contributions.
- **DCA:** decide a fixed USD purchase every N observations, fill at the following observation, and stop spending when funded cash runs out. Contributions must be explicitly supplied.
- **SMA:** after N observations of warmup, target the asset when the current observation exceeds its trailing N-observation average, otherwise target cash. Change exposure at the next observation.

Use [the model contract](references/model.md) to prepare JSON. Unknown strategy fields fail validation; a prose thesis is not executable code. If a rule is unsupported, return its precise specification and the required data/engine capabilities instead of claiming it ran.

## Establish the data

Accept a local dataset with exact identity, USD units, daily timestamps, provider/source, retrieval time and aggregate-snapshot versus venue-close semantics. Reject nonpositive prices, duplicate/reversed dates, daily gaps or observations after retrieval. Do not fill gaps, reuse a stale cached value as a new candle or assume an aggregate price was tradeable.

For public historical data, use the user's existing official source or the CoinGecko daily market-chart procedure in [research and source selection](references/research.md). The separately installable `galleon-defi-market-snapshot` can collect compatible history, but this skill also works alone with the documented JSON format. No API key is required by the backtest; provider access is a separate read.

## Run and inspect

From this skill directory:

```bash
node scripts/backtest.mjs --data examples/synthetic-daily.json --spec examples/sma.json
node scripts/backtest.mjs --data <daily-data.json> --spec <strategy.json>
node scripts/validate-strategy.mjs --data examples/synthetic-daily.json --spec examples/sma.json --split 30
```

The shipped example is synthetic. Use it to verify the installation and accounting, never as evidence about an actual token. Both scripts read only the two local files and print JSON; they do not download data, sign, submit, store account state or create jobs. Preserve the input hashes with the report. The npm CLI exposes `backtest` and `validate-strategy` with the same arguments.

Inspect the first trade: `decisionAt` must precede `executedAt` by one day. Check modeled buy/sell price direction, fees, cash and contribution totals, retained uninvested cash and final open exposure. Compare the identical-flow, identical-cost benchmark. Use return index and drawdown to avoid counting a deposit as profit. Total contributed capital and net profit should reconcile to ending marked equity.

## Test the thesis honestly

Apply [the research workflow](references/research.md). Freeze the rule and assumptions before testing an unseen period; report its dates and sample size separately. `validate-strategy` partitions at the zero-based `--split` index (default half, rounded down), then runs the same rule and its benchmark with baseline and higher costs in both periods. Higher fees/slippage default to `max(2 × baseline, baseline + 10 bps)`, capped at 1000 each; optional `--stress-fee-bps` and `--stress-slippage-bps` set the declared stress assumptions. Neither cost may decrease, and at least one must increase.

Each period independently restarts with declared initial cash, zero asset units, fresh indicator warmup and only its own contributions. Inspect `periods.reference` and `periods.heldOut` separately; retain their `baseline`, `higherCosts` and `costSensitivity` reports. Do not add balances or geometrically link these independent restarts as a continuous account. A chronological split cannot prove the later observations were unseen before the user supplied the rule. The runner performs no parameter search. Report additional manually attempted variants, including losses; do not optimize across the full dataset and call the same history out of sample.

Use fixed `buy-and-hold`, `weekly-dca`, `sma-10` or `sma-30` templates from `STRATEGY_TEMPLATES` in `scripts/engine.mjs` when a starting specification is useful. `createStrategySpec` requires explicit initial cash, fees and slippage; weekly DCA also requires `amountUsd`. Templates declare daily data requirements, minimum per-period samples and a requested 180-observation research horizon. The same exports are available at `galleon-defi-strategy-skills/engine`. Their parameters are fixed starting points, not optimized choices or profitability recommendations.

A stop loss needs intraday price paths and a specified fill convention; this engine cannot model one from daily aggregate samples. Small samples, a single surviving asset and limited provider history constrain conclusions. Do not add a Sharpe, win rate or annualized figure whose definition/data have not been established.

## Deliver

Return the written rule, asset/data identity, dates, input hashes, starting/contributed capital, ending marked equity, net profit, time-weighted return, maximum drawdown, modeled fees/slippage and benchmark differences. Include the equity curve and trades when useful, plus the material assumptions and limitations from the report. State whether evidence was synthetic, aggregate market data or venue history.

Completion means the supported specification ran on validated dated inputs, accounting reconciled and the report includes a benchmark and limits. For validation, include both independent periods and both cost scenarios, the frozen rule and split convention. `ok: true` means the run completed, not a trading suitability pass. A historical result does not establish future performance, paper deployment, venue fill realism or permission to trade. For a requested next step, prepare the concrete terms and hand off to the user's existing venue/scheduler workflow within their authority.
