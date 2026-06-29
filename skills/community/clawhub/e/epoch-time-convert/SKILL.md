---
name: epoch-time-convert
description: Convert between Unix epoch timestamps and human-readable datetimes, with timezone support and automatic unit detection (seconds/millis/micros/nanos). Use when a task involves reading or producing epoch timestamps, converting log timestamps to local time, computing the current epoch, or translating a date string into an epoch value.
---

# Epoch Time Convert

## Overview

Convert Unix epoch timestamps to ISO datetimes and back, in any IANA timezone. The bundled script auto-detects whether an epoch value is in seconds, milliseconds, microseconds, or nanoseconds.

## Quick Start

Run the script with one of three subcommands:

```bash
# Current time (UTC by default)
python3 scripts/epoch.py now --tz Asia/Shanghai

# Epoch -> ISO datetime (unit auto-detected)
python3 scripts/epoch.py to-human 1718000000 --tz UTC

# Datetime -> epoch seconds
python3 scripts/epoch.py to-epoch "2024-06-10 08:00:00" --tz Asia/Shanghai
```

## Commands

- `now [--tz TZ]` — print current epoch seconds, epoch millis, and ISO datetime.
- `to-human <EPOCH> [--tz TZ]` — convert an epoch value to an ISO datetime. Unit is auto-detected by magnitude (s / ms / µs / ns).
- `to-epoch "<DATETIME>" [--tz TZ]` — convert a datetime string to epoch seconds. Accepts `YYYY-MM-DD[ T]HH:MM[:SS]` and `YYYY-MM-DD`.

## Notes

- `--tz` accepts any IANA timezone name (e.g. `UTC`, `Asia/Shanghai`, `America/New_York`). Defaults to `UTC`.
- Timezone support uses the standard-library `zoneinfo` (Python 3.9+). On older runtimes, only `UTC` is available.
- For naive datetime input, the value is interpreted in the supplied `--tz`, not the machine's local time.
