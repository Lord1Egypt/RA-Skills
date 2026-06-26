---
name: flow-state-monitoring
description: Workflow-driven skill that infers deep focus and autonomously mutes interruptions.
os: all
requires:
  bins: [gog]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Flow State Monitoring

This skill orchestrates a workflow to analyze focus telemetry and autonomously update your status in Google Workspace to protect your flow state.

## Cognitive Directives
WHEN [telemetry from local sensors indicates deep focus] 
THEN [
  Execute the following Jidoka-validated loop:
  1. Execute `llm_classify_intent` (Sub-Agent) to classify the activity.
     - **Verification Step (Jidoka):** Verify the sub-agent returns a valid classification (e.g., "Deep Work"). IF it hallucinates text, retry classification.
  2. IF classified as "Deep Work", Execute the native terminal command `gog calendar create primary --summary "Busy - In Flow"` to block interruptions.
     - **Verification Step (Jidoka):** Check if the calendar event creation returns a successful JSON response. IF it fails, wait 3 seconds and retry (max 3 times). IF it still fails, report the error and STOP.
]

## Expected Output
A JSON confirmation of the calendar status update.
