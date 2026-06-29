---
name: deepread-purchase-orders
title: DeepRead Purchase Orders
description: Extract structured data from purchase orders — PO number, buyer/supplier, line items, quantities, prices, delivery dates, totals — as typed JSON. 2-way/3-way match against invoices. Per-field confidence flags. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Purchase Orders

Turn purchase orders — PDF or scanned — into clean, typed JSON: PO number, buyer and supplier, every line item with quantity and price, delivery dates, and totals. Pair it with extracted invoices for automated 2-way / 3-way matching.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "po_number", "value": "PO-2026-5512", "needs_review": false, "location": {"page": 1}},
      {"key": "order_date", "value": "2026-04-02", "needs_review": false, "location": {"page": 1}},
      {"key": "supplier_name", "value": "Globex Supplies", "needs_review": false, "location": {"page": 1}},
      {"key": "buyer_name", "value": "Initech Inc", "needs_review": false, "location": {"page": 1}},
      {"key": "delivery_date", "value": "2026-04-20", "needs_review": false, "location": {"page": 1}},
      {"key": "total", "value": 4860.00, "needs_review": false, "location": {"page": 1}},
      {"key": "line_items", "value": [
        {"sku": "WDG-100", "description": "Widget A", "quantity": 200, "unit_price": 18.00, "amount": 3600.00},
        {"sku": "WDG-200", "description": "Widget B", "quantity": 60, "unit_price": 21.00, "amount": 1260.00}
      ], "needs_review": false, "location": {"page": 1}}
    ]
  }
}
```

## Setup

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## Schema

```json
{
  "type": "object",
  "properties": {
    "po_number":     {"type": "string", "description": "Purchase order number"},
    "order_date":    {"type": "string", "description": "PO date (YYYY-MM-DD)"},
    "supplier_name": {"type": "string", "description": "Supplier / vendor name"},
    "buyer_name":    {"type": "string", "description": "Buyer / ordering company"},
    "delivery_date": {"type": ["string","null"], "description": "Requested delivery date (YYYY-MM-DD)"},
    "ship_to":       {"type": ["string","null"], "description": "Ship-to address"},
    "currency":      {"type": "string", "description": "Currency code"},
    "subtotal":      {"type": ["number","null"], "description": "Subtotal before tax"},
    "tax":           {"type": ["number","null"], "description": "Tax amount"},
    "total":         {"type": "number", "description": "Total order amount"},
    "line_items": {
      "type": "array",
      "description": "Ordered line items",
      "items": {"type": "object", "properties": {
        "sku":         {"type": ["string","null"], "description": "SKU / item code"},
        "description": {"type": "string", "description": "Item description"},
        "quantity":    {"type": "number", "description": "Quantity ordered"},
        "unit_price":  {"type": "number", "description": "Price per unit"},
        "amount":      {"type": "number", "description": "Line total"}
      }, "required": ["description", "quantity"]}
    }
  }
}
```

## 2-Way Match (PO vs Invoice)

Extract both the PO and the matching invoice (use `deepread-invoice`), then reconcile in code:

```python
po_total = po_fields["total"]
inv_total = invoice_fields["total"]
if abs(po_total - inv_total) > 0.01:
    print(f"⚠ MISMATCH: PO {po_total} vs invoice {inv_total} — hold for review")
else:
    print("✓ PO and invoice match — approve for payment")
```

## Use Cases

- **Procurement automation** — capture POs into your ERP without manual entry
- **AP 2-way / 3-way matching** — reconcile PO ↔ invoice ↔ receipt automatically
- **Supplier management** — track ordered SKUs, quantities, and delivery commitments
- **Spend analysis** — aggregate line items across POs

## Tips

- **Capture `sku`** when present — it's the most reliable key for matching.
- **Recurring supplier format?** Build a blueprint at `https://www.deepread.tech/dashboard/optimizer`.
- **Check `needs_review`** — only flagged fields need a human.

## Related DeepRead Skills

- **deepread-invoice** — match POs against invoices — `clawhub install uday390/deepread-invoice`
- **deepread-ocr** — general extraction — `clawhub install uday390/deepread-ocr`
- **deepread-byok** — bring your own AI key — `clawhub install uday390/deepread-byok`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
