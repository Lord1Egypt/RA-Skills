# Schedule Format

Supported schedule strings for `subscribe-journal` and `subscribe-topic`:

- `daily@09:00`
- `weekly@mon@09:00`
- `weekly@1@09:00`
- `workday@09:00`
- `every:6h`
- `at:2026-03-09T09:00:00+08:00`
- `cron:0 9 * * *`

Rules:

- If the caller omits `--schedule`, use the configured `defaultSchedule`.
- `daily@HH:MM`, `weekly@...`, and `workday@HH:MM` are translated to exact cron expressions with the configured timezone.
- `every:` passes the duration directly to `openclaw cron add --every`.
- `at:` passes the value directly to `openclaw cron add --at`.
- `cron:` passes the cron expression directly to `openclaw cron add --cron --tz`.
- When reporting a created subscription, include both the original schedule string and the resolved timezone.

Weekday aliases:

- English: `mon tue wed thu fri sat sun`
- Numeric: `1..7`
- Chinese: `周一 周二 周三 周四 周五 周六 周日`, `星期一 ... 星期日`
