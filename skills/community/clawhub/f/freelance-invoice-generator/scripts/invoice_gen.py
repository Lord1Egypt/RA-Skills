#!/usr/bin/env python3
"""
Freelance Invoice Generator — turn line items into a clean, client-ready
Markdown/HTML invoice with tax, discount, and late-fee terms baked in.

No external services or API keys required. Reads a JSON job file describing
the freelancer, client, and line items, and writes a formatted invoice.

Job JSON schema:
{
  "invoice_number": "INV-2026-014",
  "date": "2026-07-22",
  "due_date": "2026-08-05",
  "from": {"name": "...", "email": "...", "address": "..."},
  "to": {"name": "...", "email": "...", "address": "..."},
  "items": [
    {"description": "Website redesign", "quantity": 1, "rate": 1500},
    {"description": "Hosting setup", "quantity": 2, "rate": 75}
  ],
  "tax_rate_pct": 0,
  "discount_usd": 0,
  "currency": "USD",
  "notes": "Thank you for your business!",
  "late_fee_pct_per_month": 1.5
}

Usage:
    python3 invoice_gen.py job.json --out invoice.md
    python3 invoice_gen.py job.json --out invoice.html --format html
"""

import argparse
import json
import sys
from datetime import datetime


def build_totals(job):
    items = job["items"]
    subtotal = sum(i["quantity"] * i["rate"] for i in items)
    discount = job.get("discount_usd", 0) or 0
    taxable = subtotal - discount
    tax_rate = job.get("tax_rate_pct", 0) or 0
    tax = taxable * (tax_rate / 100)
    total = taxable + tax
    return subtotal, discount, tax, total


def render_markdown(job) -> str:
    subtotal, discount, tax, total = build_totals(job)
    currency = job.get("currency", "USD")
    f = job.get("from", {})
    t = job.get("to", {})

    lines = []
    lines.append(f"# Invoice {job.get('invoice_number', '')}")
    lines.append("")
    lines.append(f"**Date:** {job.get('date', datetime.now().date().isoformat())}  ")
    lines.append(f"**Due:** {job.get('due_date', 'On receipt')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**From:** {f.get('name', '')}")
    if f.get("email"):
        lines.append(f"  {f['email']}")
    if f.get("address"):
        lines.append(f"  {f['address']}")
    lines.append("")
    lines.append(f"**Bill To:** {t.get('name', '')}")
    if t.get("email"):
        lines.append(f"  {t['email']}")
    if t.get("address"):
        lines.append(f"  {t['address']}")
    lines.append("")
    lines.append("| Description | Qty | Rate | Amount |")
    lines.append("|---|---|---|---|")
    for i in job["items"]:
        amount = i["quantity"] * i["rate"]
        lines.append(f"| {i['description']} | {i['quantity']} | {currency} {i['rate']:,.2f} | {currency} {amount:,.2f} |")
    lines.append("")
    lines.append(f"**Subtotal:** {currency} {subtotal:,.2f}  ")
    if discount:
        lines.append(f"**Discount:** -{currency} {discount:,.2f}  ")
    if job.get("tax_rate_pct"):
        lines.append(f"**Tax ({job['tax_rate_pct']}%):** {currency} {tax:,.2f}  ")
    lines.append(f"**Total Due:** {currency} {total:,.2f}")
    lines.append("")
    if job.get("late_fee_pct_per_month"):
        lines.append(f"_Late payments are subject to a {job['late_fee_pct_per_month']}% monthly fee after the due date._")
        lines.append("")
    if job.get("notes"):
        lines.append(f"**Notes:** {job['notes']}")
    return "\n".join(lines)


def render_html(job) -> str:
    subtotal, discount, tax, total = build_totals(job)
    currency = job.get("currency", "USD")
    f = job.get("from", {})
    t = job.get("to", {})
    rows = "".join(
        f"<tr><td>{i['description']}</td><td>{i['quantity']}</td>"
        f"<td>{currency} {i['rate']:,.2f}</td>"
        f"<td>{currency} {i['quantity'] * i['rate']:,.2f}</td></tr>"
        for i in job["items"]
    )
    extra_rows = ""
    if discount:
        extra_rows += f"<tr><td colspan=3 align=right>Discount</td><td>-{currency} {discount:,.2f}</td></tr>"
    if job.get("tax_rate_pct"):
        extra_rows += f"<tr><td colspan=3 align=right>Tax ({job['tax_rate_pct']}%)</td><td>{currency} {tax:,.2f}</td></tr>"

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Invoice {job.get('invoice_number', '')}</title>
<style>
body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; max-width: 720px; margin: 40px auto; color: #1a1a1a; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
th {{ background: #f5f5f5; }}
.total {{ font-size: 1.2em; font-weight: bold; }}
.meta {{ color: #555; }}
</style></head>
<body>
<h1>Invoice {job.get('invoice_number', '')}</h1>
<p class="meta">Date: {job.get('date', datetime.now().date().isoformat())} &nbsp;|&nbsp; Due: {job.get('due_date', 'On receipt')}</p>
<hr>
<p><strong>From:</strong> {f.get('name', '')}<br>{f.get('email', '')}<br>{f.get('address', '')}</p>
<p><strong>Bill To:</strong> {t.get('name', '')}<br>{t.get('email', '')}<br>{t.get('address', '')}</p>
<table>
<tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
{rows}
{extra_rows}
<tr class="total"><td colspan=3 align=right>Total Due</td><td>{currency} {total:,.2f}</td></tr>
</table>
{"<p><em>Late payments are subject to a " + str(job['late_fee_pct_per_month']) + "% monthly fee after the due date.</em></p>" if job.get('late_fee_pct_per_month') else ""}
{"<p><strong>Notes:</strong> " + job['notes'] + "</p>" if job.get('notes') else ""}
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Generate a freelance invoice from a JSON job file")
    ap.add_argument("job_json", help="Path to job JSON file")
    ap.add_argument("--out", required=True, help="Output file path")
    ap.add_argument("--format", choices=["markdown", "html"], default="markdown")
    args = ap.parse_args()

    with open(args.job_json) as f:
        job = json.load(f)

    if not job.get("items"):
        sys.exit("Job file must include at least one line item under 'items'")

    content = render_html(job) if args.format == "html" else render_markdown(job)
    with open(args.out, "w") as f:
        f.write(content)

    _, _, _, total = build_totals(job)
    print(f"Invoice written to {args.out}")
    print(f"Total due: {job.get('currency', 'USD')} {total:,.2f}")


if __name__ == "__main__":
    main()
