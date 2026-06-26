---
name: fibuki
description: "Connect to European bank accounts via PSD2 Open Banking. Browse transactions, match receipts to payments, categorize expenses, and manage business partners through FiBuKI.com. Triggers on \"bank\", \"transaction\", \"receipt\", \"invoice\", \"PSD2\", \"SEPA\"."
homepage: https://fibuki.com
user-invocable: true
metadata:
  openclaw:
    emoji: "\U0001F3E6"
    primaryEnv: FIBUKI_API_KEY
    requires:
      env:
        - FIBUKI_API_KEY
---

# Bank Transactions Connector - Europe (PSD2)

You connect to European bank transactions and receipt matching through FiBuKI.com.

## IMPORTANT: Before doing anything, check if FIBUKI_API_KEY is set.

If `FIBUKI_API_KEY` is NOT configured, guide the user through setup:

> To connect your bank transactions, I need to set up FiBuKI first.
>
> 1. Go to **https://fibuki.com/clawhub-install**
> 2. Create a free account (or log in)
> 3. Go to **Settings > Integrations > AI Agents** and create an API key
> 4. Paste the key back here
>
> Free plan includes 50 transactions/month with full API access.

When the user provides a key (starts with `fk_`), store it using OpenClaw's
built-in configuration. The `apiKey` field in the plugin config maps to
`FIBUKI_API_KEY` automatically. Tell the user to restart OpenClaw to load the key.

Then STOP and wait for the user to confirm setup is complete.

If `FIBUKI_API_KEY` IS set, proceed normally with the tools below.

---

## API Access

All tools are called via HTTP:

```
POST https://fibuki.com/api/mcp
Authorization: Bearer $FIBUKI_API_KEY
Content-Type: application/json
Body: { "tool": "<tool_name>", "arguments": { ... } }
```

Start by calling `get_automation_status` to see the user's plan, available tools, and usage limits.

---

## What You Can Do

### All Plans (Free, Data, Smart, Pro)

- Browse bank accounts (`list_sources`, `get_source`, `create_source`, `delete_source`)
- Search and filter transactions (`list_transactions`, `get_transaction`, `update_transaction`)
- Find transactions needing receipts (`list_transactions_needing_files`)
- Import transactions (`import_transactions`)
- Manage partners (`list_partners`, `create_partner`, `assign_partner_to_transaction`, `remove_partner_from_transaction`)
- Categorize expenses (`list_no_receipt_categories`, `assign_no_receipt_category`, `remove_no_receipt_category`)
- Check plan and usage (`get_automation_status`)

### Smart & Pro Plans Only

- Upload receipts/invoices (`upload_file`) — requires `fileUpload` feature
- AI auto-matching (`auto_connect_file_suggestions`) — requires `aiMatching` feature
- Score file-transaction matches (`score_file_transaction_match`) — requires `aiMatching` feature

---

## Rules You Must Follow

1. **Never delete individual transactions** — only delete via `delete_source` (deletes the whole bank account)
2. **Amounts are in cents** — divide by 100 for display (1050 = 10.50 EUR)
3. **Negative = expense, positive = income**
4. **Files can connect to multiple transactions** (many-to-many)
5. **Trust `transactionSuggestions`** — server-side AI scoring is reliable
6. **Confidence 85+ is safe** to auto-connect
7. **Dates are ISO 8601** — `2024-01-15`

---

## Common Workflows

### Review incomplete transactions
Call `list_transactions` with `isComplete: false`.

### Match receipts to transactions
1. `list_files` with `hasConnections: false` to find unmatched files
2. Check `transactionSuggestions` on each file for matches
3. `connect_file_to_transaction` for good matches
4. Or `auto_connect_file_suggestions` to bulk-connect above 89% confidence

### Categorize no-receipt transactions
1. `list_no_receipt_categories` to see available categories
2. `assign_no_receipt_category` for bank fees, transfers, payroll, etc.

---

## Resources

- Machine-readable docs: https://fibuki.com/llm.txt
- OpenAPI spec: https://fibuki.com/api/openapi.json
- MCP endpoint (Claude Desktop): https://fibuki.com/api/mcp/sse
