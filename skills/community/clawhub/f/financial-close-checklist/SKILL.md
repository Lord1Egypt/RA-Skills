---
name: financial-close-checklist
description: >
  Automate and track month-end and quarter-end financial close processes for accounting firms and
  finance teams. Generates customizable close checklists, assigns task owners, tracks completion status,
  flags exceptions and reconciling items, and produces a close summary report. Covers GL reconciliation,
  AR/AP sub-ledger tie-outs, accruals, prepaid amortization, fixed asset depreciation, bank reconciliation,
  and financial statement review steps. Use when a controller, CFO, or accountant needs to run a structured
  close, document completion evidence, or accelerate a multi-day close down to same-day.
  NOT for: real-time bookkeeping entry (use qbo-automation), tax filing preparation (use tax-deadline-calendar),
  payroll processing, or audit fieldwork (different scope than close procedures).
version: 1.0.0
author: PrecisionLedger
tags:
  - accounting
  - month-end
  - close
  - reconciliation
  - finance-ops
  - controller
  - audit-ready
---

# Financial Close Checklist Skill

Structured, repeatable month-end and quarter-end close for accounting teams. This skill guides Sam Ledger through generating close checklists, tracking task status, flagging exceptions, and producing close summary reports for controllers, CFOs, and auditors.

---

## When to Use This Skill

**Trigger phrases:**
- "Run month-end close"
- "Generate the close checklist for [month]"
- "What's left in the close?"
- "We need to close the books by Friday"
- "Tie out our AR sub-ledger"
- "Quarter-end close procedures"
- "Accelerate our close process"
- "How do I run a fast close?"
- "Close summary for the board"

**NOT for:**
- Entering journal entries or transactions — use `qbo-automation` for live QBO writes
- Tax return preparation — use `tax-deadline-calendar` and engage CPA
- Payroll runs — separate payroll workflow, not a close step
- External audit fieldwork — close procedures feed audit prep, not replace it
- Real-time dashboards — use `kpi-alert-system` for live monitoring

---

## The Standard Close Checklist

### PHASE 1: Transaction Cutoff (Days 1–2)

These steps ensure all activity belongs in the correct period.

```
□ 1.1  Post all cash receipts through last day of month
□ 1.2  Record all vendor bills/invoices received through month-end
□ 1.3  Confirm credit card transactions downloaded and coded
□ 1.4  Post payroll through final pay date in period
□ 1.5  Record any wire transfers or ACH payments initiated in period
□ 1.6  Confirm sales/revenue recognition cutoff (invoiced vs. shipped)
□ 1.7  Identify any transactions in wrong period → post correcting entries
```

### PHASE 2: Sub-Ledger Reconciliations (Days 2–3)

Each sub-ledger must tie to the GL before proceeding.

#### 2a. Accounts Receivable
```
□ 2.1  Run AR aging report
□ 2.2  Confirm AR sub-ledger total = GL AR balance
□ 2.3  Identify invoices > 90 days → flag for collections or bad debt reserve
□ 2.4  Post bad debt expense if reserve adjustment needed
□ 2.5  Clear any unapplied customer payments
□ 2.6  Confirm deferred revenue balance for advance payments
```

**AR Tie-Out Formula:**
```
GL AR Balance = Sub-Ledger Total
If difference > $0: investigate open credits, unapplied payments, timing entries
```

#### 2b. Accounts Payable
```
□ 2.7  Run AP aging report
□ 2.8  Confirm AP sub-ledger total = GL AP balance
□ 2.9  Review bills due within 10 days → schedule payments
□ 2.10 Identify duplicate bills or credits not applied
□ 2.11 Accrue for invoices received but not yet entered (goods/services received)
```

#### 2c. Bank Reconciliation
```
□ 2.12 Download bank statement through month-end
□ 2.13 Reconcile book balance to bank statement balance
□ 2.14 List outstanding checks (issued, not cleared)
□ 2.15 List deposits in transit (posted in books, not cleared bank)
□ 2.16 Identify bank fees and post to GL
□ 2.17 Confirm reconciled balance = GL Cash balance
```

**Bank Rec Formula:**
```
Bank Statement Balance
+ Deposits in Transit
- Outstanding Checks
= Adjusted Bank Balance

Must equal:

GL Cash Balance
+ Any timing JEs
= Adjusted Book Balance
```

### PHASE 3: Accruals & Adjusting Entries (Day 3–4)

These are estimates for expenses incurred but not yet billed.

```
□ 3.1  Accrue payroll for days worked but not yet paid
□ 3.2  Accrue employer payroll taxes on accrued payroll
□ 3.3  Accrue any known vendor invoices not yet received
□ 3.4  Accrue interest expense on outstanding debt
□ 3.5  Record prepaid expense amortization (insurance, rent, subscriptions)
□ 3.6  Record deferred revenue recognition (earned portion of advance payments)
□ 3.7  Post depreciation/amortization for fixed assets and intangibles
□ 3.8  Record any inventory adjustments (if applicable)
□ 3.9  Post reclassifying entries for misposted transactions
```

#### Prepaid Amortization Tracker
```
Asset           | Total Cost | Start Date  | Months | Monthly Amort | Remaining
----------------|------------|-------------|--------|---------------|----------
D&O Insurance   | $24,000    | Jan 1, 2026 | 12     | $2,000        | $18,000
AWS Annual Plan | $6,000     | Mar 1, 2026 | 12     | $500          | $5,500
Office Lease    | $3,600     | Jan 1, 2026 | 12     | $300          | $2,700
```

#### Depreciation Schedule
```
Asset           | Cost    | Useful Life | Method    | Monthly Depr | Accum Depr
----------------|---------|-------------|-----------|--------------|------------
MacBook Pro x3  | $9,000  | 3 years     | Straight  | $250         | $1,500
Server Rack     | $15,000 | 5 years     | Straight  | $250         | $750
```

### PHASE 4: Financial Statement Review (Day 4–5)

```
□ 4.1  Generate Trial Balance — review for unusual balances
□ 4.2  Compare P&L to prior month (flag >15% variance in any line item)
□ 4.3  Compare P&L to budget/forecast — document significant variances
□ 4.4  Verify Balance Sheet balances (Assets = Liabilities + Equity)
□ 4.5  Review Cash Flow Statement — confirm net change ties to cash account movement
□ 4.6  Confirm all intercompany eliminations (if multi-entity)
□ 4.7  Review equity rollforward (beginning + net income - distributions = ending)
□ 4.8  Confirm no accounts with unexpected zero or negative balances
```

#### Variance Analysis Template
```
Account          | Prior Month | Current Month | $ Change | % Change | Explanation
-----------------|-------------|---------------|----------|----------|-------------
Revenue          | $85,000     | $92,000       | +$7,000  | +8.2%    | New client X
Payroll          | $42,000     | $48,000       | +$6,000  | +14.3%   | New hire Mar 1
Software Subs    | $3,200      | $5,100        | +$1,900  | +59.4%   | ← INVESTIGATE
```

### PHASE 5: Close Lock & Sign-Off (Day 5)

```
□ 5.1  Lock period in accounting system (prevent backdating)
□ 5.2  Export final Trial Balance, P&L, Balance Sheet, Cash Flow
□ 5.3  Save to close folder: /close/YYYY-MM/
□ 5.4  Obtain controller/CFO sign-off
□ 5.5  Distribute financial package to stakeholders
□ 5.6  Log close completion date and duration for process improvement tracking
□ 5.7  Note any open items / carryforward items for next month
```

---

## Close Templates by Entity Type

### Small Business / SMB (5-day close target)
```
Day 1: Transaction cutoff, download bank statements
Day 2: Bank rec, AR/AP sub-ledger tie-out
Day 3: Accruals, prepaid amortization, depreciation
Day 4: Trial balance review, variance analysis
Day 5: FS review, lock period, distribute package
```

### Startup / SaaS Company (3-day fast close)
```
Day 1 AM: Transaction cutoff + bank rec
Day 1 PM: AR/AP tie-out + deferred revenue schedule
Day 2 AM: Accruals + stock comp expense entry
Day 2 PM: Trial balance + P&L vs. budget variance
Day 3:    FS review + board package prep + lock
```

### Accounting Firm / Client Close (day-of close)
```
Hour 1: Pull all source data (bank, payroll, CC)
Hour 2: Post entries, run bank rec
Hour 3: Accrue + amortize + depreciate
Hour 4: Review FS, document exceptions
Hour 5: Deliver client package, lock period
```

---

## Quarter-End Additional Steps

In addition to all monthly steps:

```
□ Q1  Reconcile all balance sheet accounts (not just AR/AP/Cash)
□ Q2  Review equity accounts — capital contributions, distributions, retained earnings
□ Q3  Compute estimated income tax provision (if C-Corp or S-Corp with tax)
□ Q4  Review fixed asset register — any disposals, fully depreciated assets?
□ Q5  Confirm loan balances match amortization schedules
□ Q6  Review contingent liabilities (pending lawsuits, commitments)
□ Q7  Prepare quarter-end management report (P&L + BS + Cash Flow + KPIs)
□ Q8  Deliver to board/investors within 15 days of quarter-end
```

### Year-End Additional Steps

```
□ Y1  All quarterly steps above
□ Y2  Issue 1099-NECs by January 31 (contractors paid ≥ $600)
□ Y3  Reconcile payroll W-2s to payroll tax returns (940, 941)
□ Y4  Inventory count and valuation (if applicable)
□ Y5  Goodwill and intangible asset impairment review
□ Y6  Related-party transaction disclosure documentation
□ Y7  Engage CPA for tax return preparation
□ Y8  Prepare audit support package (if audited)
```

---

## Exception Handling Protocols

### When AR Sub-Ledger Doesn't Tie to GL
```
Step 1: Run AR aging with open invoice detail
Step 2: Compare sub-ledger total to GL AR account balance
Step 3: If difference found:
  a. Check for unposted transactions in AR module
  b. Look for manual JEs directly to AR GL account (bypassing sub-ledger)
  c. Check for duplicate customer payments not applied
  d. Review void/deleted transactions in prior periods
Step 4: Post reconciling JE with clear memo explaining difference
Step 5: Document root cause to prevent recurrence
```

### When Bank Rec Won't Balance
```
Step 1: Confirm bank statement ending date matches close date
Step 2: List ALL outstanding checks — verify against prior month's list
Step 3: List ALL deposits in transit — confirm cleared in subsequent statement
Step 4: Look for duplicate transactions in GL
Step 5: Check for NSF checks posted by bank but not recorded in books
Step 6: Verify no automatic bank charges missed (wire fees, service charges)
```

### Large Unexplained Variance (>15% MoM)
```
Trigger: Any P&L line item with >15% month-over-month change without explanation
Action:
  1. Pull transaction detail for that GL account
  2. Identify the specific transaction(s) driving the variance
  3. Confirm correct coding (not misposted from another account)
  4. If legitimate: document business reason in variance memo
  5. If error: post correcting JE before close
```

---

## Close Summary Report Format

Produce this report after each close:

```
MONTH-END CLOSE SUMMARY
Period: [Month YYYY]
Close Completed: [Date]
Prepared By: [Name]
Reviewed By: [Name]

FINANCIALS AT A GLANCE
  Revenue:         $XX,XXX   (vs. prior month: +/-X%)
  Gross Profit:    $XX,XXX   (Gross Margin: XX%)
  Net Income:      $XX,XXX
  Cash Balance:    $XX,XXX
  AR Balance:      $XX,XXX   (Avg DSO: XX days)
  AP Balance:      $XX,XXX

CLOSE STATUS
  ✅ Bank reconciliation — completed [date]
  ✅ AR sub-ledger tie-out — completed [date]
  ✅ AP sub-ledger tie-out — completed [date]
  ✅ Accruals posted — [# of entries]
  ✅ Depreciation/amortization posted
  ✅ Period locked in [system]
  ⚠️  OPEN ITEMS (carry forward):
      - [Item 1]: awaiting [input/resolution]
      - [Item 2]: to be resolved by [date]

KEY VARIANCES EXPLAINED
  [Account]: [$ change] [% change] — [brief explanation]
  
ATTACHMENTS
  □ Trial Balance
  □ P&L Statement
  □ Balance Sheet
  □ Cash Flow Statement
  □ Bank Reconciliation
  □ AR Aging
  □ AP Aging
```

---

## Close Duration Benchmarks

| Company Stage | Target Close Duration | Best Practice |
|---|---|---|
| Startup (< $1M ARR) | Same day | Automated bank feeds, cloud accounting |
| SMB ($1M–$10M) | 3–5 business days | Dedicated bookkeeper, clear cutoffs |
| Mid-market ($10M–$100M) | 5–7 business days | ERP system, close calendar |
| Enterprise ($100M+) | 10–15 business days | Dedicated close team, automated consolidation |
| **Target (any)** | **Reduce by 30% YoY** | **Process automation + checklist discipline** |

---

## Accelerating the Close: Quick Wins

```
1. Automate bank feeds — eliminate manual download/import
2. Set transaction cutoff rules — no backdating without approval
3. Standardize chart of accounts — fewer coding questions = faster entry
4. Create recurring JE templates — one-click accruals, depreciation, amortization
5. Use close management software — FloQast, Blackline, or a simple Google Sheet tracker
6. Pre-schedule close calls — 15-min daily standup during close week
7. Designate a close owner — one person accountable for the checklist
8. Post-close retrospective — 15 min after each close to capture what slowed you down
```

---

## Integration Points

- **`qbo-automation`** — pull actuals from QuickBooks; post accruals and JEs programmatically
- **`budget-vs-actual`** — compare close results against plan; generate variance commentary
- **`ar-collections-agent`** — escalate high-risk AR items identified in close aging review
- **`kpi-alert-system`** — set alerts on close metrics (DSO, DPO, cash balance thresholds)
- **`report-generator`** — format close summary into client-ready PDF or board deck
- **`thirteen-week-cash-flow`** — feed actual month-end cash balance as input to 13-week forecast
- **`tax-deadline-calendar`** — trigger quarterly estimated tax tasks from close data

---

## Example Usage

**User:** "It's March 31st — help me close February's books for a client. They're on QBO, about $180k/month revenue, 8 employees."

**Sam's response:**
```
Close Checklist — February 2026
Client: [Name] | System: QuickBooks Online | Revenue: ~$180k/mo

PHASE 1 — Transaction Cutoff (Today)
□ Confirm all customer payments through Feb 28 posted
□ Enter any bills received in February not yet in QBO
□ Download and match credit card transactions through Feb 28
□ Confirm payroll for Feb 1–28 pay dates is posted

PHASE 2 — Sub-Ledger Reconciliations (Today)
□ Run AR aging in QBO → does it match GL 1200 balance?
□ Run AP aging → does it match GL 2000 balance?
□ Download bank statement → run bank reconciliation

PHASE 3 — Accruals (Today/Tomorrow)
□ Accrue Feb 27-28 payroll (2 days unpaid)
□ Amortize prepaid expenses (pull your prepaid schedule)
□ Post February depreciation

PHASE 4 — Review (Tomorrow)
□ Compare Feb P&L to January — flag any line >15% change
□ Confirm Balance Sheet balances
□ Review cash balance vs. bank rec

PHASE 5 — Lock & Deliver
□ Lock February period in QBO
□ Export TB, P&L, BS, Cash Flow
□ Prepare close summary → send to client

Estimated time: 4-6 hours for clean books.
Want me to start with the bank rec or the AR aging tie-out?
```

---

## Reference: Close Calendar Template

```
MONTH-END CLOSE CALENDAR

Day 1 (Month + 1):   Bank statement available → begin bank rec
Day 2:               AR/AP tie-out, post accruals
Day 3:               Depreciation, prepaid amortization
Day 4:               TB review, variance analysis, adjusting entries
Day 5:               FS review, controller sign-off, lock period
Day 6:               Distribute financial package
Day 7–10:            Client meeting / board presentation (if applicable)

QUARTERLY EXTRAS (end of Q1/Q2/Q3/Q4):
+Day 5–6:  Full BS reconciliation, tax provision
+Day 7:    Board/investor package
+Day 10:   Quarterly filings (941, sales tax, etc.)
```
