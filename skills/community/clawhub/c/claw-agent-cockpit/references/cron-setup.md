# Cron Setup Guide

## Data Update Cron (Recommended)

Create a Cron job to update agent-data.json with fresh session data.

### Recommended Settings

- **Schedule**: Every 3 hours (`kind: every`, `everyMs: 10800000`)
- **Agent**: Your primary agent ID
- **Session Target**: isolated
- **Delivery**: none (silent background task)

### Cron Payload Template

```
Execute Agent monitoring data update:
1. Call sessions_list (limit=20, messageLimit=0)
2. Determine status per agent:
   - ok: task in progress (progress < 100%)
   - rest: task complete, ≤24h inactive
   - idle: task complete, ≥24h but <7 days inactive
   - lost: ≥7 days inactive
3. Write results to {workspace}/agent-data.json
4. Process only main sessions (exclude subagent and cron sessions)
5. Output update summary
```

### Estimated Cost

- ~2-3 API calls per execution
- 8 executions/day at 3-hour interval = ~16-24 calls/day

### Context Check Cron (Optional)

- **Schedule**: Twice daily (e.g. `0 9,17 * * *`)
- **Purpose**: Check Agent context usage and MEMORY.md size
- **Estimated cost**: ~3-5 API calls per execution

## Adjusting Frequency

Lower frequency = fewer API calls but less fresh data.

| Frequency | Calls/Day | Freshness |
|-----------|-----------|-----------|
| Every 1 hour | 48-72 | Very fresh |
| Every 3 hours | 16-24 | Balanced ✅ |
| Every 6 hours | 8-12 | Moderate |
| Every 12 hours | 4-6 | Basic |
