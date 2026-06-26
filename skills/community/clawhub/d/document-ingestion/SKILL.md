---
name: document-ingestion
description: "Process raw accounting source documents (PDFs, CSVs, bank statements, invoices, receipts) into standardized transaction records for QBO import. Use when batch-processing client documents for month-end close, categorizing transactions, or extracting data from 1099s and payroll reports. NOT for bank reconciliation, P&L variance analysis, or AR collections."
license: MIT
metadata:
  openclaw:
    emoji: "📄"
---

# Document Ingestion Engine — SKILL.md

## When to Use This Skill
Use when a user needs to process raw accounting source documents into standardized transaction records for QBO import. Triggers on:
- "Process these documents / invoices / receipts / bank statements"
- "Ingest docs for [client]"
- "I have PDFs/CSVs to categorize"
- "Batch import these transactions to QBO"
- "Extract data from 1099s / payroll reports"
- Document drop + categorization requests during month-end close

## When NOT to Use
- **Not** for running bank reconciliation (use `bank-reconciliation` skill)
- **Not** for P&L variance analysis (use `pl-quick-compare` skill)
- **Not** for single manual journal entries (just post directly in QBO)
- **Not** for AR collections or aging (use `ar-collections-agent` skill)

---

## What It Does

Processes 6 document types → standardized records → Excel workbook + QBO import CSV.

| Input Type | Formats | Extracts |
|---|---|---|
| Bank Statements | CSV, OFX/QFX, PDF | Date, vendor, amount |
| Credit Card Stmts | CSV, PDF | Date, merchant, amount, category |
| Invoices | PDF | Vendor, total, date, due date, invoice #, line items |
| Receipts | PDF, JPG/PNG* | Merchant, date, amount |
| 1099 / Tax Forms | PDF | Payer, TIN, form type, box amounts |
| Payroll Reports | CSV, PDF | Employee, gross, taxes, net per employee |

*Image OCR requires `tesseract` installed.

### Processing Steps
1. **File type detection** — magic bytes + extension fallback
2. **Document classification** — bank/CC/invoice/receipt/1099/payroll
3. **Content extraction** — CSV parsing, OFX parsing, PDF text extraction
4. **Format normalization** — dates (multi-format), amounts (Decimal), vendor names (strip noise)
5. **QBO COA pull** — fetches live Chart of Accounts from QBO for categorization
6. **Duplicate detection** — same amount + vendor within ±3 days → flagged
7. **Auto-categorization** — vendor map → COA keywords → doc-class default
8. **Confidence scoring** — HIGH (exact match) / MEDIUM (fuzzy) / LOW (needs review)
9. **Exception flagging** — missing dates, zero amounts, unknown vendors, LOW confidence
10. **QBO import CSV** — ready for batch import (excludes dups + failed extractions)
11. **Excel workbook** — 6 tabs (see below)
12. **CDC tracking** — delta since last run cached in `.cache/document-ingestion/{slug}.json`

### Excel Output Tabs
| Tab | Contents |
|---|---|
| Processed Transactions | All records with category, confidence, dup flag, exception |
| ⚠ Exceptions | Records needing manual review before import |
| Duplicates | Flagged potential duplicates with "Dup Of" reference |
| Category Mapping | Unique vendor → QBO account map with confidence |
| Import Ready | QBO-format rows (Date, Description, Amount, Account, Memo) |
| CDC Log | Delta metrics vs. prior run + this-run stats summary |

---

## Script Location
```
scripts/pipelines/document-ingestion.py
```

## Usage

```bash
# Process a directory of mixed documents
python3 scripts/pipelines/document-ingestion.py \
    --slug sb-paulson \
    --input-dir ~/Downloads/month-end-docs

# Single file
python3 scripts/pipelines/document-ingestion.py \
    --slug sb-paulson \
    --file ~/Downloads/invoice_march.pdf

# Multiple files + custom output dir
python3 scripts/pipelines/document-ingestion.py \
    --slug glowlabs \
    --file ~/Downloads/stmt.csv \
    --file ~/Downloads/payroll.csv \
    --out ~/Desktop/ingested

# Offline mode (no QBO auth needed)
python3 scripts/pipelines/document-ingestion.py \
    --slug sb-paulson \
    --input-dir ./docs \
    --no-qbo-coa

# QBO sandbox
python3 scripts/pipelines/document-ingestion.py \
    --slug sb-paulson \
    --input-dir ./docs \
    --sandbox
```

### All CLI Flags
| Flag | Default | Description |
|---|---|---|
| `--slug` | required | Company slug (QBO + client vendor map) |
| `--input-dir` | — | Directory of docs to process |
| `--file` | — | Single file (repeatable) |
| `--out` | `~/Desktop` | Output directory |
| `--no-qbo-coa` | false | Use built-in COA only (offline) |
| `--sandbox` | false | QBO sandbox mode |

---

## Dependencies

### Required (pip)
```bash
pip install openpyxl
```

### Optional (better extraction quality)
```bash
pip install pdfminer.six   # Better PDF text extraction
pip install ofxparse       # Better OFX/QFX parsing
brew install tesseract     # Image receipt OCR (JPG/PNG)
```

### Node.js QBO Client
```
Node.js QBO client   # Auth token must be configured
```

---

## Categorization Logic

### Priority Chain
1. **Vendor Map exact match** → `HIGH` confidence
2. **Vendor Map substring match** → `HIGH` confidence
3. **COA keyword index** (built from COA account names + keywords) → `MEDIUM` confidence
4. **Doc-class default** → `LOW` confidence

### Built-in Vendor Map
50+ known vendors pre-mapped:
- Stripe/Square/PayPal → Sales Revenue
- Gusto/ADP/Deel/Paychex → Payroll - Salaries & Wages
- Google/Microsoft/Slack/GitHub/Zoom → Software & Subscriptions
- Delta/United/Marriott/Uber → Travel
- FedEx/UPS/USPS → Postage & Delivery
- Chase/BofA service charges → Bank & Merchant Fees
- etc. (see `VENDOR_MAP` in script)

### Client-Specific Overrides
Auto-loaded by `--slug`:
- **glowlabs** → Loads GlowLabs vendor map (Deel, Toptal, Brex, Huellas Labs, etc.)
- **sb-paulson / willo** → Loads Willo Salons vendor map
- Other clients → Reads `clients/{slug}/categorization-map*.md` markdown tables

---

## Duplicate Detection Rules
- **Window:** ±3 days (configurable via `DUP_WINDOW_DAYS` constant)
- **Match criteria:** Same amount (exact Decimal) + same vendor key (first 3 meaningful words)
- **Action:** Flagged as `is_duplicate=True`, excluded from import file
- **Always confirm** before deleting — duplicates tab shows "Dup Of Row #" reference

---

## Exception Rules (auto-flagged)
| Condition | Flag |
|---|---|
| Missing transaction date | "Missing transaction date" |
| Zero amount (non-1099) | "Zero amount — verify or skip" |
| Empty/unknown vendor | "Vendor name missing or unknown" |
| LOW confidence category | "Low categorization confidence — manual review" |
| PDF extraction failed | "PDF text extraction failed — manual review required" |
| Image without tesseract | "Image OCR not available — manual entry required" |

---

## QBO Import CSV Format
Ready-to-import columns:
```
Date | Description | Amount | Vendor/Customer | Account | Class | Memo | Doc Number
```
- Amount sign: positive = expense (debit), negative = credit/income
- Memo includes source file + doc type for audit trail
- Excludes: duplicates, failed extractions

---

## CDC Cache
Location: `.cache/document-ingestion/{slug}.json`

Tracks between runs:
- `docs_processed`, `records_extracted`, `duplicates_caught`
- `exceptions_flagged`, `import_ready`
- `high_confidence`, `medium_confidence`, `low_confidence`

---

## Output File Naming
```
DocIngestion_{slug}_{YYYYMMDD}.xlsx
DocIngestion_{slug}_{YYYYMMDD}_QBO_Import.csv
```

---

## Agent Instructions

### Standard Run
1. Collect input files from user (directory path or individual files)
2. Get client slug (`sb-paulson`, `glowlabs`, etc.)
3. Run pipeline. If QBO auth not set, use `--no-qbo-coa`
4. Deliver summary:
   - Records extracted, dups caught, exceptions
   - HIGH/MED/LOW confidence split
   - Path to Excel + import CSV
5. Walk user through Exceptions tab — those need action before import

### Month-End Close Integration
- Run AFTER bank statement download, BEFORE bank reconciliation
- Use `--input-dir` pointing to client's document drop folder
- Import CSV goes into QBO → then run `bank-reconciliation.py`

### Exception Handling
- PDFs with no extractable text → LOW confidence + exception flag → send to client for re-scan
- Image receipts with no tesseract → exception flag → use `nano-pdf` skill or manual entry
- Unknown vendors → update `VENDOR_MAP` in script or add to `clients/{slug}/categorization-map.md`

### Adding New Client Vendor Maps
Edit `load_client_vendor_map()` in the script:
```python
if slug_lower in ("new-client", "nc"):
    client_map.update({
        "vendor name": "QBO Account Name",
    })
```
Or create `clients/{slug}/categorization-map.md` with markdown table:
```markdown
| Vendor / Memo Keyword | Primary Account | Notes |
|---|---|---|
| Amazon | Office Supplies | |
| Comcast | Utilities | |
```

---

## Financial Math
All amounts use Python `Decimal` with `ROUND_HALF_UP` to 2 decimal places. No float arithmetic.
