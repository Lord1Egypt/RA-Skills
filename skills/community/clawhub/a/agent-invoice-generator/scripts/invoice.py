#!/usr/bin/env python3
"""Invoice Generator - Create professional PDF invoices."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "invoice-config.json"
DATA_PATH = Path.home() / ".openclaw" / "invoices"
OUTPUT_DIR = Path.home() / "Documents" / "Invoices"

CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "CAD": "C$", "AUD": "A$",
    "JPY": "¥", "CHF": "CHF", "CNY": "¥", "INR": "₹", "BRL": "R$",
    "MXN": "MX$", "KRW": "₩", "SEK": "kr", "NOK": "kr", "DKK": "kr",
    "PLN": "zł", "CZK": "Kč", "HUF": "Ft", "TRY": "₺", "ZAR": "R",
    "SGD": "S$", "HKD": "HK$", "NZD": "NZ$", "THB": "฿",
}


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {
        "business": {"name": "", "email": "", "address": "", "phone": ""},
        "nextNumber": 1,
        "defaultCurrency": "USD",
        "defaultTax": 0,
        "defaultDueDays": 30,
    }


def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))


def get_invoice_number(config):
    year = datetime.now().year
    num = config.get("nextNumber", 1)
    config["nextNumber"] = num + 1
    save_config(config)
    return f"INV-{year}-{num:03d}"


def parse_items(item_strings):
    """Parse item strings in format 'Description,Qty,Rate'."""
    items = []
    for item_str in item_strings:
        parts = item_str.split(",")
        if len(parts) != 3:
            print(f"Warning: Invalid item format '{item_str}', expected 'Description,Qty,Rate'")
            continue
        desc = parts[0].strip()
        qty = float(parts[1].strip().rstrip("h"))
        rate = float(parts[2].strip().lstrip("$€£"))
        items.append({"description": desc, "quantity": qty, "rate": rate, "amount": qty * rate})
    return items


def generate_pdf(invoice, output_path):
    """Generate PDF invoice. Falls back to HTML if reportlab unavailable."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Header
        elements.append(Paragraph(f"<b>{invoice['business']['name']}</b>", styles['Title']))
        elements.append(Paragraph(invoice['business'].get('address', ''), styles['Normal']))
        elements.append(Paragraph(invoice['business'].get('email', ''), styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

        # Invoice details
        elements.append(Paragraph(f"<b>INVOICE {invoice['number']}</b>", styles['Heading1']))
        elements.append(Paragraph(f"Date: {invoice['date']}", styles['Normal']))
        elements.append(Paragraph(f"Due: {invoice['dueDate']}", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        # Client
        elements.append(Paragraph(f"<b>Bill To:</b>", styles['Normal']))
        elements.append(Paragraph(invoice['client'], styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

        # Items table
        sym = CURRENCY_SYMBOLS.get(invoice['currency'], '$')
        data = [['Description', 'Qty', 'Rate', 'Amount']]
        for item in invoice['items']:
            data.append([
                item['description'],
                f"{item['quantity']:.0f}" if item['quantity'] == int(item['quantity']) else f"{item['quantity']:.1f}",
                f"{sym}{item['rate']:.2f}",
                f"{sym}{item['amount']:.2f}",
            ])

        table = Table(data, colWidths=[3.5 * inch, 0.8 * inch, 1.2 * inch, 1.2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))

        # Totals
        totals_data = [
            ['', '', 'Subtotal:', f"{sym}{invoice['subtotal']:.2f}"],
        ]
        if invoice.get('discount', 0) > 0:
            totals_data.append(['', '', f"Discount ({invoice['discount']}%):", f"-{sym}{invoice['discountAmount']:.2f}"])
        if invoice.get('tax', 0) > 0:
            totals_data.append(['', '', f"Tax ({invoice['tax']}%):", f"{sym}{invoice['taxAmount']:.2f}"])
        totals_data.append(['', '', 'TOTAL:', f"{sym}{invoice['total']:.2f}"])

        totals = Table(totals_data, colWidths=[3.5 * inch, 0.8 * inch, 1.2 * inch, 1.2 * inch])
        totals.setStyle(TableStyle([
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
            ('LINEABOVE', (2, -1), (-1, -1), 1, colors.black),
        ]))
        elements.append(totals)

        # Notes
        if invoice.get('notes'):
            elements.append(Spacer(1, 0.4 * inch))
            elements.append(Paragraph(f"<b>Notes:</b>", styles['Normal']))
            elements.append(Paragraph(invoice['notes'], styles['Normal']))

        doc.build(elements)
        return True

    except ImportError:
        # Fallback: generate HTML invoice
        html_path = output_path.with_suffix('.html')
        sym = CURRENCY_SYMBOLS.get(invoice['currency'], '$')
        html = f"""<!DOCTYPE html>
<html><head><style>
body {{ font-family: -apple-system, Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
.header {{ border-bottom: 3px solid #2C3E50; padding-bottom: 20px; margin-bottom: 20px; }}
.invoice-num {{ color: #2C3E50; font-size: 24px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th {{ background: #2C3E50; color: white; padding: 10px; text-align: left; }}
td {{ padding: 8px 10px; border-bottom: 1px solid #eee; }}
.totals td {{ text-align: right; }}
.total-row {{ font-weight: bold; border-top: 2px solid #333; }}
.notes {{ margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 4px; }}
</style></head><body>
<div class="header">
<h1>{invoice['business']['name']}</h1>
<p>{invoice['business'].get('address', '')}<br>{invoice['business'].get('email', '')}</p>
</div>
<div class="invoice-num">INVOICE {invoice['number']}</div>
<p>Date: {invoice['date']}<br>Due: {invoice['dueDate']}</p>
<p><strong>Bill To:</strong><br>{invoice['client']}</p>
<table>
<tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
"""
        for item in invoice['items']:
            html += f"<tr><td>{item['description']}</td><td>{item['quantity']}</td><td>{sym}{item['rate']:.2f}</td><td>{sym}{item['amount']:.2f}</td></tr>\n"

        html += f"""</table>
<table class="totals">
<tr><td colspan="3">Subtotal:</td><td>{sym}{invoice['subtotal']:.2f}</td></tr>
"""
        if invoice.get('discount', 0) > 0:
            html += f"<tr><td colspan='3'>Discount ({invoice['discount']}%):</td><td>-{sym}{invoice['discountAmount']:.2f}</td></tr>\n"
        if invoice.get('tax', 0) > 0:
            html += f"<tr><td colspan='3'>Tax ({invoice['tax']}%):</td><td>{sym}{invoice['taxAmount']:.2f}</td></tr>\n"
        html += f"""<tr class="total-row"><td colspan="3">TOTAL:</td><td>{sym}{invoice['total']:.2f}</td></tr>
</table>
"""
        if invoice.get('notes'):
            html += f'<div class="notes"><strong>Notes:</strong><br>{invoice["notes"]}</div>'
        html += "</body></html>"

        html_path.write_text(html)
        print(f"Note: Install reportlab for PDF output (pip3 install reportlab). HTML generated instead.")
        return True


def create_invoice(args):
    config = load_config()

    if not config['business'].get('name'):
        print("Warning: Business info not configured. Run 'setup' first.")

    items = parse_items(args.items)
    if not items:
        print("Error: No valid items provided.")
        return

    subtotal = sum(i['amount'] for i in items)
    discount_pct = args.discount or 0
    discount_amount = subtotal * (discount_pct / 100)
    after_discount = subtotal - discount_amount
    tax_pct = args.tax or config.get('defaultTax', 0)
    tax_amount = after_discount * (tax_pct / 100)
    total = after_discount + tax_amount

    due_days = args.due_days or config.get('defaultDueDays', 30)
    currency = args.currency or config.get('defaultCurrency', 'USD')

    invoice = {
        "number": get_invoice_number(config),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "dueDate": (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d"),
        "client": args.client,
        "business": config['business'],
        "items": items,
        "subtotal": subtotal,
        "discount": discount_pct,
        "discountAmount": discount_amount,
        "tax": tax_pct,
        "taxAmount": tax_amount,
        "total": total,
        "currency": currency,
        "notes": args.notes or "",
        "status": "unpaid",
    }

    # Save invoice data
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    (DATA_PATH / f"{invoice['number']}.json").write_text(json.dumps(invoice, indent=2))

    # Generate PDF
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{invoice['number']}.pdf"
    generate_pdf(invoice, output_path)

    sym = CURRENCY_SYMBOLS.get(currency, '$')
    print(f"\nInvoice Created: {invoice['number']}")
    print(f"Client: {args.client}")
    print(f"Items: {len(items)}")
    print(f"Subtotal: {sym}{subtotal:.2f}")
    if discount_pct:
        print(f"Discount: {discount_pct}% (-{sym}{discount_amount:.2f})")
    if tax_pct:
        print(f"Tax: {tax_pct}% (+{sym}{tax_amount:.2f})")
    print(f"Total: {sym}{total:.2f}")
    print(f"Due: {invoice['dueDate']}")
    print(f"Saved: {output_path}")


def list_invoices(args):
    if not DATA_PATH.exists():
        print("No invoices found.")
        return

    invoices = []
    for f in sorted(DATA_PATH.glob("INV-*.json")):
        inv = json.loads(f.read_text())
        if args.status and inv.get("status") != args.status:
            continue
        invoices.append(inv)

    if not invoices:
        print("No invoices match.")
        return

    print(f"{'Invoice':<16} | {'Client':<20} | {'Total':>10} | {'Status':<8} | {'Due'}")
    print("-" * 75)
    for inv in invoices:
        sym = CURRENCY_SYMBOLS.get(inv.get('currency', 'USD'), '$')
        print(f"{inv['number']:<16} | {inv['client'][:20]:<20} | {sym}{inv['total']:>9.2f} | {inv.get('status', 'unpaid'):<8} | {inv['dueDate']}")


def mark_paid(args):
    path = DATA_PATH / f"{args.id}.json"
    if not path.exists():
        print(f"Invoice {args.id} not found.")
        return
    inv = json.loads(path.read_text())
    inv["status"] = "paid"
    inv["paidDate"] = datetime.now().strftime("%Y-%m-%d")
    path.write_text(json.dumps(inv, indent=2))
    print(f"Invoice {args.id} marked as paid.")


def setup_business(args):
    config = load_config()
    config["business"] = {
        "name": args.business,
        "email": args.email or "",
        "address": args.address or "",
        "phone": args.phone or "",
    }
    save_config(config)
    print(f"Business info saved for: {args.business}")


def main():
    parser = argparse.ArgumentParser(description="Invoice Generator")
    sub = parser.add_subparsers(dest="command")

    create_p = sub.add_parser("create")
    create_p.add_argument("--client", required=True)
    create_p.add_argument("--items", nargs="+", required=True)
    create_p.add_argument("--tax", type=float, default=0)
    create_p.add_argument("--discount", type=float, default=0)
    create_p.add_argument("--currency", default="USD")
    create_p.add_argument("--due-days", type=int, default=30)
    create_p.add_argument("--notes", default="")

    list_p = sub.add_parser("list")
    list_p.add_argument("--status", choices=["paid", "unpaid"])

    paid_p = sub.add_parser("paid")
    paid_p.add_argument("--id", required=True)

    view_p = sub.add_parser("view")
    view_p.add_argument("--id", required=True)

    setup_p = sub.add_parser("setup")
    setup_p.add_argument("--business", required=True)
    setup_p.add_argument("--email")
    setup_p.add_argument("--address")
    setup_p.add_argument("--phone")
    setup_p.add_argument("--logo")

    recur_p = sub.add_parser("recurring")
    recur_p.add_argument("--client", required=True)
    recur_p.add_argument("--items", nargs="+", required=True)
    recur_p.add_argument("--frequency", default="monthly")
    recur_p.add_argument("--start", default=datetime.now().strftime("%Y-%m-%d"))

    args = parser.parse_args()

    if args.command == "create":
        create_invoice(args)
    elif args.command == "list":
        list_invoices(args)
    elif args.command == "paid":
        mark_paid(args)
    elif args.command == "setup":
        setup_business(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
