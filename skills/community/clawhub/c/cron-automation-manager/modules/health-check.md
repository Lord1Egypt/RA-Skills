# Health Check Module

Purpose: verify that automation tasks are operating normally.

## Checks

1. Verify cron jobs exist and are enabled.
2. Inspect last run status.
3. Detect repeated failures.
4. Confirm message delivery success.

## Behavior

If all tasks are healthy:

Return a short confirmation message.

If issues are detected:

Return a structured alert including:

Task name
Last run status
Possible reason
Suggested fix

## Typical user request

"check automation health"
"are my cron tasks running"
