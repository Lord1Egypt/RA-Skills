---
name: invoice-generator
description: Generate professional PDF invoices from natural language or structured data. Use when the user asks to create an invoice, bill a client, generate a receipt, track payments, or manage invoicing. Supports line items, tax calculation, discounts, multiple currencies, recurring invoices, and payment tracking. Outputs clean PDF invoices ready to send.
---

# Invoice Generator

Create professional invoices instantly from your agent.

## Quick Start

Generate an invoice:
```bash
python3 scripts/invoice.py create \
  --client "Acme Corp" \
  --items "Web Development,40h,$150" "Hosting Setup,1,$500" \
  --tax 7 \
  --due-days 30
```

## Commands

### Create Invoice
```bash
python3 scripts/invoice.py create \
  --client "Client Name" \
  --items "Description,Qty,Rate" \
  --tax 7 \
  --discount 10 \
  --currency USD \
  --due-days 30 \
  --notes "Payment via wire transfer"
```

### From Natural Language
When the user says something like "Invoice Acme Corp for 40 hours of dev work at $150/hr plus a $500 setup fee, 7% tax, net 30" — parse and pass to the create command.

### List Invoices
```bash
python3 scripts/invoice.py list
python3 scripts/invoice.py list --status unpaid
```

### Mark as Paid
```bash
python3 scripts/invoice.py paid --id INV-2026-001
```

### View Invoice
```bash
python3 scripts/invoice.py view --id INV-2026-001
```

## Business Info Setup

Configure your business details once:
```bash
python3 scripts/invoice.py setup \
  --business "Your Company" \
  --email "billing@company.com" \
  --address "123 Main St, City, ST 12345" \
  --phone "+1-555-0100" \
  --logo assets/logo.png
```

Stored at `~/.openclaw/invoice-config.json`.

## Invoice Format

Generated invoices include:
- Invoice number (auto-incrementing: INV-YYYY-NNN)
- Business and client details
- Itemized line items with quantities and rates
- Subtotal, tax, discount, and total
- Due date and payment terms
- Notes/terms section
- Professional formatting

## Output

- PDF saved to `~/Documents/Invoices/INV-YYYY-NNN.pdf`
- Markdown summary printed to chat
- Optional: email invoice directly via configured email skill

## Currencies

Supports: USD, EUR, GBP, CAD, AUD, JPY, CHF, and 20+ others with proper symbol formatting.

## Recurring Invoices

```bash
python3 scripts/invoice.py recurring \
  --client "Client" \
  --items "Monthly Retainer,1,$2000" \
  --frequency monthly \
  --start 2026-03-01
```

Set up as a cron job for automatic generation and delivery.
