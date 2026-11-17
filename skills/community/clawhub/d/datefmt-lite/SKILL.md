---
name: datefmt-lite
description: Convert and format dates/times with zero external APIs — ISO 8601, Unix epoch, RFC 2822, and timezone conversion using only the local `date` binary and TZ database. Use when you need quick timestamp formatting, epoch conversion, duration arithmetic, or "what time is it in <city>" math without network calls.
metadata:
  license: MIT
---

# datefmt-lite

Small, dependency-free toolkit for turning one timestamp format into another.
Everything runs locally through GNU coreutils `date` and the TZ database
(`/usr/share/zoneinfo`). No curl, no API keys, no network.

## When to use

- Convert between ISO 8601 ↔ Unix epoch ↔ RFC 2822
- "What time is 2026-09-06 08:28 GMT+8 in UTC / Los Angeles?"
- Add or subtract durations from a date
- Sanity-check cron expressions against real weekdays
- Any shell environment where installing a library is overkill

## Prerequisites

- GNU coreutils `date` (Linux default; macOS: `brew install coreutils`,
  use `gdate` or prefix commands with `g`).
- TZ database present (`ls /usr/share/zoneinfo` should list regions).

## Core recipes

### 1. Now in common formats

```bash
date +%s                       # Unix epoch seconds (handy for logs)
date -u +"%Y-%m-%dT%H:%M:%SZ"  # ISO 8601 UTC (sortable, unambiguous)
date -R                        # RFC 2822 (email/HTTP headers)
```

### 2. Parse "ISO string → epoch"

```bash
date -u -d "2026-09-06T08:28:00+08:00" +%s      # → 1788654480 (GNU date)
# Reading an epoch back into a human form:
date -u -d "@1788654480"                        # → Sun Sep  6 00:28:00 UTC 2026
```

### 3. Timezone conversion without computing offsets yourself

Pick any zone name from `timedatectl list-timezones` or `/usr/share/zoneinfo`.

```bash
# "2026-09-06 08:28 GMT+8" expressed in three other zones:
TZ=America/Los_Angeles date -d "2026-09-06 08:28 +0800"
# Sat Sep  5 17:28:00 PDT 2026
TZ=Europe/Berlin         date -d "2026-09-06 08:28 +0800"
TZ=Australia/Sydney      date -d "2026-09-06 08:28 +0800"
```

The trick: `TZ=... date` re-renders the *same instant* in the target zone,
so you never add/subtract offsets by hand (DST handled automatically).

### 4. Duration arithmetic

```bash
date -d "2026-09-06 + 45 days" +%F          # add 45 days  → 2026-10-21
date -d "2026-09-06 08:28 - 3 hours" +%s    # subtract 3h → epoch
echo $(( $(date -d "2026-10-01" +%s) - $(date -d "2026-09-06" +%s) ))
# seconds between two dates (divide by 86400 for days)
```

### 5. Cron-expression sanity check

Before scheduling `30 2 * * 1-5`, confirm the weekday names for the run dates:

```bash
for d in 2026-09-07 2026-09-08 2026-09-12; do
  echo "$d -> $(date -d "$d" +%A) $([ "$(date -d "$d" +%u)" -le 5 ] && echo weekday || echo Weekend)"
done
```

## Common mistakes to avoid

- **Writing `TZ=Asia/Shanghai date` instead of converting a moment.**
  That renders *now*, not a timestamp you were holding. Use `date -d "<ts>"`.
- Forgetting `-u` when logging. Local-zone strings in logs sort wrong
  across DST boundaries and confuse anyone not in your zone.
- Relying on `%F` alone — always include zone or epoch when persisting.

## Verification one-liner

Round-trip check that your toolchain parses what it emits:

```bash
e=$(date +%s); iso=$(date -u -d "@$e" +"%Y-%m-%dT%H:%M:%SZ"); \
  back=$(date -u -d "$iso" +%s); [ "$e" = "$back" ] && echo "OK"
```

If this prints `OK`, your `date` build handles ISO 8601 correctly.
