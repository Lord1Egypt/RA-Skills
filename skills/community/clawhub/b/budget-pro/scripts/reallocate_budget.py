#!/usr/bin/env python3
"""Reallocate budget between categories."""
import json
import os
import uuid
import argparse
from datetime import datetime

BUDGET_DIR = os.path.expanduser("~/.openclaw/workspace/memory/budget")
BUDGET_FILE = os.path.join(BUDGET_DIR, "budget.json")
EXPENSES_FILE = os.path.join(BUDGET_DIR, "expenses.json")

def load_budget():
    if not os.path.exists(BUDGET_FILE):
        return {"budgets": [], "reallocations": []}
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

def save_budget(data):
    os.makedirs(BUDGET_DIR, exist_ok=True)
    with open(BUDGET_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Reallocate budget')
    parser.add_argument('--from-cat', help='Category to take from')
    parser.add_argument('--to-cat', help='Category to add to')
    parser.add_argument('--amount', type=float, help='Amount to move')
    parser.add_argument('--check-available', action='store_true',
                        help='Show available funds for reallocation')
    parser.add_argument('--preview', action='store_true',
                        help='Preview without executing')
    parser.add_argument('--confirm', action='store_true',
                        help='Confirm reallocation')
    
    args = parser.parse_args()
    
    data = load_budget()
    
    if args.check_available:
        print("\nAVAILABLE FOR REALLOCATION")
        print("=" * 50)
        
        for budget in data.get('budgets', []):
            spent = get_spent_by_category(budget['category'])
            limit = budget['limit']
            remaining = limit - spent
            pct = (spent / limit * 100) if limit > 0 else 0
            
            if remaining > 20:  # Only show categories with meaningful surplus
                safe_to_move = remaining - (limit * 0.1)  # Keep 10% buffer
                if safe_to_move > 10:
                    print(f"\n{budget['category']}:")
                    print(f"  Budget: ${limit:.2f}")
                    print(f"  Spent:  ${spent:.2f}")
                    print(f"  Remaining: ${remaining:.2f} ({100-pct:.0f}%)")
                    print(f"  Safe to reallocate: ~${safe_to_move:.0f}")
        
        return
    
    if not args.from_cat or not args.to_cat or not args.amount:
        print("Error: --from-cat, --to-cat, and --amount required")
        print("Use --check-available to see available funds")
        return
    
    # Find categories
    from_budget = None
    to_budget = None
    
    for b in data.get('budgets', []):
        if b['category'].lower() == args.from_cat.lower():
            from_budget = b
        if b['category'].lower() == args.to_cat.lower():
            to_budget = b
    
    if not from_budget:
        print(f"Error: Category '{args.from_cat}' not found")
        return
    
    if not to_budget:
        print(f"Error: Category '{args.to_cat}' not found")
        return
    
    # Check available
    from_spent = get_spent_by_category(from_budget['category'])
    from_remaining = from_budget['limit'] - from_spent
    
    if args.amount > from_remaining:
        print(f"\n⚠️  Cannot reallocate ${args.amount:.2f}")
        print(f"   {args.from_cat} only has ${from_remaining:.2f} remaining")
        print(f"   Maximum safe reallocation: ${max(0, from_remaining - 20):.2f}")
        return
    
    # Preview
    print(f"\nREALLOCATION PREVIEW")
    print("=" * 50)
    print(f"Move ${args.amount:.2f} from {args.from_cat} to {args.to_cat}")
    print()
    print(f"{args.from_cat}:")
    print(f"  Current budget: ${from_budget['limit']:.2f}")
    print(f"  New budget: ${from_budget['limit'] - args.amount:.2f}")
    print(f"  Currently spent: ${from_spent:.2f}")
    print(f"  New remaining: ${from_remaining - args.amount:.2f}")
    print()
    print(f"{args.to_cat}:")
    print(f"  Current budget: ${to_budget['limit']:.2f}")
    print(f"  New budget: ${to_budget['limit'] + args.amount:.2f}")
    
    if args.preview:
        return
    
    if not args.confirm:
        print("\nAdd --confirm to execute this reallocation")
        return
    
    # Execute
    from_budget['limit'] -= args.amount
    from_budget['updated_at'] = datetime.now().isoformat()
    to_budget['limit'] += args.amount
    to_budget['updated_at'] = datetime.now().isoformat()
    
    # Log reallocation
    reallocation = {
        "id": str(uuid.uuid4())[:8],
        "from_category": args.from_cat,
        "to_category": args.to_cat,
        "amount": args.amount,
        "date": datetime.now().isoformat()
    }
    
    if 'reallocations' not in data:
        data['reallocations'] = []
    data['reallocations'].append(reallocation)
    
    save_budget(data)
    
    print(f"\n✓ Reallocation complete!")
    print(f"  Moved ${args.amount:.2f} from {args.from_cat} to {args.to_cat}")

if __name__ == '__main__':
    main()
