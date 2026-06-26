---
name: backlog-grooming
description: Workflow-driven skill that autonomously manages stale items in Google Tasks.
os: all
requires:
  bins: []
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Backlog Grooming

This skill directs the agent to trigger the native programmatic backlog grooming plugin to maintain a clean workspace.

## Cognitive Directives
WHEN [Triggered by schedule or user request to groom backlog] 
THEN [
  Execute the following Jidoka-validated loop:
  1. **Execute Node:** Execute the `workflow_backlog_grooming` plugin tool with empty JSON `{}` to trigger the grooming process.
  2. **Verification Step (Jidoka):** Check if the tool returns a valid JSON response with `{"success": true}` or an error message. IF it returns an error or hallucinated output, report the error, wait 3 seconds, and retry (max 3 times). IF it still fails, stop and notify the user.
]
## Expected Output
A JSON summary of the groomed tasks returned by the plugin.
