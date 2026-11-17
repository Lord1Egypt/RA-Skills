#!/usr/bin/env python3
"""
API Cockpit - Cost Predictor
Predicts monthly cost based on historical data
"""

import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')

os.makedirs(DATA_DIR, exist_ok=True)
COST_FILE = os.path.join(DATA_DIR, 'costs.json')

def load_costs():
    """Load cost data from file"""
    if os.path.exists(COST_FILE):
        with open(COST_FILE, 'r') as f:
            return json.load(f)
    return {
        'daily': defaultdict(dict),
        'monthly': defaultdict(dict),
        'total': {},
        'by_model': {
            'daily': defaultdict(dict),
            'monthly': defaultdict(dict)
        }
    }

def predict_monthly_cost():
    """Predict monthly cost based on current daily average"""
    costs = load_costs()
    today = datetime.now()
    current_month = today.strftime('%Y-%m')
    days_passed = today.day
    days_in_month = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).day if today.month < 12 else 31
    
    # Get current month's cost so far
    monthly_cost = 0.0
    if current_month in costs['monthly']:
        monthly_cost = sum(costs['monthly'][current_month].values())
    
    # Predict total
    if days_passed > 0:
        daily_avg = monthly_cost / days_passed
        predicted_total = daily_avg * days_in_month
    else:
        daily_avg = 0
        predicted_total = monthly_cost
    
    return {
        'current_month': current_month,
        'days_passed': days_passed,
        'days_in_month': days_in_month,
        'cost_so_far': monthly_cost,
        'daily_average': daily_avg,
        'predicted_total': predicted_total,
        'predicted_remaining': predicted_total - monthly_cost
    }

def get_cost_trend(days=7):
    """Get cost trend for last N days"""
    costs = load_costs()
    trend = []
    
    for i in range(days-1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        day_cost = sum(costs['daily'].get(date, {}).values())
        trend.append({
            'date': date,
            'cost': day_cost
        })
    
    return trend

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: cost_predictor.py [predict|trend]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'predict':
        print(json.dumps(predict_monthly_cost(), indent=2))
    elif command == 'trend':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(json.dumps(get_cost_trend(days), indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
