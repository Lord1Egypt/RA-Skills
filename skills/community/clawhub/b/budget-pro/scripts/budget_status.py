#!/usr/bin/env python3
"""Check budget status."""
import json
import os
import argparse
from datetime import datetime

BUDGET_DIR = os.path.expanduser("~/.openclaw/workspace/memory/budget")
BUDGET_FILE = os.path.join(BUDGET_DIR, "budget.json")
EXPENSES_FILE = os.path.join(BUDGET_DIR, "expenses.json")

def load_budget():
    if not os.path.exists(BUDGET_FILE):
        return {"budgets": [], "income": {"total_monthly": 0}}
    with open(BUDGET_FILE, 'r') as f:
        return json.load(f)

def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return {"expenses": []}
    with open(EXPENSES_FILE, 'r') as f:
        return json.load(f)

def get_spent_by_category(category):
    """Get total spent in category for current month."""
    data = load_expenses()
    now = datetime.now()
    total = 0
    
    for exp in data.get('expenses', []):
        exp_date = datetime.fromisoformat(exp['timestamp'])
        if (exp['category'] == category and 
            exp_date.year == now.year and 
            exp_date.month == now.month):
            total += exp['amount']
    
    return total

def main():
    parser = argparse.ArgumentParser(description='Check budget status')
    parser.add_argument('--category', help='Check specific category')
    parser.add_argument('--show-limits', action='store_true', 
                        help='Show all budget limits')
    
    args = parser.parse_args()
    
    budget_data = load_budget()
    
    if args.show_limits:
        print("\nBUDGET LIMITS")
        print("=" * 50)
        total = 0
        for b in budget_data.get('budgets', []):
            print(f"• {b['category']}: ${b['limit']:.2f} {b['period']}")
            total += b['limit']
        print(f"\nTotal budgeted: ${total:.2f}")
        if budget_data['income']['total_monthly'] > 0:
            print(f"Monthly income: ${budget_data['income']['total_monthly']:.2f}")
        return
    
    if args.category:
        # Show specific category
        budget = None
        for b in budget_data.get('budgets', []):
            if b['category'].lower() == args.category.lower():
                budget = b
                break
        
        if not budget:
            print(f"No budget set for {args.category}")
            return
        
        spent = get_spent_by_category(budget['category'])
        limit = budget['limit']
        remaining = limit - spent
        pct = (spent / limit * 100) if limit > 0 else 0
        
        print(f"\n{budget['category'].upper()} BUDGET")
        print("=" * 40)
        print(f"Budget: ${limit:.2f}")
        print(f"Spent:  ${spent:.2f}")
        print(f"Remaining: ${remaining:.2f}")
        print(f"Used: {pct:.0f}%")
        
        # Status indicator
        if pct >= 100:
            print("Status: 🚨 OVER BUDGET")
        elif pct >= 90:
            print("Status: ⚠️  WARNING")
        elif pct >= 70:
            print("Status: 📊 Approaching limit")
        else:
            print("Status: ✅ On track")
        
        return
    
    # Show overall status
    print("\n💰 BUDGET STATUS")
    print("=" * 60)
    print(f"Month: {datetime.now().strftime('%B %Y')}")
    
    if not budget_data.get('budgets'):
        print("\nNo budgets set yet.")
        print("Run: set_budget.py --category [name] --limit [amount]")
        return
    
    total_budget = 0
    total_spent = 0
    
    categories_ok = []
    categories_warning = []
    categories_over = []
    
    for budget in budget_data['budgets']:
        spent = get_spent_by_category(budget['category'])
        limit = budget['limit']
        remaining = limit - spent
        pct = (spent / limit * 100) if limit > 0 else 0
        
        total_budget += limit
        total_spent += spent
        
        cat_info = {
            'name': budget['category'],
            'spent': spent,
            'limit': limit,
            'remaining': remaining,
            'pct': pct
        }
        
        if pct >= 100:
            categories_over.append(cat_info)
        elif pct >= 70:
            categories_warning.append(cat_info)
        else:
            categories_ok.append(cat_info)
    
    # Overall summary
    overall_pct = (total_spent / total_budget * 100) if total_budget > 0 else 0
    print(f"\nOverall: ${total_spent:.2f} / ${total_budget:.2f} ({overall_pct:.0f}%)")
    
    if categories_over:
        print("\n🚨 OVER BUDGET:")
        for c in categories_over:
            print(f"  • {c['name']}: ${c['spent']:.0f}/${c['limit']:.0f} ({c['pct']:.0f}%)")
    
    if categories_warning:
        print("\n⚠️  APPROACHING LIMIT:")
        for c in categories_warning:
            print(f"  • {c['name']}: ${c['spent']:.0f}/${c['limit']:.0f} ({c['pct']:.0f}%)")
    
    if categories_ok:
        print("\n✅ ON TRACK:")
        for c in categories_ok:
            print(f"  • {c['name']}: ${c['spent']:.0f}/${c['limit']:.0f} ({c['pct']:.0f}%)")
    
    # Daily budget remaining
    today = datetime.now()
    if today.month == 12:
        last_day = datetime(today.year + 1, 1, 1)
    else:
        last_day = datetime(today.year, today.month + 1, 1)
    days_remaining = (last_day - today).days
    
    total_remaining = total_budget - total_spent
    if days_remaining > 0:
        daily = total_remaining / days_remaining
        print(f"\n📅 Days remaining: {days_remaining}")
        print(f"💵 Daily budget remaining: ${daily:.2f}/day")

if __name__ == '__main__':
    main()
