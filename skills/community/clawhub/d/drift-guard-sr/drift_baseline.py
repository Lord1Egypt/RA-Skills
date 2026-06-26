#!/usr/bin/env python3
"""
Drift Guard — Baseline Capture Tool
Creates and manages behavior baselines for drift detection.

Author: Shadow Rose
License: MIT
"""

import json
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def capture_baseline_from_files(file_paths: List[str], config: Dict) -> Dict:
    """
    Capture baseline metrics from multiple text files.
    
    Args:
        file_paths: List of paths to text files containing agent responses
        config: Configuration dictionary
        
    Returns:
        Baseline metrics dictionary
    """
    from drift_guard import DriftGuard
    
    dg = DriftGuard(config)
    all_metrics = []
    
    print(f"Analyzing {len(file_paths)} files for baseline...")
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                text = f.read()
            
            metrics = dg.analyze_text(text)
            all_metrics.append(metrics)
            print(f"  ✓ {file_path}")
        
        except Exception as e:
            print(f"  ✗ {file_path}: {e}")
    
    if not all_metrics:
        raise ValueError("No valid metrics captured. Cannot create baseline.")
    
    # Calculate average of each metric
    baseline_metrics = {}
    metric_keys = all_metrics[0].keys()
    
    for key in metric_keys:
        values = [m[key] for m in all_metrics if key in m]
        baseline_metrics[key] = sum(values) / len(values)
    
    baseline = {
        'created': datetime.now().isoformat(),
        'sample_count': len(all_metrics),
        'metrics': baseline_metrics,
        'source_files': file_paths
    }
    
    return baseline


def capture_baseline_from_stdin(config: Dict) -> Dict:
    """
    Capture baseline from stdin (single sample).
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Baseline metrics dictionary
    """
    from drift_guard import DriftGuard
    
    dg = DriftGuard(config)
    text = sys.stdin.read()
    
    metrics = dg.analyze_text(text)
    
    baseline = {
        'created': datetime.now().isoformat(),
        'sample_count': 1,
        'metrics': metrics,
        'source': 'stdin'
    }
    
    return baseline


def save_baseline(baseline: Dict, output_path: str):
    """
    Save baseline to file.
    
    Args:
        baseline: Baseline metrics dictionary
        output_path: Path to save baseline JSON
    """
    with open(output_path, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print(f"\n✓ Baseline saved to {output_path}")
    print(f"  Sample count: {baseline['sample_count']}")
    print(f"  Metrics captured: {len(baseline['metrics'])}")


def compare_baselines(baseline1_path: str, baseline2_path: str):
    """
    Compare two baselines and show differences.
    
    Args:
        baseline1_path: Path to first baseline
        baseline2_path: Path to second baseline
    """
    with open(baseline1_path, 'r') as f:
        b1 = json.load(f)
    
    with open(baseline2_path, 'r') as f:
        b2 = json.load(f)
    
    print(f"\nComparing baselines:")
    print(f"  Baseline 1: {baseline1_path} (created {b1['created']})")
    print(f"  Baseline 2: {baseline2_path} (created {b2['created']})")
    print()
    
    m1 = b1['metrics']
    m2 = b2['metrics']
    
    print(f"{'Metric':<30} {'Baseline 1':>15} {'Baseline 2':>15} {'% Diff':>10}")
    print("-" * 75)
    
    for key in sorted(m1.keys()):
        if key not in m2:
            continue
        
        val1 = m1[key]
        val2 = m2[key]
        
        if val1 != 0:
            diff_pct = ((val2 - val1) / val1) * 100
        else:
            diff_pct = 0.0 if val2 == 0 else 100.0
        
        print(f"{key:<30} {val1:>15.4f} {val2:>15.4f} {diff_pct:>9.1f}%")


def show_baseline(baseline_path: str):
    """
    Display baseline metrics in human-readable format.
    
    Args:
        baseline_path: Path to baseline JSON
    """
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    
    print(f"\nBaseline: {baseline_path}")
    print(f"Created: {baseline['created']}")
    print(f"Samples: {baseline['sample_count']}")
    print("\nMetrics:")
    print(f"{'Metric':<30} {'Value':>15}")
    print("-" * 50)
    
    for key, value in sorted(baseline['metrics'].items()):
        print(f"{key:<30} {value:>15.4f}")


def main():
    """CLI for baseline management."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Drift Guard Baseline Manager')
    parser.add_argument('action', choices=['capture', 'compare', 'show'],
                       help='Action to perform')
    parser.add_argument('--files', nargs='+', help='Text files to analyze (for capture)')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin (for capture)')
    parser.add_argument('--output', default='baseline.json', help='Output baseline file')
    parser.add_argument('--baseline1', help='First baseline (for compare)')
    parser.add_argument('--baseline2', help='Second baseline (for compare)')
    parser.add_argument('--baseline', help='Baseline to show')
    parser.add_argument('--config', help='Config file (Python module)')
    
    args = parser.parse_args()
    
    # Load config
    if args.config:
        sys.path.insert(0, str(Path(args.config).parent))
        module_name = Path(args.config).stem
        config_module = __import__(module_name)
        config = config_module.CONFIG
    else:
        try:
            from config import CONFIG
            config = CONFIG
        except ImportError:
            print("Error: config.py not found. Copy config_example.py to config.py")
            sys.exit(1)
    
    # Execute action
    if args.action == 'capture':
        if args.stdin:
            baseline = capture_baseline_from_stdin(config)
        elif args.files:
            baseline = capture_baseline_from_files(args.files, config)
        else:
            print("Error: Must specify --files or --stdin")
            sys.exit(1)
        
        save_baseline(baseline, args.output)
    
    elif args.action == 'compare':
        if not args.baseline1 or not args.baseline2:
            print("Error: Must specify --baseline1 and --baseline2")
            sys.exit(1)
        
        compare_baselines(args.baseline1, args.baseline2)
    
    elif args.action == 'show':
        if not args.baseline:
            print("Error: Must specify --baseline")
            sys.exit(1)
        
        show_baseline(args.baseline)


if __name__ == '__main__':
    main()
