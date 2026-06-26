#!/usr/bin/env python3
"""
Anti-Infinite-Loop — Morgana Guardian Skill
Protects against infinite loops in AI agent execution

Usage:
    python3 anti_infinite_loop.py --max-iterations 10 --timeout 300
"""

import argparse
import sys
import time
from pathlib import Path


class AntiInfiniteLoop:
    """Guardian against infinite loops"""
    
    def __init__(self, max_iterations=10, max_time=300):
        self.max_iterations = max_iterations
        self.max_time = max_time
        self.iteration_count = 0
        self.start_time = None
        self.action_history = []
    
    def should_stop(self):
        """Check if execution should stop"""
        # Check iteration limit
        if self.iteration_count >= self.max_iterations:
            return True, "MAX_ITERATIONS_REACHED"
        
        # Check time limit
        if self.start_time and (time.time() - self.start_time) > self.max_time:
            return True, "TIMEOUT_EXCEEDED"
        
        # Check for repeated actions
        if len(self.action_history) >= 3:
            if self.action_history[-3] == self.action_history[-2] == self.action_history[-1]:
                return True, "REPEATED_ACTION_DETECTED"
        
        return False, None
    
    def track_action(self, action_name):
        """Track an action for pattern detection"""
        self.iteration_count += 1
        if self.start_time is None:
            self.start_time = time.time()
        self.action_history.append(action_name)
        if len(self.action_history) > 10:
            self.action_history.pop(0)
    
    def check_progress(self, result):
        """Check if progress is being made"""
        return result is not None


def main():
    parser = argparse.ArgumentParser(description="Anti-Infinite-Loop Guardian")
    parser.add_argument("--max-iterations", type=int, default=10, help="Max iterations")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    parser.add_argument("--test", action="store_true", help="Run test")
    args = parser.parse_args()
    
    guardian = AntiInfiniteLoop(max_iterations=args.max_iterations, max_time=args.timeout)
    
    if args.test:
        # Run basic test
        print("🧪 Testing Anti-Infinite-Loop...")
        for i in range(12):
            guardian.track_action(f"action_{i}")
            stop, reason = guardian.should_stop()
            print(f"  Iteration {i+1}: stop={stop}, reason={reason}")
            if stop:
                break
        print("✅ Test complete")
        return 0
    
    print("🛡️ Anti-Infinite-Loop Guardian initialized")
    print(f"   Max iterations: {args.max_iterations}")
    print(f"   Timeout: {args.timeout}s")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
