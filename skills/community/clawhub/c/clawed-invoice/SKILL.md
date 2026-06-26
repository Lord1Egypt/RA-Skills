---
name: Clawed Invoice Generator
slug: clawed-invoice
version: 1.0.0
description: "Generate professional PDF invoices with a clean layout — no Playwright, no browser, no complex dependencies. Built for reliability on constrained hosting environments ( Railway, minimal containers, offline setups). Just jsPDF + plain Node.js. Supports EUR/GBP/USD, multi-item tables, custom brand colours, and payment details footer."
inputs:
  invoiceNumber: Unique invoice number (e.g. "INV-001")
  invoiceDate: Invoice issue date (e.g. "01/06/2026")
  customerNumber: Customer account reference (e.g. "CUST-001")
  dueDate: Payment due date (e.g. "07/06/2026")
  customerName: Customer or company name (e.g. "Acme Corp")
  customerAddress: Multiline address (e.g. "123 High Street\nLondon, EC1 1AB")
  entity:
    description: Company entity block from config
    properties:
      entity: Company legal name
      swift: SWIFT/BIC code
      iban: IBAN bank account
      companyNumber: Registration number
  items:
    - code: Line item code/reference (e.g. "SVC")
      description: Service or product description
      qty: Quantity (default "1")
      net: Net amount before VAT (e.g. "1,000.00")
      vatRate: VAT rate as string (e.g. "20%" or "0%")
      vatAmt: VAT charge amount (e.g. "200.00")
      gross: Gross amount incl. VAT (e.g. "1,200.00")
  currency: EUR | GBP | USD — selects currency symbol (default EUR)
  outputDir: Output directory (default /tmp/invoices)
outputs:
  invoice-<invoiceNumber>.pdf: PDF written to outputDir
examples:
  - description: Generate a sample GBP invoice
    command: |
      node /data/workspace/skills/clawed-invoice/scripts/generate.js \
        --config /data/workspace/skills/clawed-invoice/references/config.json \
        --data '{"invoiceNumber":"INV-001","invoiceDate":"01/06/2026","customerNumber":"CUST-001","dueDate":"07/06/2026","customerName":"Acme Corp","customerAddress":"123 High Street\nLondon, EC1 1AB","items":[{"code":"SVC","description":"Consulting services — 8 hours","qty":"8","net":"2,400.00","vatRate":"20%","vatAmt":"480.00","gross":"2,880.00"}],"currency":"GBP","entity":"default"}'
---

# Clawed Invoice Generator

Generate clean, professional PDF invoices with a consistent layout and customisable brand colours.

## Layout

```
┌─────────────────────────────────────────────────────────┐
│  HEADER BAR (dark)  │  Invoice No / Date / Customer No │
│  COMPANY NAME (gold) │  Payment Due Date                  │
├─────────────────────────────────────────────────────────┤
│  BILL TO                                                       │
│  Customer Name                                           │
│  Customer Address                                         │
├─────────────────────────────────────────────────────────┤
│  Code │ Description │ Qty │ Net │ VAT │ Gross            │
│  ─────┼──────────────┼─────┼─────┼─────┼────────          │
│  SVC  │ Service desc │  1  │£xxx │ xx% │ £xxx             │
├─────────────────────────────────────────────────────────┤
│  Subtotal (NET):                              £x,xxx.xx  │
│  VAT 20%:                                     £xxx.xx    │
│  ██████████████ Total ██████████████████████  £x,xxx.xx  │
├─────────────────────────────────────────────────────────┤
│  PAYMENT DETAILS                                         │
│  Account holder: [Company Name]                           │
│  Swift/BIC:    [XXXXXXXX]                                │
│  IBAN:         [XXXX XXXX XXXX XXXX]                    │
├─────────────────────────────────────────────────────────┤
│  Notes / payment terms / legal text                       │
└─────────────────────────────────────────────────────────┘
```

## Colour Palette (customisable via config)

| Element         | Hex       | Usage                        |
|-----------------|-----------|------------------------------|
| Header / boxes  | `#2F3640` | Dark charcoal — use in config |
| Accent / total  | `#FFC11E` | Gold — use in config          |
| Row background  | `#F8F8F8` | Light grey alternating rows   |
| Body text       | `#000000` | Primary content               |
| Labels / muted  | `#505050` | Secondary text                |

## Usage

**1. Prepare your invoice data as JSON:**
```json
{
  "invoiceNumber": "INV-001",
  "invoiceDate":   "01/06/2026",
  "customerNumber": "CUST-001",
  "dueDate":       "07/06/2026",
  "customerName":  "Acme Corp",
  "customerAddress": "123 High Street\nLondon, EC1 1AB",
  "items": [
    {
      "code": "SVC",
      "description": "Consulting services",
      "qty": "8",
      "net": "2,400.00",
      "vatRate": "20%",
      "vatAmt": "480.00",
      "gross": "2,880.00"
    }
  ],
  "currency": "GBP",
  "entity": "default"
}
```

**2. Run the generator:**
```bash
node /data/workspace/skills/clawed-invoice/scripts/generate.js \
  --config /data/workspace/skills/clawed-invoice/references/config.json \
  --datafile /path/to/your-invoice.json
```

**3. Output** → `invoice-INV-001.pdf` in `/tmp/invoices/` (or your `outputDir`)

## Configuration

Edit `references/config.json` to set your company details once — the generator pulls them automatically per invoice:

```json
{
  "default": {
    "entity": "Your Company Name Ltd",
    "swift": "XXXXXXXX",
    "iban": "XXXX XXXX XXXX XXXX XXXX",
    "companyNumber": "XXXXXXX",
    "currency": "GBP",
    "vatRate": "20%"
  }
}
```

For multiple entities (e.g. UK + EU subsidiaries), add additional keys and select via `entity: "eu"` in your invoice data.

## Dependencies

Requires `jspdf` installed at `/data/local/node_modules/jspdf`