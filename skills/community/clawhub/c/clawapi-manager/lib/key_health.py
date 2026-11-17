#!/usr/bin/env python3
"""
API Cockpit - Key Failure Detector
Detects API key failures from logs (401, 403, rate limit, etc.)
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')
FAILURE_FILE = os.path.join(DATA_DIR, 'key_failures.json')

# Error patterns to detect
ERROR_PATTERNS = {
    "401": r"(401|Unauthorized|invalid.*api.?key|invalid.*token)",
    "403": r"(403|Forbidden|permission.*denied|access.*denied)",
    "429": r"(429|rate.?limit|too.?many.?requests|quota.?exceeded)",
    "timeout": r"(timeout|timed.?out|connection.?timeout)",
    "500": r"(500|internal.?error|server.?error)",
    "503": r"(503|service.?unavailable)",
}

def load_failures():
    """Load failure history"""
    if os.path.exists(FAILURE_FILE):
        with open(FAILURE_FILE, 'r') as f:
            return json.load(f)
    return {"failures": [], "key_status": {}}

def save_failures(failures):
    """Save failure history"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FAILURE_FILE, 'w') as f:
        json.dump(failures, f, indent=2)

def detect_failures(log_content, provider=None):
    """Detect API failures from log content"""
    failures = []
    
    for error_type, pattern in ERROR_PATTERNS.items():
        matches = re.finditer(pattern, log_content, re.IGNORECASE)
        for match in matches:
            failures.append({
                "type": error_type,
                "message": match.group(0)[:100],
                "timestamp": datetime.now().isoformat(),
                "provider": provider or "unknown"
            })
    
    return failures

def check_key_health(provider):
    """Check health status of a provider's key"""
    failures = load_failures()
    
    # Count recent failures for this provider
    recent_failures = [
        f for f in failures.get('failures', [])
        if f.get('provider') == provider
        and (datetime.now() - datetime.fromisoformat(f['timestamp'])) < timedelta(hours=24)
    ]
    
    failure_count = len(recent_failures)
    
    if failure_count >= 5:
        status = "dead"
    elif failure_count >= 3:
        status = "degraded"
    elif failure_count >= 1:
        status = "unstable"
    else:
        status = "healthy"
    
    return {
        "provider": provider,
        "status": status,
        "failure_count_24h": failure_count,
        "recent_failures": recent_failures[-3:]
    }

def get_all_key_status():
    """Get status of all API keys"""
    failures = load_failures()
    providers = set(f.get('provider') for f in failures.get('failures', []))
    
    status = {}
    for provider in providers:
        status[provider] = check_key_health(provider)
    
    return status

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        # Show all key status
        status = get_all_key_status()
        print(json.dumps(status, indent=2))
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'check':
        if len(sys.argv) < 3:
            print("Usage: key_health.py check <provider>")
            sys.exit(1)
        result = check_key_health(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif command == 'status':
        status = get_all_key_status()
        print(json.dumps(status, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
