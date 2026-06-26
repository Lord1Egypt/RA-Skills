---
name: clean-log-toolkit
description: Local log file inspection and analysis toolkit. Parse common log formats (apache-common, apache-combined, nginx-access, syslog, JSON-line) or custom regex with named groups into structured TSV/CSV/JSONL. Aggregate errors by level and time bucket (minute/hour/day), surface the most common error groups via fingerprint normalization, and produce JSON/Markdown/CSV reports. Grep log lines with optional time-window (--since/--until), level filter, named-group regex, and -B/-A/-C context lines. Pure Python 3 standard library, no third-party dependencies, no remote calls.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/clean-log-toolkit"}}
---

# clean-log-toolkit

v0.2.0

A small, honest local toolkit for the work agents end up doing constantly: read a log someone sent you, figure out the format, find the actual problems, and produce a summary you can paste into a ticket. Built on Python 3 standard library only. No `awk`/`sed`/`jq` wrappers, no pip installs, no remote calls.

This skill is the third of the "clean-*" trio:
- [`clean-csv-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit) — structured tabular data
- [`clean-text-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit) — unstructured text
- **`clean-log-toolkit`** — semi-structured timestamped logs

## What this skill does

- `scripts/parse.py` — parse a log file into structured rows. Auto-detects `apache-common`, `apache-combined`, `nginx-access`, `syslog`, and `json-line` formats by sniffing the first ~50 lines. Falls back to a generic timestamp + level + message extractor when nothing matches. Pass `--regex PATTERN` with named groups to define a custom format. Output as `.csv`, `.tsv`, or `.jsonl`.
- `scripts/errors.py` — aggregate the errors in a log file. Counts by level (WARN / ERROR / FATAL by default), buckets the timeline by minute / hour / day, normalizes each message into a "fingerprint" (replaces numbers, UUIDs, hex tokens, file:line pairs, and embedded timestamps with placeholders) and surfaces the top-N most frequent error groups. Writes a JSON / Markdown / CSV report or prints a one-screen summary.
- `scripts/grep.py` — grep, but log-aware. Combine `--pattern REGEX`, `--not-pattern REGEX`, `--level LVL[,LVL2...]`, `--since TIMESTAMP`, `--until TIMESTAMP`, and `-B / -A / -C` context lines into one filter pass.
- `scripts/follow.py` (NEW in v0.2.0) — `tail -F` equivalent, log-aware. Streams new lines as they arrive with the same `--pattern` / `--not-pattern` / `--level` / `--since` filters as `grep.py`. Detects log rotation automatically (inode change or file truncation reopens the file). `--max-events N` exits cleanly after N matched events (CI-friendly); `--timeout SECONDS` exits on inactivity; `--json` emits per-line envelopes with extracted timestamp + level.
- `scripts/check_deps.sh` — verify `python3` is available.

## What this skill does not do

- Live tail-and-follow is now supported via `scripts/follow.py` (added v0.2.0).
- It does not call any LLM, web service, or remote API.
- It does not write outside the input/output paths the caller provides.

## Quick start

### 1. Parse an unknown log file

```bash
# Auto-detect the format
python3 scripts/parse.py app.log app.csv

# Or be explicit
python3 scripts/parse.py access.log out.jsonl --format apache-combined
python3 scripts/parse.py syslog.txt out.csv --format syslog
python3 scripts/parse.py events.log out.csv --format json-line --fields ts,level,msg
```

### 2. Custom format via named-group regex

```bash
python3 scripts/parse.py app.log structured.csv \
    --regex '^(?P<ts>\S+)\s+(?P<level>\S+)\s+(?P<message>.*)$'
```

### 3. Aggregate errors and produce a report

```bash
# One-screen summary
python3 scripts/errors.py app.log

# Bucket by minute, top 20 message groups
python3 scripts/errors.py app.log --bucket minute --top 20

# Only count specific levels
python3 scripts/errors.py app.log --level ERROR,FATAL

# Write a Markdown report ready to paste into a ticket
python3 scripts/errors.py app.log --output report.md

# Or a JSON report for downstream tooling
python3 scripts/errors.py app.log --output report.json --bucket hour

# Or a CSV of the timeline only
python3 scripts/errors.py app.log --output timeline.csv --bucket minute
```

`errors.py` fingerprints messages so repeated errors that only differ in numbers / UUIDs / file-line refs collapse to one group with a count. Example: 50 occurrences of `Connection timeout to 10.0.0.5 after 1234ms` and `Connection timeout to 10.0.0.7 after 567ms` collapse into one group `Connection timeout to <N>.<N>.<N>.<N> after <N>ms` with count 50.

### 4. Log-aware grep

```bash
# Pattern + level filter
python3 scripts/grep.py app.log --pattern "Database" --level ERROR,FATAL

# Time window
python3 scripts/grep.py app.log \
    --since "2026-05-10T10:00:00Z" \
    --until "2026-05-10T11:00:00Z"

# Context lines (1 before + 1 after each match)
python3 scripts/grep.py app.log --pattern "FATAL" -C 1 --with-line

# Exclude noisy lines while keeping the rest
python3 scripts/grep.py app.log --level ERROR --not-pattern "heartbeat"

# Invert: keep everything that does NOT match
python3 scripts/grep.py app.log --pattern "INFO" --invert
```

`--since` and `--until` accept the same timestamp formats `parse.py` understands: ISO 8601 (`2026-05-10T10:00:00Z`, `2026-05-10 10:00:00`, with or without microseconds / timezone), apache-style (`10/May/2026:10:00:00 +0000`), and syslog (`May 10 10:00:00` — current year assumed).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success / one or more rows / one or more matches |
| 1 | parse produced zero rows / grep found zero matches / errors found zero matching log entries |
| 2 | bad arguments / unsafe path / missing input / bad regex / unknown format / unsupported output extension |

This 0 / 1 / 2 split is consistent across all three scripts so they slot into shell pipelines cleanly:

```bash
# Parse to JSONL, then summarize errors, then post to a ticket
python3 scripts/parse.py raw.log structured.jsonl \
  && python3 scripts/errors.py raw.log --output ticket.md \
  && cat ticket.md
```

## Safety properties

- Pure Python 3 standard library. No third-party dependencies.
- No `subprocess` calls. No shell invocation.
- All file paths are validated against a strict allowlist regex that rejects shell metacharacters. The same `safe_path()` helper used in `clean-csv-toolkit` and `clean-text-toolkit`.
- Scripts only read the input paths the caller provides and write to the output paths the caller provides.
- All inputs default to UTF-8; reads fall back through `utf-8-sig`, `cp1252`, `latin-1` if needed. Writes are always UTF-8.

## Timestamp + level detection

`_common.py` ships a pragmatic timestamp parser that tries the following formats in order, picking the first that matches:

```
2026-05-10T10:00:00.123456+00:00     (ISO 8601 with TZ + microseconds)
2026-05-10T10:00:00+00:00            (ISO 8601 with TZ)
2026-05-10T10:00:00.123Z              (ISO 8601 UTC Zulu)
2026-05-10T10:00:00Z                  (ISO 8601 UTC Zulu)
2026-05-10T10:00:00                   (ISO 8601 no TZ)
2026-05-10 10:00:00                   (space-separated)
2026/05/10 10:00:00
10/May/2026:10:00:00 +0000           (apache common log)
May 10 10:00:00                       (syslog, no year)
```

Levels are detected case-insensitively from these tokens and folded to canonical names: `TRACE`, `DEBUG`, `INFO`, `NOTICE`, `WARN` (from WARN/WARNING), `ERROR` (from ERROR/ERR), `FATAL` (from FATAL/CRITICAL/CRIT/EMERG/EMERGENCY).

## Known limitations

- The regex-based parsers are pragmatic, not strict — they accept slightly malformed Apache / nginx / syslog lines as long as the structure is close enough.
- `errors.py` fingerprint normalization is a best-effort heuristic. Two semantically different errors that happen to differ only in numbers / hashes will be collapsed; if that matters, use `--top` with a larger N and inspect the samples.
- `parse.py` does not follow a live log file. For tail-follow, pipe `tail -F file | ...` into your own tool. If there's enough demand for a built-in follower, it will land in v0.2.

## Pairs well with

- [`clean-csv-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit) — pipe `parse.py` output (CSV / JSONL) into `inspect`, `validate`, `pivot`, or `transform` to turn raw logs into reportable tables.
- [`clean-text-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit) — pair `parse.py` with `text-toolkit/redact.py` to scrub PII before sharing log dumps.

## v0.2.0 changes

- Added `scripts/follow.py`: live tail-and-follow with log-aware filtering. Same `--pattern` / `--not-pattern` / `--level` / `--since` filters as `grep.py`. Automatic log-rotation detection (inode change or truncation triggers a transparent reopen). `--max-events N` and `--timeout SECONDS` make it CI-friendly; `--json` emits one envelope per matched line with extracted timestamp + level. Closes the only documented limitation from v0.1.x.

## v0.1.1 changes

- Fixed timestamp parser: `--since` and `--until` on `grep.py` now accept date-only values like `2026-05-09`, `2026/05/09`, and `09/05/2026` (European). Previously only full ISO 8601 timestamps were accepted, so users trying to filter by a calendar date got a `could not parse --since` error.

## v0.1.0 changes

- First public release of clean-log-toolkit.
- Three scripts: `parse.py`, `errors.py`, `grep.py`.
- Shared `_common.py` with `safe_path`, `iter_lines`, `parse_timestamp`, `extract_timestamp`, `extract_level` helpers (mirrors the design of `clean-csv-toolkit/scripts/_common.py` and `clean-text-toolkit/scripts/_common.py`).
- Auto-detects 5 log formats by sniffing the first 50 lines.
- Zero third-party dependencies; works on any system that ships Python 3.

## License

MIT
