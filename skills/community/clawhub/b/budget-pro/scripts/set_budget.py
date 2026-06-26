#!/usr/bin/env python3
"""Set budget for a category."""
import json
import os
import uuid
import argparse
from datetime import datetime

BUDGET_DIR = os.path.expanduser("~/.openclaw/workspace/memory/budget")
BUDGET_FILE = os.path.join(BUDGET_DIR, "budget.json")

def ensure_dir():
    os.makedirs(BUDGET_DIR, exist_ok=True)

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            return json.load(f)
    return {"budgets": [], "income": {"sources": [], "total_monthly": 0}}

def save_budget(data):
    ensure_dir()
    with open(BUDGET_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Set budget')
    parser.add_argument('--category', help='Category name')
    parser.add_argument('--limit', type=float, help='Budget limit')
    parser.add_argument('--period', default='monthly', 
                        choices=['weekly', 'monthly', 'yearly'])
    parser.add_argument('--type', choices=['income', 'expense'], 
                        default='expense')
    parser.add_argument('--amount', type=float, help='Income amount')
    parser.add_argument('--source', default='', help='Income source name')
    parser.add_argument('--frequency', default='monthly',
                        choices=['weekly', 'monthly', 'yearly'])
    parser.add_argument('--update', action='store_true', 
                        help='Update existing budget')
    
    args = parser.parse_args()
    
    data = load_budget()
    
    if args.type == 'income':
        if not args.amount:
            print("Error: --amount required for income")
            return
        
        income = {
            "name": args.source or "Income",
            "amount": args.amount,
            "frequency": args.frequency
        }
        data['income']['sources'].append(income)
        
        # Recalculate total monthly
        monthly_total = 0
        for src in data['income']['sources']:
            amt = src['amount']
            if src['frequency'] == 'weekly':
                amt *= 4.33
            elif src['frequency'] == 'yearly':
                amt /= 12
            monthly_total += amt
        
        data['income']['total_monthly'] = round(monthly_total, 2)
        save_budget(data)
        
        print(f"✓ Income added: {income['name']}")
        print(f"  Amount: ${args.amount:.2f} {args.frequency}")
        print(f"  Total monthly income: ${monthly_total:.2f}")
        return
    
    # Expense budget
    if not args.category or args.limit is None:
        print("Error: --category and --limit required")
        return
    
    existing = None
    for i, b in enumerate(data['budgets']):
        if b['category'].lower() == args.category.lower():
            existing = i
            break
    
    budget = {
        "id": str(uuid.uuid4())[:8] if not existing else data['budgets'][existing]['id'],
        "category": args.category.lower(),
        "limit": args.limit,
        "period": args.period,
        "created_at": datetime.now().isoformat() if not existing else data['budgets'][existing].get('created_at'),
        "updated_at": datetime.now().isoformat()
    }
    
    if existing is not None and args.update:
        data['budgets'][existing] = budget
        action = "Updated"
    elif existing is not None:
        print(f"Budget for {args.category} already exists. Use --update to modify.")
        return
    else:
        data['budgets'].append(budget)
        action = "Set"
    
    save_budget(data)
    
    print(f"✓ Budget {action}: {args.category}")
    print(f"  Limit: ${args.limit:.2f} {args.period}")
    
    # Show total budgeted
    total = sum(b['limit'] for b in data['budgets'])
    print(f"\nTotal budgeted: ${total:.2f}")
    if data['income']['total_monthly'] > 0:
        remaining = data['income']['total_monthly'] - total
        print(f"Monthly income: ${data['income']['total_monthly']:.2f}")
        print(f"Remaining: ${remaining:.2f}")

if __name__ == '__main__':
    main()
