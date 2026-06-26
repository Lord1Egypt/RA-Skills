---
name: fund-agent-wallet-for-task
description: Fund your CAI custodial wallet so your agent can continue a paid task. Uses create_deposit_link and wallet_balances. No transfer until user is ready. Powered by CAI.com. Canonical skill v1.0.15.
metadata:
  version: 1.0.15
---

# Fund your agent wallet for the next task

Before **book flight**, **buy license**, or **pay OpenRouter**, the agent may detect **insufficient balance**. This skill routes funding through CAI **hosted deposit** — not external wallet hand-holding.

## When to Use

- "Fund my agent wallet so it can continue"
- "I need to top up before the agent pays"
- "Give me a deposit link for my CAI account"
- "Add USDC so my agent can finish the purchase"

## Task flow (agent-native)

1. `wallet_balances` on required chain/token.
2. If short → `create_deposit_link` (`action_type: deposit`) with optional `constraints` (chain, `payment_method`, asset hints).
3. Return Hosted action URL (`url`) to user; wait for funding.
4. Re-check `wallet_balances` before any `transfer`.
5. Continue parent task skill (payment, license, etc.).

**Honesty:** Deposit indexing may be `partial_live` — use `wallet_deposit_confirm` if user supplies tx hash.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- https://cai.com/skill.md §1 create_deposit_link
- https://cai.com/developers.html
