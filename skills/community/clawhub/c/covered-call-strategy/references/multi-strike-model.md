# Multi-Strike Covered Call Model

## Position Structure Notation

A covered call portfolio with N shares and M short calls across K strikes:

```
Position = {
  shares: [
    { qty: 100, cost: 430 },
    { qty: 100, cost: 484 },
    { qty: 100, cost: 588 }
  ],
  calls: [
    { strike: 580, expiry: "2026-12-18", premium: 54.85, current: 262 },
    { strike: 580, expiry: "2026-12-18", premium: 80.05, current: 262 },
    { strike: 820, expiry: "2026-12-18", premium: 115.00, current: 166 }
  ]
}
```

## P&L Calculation at Expiry

For each stock price S at expiry:

```
For each call i:
  if S > strike_i:
    # ITM - shares assigned at strike
    call_pnl = premium_i  # keep full premium
    stock_sell_price = strike_i
  else:
    # OTM - call expires worthless
    call_pnl = premium_i  # keep full premium
    stock_sell_price = S   # sell at market

total_pnl = Σ (stock_sell_price - cost_j) × 100 + Σ call_pnl × 100
```

## Net Premium After Roll

When rolling from strike A to strike B:

```
net_premium = original_premium - buy_back_cost + new_premium_received

Example: Roll 1 call from $580 to $820
  original_premium = $54.85  (already received)
  buy_back_cost    = $262    (current market price)
  new_premium      = $166    (selling new $820 call)
  net_premium      = $54.85 - $262 + $166 = -$41.15 per share

This means the roll DESTROYED $41.15 of premium cushion per share.
```

## Scenario Matrix Template

```
| Stock at Expiry | Stock P&L | Net Premium | Assignment | Total P&L |
|----------------|-----------|-------------|------------|-----------|
| S < min(strike) | (S-avg_cost)×N | net_premium×N | none | sum |
| min < S < mid   | partial assignment | net_premium×N | ITM calls | sum |
| S > max(strike)  | all assigned | net_premium×N | all calls | sum |
```

## Key Insight: Net Premium is the Only Variable That Differs Across Strategies for Downside

For downside scenarios (S < all strikes), ALL strategies have the same stock P&L. The only difference is net premium. Therefore:

**Downside P&L difference = Δ net premium between strategies**

This means:
- Do Nothing (highest net premium) → best downside outcome
- Full Roll Up (lowest net premium) → worst downside outcome
- The difference is exactly the cost of the roll

## Multi-Batch Cost Basis

When shares were bought at different prices, assignment order matters:

| Scenario | Which shares get assigned? | Impact |
|----------|--------------------------|--------|
| All calls same strike | Random (broker decides) | Average cost applies |
| Different strikes | Lower strike calls assigned first | Cheaper shares sold first (better) |
| Partial roll | Depends on specific assignment | Calculate per-batch |

For simplicity in analysis, use weighted average cost basis unless specific assignment order significantly impacts the result.
