---
name: envelopebudget
description: Manage budgets, transactions, accounts, envelopes, and payees via the EnvelopeBudget.com API. Use when user asks about: (1) checking balances or budget status, (2) listing/creating/updating transactions, (3) managing envelopes (budget categories), (4) account balances or reconciliation, (5) transferring money between accounts or envelopes, (6) spending reports or category breakdowns, (7) payee management, (8) anything related to budgeting, expenses, or financial tracking in EnvelopeBudget.
metadata: {"openclaw":{"emoji":"💰","primaryEnv":"ENVELOPE_BUDGET_API_KEY","requires":{"bins":["curl","python3"],"env":["ENVELOPE_BUDGET_API_KEY"]},"homepage":"https://envelopebudget.com","source":"https://github.com/envelope-budget/monolith"}}
---

# EnvelopeBudget

Query and manage budgets on [EnvelopeBudget.com](https://envelopebudget.com) via REST API.

## Setup

- Requires env: `ENVELOPE_BUDGET_API_KEY`
- API reference: see [references/api-reference.md](references/api-reference.md)

## Usage

Use the helper script for all API calls:

```bash
scripts/eb_api.sh <METHOD> <path> [json_body]
```

### Common workflows

**Check budget overview:**
```bash
scripts/eb_api.sh GET /api/budgets
scripts/eb_api.sh GET /api/budgets/BUDGET_ID/available-to-budget
```

**List recent transactions:**
```bash
scripts/eb_api.sh GET "/api/transactions/BUDGET_ID?limit=20"
scripts/eb_api.sh GET "/api/transactions/BUDGET_ID?search=grocery&limit=10"
```

**Add a transaction (amounts in cents, negative = spending):**
```bash
scripts/eb_api.sh POST /api/transactions/BUDGET_ID \
  '{"account_id":"ACCT_ID","payee":"Costco","envelope_id":"ENV_ID","date":"2026-03-06","amount":-8500,"memo":"Groceries"}'
```

**Check envelope balances:**
```bash
scripts/eb_api.sh GET /api/envelopes/BUDGET_ID
```

**Transfer between envelopes:**
```bash
scripts/eb_api.sh POST /api/envelopes/BUDGET_ID/transfer \
  '{"from_envelope_id":"FROM_ID","to_envelope_id":"TO_ID","amount":5000}'
```

**Spending report:**
```bash
scripts/eb_api.sh GET /api/reports/spending-by-category-data/BUDGET_ID
```

## Important notes

- **Amounts are in cents**: $50.00 = 5000, -$25.50 = -2550
- **Negative = outflow** (spending), **Positive = inflow** (income)
- Always fetch budgets first to get `budget_id`, then accounts/envelopes for their IDs
- For full API details: read [references/api-reference.md](references/api-reference.md)
