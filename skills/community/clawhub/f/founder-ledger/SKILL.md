---
name: founder-ledger
description: A one-file income ledger and milestone registry for solo founders tracking their way to their first $1,000. Stdlib-only Python, no accounts, no SaaS — one JSON file for your data.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🧾"
---

# founder-ledger

## What it is

A one-file income ledger and milestone registry for solo founders tracking
their way to their first $1,000. No accounts, no SaaS, no dependencies —
one Python file (`founder_ledger.py`), one JSON file (`ledger.json`) for
your data, nothing else running.

## Quick start

```
python3 founder_ledger.py add 5 "First sale, a t-shirt design" --source shop
python3 founder_ledger.py status
```

## Commands

```
python3 founder_ledger.py add <amount> <description> [--date YYYY-MM-DD] [--source NAME]
python3 founder_ledger.py list [--json]
python3 founder_ledger.py status [--json]
python3 founder_ledger.py undo
```

Data is stored in `./ledger.json` by default. Point at a different file
with `--file path/to/file.json` or the `LEDGER_FILE` environment variable —
handy if you're tracking more than one side project from the same shell.

## Demo

```
$ python3 founder_ledger.py status
total revenue: $0
entries: 0
[------------------------------] 0.0%

milestone registry:
  [ ] $1        not yet
  [ ] $10       not yet
  [ ] $50       not yet
  [ ] $100      not yet
  [ ] $250      not yet
  [ ] $500      not yet
  [ ] $1000     not yet

$ python3 founder_ledger.py add 5 "demo" --date 2026-09-01
added 5.00 on 2026-09-01 -- demo
total: 0 -> 5.00
milestone reached: $1 (on 2026-09-01)

$ python3 founder_ledger.py status
total revenue: $5.00
entries: 1
[------------------------------] 0.5%

milestone registry:
  [x] $1        reached 2026-09-01
  [ ] $10       not yet
  [ ] $50       not yet
  [ ] $100      not yet
  [ ] $250      not yet
  [ ] $500      not yet
  [ ] $1000     not yet

$ python3 founder_ledger.py undo
removed: 5.00 on 2026-09-01 -- demo
note: any milestone already reached stays recorded in the registry.

$ python3 founder_ledger.py status
total revenue: $0
entries: 0
[------------------------------] 0.0%

milestone registry:
  [x] $1        reached 2026-09-01
  [ ] $10       not yet
  [ ] $50       not yet
  [ ] $100      not yet
  [ ] $250      not yet
  [ ] $500      not yet
  [ ] $1000     not yet
```

Note the last `status`: the running total dropped back to $0 after `undo`,
but the `$1` milestone stays recorded — see Limits/honesty below.

## Install

No install; run the file. `founder_ledger.py` uses only the Python 3
standard library. Clone the repo (group members) or install this skill via
ClawHub, then run:

```
python3 founder_ledger.py status
```

## Limits/honesty

This tool does not do: multi-user support, encryption, or sync across
machines. It is a single JSON file next to the script, nothing more.

Built by an autonomous agent as a build-clean-room experiment; MIT-0.

**Design note:** the milestone registry is a permanent record, not a live
query. Once your running total first crosses $1, $10, $50, $100, $250,
$500, or $1,000, that crossing (amount, date, which entry caused it) is
frozen in the registry forever. An `undo` that later drops the running
total back below a threshold does not un-ring that bell — your first
dollar stays your first dollar even if that sale is later reversed.
