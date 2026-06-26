#!/usr/bin/env python3
"""List expenses with filters."""
import json
import os
import argparse
from datetime import datetime, timedelta

BUDGET_DIR = os.path.expanduser("~/.openclaw/workspace/memory/budget")
EXPENSES_FILE = os.path.join(BUDGET_DIR, "expenses.json")

def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return {"expenses": []}
    with open(EXPENSES_FILE, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='List expenses')
    parser.add_argument('--days', type=int, help='Show last N days')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--today', action='store_true', help='Show today only')
    parser.add_argument('--week', action='store_true', help='Show this week')
    parser.add_argument('--month', help='Show specific month (YYYY-MM)')
    parser.add_argument('--limit', type=int, default=20, help='Limit results')
    
    args = parser.parse_args()
    
    data = load_expenses()
    expenses = data.get('expenses', [])
    
    if not expenses:
        print("No expenses logged yet.")
        return
    
    now = datetime.now()
    
    # Filter by date
    if args.today:
        expenses = [e for e in expenses 
                   if datetime.fromisoformat(e['timestamp']).date() == now.date()]
    elif args.days:
        cutoff = now - timedelta(days=args.days)
        expenses = [e for e in expenses 
                   if datetime.fromisoformat(e['timestamp']) >= cutoff]
    elif args.week:
        cutoff = now - timedelta(days=7)
        expenses = [e for e in expenses 
                   if datetime.fromisoformat(e['timestamp']) >= cutoff]
    elif args.month:
        year, month = map(int, args.month.split('-'))
        expenses = [e for e in expenses 
                   if datetime.fromisoformat(e['timestamp']).year == year and
                      datetime.fromisoformat(e['timestamp']).month == month]
    
    # Filter by category
    if args.category:
        expenses = [e for e in expenses 
                   if e['category'].lower() == args.category.lower()]
    
    # Sort by date (newest first)
    expenses.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Limit results
    expenses = expenses[:args.limit]
    
    if not expenses:
        print("No expenses match the criteria.")
        return
    
    print(f"\nEXPENSES ({len(expenses)} shown)")
    print("=" * 60)
    
    total = 0
    for exp in expenses:
        date_str = datetime.fromisoformat(exp['timestamp']).strftime('%m/%d')
        total += exp['amount']
        
        desc = exp.get('description', '')
        if len(desc) > 25:
            desc = desc[:22] + '...'
        
        print(f"{date_str}  ${exp['amount']:>7.2f}  {exp['category']:<12}  {desc}")
    
    print("-" * 60)
    print(f"Total: ${total:.2f}")
    
    # Show category breakdown if multiple categories
    if len(set(e['category'] for e in expenses)) > 1:
        print("\nBy Category:")
        by_cat = {}
        for e in expenses:
            cat = e['category']
            by_cat[cat] = by_cat.get(cat, 0) + e['amount']
        
        for cat, amount in sorted(by_cat.items(), key=lambda x: -x[1]):
            print(f"  {cat}: ${amount:.2f}")

if __name__ == '__main__':
    main()
