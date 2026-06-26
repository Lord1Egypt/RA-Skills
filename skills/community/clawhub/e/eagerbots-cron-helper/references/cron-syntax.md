# Cron Syntax Quick Reference

## Field Order (5-field standard cron)

```
┌─────────── minute       (0–59)
│ ┌───────── hour         (0–23)
│ │ ┌─────── day of month (1–31)
│ │ │ ┌───── month        (1–12)
│ │ │ │ ┌─── day of week  (0–7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * *
```

## Special Characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `*`       | Any / every value | `* * * * *` = every minute |
| `/`       | Step / interval | `*/15 * * * *` = every 15 min |
| `-`       | Range | `1-5` = 1, 2, 3, 4, 5 |
| `,`       | List | `1,3,5` = 1, 3, and 5 |

## Common Examples

| Expression | Meaning |
|------------|---------|
| `* * * * *` | Every minute |
| `*/5 * * * *` | Every 5 minutes |
| `*/15 * * * *` | Every 15 minutes |
| `0 * * * *` | Every hour (on the hour) |
| `0 */2 * * *` | Every 2 hours |
| `0 9 * * *` | Every day at 9:00 AM |
| `0 9 * * 1-5` | Every weekday at 9:00 AM |
| `0 9 * * 1` | Every Monday at 9:00 AM |
| `0 9 * * 6,0` | Every weekend at 9:00 AM |
| `0 0 * * *` | Every day at midnight |
| `0 12 * * *` | Every day at noon |
| `0 0 1 * *` | First day of every month at midnight |
| `0 0 1 1 *` | January 1st at midnight (yearly) |
| `0 0 * * 0` | Every Sunday at midnight |
| `30 8 * * 1-5` | Weekdays at 8:30 AM |
| `0 6,18 * * *` | 6 AM and 6 PM daily |
| `0 0 1,15 * *` | 1st and 15th of month at midnight |

## Valid Ranges

| Field | Range | Notes |
|-------|-------|-------|
| Minute | 0–59 | `60` is invalid |
| Hour | 0–23 | `24` is invalid |
| Day of Month | 1–31 | Not all months have 31 days |
| Month | 1–12 | |
| Day of Week | 0–7 | Both `0` and `7` mean Sunday |

## Common Mistakes

- `60 * * * *` — minute 60 doesn't exist (use `0` for top of hour)
- `* * * * 8` — weekday 8 doesn't exist (0–7)
- `0 0 30 2 *` — Feb 30 never exists; this cron never fires
- `0 24 * * *` — hour 24 doesn't exist (use `0` for midnight)

## OpenClaw Cron Format

OpenClaw uses standard 5-field cron for scheduled tasks.
See: https://docs.openclaw.com/cron for scheduler configuration details.
