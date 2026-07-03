---
name: deepread-shipping-docs
title: DeepRead Shipping Documents
description: Extract structured data from bills of lading, packing lists, and shipping manifests — shipper, consignee, carrier, tracking, containers, line items, weights — as typed JSON. Works on PDFs and scans. Per-field confidence flags. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Shipping Documents

Turn bills of lading, packing lists, and shipping manifests into clean, typed JSON — shipper, consignee, carrier, tracking/BOL numbers, containers, and itemized contents with weights — with a `needs_review` flag on every field. Logistics paperwork, finally machine-readable.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "bol_number", "value": "BOL-99213", "needs_review": false, "location": {"page": 1}},
      {"key": "carrier", "value": "Blue Ocean Freight", "needs_review": false, "location": {"page": 1}},
      {"key": "shipper", "value": "Globex Mfg, Shenzhen", "needs_review": false, "location": {"page": 1}},
      {"key": "consignee", "value": "Initech Inc, Austin TX", "needs_review": false, "location": {"page": 1}},
      {"key": "ship_date", "value": "2026-03-28", "needs_review": false, "location": {"page": 1}},
      {"key": "container_numbers", "value": ["MSKU7654321"], "needs_review": false, "location": {"page": 1}},
      {"key": "total_weight_kg", "value": 1840.5, "needs_review": false, "location": {"page": 1}},
      {"key": "items", "value": [
        {"description": "Widgets, palletized", "quantity": 40, "weight_kg": 1600.0},
        {"description": "Spare parts", "quantity": 6, "weight_kg": 240.5}
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
    "document_type":  {"type": "string", "description": "Bill of Lading, Packing List, or Manifest"},
    "bol_number":     {"type": ["string","null"], "description": "Bill of lading / tracking number"},
    "carrier":        {"type": ["string","null"], "description": "Carrier / freight company"},
    "shipper":        {"type": "string", "description": "Shipper name and origin"},
    "consignee":      {"type": "string", "description": "Consignee name and destination"},
    "ship_date":      {"type": ["string","null"], "description": "Ship date (YYYY-MM-DD)"},
    "container_numbers": {"type": "array", "items": {"type": "string"}, "description": "Container / seal numbers"},
    "total_weight_kg":{"type": ["number","null"], "description": "Total gross weight in kg"},
    "incoterms":      {"type": ["string","null"], "description": "Incoterms, e.g. FOB, CIF"},
    "items": {
      "type": "array",
      "description": "Itemized contents",
      "items": {"type": "object", "properties": {
        "description": {"type": "string", "description": "Item / commodity description"},
        "quantity":    {"type": ["number","null"], "description": "Quantity / packages"},
        "weight_kg":   {"type": ["number","null"], "description": "Weight in kg"}
      }, "required": ["description"]}
    }
  }
}
```

## Extract (cURL)

```bash
curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@bol.pdf" \
  -F 'schema={"type":"object","properties":{"bol_number":{"type":"string"},"carrier":{"type":"string"},"shipper":{"type":"string"},"consignee":{"type":"string"},"items":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"quantity":{"type":"number"}}}}}}'
```

## Use Cases

- **Freight & logistics** — capture BOLs and manifests into a TMS without rekeying
- **Customs & compliance** — extract commodities, weights, and incoterms for filings
- **Warehouse receiving** — reconcile packing lists against received goods
- **Supply-chain visibility** — track containers and shipments across documents

## Tips

- **`container_numbers` as an array** handles multi-container shipments cleanly.
- **Recurring carrier format?** Build a blueprint at `https://www.deepread.tech/dashboard/optimizer`.
- **Check `needs_review`** — handwritten weights/quantities are the usual flags.

## Related DeepRead Skills

- **deepread-invoice** — commercial invoices for shipments — `clawhub install uday390/deepread-invoice`
- **deepread-purchase-orders** — match shipments to POs — `clawhub install uday390/deepread-purchase-orders`
- **deepread-ocr** — general extraction — `clawhub install uday390/deepread-ocr`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
