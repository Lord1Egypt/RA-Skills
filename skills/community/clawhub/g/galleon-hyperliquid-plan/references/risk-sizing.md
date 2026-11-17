# Risk sizing

Size exposure from the loss at a stressed stop, not from leverage or desired profit.

## Inputs

- live account equity and free margin for the actual account mode
- current positions, open orders, correlated exposure, and daily loss state
- side, entry, stop, intended order type, and requested leverage
- user risk per trade and total open-risk limit
- `szDecimals`, margin table, max trade size, minimum notional, and current fees
- book depth for entry and forced exit at the planned size

Missing or stale inputs produce `REJECT: missing input`.

## Arithmetic

```text
risk_budget       = equity * risk_percent
nominal_distance  = abs(entry - stop)
stop_slippage     = entry * stop_slippage_bps / 10_000
stressed_stop     = stop - stop_slippage for a long
                    stop + stop_slippage for a short
fees_per_unit     = entry * entry_fee_rate + stressed_stop * exit_fee_rate
stressed_distance = abs(entry - stressed_stop) + fees_per_unit
raw_size          = risk_budget / stressed_distance
size              = round_down(raw_size, szDecimals)
notional          = size * entry
stressed_risk     = size * stressed_distance
```

Use `node scripts/risk.mjs` for the arithmetic. The slippage assumption must come from a current walk of the exit side of the book, widened for gaps and liquidation stress. It is an assumption, not a maximum loss guarantee.

## Gates

- Stop is on the loss side of entry.
- Rounded size is nonzero and meets the exchange minimum without rounding up.
- Post-trade notional fits the applicable margin tier and user leverage limit.
- Initial margin plus headroom fits current free margin under the actual account mode.
- Stressed total open risk and correlated exposure stay within user limits.
- Daily loss stop and market allowlist pass.
- Resulting position has an exchange-resting protection plan.
- Portfolio-margin borrow, interest, LTV, caps, and combined liquidation remain acceptable.

Use the exchange's `activeAssetData` values as constraints, not as a sizing objective. Maximum available exposure is not recommended exposure.
