# Auto Revolution Scripts

This publishing bundle keeps only supervised workflow helpers.

## Included

- `create-task.js`
- `activate-queued-tasks.js`
- `security-scan.js`
- `trigger-review.js`
- `apply-review.js`
- `log-event.js`
- `atomic-lock.sh`
- `force-unlock.sh`
- `unblock-task.sh`

## Excluded from publish bundle

- autonomous heartbeat coordinators
- direct execution engines
- remote review runner scripts
- internal test and experiment scripts

## Guidance

Use these scripts to manage task state and review data. Keep any real execution under explicit human supervision outside this publishing package.
