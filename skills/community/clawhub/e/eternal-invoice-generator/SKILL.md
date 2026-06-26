---
name: invoice-generator
description: Generate professional PDF invoices from command-line input or templates. Use when the user wants to: create an invoice, generate a bill, send a payment request, create a receipt for services/products, or manage invoice templates. Triggers on "create invoice", "generate bill", "invoice for", "make a receipt", "payment request", "bill template".
---

# Invoice Generator

Create professional PDF invoices from the command line.

## Quick Start

```bash
python3 scripts/invoice.py create \
  --from "Your Business Name" \
  --to "Client Name" \
  --item "Consulting,8hrs,75" \
  --item "Design,3hrs,100" \
  --due 14
```

## Commands

| Command | Description |
|---------|-------------|
| `create` | Generate a new invoice PDF |
| `estimate` | Create a quote/estimate instead |
| `recurring` | Set up a recurring invoice template |
| `list` | List generated invoices |
| `remind` | Generate a payment reminder |

## Item Format

Items are specified as: `"Description,Quantity,UnitPrice"`

Examples:
- `"Web Development,40,85"` — 40 hours at $85/hr
- `"Logo Design,1,1500"` — flat rate $1500
- `"Hosting,12,29.99"` — 12 months at $29.99/mo

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--from` | (required) | Your business/personal name |
| `--from-email` | | Your email |
| `--from-address` | | Your address |
| `--to` | (required) | Client name |
| `--to-email` | | Client email |
| `--to-address` | | Client address |
| `--item` | (repeatable) | Line items |
| `--tax` | 0 | Tax percentage |
| `--discount` | 0 | Discount percentage or flat amount |
| `--due` | 30 | Payment due in N days |
| `--currency` | USD | Currency code |
| `--notes` | | Additional notes |
| `--prefix` | INV | Invoice number prefix |
| `--bank` | | Bank details for payment |
| `--output` | auto | Output filename |

## Output

Generates a clean, professional PDF with:
- Invoice number (auto-incremented)
- Issue date and due date
- Itemized line items with subtotals
- Tax, discount, and total calculations
- Payment terms and bank details
- Professional formatting

## Templates

Invoices use a clean minimal template by default. To customize:
1. Edit `scripts/invoice_template.html`
2. Add your logo to `assets/logo.png`
