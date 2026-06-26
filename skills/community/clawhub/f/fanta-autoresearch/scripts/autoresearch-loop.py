#!/usr/bin/env python3
"""
Autoresearch Loop Executor

Run autonomous iteration loops for optimization tasks.

Usage:
    python autoresearch-loop.py --goal "Improve Top-1 to 75%" --verify "openclaw cron runs ..." --max-iterations 5
"""

import argparse
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

def parse_args():
    parser = argparse.ArgumentParser(description='Run autoresearch loop')
    parser.add_argument('--goal', required=True, help='Goal description')
    parser.add_argument('--verify', required=True, help='Verification command')
    parser.add_argument('--metric-extract', help='Regex to extract metric from output')
    parser.add_argument('--max-iterations', type=int, default=10, help='Maximum iterations')
    parser.add_argument('--log', default='autoresearch-log.tsv', help='Log file path')
    parser.add_argument('--threshold', type=float, default=1.0, help='Minimum improvement %')
    return parser.parse_args()

def run_command(cmd: str) -> Tuple[int, str]:
    """Run shell command and return exit code + output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr

def extract_metric(output: str, pattern: str) -> Optional[float]:
    """Extract numeric metric from output using regex pattern."""
    if not pattern:
        return None
    match = re.search(pattern, output)
    if match:
        try:
            return float(match.group(1))
        except (ValueError, IndexError):
            return None
    return None

def log_iteration(log_path: str, iteration: int, change: str, 
                  metric_before: Optional[float], metric_after: Optional[float],
                  status: str, description: str):
    """Log iteration result to TSV file."""
    delta = 0.0
    if metric_before is not None and metric_after is not None:
        delta = metric_after - metric_before
    
    with open(log_path, 'a') as f:
        f.write(f"{iteration}\t{change}\t{metric_before or 'N/A'}\t{metric_after or 'N/A'}\t{delta:+.1f}\t{status}\t{description}\n")

def main():
    args = parse_args()
    
    print(f"=== Autoresearch Loop ===")
    print(f"Goal: {args.goal}")
    print(f"Max iterations: {args.max_iterations}")
    print(f"Log: {args.log}")
    print()
    
    # Initialize log
    with open(args.log, 'w') as f:
        f.write("iteration\tchange\tmetric_before\tmetric_after\tdelta\tstatus\tdescription\n")
    
    # Establish baseline
    print("Establishing baseline...")
    code, output = run_command(args.verify)
    baseline_metric = extract_metric(output, args.metric_extract) if args.metric_extract else None
    
    print(f"Baseline metric: {baseline_metric}")
    log_iteration(args.log, 0, "baseline", baseline_metric, baseline_metric, 
                  "baseline", "initial state")
    
    print()
    print("Starting iteration loop...")
    print("Note: This script only runs the verification loop.")
    print("The actual changes must be made manually or by an agent.")
    print()
    
    current_metric = baseline_metric
    iteration = 0
    
    while iteration < args.max_iterations:
        iteration += 1
        
        # Prompt for change description
        print(f"\n--- Iteration {iteration} ---")
        change = input("Describe the change made (or 'stop' to exit): ").strip()
        
        if change.lower() == 'stop':
            print("Stopping loop per user request.")
            break
        
        if not change:
            print("No change description, skipping iteration.")
            iteration -= 1
            continue
        
        # Run verification
        print("Running verification...")
        code, output = run_command(args.verify)
        new_metric = extract_metric(output, args.metric_extract) if args.metric_extract else None
        
        print(f"New metric: {new_metric}")
        
        # Determine status
        if new_metric is not None and current_metric is not None:
            improvement = new_metric - current_metric
            if improvement >= args.threshold:
                status = "keep"
                current_metric = new_metric
                print(f"✅ IMPROVED by {improvement:+.1f}")
            elif improvement < -args.threshold:
                status = "revert"
                print(f"❌ REGRESSED by {improvement:+.1f}")
            else:
                status = "neutral"
                print(f"➡️ No significant change ({improvement:+.1f})")
        else:
            status = "unknown"
            print("⚠️ Could not extract metric")
        
        # Log result
        log_iteration(args.log, iteration, change, current_metric, new_metric,
                      status, f"code={code}")
    
    # Final summary
    print(f"\n=== Summary ===")
    print(f"Initial metric: {baseline_metric}")
    print(f"Final metric: {current_metric}")
    if baseline_metric and current_metric:
        print(f"Total improvement: {current_metric - baseline_metric:+.1f}")
    print(f"Log saved to: {args.log}")

if __name__ == '__main__':
    main()