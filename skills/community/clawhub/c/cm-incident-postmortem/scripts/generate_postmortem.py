#!/usr/bin/env python3
"""Generate structured incident postmortem reports.

Parses log files, timeline data, and incident metadata to produce
blame-free postmortem documents with root cause analysis, timeline,
impact assessment, and action items.

Usage:
    python3 generate_postmortem.py --title "Database outage" --severity P1
    python3 generate_postmortem.py --title "API latency spike" --log /var/log/app.log --since 2h
    python3 generate_postmortem.py --title "Deploy failure" --timeline timeline.json --output html
    python3 generate_postmortem.py --from incident.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from hashlib import md5
from pathlib import Path

# --- Blame-free language checker ---

BLAMEFUL_PATTERNS = [
    (r'\b(he|she|they|someone|developer|engineer|admin|operator)\s+(forgot|failed|missed|neglected|caused|broke|didn\'t)\b',
     'Use passive voice or system-focused language'),
    (r'\b(human error|operator error|user error|negligence|carelessness|incompetence)\b',
     'Describe the system condition, not the person'),
    (r'\b(fault|blame|responsible for the failure|should have known)\b',
     'Focus on process gaps, not individual responsibility'),
    (r'\b(stupid|dumb|obvious|trivial|simple mistake|rookie)\b',
     'Remove judgmental language'),
]

def check_blame_language(text):
    """Return list of (line_num, match, suggestion) for blameful language."""
    issues = []
    for i, line in enumerate(text.split('\n'), 1):
        for pattern, suggestion in BLAMEFUL_PATTERNS:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                issues.append((i, m.group(0), suggestion))
    return issues

# --- Log parsing (simplified, focused on timeline extraction) ---

TIMESTAMP_PATTERNS = [
    # ISO 8601
    (r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)', '%Y-%m-%dT%H:%M:%S'),
    # Syslog
    (r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', None),
    # Nginx error
    (r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})', '%Y/%m/%d %H:%M:%S'),
    # Bracket timestamp
    (r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]', '%Y-%m-%d %H:%M:%S'),
]

SEVERITY_KEYWORDS = {
    'fatal': 'FATAL', 'critical': 'FATAL', 'crit': 'FATAL',
    'error': 'ERROR', 'err': 'ERROR', 'fail': 'ERROR', 'failed': 'ERROR',
    'exception': 'ERROR', 'panic': 'ERROR',
    'warn': 'WARN', 'warning': 'WARN',
}

ERROR_INDICATORS = [
    (r'out of memory|OOM|oom.killer|Cannot allocate', 'OOM / Memory exhaustion'),
    (r'connection refused|ECONNREFUSED|connect\(\) failed', 'Connection refused'),
    (r'connection timed? ?out|ETIMEDOUT', 'Connection timeout'),
    (r'disk full|no space left|ENOSPC', 'Disk full'),
    (r'permission denied|EACCES|403 Forbidden', 'Permission denied'),
    (r'too many open files|EMFILE', 'File descriptor exhaustion'),
    (r'SSL|TLS|certificate|handshake', 'SSL/TLS issue'),
    (r'rate limit|429|throttl', 'Rate limiting'),
    (r'deadlock|lock timeout|lock wait', 'Database deadlock'),
    (r'segfault|segmentation fault|SIGSEGV', 'Segmentation fault'),
    (r'killed|SIGKILL|SIGTERM', 'Process killed'),
    (r'dns|resolve|ENOTFOUND|name resolution', 'DNS resolution failure'),
    (r'replication lag|replica behind', 'Replication lag'),
    (r'health.?check.*fail|unhealthy', 'Health check failure'),
    (r'rollback|roll.?back', 'Rollback event'),
    (r'deploy|deployment|release', 'Deployment event'),
    (r'restart|reboot|recovering', 'Service restart'),
    (r'failover|switchover|primary.*secondary', 'Failover event'),
]

def parse_timestamp(line):
    """Extract timestamp from a log line."""
    for pattern, fmt in TIMESTAMP_PATTERNS:
        m = re.search(pattern, line)
        if m:
            ts_str = m.group(1)
            try:
                if fmt:
                    return datetime.strptime(ts_str.split('.')[0].replace('Z','').split('+')[0].split('-0')[0][:19],
                                           fmt.replace('T', ' ') if 'T' not in fmt else fmt)
                else:
                    # Syslog — assume current year
                    now = datetime.now()
                    return datetime.strptime(f"{now.year} {ts_str}", "%Y %b %d %H:%M:%S")
            except ValueError:
                try:
                    return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    continue
    return None

def extract_severity(line):
    """Detect severity from log line."""
    lower = line.lower()
    for keyword, level in SEVERITY_KEYWORDS.items():
        if re.search(r'\b' + keyword + r'\b', lower):
            return level
    return 'INFO'

def classify_event(line):
    """Classify a log line into event categories."""
    categories = []
    for pattern, label in ERROR_INDICATORS:
        if re.search(pattern, line, re.IGNORECASE):
            categories.append(label)
    return categories

def parse_log_file(path, since=None):
    """Parse a log file and extract timeline events."""
    events = []
    try:
        with open(path, 'r', errors='replace') as f:
            lines = f.readlines()
    except (OSError, IOError) as e:
        print(f"Warning: Cannot read {path}: {e}", file=sys.stderr)
        return events

    for line in lines:
        line = line.strip()
        if not line:
            continue

        ts = parse_timestamp(line)
        if since and ts and ts < since:
            continue

        severity = extract_severity(line)
        if severity in ('INFO',):
            # Only keep info lines if they have event indicators
            categories = classify_event(line)
            if not categories:
                continue
        else:
            categories = classify_event(line)

        if severity in ('ERROR', 'FATAL', 'WARN') or categories:
            events.append({
                'timestamp': ts.isoformat() if ts else None,
                'severity': severity,
                'message': line[:500],
                'categories': categories or [severity.lower()],
            })

    return events

def parse_since(since_str):
    """Parse --since value into datetime."""
    if not since_str:
        return None
    m = re.match(r'^(\d+)(h|d|m)$', since_str)
    if m:
        val, unit = int(m.group(1)), m.group(2)
        delta = {'h': timedelta(hours=val), 'd': timedelta(days=val), 'm': timedelta(minutes=val)}
        return datetime.now() - delta[unit]
    try:
        return datetime.fromisoformat(since_str)
    except ValueError:
        return None

# --- Timeline from JSON ---

def load_timeline_json(path):
    """Load timeline from a JSON file.

    Expected format:
    [
        {"time": "2026-03-28T02:30:00", "event": "Deploy started", "type": "action"},
        {"time": "2026-03-28T02:35:00", "event": "Error rate spike", "type": "detection"},
        ...
    ]
    """
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and 'timeline' in data:
        return data['timeline']
    return []

# --- Incident from JSON ---

def load_incident_json(path):
    """Load full incident definition from JSON.

    Expected format:
    {
        "title": "Database outage",
        "severity": "P1",
        "date": "2026-03-28",
        "duration": "45 minutes",
        "summary": "Primary database became unresponsive...",
        "impact": "All API requests returned 503 for 45 minutes",
        "root_cause": "Connection pool exhaustion due to leaked connections",
        "timeline": [...],
        "action_items": [...]
    }
    """
    with open(path) as f:
        return json.load(f)

# --- Report generation ---

SEVERITY_LABELS = {
    'P0': {'label': 'Critical (P0)', 'color': '#dc2626', 'desc': 'Complete service outage, data loss, security breach'},
    'P1': {'label': 'Major (P1)', 'color': '#ea580c', 'desc': 'Significant degradation, major feature unavailable'},
    'P2': {'label': 'Minor (P2)', 'color': '#ca8a04', 'desc': 'Partial degradation, workaround available'},
    'P3': {'label': 'Low (P3)', 'color': '#16a34a', 'desc': 'Minimal impact, cosmetic or non-critical'},
}

def build_timeline_section(events):
    """Format events into a timeline."""
    if not events:
        return "No timeline events recorded.\n"

    lines = []
    for e in sorted(events, key=lambda x: x.get('time') or x.get('timestamp') or ''):
        ts = e.get('time') or e.get('timestamp', '??:??')
        if isinstance(ts, str) and 'T' in ts:
            ts = ts.replace('T', ' ')
        event = e.get('event') or e.get('message', '')
        etype = e.get('type', '')
        prefix = {'detection': '[DETECTED]', 'action': '[ACTION]', 'resolution': '[RESOLVED]',
                  'escalation': '[ESCALATED]', 'communication': '[COMMS]'}.get(etype, '')
        lines.append(f"- **{ts}** — {prefix} {event}".strip())
    return '\n'.join(lines) + '\n'

def build_log_analysis(events):
    """Summarize parsed log events."""
    if not events:
        return ""

    # Count categories
    cat_counts = {}
    for e in events:
        for c in e.get('categories', []):
            cat_counts[c] = cat_counts.get(c, 0) + 1

    sev_counts = {}
    for e in events:
        s = e['severity']
        sev_counts[s] = sev_counts.get(s, 0) + 1

    lines = ["## Log Analysis\n"]
    lines.append(f"**Total events extracted:** {len(events)}\n")

    if sev_counts:
        lines.append("**By severity:**")
        for s in ['FATAL', 'ERROR', 'WARN']:
            if s in sev_counts:
                lines.append(f"- {s}: {sev_counts[s]}")
        lines.append("")

    if cat_counts:
        lines.append("**Top event categories:**")
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1])[:10]:
            lines.append(f"- {cat}: {count}")
        lines.append("")

    # Show first few critical events
    critical = [e for e in events if e['severity'] in ('FATAL', 'ERROR')][:5]
    if critical:
        lines.append("**Key error events:**")
        for e in critical:
            ts = e.get('timestamp', '??:??')
            msg = e['message'][:200]
            lines.append(f"- `{ts}` — {msg}")
        lines.append("")

    return '\n'.join(lines) + '\n'

def generate_markdown(incident, timeline_events=None, log_events=None):
    """Generate a markdown postmortem report."""
    title = incident.get('title', 'Untitled Incident')
    severity = incident.get('severity', 'P2')
    sev_info = SEVERITY_LABELS.get(severity, SEVERITY_LABELS['P2'])
    date = incident.get('date', datetime.now().strftime('%Y-%m-%d'))
    duration = incident.get('duration', 'TBD')

    sections = []

    # Header
    sections.append(f"# Incident Postmortem: {title}\n")
    sections.append(f"| Field | Value |")
    sections.append(f"|-------|-------|")
    sections.append(f"| **Date** | {date} |")
    sections.append(f"| **Severity** | {sev_info['label']} |")
    sections.append(f"| **Duration** | {duration} |")
    sections.append(f"| **Status** | {incident.get('status', 'Resolved')} |")
    sections.append(f"| **Author** | {incident.get('author', 'Auto-generated')} |")
    sections.append("")

    # Summary
    sections.append("## Summary\n")
    sections.append(incident.get('summary', '_Provide a 2-3 sentence summary of what happened._\n'))
    sections.append("")

    # Impact
    sections.append("## Impact\n")
    impact = incident.get('impact', '')
    if impact:
        sections.append(impact)
    else:
        sections.append("_Describe the user-facing impact:_")
        sections.append("- **Users affected:** ")
        sections.append("- **Requests failed:** ")
        sections.append("- **Revenue impact:** ")
        sections.append("- **SLA impact:** ")
    sections.append("")

    # Timeline
    sections.append("## Timeline\n")
    all_events = []
    if timeline_events:
        all_events.extend(timeline_events)
    if incident.get('timeline'):
        all_events.extend(incident['timeline'])
    sections.append(build_timeline_section(all_events))

    # Log analysis (if logs were provided)
    if log_events:
        sections.append(build_log_analysis(log_events))

    # Root cause
    sections.append("## Root Cause\n")
    root_cause = incident.get('root_cause', '')
    if root_cause:
        sections.append(root_cause)
    else:
        sections.append("_Describe the technical root cause. Focus on system conditions, not people._\n")
        sections.append("**Contributing factors:**")
        sections.append("- ")
    sections.append("")

    # Detection
    sections.append("## Detection\n")
    detection = incident.get('detection', '')
    if detection:
        sections.append(detection)
    else:
        sections.append("_How was the incident detected?_")
        sections.append("- **Method:** (monitoring alert / customer report / manual observation)")
        sections.append("- **Time to detect:** ")
        sections.append("- **Gaps:** ")
    sections.append("")

    # Resolution
    sections.append("## Resolution\n")
    resolution = incident.get('resolution', '')
    if resolution:
        sections.append(resolution)
    else:
        sections.append("_What was done to resolve the incident?_")
        sections.append("1. ")
    sections.append("")

    # Lessons learned
    sections.append("## Lessons Learned\n")
    lessons = incident.get('lessons_learned', '')
    if lessons:
        if isinstance(lessons, list):
            for l in lessons:
                sections.append(f"- {l}")
        else:
            sections.append(lessons)
    else:
        sections.append("### What went well")
        sections.append("- ")
        sections.append("")
        sections.append("### What went poorly")
        sections.append("- ")
        sections.append("")
        sections.append("### Where we got lucky")
        sections.append("- ")
    sections.append("")

    # Action items
    sections.append("## Action Items\n")
    actions = incident.get('action_items', [])
    if actions:
        sections.append("| # | Action | Owner | Priority | Due | Status |")
        sections.append("|---|--------|-------|----------|-----|--------|")
        for i, a in enumerate(actions, 1):
            if isinstance(a, dict):
                sections.append(f"| {i} | {a.get('action', '')} | {a.get('owner', 'TBD')} | {a.get('priority', 'P2')} | {a.get('due', 'TBD')} | {a.get('status', 'Open')} |")
            else:
                sections.append(f"| {i} | {a} | TBD | P2 | TBD | Open |")
    else:
        sections.append("| # | Action | Owner | Priority | Due | Status |")
        sections.append("|---|--------|-------|----------|-----|--------|")
        sections.append("| 1 | _Add action items_ | TBD | P2 | TBD | Open |")
    sections.append("")

    # Appendix
    sections.append("---\n")
    sections.append("*This postmortem follows a blame-free format. The goal is to learn and improve systems, not assign blame.*")

    return '\n'.join(sections)

def generate_html(markdown_content, title):
    """Wrap markdown content in a simple HTML template."""
    # Simple markdown-to-HTML conversion for key elements
    html = markdown_content

    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Italic
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    # Code
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # Tables (simple conversion)
    def convert_table(match):
        lines = match.group(0).strip().split('\n')
        rows = []
        for i, line in enumerate(lines):
            if '---' in line:
                continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            tag = 'th' if i == 0 else 'td'
            row = ''.join(f'<{tag}>{c}</{tag}>' for c in cells)
            rows.append(f'<tr>{row}</tr>')
        return f'<table>{"".join(rows)}</table>'

    html = re.sub(r'(\|.+\|(?:\n\|.+\|)*)', convert_table, html)

    # Paragraphs (lines not already wrapped)
    lines = html.split('\n')
    processed = []
    for line in lines:
        if line.strip() and not line.strip().startswith('<') and not line.strip().startswith('*'):
            processed.append(f'<p>{line}</p>')
        else:
            processed.append(line)
    html = '\n'.join(processed)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Postmortem: {title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.6; }}
h1 {{ color: #dc2626; border-bottom: 2px solid #dc2626; padding-bottom: 10px; }}
h2 {{ color: #374151; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; margin-top: 32px; }}
h3 {{ color: #4b5563; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #d1d5db; padding: 8px 12px; text-align: left; }}
th {{ background: #f3f4f6; font-weight: 600; }}
tr:nth-child(even) td {{ background: #f9fafb; }}
code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
li {{ margin: 4px 0; }}
em {{ color: #6b7280; }}
hr {{ border: none; border-top: 2px solid #e5e7eb; margin: 32px 0; }}
</style>
</head>
<body>
{html}
</body>
</html>"""

def generate_json(incident, timeline_events=None, log_events=None):
    """Generate a JSON postmortem report."""
    report = {
        'title': incident.get('title', 'Untitled Incident'),
        'severity': incident.get('severity', 'P2'),
        'date': incident.get('date', datetime.now().strftime('%Y-%m-%d')),
        'duration': incident.get('duration', 'TBD'),
        'status': incident.get('status', 'Resolved'),
        'summary': incident.get('summary', ''),
        'impact': incident.get('impact', ''),
        'root_cause': incident.get('root_cause', ''),
        'detection': incident.get('detection', ''),
        'resolution': incident.get('resolution', ''),
        'timeline': [],
        'lessons_learned': incident.get('lessons_learned', []),
        'action_items': incident.get('action_items', []),
    }

    all_events = []
    if timeline_events:
        all_events.extend(timeline_events)
    if incident.get('timeline'):
        all_events.extend(incident['timeline'])
    report['timeline'] = sorted(all_events, key=lambda x: x.get('time') or x.get('timestamp') or '')

    if log_events:
        report['log_analysis'] = {
            'total_events': len(log_events),
            'by_severity': {},
            'top_categories': {},
            'key_errors': [e for e in log_events if e['severity'] in ('FATAL', 'ERROR')][:10],
        }
        for e in log_events:
            s = e['severity']
            report['log_analysis']['by_severity'][s] = report['log_analysis']['by_severity'].get(s, 0) + 1
            for c in e.get('categories', []):
                report['log_analysis']['top_categories'][c] = report['log_analysis']['top_categories'].get(c, 0) + 1

    return json.dumps(report, indent=2, default=str)

# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description='Generate structured incident postmortem reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --title "DB outage" --severity P1
  %(prog)s --title "API latency" --log /var/log/app.log --since 2h
  %(prog)s --from incident.json --output html
  %(prog)s --title "Deploy fail" --timeline events.json -o report.md
        """
    )

    parser.add_argument('--title', help='Incident title')
    parser.add_argument('--severity', choices=['P0', 'P1', 'P2', 'P3'], default='P2', help='Incident severity (default: P2)')
    parser.add_argument('--date', help='Incident date (default: today)')
    parser.add_argument('--duration', help='Incident duration')
    parser.add_argument('--summary', help='Brief summary')
    parser.add_argument('--impact', help='Impact description')
    parser.add_argument('--root-cause', help='Root cause description')
    parser.add_argument('--log', action='append', help='Log file(s) to parse for timeline events (repeatable)')
    parser.add_argument('--since', help='Time filter for log parsing (1h, 24h, 7d, or ISO date)')
    parser.add_argument('--timeline', help='Timeline JSON file')
    parser.add_argument('--from', dest='from_file', help='Load full incident from JSON file')
    parser.add_argument('--output', choices=['markdown', 'html', 'json', 'text'], default='markdown', help='Output format (default: markdown)')
    parser.add_argument('-o', '--out', help='Output file path (default: stdout)')
    parser.add_argument('--check-blame', help='Check a file for blameful language')
    parser.add_argument('--template', choices=['full', 'quick', 'minimal'], default='full', help='Template detail level (default: full)')

    args = parser.parse_args()

    # Blame language checker mode
    if args.check_blame:
        with open(args.check_blame) as f:
            text = f.read()
        issues = check_blame_language(text)
        if issues:
            print(f"Found {len(issues)} blameful language issue(s):\n")
            for line_num, match, suggestion in issues:
                print(f"  Line {line_num}: \"{match}\"")
                print(f"    -> {suggestion}\n")
            sys.exit(1)
        else:
            print("No blameful language detected.")
            sys.exit(0)

    # Build incident data
    if args.from_file:
        incident = load_incident_json(args.from_file)
    else:
        if not args.title:
            parser.error("--title is required (or use --from to load from JSON)")
        incident = {
            'title': args.title,
            'severity': args.severity,
            'date': args.date or datetime.now().strftime('%Y-%m-%d'),
            'duration': args.duration or 'TBD',
            'summary': args.summary or '',
            'impact': args.impact or '',
            'root_cause': args.root_cause or '',
        }

    # Parse logs
    log_events = []
    if args.log:
        since = parse_since(args.since)
        for log_path in args.log:
            log_events.extend(parse_log_file(log_path, since))
        log_events.sort(key=lambda x: x.get('timestamp') or '')

    # Load timeline
    timeline_events = []
    if args.timeline:
        timeline_events = load_timeline_json(args.timeline)

    # Generate report
    if args.output == 'json':
        report = generate_json(incident, timeline_events, log_events)
    elif args.output == 'html':
        md = generate_markdown(incident, timeline_events, log_events)
        report = generate_html(md, incident.get('title', 'Incident'))
    else:
        report = generate_markdown(incident, timeline_events, log_events)

    # Output
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"Report written to {args.out}", file=sys.stderr)
    else:
        print(report)

    # Exit code based on severity
    if incident.get('severity') in ('P0', 'P1'):
        sys.exit(2)
    elif log_events and any(e['severity'] == 'FATAL' for e in log_events):
        sys.exit(2)
    elif log_events and any(e['severity'] == 'ERROR' for e in log_events):
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
