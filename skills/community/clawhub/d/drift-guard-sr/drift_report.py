#!/usr/bin/env python3
"""
Drift Guard — Trend Analysis & Reporting
Analyzes drift history and generates trend reports.

Author: Shadow Rose
License: MIT
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def load_history(history_path: str) -> List[Dict]:
    """Load drift history from file."""
    with open(history_path, 'r') as f:
        return json.load(f)


def filter_by_timerange(history: List[Dict], hours: Optional[int] = None) -> List[Dict]:
    """
    Filter history to specific time range.
    
    Args:
        history: Full history list
        hours: Number of hours to include (None = all)
        
    Returns:
        Filtered history
    """
    if hours is None:
        return history
    
    cutoff = datetime.now() - timedelta(hours=hours)
    cutoff_ts = cutoff.timestamp()
    
    return [h for h in history if h['timestamp'] >= cutoff_ts]


def calculate_trend(history: List[Dict]) -> Dict:
    """
    Calculate drift trend statistics.
    
    Args:
        history: Drift history records
        
    Returns:
        Trend statistics dictionary
    """
    if not history:
        return {'error': 'No history data'}
    
    drift_scores = [h['drift_score'] for h in history]
    
    # Basic stats
    stats = {
        'count': len(drift_scores),
        'current': drift_scores[-1],
        'min': min(drift_scores),
        'max': max(drift_scores),
        'avg': sum(drift_scores) / len(drift_scores),
        'first': drift_scores[0],
        'last': drift_scores[-1]
    }
    
    # Trend direction (compare first half to second half)
    mid = len(drift_scores) // 2
    if mid > 0:
        first_half_avg = sum(drift_scores[:mid]) / mid
        second_half_avg = sum(drift_scores[mid:]) / (len(drift_scores) - mid)
        stats['trend'] = 'worsening' if second_half_avg > first_half_avg else 'improving'
        stats['trend_magnitude'] = abs(second_half_avg - first_half_avg)
    else:
        stats['trend'] = 'insufficient_data'
        stats['trend_magnitude'] = 0.0
    
    # Recent change (last 10% vs previous 10%)
    recent_window = max(1, len(drift_scores) // 10)
    if len(drift_scores) >= recent_window * 2:
        recent = drift_scores[-recent_window:]
        previous = drift_scores[-recent_window*2:-recent_window]
        recent_avg = sum(recent) / len(recent)
        previous_avg = sum(previous) / len(previous)
        stats['recent_change'] = recent_avg - previous_avg
    else:
        stats['recent_change'] = 0.0
    
    # Volatility (standard deviation)
    if len(drift_scores) > 1:
        mean = stats['avg']
        variance = sum((x - mean) ** 2 for x in drift_scores) / len(drift_scores)
        stats['std_dev'] = variance ** 0.5
    else:
        stats['std_dev'] = 0.0
    
    return stats


def analyze_metric_trends(history: List[Dict], metric_name: str) -> Dict:
    """
    Analyze trend for a specific metric.
    
    Args:
        history: Drift history records
        metric_name: Name of metric to analyze
        
    Returns:
        Metric trend statistics
    """
    values = []
    for h in history:
        if 'metrics' in h and metric_name in h['metrics']:
            values.append(h['metrics'][metric_name])
    
    if not values:
        return {'error': f'Metric {metric_name} not found in history'}
    
    stats = {
        'count': len(values),
        'min': min(values),
        'max': max(values),
        'avg': sum(values) / len(values),
        'current': values[-1]
    }
    
    # Change over time
    if len(values) > 1:
        stats['change'] = values[-1] - values[0]
        stats['change_pct'] = (stats['change'] / values[0] * 100) if values[0] != 0 else 0.0
    
    return stats


def detect_anomalies(history: List[Dict], threshold: float = 2.0) -> List[Dict]:
    """
    Detect anomalous drift measurements (outliers).
    
    Args:
        history: Drift history records
        threshold: Standard deviations from mean to flag as anomaly
        
    Returns:
        List of anomalous records
    """
    if len(history) < 3:
        return []
    
    drift_scores = [h['drift_score'] for h in history]
    mean = sum(drift_scores) / len(drift_scores)
    variance = sum((x - mean) ** 2 for x in drift_scores) / len(drift_scores)
    std_dev = variance ** 0.5
    
    anomalies = []
    for h in history:
        score = h['drift_score']
        if abs(score - mean) > (threshold * std_dev):
            anomalies.append({
                'timestamp': h['timestamp'],
                'datetime': h['datetime'],
                'drift_score': score,
                'deviation': abs(score - mean) / std_dev
            })
    
    return anomalies


def generate_report(history_path: str, hours: Optional[int] = None, output_format: str = 'text'):
    """
    Generate comprehensive drift report.
    
    Args:
        history_path: Path to drift history file
        hours: Time range in hours (None = all time)
        output_format: 'text' or 'json'
    """
    history = load_history(history_path)
    filtered = filter_by_timerange(history, hours)
    
    if not filtered:
        print("No data in specified time range.")
        return
    
    # Calculate statistics
    trend = calculate_trend(filtered)
    anomalies = detect_anomalies(filtered)
    
    # Time range info
    time_range = {
        'start': filtered[0]['datetime'],
        'end': filtered[-1]['datetime'],
        'span_hours': hours if hours else 'all'
    }
    
    # Metric-specific trends
    metric_trends = {}
    if filtered and 'metrics' in filtered[0]:
        for metric_name in filtered[0]['metrics'].keys():
            metric_trends[metric_name] = analyze_metric_trends(filtered, metric_name)
    
    report = {
        'time_range': time_range,
        'drift_trend': trend,
        'anomalies': anomalies,
        'metric_trends': metric_trends
    }
    
    if output_format == 'json':
        print(json.dumps(report, indent=2))
    else:
        print_text_report(report)


def print_text_report(report: Dict):
    """Print report in human-readable text format."""
    print("\n" + "=" * 70)
    print("DRIFT GUARD — TREND REPORT")
    print("=" * 70)
    
    # Time range
    tr = report['time_range']
    print(f"\nTime Range: {tr['start']} to {tr['end']}")
    print(f"Span: {tr['span_hours']} hours" if isinstance(tr['span_hours'], int) else f"Span: {tr['span_hours']}")
    
    # Drift trend
    print("\n" + "-" * 70)
    print("DRIFT TREND")
    print("-" * 70)
    
    trend = report['drift_trend']
    print(f"Measurements: {trend['count']}")
    print(f"Current Score: {trend['current']:.3f}")
    print(f"Average: {trend['avg']:.3f}")
    print(f"Range: {trend['min']:.3f} to {trend['max']:.3f}")
    print(f"Std Dev: {trend.get('std_dev', 0):.3f}")
    
    if 'trend' in trend and trend['trend'] != 'insufficient_data':
        print(f"\nTrend: {trend['trend'].upper()} (magnitude: {trend['trend_magnitude']:.3f})")
        print(f"Recent Change: {trend['recent_change']:+.3f}")
    
    # Anomalies
    if report['anomalies']:
        print("\n" + "-" * 70)
        print(f"ANOMALIES ({len(report['anomalies'])} detected)")
        print("-" * 70)
        for a in report['anomalies'][:10]:  # Show up to 10
            print(f"  {a['datetime']}: {a['drift_score']:.3f} ({a['deviation']:.1f}σ)")
    
    # Top metric changes
    if report['metric_trends']:
        print("\n" + "-" * 70)
        print("TOP METRIC CHANGES")
        print("-" * 70)
        
        # Sort by absolute change percentage
        sorted_metrics = sorted(
            [(k, v) for k, v in report['metric_trends'].items() if 'change_pct' in v],
            key=lambda x: abs(x[1].get('change_pct', 0)),
            reverse=True
        )
        
        for metric_name, stats in sorted_metrics[:10]:
            change_pct = stats.get('change_pct', 0)
            print(f"  {metric_name:<30} {change_pct:+7.1f}% (current: {stats['current']:.3f})")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """CLI for drift reporting."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Drift Guard Trend Reporter')
    parser.add_argument('--history', default='drift_history.json',
                       help='Path to drift history file')
    parser.add_argument('--hours', type=int, help='Time range in hours (default: all)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format')
    
    args = parser.parse_args()
    
    try:
        generate_report(args.history, args.hours, args.format)
    except FileNotFoundError:
        print(f"Error: History file not found: {args.history}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
