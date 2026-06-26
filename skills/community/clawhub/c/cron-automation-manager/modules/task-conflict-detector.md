# Task Conflict Detector Module

Purpose: detect scheduling conflicts between automation tasks.

## Conflict Types

1. Multiple heavy jobs at the same time
2. Duplicate monitoring tasks
3. Excessive notification bursts

## Strategy

When creating a new cron job:

1. inspect existing schedules
2. detect if multiple tasks run at the same minute

If conflict detected:

- suggest shifting schedule
- ask user to confirm

Example:

Existing tasks:
AI News 12:00
AI Tools 12:00

New request:
Startup Radar 12:00

System suggestion:
"Consider scheduling at 12:15 to distribute load."