# /// script
# dependencies = ["rich", "croniter"]
# ///

"""
cron-helper: Explain, generate, validate, and preview cron expressions.
Usage:
  cron.py explain "<expr>"
  cron.py generate "<plain English>"
  cron.py next "<expr>" [--count N]
  cron.py validate "<expr>"
"""

import sys
import re
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    from croniter import croniter, CroniterBadCronError
except ImportError:
    print("Missing dependencies. Run with: uv run scripts/cron.py")
    sys.exit(1)

console = Console()

# ---------------------------------------------------------------------------
# Field metadata
# ---------------------------------------------------------------------------
FIELDS = ["Minute", "Hour", "Day", "Month", "Weekday"]
FIELD_RANGES = {
    "Minute": (0, 59),
    "Hour": (0, 23),
    "Day": (1, 31),
    "Month": (1, 12),
    "Weekday": (0, 7),
}
MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}
DAY_NAMES = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday",
}


# ---------------------------------------------------------------------------
# explain helpers
# ---------------------------------------------------------------------------

def _explain_field(name, value):
    """Return a human-readable description for a single cron field."""
    if value == "*":
        return f"every {name.lower()}"

    # Step value: */N or base/N
    step_match = re.fullmatch(r"(\*|\d+)/(\d+)", value)
    if step_match:
        base, step = step_match.group(1), int(step_match.group(2))
        if name == "Minute":
            return f"every {step} minute{'s' if step > 1 else ''}"
        if name == "Hour":
            return f"every {step} hour{'s' if step > 1 else ''}"
        return f"every {step} {name.lower()}{'s' if step > 1 else ''}"

    # Range: N-M
    range_match = re.fullmatch(r"(\d+)-(\d+)", value)
    if range_match:
        lo, hi = int(range_match.group(1)), int(range_match.group(2))
        if name == "Weekday":
            return f"{DAY_NAMES.get(lo, lo)} through {DAY_NAMES.get(hi, hi)}"
        if name == "Month":
            return f"{MONTH_NAMES.get(lo, lo)} through {MONTH_NAMES.get(hi, hi)}"
        return f"{lo} through {hi}"

    # List: N,M,...
    if "," in value:
        parts = value.split(",")
        if name == "Weekday":
            return ", ".join(DAY_NAMES.get(int(p), p) for p in parts)
        if name == "Month":
            return ", ".join(MONTH_NAMES.get(int(p), p) for p in parts)
        return f"at {', '.join(parts)}"

    # Single value
    v = int(value)
    if name == "Minute":
        return f"at minute {v}"
    if name == "Hour":
        suffix = "AM" if v < 12 else "PM"
        hr = v if v <= 12 else v - 12
        hr = 12 if hr == 0 else hr
        return f"at {hr} {suffix}"
    if name == "Weekday":
        return DAY_NAMES.get(v, str(v))
    if name == "Month":
        return MONTH_NAMES.get(v, str(v))
    return f"{value}"


def _build_summary(parts):
    minute, hour, day, month, weekday = parts
    time_str = ""
    if re.fullmatch(r"\d+", minute) and re.fullmatch(r"\d+", hour):
        h, m = int(hour), int(minute)
        suffix = "AM" if h < 12 else "PM"
        hr = h % 12 or 12
        time_str = f"at {hr}:{m:02d} {suffix}"
    elif minute == "0" and hour == "*":
        time_str = "at the top of every hour"
    elif re.fullmatch(r"\*/\d+", minute):
        step = minute.split("/")[1]
        time_str = f"every {step} minute{'s' if step != '1' else ''}"
    elif re.fullmatch(r"\*/\d+", hour) and minute == "0":
        step = hour.split("/")[1]
        time_str = f"every {step} hour{'s' if step != '1' else ''}"

    day_str = ""
    if weekday != "*" and day == "*":
        day_str = f", {_explain_field('Weekday', weekday)}"
    elif day != "*" and weekday == "*":
        day_str = f", on day {day} of the month"
    elif day == "*" and weekday == "*":
        day_str = ", every day"

    month_str = ""
    if month != "*":
        month_str = f" in {_explain_field('Month', month)}"

    return f"{time_str}{day_str}{month_str}".strip(", ")


def cmd_explain(expr):
    parts = expr.strip().split()
    if len(parts) != 5:
        console.print(f"[red]Expected 5 fields, got {len(parts)}. Use standard 5-field cron.[/red]")
        sys.exit(1)

    summary = _build_summary(parts)

    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value", style="yellow")
    table.add_column("Meaning")

    for name, value in zip(FIELDS, parts):
        table.add_row(name, value, _explain_field(name, value))

    panel = Panel(
        f"[bold]{expr}[/bold]\n[green]{summary}[/green]",
        title="⏰ Cron Expression",
        border_style="blue",
    )
    console.print(panel)
    console.print(table)


# ---------------------------------------------------------------------------
# generate
# ---------------------------------------------------------------------------

GENERATE_RULES = [
    # every N minutes
    (r"every (\d+) minutes?", lambda m: f"*/{m.group(1)} * * * *"),
    # every minute
    (r"every minute", lambda m: "* * * * *"),
    # every N hours
    (r"every (\d+) hours?", lambda m: f"0 */{m.group(1)} * * *"),
    # every hour
    (r"every hour", lambda m: "0 * * * *"),
    # every weekday at Xam/pm
    (r"every weekday at (\d+)\s*(am|pm)?", lambda m: _at_time(m, "1-5")),
    # every weekend at X
    (r"every weekend at (\d+)\s*(am|pm)?", lambda m: _at_time(m, "6,0")),
    # every monday/tuesday/... at X
    (r"every (monday|tuesday|wednesday|thursday|friday|saturday|sunday) at (\d+)\s*(am|pm)?",
     lambda m: _weekday_at(m)),
    # every day at X
    (r"every day at (\d+)\s*(am|pm)?", lambda m: _at_time(m, "*")),
    # daily at X
    (r"daily at (\d+)\s*(am|pm)?", lambda m: _at_time(m, "*")),
    # midnight
    (r"(every day at )?midnight", lambda m: "0 0 * * *"),
    # noon
    (r"(every day at )?noon", lambda m: "0 12 * * *"),
    # first day of month
    (r"(first|1st) day of (the )?month", lambda m: "0 0 1 * *"),
    # last day — approximation
    (r"last day of (the )?month", lambda m: "0 0 28-31 * *"),
    # every week on monday
    (r"every week(ly)? on (monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
     lambda m: _weekly_on(m)),
]

WEEKDAY_MAP = {
    "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4,
    "friday": 5, "saturday": 6, "sunday": 0,
}


def _hour_value(hour_str, ampm):
    h = int(hour_str)
    if ampm == "pm" and h != 12:
        h += 12
    if ampm == "am" and h == 12:
        h = 0
    return h


def _at_time(m, weekday_field):
    groups = m.groups()
    hour = _hour_value(groups[0], groups[1] if len(groups) > 1 else None)
    return f"0 {hour} * * {weekday_field}"


def _weekday_at(m):
    day_name = m.group(1).lower()
    hour = _hour_value(m.group(2), m.group(3))
    dow = WEEKDAY_MAP.get(day_name, "*")
    return f"0 {hour} * * {dow}"


def _weekly_on(m):
    day_name = m.group(2).lower()
    dow = WEEKDAY_MAP.get(day_name, "*")
    return f"0 9 * * {dow}"


def cmd_generate(description):
    desc = description.strip().lower()
    for pattern, handler in GENERATE_RULES:
        match = re.search(pattern, desc)
        if match:
            result = handler(match)
            console.print(Panel(
                f"[bold yellow]{result}[/bold yellow]",
                title=f"⏰ Cron for: {description}",
                border_style="green",
            ))
            # Also show what it means
            cmd_explain(result)
            return

    console.print(f"[yellow]Could not parse: [bold]{description}[/bold][/yellow]")
    console.print("[dim]Try phrases like: 'every 15 minutes', 'every weekday at 9am', 'every day at midnight'[/dim]")
    sys.exit(1)


# ---------------------------------------------------------------------------
# next
# ---------------------------------------------------------------------------

def cmd_next(expr, count=5):
    try:
        cron = croniter(expr, datetime.now())
    except (CroniterBadCronError, ValueError) as e:
        console.print(f"[red]Invalid cron expression: {e}[/red]")
        sys.exit(1)

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Date & Time", style="bold green")
    table.add_column("Day", style="yellow")

    for i in range(count):
        nxt = cron.get_next(datetime)
        table.add_row(str(i + 1), nxt.strftime("%Y-%m-%d %H:%M:%S"), nxt.strftime("%A"))

    console.print(Panel(
        f"[bold]{expr}[/bold]",
        title=f"⏰ Next {count} runs",
        border_style="blue",
    ))
    console.print(table)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------

def cmd_validate(expr):
    parts = expr.strip().split()
    if len(parts) != 5:
        console.print(f"[red]✗ Expected 5 fields, got {len(parts)}.[/red]")
        sys.exit(1)

    warnings = []
    errors = []

    for name, value, (lo, hi) in zip(FIELDS, parts, FIELD_RANGES.values()):
        if value == "*":
            continue
        # Extract all numeric values for range checking
        nums = re.findall(r"\d+", value)
        for n in nums:
            n = int(n)
            if n < lo or n > hi:
                errors.append(f"{name}: {n} is out of range ({lo}–{hi})")

    # Specific common-mistake warnings
    minute_nums = re.findall(r"\d+", parts[0])
    if any(int(n) == 60 for n in minute_nums):
        warnings.append("Minute field contains 60 — valid range is 0–59. Did you mean 0?")

    hour_nums = re.findall(r"\d+", parts[1])
    if any(int(n) == 24 for n in hour_nums):
        warnings.append("Hour field contains 24 — valid range is 0–23. Did you mean 0 (midnight)?")

    # Feb 30 — never runs
    if parts[2] in ("30", "31") and parts[3] == "2":
        warnings.append("February never has day 30 or 31 — this expression will never run.")

    # Try croniter parse
    try:
        croniter(expr)
        valid = True
    except (CroniterBadCronError, ValueError) as e:
        errors.append(str(e))
        valid = False

    if not errors and not warnings:
        console.print(Panel(
            f"[bold green]✓ Valid[/bold green]  [dim]{expr}[/dim]",
            title="⏰ Cron Validation",
            border_style="green",
        ))
    else:
        lines = []
        for e in errors:
            lines.append(f"[red]✗ {e}[/red]")
        for w in warnings:
            lines.append(f"[yellow]⚠ {w}[/yellow]")
        status = "[red]✗ Invalid[/red]" if errors else "[yellow]⚠ Valid with warnings[/yellow]"
        console.print(Panel(
            f"{status}  [dim]{expr}[/dim]\n" + "\n".join(lines),
            title="⏰ Cron Validation",
            border_style="red" if errors else "yellow",
        ))
        if errors:
            sys.exit(1)


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    if not args:
        console.print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "explain":
        if len(args) < 2:
            console.print("[red]Usage: cron.py explain \"<expr>\"[/red]")
            sys.exit(1)
        cmd_explain(args[1])

    elif cmd == "generate":
        if len(args) < 2:
            console.print("[red]Usage: cron.py generate \"<description>\"[/red]")
            sys.exit(1)
        cmd_generate(args[1])

    elif cmd == "next":
        if len(args) < 2:
            console.print("[red]Usage: cron.py next \"<expr>\" [--count N][/red]")
            sys.exit(1)
        count = 5
        if "--count" in args:
            idx = args.index("--count")
            count = int(args[idx + 1])
        cmd_next(args[1], count)

    elif cmd == "validate":
        if len(args) < 2:
            console.print("[red]Usage: cron.py validate \"<expr>\"[/red]")
            sys.exit(1)
        cmd_validate(args[1])

    else:
        console.print(f"[red]Unknown command: {cmd}[/red]")
        console.print("Commands: explain, generate, next, validate")
        sys.exit(1)


if __name__ == "__main__":
    main()
