---
name: deepread-invoice
title: DeepRead Invoice Processing
description: Extract structured data from invoices, receipts, and bills using DeepRead. Pre-built schemas for vendor, line items, totals, tax, due dates. 97%+ accuracy with human-in-the-loop flags. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Invoice Processing

Extract structured data from invoices, receipts, purchase orders, and bills. Submit a PDF or image, get back typed JSON with vendor, line items, totals, tax, and due dates — with confidence flags telling you exactly which fields need human review.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back

Submit an invoice PDF and get structured JSON like this:

```json
{
  "vendor": {"value": "Acme Corp", "hil_flag": false, "found_on_page": 1},
  "invoice_number": {"value": "INV-2026-0042", "hil_flag": false, "found_on_page": 1},
  "invoice_date": {"value": "2026-03-15", "hil_flag": false, "found_on_page": 1},
  "due_date": {"value": "2026-04-15", "hil_flag": false, "found_on_page": 1},
  "subtotal": {"value": 1150.00, "hil_flag": false, "found_on_page": 1},
  "tax": {"value": 100.00, "hil_flag": false, "found_on_page": 1},
  "total": {"value": 1250.00, "hil_flag": false, "found_on_page": 1},
  "currency": {"value": "USD", "hil_flag": false, "found_on_page": 1},
  "payment_terms": {"value": "Net 30", "hil_flag": true, "reason": "Inferred from dates"},
  "line_items": {"value": [
    {"description": "Consulting services - March", "quantity": 40, "unit_price": 25.00, "amount": 1000.00},
    {"description": "Software license", "quantity": 1, "unit_price": 150.00, "amount": 150.00}
  ], "hil_flag": false, "found_on_page": 1}
}
```

Fields with `hil_flag: true` need human review. Everything else is high-confidence and can be auto-processed.

## Setup

### Get Your API Key

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
```

Save it:
```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## Invoice Schema

Use this pre-built schema for invoices. It covers the most common fields across invoice formats:

```json
{
  "type": "object",
  "properties": {
    "vendor": {"type": "string", "description": "Company or vendor name on the invoice"},
    "vendor_address": {"type": "string", "description": "Vendor's full mailing address"},
    "invoice_number": {"type": "string", "description": "Invoice number or reference ID"},
    "invoice_date": {"type": "string", "description": "Date the invoice was issued (YYYY-MM-DD)"},
    "due_date": {"type": "string", "description": "Payment due date (YYYY-MM-DD)"},
    "po_number": {"type": "string", "description": "Purchase order number if referenced"},
    "bill_to": {"type": "string", "description": "Name and address of the entity being billed"},
    "subtotal": {"type": "number", "description": "Subtotal before tax and discounts"},
    "tax": {"type": "number", "description": "Total tax amount"},
    "discount": {"type": "number", "description": "Total discount applied"},
    "total": {"type": "number", "description": "Total amount due including tax"},
    "currency": {"type": "string", "description": "Currency code (USD, EUR, GBP, etc.)"},
    "payment_terms": {"type": "string", "description": "Payment terms (Net 30, Due on receipt, etc.)"},
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": {"type": "string", "description": "Item or service description"},
          "quantity": {"type": "number", "description": "Quantity"},
          "unit_price": {"type": "number", "description": "Price per unit"},
          "amount": {"type": "number", "description": "Line total"}
        }
      },
      "description": "List of line items on the invoice"
    }
  }
}
```

## Extract Data From an Invoice

### Python

```python
import requests
import json
import time

API_KEY = "sk_live_YOUR_KEY"
BASE = "https://api.deepread.tech"
headers = {"X-API-Key": API_KEY}

# Invoice schema
schema = json.dumps({
    "type": "object",
    "properties": {
        "vendor": {"type": "string", "description": "Company or vendor name"},
        "invoice_number": {"type": "string", "description": "Invoice number"},
        "invoice_date": {"type": "string", "description": "Date issued (YYYY-MM-DD)"},
        "due_date": {"type": "string", "description": "Payment due date (YYYY-MM-DD)"},
        "subtotal": {"type": "number", "description": "Subtotal before tax"},
        "tax": {"type": "number", "description": "Total tax amount"},
        "total": {"type": "number", "description": "Total amount due"},
        "currency": {"type": "string", "description": "Currency code (USD, EUR, etc.)"},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "amount": {"type": "number"}
                }
            },
            "description": "Line items"
        }
    }
})

# Submit invoice
with open("invoice.pdf", "rb") as f:
    job = requests.post(
        f"{BASE}/v1/process",
        headers=headers,
        files={"file": f},
        data={"schema": schema},
    ).json()

job_id = job["id"]
print(f"Processing invoice: {job_id}")

# Poll for results
delay = 5
while True:
    time.sleep(delay)
    result = requests.get(f"{BASE}/v1/jobs/{job_id}", headers=headers).json()

    if result["status"] == "completed":
        data = result["result"]["data"]

        # Auto-process high-confidence fields
        for field, value in data.items():
            if isinstance(value, dict):
                if value.get("hil_flag"):
                    print(f"  REVIEW: {field} = {value['value']} ({value.get('reason')})")
                else:
                    print(f"  OK: {field} = {value['value']}")
        break
    elif result["status"] == "failed":
        print(f"Failed: {result.get('error')}")
        break

    delay = min(delay * 1.5, 15)
```

### cURL

```bash
# Submit invoice with schema
JOB_ID=$(curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F 'schema={"type":"object","properties":{"vendor":{"type":"string","description":"Company name"},"invoice_number":{"type":"string","description":"Invoice number"},"total":{"type":"number","description":"Total due"},"due_date":{"type":"string","description":"Due date"},"line_items":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"amount":{"type":"number"}}},"description":"Line items"}}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

echo "Processing: $JOB_ID"

# Poll
while true; do
  sleep 5
  RESULT=$(curl -s "https://api.deepread.tech/v1/jobs/$JOB_ID" -H "X-API-Key: $DEEPREAD_API_KEY")
  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "  Status: $STATUS"
  [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ] && break
done

echo "$RESULT" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['result']['data'], indent=2))"
```

## Use Cases

- **Accounts Payable** — Auto-extract vendor, amount, due date from incoming invoices and route to approval
- **Receipt Processing** — Pull totals, dates, and vendor from expense receipts for reimbursement
- **Purchase Orders** — Match PO numbers and line items against invoices
- **Bookkeeping** — Bulk-process monthly invoices into structured data for your accounting system
- **Audit** — Extract and verify invoice data at scale with confidence scoring

## Tips for Best Accuracy

- **Be specific in descriptions** — "Invoice number or reference ID" works better than just "number"
- **Use YYYY-MM-DD for dates** — Reduces ambiguity between US and international date formats
- **Use blueprints for recurring vendors** — If you process the same vendor's invoices repeatedly, create a blueprint at deepread.tech/dashboard/optimizer for 20-30% accuracy improvement
- **Check hil_flag fields** — These are the only fields that need human review. Everything else is high-confidence.

## Batch Processing

For processing multiple invoices, submit them in parallel and collect results:

```python
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

API_KEY = "sk_live_YOUR_KEY"
BASE = "https://api.deepread.tech"
headers = {"X-API-Key": API_KEY}

schema = json.dumps({...})  # Use the invoice schema above

def process_invoice(file_path):
    with open(file_path, "rb") as f:
        job = requests.post(
            f"{BASE}/v1/process",
            headers=headers,
            files={"file": f},
            data={"schema": schema},
        ).json()

    job_id = job["id"]
    delay = 5
    while True:
        time.sleep(delay)
        result = requests.get(f"{BASE}/v1/jobs/{job_id}", headers=headers).json()
        if result["status"] in ("completed", "failed"):
            return result
        delay = min(delay * 1.5, 15)

# Process 10 invoices in parallel
invoice_files = ["invoice_01.pdf", "invoice_02.pdf", "invoice_03.pdf"]
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(process_invoice, invoice_files))

for r in results:
    if r["status"] == "completed":
        data = r["result"]["data"]
        vendor = data.get("vendor", {}).get("value", "Unknown")
        total = data.get("total", {}).get("value", 0)
        print(f"  {vendor}: ${total}")
```

## BYOK — Zero Processing Costs

Connect your own OpenAI, Google, or OpenRouter key via the dashboard. All invoice processing routes through your provider — zero DeepRead LLM costs, page quota skipped.

Set it up: https://www.deepread.tech/dashboard/byok

## Related DeepRead Skills

- **deepread-ocr** — General OCR and structured extraction — `clawhub install uday390/deepread-ocr`
- **deepread-form-fill** — Fill PDF forms with AI vision — `clawhub install uday390/deepread-form-fill`
- **deepread-pii** — Redact PII from documents — `clawhub install uday390/deepread-pii`
- **deepread-agent-setup** — OAuth device flow authentication — `clawhub install uday390/deepread-agent-setup`
- **deepread-byok** — Bring Your Own Key setup — `clawhub install uday390/deepread-byok`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Demo Repo**: https://github.com/deepread-tech/deepread-demo
- **Issues**: https://github.com/deepread-tech/deep-read-service/issues
- **Email**: hello@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
