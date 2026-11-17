---
name: bankconv
description: Convert PDF bank and credit card statements into clean transactions (JSON) or CSV, OFX, QFX, QBO and Xero CSV files with the BankConv API. Use when the user wants to read, analyse, total or import the transactions in a bank statement PDF, or needs a file for Excel, QuickBooks, Xero, Quicken, MYOB or Sage.
version: 0.1.1
license: MIT
metadata:
  openclaw:
    requires:
      env: [BANKCONV_API_KEY]
    primaryEnv: BANKCONV_API_KEY
    homepage: https://bankconv.com/integrations/mcp
---

# BankConv: bank statement PDFs to transactions and accounting files

BankConv reads the transaction tables in a PDF bank or credit card statement and returns clean transactions: ISO dates, one signed amount (money in positive, money out negative) and the running balance, with opening balances and total lines left out. It also writes CSV, OFX, QFX, QBO and Xero CSV files. It reads scanned and password-protected PDFs.

If the `bankconv` MCP server is connected, use its tools (`convert_statement`, `get_transactions`, `download_statement`, `list_conversions`, `get_credits`) instead of the steps below.

## Before you start

- The API key is in `BANKCONV_API_KEY`. If it is missing, ask the user to create one at https://app.bankconv.com/teams/api-keys. Never print the key.
- Each PDF page uses one page of the user's BankConv account. Before converting many files, check the balance: `GET /credits`.
- Base URL: `https://bankconv.com/api/v1`. Send `Authorization: Bearer $BANKCONV_API_KEY` and `Accept: application/json` on every request.

## Convert a statement

1. Upload the PDF (add `-F "password=…"` only if the user gave a PDF password):

   ```bash
   curl -s -X POST https://bankconv.com/api/v1/conversions \
     -H "Authorization: Bearer $BANKCONV_API_KEY" -H "Accept: application/json" \
     -F "file=@statement.pdf"
   ```

   Keep `data.id` from the response.

2. Poll every 3 seconds until `data.status` is `completed`:

   ```bash
   curl -s https://bankconv.com/api/v1/conversions/$ID \
     -H "Authorization: Bearer $BANKCONV_API_KEY" -H "Accept: application/json"
   ```

   Stop on `failed` (the PDF couldn't be converted) or `no_credits` (the account needs pages; https://app.bankconv.com/plans).

3. Get what the user needs:
   - **To analyse or answer questions:** `GET /conversions/$ID/transactions`. It returns the bank, account, period, currency and a `transactions` array.
   - **To save a file:** `GET /conversions/$ID/download?format=FORMAT -o FILE`, where FORMAT is from the table below. For CSV use `format=csv&view=merged`. The `X-BankConv-Warnings` header lists warnings as a JSON array; tell the user about them.

   If either call answers `422` with `error.code` = `not_ready`, the statement details are still being read. Wait 5 seconds and retry, for up to 5 minutes.

## Which format

| The user wants | format | Save as |
|---|---|---|
| Excel, Google Sheets, most software | `csv` (with `view=merged`) | `.csv` |
| Xero, MYOB, Sage, QuickBooks Online, no column mapping | `ofx` | `.ofx` |
| Quicken | `qfx` | `.qfx` |
| QuickBooks Desktop (Web Connect) | `qbo` | `.qbo` |
| Xero's own CSV columns | `xero` | `-xero.csv` |

## Errors

Errors look like `{"error": {"code": "...", "message": "..."}}`. Tell the user the message. Common codes: `unauthenticated` (bad key), `insufficient_credits` (not enough pages), `unreadable_statement` (the tables can't be read as transactions; the message names the row), `gone` (deleted under data retention, 24 hours by default).

## Privacy

The PDF goes to BankConv over HTTPS and is deleted after 24 hours by default. Only upload files the user asked you to convert. Full API reference: https://bankconv.com/api-docs
