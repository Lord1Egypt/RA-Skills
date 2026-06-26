---
name: expense-categorization
description: Receipt OCR, GL code mapping, policy compliance checking, and anomaly detection for business expenses. Use when you need to: (1) extract data from receipt images or PDFs via OCR, (2) map expenses to chart of accounts or GL codes, (3) check receipts against expense policies (per diem limits, category restrictions, required fields), (4) detect anomalies like duplicates, out-of-policy amounts, missing receipts, or unusual vendors, (5) batch-process expense reports for approval routing, (6) categorize credit card transactions into accounting categories. Works with QBO chart of accounts, generic GL structures, or custom category lists. NOT for: tax filing or PTIN-backed services, payroll processing, or real-time bank feed categorization without human review.
---

# Expense Categorization

Receipt OCR, GL mapping, policy compliance, and anomaly detection for business expenses.

## Workflow

### 1. Receipt Extraction (OCR)

Use `tesseract` (local) or Vision API for image receipts; `pdfplumber` for PDF receipts.

Key fields to extract:
- Vendor name, date, total amount, line items
- Payment method (last 4 digits if visible)
- Tax amount (HST/GST/sales tax)
- Tips/gratuity (separate from subtotal)

```bash
# Tesseract OCR on receipt image
tesseract receipt.jpg stdout --psm 4 | python3 scripts/parse_receipt.py

# Or use Claude vision directly for complex layouts
```

For complex or handwritten receipts → use vision model with prompt in `references/ocr-prompt.md`.

### 2. GL Code Mapping

Map extracted expense category to chart of accounts. See `references/gl-mapping.md` for:
- Standard QBO GL codes for common expense types
- IRS-aligned categories (meals 50%, travel, home office, etc.)
- Crypto/DeFi expense categories

**Matching logic:**
1. Exact vendor name match (known vendor list)
2. MCC code match (credit card transactions)
3. Keyword match on description/line items
4. Fallback: prompt user to select category

### 3. Policy Compliance Check

Apply policy rules before approval routing. See `references/policy-rules.md` for standard rules.

Core checks:
- **Per diem limits**: Meals >$75 require itemized receipt; travel per diem by city
- **Receipt threshold**: Receipt required for any expense ≥$25 (IRS standard)
- **Time limit**: Receipts must be submitted within 30/60/90 days (configurable)
- **Duplicate detection**: Same vendor + amount ± $1 within 7 days = flag
- **Split transactions**: Same vendor, sequential dates, amounts just below approval threshold = flag

### 4. Anomaly Detection

Flag for human review:
- Amount > 2× historical average for that vendor/category
- Weekend or holiday transactions (especially travel/entertainment)
- Round-number amounts (potential personal purchase)
- Vendor in restricted list (casinos, adult entertainment, competitors)
- Missing required fields (date, vendor, business purpose)
- Out-of-state purchases for office supply categories

### 5. Output Format

```json
{
  "receipt_id": "REC-20260315-001",
  "vendor": "Delta Air Lines",
  "date": "2026-03-15",
  "amount": 487.50,
  "currency": "USD",
  "gl_code": "6200",
  "category": "Travel - Air",
  "policy_status": "approved",
  "flags": [],
  "confidence": 0.94,
  "requires_review": false,
  "notes": "Business purpose required for reimbursement"
}
```

## Batch Processing

For expense report batches:

```python
# Process folder of receipts
import glob
receipts = glob.glob("receipts/*.{jpg,png,pdf}")
results = [categorize(r) for r in receipts]

# Summary stats
flagged = [r for r in results if r["requires_review"]]
total = sum(r["amount"] for r in results)
by_category = group_by(results, "category")
```

Output batch summary as CSV or feed directly to QBO via qbo-automation skill.

## Common Patterns

**Credit card statement import:**
1. Parse CSV/OFX from bank
2. Match known vendors → auto-categorize
3. Unknown vendors → ML classification or prompt
4. Export mapped transactions to QBO

**Expense report approval routing:**
- Auto-approve: policy-compliant, under $250, no flags
- Manager approval: $250–$2,500 or single flag
- Finance review: >$2,500, multiple flags, or restricted category

**Mileage reimbursement:**
- Extract start/end locations + business purpose
- Calculate at current IRS rate (check `references/irs-rates.md`)
- Map to GL 6210 (Auto/Mileage)

## Integration Points

- **qbo-automation**: Push categorized transactions directly to QBO
- **crypto-tax-agent**: Route DeFi/crypto expenses for cost basis tracking
- **kpi-alert-system**: Trigger alerts when department spend exceeds budget
- **invoice-automation**: Cross-reference receipts with vendor invoices

## Negative Boundaries

- **Not for PTIN-backed tax work** — categorization ≠ tax advice; defer to licensed preparer
- **Not for payroll** — employee expense reimbursement != payroll processing
- **Not a real-time feed** — batch review with human sign-off before posting to GL
- **Not for legal contracts** — use contract-review-agent for vendor agreements
- **Confidence <0.7** → always route to human review, never auto-post
