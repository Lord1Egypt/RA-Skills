# apple-calendar-ops boundary

## What this skill is

A reusable Apple Calendar / CalDAV operations layer.

It exists so higher-level systems can call a stable interface for calendar reads and writes.

## In scope

- list available calendars
- fetch events by time range
- create events
- update events
- delete events
- normalize event data into a stable JSON shape
- resolve credentials from `secrets.json`

## Out of scope

- deciding how to schedule the user's day
- prioritizing Todoist tasks against calendar events
- generating human-facing daily plans
- learning user preferences over time
- cross-system orchestration logic

## Write-safety policy

Reads are low risk.
Writes are higher risk.

For writes:
- support dry-run whenever practical
- prefer explicit identifiers for update/delete
- do not perform broad fuzzy deletes
- surface what will change before changing it when operating interactively

## Upstream caller expectations

A higher-level caller may be:
- the main chat session
- a scheduler/orchestrator task
- another skill/script

This skill should stay narrow and predictable so upstream systems remain simple.
