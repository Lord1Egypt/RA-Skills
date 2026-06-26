# Duplicate Task Detection Module

Purpose: prevent creation of redundant cron jobs that monitor the same thing with the same schedule.

## Detection Strategy

Before creating a new cron task:

1. List existing cron jobs.
2. Compare:
   - schedule
   - task objective keywords
   - delivery channel

If a similar job already exists:

- warn the user
- show the existing job
- ask whether to reuse, modify, or create a new one

## Example

User request: "monitor AI news every day"

Existing job:
AI News Radar
0 12 * * *

System response:
"A similar task already exists. Do you want to update it instead?"
