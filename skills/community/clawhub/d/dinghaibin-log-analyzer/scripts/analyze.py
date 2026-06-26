#!/usr/bin/env python3
"""
Log Analyzer - Analyze log files to extract insights and patterns
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


LEVELS = ['ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'FATAL', 'CRITICAL']


def parse_log_line(line):
    """Parse a log line and extract components."""
    # Try common formats
    patterns = [
        # Apache/Nginx: 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET / HTTP/1.1" 200 1024
        r'(\d+\.\d+\.\d+\.\d+).*\[([^\]]+)\].*"(GET|POST|PUT|DELETE|HEAD|OPTIONS)\s+([^\s]+).*" (\d+)',
        # Standard: 2023-10-10 10:00:00 ERROR message
        r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\s]*)\s+(ERROR|WARN|WARNING|INFO|DEBUG|TRACE|FATAL|CRITICAL)\s+(.*)',
        # JSON-like: {"level": "error", "message": "..."}
        r'"level"\s*:\s*"([^"]+)".*"message"\s*:\s*"([^"]+)"',
    ]
    
    line = line.strip()
    
    # Check for error/warning keywords
    level = None
    for lvl in LEVELS:
        if lvl in line.upper():
            level = lvl
            break
    
    return {
        'raw': line,
        'level': level,
        'timestamp': None,
        'message': line
    }


def analyze_file(filepath, options):
    """Analyze a log file."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"Error: {filepath} does not exist")
        return None
    
    stats = {
        'total_lines': 0,
        'errors': 0,
        'warnings': 0,
        'by_level': Counter(),
        'patterns': Counter(),
        'error_lines': [],
        'warning_lines': []
    }
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stats['total_lines'] += 1
                parsed = parse_log_line(line)
                
                level = parsed.get('level', 'UNKNOWN')
                if level:
                    stats['by_level'][level] += 1
                    
                    if level in ['ERROR', 'FATAL', 'CRITICAL']:
                        stats['errors'] += 1
                        if len(stats['error_lines']) < 100:
                            stats['error_lines'].append(line.strip())
                    elif level in ['WARN', 'WARNING']:
                        stats['warnings'] += 1
                        if len(stats['warning_lines']) < 100:
                            stats['warning_lines'].append(line.strip())
                
                # Pattern matching
                if options.pattern:
                    if re.search(options.pattern, line):
                        stats['patterns'][options.pattern] += 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    return stats


def print_summary(stats):
    """Print summary statistics."""
    print("\n=== Log Analysis Summary ===")
    print(f"Total lines: {stats['total_lines']}")
    print(f"\nBy Level:")
    for level, count in sorted(stats['by_level'].items()):
        print(f"  {level}: {count}")
    print(f"\nErrors: {stats['errors']}")
    print(f"Warnings: {stats['warnings']}")


def main():
    parser = argparse.ArgumentParser(description='Log Analyzer')
    parser.add_argument('logfile', help='Log file to analyze')
    parser.add_argument('--errors', action='store_true', help='Show error lines')
    parser.add_argument('--warnings', action='store_true', help='Show warning lines')
    parser.add_argument('--pattern', help='Search for regex pattern')
    parser.add_argument('--summary', action='store_true', help='Show summary')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--output', help='Output file')
    parser.add_argument('--lines', type=int, default=20, help='Lines to show')
    
    args = parser.parse_args()
    
    stats = analyze_file(args.logfile, args)
    if not stats:
        return 1
    
    # Output
    if args.json:
        output = {
            'total_lines': stats['total_lines'],
            'errors': stats['errors'],
            'warnings': stats['warnings'],
            'by_level': dict(stats['by_level']),
            'error_lines': stats['error_lines'][:args.lines]
        }
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Saved to: {args.output}")
        else:
            print(json.dumps(output, indent=2))
        return 0
    
    # Show errors
    if args.errors:
        print("\n=== Errors ===")
        for line in stats['error_lines'][:args.lines]:
            print(line)
        if len(stats['error_lines']) > args.lines:
            print(f"... and {len(stats['error_lines']) - args.lines} more")
    
    # Show warnings
    if args.warnings:
        print("\n=== Warnings ===")
        for line in stats['warning_lines'][:args.lines]:
            print(line)
        if len(stats['warning_lines']) > args.lines:
            print(f"... and {len(stats['warning_lines']) - args.lines} more")
    
    # Summary
    if args.summary or (not args.errors and not args.warnings):
        print_summary(stats)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
