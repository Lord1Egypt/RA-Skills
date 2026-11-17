#!/usr/bin/env python3
"""
Cost Monitor - Tracks API usage costs across providers and models
Generates daily/monthly reports and charts with model-level grouping
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
LOG_DIR = os.path.join(PARENT_DIR, 'logs')
DATA_DIR = os.path.join(PARENT_DIR, 'data')

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Cost data file
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

def save_costs(costs):
    """Save cost data to file"""
    with open(COST_FILE, 'w') as f:
        json.dump(costs, f, indent=2)

def record_usage(provider, model, cost):
    """Record a cost entry with model-level tracking"""
    costs = load_costs()
    
    today = datetime.now().strftime('%Y-%m-%d')
    month = datetime.now().strftime('%Y-%m')
    
    # Provider-level cost
    if provider not in costs['daily'][today]:
        costs['daily'][today][provider] = 0.0
    costs['daily'][today][provider] += cost
    
    if provider not in costs['monthly'][month]:
        costs['monthly'][month][provider] = 0.0
    costs['monthly'][month][provider] += cost
    
    if provider not in costs['total']:
        costs['total'][provider] = 0.0
    costs['total'][provider] += cost
    
    # Model-level cost
    model_key = f"{provider}:{model}"
    
    if model_key not in costs['by_model']['daily'][today]:
        costs['by_model']['daily'][today][model_key] = 0.0
    costs['by_model']['daily'][today][model_key] += cost
    
    if model_key not in costs['by_model']['monthly'][month]:
        costs['by_model']['monthly'][month][model_key] = 0.0
    costs['by_model']['monthly'][month][model_key] += cost
    
    save_costs(costs)

def get_daily_report(date=None):
    """Get daily cost report"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    costs = load_costs()
    daily_costs = costs['daily'].get(date, {})
    daily_by_model = costs['by_model']['daily'].get(date, {})
    
    total = sum(daily_costs.values())
    
    return {
        'date': date,
        'breakdown': daily_costs,
        'by_model': daily_by_model,
        'total': total
    }

def get_monthly_report(month=None):
    """Get monthly cost report"""
    if month is None:
        month = datetime.now().strftime('%Y-%m')
    
    costs = load_costs()
    monthly_costs = costs['monthly'].get(month, {})
    monthly_by_model = costs['by_model']['monthly'].get(month, {})
    
    total = sum(monthly_costs.values())
    
    return {
        'month': month,
        'breakdown': monthly_costs,
        'by_model': monthly_by_model,
        'total': total
    }

def get_chart_data(days=30):
    """Get data for chart generation"""
    costs = load_costs()
    
    dates = []
    data = defaultdict(list)
    model_data = defaultdict(list)
    
    # Get last N days
    for i in range(days-1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dates.append(date)
        
        day_costs = costs['daily'].get(date, {})
        day_by_model = costs['by_model']['daily'].get(date, {})
        
        for provider in ['antigravity', 'codex', 'copilot', 'windsurf']:
            data[provider].append(day_costs.get(provider, 0.0))
        
        # Group by model
        for model_key, cost in day_by_model.items():
            model_data[model_key].append(cost)
    
    return {
        'dates': dates,
        'series': data,
        'by_model': model_data
    }

def generate_text_report():
    """Generate a text report for Telegram"""
    daily = get_daily_report()
    monthly = get_monthly_report()
    
    report = f"📊 *Cost Report*\n\n"
    report += f"*Today ({daily['date']}):* ${daily['total']:.2f}\n"
    
    # Provider breakdown
    for provider, cost in daily['breakdown'].items():
        if cost > 0:
            report += f"  • {provider}: ${cost:.2f}\n"
    
    # Model breakdown
    report += f"\n*By Model (Today):*\n"
    for model_key, cost in daily['by_model'].items():
        if cost > 0:
            report += f"  • {model_key}: ${cost:.2f}\n"
    
    report += f"\n*This Month ({monthly['month']}):* ${monthly['total']:.2f}\n"
    for provider, cost in monthly['breakdown'].items():
        if cost > 0:
            report += f"  • {provider}: ${cost:.2f}\n"
    
    return report

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: cost_monitor.py [report|daily|monthly|chart|record]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'report':
        print(generate_text_report())
    elif command == 'daily':
        print(json.dumps(get_daily_report(), indent=2))
    elif command == 'monthly':
        print(json.dumps(get_monthly_report(), indent=2))
    elif command == 'chart':
        print(json.dumps(get_chart_data(), indent=2))
    elif command == 'record':
        if len(sys.argv) < 5:
            print("Usage: cost_monitor.py record <provider> <model> <cost>")
            sys.exit(1)
        provider = sys.argv[2]
        model = sys.argv[3]
        cost = float(sys.argv[4])
        record_usage(provider, model, cost)
        print(f"Recorded ${cost:.2f} for {provider}:{model}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
