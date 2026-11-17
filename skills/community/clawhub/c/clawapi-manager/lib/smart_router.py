#!/usr/bin/env python3
"""
API Cockpit - Smart Router
Routes requests to best available provider based on quota, latency, cost
"""

import os
import sys
import json
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')

os.makedirs(DATA_DIR, exist_ok=True)
ROUTING_FILE = os.path.join(DATA_DIR, 'routing_state.json')

def load_routing():
    """Load routing configuration"""
    if os.path.exists(ROUTING_FILE):
        with open(ROUTING_FILE, 'r') as f:
            return json.load(f)
    return {
        'providers': {},  # {name: {url, cost_per_1k, latency_ms, priority}}
        'weights': {}     # {name: weight}
    }

def save_routing(routing):
    """Save routing configuration"""
    with open(ROUTING_FILE, 'w') as f:
        json.dump(routing, f, indent=2)

def add_provider(name, url, cost_per_1k=0, latency_ms=100, priority=50):
    """Add a provider to the routing pool"""
    routing = load_routing()
    routing['providers'][name] = {
        'url': url,
        'cost_per_1k': cost_per_1k,
        'latency_ms': latency_ms,
        'priority': priority,
        'status': 'active',
        'added_at': datetime.now().isoformat()
    }
    save_routing(routing)
    print(f"Added provider: {name}")

def get_best_provider(criteria='balanced'):
    """Get best provider based on criteria"""
    routing = load_routing()
    providers = routing.get('providers', {})
    
    if not providers:
        return None
    
    # Filter active providers
    active = {k: v for k, v in providers.items() if v.get('status') == 'active'}
    
    if not active:
        return None
    
    # Score providers
    scored = []
    for name, info in active.items():
        if criteria == 'cost':
            score = 100 - info.get('cost_per_1k', 0)
        elif criteria == 'latency':
            score = 100 - info.get('latency_ms', 100)
        elif criteria == 'priority':
            score = info.get('priority', 50)
        else:  # balanced
            cost_score = (100 - info.get('cost_per_1k', 0)) / 3
            latency_score = (100 - info.get('latency_ms', 100)) / 3
            priority_score = info.get('priority', 50) / 3
            score = cost_score + latency_score + priority_score
        
        scored.append((name, info, score))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[2], reverse=True)
    
    return scored[0] if scored else None

def record_failure(provider_name):
    """Record a provider failure, decrease priority"""
    routing = load_routing()
    if provider_name in routing['providers']:
        current = routing['providers'][provider_name].get('priority', 50)
        routing['providers'][provider_name]['priority'] = max(0, current - 10)
        routing['providers'][provider_name]['status'] = 'degraded'
        save_routing(routing)
        print(f"Recorded failure for {provider_name}, new priority: {routing['providers'][provider_name]['priority']}")

def record_success(provider_name):
    """Record a provider success, increase priority"""
    routing = load_routing()
    if provider_name in routing['providers']:
        current = routing['providers'][provider_name].get('priority', 50)
        routing['providers'][provider_name]['priority'] = min(100, current + 5)
        routing['providers'][provider_name]['status'] = 'active'
        save_routing(routing)
        print(f"Recorded success for {provider_name}, new priority: {routing['providers'][provider_name]['priority']}")

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: smart_router.py [add|best|fail|success|list]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 5:
            print("Usage: smart_router.py add <name> <url> <cost_per_1k> <latency_ms>")
            sys.exit(1)
        add_provider(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]))
    elif command == 'best':
        criteria = sys.argv[2] if len(sys.argv) > 2 else 'balanced'
        best = get_best_provider(criteria)
        if best:
            print(json.dumps({'provider': best[0], 'info': best[1], 'score': best[2]}, indent=2))
        else:
            print("No available providers")
    elif command == 'fail':
        if len(sys.argv) < 3:
            print("Usage: smart_router.py fail <provider_name>")
            sys.exit(1)
        record_failure(sys.argv[2])
    elif command == 'success':
        if len(sys.argv) < 3:
            print("Usage: smart_router.py success <provider_name>")
            sys.exit(1)
        record_success(sys.argv[2])
    elif command == 'list':
        print(json.dumps(load_routing(), indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
