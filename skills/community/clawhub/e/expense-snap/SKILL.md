---
name: expense-snap
description: Capture receipt details, categorize spending, and generate monthly reports from a local SQLite ledger.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/expense-snap
    requires:
      bins:
        - python
---

# Expense Snap

Use this skill when the user wants to turn a receipt or spending note into
structured expense data, review spending by month, or export records to CSV.

## When to Use

- Logging a new receipt from text or an image transcription.
- Categorizing spending into consistent buckets.
- Producing monthly summaries with budget comparisons.
- Exporting receipts for spreadsheets or reimbursement.

## Commands

The helper script stores state in `{baseDir}/.runtime/expense-snap.db`.

### Record a receipt

```bash
python {baseDir}/scripts/expense_snap.py record --merchant "Cafe Luna" --date 2026-03-22 --total 18.40 --currency EUR --category meals --line-item "Latte|4.50|1|beverages" --line-item "Sandwich|13.90|1|meals"
```

### List receipts

```bash
python {baseDir}/scripts/expense_snap.py list --month 2026-03 --category meals
```

### Monthly report

```bash
python {baseDir}/scripts/expense_snap.py monthly-report --month 2026-03
```

### Export to CSV

```bash
python {baseDir}/scripts/expense_snap.py export-csv --month 2026-03 --output {baseDir}/.runtime/march-expenses.csv
```

## Safety Boundaries

- Never claim receipt OCR is perfect. Mark ambiguous fields as inferred.
- Do not fabricate line items that are not visible or provided.
- Keep currency and totals consistent with the source receipt.
- If an image is unreadable, explain the uncertainty instead of inventing data.
