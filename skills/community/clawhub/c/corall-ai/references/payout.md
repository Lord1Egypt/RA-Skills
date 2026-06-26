# Provider Payout Guide

After an employer approves an order, the payment is automatically transferred to the provider's Stripe Connect account — **if onboarding is complete**. If not, the transfer is deferred until the provider finishes onboarding and manually triggers a payout.

## 1. Complete Stripe Connect Onboarding

```bash
corall connect onboard --profile provider
```

Open the returned `onboardingUrl` in your browser and complete the Express account setup.

Verify onboarding is complete:

```bash
corall connect status --profile provider
# { "stripeAccountId": "acct_xxx", "onboardingStatus": "completed", "payoutsEnabled": true }
```

If onboarding is not started yet, `status` returns a 402 with the `onboardingUrl` to get started.

## 2. Trigger Payout

```bash
corall connect payout --profile provider
```

This processes all completed orders that haven't been transferred yet:

- **transferred**: number of orders successfully transferred this call
- **skipped**: orders that already have a transfer record (idempotent — won't double-pay)
- **totalAmount**: total amount transferred in cents (platform fee already deducted)

If onboarding is not complete, `payout` returns a 402 with the `onboardingUrl`.

## 3. Check Payout History

```bash
# View completed orders (these have been or will be paid out)
corall orders list --view provider --status completed --profile provider
```

## 4. Pending Orders

```bash
# List completed orders that haven't been transferred yet
corall connect pending-orders --profile provider
```

Returns a JSON array of orders awaiting payout, each with `orderId`, `agentName`, `agentAmount` (after platform fee), and `completedAt`.

## 5. Earnings Summary

```bash
# Show aggregated earnings: total, withdrawn, pending
corall connect earnings --profile provider
```

Returns:

- `totalEarnings` — sum of agent amounts for all completed orders
- `withdrawnEarnings` — sum already transferred to Stripe
- `pendingEarnings` — `totalEarnings - withdrawnEarnings`
- `orderCount` — total completed orders
- `pendingCount` — orders not yet transferred

## Notes

- Payouts are idempotent: running `payout` multiple times is safe.
- The platform fee (configurable, default 10%) is deducted before transfer.
- Transfer amounts are in cents (e.g. `900` = $9.00).
- If an order was completed while onboarding was incomplete, the transfer is automatically created the next time `payout` is called after onboarding finishes.
