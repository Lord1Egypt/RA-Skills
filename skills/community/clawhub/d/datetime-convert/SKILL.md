---
name: datetime-convert
description: Convert any time representation — unix timestamps (s/ms/us/ns), ISO 8601/RFC 3339/RFC 2822, strftime, spreadsheet serials, IANA timezones, natural language ("3 days ago"/"下周一"), date arithmetic, durations. Use for bare epoch numbers, timezone/format conversion, 时间戳转北京时间, or a whole time column.
---

# Datetime conversion

Time math done by hand is where quiet mistakes come from: milliseconds read as seconds,
a timezone offset applied the wrong way, DST ignored, a leap year forgotten. The bundled
script removes all of that guesswork — run it and report what it says instead of
computing in your head.

## Usage

```bash
python3 scripts/dtconv.py [INPUT ...] [-z TZ] [--in-tz TZ] [-f FORMAT] [-u UNIT] [--add DELTA] [--diff OTHER] [--json]
```

Path is relative to this skill directory; use the absolute path when running from elsewhere.
Standard library only. Python 3.9+ gets everything; on 3.7/3.8 the single casualty is IANA
zone names (`Asia/Shanghai`), because `zoneinfo` does not exist there — the script says so
and points at `UTC` / `local` / `+08:00`, and every other feature keeps working. Same story
if `zoneinfo` exists but the tz database is missing (minimal containers, Windows): the error
names the fix (`pip install tzdata`).

With no `-f`, the script prints a full report (epoch seconds and millis, UTC, local wall
clock, ISO 8601, RFC 2822, weekday/ISO week/day-of-year, and a human "2 days ago").
When the user asked for one specific thing, pass `-f` and give them that single value.

- `-z, --tz` — output timezone: `Asia/Shanghai`, `UTC`, `+08:00`, `local` (default `local`)
- `--in-tz` — timezone assumed for input that has no offset (default `local`). Epoch numbers
  are absolute instants, so this does not affect them.
- `-f, --format` — named format or any strftime pattern. Named: `iso`, `rfc3339`, `rfc2822`,
  `http`, `unix`, `unix_ms`, `unix_us`, `unix_ns`, `date`, `time`, `datetime`, `sql`,
  `compact`, `cn`
- `-u, --unit` — force `s|ms|us|ns` for numeric input instead of auto-detecting, or `excel`
  to read spreadsheet serial numbers (`45900` → 2025-08-31)
- `--add` — shift the result: `+3d`, `-2h30m`, `1 month`, `1年2个月`
- `--diff` — duration from input to another moment
- `--json` — machine-readable output, useful when feeding another script

Multiple inputs are converted in one call, one line of output each — prefer that over
looping the script. For a whole column or file, pass the values as arguments
(`xargs` works well) or use `--json` and post-process; a one-off `sed`/`awk` on date
strings tends to break on the rows that do not match the shape you assumed.

## Examples

```bash
# timestamp -> readable, in Beijing time
python3 scripts/dtconv.py 1735689600 -z Asia/Shanghai

# datetime string -> epoch millis, input understood as Beijing time
python3 scripts/dtconv.py "2026-08-26 15:30" --in-tz Asia/Shanghai -f unix_ms

# timezone hop, keeping only the wall clock
python3 scripts/dtconv.py "2026-08-26T07:30:00Z" -z America/New_York -f datetime

# natural language, several at once
python3 scripts/dtconv.py "3 days ago" "下周一 09:00" "明天下午3点" -f datetime

# arithmetic and durations
python3 scripts/dtconv.py now --add=-2h30m -f iso
python3 scripts/dtconv.py "2026-01-01" --diff "2026-12-25"
```

## Input it understands

- Epoch numbers, unit inferred from magnitude: seconds, millis, micros, nanos; floats fine
- ISO 8601 / RFC 3339 in any shape: `2026-08-26T07:30:00Z`, `+08:00` or `+0800` offsets,
  ISO basic format `20260826T073000`, nanosecond fractions from Go/Java logs (digits below
  microsecond precision are dropped — `datetime` cannot hold them)
- RFC 2822 / HTTP dates (`Wed, 01 Jan 2025 08:00:00 +0800`)
- Common patterns: `2026-08-26 15:30:00`, `2026/08/26`, `20260826`, `202608261530`,
  `2026年8月26日`, `Aug 26 2026`, bare `15:30` (means today)
- Relative phrases: `now`, `today`, `tomorrow`, `yesterday`, `前天/后天/大后天`,
  `3 days ago`, `in 2 hours`, `2天前`, `3小时后`, `next friday`, `last monday`,
  `下周一`, `上个月`, `明年`, optionally with a time (`tomorrow 9:30am`, `明天下午3点`)
- Spreadsheet serial numbers with `-u excel` (they look like plain integers, so this one
  is opt-in rather than auto-detected)

Not covered: cron expressions, business-day/holiday calendars, and Windows FILETIME. Say so
rather than improvising if one of those comes up.

## Things worth knowing before you answer

Naive input (no offset in the string) is interpreted in `--in-tz`, which defaults to the
machine's local zone. When the user's data comes from a server in another zone, say so and
pass `--in-tz` explicitly — this is the most common source of an off-by-N-hours answer.

An 8-digit number like `20260826` is read as a compact date, not a 1970s epoch, because
that is almost always what it is. Pass `-u s` when you really do mean the epoch. If you
are unsure which the user meant, the report line `parsed as ...` tells you what happened —
quote it when the input was ambiguous.

`01/02/2026` is genuinely ambiguous. The script assumes M/D/Y and prints a note with the
D/M/Y reading; surface that note rather than silently picking one.

In `--add`, `m` means minutes and `mo`/`月` means months. Month and year steps clamp the
day, so Jan 31 + 1 month is Feb 28. Timezone conversion goes through the IANA database, so
DST is handled — if a result looks an hour off around a DST boundary, it is probably right.

When the answer hinges on a timezone, include it in your reply (`2025-01-01 08:00:00
+0800`). A time without its zone is the kind of value that gets copied into a bug.
