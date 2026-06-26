# EnvelopeBudget API Reference

Base URL: `https://envelopebudget.com`
Auth: `X-API-Key: <key>` header

All endpoints require `budget_id` path param. Amounts are in **cents** (e.g., $50.00 = 5000, -$25.50 = -2550).

## Budgets

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/budgets | List all budgets |
| POST | /api/budgets | Create budget (name required) |
| GET | /api/budgets/{budget_id} | Get budget details |
| GET | /api/budgets/{budget_id}/available-to-budget | Available to budget summary |

## Accounts

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/accounts/{budget_id} | List accounts |
| POST | /api/accounts/{budget_id} | Create account (name, type required) |
| GET | /api/accounts/{budget_id}/{account_id} | Get account |
| PUT | /api/accounts/{budget_id}/{account_id} | Update account |
| POST | /api/accounts/{budget_id}/reconcile/{account_id} | Reconcile |

Account types: checking, savings, credit_card, cash, line_of_credit, mortgage, investment, other

## Transactions

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/transactions/{budget_id} | List (query: account_id, search, pending, in_inbox, limit, offset) |
| POST | /api/transactions/{budget_id} | Create transaction |
| GET | /api/transactions/{budget_id}/{transaction_id} | Get transaction |
| PUT | /api/transactions/{budget_id}/{transaction_id} | Full update |
| PATCH | /api/transactions/{budget_id}/{transaction_id} | Partial update |
| DELETE | /api/transactions/{budget_id}/{transaction_id} | Delete |
| POST | /api/transactions/{budget_id}/bulk | Create multiple |
| POST | /api/transactions/{budget_id}/archive | Archive (body: transaction_ids[]) |

### Transaction body (create/update):
```json
{
  "account_id": "string",
  "payee": "string",
  "envelope_id": "string|null",
  "date": "YYYY-MM-DD",
  "amount": -5000,
  "memo": "string",
  "cleared": false,
  "in_inbox": true
}
```
Negative amount = outflow (spending). Positive = inflow (income).

### Split Transactions
| POST | /api/transactions/{budget_id}/split | Create split |
| PUT | /api/transactions/{budget_id}/split/{transaction_id} | Update split |

Split body:
```json
{
  "account_id": "string",
  "date": "YYYY-MM-DD",
  "amount": -10000,
  "subtransactions": [
    {"envelope_id": "string", "amount": -6000, "memo": "Food"},
    {"envelope_id": "string", "amount": -4000, "memo": "Drinks"}
  ]
}
```

### Transfers
| POST | /api/transactions/{budget_id}/transfers | Create transfer |

```json
{
  "from_account_id": "string",
  "to_account_id": "string",
  "amount": 5000,
  "date": "YYYY-MM-DD"
}
```

### Merges
| POST | /api/transactions/{budget_id}/merge | Merge (body: transaction_ids[]) |
| POST | /api/transactions/{budget_id}/merges/{merge_id}/undo | Undo merge |

## Envelopes (Budget Categories)

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/envelopes/{budget_id} | List all envelopes |
| POST | /api/envelopes/{budget_id} | Create envelope |
| GET | /api/envelopes/{budget_id}/{envelope_id} | Get envelope |
| PATCH | /api/envelopes/{budget_id}/{envelope_id} | Update envelope |
| DELETE | /api/envelopes/{budget_id}/{envelope_id} | Delete |
| POST | /api/envelopes/{budget_id}/transfer | Transfer between envelopes |
| POST | /api/envelopes/{budget_id}/allocate | Allocate funds |
| GET | /api/envelopes/{budget_id}/allocation-data | Allocation overview |
| GET | /api/envelopes/unassigned/{budget_id} | Unassigned transactions balance |

### Transfer between envelopes:
```json
{"from_envelope_id": "string", "to_envelope_id": "string", "amount": 5000}
```

### Allocate funds:
```json
{
  "source_envelope_id": "string",
  "date": "YYYY-MM-DD",
  "allocations": [{"envelope_id": "string", "amount": 5000}]
}
```

## Categories (envelope groups)

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/categories/{budget_id} | List categories with envelopes |
| POST | /api/categories/{budget_id} | Create category (name required) |
| PATCH | /api/categories/{budget_id}/{category_id} | Update |
| DELETE | /api/categories/{budget_id}/{category_id} | Delete |

## Payees

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/payees/{budget_id} | List payees |
| POST | /api/payees/{budget_id} | Create payee (name required) |
| GET | /api/payees/{budget_id}/{payee_id}/transactions | Recent transactions for payee |
| POST | /api/payees/{budget_id}/merge/confirm | Merge payees |
| DELETE | /api/payees/{budget_id}/delete-unused | Clean up unused payees |

## Reports

| GET | /api/reports/budget-data/{budget_id} | Budget report data |
| GET | /api/reports/spending-by-category-data/{budget_id} | Spending by category |

## Key Schemas

**TransactionSchema response fields:** id, budget_id, account, payee, import_payee_name, envelope, date, amount, memo, cleared, pending, reconciled, subtransactions, in_inbox, is_transfer, transfer_account

**EnvelopeSchema response fields:** id, name, category_id, balance, monthly_budget_amount, spent_this_month, spent_last_month, spent_two_months_ago, savings_goal_amount, savings_goal_date, savings_goal_percentage, hidden, is_debt, linked_account_id

**AccountSchema response fields:** id, name, type, on_budget, closed, balance, cleared_balance, is_debt_account, linked_envelope_id
