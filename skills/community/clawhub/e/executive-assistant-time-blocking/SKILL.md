---
name: executive-assistant-time-blocking
description: Standard Operating Procedure (SOP) that acts as an executive assistant to block out calendar time using TS atomic plugins.
os: all
requires:
  bins: [gog]
  plugins: [autonomous-workflows-plugin]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This workflow relies entirely on discrete, single-responsibility TS tools rather than a monolithic markdown loop.
- **Standardized Work (Hyojun Sagyo):** This node represents a strict, step-by-step Standard Operating Procedure (SOP) for automated time-blocking.
- **Jidoka (自働化):** Includes autonomous self-healing loops with hard verification stops between every step.

# Executive Assistant Time Blocking SOP

This procedure guides the agent to evaluate current incomplete tasks from Google Tasks, estimate their duration, and sequentially schedule them into available gaps using TS atomic tools.

## Cognitive Directives

WHEN [Requested to schedule tasks, time-block the backlog, or act as an executive assistant for schedule management]
THEN [
  Follow this strict Standard Operating Procedure:

  **Step 1: Task Collection**
  - Execute `gog tasks list @default --json` to retrieve incomplete tasks.
  - **Jidoka Stop:** IF the output is not a valid JSON array, retry. IF empty, report no tasks and STOP.

  **Step 2: Cognitive Assessment**
  - Autonomously assign duration and urgency to each task.

  **Step 3: Schedule Retrieval**
  - Execute `gog calendar events primary --from "<start>" --to "<end>" --json`.
  - **Jidoka Stop:** Verify the response. Retry on error.

  **Step 4: Gap Analysis**
  - Execute the `workflow_calculate_schedule_gaps` atomic TS tool, passing the events array.
  - **Jidoka Stop:** IF the tool returns an error, correct and retry.

  **Step 5: Sequential Time Blocking**
  - For each task, map it to a free gap.
  - Execute the `Google Calendar Create Event` atomic node.
  - **Jidoka Stop:** Verify event creation success.

  **Step 6: Overlap Audit**
  - Execute the `workflow_audit_schedule_overlaps` atomic TS tool.
  - **Jidoka Stop:** IF overlaps are detected, resolve them using `Google Calendar Delete Event` and repeat the scheduling loop.
]

## Expected Output
A comprehensive summary of the scheduled tasks, detailing the timeline and confirmation of overlap-free scheduling.
