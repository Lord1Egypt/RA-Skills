#!/usr/bin/env python3
"""cronexplain — Parse and explain cron expressions. Zero dependencies."""
import sys, argparse
from datetime import datetime, timedelta

FIELDS = ["minute", "hour", "day_of_month", "month", "day_of_week"]
MONTHS = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
DAYS = {0:"Sun",1:"Mon",2:"Tue",3:"Wed",4:"Thu",5:"Fri",6:"Sat",7:"Sun"}

def parse_field(field, name, min_val, max_val):
    """Parse a cron field into a set of values."""
    values = set()
    for part in field.split(","):
        if "/" in part:
            range_part, step = part.split("/", 1)
            step = int(step)
            if range_part == "*":
                start, end = min_val, max_val
            elif "-" in range_part:
                start, end = map(int, range_part.split("-", 1))
            else:
                start, end = int(range_part), max_val
            values.update(range(start, end + 1, step))
        elif "-" in part:
            start, end = map(int, part.split("-", 1))
            values.update(range(start, end + 1))
        elif part == "*":
            values.update(range(min_val, max_val + 1))
        else:
            values.add(int(part))
    return sorted(values)

def explain_field(field, name, min_val, max_val):
    """Generate human-readable explanation of a cron field."""
    if field == "*":
        return f"every {name}"
    if "/" in field and field.startswith("*/"):
        step = field.split("/")[1]
        return f"every {step} {name}s"
    vals = parse_field(field, name, min_val, max_val)
    if name == "month":
        return ", ".join(MONTHS.get(v, str(v)) for v in vals)
    if name == "day_of_week":
        return ", ".join(DAYS.get(v, str(v)) for v in vals)
    if name == "minute" and len(vals) == 1:
        return f"at minute {vals[0]}"
    if name == "hour" and len(vals) == 1:
        return f"at {vals[0]:02d}:00"
    return ", ".join(str(v) for v in vals)

def explain(expr):
    """Explain a cron expression in plain English."""
    parts = expr.strip().split()
    if len(parts) != 5:
        return f"Error: expected 5 fields, got {len(parts)}"
    
    minute, hour, dom, month, dow = parts
    pieces = []
    
    # Special patterns
    if expr == "* * * * *":
        return "Every minute"
    if expr == "0 * * * *":
        return "Every hour, at minute 0"
    if minute != "*" and hour != "*" and dom == "*" and month == "*" and dow == "*":
        mins = parse_field(minute, "minute", 0, 59)
        hrs = parse_field(hour, "hour", 0, 23)
        times = [f"{h:02d}:{m:02d}" for h in hrs for m in mins]
        return f"Every day at {', '.join(times)}"
    
    if minute != "*":
        pieces.append(explain_field(minute, "minute", 0, 59))
    if hour != "*":
        pieces.append(explain_field(hour, "hour", 0, 23))
    if dom != "*":
        pieces.append(f"on day {explain_field(dom, 'day_of_month', 1, 31)} of the month")
    if month != "*":
        pieces.append(f"in {explain_field(month, 'month', 1, 12)}")
    if dow != "*":
        pieces.append(f"on {explain_field(dow, 'day_of_week', 0, 7)}")
    
    return "; ".join(pieces) if pieces else "Every minute"

def next_runs(expr, count=5):
    """Calculate next N run times (approximate)."""
    parts = expr.strip().split()
    if len(parts) != 5:
        return []
    mins = parse_field(parts[0], "min", 0, 59)
    hrs = parse_field(parts[1], "hour", 0, 23)
    doms = parse_field(parts[2], "dom", 1, 31)
    mons = parse_field(parts[3], "month", 1, 12)
    dows = parse_field(parts[4], "dow", 0, 7)
    # Normalize Sunday
    if 7 in dows:
        dows = sorted(set(dows) | {0})
    
    now = datetime.now()
    runs = []
    dt = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
    attempts = 0
    while len(runs) < count and attempts < 525960:  # ~1 year of minutes
        if (dt.minute in mins and dt.hour in hrs and dt.month in mons
            and (dt.day in doms or dt.weekday() in [(d - 1) % 7 for d in dows if d != 0] or (0 in dows and dt.weekday() == 6))):
            # Simpler dow check
            py_dow = (dt.isoweekday() % 7)  # Sun=0
            if parts[2] == "*" and parts[4] != "*":
                if py_dow in dows:
                    runs.append(dt)
            elif parts[4] == "*" and parts[2] != "*":
                if dt.day in doms:
                    runs.append(dt)
            else:
                runs.append(dt)
        dt += timedelta(minutes=1)
        attempts += 1
    return runs

def main():
    p = argparse.ArgumentParser(prog="cronexplain", description="Explain cron expressions")
    p.add_argument("expression", nargs="+", help="Cron expression (5 fields)")
    p.add_argument("-n", "--next", type=int, default=0, help="Show next N run times")
    args = p.parse_args()
    
    expr = " ".join(args.expression)
    print(f"📅 {expr}")
    print(f"   → {explain(expr)}")
    
    if args.next > 0:
        runs = next_runs(expr, args.next)
        if runs:
            print(f"\n   Next {len(runs)} runs:")
            for r in runs:
                print(f"   • {r.strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
