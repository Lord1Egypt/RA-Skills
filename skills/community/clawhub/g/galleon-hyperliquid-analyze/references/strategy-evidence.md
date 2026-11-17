# Strategy evidence

Treat every strategy as a falsifiable rule set, not a story.

## Freeze the claim

Record instrument, DEX, network, bar interval and close rule, data fields, entry, abstention, exit, stop, time exit, sizing, leverage, costs, funding, partial-fill behavior, rejected-order behavior, and the condition that would abandon the idea.

For an imported claim, also record its exact source and retrieval date, every reported parameter set, asset, timeframe, and trial. Missing rules stay missing. Do not supply plausible defaults without labeling them as new assumptions.

## Data record

Save the exact API request, network, fetch time, returned range, gaps, duplicate policy, and any remapped market identity. Keep raw data immutable. Derivations belong in a separate file or step.

## Backtest gates

- Signals at time `t` use only information available at `t`.
- Execution occurs at the stated next observable price.
- Charge effective maker or taker fees, funding at its true interval, spread, size-aware slippage, and borrow interest where relevant.
- Freeze rules before reading the chronological holdout. Looking at a holdout spends it.
- Record every variant and trial, including failed ones and those run by the original source.
- Report trade count, result distribution, expectancy, drawdown, turnover, fees, funding, and dependence on one market or period.
- Resample trades in blocks to preserve streaks. Report a lower confidence bound, not only mean expectancy.

## Falsification

Flip the signal, shuffle entry times, remove the best trades, double costs, split by market and regime, and test sensitivity around each chosen parameter. A result that disappears under a small cost or parameter change is not demonstrated edge.

Use `PASS`, `WEAK`, or `REJECTED`. A profitable in-sample curve with reused holdout data is in-sample evidence only.

## Forward test

Unsigned plans can forward-test signals when the user wants a simulation stage. They must not submit orders. Agree the duration and sample size before the first signal, then compare forward fills and costs with the backtest without changing the rules mid-test.

Only receipt-verified live fills validate a strategy for live sizing. Keep simulated and live results separate and never blend them, and never declare a variant validated from a handful of selected winners. When the user has authorized live trading, a small risk-sized live starter with its own qualified evidence is a legitimate test; it does not require claiming the broad strategy is proven.

## Portable experiment record

Return a user-owned experiment record in the requested format: stable strategy ID,
rule revision, source parameters, chosen data provider and actual tool, dataset
window or digest, trial ledger, cost model, benchmark, result class and next test.
A revision is a new experiment; do not overwrite results or silently change an
active strategy. The same rules may be evaluated through different providers if
coverage, identity and cost assumptions remain comparable.

Label every result as historical simulation, forward paper observation, or verified
live execution. A paper fill needs a declared fill rule, timing and costs; observing
a signal alone is not a fill. Missing historical coverage produces a scoped test
plan or partial result, not invented performance. Start with the user's own rules;
optional templates are examples, not a required strategy catalog.
