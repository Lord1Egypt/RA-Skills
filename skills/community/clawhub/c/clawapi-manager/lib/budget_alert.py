#!/usr/bin/env python3
"""
API Cockpit - Budget Alert
Monitors spending and alerts when thresholds are exceeded
"""

import os
import sys
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')
BUDGET_FILE = os.path.join(DATA_DIR, 'budget.json')

def load_budget():
    """Load budget config"""
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            return json.load(f)
    return {
        "monthly_limit": 100.0,
        "daily_limit": 10.0,
        "warn_at_percent": 80,
        "alert_channels": ["telegram"]
    }

def save_budget(budget):
    """Save budget config"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(BUDGET_FILE, 'w') as f:
        json.dump(budget, f, indent=2)

def check_budget(current_spend):
    """Check if budget threshold exceeded"""
    budget = load_budget()
    
    daily_limit = budget.get('daily_limit', 10.0)
    monthly_limit = budget.get('monthly_limit', 100.0)
    warn_percent = budget.get('warn_at_percent', 80)
    
    alerts = []
    
    # Daily check
    if current_spend.get('daily', 0) >= daily_limit:
        alerts.append(f"🚨 Daily budget exceeded: ${current_spend.get('daily', 0):.2f} >= ${daily_limit}")
    elif current_spend.get('daily', 0) >= daily_limit * warn_percent / 100:
        alerts.append(f"⚠️ Daily budget warning: ${current_spend.get('daily', 0):.2f} ({warn_percent}% of ${daily_limit})")
    
    # Monthly check
    if current_spend.get('monthly', 0) >= monthly_limit:
        alerts.append(f"🚨 Monthly budget exceeded: ${current_spend.get('monthly', 0):.2f} >= ${monthly_limit}")
    elif current_spend.get('monthly', 0) >= monthly_limit * warn_percent / 100:
        alerts.append(f"⚠️ Monthly budget warning: ${current_spend.get('monthly', 0):.2f} ({warn_percent}% of ${monthly_limit})")
    
    return {
        "status": "ok" if not alerts else "warning" if "warning" in alerts[0] else "exceeded",
        "alerts": alerts,
        "budget": budget
    }

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        # Show current budget
        budget = load_budget()
        print(json.dumps(budget, indent=2))
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'set':
        if len(sys.argv) < 4:
            print("Usage: budget_alert.py set <monthly_limit> <daily_limit>")
            sys.exit(1)
        budget = load_budget()
        budget['monthly_limit'] = float(sys.argv[2])
        budget['daily_limit'] = float(sys.argv[3])
        save_budget(budget)
        print("Budget updated")
    elif command == 'check':
        # For testing, accept JSON spend data
        spend = json.loads(' '.join(sys.argv[2:])) if len(sys.argv) > 2 else {"daily": 0, "monthly": 0}
        result = check_budget(spend)
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
