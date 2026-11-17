# Input and accounting contract

The engine accepts one asset's consecutive daily USD observations. The CLI also accepts the successful `galleon-defi-market-snapshot` history envelope and validates its `dataset` field; its integrity hash still covers the exact envelope bytes. Field name `close` is a model convention: `priceType` distinguishes an actual venue close from an aggregate snapshot. No network requests occur in the engine or backtest CLI.

## Dataset

```json
{
  "schemaVersion": 1,
  "identity": {"namespace": "coingecko", "id": "bitcoin"},
  "unit": "USD",
  "intervalSeconds": 86400,
  "priceType": "aggregate-snapshot",
  "provenance": {
    "provider": "coingecko",
    "source": "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
    "retrievedAt": "2026-10-02T12:00:00.000Z",
    "synthetic": false
  },
  "candles": [
    {"timestamp": "2026-09-30T00:00:00.000Z", "close": 100},
    {"timestamp": "2026-10-01T00:00:00.000Z", "close": 110}
  ]
}
```

Values above illustrate shape; they are not live Bitcoin evidence. Use exact ISO UTC midnight dates, 2 to 10,000 rows in ascending consecutive-day order, and finite prices from `1e-12` to `1e12`. Retrieval time must follow every observation. Identity uses lowercase provider namespace and an opaque ID. Non-synthetic sources must be HTTPS without URL credentials, query strings or fragments; retain safe normalized parameters separately in the research record. Optional `rawSha256` identifies original response bytes. A synthetic dataset must explicitly set `synthetic: true` and a `fixture:<name>` source.

## Strategy specification

```json
{
  "schemaVersion": 1,
  "initialCashUsd": 1000,
  "feeBps": 10,
  "slippageBps": 20,
  "strategy": {"type": "sma", "period": 20},
  "contributions": [
    {"timestamp": "2026-10-01T00:00:00.000Z", "amountUsd": 100}
  ]
}
```

Choose exactly one strategy. `buy-and-hold` accepts only `type`. `dca` adds a positive `amountUsd` and integer `everyBars`; the purchase budget includes fees. `sma` adds an integer `period` from 2 to one less than the observation count. Unknown fields fail instead of being ignored. Fees/slippage are finite basis points from 0 to 1000. Initial cash and individual contributions range from $0.01 to $1 trillion; this is an input bound, not a practical position-size claim.

Contributions are optional positive cash deposits at unique observation dates. Withdrawals are unsupported. A funded DCA experiment keeps its initial budget in non-interest-bearing cash until its purchase date; it does not create new money each interval. Supply scheduled deposits explicitly when comparing a monthly saving plan.

## Daily ordering

1. Mark the existing asset units at the current observation; this captures movement since the prior observation.
2. Add any scheduled contribution to cash.
3. Execute the rule decided at the previous observation, using the current mark and adverse slippage. No order executes on the first observation.
4. Mark ending cash/units, record costs and calculate the return index.
5. Form the next decision using only observations through the current date. A final decision has no fill when no next observation exists.

Buy fill = mark × (1 + slippage rate). Sell fill = mark × (1 - slippage rate). Fee = traded notional × fee rate. An all-cash buy uses notional = available cash / (1 + fee rate); quantity = notional / buy fill. An all-unit sale returns quantity × sell fill minus its fee. Fractional spot units are allowed; there is no shorting or leverage.

SMA includes the current observation in its trailing average; equality targets cash. Warmup observations remain cash. DCA decisions occur on indices 0, N, 2N and so forth, with fills on indices 1, N+1, 2N+1. The benchmark uses the same dates, costs and deposits and invests available cash at the next observation under its standing buy rule.

## Returns and drawdown

Let previous post-trade equity be V, current pre-deposit marked equity be M, contribution be C, and current post-trade marked equity be E. Link the interval's two factors:

`returnIndex *= (M / V) * (E / (M + C))`

The first observation has market factor 1. This separates market movement before the deposit from trading costs after it. The contribution itself is not investment return. Time-weighted return = `(returnIndex - 1) × 100`. The flow-neutral maximum drawdown is the largest `1 - returnIndex / priorPeakIndex`, including initial index 1.

Net profit = ending marked equity - initial cash - additional contributions. `contributionAdjustedProfitPct` divides this dollar profit by all contributed capital; it is a simple profit ratio, not an annualized return or money-weighted IRR. The time-weighted return and ending-equity benchmark differences answer different questions when deposits occur.

## Hand-checkable examples

With $100 cash, no costs and prices 100 → 200 → 300, buy-and-hold decides at 100, buys 0.5 units at the next mark 200, and ends at $150. It earns 50%, not 200%.

With $100 cash, prices 100 → 100 → 50 and a $1,000 contribution at the final observation, the existing unit loses $50 before the deposit. Ending equity is $1,050 against $1,100 contributed; time-weighted return and drawdown are both -50%/50%. The deposit does not turn the price loss into a profit.

With a flat $100 mark, a $100 buy budget and 100 bps each of fee and adverse slippage, marked asset value is `100 / 1.01 / 1.01`, approximately $98.0296. The cost difference is accounted for by recorded fees and slippage.

All final assets remain open and marked. Exit fees/slippage require an actual modeled sale; the report does not imply the displayed equity could be withdrawn immediately. Floating-point calculations are research estimates and are unsuitable for constructing token amounts or transactions.

## Frozen-rule validation contract

`runStrategyValidation(dataset, spec, {splitIndex?, stressFeeBps?, stressSlippageBps?})` lives in the same pure ESM engine as `runBacktest`. It accepts the unchanged dataset/spec schemas. Its standalone wrapper is `node scripts/validate-strategy.mjs --data <dataset.json> --spec <spec.json> [--split <index>] [--stress-fee-bps <bps>] [--stress-slippage-bps <bps>]`. Unknown options fail. The wrapper hashes the exact data/spec bytes, including a supported history envelope; the report itself records the split and stress options.

`splitIndex` is an integer zero-based first held-out observation, default `floor(observations / 2)`. The reference period is `[0, splitIndex)` and the held-out period `[splitIndex, observations)`. They are disjoint and cover the full dataset. Each must contain at least 3 observations for buy-and-hold, `max(3, everyBars + 2)` for DCA or `period + 2` for SMA. The latter permits warmup, a possible next-observation fill and a later mark; DCA permits two scheduled purchase opportunities. Funding or price paths can still produce fewer actual trades. These minimums are mechanical, not evidence of statistical adequacy.

Each period starts from `initialCashUsd`, zero units and no pending order. Contributions belong to their own dates only, including a contribution on the first held-out date. DCA cadence and SMA warmup restart at each period's first observation. The reference final decision has no next observation within that experiment and does not execute in the held-out period. No prehistory or asset/cash balance crosses the split. Original provider identity/provenance remain attached to both subsets.

For each period, `baseline` and `higherCosts` are full backtest reports with the same-flow/same-cost benchmark. Each stress component defaults to `min(1000, max(2 × baseline, baseline + 10))` basis points. Explicit stresses must be finite, at least their baseline and no more than 1000; their sum must be strictly larger. A baseline already at 1000 bps for both costs cannot be stressed within this model and fails. Costs are applied on actual fills; there is no forced exit.

`costSensitivity` subtracts baseline from higher-cost ending equity, time-weighted return, maximum drawdown and summed modeled fees/slippage. Do not assume every difference is adverse on every strategy/path: cost changes can alter the invested unit amounts or later cost totals. Inspect the underlying reports.

Top-level fields include `frozenSpec`, `partition`, `costScenarios`, `accounting`, `periods.reference` and `periods.heldOut`, assumptions and limitations. There is no combined performance or account balance. The result is tagged `evidence: historical-simulation`. `ok: true` confirms valid execution only. It does not attest that the held-out period was unseen, validate profitability, represent a live paper account or authorize a trade.

With prices 100 → 200 → 300 / 100 → 50 → 100 and $100 initial cash per period, no costs or contributions, reference ending equity is $150 and held-out ending equity is $200. The held-out buy executes at 50 after a new decision at its initial 100 mark; it does not reuse the reference units or $150 equity. These balances describe independent experiments and cannot be summed into a portfolio balance.
