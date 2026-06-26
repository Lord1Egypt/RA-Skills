---
name: calendar-guard
description: Standard Operating Procedure (SOP) that autonomously defends your schedule using TS atomic plugins.
os: all
requires:
  bins: [gog]
  plugins: [autonomous-workflows-plugin]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This workflow relies entirely on discrete, single-responsibility TS tools rather than a monolithic loop.
- **Standardized Work (Hyojun Sagyo):** This node represents a strict, step-by-step Standard Operating Procedure (SOP) for scheduling recovery blocks.
- **Jidoka (自働化):** Includes autonomous self-healing loops with hard verification stops between every step.

# Calendar Guard SOP

This procedure evaluates schedule density and automatically injects recovery blocks into your Google Calendar when needed to prevent burnout.

## Cognitive Directives
WHEN [Requested to check calendar for burnout risks OR running on a daily schedule]
THEN [
  Follow this strict Standard Operating Procedure:

  **Step 1: Event Retrieval**
  - Execute `gog calendar events primary --from "..." --to "..." --json` for the target timeframe.
  - **Jidoka Stop:** Verify JSON output. IF fails, retry 3 times. IF still fails, STOP.

  **Step 2: High Load Detection**
  - Execute the `workflow_detect_high_load_periods` atomic TS tool with the retrieved events.
  - **Jidoka Stop:** Verify the tool returns structured load periods. IF it returns an error, correct input and retry.

  **Step 3: Recovery Injection**
  - For each detected high-load period, execute `Google Calendar Create Event` to inject a "Recovery Block".
  - **Jidoka Stop:** Verify creation. IF it fails, log the failure and continue to the next.
]

## Expected Output
A JSON log of any recovery blocks injected.
