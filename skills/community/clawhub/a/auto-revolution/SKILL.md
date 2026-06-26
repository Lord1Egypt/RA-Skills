---
name: auto-revolution
description: Safe publishing variant of Auto Revolution. Provides structured task templates, review prompts, safety scanning, task state updates, and logging for human supervised multi step workflows. Use when creating or reviewing task JSON files, applying review results, scanning instruction text for risky shell patterns, or managing queued task activation. This package avoids autonomous background execution and does not run arbitrary shell instruction strings.
---

# Auto Revolution

This is the ClawHub publishing variant.

## Use this skill for

- creating structured task JSON files
- activating queued tasks whose dependencies are complete
- scanning proposed instruction text for risky shell patterns
- applying review JSON back into a task file
- logging workflow events in JSONL
- generating a review prompt for manual or supervised review

## Do not use this package for

- autonomous cron loops
- unsupervised background execution
- direct execution of arbitrary shell instruction strings
- remote agent spawning from bundled scripts

## Files to use

- `task-schema.json` for task structure reference
- `config/models.json` for example role configuration
- `scripts/create-task.js` to create a task interactively
- `scripts/activate-queued-tasks.js` to move ready tasks from `queued` to `pending`
- `scripts/security-scan.js` to scan instruction text or a task review block
- `scripts/trigger-review.js` to generate a review prompt for supervised review
- `scripts/apply-review.js` to write a review result back into a task JSON file
- `scripts/log-event.js` to append JSONL audit events
- `scripts/atomic-lock.sh`, `scripts/force-unlock.sh`, `scripts/unblock-task.sh` for task lock maintenance

## Minimal workflow

1. Create or edit a task JSON.
2. If the task depends on other tasks, run `scripts/activate-queued-tasks.js` when dependencies may be complete.
3. Generate a review prompt with `scripts/trigger-review.js`.
4. Obtain a supervised review result as JSON.
5. Apply that result with `scripts/apply-review.js`.
6. If you need to inspect instruction text, run `scripts/security-scan.js` before any manual execution.

## Safety rules

- Keep a human in the loop for any real execution.
- Treat generated instructions as untrusted until reviewed.
- Prefer structured task updates over free form shell execution.
- Do not add scripts that call `execSync` on model generated instruction strings in the publishing package.

## Notes

This package is intentionally minimal for publication. Internal development documents, autonomous heartbeat runners, and direct execution engines belong in the private local version, not the published package.
