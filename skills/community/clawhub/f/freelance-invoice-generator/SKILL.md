---
name: freelance-invoice-generator
description: Generate professional, client-ready freelance invoices in Markdown or HTML from a simple JSON job file with line items, tax rate, discounts, and late-fee terms. No external API, account, or subscription required. Useful for freelance consulting, python contract work, ai agent development gigs, and any passive income side hustle that needs fast, clean invoicing without paying for QuickBooks or FreshBooks. Handles multi-item invoices, subtotal/discount/tax math, and due-date and late-payment-fee language automatically.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Freelance Invoice Generator

Generates a polished invoice (Markdown or HTML) from a plain JSON job
description — no signup, no paid invoicing SaaS.

## When to use this skill

- Billing a client for freelance/consulting work and you want a clean,
  professional document in under a minute
- Need consistent invoice numbering, tax math, and late-fee language across
  multiple clients
- Want an invoice you can convert to PDF (e.g. via `pandoc`) or paste into
  an email

## How to use it

1. Create a job JSON file describing the invoice (see the docstring in
   `scripts/invoice_gen.py` for the full schema):
   ```json
   {
     "invoice_number": "INV-2026-014",
     "date": "2026-07-22",
     "due_date": "2026-08-05",
     "from": {"name": "Your Name", "email": "you@example.com"},
     "to": {"name": "Client Co", "email": "ap@client.com"},
     "items": [{"description": "Backend API build", "quantity": 1, "rate": 1500}],
     "tax_rate_pct": 5,
     "discount_usd": 0,
     "notes": "Thanks for the business!",
     "late_fee_pct_per_month": 1.5
   }
   ```
2. Generate the invoice:
   ```
   python3 scripts/invoice_gen.py job.json --out invoice.md
   python3 scripts/invoice_gen.py job.json --out invoice.html --format html
   ```
3. Optionally convert to PDF with `pandoc invoice.md -o invoice.pdf` if
   pandoc is available in your environment.

## Limitations

- Single currency per invoice (no multi-currency conversion)
- Does not track payment status or send the invoice — generation only
- No built-in recurring/subscription billing
