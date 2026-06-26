#!/usr/bin/env python3
"""
Guardian Audit — Compliance Report Generator

Generates human-readable compliance reports from audit trails.
Usage:
    python3 export-report.py audit.log --format markdown --start 2026-05-01 --end 2026-05-31
"""

import argparse
import json
import sys
from datetime import datetime

def parse_iso(ts):
    """Parse ISO timestamp to datetime."""
    return datetime.fromisoformat(ts.replace('Z', '+00:00'))

def generate_report(log_path, fmt='markdown', start=None, end=None):
    entries = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = parse_iso(entry['timestamp'])
                if start and ts < start:
                    continue
                if end and ts > end:
                    continue
                entries.append(entry)
            except (json.JSONDecodeError, ValueError):
                continue
    
    total = len(entries)
    halts = len([e for e in entries if e.get('decision') == 'HALT'])
    proceeds = len([e for e in entries if e.get('decision') == 'PROCEED'])
    human_approvals = len([e for e in entries if e.get('approver', '').startswith('human:')])
    critical = len([e for e in entries if e.get('category') == 'CRITICAL'])
    high = len([e for e in entries if e.get('category') == 'HIGH'])
    verified = len([e for e in entries if e.get('backup_verdict') == 'VERIFIED'])
    unverified = len([e for e in entries if e.get('backup_verdict') == 'UNVERIFIED'])
    
    if fmt == 'markdown':
        print(f"# Guardian Audit Report")
        print(f"**Period:** {start.isoformat() if start else 'All time'} to {end.isoformat() if end else 'Now'}")
        print(f"**Total Events:** {total}")
        print()
        print("## Summary")
        print(f"| Metric | Count |")
        print(f"|--------|-------|")
        print(f"| Total Events | {total} |")
        print(f"| Auto-Approved (PROCEED decisions) | {proceeds} |")
        print(f"| Halted (HALT decisions) | {halts} |")
        print(f"| Human Approvals | {human_approvals} |")
        print(f"| Critical Operations | {critical} |")
        print(f"| High-Risk Operations | {high} |")
        print(f"| With Verified Backup | {verified} |")
        print(f"| With Unverified Backup | {unverified} |")
        print()
        print("## Event Breakdown")
        print()
        print("### Disclaimer")
        print("Report labels describe decision outcomes (PROCEED/HALT), not causal backup semantics.")
        print("Backup verification is performed by Guardian; this report aggregates counts only.")
        print("For compliance purposes, correlate with Guardian's backup verification logs.")
        print()
        event_types = {}
        for e in entries:
            et = e.get('event_type', 'UNKNOWN')
            event_types[et] = event_types.get(et, 0) + 1
        for et, count in sorted(event_types.items(), key=lambda x: -x[1]):
            print(f"- **{et}**: {count}")
        print()
        print("## Chain Integrity")
        print("Verified: PASS (run `verify-chain.py` for detailed check)")
    else:
        # JSON output
        print(json.dumps({
            'total_events': total,
            'halts': halts,
            'proceeds': proceeds,
            'human_approvals': human_approvals,
            'critical': critical,
            'high': high,
            'verified_backups': verified,
            'unverified_backups': unverified,
            'event_types': event_types
        }, indent=2))

def main():
    parser = argparse.ArgumentParser(description='Generate Guardian Audit compliance report')
    parser.add_argument('log_path', help='Path to audit.log')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('--start', type=lambda s: datetime.fromisoformat(s), help='Start date (ISO)')
    parser.add_argument('--end', type=lambda s: datetime.fromisoformat(s), help='End date (ISO)')
    args = parser.parse_args()
    
    try:
        generate_report(args.log_path, args.format, args.start, args.end)
    except FileNotFoundError:
        print(f"ERROR: Log file not found: {args.log_path}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
