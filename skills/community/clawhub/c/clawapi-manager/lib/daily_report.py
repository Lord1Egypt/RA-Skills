#!/usr/bin/env python3
"""
API Cockpit - Daily Report Generator
Parses session logs and generates cost reports
"""

import os
import sys
import json
import glob
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')

# Model pricing (per 1M tokens)
MODEL_PRICING = {
    "claude-opus-4-6": {"input": 15.0, "output": 75.0},   # $15/$75
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-opus-4-5": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0},
    "gpt-4o": {"input": 5.0, "output": 15.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "mini-max": {"input": 0.1, "output": 0.1},
    "yi-light": {"input": 0.6, "output": 2.0},
    "default": {"input": 1.0, "output": 3.0}
}

def get_pricing(model):
    """Get pricing for a model"""
    model_lower = model.lower() if model else ""
    for key, price in MODEL_PRICING.items():
        if key in model_lower:
            return price
    return MODEL_PRICING["default"]

def parse_session_file(filepath):
    """Parse a session file and extract usage"""
    usage_data = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    # Look for usage in various fields
                    if 'usage' in entry and entry['usage']:
                        usage_data.append({
                            'timestamp': entry.get('timestamp', ''),
                            'usage': entry['usage'],
                            'model': entry.get('model', 'unknown'),
                            'provider': entry.get('provider', 'unknown')
                        })
                    # Also check for cost field
                    if 'cost' in entry and entry['cost']:
                        usage_data.append({
                            'timestamp': entry.get('timestamp', ''),
                            'cost': entry['cost'],
                            'model': entry.get('model', 'unknown'),
                            'provider': entry.get('provider', 'unknown')
                        })
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return usage_data

def calculate_cost(usage):
    """Calculate cost from usage data"""
    if 'cost' in usage:
        return usage['cost']
    
    input_tokens = usage.get('input_tokens', 0)
    output_tokens = usage.get('output_tokens', 0)
    
    model = usage.get('model', 'unknown')
    pricing = get_pricing(model)
    
    input_cost = (input_tokens / 1_000_000) * pricing['input']
    output_cost = (output_tokens / 1_000_000) * pricing['output']
    
    return input_cost + output_cost

def generate_report(date=None, sessions_dir=None):
    """Generate daily cost report"""
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    if sessions_dir is None:
        sessions_dir = os.path.expanduser("~/.openclaw/agents/main/sessions")
    
    print(f"Generating report for {date}...")
    
    # Find session files
    session_files = glob.glob(os.path.join(sessions_dir, "*.jsonl"))
    
    total_cost = 0
    by_model = defaultdict(float)
    by_provider = defaultdict(float)
    session_count = 0
    
    for filepath in session_files:
        # Check if file was modified on the target date
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        if mtime.strftime('%Y-%m-%d') != date:
            continue
        
        usage_data = parse_session_file(filepath)
        for usage in usage_data:
            cost = calculate_cost(usage)
            total_cost += cost
            
            model = usage.get('model', 'unknown')
            provider = usage.get('provider', 'unknown')
            
            by_model[model] += cost
            by_provider[provider] += cost
            session_count += 1
    
    report = {
        "date": date,
        "total_cost": round(total_cost, 4),
        "session_count": session_count,
        "by_model": dict(by_model),
        "by_provider": dict(by_provider),
        "generated_at": datetime.now().isoformat()
    }
    
    return report

def format_report(report):
    """Format report as message"""
    lines = [
        f"📊 *Daily Cost Report - {report['date']}*",
        "",
        f"💰 *Total: ${report['total_cost']:.4f}*",
        f"📝 Sessions: {report['session_count']}",
        ""
    ]
    
    if report['by_model']:
        lines.append("*By Model:*")
        for model, cost in sorted(report['by_model'].items(), key=lambda x: -x[1]):
            lines.append(f"  • {model}: ${cost:.4f}")
        lines.append("")
    
    if report['by_provider']:
        lines.append("*By Provider:*")
        for provider, cost in sorted(report['by_provider'].items(), key=lambda x: -x[1]):
            lines.append(f"  • {provider}: ${cost:.4f}")
    
    return "\n".join(lines)

def main():
    """CLI entry point"""
    date = None
    if len(sys.argv) > 1:
        date = sys.argv[1]
    
    report = generate_report(date)
    print(json.dumps(report, indent=2))
    print()
    print(format_report(report))

if __name__ == '__main__':
    main()
