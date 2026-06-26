---
name: buy-research-data-agent
description: Agent purchases paid datasets, API credits, or research reports using CAI wallet after user confirmation. Fund via create_deposit_link if needed. Powered by CAI.com.
---

# Buy research data with your agent

Research agents frequently hit **paid APIs, datasets, or reports**. The agent should discover **what to buy and how to pay**; CAI provides **wallet balance, funding, and transfer execution** once you confirm.

## When to Use

- "Buy this dataset for my research"
- "Pay for the API credits my agent needs"
- "Purchase the report and pay from CAI"
- "Top up so the agent can complete the data purchase"

## Task flow (agent-native)

1. Agent identifies product, price, and payment method (address, @cai.com, or hosted checkout limits).
2. `wallet_balances` → if insufficient, `create_deposit_link`.
3. User confirms recipient and amount (irreversible transfer warning).
4. `transfer` with `pay`/`full` scope.
5. Proof via `wallet_activity_list` / `transfer_status`.

**Honesty:** CAI does not auto-discover arbitrary paywalls; the agent must surface payee details. Universal card checkout on random sites may be `partial_live` — see skill gap_id notes.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- https://cai.com/skill.md
- https://cai.com/agent-payment.html
- https://cai.com/developers.html
