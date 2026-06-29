---
name: deepread-bank-statements
title: DeepRead Bank Statements
description: Extract structured data from bank statements — account holder, period, opening/closing balances, and every transaction as typed JSON. Works on PDF and scanned statements from any bank. Per-field confidence flags. PII redaction for compliant sharing. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Bank Statements

Turn any bank statement — PDF export or scanned/photographed — into clean, typed JSON: account holder, statement period, opening and closing balances, and a row-by-row transaction list with dates, descriptions, amounts, and running balances. Every field comes back with a `needs_review` flag so you know exactly what to trust and what to double-check.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## Why this is hard (and why DeepRead handles it)

Bank statements are the worst of OCR: dense tables, multi-page transaction runs, inconsistent layouts across thousands of banks, credits and debits in separate columns, and running balances that have to reconcile. A single-model OCR pass silently drops rows or flips a debit into a credit. DeepRead runs **multi-model consensus** (GPT + Gemini + an LLM judge), returns a confidence flag per field, and lets you reconcile against the stated opening/closing balances.

## What You Get Back

Submit a statement PDF, get structured JSON. Extracted fields come back under `extraction.fields[]` (each with `key`, `value`, `needs_review`, `location.page`):

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "account_holder", "value": "Jordan Rivera", "needs_review": false, "location": {"page": 1}},
      {"key": "bank_name", "value": "First National Bank", "needs_review": false, "location": {"page": 1}},
      {"key": "account_number_masked", "value": "****4821", "needs_review": false, "location": {"page": 1}},
      {"key": "statement_period_start", "value": "2026-03-01", "needs_review": false, "location": {"page": 1}},
      {"key": "statement_period_end", "value": "2026-03-31", "needs_review": false, "location": {"page": 1}},
      {"key": "opening_balance", "value": 4210.55, "needs_review": false, "location": {"page": 1}},
      {"key": "closing_balance", "value": 3987.12, "needs_review": false, "location": {"page": 1}},
      {"key": "transactions", "value": [
        {"date": "2026-03-02", "description": "ACH PAYROLL ACME CORP", "amount": 2500.00, "type": "credit", "balance": 6710.55},
        {"date": "2026-03-05", "description": "CARD PURCHASE - WHOLE FOODS", "amount": -82.41, "type": "debit", "balance": 6628.14},
        {"date": "2026-03-15", "description": "MORTGAGE - HOMEFIRST", "amount": -1840.00, "type": "debit", "balance": 4788.14}
      ], "needs_review": false, "location": {"page": 1}}
    ]
  },
  "review": {"needs_review": false, "fields_total": 8, "fields_needing_review": 0, "review_rate": 0.0}
}
```

## Setup

### Get Your API Key

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
```

Save it:
```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

No key yet? Install `deepread-agent-setup` and your agent fetches one via OAuth device flow — no copy/paste:
```bash
clawhub install uday390/deepread-agent-setup
```

## Bank Statement Schema

Pre-built schema covering the fields common to most statements. The `transactions` array is the heart of it — each row is extracted as a typed object.

```json
{
  "type": "object",
  "properties": {
    "bank_name":      {"type": "string", "description": "Name of the bank or financial institution"},
    "account_holder": {"type": "string", "description": "Full name of the account holder"},
    "account_number_masked": {"type": "string", "description": "Account number, masked except last 4 digits"},
    "account_type":   {"type": ["string", "null"], "description": "Checking, savings, credit, etc."},
    "currency":       {"type": "string", "description": "Currency code (USD, EUR, GBP, INR, ...)"},
    "statement_period_start": {"type": "string", "description": "Statement start date (YYYY-MM-DD)"},
    "statement_period_end":   {"type": "string", "description": "Statement end date (YYYY-MM-DD)"},
    "opening_balance": {"type": "number", "description": "Balance at the start of the period"},
    "closing_balance": {"type": "number", "description": "Balance at the end of the period"},
    "total_deposits":  {"type": ["number", "null"], "description": "Sum of all credits, if stated"},
    "total_withdrawals": {"type": ["number", "null"], "description": "Sum of all debits, if stated"},
    "transactions": {
      "type": "array",
      "description": "Every transaction line on the statement, in order",
      "items": {
        "type": "object",
        "properties": {
          "date":        {"type": "string", "description": "Transaction date (YYYY-MM-DD)"},
          "description": {"type": "string", "description": "Transaction description / payee as printed"},
          "amount":      {"type": "number", "description": "Signed amount: negative for debits, positive for credits"},
          "type":        {"type": "string", "description": "'debit' or 'credit'"},
          "balance":     {"type": ["number", "null"], "description": "Running balance after this transaction, if shown"}
        },
        "required": ["date", "description", "amount"]
      }
    }
  }
}
```

## Extract a Bank Statement

### Python

```python
import requests, json, time

API_KEY = "sk_live_YOUR_KEY"
BASE = "https://api.deepread.tech"
headers = {"X-API-Key": API_KEY}

schema = json.dumps({
    "type": "object",
    "properties": {
        "bank_name": {"type": "string", "description": "Bank or institution name"},
        "account_holder": {"type": "string", "description": "Account holder full name"},
        "statement_period_start": {"type": "string", "description": "Start date YYYY-MM-DD"},
        "statement_period_end": {"type": "string", "description": "End date YYYY-MM-DD"},
        "opening_balance": {"type": "number", "description": "Opening balance"},
        "closing_balance": {"type": "number", "description": "Closing balance"},
        "transactions": {
            "type": "array",
            "description": "Every transaction line, in order",
            "items": {"type": "object", "properties": {
                "date": {"type": "string", "description": "YYYY-MM-DD"},
                "description": {"type": "string", "description": "Payee / description"},
                "amount": {"type": "number", "description": "Signed: negative=debit, positive=credit"},
                "balance": {"type": ["number", "null"], "description": "Running balance if shown"}
            }, "required": ["date", "description", "amount"]}
        }
    }
})

with open("statement.pdf", "rb") as f:
    job = requests.post(f"{BASE}/v1/process", headers=headers,
                        files={"file": f}, data={"schema": schema}).json()

job_id = job["id"]
delay = 5
while True:
    time.sleep(delay)
    result = requests.get(f"{BASE}/v1/jobs/{job_id}", headers=headers).json()
    if result["status"] in ("completed", "failed"):
        break
    delay = min(delay * 1.5, 20)

if result["status"] == "completed":
    by_key = {f["key"]: f["value"] for f in result["extraction"]["fields"]}
    txns = by_key.get("transactions", [])
    print(f"{by_key.get('account_holder')} — {len(txns)} transactions")

    # Reconcile: opening + sum(amounts) should equal closing
    opening = by_key.get("opening_balance", 0)
    closing = by_key.get("closing_balance", 0)
    computed = round(opening + sum(t["amount"] for t in txns), 2)
    if abs(computed - closing) > 0.01:
        print(f"⚠ RECONCILE MISMATCH: computed {computed} vs stated {closing} — review extraction")
    else:
        print("✓ reconciles to stated closing balance")
```

### cURL

```bash
curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@statement.pdf" \
  -F 'schema={"type":"object","properties":{"account_holder":{"type":"string"},"closing_balance":{"type":"number"},"transactions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string"},"description":{"type":"string"},"amount":{"type":"number"}}}}}}'
```

## Reconciliation: your built-in accuracy check

Bank statements have a property most documents don't: they **must** balance. `opening_balance + Σ(transaction amounts) == closing_balance`. Always run this check (see the Python example). If it doesn't reconcile, a row was misread — combine it with the `needs_review` flags to find exactly which line to fix. This turns "97% accurate" into "provably correct or flagged."

## Use Cases

- **Lending / underwriting** — pull income deposits and recurring obligations to assess affordability
- **Accounting & bookkeeping** — import transactions into QuickBooks/Xero without manual keying
- **Personal finance apps** — onboard users by statement upload instead of fragile bank screen-scraping
- **Cash-flow analysis** — categorize and trend transactions across months
- **Audit & forensics** — extract and reconcile statements at scale with confidence flags

## Compliant Sharing — Redact First

Bank statements are loaded with PII (names, account numbers, addresses). Before sharing externally or sending to another model, redact with `deepread-pii`:

```bash
curl -X POST https://api.deepread.tech/v1/pii/redact \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@statement.pdf"
```

Install it: `clawhub install uday390/deepread-pii`

## Tips for Best Accuracy

- **Always reconcile** opening + transactions == closing (shown above) — it's free verification.
- **Use signed amounts** (negative for debits) so reconciliation math just works.
- **Recurring bank/format?** Turn this schema into a blueprint at `https://www.deepread.tech/dashboard/optimizer` for a 20–30% accuracy lift on that bank's layout.
- **Multi-page statements** are handled automatically; transactions come back in document order.
- **Check `needs_review`** — only flagged fields need a human; the rest auto-process.

## BYOK — Zero Processing Costs

Connect your own OpenAI, Google, or OpenRouter key in the dashboard. All processing routes through your provider — zero DeepRead LLM costs, page quota skipped. Set it up: https://www.deepread.tech/dashboard/byok

## Related DeepRead Skills

- **deepread-ocr** — general OCR + structured extraction — `clawhub install uday390/deepread-ocr`
- **deepread-invoice** — invoices, receipts, bills — `clawhub install uday390/deepread-invoice`
- **deepread-pii** — redact sensitive data before sharing — `clawhub install uday390/deepread-pii`
- **deepread-byok** — bring your own AI key — `clawhub install uday390/deepread-byok`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Issues**: https://github.com/deepread-tech/deep-read-service/issues
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
