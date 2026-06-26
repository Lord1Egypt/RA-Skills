#!/usr/bin/env python3
"""
Canary Audit — Audit Trail and Reporting
Analyzes Canary logs and generates safety reports.

Author: Shadow Rose
License: MIT
"""

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CanaryAuditor:
    """Audit trail analyzer and reporter."""
    
    def __init__(self, log_file: str = 'canary.log', tripwire_dir: str = '.canary_tripwires'):
        """
        Initialize auditor.
        
        Args:
            log_file: Path to main Canary log file
            tripwire_dir: Directory containing tripwire logs
        """
        self.log_file = Path(log_file)
        self.tripwire_dir = Path(tripwire_dir)
        self.alert_log = self.tripwire_dir / 'alerts.log'
        
        self.actions = []
        self.violations = []
        self.halts = []
        self.tripwire_alerts = []
        
        self._load_logs()
    
    def _load_logs(self):
        """Load all log files."""
        # Load main Canary log
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    try:
                        if line.startswith('VIOLATION:'):
                            entry = json.loads(line.split('VIOLATION:', 1)[1].strip())
                            self.violations.append(entry)
                        elif line.startswith('HALT:'):
                            entry = json.loads(line.split('HALT:', 1)[1].strip())
                            self.halts.append(entry)
                        else:
                            entry = json.loads(line)
                            self.actions.append(entry)
                    except:
                        continue
        
        # Load tripwire alerts
        if self.alert_log.exists():
            with open(self.alert_log, 'r') as f:
                for line in f:
                    try:
                        alert = json.loads(line.strip())
                        self.tripwire_alerts.append(alert)
                    except:
                        continue
    
    def generate_summary_report(self) -> Dict:
        """
        Generate summary report of all Canary activity.
        
        Returns:
            Report dictionary
        """
        # Calculate time range
        all_timestamps = []
        for entry in self.actions + self.violations + self.tripwire_alerts:
            if 'timestamp' in entry:
                all_timestamps.append(entry['timestamp'])
        
        if all_timestamps:
            earliest = min(all_timestamps)
            latest = max(all_timestamps)
            time_range = f"{earliest} to {latest}"
        else:
            time_range = "No data"
        
        # Count severities
        violation_severities = Counter(v.get('severity', 'unknown') for v in self.violations)
        alert_severities = Counter(a.get('severity', 'unknown') for a in self.tripwire_alerts)
        
        # Count action types
        action_types = Counter(a.get('type', 'unknown') for a in self.actions)
        
        return {
            'time_range': time_range,
            'total_actions': len(self.actions),
            'total_violations': len(self.violations),
            'total_tripwire_alerts': len(self.tripwire_alerts),
            'total_halts': len(self.halts),
            'action_types': dict(action_types),
            'violation_severities': dict(violation_severities),
            'alert_severities': dict(alert_severities),
        }
    
    def get_violations_by_severity(self, severity: str) -> List[Dict]:
        """
        Get violations of specific severity.
        
        Args:
            severity: Severity level to filter
            
        Returns:
            List of violation entries
        """
        return [v for v in self.violations if v.get('severity') == severity]
    
    def get_timeline(self, hours: int = 24) -> List[Dict]:
        """
        Get timeline of events in recent hours.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            Chronological list of events
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        
        timeline = []
        
        # Add all events
        for action in self.actions:
            ts = datetime.fromisoformat(action['timestamp'])
            if ts >= cutoff:
                timeline.append({
                    'timestamp': action['timestamp'],
                    'type': 'action',
                    'event': action,
                })
        
        for violation in self.violations:
            ts = datetime.fromisoformat(violation['timestamp'])
            if ts >= cutoff:
                timeline.append({
                    'timestamp': violation['timestamp'],
                    'type': 'violation',
                    'event': violation,
                })
        
        for alert in self.tripwire_alerts:
            ts = datetime.fromisoformat(alert['timestamp'])
            if ts >= cutoff:
                timeline.append({
                    'timestamp': alert['timestamp'],
                    'type': 'tripwire_alert',
                    'event': alert,
                })
        
        # Sort chronologically
        timeline.sort(key=lambda x: x['timestamp'])
        
        return timeline
    
    def get_top_targets(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get most frequently accessed targets.
        
        Args:
            limit: Number of top targets to return
            
        Returns:
            List of (target, count) tuples
        """
        targets = Counter(a.get('target', 'unknown') for a in self.actions)
        return targets.most_common(limit)
    
    def detect_patterns(self) -> Dict:
        """
        Detect suspicious patterns in logs.
        
        Returns:
            Dictionary of detected patterns
        """
        patterns = {
            'rapid_violations': [],
            'repeated_targets': [],
            'time_clusters': [],
        }
        
        # Detect rapid violations (multiple violations within short time)
        if len(self.violations) >= 2:
            for i in range(len(self.violations) - 1):
                t1 = datetime.fromisoformat(self.violations[i]['timestamp'])
                t2 = datetime.fromisoformat(self.violations[i + 1]['timestamp'])
                
                if (t2 - t1).total_seconds() < 10:  # Within 10 seconds
                    patterns['rapid_violations'].append({
                        'violation1': self.violations[i],
                        'violation2': self.violations[i + 1],
                        'gap_seconds': (t2 - t1).total_seconds(),
                    })
        
        # Detect repeated target access
        target_counts = Counter()
        for action in self.actions:
            target = action.get('target')
            if target:
                target_counts[target] += 1
        
        for target, count in target_counts.items():
            if count > 10:  # More than 10 accesses
                patterns['repeated_targets'].append({
                    'target': target,
                    'count': count,
                })
        
        # Detect time clustering (many actions in short period)
        if self.actions:
            action_times = [datetime.fromisoformat(a['timestamp']) for a in self.actions]
            action_times.sort()
            
            for i in range(len(action_times) - 4):
                window_start = action_times[i]
                window_end = action_times[i + 4]
                
                if (window_end - window_start).total_seconds() < 5:  # 5 actions in 5 seconds
                    patterns['time_clusters'].append({
                        'start': window_start.isoformat(),
                        'end': window_end.isoformat(),
                        'action_count': 5,
                    })
        
        return patterns
    
    def export_report(self, output_file: str, format: str = 'json'):
        """
        Export audit report to file.
        
        Args:
            output_file: Output file path
            format: Export format (json, markdown)
        """
        summary = self.generate_summary_report()
        patterns = self.detect_patterns()
        
        if format == 'json':
            report = {
                'generated': datetime.now().isoformat(),
                'summary': summary,
                'patterns': patterns,
                'violations': self.violations,
                'tripwire_alerts': self.tripwire_alerts,
                'halts': self.halts,
            }
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
        
        elif format == 'markdown':
            md = self._generate_markdown_report(summary, patterns)
            with open(output_file, 'w') as f:
                f.write(md)
        
        print(f"✅ Report exported: {output_file}")
    
    def _generate_markdown_report(self, summary: Dict, patterns: Dict) -> str:
        """Generate markdown formatted report."""
        md = f"""# Canary Audit Report

**Generated:** {datetime.now().isoformat()}

---

## Summary

**Time Range:** {summary['time_range']}

- **Total Actions:** {summary['total_actions']}
- **Total Violations:** {summary['total_violations']}
- **Tripwire Alerts:** {summary['total_tripwire_alerts']}
- **System Halts:** {summary['total_halts']}

### Action Types

"""
        for action_type, count in summary['action_types'].items():
            md += f"- {action_type}: {count}\n"
        
        md += "\n### Violation Severities\n\n"
        for severity, count in summary['violation_severities'].items():
            md += f"- {severity}: {count}\n"
        
        md += "\n---\n\n## Detected Patterns\n\n"
        
        md += f"### Rapid Violations\n\n"
        md += f"Found {len(patterns['rapid_violations'])} instance(s) of rapid violations.\n\n"
        
        md += f"### Repeated Targets\n\n"
        if patterns['repeated_targets']:
            for item in patterns['repeated_targets']:
                md += f"- {item['target']}: {item['count']} accesses\n"
        else:
            md += "None detected.\n"
        
        md += f"\n### Time Clusters\n\n"
        md += f"Found {len(patterns['time_clusters'])} time cluster(s).\n\n"
        
        md += "\n---\n\n## Recent Violations\n\n"
        recent_violations = sorted(self.violations, key=lambda x: x['timestamp'], reverse=True)[:10]
        
        for v in recent_violations:
            md += f"### {v['timestamp']}\n\n"
            md += f"- **Severity:** {v['severity']}\n"
            md += f"- **Message:** {v['message']}\n\n"
        
        return md


def main():
    """CLI for audit reporting."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Canary Audit Reporter')
    parser.add_argument('action', choices=['summary', 'violations', 'timeline', 'patterns', 'export'],
                       help='Action to perform')
    parser.add_argument('--log', default='canary.log', help='Main log file')
    parser.add_argument('--tripwire-dir', default='.canary_tripwires', help='Tripwire directory')
    parser.add_argument('--severity', help='Filter by severity')
    parser.add_argument('--hours', type=int, default=24, help='Hours to look back')
    parser.add_argument('--output', help='Output file for export')
    parser.add_argument('--format', default='json', choices=['json', 'markdown'], help='Export format')
    
    args = parser.parse_args()
    
    auditor = CanaryAuditor(args.log, args.tripwire_dir)
    
    if args.action == 'summary':
        summary = auditor.generate_summary_report()
        print("\nCanary Audit Summary")
        print("=" * 70)
        print(f"Time Range:         {summary['time_range']}")
        print(f"Total Actions:      {summary['total_actions']}")
        print(f"Total Violations:   {summary['total_violations']}")
        print(f"Tripwire Alerts:    {summary['total_tripwire_alerts']}")
        print(f"System Halts:       {summary['total_halts']}")
        print("\nAction Types:")
        for action_type, count in summary['action_types'].items():
            print(f"  {action_type:20} {count}")
        print("\nViolation Severities:")
        for severity, count in summary['violation_severities'].items():
            print(f"  {severity:20} {count}")
        print()
    
    elif args.action == 'violations':
        if args.severity:
            violations = auditor.get_violations_by_severity(args.severity)
        else:
            violations = auditor.violations
        
        print(f"\nViolations ({len(violations)}):")
        print("-" * 70)
        for v in violations:
            print(f"[{v['timestamp']}] {v['severity'].upper()}")
            print(f"  {v['message']}")
            print()
    
    elif args.action == 'timeline':
        timeline = auditor.get_timeline(hours=args.hours)
        print(f"\nEvent Timeline (last {args.hours} hours):")
        print("-" * 70)
        for event in timeline:
            print(f"[{event['timestamp']}] {event['type'].upper()}")
            if event['type'] == 'violation':
                print(f"  {event['event']['message']}")
            elif event['type'] == 'tripwire_alert':
                print(f"  {event['event']['path']}: {event['event']['event']}")
            print()
    
    elif args.action == 'patterns':
        patterns = auditor.detect_patterns()
        print("\nDetected Patterns:")
        print("=" * 70)
        print(f"Rapid Violations:   {len(patterns['rapid_violations'])}")
        print(f"Repeated Targets:   {len(patterns['repeated_targets'])}")
        print(f"Time Clusters:      {len(patterns['time_clusters'])}")
        
        if patterns['repeated_targets']:
            print("\nRepeated Targets:")
            for item in patterns['repeated_targets']:
                print(f"  {item['target']:40} {item['count']} times")
        print()
    
    elif args.action == 'export':
        if not args.output:
            print("Error: --output required for export")
            return
        
        auditor.export_report(args.output, format=args.format)


if __name__ == '__main__':
    main()
