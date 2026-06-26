---
name: Event-Cancellation-Reconciler
description: Standard Operating Procedure (SOP) to autonomously detect cancelled events and sync the calendar state using atomic nodes.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This workflow relies entirely on discrete, single-responsibility atomic nodes rather than a monolithic loop.
- **Standardized Work (Hyojun Sagyo):** This node represents a strict, step-by-step Standard Operating Procedure (SOP) for state-syncing Google Calendar based on cancellation notices.
- **Jidoka (自働化):** Includes autonomous self-healing loops with hard verification stops between every step.

# Event Cancellation Reconciler SOP

This procedure guides the agent to process cancelled events using explicitly defined atomic nodes.

## Cognitive Directives
WHEN [Requested to handle a cancelled event from an email OR when reading an email indicating a cancellation/reschedule]
THEN [
  Follow this strict Standard Operating Procedure:

  **Step 1: Extract Event Details**
  - Execute the `LLM-Extract-JSON` or `LLM-Extract-Action-Items` atomic skill against the email body to extract `original_date`, `original_time`, and `target_entity`.
  - **Jidoka Stop:** Validate the extracted payload. IF extraction fails, ask the user for details and STOP. Do NOT proceed.

  **Step 2: Locate Orphaned Event**
  - Execute the atomic node for calendar search (e.g., `gog calendar events primary --from "<original_date>T00:00:00Z" --to "<original_date>T23:59:59Z" --json`).
  - **Jidoka Stop:** Verify events are returned. IF no matching event is found, reply "No conflicting calendar events found" and STOP. Do NOT proceed.

  **Step 3: Reconcile State**
  - Execute the `Google Calendar Delete Event` atomic node or the `Google Calendar Update Summary` atomic node to append "[CANCELLED]".
  - **Jidoka Stop:** Verify the atomic node returns a success JSON response. IF it fails, retry the node up to 3 times with the exact error. IF it still fails, report the error to the user and STOP.

  **Step 4: Notify**
  - Inform the user that the calendar state has been successfully reconciled.
]

## Expected Output
A confirmation message stating the calendar has been synced and the specific event has been handled.
