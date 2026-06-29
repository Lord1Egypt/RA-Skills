# Cron Templates for Agent Organizations

## Daily Learning (Staggered Morning)

```json
{
  "name": "Learning · [Dept]",
  "schedule": {"kind": "cron", "expr": "[MM] [HH] * * *", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are [dept]. Search 1-2 trends in [domain]. Write ~300 words to company/departments/[dept]/learning_YYYYMMDD.md.",
    "model": "zai/glm-4-flash",
    "lightContext": true
  },
  "delivery": {"mode": "none", "bestEffort": true}
}
```

## Daily Report (Staggered Evening)

```json
{
  "name": "[Dept] · Daily Report",
  "schedule": {"kind": "cron", "expr": "[MM] 22 * * *", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are [dept]. List today's work, pending items, next steps. Send via sessions_send to main. Do NOT use message tool.",
    "model": "zai/glm-4-flash",
    "lightContext": true
  },
  "delivery": {"mode": "none", "bestEffort": true}
}
```

## Inspection (3x Daily)

Three separate crons — one per shift:

```json
{
  "name": "Inspector · AM Patrol",
  "schedule": {"kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are Inspector. Check: (1) daily reports filed (2) learning notes written (3) outputs on schedule (4) flag anomalies. Write to company/departments/inspector/patrol_YYYYMMDD.md.",
    "model": "zai/glm-4-flash",
    "lightContext": true
  },
  "delivery": {"mode": "none", "bestEffort": true}
}
```

Duplicate for PM (`0 14 * * *`) and Night (`0 22 * * *`) with adjusted names.

## Model Selection Guide

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| Internal ops (reports, learning) | zai/glm-4-flash | Free, fast |
| Content generation | deepseek-v4-pro | Quality writing |
| Code/technical | zai/glm-4-flash | Sufficient |
| Customer-facing | Cloud Pro models | Best quality |

## Anti-Pattern: message tool in isolated sessions

The `message` tool may fail in isolated cron sessions due to missing auth config. Always use `sessions_send` to main instead.

```json
// BAD - may fail
"message": "...then use message tool to send to feishu..."

// GOOD - reliable
"message": "...send via sessions_send to main..."
```
