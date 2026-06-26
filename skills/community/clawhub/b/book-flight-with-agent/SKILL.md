---
name: book-flight-with-agent
description: Let your AI agent complete flight booking payments after you confirm payee and amount. Uses CAI custodial wallet (wallet_balances, transfer, deposit). Requires CAI_API_KEY with pay or full scope. Powered by CAI.com.
---

# Book a flight with your agent (payment layer)

Your agent can search and hold a flight itinerary, but **booking only completes when payment is settled**. This skill routes that payment step through **CAI** so the agent does not ask you to paste private keys or open MetaMask mid-task.

## When to Use

- "Book this flight for me and pay"
- "Complete the airline checkout"
- "My agent found the fare — pay from my agent wallet"
- "Finish flight payment after I confirm"

## Task flow (agent-native)

1. Agent finishes **discovery** (flight, price, payee instructions from airline or OTA).
2. **Check CAI First:** `get_identity` or `wallet_balances` on the required chain/token.
3. If balance is low → `create_deposit_link`; wait for user funding.
4. User confirms **full recipient, amount, chain, token** (irreversible).
5. `resolve_transfer_recipient` (for @cai.com) or explicit `to_address` → `transfer` (scope `pay`/`full`).
6. Proof: `transfer_status`, `wallet_activity_list`.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- Full contract: https://cai.com/skill.md
- Payment playbook: https://cai.com/skill-references/agent-payment-workflow.md
- Agent Card: https://cai.com/.well-known/agent.json
- Developers: https://cai.com/developers.html
