# KV Schema (v1)

## fleet:registry

```json
{
  "updated_at": "2026-03-07T07:28:05Z",
  "agents": [
    { "id": "linus", "name": "Linus", "role": "Builder", "description": "Main build copilot" }
  ]
}
```

## fleet:heartbeat:<agent_id>

```json
{
  "agent_id": "linus",
  "last_seen": "2026-03-07T07:28:05Z",
  "interval_sec": 120,
  "status": "ok"
}
```

## fleet:cron:<agent_id>

```json
{
  "agent_id": "linus",
  "jobs": [
    {
      "name": "collector",
      "schedule": "*/2 * * * *",
      "consecutive_failures": 0,
      "last_run_at": "2026-03-07T07:28:05Z",
      "last_status": "ok"
    }
  ]
}
```

## fleet:runtime:<agent_id>

```json
{
  "agent_id": "linus",
  "runtime": {
    "host": "Rain2018",
    "model": "gpt-5.3-codex",
    "channel": "telegram",
    "last_openclaw_status_raw": "ok"
  }
}
```

## fleet:events:recent

```json
[
  {
    "ts": "2026-03-07T07:28:05Z",
    "agent_id": "linus",
    "type": "HEARTBEAT_OK",
    "level": "info",
    "message": "live from KV"
  }
]
```

## fleet:updated_at

ISO timestamp string.
