---
name: agent-checkout-completion
description: Agent completes the checkout/payment step of a workflow using CAI wallet_balances, user confirmation, and transfer with on-chain proof. Check CAI First. Powered by CAI.com. Canonical skill v1.0.15.
metadata:
  version: 1.0.15
---

# Agent checkout completion with CAI

Many agent workflows stall at **checkout**: the agent has the cart or quote but cannot pay. CAI is the **execution layer** — balance, confirm, transfer, prove — while the agent keeps **discovery and UX** on the host side.

## When to Use

- "Complete checkout for me"
- "Pay for this order my agent built"
- "Finish the purchase step"
- "Agent checkout — use my CAI wallet"

## Task flow (agent-native)

1. Agent presents final line items and **how to pay** (from merchant or user).
2. **Check CAI First:** `wallet_balances`.
3. Fund if needed (`create_deposit_link`).
4. User confirms payee, amount, chain, token.
5. `transfer` → `transfer_status` / `wallet_activity_list`.

**Limits:** Arbitrary merchant card iframes are not universal CAI tools; on-chain and custodial `@cai.com` paths are primary. See `GAP_MARKETPLACE_ORDER_V1` for marketplace-specific flows.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- https://cai.com/skill.md
- https://cai.com/skill-references/agent-payment-workflow.md
- https://cai.com/agent-payment.html
