# Safety Gates Reference

## Thresholds (configurable in `polymarket.yaml`)

```yaml
safety:
  warn_threshold_usd: 50     # single confirmation above this
  confirm_threshold_usd: 500 # double confirmation above this
```

## Confirmation Levels

| Amount | Behavior |
|--------|----------|
| < $50 | Proceeds automatically, no prompt |
| $50-$499 | Shows warning with estimated price and odds, asks once |
| >= $500 | Hard double-confirmation — must confirm twice |

## Hard-Stops (cannot proceed, must fix first)

| Condition | Error |
|-----------|-------|
| USDC.e balance < trade amount (buy) | Auto-swap POL→USDC.e offered; hard-stop only if POL also insufficient |
| CTF token balance < sell shares | "Insufficient YES/NO tokens" |
| POL gas < 0.01 | "Insufficient POL gas" |
| Market status != ACTIVE | "Market is CLOSED" |
| Trade amount < min_order_size | "Below min order size" |

## Security Properties

- **No MaxUint256 approvals** — BUY approves the exact USDC.e amount per trade
- **setApprovalForAll for SELL** — approves only the exchange operator, no dollar amount
- **Confirmation prompts** — user explicitly types "yes" to proceed
- **Hard-stop before approval** — checks run before any on-chain transaction
