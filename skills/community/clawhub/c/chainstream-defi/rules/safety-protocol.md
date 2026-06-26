# Safety Protocol

Hard requirements for all destructive DeFi operations. These rules are NOT suggestions — they are mandatory.

## Two-Phase Confirmation

Every destructive operation (swap, bridge, create, send) MUST:

1. **Show quote/summary BEFORE execution** — price impact, slippage, gas, amounts
2. **Wait for explicit user confirmation** — "y", "yes", "confirm"
3. If user skips confirmation ("just do it"), show summary anyway and ask

## Risk Thresholds

### Price Impact

| Impact | Action |
|--------|--------|
| < 1% | Proceed normally |
| 1-5% | Warn user: "Price impact is X%, higher than typical" |
| 5-15% | Strong warning: "High price impact. You will receive significantly less." |
| > 15% | Block by default: "Extremely high price impact. Are you sure? (type YES to confirm)" |

### Slippage

| Slippage | Action |
|----------|--------|
| 0.1-1% | Normal range |
| 1-5% | Acceptable for volatile tokens |
| 5-50% | Warn: "High slippage tolerance. You may receive much less than quoted." |
| > 50% | Reject: "Slippage too high. Maximum allowed: 50%." |

## Emergency Abort

Abort and show error if:
- Wallet balance is insufficient
- Gas estimate exceeds 10% of trade value
- API returns transaction simulation failure

## Post-Trade Requirements

After every successful transaction:
1. Show actual fill amounts (not just estimated)
2. Show block explorer link
3. Show gas cost paid

## Forbidden Actions

- Auto-retry failed transactions (user must re-confirm)
- Execute multiple swaps in batch without individual confirmation
- Use funds beyond what user explicitly specified
- Skip quote phase for any reason
