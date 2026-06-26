# GitHub Workflow

## Branching
Recommended branch patterns:
- `proposal/...`
- `task/...`
- `review/...`

Treat the default branch as approved shared state.

## Files vs Issues vs PRs
- Use files in `workspace/` for durable structured state.
- Use Issues for discussion, escalation, and cross-cutting tracking.
- Use PRs for proposed changes that require review or approval.

## Suggested Flow
1. Create or update a task.
2. Draft a proposal if approval is required.
3. Open a PR or commit proposal artifacts.
4. Wait for human approval where required.
5. Merge approved outputs into the default branch.
6. Record the final decision if it changes policy or future work.

## Review Expectations
Every change should make these items obvious:
- visibility level
- owner or requester
- approval status
- affected task IDs

## Audit Expectations
Use commit messages, PR descriptions, and decision files so future reviewers can answer:
- who proposed the change
- who approved the change
- which task or proposal it belongs to
- whether the change affected policy, execution, or risk posture
