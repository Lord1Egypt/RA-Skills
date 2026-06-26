---
name: epoch-time-converter
description: Convert between Unix epoch timestamps (seconds or milliseconds) and human-readable date strings in any IANA timezone. Use when the user provides a number that looks like a Unix timestamp (10 digits ≈ seconds, 13 digits ≈ milliseconds) and asks what time it is, or provides a date/time string and wants the corresponding epoch value. Triggers on phrases like "what time is 1700000000", "convert epoch", "unix timestamp to date", "to UTC", "to Asia/Shanghai", "epoch in milliseconds".
---

# Epoch Time Converter

## Overview

Two-way conversion between Unix epoch timestamps and human-readable datetimes, with explicit timezone handling. Backed by a single self-contained Python script that uses only the standard library (`datetime`, `zoneinfo`).

## Quick start

```bash
# Epoch seconds -> human time in a given timezone
python3 scripts/epoch.py to-date 1700000000 --tz Asia/Shanghai
# -> 2023-11-15 06:13:20 +08:00 (Asia/Shanghai)

# Epoch milliseconds -> human time
python3 scripts/epoch.py to-date 1700000000000 --unit ms --tz UTC

# Human time -> epoch seconds (input timezone is required)
python3 scripts/epoch.py to-epoch "2023-11-15 06:13:20" --tz Asia/Shanghai
# -> 1700000000

# Human time -> epoch milliseconds
python3 scripts/epoch.py to-epoch "2023-11-15T06:13:20" --tz Asia/Shanghai --unit ms
```

## Decision tree

1. Input is purely numeric → use `to-date`.
   - 10 digits → `--unit s` (default).
   - 13 digits → `--unit ms`.
2. Input looks like a date/time string → use `to-epoch` and require `--tz`.
3. If the user did not specify a timezone for `to-date`, default to UTC and explicitly tell them which timezone you used.

## Output format

Both subcommands print one line: `<value> (<context>)`. Always echo this raw output back to the user, then add a one-line plain-language summary.

## Edge cases to watch

- Bare numbers without a unit hint: prefer length-based detection (10 vs 13 digits) over guessing.
- Strings without timezone offsets (e.g. `2024-01-01 09:00`) are interpreted in the `--tz` value; do not silently fall back to system local time.
- Negative epoch values (pre-1970) are supported.

## Resources

### scripts/

- `epoch.py` — CLI implementing `to-date` and `to-epoch`. Pure stdlib; runs on any Python 3.9+.
