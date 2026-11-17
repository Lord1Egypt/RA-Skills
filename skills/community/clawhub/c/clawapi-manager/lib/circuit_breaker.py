#!/usr/bin/env python3
"""
API Cockpit - Circuit Breaker State Machine
Implements failure -> circuit -> probe -> recovery states
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from enum import Enum

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')

os.makedirs(DATA_DIR, exist_ok=True)

STATE_FILE = os.path.join(DATA_DIR, 'circuit_state.json')

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Circuit tripped, no requests
    HALF_OPEN = "half_open" # Testing if recovered

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout  # seconds
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.load_state()
    
    def load_state(self):
        """Load state from file"""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                self.state = CircuitState(data.get('state', 'closed'))
                self.failure_count = data.get('failure_count', 0)
                if data.get('last_failure_time'):
                    self.last_failure_time = datetime.fromisoformat(data['last_failure_time'])
    
    def save_state(self):
        """Save state to file"""
        data = {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'updated_at': datetime.now().isoformat()
        }
        
        # Atomic write
        tmp_file = f"{STATE_FILE}.tmp"
        with open(tmp_file, 'w') as f:
            json.dump(data, f, indent=2)
        os.rename(tmp_file, STATE_FILE)
    
    def record_failure(self):
        """Record a failure"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.state == CircuitState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"🔌 CIRCUIT OPENED after {self.failure_count} failures")
        
        self.save_state()
    
    def record_success(self):
        """Record a success"""
        if self.state == CircuitState.HALF_OPEN:
            # Success in half-open -> close the circuit
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            print("✅ CIRCUIT CLOSED - service recovered")
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = max(0, self.failure_count - 1)
        
        self.save_state()
    
    def can_proceed(self):
        """Check if request can proceed"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    print("🧪 Entering HALF-OPEN state - testing recovery")
                    self.save_state()
                    return True
        
        if self.state == CircuitState.HALF_OPEN:
            # Allow one request to test
            return True
        
        return False
    
    def get_status(self):
        """Get current status"""
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'last_failure': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'can_proceed': self.can_proceed()
        }

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: circuit_breaker.py [status|fail|success|test]")
        sys.exit(1)
    
    cb = CircuitBreaker()
    command = sys.argv[1]
    
    if command == 'status':
        print(json.dumps(cb.get_status(), indent=2))
    elif command == 'fail':
        cb.record_failure()
        print(json.dumps(cb.get_status(), indent=2))
    elif command == 'success':
        cb.record_success()
        print(json.dumps(cb.get_status(), indent=2))
    elif command == 'test':
        print(f"Can proceed: {cb.can_proceed()}")
        print(json.dumps(cb.get_status(), indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
