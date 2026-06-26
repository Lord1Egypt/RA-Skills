---
name: bank-reconciliation-agent
description: >
  Automate bank statement reconciliation against general ledger records. Upload or paste bank statements (CSV, OFX,
  QFX, or plain text) alongside GL export data, and the agent matches transactions, flags discrepancies, identifies
  unrecorded items, and produces a reconciliation report ready for sign-off. Supports multi-bank, multi-account
  reconciliation with adjusting entry suggestions. Integrates with QBO exports and standard GL formats.
  Use when: monthly close reconciliation, bank statement upload matching, investigating GL/bank discrepancies,
  catching duplicate payments, finding missed deposits, or producing the reconciliation worksheet for audit.
  NOT for: real-time bank feed automation (use QBO bank rules), tax preparation, payroll reconciliation,
  intercompany eliminations, or investment account reconciliation (brokerage/crypto — use crypto-tax-agent).
version: 1.0.0
author: PrecisionLedger
tags:
  - accounting
  - reconciliation
  - bank
  - close
  - audit
  - qbo
  - finance
---

# Bank Reconciliation Agent

Automated bank-to-GL reconciliation with discrepancy detection, adjusting entry suggestions, and audit-ready output.

## What It Does

- **Match** bank statement transactions to GL entries by date, amount, and reference
- **Flag** unmatched items on either side (bank not in GL, GL not in bank)
- **Identify** common issues: duplicates, reversed transactions, timing differences, bank errors
- **Suggest** adjusting journal entries for unrecorded bank items (NSF fees, interest, service charges)
- **Produce** a formatted reconciliation worksheet (balance reconciliation + item detail)
- **Export** results as structured data (CSV/JSON) or formatted text report

## Trigger Phrases

- "reconcile the bank statement"
- "match transactions for [account] in [month]"
- "find the difference between bank and GL"
- "I have a $X discrepancy in my checking account"
- "run month-end bank rec for [entity]"
- "upload bank CSV and reconcile"

## Required Inputs

**Bank Statement Data** (any of):
- CSV export from bank portal
- OFX/QFX file
- Pasted tabular data (date, description, amount)
- PDF statement (agent will extract tabular data)

**GL / Book Data** (any of):
- QBO transaction export (CSV)
- Journal entry list from accounting software
- Excel/Sheets ledger extract

**Account Info:**
- Bank account name and number (last 4 digits)
- Entity/company name
- Reconciliation period (month/year)
- Beginning balance (statement) and ending balance (statement)
- Book balance as of period end

## Reconciliation Workflow

### Step 1 — Parse & Normalize

```
Parse bank statement → normalize to: {date, description, amount, type}
Parse GL data → normalize to: {date, memo, debit, credit, account}
Convert debits/credits to signed amounts for matching
```

### Step 2 — Match Transactions

**Matching priority (in order):**
1. Exact match: date + amount + description keyword overlap
2. Fuzzy date (±3 days) + exact amount (common for ACH timing)
3. Amount-only match within date window (flag for manual review)
4. Partial matches flagged as "possible match — confirm"

**Match confidence levels:**
- ✅ Confirmed: exact date + amount
- 🟡 Probable: fuzzy date or partial description
- 🔴 Unmatched: no candidate found

### Step 3 — Reconciliation Calculation

```
Bank Statement Ending Balance:           $XX,XXX.XX
+ Deposits in Transit (GL not on stmt):  +$X,XXX.XX
- Outstanding Checks (GL not on stmt):   -$X,XXX.XX
= Adjusted Bank Balance:                 $XX,XXX.XX

Book Balance per GL:                     $XX,XXX.XX
+ Add: Bank items not in books:          +$XXX.XX
  (interest income, credits)
- Less: Bank items not in books:         -$XXX.XX
  (NSF fees, service charges, errors)
= Adjusted Book Balance:                 $XX,XXX.XX

Difference: $0.00 ← Target
```

### Step 4 — Discrepancy Analysis

If difference ≠ $0, the agent performs:
- **Transposition check:** look for amounts where digits are swapped (e.g., $1,872 vs $1,782)
- **Duplicate detection:** same amount hitting both sides twice
- **Missing transaction scan:** amounts that sum to the difference
- **Rounding error check:** differences of $0.01–$0.10 often rounding
- **Date boundary check:** items crossing month-end

### Step 5 — Output

**Reconciliation Worksheet:**
```
BANK RECONCILIATION
Entity: [Company Name]
Account: [Bank Name] – Checking (...1234)
Period: [Month Year]
Prepared by: [Agent] | Date: [Today]

BANK BALANCE RECONCILIATION
  Statement Ending Balance:      $50,000.00
  Add: Deposits in Transit
    03/28 ACH Deposit – Client A   $5,200.00
  Less: Outstanding Checks
    Ck #1042 – Vendor B           ($1,800.00)
    Ck #1047 – Vendor C             ($450.00)
  Adjusted Bank Balance:         $52,950.00

BOOK BALANCE RECONCILIATION
  GL Ending Balance:             $52,875.00
  Add: Bank Interest Income          $75.00
  Less: NSF Fee – Check #891           $0.00
  Adjusted Book Balance:         $52,950.00

DIFFERENCE:                           $0.00 ✅

UNMATCHED ITEMS (require action):
[See detail tab]
```

## Adjusting Journal Entry Templates

For each unrecorded bank item, the agent generates:

**Bank Service Charge:**
```
DR  Bank Charges Expense   $XX.XX
  CR  Checking Account         $XX.XX
Memo: Bank service charge per [Month] statement
```

**Interest Income:**
```
DR  Checking Account       $XX.XX
  CR  Interest Income           $XX.XX
Memo: Bank interest per [Month] statement
```

**NSF Check Returned:**
```
DR  Accounts Receivable    $XX.XX
  CR  Checking Account         $XX.XX
Memo: NSF – [Customer] check #[XXX] returned [date]
```

## Multi-Account Reconciliation

For entities with multiple bank accounts:

```
Reconcile [Checking – BoA ...1234] ✅
Reconcile [Savings – BoA ...5678] ✅
Reconcile [Payroll – Chase ...9012] 🔴 $234 discrepancy
  → Likely: ADP fee not recorded (check Jan statement)
```

Run as batch:
> "Reconcile all three accounts for February. Bank CSVs are attached, QBO export is in the second file."

## QBO Integration

When GL data comes from QuickBooks Online:

1. **Export from QBO:** Reports → Custom Reports → Transaction Detail → filter by account + date range → export CSV
2. **Feed to agent:** "Here's the QBO export and the bank statement for March. Reconcile them."
3. **Agent maps:** QBO columns (Date, Transaction Type, Num, Name, Memo, Amount) → standard format
4. **Output:** Reconciliation worksheet + list of entries to record in QBO

## Common Discrepancy Patterns

| Pattern | Likely Cause | Fix |
|---|---|---|
| Round number difference ($100, $500) | Missing transaction | Search GL/bank for that amount |
| Off by 9 ($9, $90, $900) | Transposition error | Check digit order in data entry |
| Small difference (<$1) | Rounding | Verify import format (2 vs 3 decimal places) |
| Recurring same amount | Duplicate entry | Check for double-import of data |
| Difference = sum of items | Multiple unrecorded | Review bank items not in GL |
| Same difference each month | Systematic error | Check prior month carry-forward |

## Negative Boundaries (When NOT to Use)

- **Real-time bank feed matching** → Use QBO bank rules (automated), not this skill
- **Payroll account reconciliation with ADP/Gusto** → Requires payroll register data; use payroll-specific reconciliation
- **Investment/brokerage accounts** → Use crypto-tax-agent or a dedicated securities reconciliation tool
- **Intercompany eliminations** → This is GL-to-bank only; intercompany requires consolidation logic
- **Tax return preparation** → Reconciliation ≠ tax basis; use tax-specific workflows
- **Real-time dispute resolution with banks** → This is an analysis tool, not a bank portal interface
- **Accounts payable/receivable sub-ledger recon** → This skill handles bank-to-GL only; AP/AR aging has its own workflow

## Output Formats

**Text Report** (default): Formatted reconciliation worksheet + adjusting entry list
**CSV Export**: `date, description, amount, match_status, match_confidence, action_required`
**JSON**: Full structured result for pipeline consumption
**Excel Template**: Pre-formatted reconciliation workbook with formulas (describe desired layout)

## Example Prompts

```
"Here's March bank statement [CSV] and QBO export. Reconcile and list any adjusting entries needed."

"I have a $1,247 difference in my Chase checking for February. Here are both files — find it."

"Run bank rec for all three accounts. Files attached. Flag anything over $500 that's unmatched."

"Bank statement shows $89,340 ending balance. Our books show $87,100. Statement and GL export attached."

"Reconcile this and give me the adjusting JEs I need to post in QBO."
```

## Error Handling

- **Mismatched date formats** → Agent normalizes MM/DD/YYYY, YYYY-MM-DD, DD-Mon-YY automatically
- **Negative/positive sign conventions** → Detects and normalizes (debits as positive vs negative)
- **Missing beginning balance** → Warns; can still match transactions but reconciliation formula incomplete
- **Duplicate rows in input** → Flags and deduplicates before matching
- **Partial period data** → Warns if bank/GL date ranges don't align

## Audit Trail

Every reconciliation produces:
- Preparer: Sam Ledger / PrecisionLedger AI
- Timestamp: ISO 8601
- Input checksums (row counts, file names)
- Match statistics (% matched, # unmatched each side)
- Adjusting entries count
- Final difference (must be $0.00 for clean close)
