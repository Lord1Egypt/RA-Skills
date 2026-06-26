#!/usr/bin/env python3
"""Log an expense."""
import json
import os
import uuid
import argparse
from datetime import datetime

BUDGET_DIR = os.path.expanduser("~/.openclaw/workspace/memory/budget")
EXPENSES_FILE = os.path.join(BUDGET_DIR, "expenses.json")
BUDGET_FILE = os.path.join(BUDGET_DIR, "budget.json")

def ensure_dir():
    os.makedirs(BUDGET_DIR, exist_ok=True)

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    return {"expenses": []}

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            return json.load(f)
    return {"budgets": []}

def save_expenses(data):
    ensure_dir()
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_spent_this_month(category):
    """Calculate spent in category for current month."""
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

def check_budget_alert(category, spent, limit):
    """Check if spending triggers alert."""
    percentage = spent / limit if limit > 0 else 0
    
    if percentage >= 1.0:
        return "🚨 OVER BUDGET", f"{percentage*100:.0f}%"
    elif percentage >= 0.9:
        return "⚠️  WARNING", f"{percentage*100:.0f}%"
    elif percentage >= 0.7:
        return "📊 Heads up", f"{percentage*100:.0f}%"
    else:
        return "✅ On track", f"{percentage*100:.0f}%"

def main():
    parser = argparse.ArgumentParser(description='Log an expense')
    parser.add_argument('--amount', type=float, required=True, help='Expense amount')
    parser.add_argument('--category', required=True, help='Category')
    parser.add_argument('--description', default='', help='Description')
    parser.add_argument('--date', help='Date (YYYY-MM-DD, default: today)')
    parser.add_argument('--merchant', default='', help='Merchant name')
    parser.add_argument('--tags', default='', help='Tags (comma-separated)')
    
    args = parser.parse_args()
    
    # Validate category exists in budget
    budget_data = load_budget()
    budget = None
    for b in budget_data.get('budgets', []):
        if b['category'].lower() == args.category.lower():
            budget = b
            break
    
    expense_date = args.date or datetime.now().strftime('%Y-%m-%d')
    
    # Create expense
    expense = {
        "id": str(uuid.uuid4())[:8],
        "amount": args.amount,
        "category": args.category.lower(),
        "description": args.description,
        "date": expense_date,
        "timestamp": datetime.now().isoformat(),
        "merchant": args.merchant,
        "tags": [t.strip() for t in args.tags.split(',') if t.strip()]
    }
    
    # Save expense
    data = load_expenses()
    data['expenses'].append(expense)
    save_expenses(data)
    
    print(f"\n✓ Expense logged: ${args.amount:.2f}")
    print(f"  Category: {args.category}")
    if args.description:
        print(f"  Description: {args.description}")
    
    # Budget impact
    if budget:
        spent = get_spent_this_month(args.category) + args.amount
        limit = budget['limit']
        remaining = limit - spent
        status, pct = check_budget_alert(args.category, spent, limit)
        
        print(f"\n📊 BUDGET IMPACT")
        print(f"  {args.category.capitalize()} budget: ${limit:.2f}")
        print(f"  Total spent: ${spent:.2f}")
        print(f"  Remaining: ${remaining:.2f}")
        print(f"  Status: {status} ({pct})")
        
        # Calculate days remaining and daily budget
        today = datetime.now()
        if today.month == 12:
            last_day = datetime(today.year + 1, 1, 1)
        else:
            last_day = datetime(today.year, today.month + 1, 1)
        days_remaining = (last_day - today).days
        
        if days_remaining > 0 and remaining > 0:
            daily = remaining / days_remaining
            print(f"  Days left: {days_remaining}")
            print(f"  Daily budget: ${daily:.2f}/day")
    else:
        print(f"\n⚠️  No budget set for {args.category}")
        print(f"   Run: set_budget.py --category {args.category} --limit [amount]")

if __name__ == '__main__':
    main()
