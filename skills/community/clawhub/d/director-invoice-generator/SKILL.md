---
name: invoice-generator
description: Create professional invoices, quotes, and billing documents. Use when user wants to (1) generate an invoice, (2) create a quote, (3) make a receipt, (4) track payments, or (5) customize billing documents. Supports PDF, DOCX, and plain text output.
---

# Invoice Generator

Create professional billing documents quickly.

## Quick Start

1. **Gather details** - Client info, items, amounts, dates
2. **Select template** - Invoice, quote, or receipt
3. **Generate** - Output to PDF, DOCX, or text
4. **Deliver** - Send to client or download

## Input Data Structure

```python
invoice = {
    "type": "invoice",  # invoice, quote, receipt
    "number": "INV-2026-001",
    "date": "2026-04-07",
    "due_date": "2026-04-21",
    "from": {
        "name": "Your Company",
        "address": "123 Main St",
        "email": "billing@company.com"
    },
    "to": {
        "name": "Client Name",
        "company": "Client Company",
        "address": "456 Business Ave",
        "email": "ap@client.com"
    },
    "items": [
        {"description": "Service Name", "qty": 10, "rate": 150},
        {"description": "Materials", "qty": 1, "rate": 500}
    ],
    "tax_rate": 0.08,  # 8%
    "notes": "Payment due within 14 days"
}
```

## Calculations

Auto-calculate:
- **Subtotal**: sum(qty × rate) for each item
- **Tax**: subtotal × tax_rate
- **Total**: subtotal + tax

## Output Templates

### Invoice
```
INVOICE #INV-2026-001
Date: April 7, 2026 | Due: April 21, 2026

From: Your Company
To: Client Company

Item                    Qty     Rate      Amount
-------------------------------------------
Consulting              10      $150      $1,500
Materials               1       $500      $500
-------------------------------------------
                        Subtotal:         $2,000
                        Tax (8%):         $160
                        TOTAL:            $2,160

Notes: Payment due within 14 days
```

### Quote
Same format, but header: "QUOTE #QT-2026-001" + "Valid for 30 days"

### Receipt
Header: "RECEIPT #RCP-2026-001" + "Paid: [date]"

## Best Practices

- Use sequential invoice numbers (INV-2026-001, INV-2026-002...)
- Include payment terms in notes
- Set due dates 14-30 days out for invoices
- Track outstanding amounts
