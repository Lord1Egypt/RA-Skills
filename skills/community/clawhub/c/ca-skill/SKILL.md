---
emoji: 🧾
name: tally-prime-ca
version: 1.0.6
author: Maxxit
description: >-
  Full-service CA skill for TallyPrime running locally. Read accounting reports
  (day book, trial balance, P&L, balance sheet, outstandings, GST) and post or
  update vouchers (purchase/sales/payment/receipt/journal, credit note, debit
  note, contra) via TallyPrime XML-over-HTTP. Use when the user mentions Tally,
  accounting entries, invoices/bills, ledgers, outstanding, GST, returns, or
  financial statements.
disableModelInvocation: false
requires:
  env:
    - TALLY_URL
metadata:
  openclaw:
    requiredEnv:
      - TALLY_URL
    bins:
      - curl
    primaryCredential: TALLY_URL
---

# TallyPrime (CA) Skill

Connect to a **locally running** TallyPrime instance via its **XML-over-HTTP** interface. All requests are HTTP POST to `$TALLY_URL` (commonly `http://localhost:9000`) with an XML body.

- **No cloud API**: TallyPrime must be open/running on the user’s machine.
- **Multi-company**: Always use the correct `SVCURRENTCOMPANY` (exact spelling).

## Hero Use Case: WhatsApp invoice → Tally entry

Goal: zero manual entry for CAs handling many clients.

1. Read bill/invoice (PDF/image) and extract: company, party, GSTIN, date, invoice no, taxable, tax, total, ledger mapping.
2. Ensure masters exist: party ledger, purchase/sales ledger, GST ledger(s), bank/cash ledger (if needed).
3. Post voucher with a **unique GUID**.
4. Confirm a summary back to the user.

## When to use this skill

Use when the user asks to:

- Post entries: purchase, sales, receipt, payment, journal, contra, credit note, debit note
- Check reports: day book, trial balance, balance sheet, profit & loss, ledger statement, outstandings, GST
- Manage masters: create/alter ledgers, groups, stock items/UOM (inventory clients)
- Fix data: alter or cancel a voucher

## Critical rules (must follow)

1. **Never assume company**: if not explicit, ask which company to use before posting.
2. **Never guess ledgers**: verify ledgers exist before voucher import; create missing masters first.
3. **Dates are `YYYYMMDD`** (no separators).
4. **Idempotency**: always set a stable unique `GUID` per voucher to prevent duplicates on retries.
5. **Balance vouchers**: total debits must equal total credits (Tally error: “Voucher totals do not match!”).
6. **Escape XML**: narration/party names may contain `&` → use `&amp;` in XML.
7. **Posting is write operation**: confirm intent (and company) before any create/alter/cancel.
8. **Prefer bill-wise allocations** for party ledgers to keep outstandings correct (see `reference/vouchers.md`).
9. **Accounting-only vouchers (no inventory items)**: set `<ISINVOICE>No</ISINVOICE>` and place the **party ledger entry first** in the `ALLLEDGERENTRIES.LIST` sequence. This makes the Day Book "Particulars" column show the party name (not the expense/purchase ledger) and defaults the voucher to the clean "As Voucher" view. Only use `ISINVOICE=Yes` for item invoices that go through `reference/inventory.md`.
10. **Accounting Invoice Mode — always use `LEDGERENTRIES.LIST`**: when `OBJVIEW="Invoice Voucher View"` is set (Modes 1 and 2 in `reference/vouchers.md`), every ledger block **must** use `<LEDGERENTRIES.LIST>`, not `<ALLLEDGERENTRIES.LIST>`. Tally silently ignores `ALLLEDGERENTRIES` in this view, causing the voucher to be saved with no entries and the error "No accounting or inventory entries are available."
11. **Voucher class decision — confirm before posting**: before posting any Purchase or Sales voucher, check whether the company's voucher type uses a class for GST splitting. Run the preflight checklist in the "Preflight checklist before posting" section below. If class mode is confirmed, set `<CLASSNAME>EXACT_CLASS_NAME</CLASSNAME>` in the voucher header and include all four GST header fields (`CMPGSTIN`, `PARTYGSTIN`, `GSTREGISTRATIONTYPE`, `PLACEOFSUPPLY`). **If class existence is unconfirmed, stop and ask — do not post without it.** Full decision rules and templates are in the "Voucher class — decision rules" section of `reference/vouchers.md`.

## Preflight checklist before posting

Run through every item before sending any Create/Alter/Delete request. **Stop at the first unresolved item and ask the user.**

| # | Check | How to verify | Block if… |
|---|---|---|---|
| 1 | **Company confirmed** | User stated it explicitly | Name not given — ask |
| 2 | **Server reachable** | `curl -s --max-time 5 "$TALLY_URL"` | No response / wrong port |
| 3 | **Voucher type uses a class?** | Export voucher type masters or ask user | Unknown — ask before posting |
| 4 | **Class name confirmed** (if class mode) | List voucher type via masters export; match exact class name in Tally | Class not found — ask, never guess |
| 5 | **Party ledger exists** | Ledger existence check (`reference/masters.md`) | Missing — create first |
| 6 | **Purchase/Sales/GST ledgers exist** | Same as above | Missing — create first |
| 7 | **GST header fields available** (if class mode) | `CMPGSTIN`, `PARTYGSTIN`, `GSTREGISTRATIONTYPE`, `PLACEOFSUPPLY` | Any missing — ask user |
| 8 | **Voucher totals balance** | Sum all `AMOUNT` values = 0 | Mismatch — fix before posting |

## Step 0: Check TallyPrime server

```bash
curl -s --max-time 5 "$TALLY_URL"
```

Expected (example):

```xml
<RESPONSE>TallyPrime Server is Running</RESPONSE>
```

If not running, stop and ask user to open TallyPrime and enable integrations for the port.

## Step 1: Company context

If the user did not specify company, ask. If they did, use **exact** name in `SVCURRENTCOMPANY`.

To list companies, use the template in `reference/reports.md` (“Company list”).

## Step 2: Verify/create required ledgers (masters)

Ledger existence checks and master creation templates are in `reference/masters.md` (includes ledgers, groups, GST/address fields, and party ledger creation with required field prompts).

**New company?** Run the "New Company Setup — Standard GST Ledgers" block in `reference/masters.md` first. It creates the seven minimum ledgers every GST-registered company needs:

| # | Ledger | Type |
|---|---|---|
| 1 | `Input Sgst @ 9 %` | Input GST |
| 2 | `Input Cgst @ 9 %` | Input GST |
| 3 | `Input IGST @ 18 %` | Input GST |
| 4 | `Purchase @ 18 %` | Purchase ledger |
| 5 | `Round Off` | Rounding |
| 6 | `Output Sgst @ 9 %` | Output GST |
| 7 | `Output Cgst @ 9 %` | Output GST |

Quick group defaults (common CA mapping):

| Ledger type | Parent group |
|---|---|
| Customer | `Sundry Debtors` |
| Vendor | `Sundry Creditors` |
| Sales | `Sales Accounts` |
| Purchases/Expenses | `Purchase Accounts` / `Direct Expenses` / `Indirect Expenses` |
| Bank | `Bank Accounts` |
| Cash | `Cash-in-Hand` |
| GST | `Duties & Taxes` |

## Step 3: Post vouchers (core)

Use `REPORTNAME=Vouchers` and always include `GUID`, `DATE`, and `VOUCHERTYPENAME`. Full templates (including bill-wise allocations, returns, contra) are in `reference/vouchers.md`.

Supported voucher types in this skill:

- Purchase, Sales, Payment, Receipt, Journal
- Credit Note, Debit Note
- Contra
- Voucher Alteration + Cancellation

## Read reports (core)

Use `TALLYREQUEST=Export` / `REPORTNAME=...` with `SVEXPORTFORMAT=$$SysName:XML`. Full templates are in `reference/reports.md`.

Common CA reports:

- Day Book (period)
- Trial Balance (period)
- Balance Sheet
- Profit and Loss
- Ledger Vouchers (ledger statement)
- Bills Receivable / Bills Payable (outstandings)
- Ledger Outstandings / Group Outstandings
- GST: GSTR-1 and related summaries (plus GSTR-3B where available)
- Stock Summary (inventory clients)

## Suggested GUID pattern

Use a deterministic pattern when invoice number exists:

```
{companyShort}-{voucherType}-{voucherNumber}-{date}
```

Examples:

- `abc-purchase-ril2026-00123-20260115`
- `abc-creditnote-cn09-20260302`

## Multi-company CA workflow (recommended)

1. Capture company name early (and confirm spelling).
2. Validate connectivity.
3. Fetch required ledgers/masters or create them.
4. Only then post the voucher.
5. Reply with: company, voucher type, voucher number, date, amount breakdown, and whether any masters were created.

## Advanced reference

- Reports and data export: `reference/reports.md`
- Voucher templates (including Debit/Credit Note, Contra, bill-wise allocations, alter/cancel): `reference/vouchers.md`
- Masters (ledgers/groups + GST/address, alteration): `reference/masters.md`
- Inventory (stock groups/items/UOM, item invoices): `reference/inventory.md`
- Error handling and troubleshooting: `reference/errors.md`
