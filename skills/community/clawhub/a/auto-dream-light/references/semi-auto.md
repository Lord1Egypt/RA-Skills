# Semi-Automatic Mode

Use this reference when the user wants a stable trigger-based workflow before cron.

## Definition

Semi-automatic means:
- the user triggers the run
- the workflow itself is fixed and predictable
- outputs and logging are standardized
- later cron adoption should require changing only the trigger method

## Standard outputs

Each run should produce up to three layers:

1. core memory file updates (if needed)
2. dream-log entry
3. concise user summary

## Standard skip rules

Skip but record when:
- recent logs are already consolidated
- no durable new memory exists
- all candidate items are duplicates with no real update

## Upgrade path to cron

What stays the same:
- scan logic
- routing logic
- dedup logic
- dream-log logic
- summary logic

What changes later:
- trigger source only (user phrase → cron)
