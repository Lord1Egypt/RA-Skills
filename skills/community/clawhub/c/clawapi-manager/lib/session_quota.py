#!/usr/bin/env python3
"""
API Cockpit - Session Quota Manager
Tracks and limits sessions per model/provider
"""

import os
import sys
import json
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')

os.makedirs(DATA_DIR, exist_ok=True)
QUOTA_FILE = os.path.join(DATA_DIR, 'session_quota.json')

def load_quota():
    """Load quota data"""
    if os.path.exists(QUOTA_FILE):
        with open(QUOTA_FILE, 'r') as f:
            return json.load(f)
    return {
        'limits': {},  # {model: max_sessions_per_day}
        'usage': {},   # {date: {model: count}}
    }

def save_quota(quota):
    """Save quota data"""
    with open(QUOTA_FILE, 'w') as f:
        json.dump(quota, f, indent=2)

def set_limit(model, max_sessions):
    """Set session limit for a model"""
    quota = load_quota()
    quota['limits'][model] = max_sessions
    save_quota(quota)
    print(f"Set limit: {model} -> {max_sessions} sessions/day")

def record_session(model):
    """Record a session"""
    quota = load_quota()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if today not in quota['usage']:
        quota['usage'][today] = {}
    
    if model not in quota['usage'][today]:
        quota['usage'][today][model] = 0
    
    quota['usage'][today][model] += 1
    save_quota(quota)
    print(f"Recorded session for {model}")

def check_quota(model):
    """Check if model has quota available"""
    quota = load_quota()
    today = datetime.now().strftime('%Y-%m-%d')
    
    limit = quota['limits'].get(model, -1)  # -1 = unlimited
    used = quota['usage'].get(today, {}).get(model, 0)
    
    if limit == -1:
        return {'available': True, 'limit': 'unlimited', 'used': used}
    
    available = limit - used
    return {
        'available': available > 0,
        'limit': limit,
        'used': used,
        'remaining': available
    }

def get_all_usage():
    """Get usage for all models today"""
    quota = load_quota()
    today = datetime.now().strftime('%Y-%m-%d')
    return quota['usage'].get(today, {})

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: session_quota.py [set|record|check|usage]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'set':
        if len(sys.argv) < 4:
            print("Usage: session_quota.py set <model> <max_sessions>")
            sys.exit(1)
        set_limit(sys.argv[2], int(sys.argv[3]))
    elif command == 'record':
        if len(sys.argv) < 3:
            print("Usage: session_quota.py record <model>")
            sys.exit(1)
        record_session(sys.argv[2])
    elif command == 'check':
        if len(sys.argv) < 3:
            print("Usage: session_quota.py check <model>")
            sys.exit(1)
        print(json.dumps(check_quota(sys.argv[2]), indent=2))
    elif command == 'usage':
        print(json.dumps(get_all_usage(), indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
