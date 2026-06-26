#!/usr/bin/env python3
"""
Invoice Generator — Create professional PDF invoices.
Uses fpdf2 for PDF generation.
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / '.invoices'
COUNTER_FILE = DATA_DIR / 'counter.json'


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_next_number(prefix='INV'):
    """Get next invoice number."""
    ensure_data_dir()
    counter = {}
    if COUNTER_FILE.exists():
        with open(COUNTER_FILE) as f:
            counter = json.load(f)
    
    key = prefix
    counter[key] = counter.get(key, 0) + 1
    
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counter, f)
    
    return f"{prefix}-{counter[key]:04d}"


def parse_item(item_str):
    """Parse item string: 'Description,Quantity,UnitPrice'"""
    parts = item_str.split(',')
    if len(parts) < 3:
        raise ValueError(f"Item must be 'Description,Quantity,Price': got '{item_str}'")
    
    desc = parts[0].strip()
    qty = float(parts[1].strip())
    price = float(parts[2].strip())
    
    return {
        'description': desc,
        'quantity': qty,
        'unit_price': price,
        'total': qty * price
    }


def generate_invoice(args):
    """Generate a PDF invoice."""
    try:
        from fpdf import FPDF
    except ImportError:
        print("  ❌ Install fpdf2: pip install fpdf2")
        sys.exit(1)
    
    ensure_data_dir()
    
    # Parse items
    items = [parse_item(i) for i in args.item]
    subtotal = sum(i['total'] for i in items)
    
    # Tax and discount
    tax_pct = float(args.tax) if args.tax else 0
    discount_pct = float(args.discount) if args.discount else 0
    
    discount = subtotal * (discount_pct / 100)
    taxable = subtotal - discount
    tax = taxable * (tax_pct / 100)
    total = taxable + tax
    
    # Invoice details
    inv_number = get_next_number(args.prefix or 'INV')
    issue_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=int(args.due or 30))).strftime('%Y-%m-%d')
    currency = args.currency or 'USD'
    curr_sym = {'USD': '$', 'EUR': '€', 'GBP': '£', 'BDT': '৳', 'JPY': '¥', 'CAD': 'C$', 'AUD': 'A$'}.get(currency, currency + ' ')
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)
    
    # Header
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 15, 'INVOICE', align='R', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, inv_number, align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 6, f'Issue Date: {issue_date}', align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 6, f'Due Date: {due_date}', align='R', new_x='LMARGIN', new_y='NEXT')
    
    pdf.ln(10)
    
    # From / To
    pdf.set_text_color(0, 0, 0)
    y_start = pdf.get_y()
    
    # From (left)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(95, 7, 'FROM:', new_x='RIGHT', new_y='TOP')
    
    # To (right)
    pdf.cell(95, 7, 'BILL TO:', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(95, 6, args.from_name or 'Your Business', new_x='RIGHT', new_y='TOP')
    pdf.cell(95, 6, args.to or 'Client Name', new_x='LMARGIN', new_y='NEXT')
    
    if args.from_email:
        pdf.cell(95, 6, args.from_email, new_x='RIGHT', new_y='TOP')
    if args.to_email:
        pdf.cell(95, 6, args.to_email, new_x='LMARGIN', new_y='NEXT')
    else:
        pdf.ln(6)
    
    if args.from_address:
        pdf.cell(95, 6, args.from_address, new_x='RIGHT', new_y='TOP')
    if args.to_address:
        pdf.cell(95, 6, args.to_address, new_x='LMARGIN', new_y='NEXT')
    else:
        pdf.ln(6)
    
    pdf.ln(10)
    
    # Table header
    pdf.set_fill_color(45, 45, 45)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    
    col_w = [80, 25, 35, 40]  # desc, qty, unit price, total
    headers = ['Description', 'Qty', 'Unit Price', 'Total']
    
    for i, (h, w) in enumerate(zip(headers, col_w)):
        pdf.cell(w, 9, h, border=0, fill=True, align='C' if i > 0 else 'L')
    pdf.ln()
    
    # Table rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    
    for idx, item in enumerate(items):
        if idx % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        
        pdf.cell(col_w[0], 8, item['description'][:40], border=0, fill=True)
        pdf.cell(col_w[1], 8, f"{item['quantity']:.0f}" if item['quantity'] == int(item['quantity']) else f"{item['quantity']:.2f}", border=0, fill=True, align='C')
        pdf.cell(col_w[2], 8, f"{curr_sym}{item['unit_price']:,.2f}", border=0, fill=True, align='R')
        pdf.cell(col_w[3], 8, f"{curr_sym}{item['total']:,.2f}", border=0, fill=True, align='R')
        pdf.ln()
    
    # Line separator
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    # Totals
    pdf.set_font('Helvetica', '', 10)
    total_x = 130
    label_w = 35
    val_w = 35
    
    pdf.cell(total_x, 7, '', new_x='RIGHT', new_y='TOP')
    pdf.cell(label_w, 7, 'Subtotal:', align='R', new_x='RIGHT', new_y='TOP')
    pdf.cell(val_w, 7, f"{curr_sym}{subtotal:,.2f}", align='R', new_x='LMARGIN', new_y='NEXT')
    
    if discount_pct > 0:
        pdf.cell(total_x, 7, '', new_x='RIGHT', new_y='TOP')
        pdf.cell(label_w, 7, f'Discount ({discount_pct}%):', align='R', new_x='RIGHT', new_y='TOP')
        pdf.set_text_color(200, 0, 0)
        pdf.cell(val_w, 7, f"-{curr_sym}{discount:,.2f}", align='R', new_x='LMARGIN', new_y='NEXT')
        pdf.set_text_color(0, 0, 0)
    
    if tax_pct > 0:
        pdf.cell(total_x, 7, '', new_x='RIGHT', new_y='TOP')
        pdf.cell(label_w, 7, f'Tax ({tax_pct}%):', align='R', new_x='RIGHT', new_y='TOP')
        pdf.cell(val_w, 7, f"{curr_sym}{tax:,.2f}", align='R', new_x='LMARGIN', new_y='NEXT')
    
    # Grand total
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(total_x, 10, '', new_x='RIGHT', new_y='TOP')
    pdf.cell(label_w, 10, 'TOTAL:', align='R', new_x='RIGHT', new_y='TOP')
    pdf.cell(val_w, 10, f"{curr_sym}{total:,.2f}", align='R', new_x='LMARGIN', new_y='NEXT')
    
    pdf.ln(10)
    
    # Payment info
    if args.bank:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 7, 'Payment Details:', new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('Helvetica', '', 9)
        for line in args.bank.split(';'):
            pdf.cell(0, 5, line.strip(), new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
    
    # Notes
    if args.notes:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 7, 'Notes:', new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('Helvetica', '', 9)
        pdf.multi_cell(0, 5, args.notes)
        pdf.ln(5)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, f'Payment due within {args.due or 30} days. Thank you for your business.', align='C')
    
    # Save
    output = args.output or f"{inv_number}.pdf"
    pdf.output(output)
    
    print(f"\n  ✅ Invoice generated: {output}")
    print(f"     📋 Number:   {inv_number}")
    print(f"     📅 Issued:   {issue_date}")
    print(f"     ⏰ Due:      {due_date}")
    print(f"     💰 Total:    {curr_sym}{total:,.2f}")
    print(f"     📦 Items:    {len(items)}")
    print(f"     📁 File:     {os.path.abspath(output)}")
    
    return output


def cmd_create(args):
    generate_invoice(args)


def cmd_list(args):
    """List generated invoices."""
    inv_dir = Path('.')
    invoices = sorted(inv_dir.glob('INV-*.pdf'))
    
    if not invoices:
        print("\n  📭 No invoices found in current directory.")
        return
    
    print(f"\n  📋 Invoices ({len(invoices)}):")
    for inv in invoices:
        size = inv.stat().st_size / 1024
        mtime = datetime.fromtimestamp(inv.stat().st_mtime).strftime('%Y-%m-%d')
        print(f"     📄 {inv.name:20s}  {size:>6.1f}KB  {mtime}")


def cmd_remind(args):
    """Generate a payment reminder."""
    try:
        from fpdf import FPDF
    except ImportError:
        print("  ❌ Install fpdf2: pip install fpdf2")
        sys.exit(1)
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'PAYMENT REMINDER', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%Y-%m-%d")}', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)
    
    if args.to:
        pdf.cell(0, 8, f'Dear {args.to},', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
    
    pdf.multi_cell(0, 7, 
        f'This is a friendly reminder that invoice {args.invoice or "N/A"} '
        f'for the amount of ${args.amount or "0.00"} is past due. '
        f'The original due date was {args.due_date or "N/A"}.'
    )
    pdf.ln(5)
    pdf.multi_cell(0, 7, 'Please arrange payment at your earliest convenience. If you have already made this payment, please disregard this notice.')
    pdf.ln(5)
    pdf.cell(0, 7, 'Thank you for your prompt attention to this matter.', new_x='LMARGIN', new_y='NEXT')
    
    output = args.output or f'reminder_{datetime.now().strftime("%Y%m%d")}.pdf'
    pdf.output(output)
    print(f"\n  ✅ Reminder generated: {output}")


def main():
    parser = argparse.ArgumentParser(description='Invoice Generator')
    sub = parser.add_subparsers(dest='command')
    
    # create
    p = sub.add_parser('create', help='Create invoice')
    p.add_argument('--from', dest='from_name', required=True, help='From business name')
    p.add_argument('--from-email', help='From email')
    p.add_argument('--from-address', help='From address')
    p.add_argument('--to', required=True, help='Client name')
    p.add_argument('--to-email', help='Client email')
    p.add_argument('--to-address', help='Client address')
    p.add_argument('--item', action='append', required=True, help='Item: "Desc,Qty,Price"')
    p.add_argument('--tax', help='Tax percentage')
    p.add_argument('--discount', help='Discount percentage')
    p.add_argument('--due', default='30', help='Due in N days')
    p.add_argument('--currency', default='USD', help='Currency code')
    p.add_argument('--notes', help='Notes')
    p.add_argument('--prefix', default='INV', help='Invoice number prefix')
    p.add_argument('--bank', help='Bank details (semicolon separated)')
    p.add_argument('--output', '-o', help='Output filename')
    
    # list
    sub.add_parser('list', help='List invoices')
    
    # remind
    p = sub.add_parser('remind', help='Payment reminder')
    p.add_argument('--to', help='Client name')
    p.add_argument('--invoice', help='Invoice number')
    p.add_argument('--amount', help='Amount due')
    p.add_argument('--due-date', help='Original due date')
    p.add_argument('--output', '-o', help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    {'create': cmd_create, 'list': cmd_list, 'remind': cmd_remind}[args.command](args)


if __name__ == '__main__':
    main()
