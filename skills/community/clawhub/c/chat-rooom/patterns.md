# Patterns - Chat Rooom

## Planner -> Builder -> Reviewer

Use one room with three channels:
- `general` for task framing and status
- `build` for implementation notes
- `review` for critique and acceptance

This pattern works best when `claims.md` points to exact files and the planner updates `summary.md` after each checkpoint.

## Research -> Decide -> Execute

Use when the team must compare options before acting:
1. Researchers post short option summaries in `general`
2. One agent records the chosen path as a `decision`
3. Execution moves to `build`

The key is to keep the decision visible so debate does not restart mid-execution.

## Incident Swarm

Open a dedicated room or `incident` channel when latency matters:
- One agent owns triage
- One agent owns mitigation
- One agent owns verification

Timebox claims tightly and update `summary.md` after every major state change.

## Review Queue

For batched reviews, keep each job as one row in `jobs.md` with:
- Item
- Owner
- Status
- Link to evidence

This avoids burying approvals inside the chat timeline.
