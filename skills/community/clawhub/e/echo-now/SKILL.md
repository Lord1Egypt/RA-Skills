---
name: echo-now
description: Print the current UTC time and ISO date in a deterministic, copy-friendly format. Use when an agent or operator needs a stable timestamp string for logs, file names, notes, or manifests and wants a single reusable command instead of rewriting date formatting each time.
---

# echo-now

Echo a stable UTC timestamp and ISO date string.

## When to use

- A log entry, note, or manifest needs a UTC timestamp.
- A file name needs a date prefix (`YYYY-MM-DD`).
- Avoid re-deriving `date` formatting in shell each time.

## Prerequisites

- POSIX `date` available on `PATH`.

## Run

```bash
scripts/echo_now.sh
```

## Output shape

Two lines:

```
utc=<YYYY-MM-DDTHH:MM:SSZ>
date=<YYYY-MM-DD>
```

Use the `utc=` value for event timestamps and the `date=` value for date-only prefixes.
