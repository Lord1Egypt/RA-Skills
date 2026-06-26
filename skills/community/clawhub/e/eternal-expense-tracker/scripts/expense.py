#!/usr/bin/env python3
"""
Expense Tracker — Personal finance tracking with receipt scanning.
Store: ~/.expense-tracker/
"""

import sys
import os
import json
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / '.expense-tracker'
TX_FILE = DATA_DIR / 'transactions.json'
BUDGET_FILE = DATA_DIR / 'budgets.json'
CAT_FILE = DATA_DIR / 'categories.json'

DEFAULT_CATEGORIES = {
    'food': ['grocery', 'restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'food', 'meal', 'dinner', 'lunch', 'breakfast', 'snack', 'uber eats', 'doordash', 'grubhub'],
    'transport': ['uber', 'lyft', 'gas', 'fuel', 'parking', 'toll', 'bus', 'metro', 'train', 'taxi', 'ride'],
    'shopping': ['amazon', 'walmart', 'target', 'clothing', 'shoes', 'electronics', 'bestbuy', 'mall'],
    'bills': ['electric', 'water', 'internet', 'phone', 'rent', 'mortgage', 'insurance', 'utility', 'subscription', 'netflix', 'spotify'],
    'health': ['pharmacy', 'doctor', 'hospital', 'gym', 'medicine', 'dental', 'vitamin'],
    'entertainment': ['movie', 'game', 'concert', 'bar', 'club', 'streaming', 'hobby'],
    'education': ['book', 'course', 'tuition', 'school', 'udemy', 'skillshare'],
    'travel': ['hotel', 'flight', 'airbnb', 'booking', 'trip', 'vacation'],
    'other': []
}

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path, default=None):
    if default is None:
        default = []
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def get_categories():
    if CAT_FILE.exists():
        return load_json(CAT_FILE, DEFAULT_CATEGORIES)
    save_json(CAT_FILE, DEFAULT_CATEGORIES)
    return DEFAULT_CATEGORIES

def auto_categorize(description, categories):
    """Auto-categorize based on keyword matching."""
    desc_lower = description.lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in desc_lower:
                return cat
    return 'other'

def cmd_add(args):
    """Add a transaction."""
    ensure_data_dir()
    transactions = load_json(TX_FILE)
    categories = get_categories()
    
    cat = args.category or auto_categorize(args.desc or '', categories)
    
    tx = {
        'id': len(transactions) + 1,
        'date': args.date or datetime.now().strftime('%Y-%m-%d'),
        'amount': float(args.amount),
        'category': cat,
        'description': args.desc or '',
        'merchant': args.merchant or '',
        'type': args.type or 'expense',
        'created_at': datetime.now().isoformat()
    }
    
    transactions.append(tx)
    save_json(TX_FILE, transactions)
    
    emoji = '🔴' if tx['type'] == 'expense' else '🟢'
    print(f"\n  {emoji} Transaction added:")
    print(f"     Date:   {tx['date']}")
    print(f"     Amount: ${tx['amount']:.2f}")
    print(f"     Cat:    {tx['category']}")
    print(f"     Desc:   {tx['description']}")
    print(f"     ID:     #{tx['id']}")

def cmd_scan(args):
    """OCR a receipt image and extract items."""
    ensure_data_dir()
    
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print("  ❌ Install required: pip install pytesseract pillow")
        print("     Also install tesseract: apt install tesseract-ocr")
        return
    
    img = Image.open(args.file)
    text = pytesseract.image_to_string(img)
    
    print(f"\n  📄 Raw OCR text from {args.file}:")
    print(f"  {'─'*40}")
    print(f"  {text[:500]}")
    print(f"  {'─'*40}")
    
    # Extract amounts (find lines with $ or numbers that look like prices)
    import re
    lines = text.split('\n')
    items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Match patterns like "Item name    12.99" or "Item $12.99"
        price_match = re.search(r'\$?\s*(\d+\.\d{2})\s*$', line)
        if price_match:
            price = float(price_match.group(1))
            name = line[:price_match.start()].strip().rstrip(' .')
            if name and price > 0:
                items.append({'name': name, 'price': price})
    
    # Find total
    total = 0
    for line in lines:
        if 'total' in line.lower():
            m = re.search(r'\$?\s*(\d+\.\d{2})', line)
            if m:
                total = float(m.group(1))
    
    if items:
        print(f"\n  🧾 Extracted {len(items)} items:")
        categories = get_categories()
        transactions = load_json(TX_FILE)
        
        for item in items:
            cat = auto_categorize(item['name'], categories)
            print(f"     • {item['name']:30s}  ${item['price']:>8.2f}  [{cat}]")
            
            tx = {
                'id': len(transactions) + 1,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'amount': item['price'],
                'category': cat,
                'description': item['name'],
                'merchant': args.file,
                'type': 'expense',
                'created_at': datetime.now().isoformat()
            }
            transactions.append(tx)
        
        save_json(TX_FILE, transactions)
        
        if total:
            print(f"\n  📊 Receipt total: ${total:.2f}")
            print(f"  📊 Extracted sum: ${sum(i['price'] for i in items):.2f}")
        
        print(f"\n  ✅ {len(items)} items saved to tracker")
    else:
        print("\n  ⚠️  No items extracted. Try a clearer image.")

def cmd_import(args):
    """Import CSV bank statement."""
    ensure_data_dir()
    transactions = load_json(TX_FILE)
    categories = get_categories()
    
    imported = 0
    with open(args.file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get(args.desc_col, row.get('Description', ''))
            amount = abs(float(row.get(args.amount_col, row.get('Amount', 0))))
            date = row.get(args.date_col, row.get('Date', ''))
            
            cat = auto_categorize(desc, categories)
            
            tx = {
                'id': len(transactions) + 1,
                'date': date,
                'amount': amount,
                'category': cat,
                'description': desc,
                'merchant': '',
                'type': 'expense',
                'created_at': datetime.now().isoformat()
            }
            transactions.append(tx)
            imported += 1
    
    save_json(TX_FILE, transactions)
    print(f"\n  ✅ Imported {imported} transactions from {args.file}")

def cmd_report(args):
    """Generate spending report."""
    transactions = load_json(TX_FILE)
    if not transactions:
        print("\n  📭 No transactions yet. Add some with: expense.py add")
        return
    
    now = datetime.now()
    
    # Filter by period
    if args.period == 'week':
        start = (now - timedelta(days=7)).strftime('%Y-%m-%d')
    elif args.period == 'month':
        start = now.strftime('%Y-%m-01')
    elif args.period == 'year':
        start = now.strftime('%Y-01-01')
    else:
        start = '1970-01-01'
    
    filtered = [t for t in transactions if t['date'] >= start]
    
    if args.category:
        filtered = [t for t in filtered if t['category'] == args.category]
    
    if not filtered:
        print(f"\n  📭 No transactions for {args.period or 'all time'}.")
        return
    
    # Category breakdown
    cat_totals = {}
    total = 0
    for t in filtered:
        if t['type'] == 'expense':
            cat_totals[t['category']] = cat_totals.get(t['category'], 0) + t['amount']
            total += t['amount']
    
    # Sort by amount
    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
    
    max_val = max(cat_totals.values()) if cat_totals else 1
    
    print(f"\n{'═'*55}")
    print(f"  📊 EXPENSE REPORT — {args.period or 'all time'.upper()}")
    print(f"  Period: {start} to {now.strftime('%Y-%m-%d')}")
    print(f"{'═'*55}")
    print(f"")
    print(f"  💰 Total Spent: ${total:,.2f}")
    print(f"  📋 Transactions: {len(filtered)}")
    print(f"")
    print(f"  ── By Category ──")
    
    for cat, amount in sorted_cats:
        pct = (amount / total * 100) if total > 0 else 0
        bar_len = int((amount / max_val) * 25) if max_val > 0 else 0
        bar = '█' * bar_len + '░' * (25 - bar_len)
        print(f"  {cat:15s}  ${amount:>9,.2f}  {bar}  {pct:.0f}%")
    
    # Top merchants
    merchant_totals = {}
    for t in filtered:
        if t.get('merchant'):
            merchant_totals[t['merchant']] = merchant_totals.get(t['merchant'], 0) + t['amount']
    
    if merchant_totals:
        sorted_merchants = sorted(merchant_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\n  ── Top Merchants ──")
        for merchant, amount in sorted_merchants:
            print(f"  {merchant:20s}  ${amount:>9,.2f}")
    
    # Budget check
    if args.budget:
        budgets = load_json(BUDGET_FILE)
        if budgets:
            print(f"\n  ── Budget Status ──")
            for cat, limit in budgets.items():
                spent = cat_totals.get(cat, 0)
                pct = (spent / limit * 100) if limit > 0 else 0
                status = '🟢' if pct < 75 else '🟡' if pct < 100 else '🔴'
                print(f"  {status} {cat:15s}  ${spent:>7,.2f} / ${limit:>7,.2f}  ({pct:.0f}%)")
    
    print(f"{'═'*55}")

def cmd_budget(args):
    """Set or view budgets."""
    ensure_data_dir()
    budgets = load_json(BUDGET_FILE)
    
    if args.set_category and args.set_amount:
        budgets[args.set_category] = float(args.set_amount)
        save_json(BUDGET_FILE, budgets)
        print(f"\n  ✅ Budget set: {args.set_category} = ${float(args.set_amount):,.2f}/month")
    else:
        if not budgets:
            print("\n  📭 No budgets set. Use --set-category food --set-amount 500")
            return
        print(f"\n  📊 Monthly Budgets:")
        for cat, limit in budgets.items():
            print(f"  {cat:15s}  ${limit:>9,.2f}")

def cmd_categories(args):
    """List categories."""
    categories = get_categories()
    print(f"\n  📂 Categories:")
    for cat, keywords in categories.items():
        print(f"  • {cat:15s}  (keywords: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''})")

def cmd_export(args):
    """Export transactions as CSV."""
    transactions = load_json(TX_FILE)
    if not transactions:
        print("  No data to export.")
        return
    
    outfile = args.output or 'expenses_export.csv'
    with open(outfile, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'date', 'amount', 'category', 'description', 'merchant', 'type'])
        writer.writeheader()
        writer.writerows(transactions)
    
    print(f"\n  ✅ Exported {len(transactions)} transactions to {outfile}")

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker')
    sub = parser.add_subparsers(dest='command')
    
    # add
    p_add = sub.add_parser('add', help='Add transaction')
    p_add.add_argument('--amount', required=True, help='Amount')
    p_add.add_argument('--category', help='Category (auto-detected if omitted)')
    p_add.add_argument('--desc', help='Description')
    p_add.add_argument('--date', help='Date (YYYY-MM-DD)')
    p_add.add_argument('--merchant', help='Merchant name')
    p_add.add_argument('--type', choices=['expense', 'income'], default='expense')
    
    # scan
    p_scan = sub.add_parser('scan', help='Scan receipt image')
    p_scan.add_argument('file', help='Image file path')
    
    # import
    p_imp = sub.add_parser('import', help='Import CSV')
    p_imp.add_argument('file', help='CSV file')
    p_imp.add_argument('--date-col', default='Date')
    p_imp.add_argument('--amount-col', default='Amount')
    p_imp.add_argument('--desc-col', default='Description')
    
    # report
    p_rep = sub.add_parser('report', help='Generate report')
    p_rep.add_argument('--period', choices=['week', 'month', 'year'])
    p_rep.add_argument('--category', help='Filter by category')
    p_rep.add_argument('--budget', action='store_true', help='Show budget status')
    
    # budget
    p_bud = sub.add_parser('budget', help='Set/view budgets')
    p_bud.add_argument('--set-category', help='Category to set budget for')
    p_bud.add_argument('--set-amount', help='Budget amount')
    
    # categories
    sub.add_parser('categories', help='List categories')
    
    # export
    p_exp = sub.add_parser('export', help='Export to CSV')
    p_exp.add_argument('--output', '-o', help='Output file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    {
        'add': cmd_add,
        'scan': cmd_scan,
        'import': cmd_import,
        'report': cmd_report,
        'budget': cmd_budget,
        'categories': cmd_categories,
        'export': cmd_export,
    }[args.command](args)

if __name__ == '__main__':
    main()
