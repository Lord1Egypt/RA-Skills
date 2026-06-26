# Scheduler Module

Responsible for translating human time descriptions into cron schedules.

Supported inputs:

- every day at time
- weekly schedule
- monthly schedule
- custom cron expression

Examples:

"every day at 12" → 0 12 * * *
"every monday 9" → 0 9 * * 1

If the user does not provide a schedule, ask clarifying questions.
