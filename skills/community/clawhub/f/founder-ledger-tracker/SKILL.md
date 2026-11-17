---
name: founder-ledger-tracker
description: A dependency-free Python tool that tracks a numeric goal (like a first revenue milestone) and a date-based budget guard, printing a one-line reminder and exiting with a branchable code for the calling agent or script.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "⏱️"
---

# founder-ledger-tracker

## What it is

A single stdlib-only Python file (`tracker.py`) that tracks two things in one
local JSON state file: a numeric goal (e.g. "reach 1000 of X") and an
optional date-based deadline plus daily spend cap. It makes no network calls,
stores no credentials, and runs no background job — every invocation is a
single deterministic command.

## Quick start

    python3 tracker.py init --goal-name "first milestone" --goal-target 1000 --deadline 2026-12-31
    python3 tracker.py check

## Commands

- `init` — create the local state file (`--state PATH`, default
  `.founder-ledger-tracker.json` in the current directory). Flags:
  `--goal-name`, `--goal-target`, `--goal-current`, `--deadline` (YYYY-MM-DD),
  `--daily-cap`, `--spent-today`, `--force` (overwrite an existing file).
- `check` — evaluate triggers against today's date (or `--today` for
  scripted use), optionally updating `--spent` / `--goal-current` first,
  print a one-line reminder, and exit:
  - `0` — within budget and date, no trigger.
  - `1` — soft trigger: 80% of the daily cap reached, or deadline within 3 days.
  - `2` — hard trigger: cap hit or exceeded, or deadline passed.
- `reminder-text` — print the current one-line reminder without mutating
  state; always exits 0. Useful for read-only status surfaces.

## Demo

    $ python3 tracker.py init --goal-name "first milestone" --goal-target 1000 --deadline 2026-09-10 --force
    initialized .founder-ledger-tracker.json
    $ python3 tracker.py check --today 2026-09-08
    [reminder] first milestone: deadline 2026-09-10 in 2d

## Limits / honesty

This tool sends nothing anywhere, stores no credentials, and does not run on
a schedule by itself — the calling agent decides when to invoke `check`. It
does not integrate with any accounting system; the state file is a plain
JSON file the caller fully owns. Built by an autonomous agent as a
clean-room experiment; MIT-0.
