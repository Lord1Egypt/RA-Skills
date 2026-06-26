# Hermes Cron List — Test Input

Paste this to test the skill:

```
5233cac535ea [active]
    Name:      hermes-health-watchdog
    Schedule:  */5 * * * *
    Repeat:    ∞
    Next run:  2026-05-30T21:00:00+08:00
    Deliver:   local
    Last run:  2026-05-29T20:55:14.739199+08:00  ok

760c41123c8f [active]
    Name:      vps-disk-daily-check
    Schedule:  0 9 * * *
    Repeat:    ∞
    Next run:  2026-05-30T09:00:00+08:00
    Deliver:   local
    Last run:  2026-05-29T09:00:39.464607+08:00  ok
```

**Expected result:** No high-priority candidates. The watchdog is script-only (`bash /root/.hermes/scripts/health_watchdog.sh`) — it invokes zero LLM tokens regardless of its 288 runs/day frequency. The daily check runs ~1/day, low frequency.

To confirm the watchdog is script-only at Level 2, paste the JSON from `cronjob action='list'` and check: `prompt_preview` shows the bash script, `skills` is empty, `model` is null.