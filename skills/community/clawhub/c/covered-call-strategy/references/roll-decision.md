# Roll Decision Framework

## When to Roll Up

Roll Up = Buy back current ITM call + Sell new higher-strike call

### Quantitative Decision

Roll Up when:

```
upside_released_per_dollar_spent > 1.5

Where:
  upside_released = (new_strike - old_strike) × shares_rolled
  cost = (buy_back_price - new_premium_received) × shares_rolled
  ratio = upside_released / cost
```

Example:
- Old strike $580, new strike $820, 100 shares
- Buy back @ $262, sell new @ $166
- Cost = ($262 - $166) × 100 = $9,600
- Upside released = ($820 - $580) × 100 = $24,000
- Ratio = 24,000 / 9,600 = 2.5 → **Good value, consider rolling**

If ratio < 1.0 → Roll costs more than the upside it releases → **Do not roll**

### Partial Roll Decision

For N short calls at same strike, rolling M of them:

```
M = min(N, floor(ratio / 2))

If ratio > 3.0:  consider full roll (M = N)
If ratio 1.5-3.0: consider partial roll (M = 1 for N=2+)
If ratio < 1.5:  do not roll
```

## When to Roll Down

Roll Down = Buy back current OTM/near-ATM call + Sell new lower-strike call

### When Stock Has Dropped Significantly

Roll down when:
1. Current call is deep OTM (delta < 0.1)
2. Premium remaining is minimal (< 5% of original)
3. Stock has stabilized at new lower level
4. New lower-strike call offers meaningful premium (> 3% of stock price)

**Caution**: Rolling down locks in a lower sell price. Only do this if:
- You've accepted the stock may not recover to original strike
- The additional premium meaningfully improves downside cushion
- You plan to hold shares long-term regardless

## When to Close (No Roll)

Close the call position (buy back) without selling a new call when:
1. You want to sell the stock (free up shares)
2. Stock has dropped and you want to cut losses without cap
3. Volatility is extremely high → call prices inflated → good time to buy back
4. You're switching to a different strategy (e.g., protective put)

## Monitoring Triggers After Roll

After rolling, set re-evaluation triggers:

| Event | Action |
|-------|--------|
| Stock reaches 90% of new strike | Evaluate second roll |
| Stock drops 15%+ from roll point | Evaluate roll down or close |
| 30 days before expiry | Final roll/close decision |
| Earnings announcement approaching | Close or roll before IV crush |
| Dividend ex-date approaching | Check if early assignment likely |

## Decision Tree

```
Is the current call ITM?
├── Yes → Is the stock likely to keep rising?
│   ├── Yes → Calculate roll ratio
│   │   ├── Ratio > 1.5 → Roll (partial or full)
│   │   └── Ratio < 1.5 → Do nothing, accept assignment
│   └── No → Do nothing, enjoy assignment at above-market price
└── No (OTM) → Is the call nearly worthless?
    ├── Yes (premium < 5% of received) →
    │   Roll down for more premium, OR
    │   Let it expire and sell new call
    └── No → Hold, premium is still protecting downside
```
