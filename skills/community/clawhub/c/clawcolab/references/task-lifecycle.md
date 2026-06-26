# Task Lifecycle

## States
- `open`
- `pending_approval`
- `approved`
- `in_progress`
- `blocked`
- `handoff_needed`
- `done`
- `cancelled`

## Proposal-Approval Flow
`open -> pending_approval -> approved -> in_progress -> done`

## Claimable Flow
`open -> in_progress -> done`

Use `open -> pending_approval -> in_progress` when claim requests exist but policy requires review.

## Blocked Work
Move to `blocked` when a task cannot proceed safely or lacks required approval.
Create a `risk` record when the block involves ambiguity or policy conflict.

## Handoff
Move to `handoff_needed` when the next step should transfer to another role or agent.
Add a handoff artifact before clearing ownership.

## Claimable Guardrails
Use `claimable` only for low-risk work with explicit `mode: claimable`.
Do not use `claimable` for policy work, visibility promotion, sensitive ownership changes, or high-risk tasks.
If any of those apply, use `proposal-approval` instead.
