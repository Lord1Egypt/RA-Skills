# Backtesting standards

Treat a backtest as a conditional historical simulation. Do not present it as a forecast.

## Define the counterfactual

Fix the pool, chain, observation window, initial capital, starting token quantities, range, fee model, action policy, latency, price source, gas model, and benchmark. The strategy may use only information available at each simulated decision time.

State whether the test models a static position or a sequence of mints, increases, decreases, collects, compounds, stakes, and range moves. A static test cannot validate an active management policy.

## Historical state

Use block-anchored pool state where possible. Record gaps and indexer lag. For each interval retain current tick or price, high and low where available, active liquidity, fee growth, liquidity events, token prices, and protocol state that affects fee or reward rights.

- Sparse intervals may be carried forward for time accounting only when no state-changing event occurred.
- Do not invent volume, fees, or a price path for a missing interval.
- Candle high and low do not reveal traversal order or time spent at each tick. Report bounds or sensitivity instead of treating uniform movement as observed fact.
- The active interval is `tickLower <= tickCurrent < tickUpper`.

## Fee estimation

Prefer position-specific fee-growth-inside reconstruction from tick state. If only global fee growth is available, label the result an approximation and state how out-of-range periods and crossed ticks are handled.

A simulated position changes the fee share of active liquidity. Apply dilution using active liquidity at each historical interval. Using today's liquidity for the whole window creates lookahead bias.

Keep fees in token units until valuation. Do not assume all fees were compounded unless the simulated policy compounds them at that time and pays the resulting costs.

## Benchmark and costs

Compare with the original HOLD quantities valued at each observation. Also report a single-token benchmark when it matches the user's objective. Include:

- entry and exit slippage
- swap, rebalance, claim, and staking costs
- gas at the simulated time
- automation or keeper fees
- idle and loose balances
- incentives with their actual eligibility and end dates

Do not subtract both divergence loss and another estimate of the same inventory effect.

## Bias checks

Test for lookahead, survivorship, pool-selection, token-list, price-source, missing-data, and parameter-search bias. Separate calibration and evaluation windows. A validation set limited to simple surviving positions does not establish accuracy for positions with later deposits or withdrawals.

Run sensitivity across range width, start time, observation interval, execution delay, slippage, gas, and fee dilution. Report where the decision changes.

## Output

Include method version, data coverage, missing intervals, assumptions, time in range, earned fees, incentives, inventory divergence, net result versus HOLD, drawdown, turnover, action count, and total costs. Separate exact reconstruction from modeled values.

## Reusable experiment

Keep a stable user-owned strategy ID and rule revision, supplied preferences,
provider/tool and dataset identity, benchmark, costs, result class and next test.
Use the user's chosen artifact format and storage; no particular service is
required. Compare static, wide-range or actively managed variants only when they
answer the user's objective, and record each trial rather than selecting only the
best run. A changed rule starts a new revision.

Distinguish historical simulation, forward paper observations and receipt-verified
live performance. A range crossing is a signal, not a simulated or live remint.
Without historical fee and liquidity coverage, return the available range/inventory
sensitivity and exact data gaps instead of an invented APR or backtest result.
