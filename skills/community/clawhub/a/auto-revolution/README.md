# Auto Revolution

Safe publishing variant for ClawHub.

## What this package includes

- structured task creation
- dependency activation for queued tasks
- instruction safety scanning
- review prompt generation
- review result application
- JSONL event logging
- task lock maintenance helpers

## What this package excludes

- autonomous cron heartbeats
- direct execution of arbitrary shell instruction strings
- bundled remote review runners
- internal design and experiment documents

## Included scripts

- `node scripts/create-task.js`
- `node scripts/activate-queued-tasks.js`
- `node scripts/security-scan.js <task-file.json>`
- `node scripts/trigger-review.js <task-id>`
- `node scripts/apply-review.js <task-id> --file <review.json>`
- `node scripts/log-event.js <event> [key=value...]`

## Safety position

This publishing variant is for supervised workflows. Generated instructions should be reviewed before any real execution. The package does not include autonomous executors.
