# Fee-Aware Arbitrage Calculator

Use this file to convert headline spreads into net economics.

## 1. Generic Net Edge

```text
gross_pnl = guaranteed_exit_value - entry_cost
net_pnl = gross_pnl - fees - financing - transfer_cost - FX_slippage - other_known_costs
net_edge_pct = net_pnl / capital_committed
```

Never use gross edge as the decision number.

## 2. Surebet Test

For opposite outcomes across books:

```text
implied_sum = (1 / decimal_odds_leg_a) + (1 / decimal_odds_leg_b)
```

Interpretation:
- `implied_sum < 1` means a pre-fee surebet exists
- `implied_sum >= 1` means no hard lock before costs

After that, still subtract fees, limits, and withdrawal drag.

## 3. Multi-Outcome Basket Test

For a complete set of mutually exclusive outcomes with fixed payout `P`:

```text
gross_edge = P - sum(cost_of_all_outcome_legs)
net_edge = gross_edge - all_costs
```

Use this for prediction market baskets and any market where all outcomes partition the event cleanly.

## 4. Cross-Venue Spot Lock

```text
buy_total = buy_price * size + taker_fee_buy + transfer_cost
sell_total = sell_price * size - taker_fee_sell
net_pnl = sell_total - buy_total
```

Add:
- withdrawal fee on the asset leg
- FX if venues settle in different currencies
- inventory carrying cost if transfer is not immediate

## 5. Basis or Carry Trade

```text
net_basis = futures_price - spot_price
net_edge = net_basis - entry_fees - exit_fees - funding - borrow - carry_cost
annualized_edge = net_edge / spot_price * (365 / days_to_expiry)
```

If the hedge requires rolling or uncertain borrow, downgrade from hard arbitrage.

## 6. Size Constraint

```text
realistic_size = min(
  size_available_leg_a,
  size_available_leg_b,
  capital_limit,
  transfer_limit,
  venue_max_size
)
```

The smallest reliable capacity wins.

## 7. Transfer-Latency Penalty

When the opportunity depends on moving inventory:

```text
latency_penalty = expected_price_move_per_hour * transfer_hours * size
adjusted_net_pnl = net_pnl - latency_penalty
```

If adjusted net PnL turns negative, the edge is not locked.

## Spreadsheet Formulas

Assume:
- `B2` = guaranteed exit value
- `B3` = entry cost
- `B4` = fees
- `B5` = financing
- `B6` = transfer cost
- `B7` = FX slippage
- `B8` = capital committed

Then:

```text
Gross PnL: =B2-B3
Net PnL: =(B2-B3)-B4-B5-B6-B7
Net Edge %: =((B2-B3)-B4-B5-B6-B7)/B8
```

For a 2-leg surebet using decimal odds in `C2` and `C3`:

```text
Surebet check: =(1/C2)+(1/C3)
```

## Output Template

```markdown
## Math
- Gross edge:
- Net edge:
- Net edge percent:
- Realistic size:
- Cost lines included:
- Unknown costs still missing:
```
