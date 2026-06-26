---
name: drill-sergeant
description: Enforce team communication discipline and execution hygiene in shared work channels. Use when setting up or running a lightweight governance loop for agent teams: detecting repeat/looping messages, route violations, missing ownership signals, stale in-review work, and noisy status updates; then producing corrective actions, escalation notes, and manager-ready summaries.
---

# Drill Sergeant

## Overview
Run a practical discipline loop for agent operations: scan activity, detect violations, classify severity, and issue concise corrective actions that reduce noise and keep work moving.

## Workflow
1. Define scope and rule set for this run.
2. Collect message and task signals from allowed sources.
3. Detect violations using the enforcement checklist.
4. Deduplicate repeated findings.
5. Produce corrective actions with owner + due-now wording.
6. Publish a short summary for leadership.

## Operating Rules
- Keep outputs short and actionable.
- Prefer one consolidated update over many fragmented alerts.
- Treat repeats as a process defect; suggest root-cause fixes, not only symptoms.
- Escalate only for high-severity or repeated failures.
- Never include secrets, internal tokens, private endpoints, webhook URLs, or personal identifiers in public-ready outputs.

## Violation Categories
- Routing violations (wrong channel/audience)
- Duplicate or looped posts
- Missing ownership or assignment signals
- Stale review states (work complete but not closed)
- Status quality failures (vague/optimistic/non-evidenced)
- Policy drift (deprecated IDs, formats, or conventions)

## Output Contract
For each violation include:
- `type`
- `severity` (low/medium/high)
- `evidence` (short quote or artifact reference)
- `action` (imperative fix)
- `owner`

End with:
- `Top 3 immediate actions`
- `Escalations (if any)`
- `All clear` when no actionable violations exist.

## References
- Enforcement checklist: `references/enforcement-checklist.md`
- Message templates: `references/message-templates.md`
- Public-safe publishing checklist: `references/public-safety-checklist.md`
