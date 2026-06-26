---
name: datetime-tool
description: Comprehensive date and time manipulation toolkit supporting multiple formats, timezone conversions, calendar calculations, natural language parsing, and date arithmetic.
---

# DateTime Tool — Advanced Date/Time Operations

Full-featured datetime manipulation toolkit for format conversion, timezone handling, date arithmetic, and calendar calculations across ISO 8601, RFC 2822, Unix timestamps, and natural language inputs.

## Quick Start

```bash
# Current time in UTC
datetime-tool --now

# Parse and reformat
datetime-tool --parse "2026-01-15 14:30:00" --format "ISO"

# Timezone conversion
datetime-tool --convert "14:00 UTC" --to "Asia/Shanghai"
```

## Usage

```bash
datetime-tool [COMMAND] [INPUT] [OPTIONS]

Commands:
  --now              Show current date/time
  --parse INPUT      Parse date from string
  --convert INPUT    Convert between timezones
  --diff START END   Calculate interval between two dates
  --add INPUT N      Add time units to a date
  --sub INPUT N      Subtract time units from a date
  --calendar YEAR    Show calendar for a year/month

Options:
  --format FMT       Output format: ISO, RFC2822, Unix, or custom format string
  --from TZ          Source timezone (default: local)
  --to TZ            Target timezone
  --units            Output units for diff: seconds, minutes, hours, days
  --json             Output as structured JSON
```

## Examples

```bash
# Get current time in multiple formats
datetime-tool --now --format ISO
datetime-tool --now --format "January 2, 2006 at 3:04 PM"

# Parse and reformat
datetime-tool --parse "2026-01-15" --format "January 15, 2026"

# Convert between timezones
datetime-tool --convert "14:00 UTC" --to "Asia/Shanghai"
datetime-tool --convert "2026-01-15 09:00" --from "America/New_York" --to "Europe/London"

# Calculate date differences
datetime-tool --diff "2026-01-01" "2026-12-31" --units days

# Add/subtract time
datetime-tool --add "2026-01-01" --days 45
datetime-tool --sub "2026-03-01" --months 2

# Calendar view
datetime-tool --calendar 2026
datetime-tool --calendar 2026-03

# Machine-readable output
datetime-tool --parse "next Friday" --json
```

## Features

- **Parse from natural language:** "next Friday", "last day of month", "+2 weeks"
- **Timezone conversion:** Any IANA timezone (UTC, local, Asia/Shanghai, etc.)
- **Date arithmetic:** Add/subtract days, weeks, months, years
- **Interval calculation:** Precise duration between any two dates
- **Multiple output formats:** ISO 8601, RFC 2822, Unix timestamp, custom templates
- **Calendar display:** Month or year view with week numbers
- **JSON output:** Structured for pipeline consumption
- **ISO week numbers & day-of-year:** For scheduling and accounting
