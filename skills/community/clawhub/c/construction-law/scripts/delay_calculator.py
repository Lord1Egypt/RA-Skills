#!/usr/bin/env python3
"""
Delay Analysis Calculator
Input delay events with dates and get critical path impact analysis.

Usage:
    python3 delay_calculator.py --baseline-start 2026-05-11 --baseline-end 2030-05-10 --events events.json
    python3 delay_calculator.py --baseline-start 2026-05-11 --baseline-end 2030-05-10 --interactive
    python3 delay_calculator.py --baseline-start 2026-05-11 --baseline-end 2030-05-10 --add "Late access|2026-06-01|2026-06-30|employer|critical" --add "Weather|2026-07-15|2026-07-25|neutral|critical"
"""

import argparse
import csv as csv_module
import json
import sys
import warnings
from datetime import datetime, timedelta

def parse_date(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d")

def days_between(d1, d2):
    return (d2 - d1).days

def analyse_delays(baseline_start, baseline_end, events, fmt="md", output=None):
    baseline_duration = days_between(baseline_start, baseline_end)
    
    # Sort events by start date
    events.sort(key=lambda e: e["start"])
    
    # Calculate total delays by responsibility
    employer_delay = 0
    contractor_delay = 0
    neutral_delay = 0
    concurrent_days = 0
    
    # Track occupied delay periods for concurrency detection
    employer_periods = []
    contractor_periods = []
    
    for e in events:
        duration = days_between(e["start"], e["end"])
        e["duration"] = duration
        
        if e["responsibility"] == "employer":
            employer_delay += duration
            employer_periods.append((e["start"], e["end"]))
        elif e["responsibility"] == "contractor":
            contractor_delay += duration
            contractor_periods.append((e["start"], e["end"]))
        elif e["responsibility"] == "neutral":
            neutral_delay += duration
    
    # Detect concurrent delay (overlapping employer + contractor periods)
    for ep_start, ep_end in employer_periods:
        for cp_start, cp_end in contractor_periods:
            overlap_start = max(ep_start, cp_start)
            overlap_end = min(ep_end, cp_end)
            if overlap_start < overlap_end:
                concurrent_days += days_between(overlap_start, overlap_end)
    
    # Calculate net delay (simple impacted method)
    total_critical_delay = sum(e["duration"] for e in events if e.get("critical", True))
    total_non_critical = sum(e["duration"] for e in events if not e.get("critical", True))
    
    # EOT entitlement (employer + neutral delays on critical path, minus concurrency)
    eot_entitlement = sum(e["duration"] for e in events 
                         if e["responsibility"] in ("employer", "neutral") and e.get("critical", True))
    
    # Projected completion
    projected_end = baseline_end + timedelta(days=total_critical_delay)
    eot_completion = baseline_end + timedelta(days=eot_entitlement)
    
    # Exposure analysis
    ld_exposure_days = max(0, total_critical_delay - eot_entitlement)
    
    if fmt == "md":
        lines = [
            "# Delay Analysis Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "---",
            "",
            "## Contract Dates",
            "",
            f"| Item | Date | Days |",
            f"|------|------|------|",
            f"| Baseline Start | {baseline_start.strftime('%d %b %Y')} | — |",
            f"| Baseline Completion | {baseline_end.strftime('%d %b %Y')} | {baseline_duration} days |",
            f"| Projected Completion | {projected_end.strftime('%d %b %Y')} | {baseline_duration + total_critical_delay} days |",
            f"| Completion with EOT | {eot_completion.strftime('%d %b %Y')} | {baseline_duration + eot_entitlement} days |",
            "",
            "## Delay Events",
            "",
            "| # | Event | Start | End | Duration | Responsibility | Critical? |",
            "|---|-------|-------|-----|----------|---------------|-----------|",
        ]
        
        for i, e in enumerate(events, 1):
            critical = "✅ Yes" if e.get("critical", True) else "❌ No"
            lines.append(f"| {i} | {e['description']} | {e['start'].strftime('%d %b %Y')} | {e['end'].strftime('%d %b %Y')} | {e['duration']} days | {e['responsibility'].title()} | {critical} |")
        
        lines.extend([
            "",
            "## Delay Summary",
            "",
            "| Category | Days |",
            "|----------|------|",
            f"| Employer-caused delay (critical) | {sum(e['duration'] for e in events if e['responsibility']=='employer' and e.get('critical',True))} days |",
            f"| Contractor-caused delay (critical) | {sum(e['duration'] for e in events if e['responsibility']=='contractor' and e.get('critical',True))} days |",
            f"| Neutral delay (critical) | {sum(e['duration'] for e in events if e['responsibility']=='neutral' and e.get('critical',True))} days |",
            f"| Non-critical delay (all) | {total_non_critical} days |",
            f"| Concurrent delay detected | {concurrent_days} days |",
            f"| **Total critical delay** | **{total_critical_delay} days** |",
            "",
            "## EOT & LD Analysis",
            "",
            "| Item | Value |",
            "|------|-------|",
            f"| EOT Entitlement (employer + neutral, critical) | **{eot_entitlement} days** |",
            f"| Contractor's own delay (critical) | {sum(e['duration'] for e in events if e['responsibility']=='contractor' and e.get('critical',True))} days |",
            f"| LD Exposure (delay beyond EOT) | **{ld_exposure_days} days** |",
            f"| Concurrent delay | {concurrent_days} days |",
            "",
            "## Concurrency Note",
            "",
        ])
        
        if concurrent_days > 0:
            lines.extend([
                f"⚠️ **{concurrent_days} days of concurrent delay detected** — employer and contractor delays overlap.",
                "",
                "**Treatment depends on jurisdiction:**",
                "- **Malmaison (England)**: Contractor gets EOT but no prolongation costs for concurrent period",
                "- **Singapore**: Apportionment approach — SO/Architect may grant partial EOT",
                "- **SCL Protocol**: If true concurrency, EOT granted but costs not recoverable",
                "",
            ])
        else:
            lines.append("No concurrent delay detected.")
            lines.append("")
        
        lines.extend([
            "## Recommendations",
            "",
            "1. **Preserve notices** — ensure all delay events have been properly notified under the contract",
            "2. **Update programme** — submit revised programme showing delay impact",
            "3. **Maintain records** — daily site diaries, progress photos, resource records",
            "4. **Quantify costs** — prepare prolongation cost calculation for EOT period",
            "5. **Mitigate** — document all mitigation measures taken",
            "",
            "---",
            "",
            "⚠️ **Disclaimer**: This is a simplified impacted as-planned analysis. For complex disputes, a Time Impact Analysis (TIA) or Windows Analysis by a delay expert is recommended.",
            "",
            f"*Generated by Construction Law Skill v2.8.1*",
        ])
        
        result = "\n".join(lines)
        if output:
            with open(output, 'w') as f:
                f.write(result)
            print(f"Report written to {output}")
        else:
            print(result)

    elif fmt == "csv":
        import csv
        out = open(output, 'w', newline='') if output else sys.stdout
        writer = csv.writer(out)
        writer.writerow(["Delay Analysis Report"])
        writer.writerow(["Baseline Start", baseline_start.strftime('%Y-%m-%d')])
        writer.writerow(["Baseline Completion", baseline_end.strftime('%Y-%m-%d')])
        writer.writerow(["Baseline Duration", f"{baseline_duration} days"])
        writer.writerow(["Projected Completion", projected_end.strftime('%Y-%m-%d')])
        writer.writerow(["EOT Entitlement", f"{eot_entitlement} days"])
        writer.writerow(["LD Exposure", f"{ld_exposure_days} days"])
        writer.writerow([])
        writer.writerow(["#", "Event", "Start", "End", "Duration", "Responsibility", "Critical"])
        for i, e in enumerate(events, 1):
            writer.writerow([i, e['description'], e['start'].strftime('%Y-%m-%d'),
                           e['end'].strftime('%Y-%m-%d'), e['duration'],
                           e['responsibility'], "Yes" if e.get('critical', True) else "No"])
        if output:
            out.close()
            print(f"CSV written to {output}")

    elif fmt == "json":
        result = {
            "baseline": {"start": baseline_start.strftime('%Y-%m-%d'), "end": baseline_end.strftime('%Y-%m-%d'), "duration": baseline_duration},
            "projected_completion": projected_end.strftime('%Y-%m-%d'),
            "eot_completion": eot_completion.strftime('%Y-%m-%d'),
            "eot_entitlement_days": eot_entitlement,
            "ld_exposure_days": ld_exposure_days,
            "concurrent_delay_days": concurrent_days,
            "total_critical_delay": total_critical_delay,
            "events": [{"description": e["description"], "start": e["start"].strftime('%Y-%m-%d'),
                        "end": e["end"].strftime('%Y-%m-%d'), "duration": e["duration"],
                        "responsibility": e["responsibility"], "critical": e.get("critical", True)}
                       for e in events]
        }
        output_str = json.dumps(result, indent=2)
        if output:
            with open(output, 'w') as f:
                f.write(output_str)
            print(f"JSON written to {output}")
        else:
            print(output_str)

def _parse_criticality(value):
    """Parse criticality string to boolean. Accepts 'critical', 'non-critical', 'yes', 'no', 'true', 'false'."""
    return value.strip().lower() not in ("non-critical", "no", "false", "0")


def main():
    parser = argparse.ArgumentParser(
        description="Delay Analysis Calculator",
        epilog="""Examples:
  # Structured event (recommended):
  %(prog)s --baseline-start 2026-05-11 --baseline-end 2030-05-10 \\
    --add-event "Late access" 2026-06-01 2026-06-30 employer critical

  # Events from CSV file:
  %(prog)s --baseline-start 2026-05-11 --baseline-end 2030-05-10 \\
    --events-csv events.csv

  # Legacy pipe-delimited (deprecated):
  %(prog)s --baseline-start 2026-05-11 --baseline-end 2030-05-10 \\
    --add "Late access|2026-06-01|2026-06-30|employer|critical"
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--baseline-start", required=True, help="Baseline start date (YYYY-MM-DD)")
    parser.add_argument("--baseline-end", required=True, help="Baseline completion date (YYYY-MM-DD)")
    parser.add_argument("--events", help="JSON file with delay events")
    parser.add_argument(
        "--add", action="append", metavar="'desc|start|end|cause|criticality'",
        help="(DEPRECATED — use --add-event or --events-csv) Add event as pipe-delimited string: "
             "'description|start_date|end_date|responsibility|critical/non-critical'. "
             "Field values must NOT contain pipe characters."
    )
    parser.add_argument(
        "--add-event", action="append", nargs=5,
        metavar=("DESCRIPTION", "START", "END", "CAUSE", "CRITICALITY"),
        help="Add a structured delay event (repeatable). "
             "CAUSE: employer|contractor|neutral. "
             "CRITICALITY: critical|non-critical."
    )
    parser.add_argument(
        "--events-csv",
        help="CSV file with columns: description, start_date, end_date, cause, criticality"
    )
    parser.add_argument("--format", default="md", choices=["md", "csv", "json"])
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    bs = parse_date(args.baseline_start)
    be = parse_date(args.baseline_end)
    events = []

    if args.events:
        with open(args.events) as f:
            raw = json.load(f)
        for e in raw:
            events.append({
                "description": e["description"],
                "start": parse_date(e["start"]),
                "end": parse_date(e["end"]),
                "responsibility": e.get("responsibility", "employer"),
                "critical": e.get("critical", True)
            })

    # --add (legacy pipe-delimited, deprecated)
    if args.add:
        warnings.warn(
            "--add is deprecated and will be removed in v3.0. "
            "Use --add-event or --events-csv instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        for a in args.add:
            parts = a.split("|")
            if len(parts) > 5:
                print(
                    f"Error: --add value has {len(parts)} pipe-separated fields (expected 4-5).\n"
                    f"  If a field contains a pipe character, use --add-event or --events-csv instead.\n"
                    f"  Example: --add-event \"Late access\" 2026-06-01 2026-06-30 employer critical",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(parts) < 4:
                print(f"Error: --add format is 'description|start|end|responsibility[|critical]'")
                sys.exit(1)
            events.append({
                "description": parts[0].strip(),
                "start": parse_date(parts[1]),
                "end": parse_date(parts[2]),
                "responsibility": parts[3].strip().lower(),
                "critical": _parse_criticality(parts[4]) if len(parts) > 4 else True
            })

    # --add-event (structured, recommended)
    if args.add_event:
        for ev in args.add_event:
            desc, start, end, cause, crit = ev
            events.append({
                "description": desc,
                "start": parse_date(start),
                "end": parse_date(end),
                "responsibility": cause.strip().lower(),
                "critical": _parse_criticality(crit)
            })

    # --events-csv
    if args.events_csv:
        with open(args.events_csv, newline='') as csvfile:
            reader = csv_module.DictReader(csvfile)
            for row in reader:
                events.append({
                    "description": row["description"].strip(),
                    "start": parse_date(row["start_date"]),
                    "end": parse_date(row["end_date"]),
                    "responsibility": row["cause"].strip().lower(),
                    "critical": _parse_criticality(row["criticality"])
                })

    if not events:
        print("Error: No events provided. Use --events, --add-event, or --events-csv")
        sys.exit(1)

    analyse_delays(bs, be, events, args.format, args.output)

if __name__ == "__main__":
    main()
