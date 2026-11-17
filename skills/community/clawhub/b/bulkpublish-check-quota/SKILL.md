---
name: check-quota
description: Check BulkPublish plan limits and current usage. Use when the user asks about their plan, limits, or remaining quota.
---

# BulkPublish — Quota Reference

## get_quota_usage

Takes no parameters. Returns current plan, limits, and usage.

## Response shape

```
plan          — "free", "ltd" (Lifetime, from an AppSumo license), "pro", or "business"
limits        — max values for each resource (-1 means unlimited)
usage         — current consumption for each resource
subscription  — status, currentPeriodEnd, cancelAtPeriodEnd
```

## Plan limits

`-1` in a response means unlimited. `0` means the resource is not available
on that plan.

| Resource | Free | Pro | Business |
|---|---|---|---|
| Channels | 3 | 30 | 75 |
| Accounts per network | 1 | 2 | 5 |
| Posts/day | 3 | 30 | unlimited |
| Posts/month | 30 | 900 | unlimited |
| Scheduled posts pending | 10 | unlimited | unlimited |
| Scheduled per day | 3 | 30 | 100 |
| Storage | 100MB | 2GB | 10GB |
| API requests/day | 30 | 5,000 | 50,000 |
| API keys | 1 | 5 | 10 |
| Repeating schedules | 0 | 10 | unlimited |
| Labels | 10 | 50 | unlimited |
| Team members | 1 | 3 | 10 |
| RSS feeds | 1 | 10 | 50 |
| RSS auto-publish | no | yes | yes |

## Notes

- Daily limits reset at midnight UTC
- Storage is cumulative — delete old media with `delete_media` to free space
- The free plan allows one account per network, so three channels means three different networks
- `-1` in the response means unlimited
- Upgrade at app.bulkpublish.com/settings/billing
