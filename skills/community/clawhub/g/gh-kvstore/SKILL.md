---
name: gh-kvstore
description: "In-memory key-value store with TTL for AI agents. Set, get, delete, list, flush, and stats. Supports any JSON value, optional TTL per key, and prefix-based key listing. Like a lightweight Redis for agent pipelines."
metadata: {"openclaw":{"emoji":"🗄️","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# KVStore

Lightweight key-value store for agent state, caching, and data sharing.

## Start the server

```bash
uvicorn kvstore.app:app --port 8013
```

## Set a value

```bash
curl -s -X POST http://localhost:8013/v1/set \
  -H "Content-Type: application/json" \
  -d '{"key": "user:1", "value": {"name": "Alice", "role": "admin"}}' | jq
```

## Set with TTL (auto-expires)

```bash
curl -s -X POST http://localhost:8013/v1/set \
  -H "Content-Type: application/json" \
  -d '{"key": "cache:token", "value": "abc123", "ttl_seconds": 3600}' | jq
```

## Get a value

```bash
curl -s http://localhost:8013/v1/get/user:1 | jq
```

Returns `key`, `value` (any JSON), and `ttl_remaining` (seconds until expiry, or null).

## List keys by prefix

```bash
curl -s "http://localhost:8013/v1/keys?prefix=user:" | jq
```

## Delete / Flush / Stats

```bash
curl -s -X DELETE http://localhost:8013/v1/delete/user:1 | jq
curl -s -X POST http://localhost:8013/v1/flush | jq
curl -s http://localhost:8013/v1/stats | jq
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/set | Set a key-value pair (optional TTL) |
| GET | /v1/get/{key} | Get value by key |
| DELETE | /v1/delete/{key} | Delete a key |
| GET | /v1/keys | List keys (optional ?prefix=) |
| POST | /v1/flush | Delete all keys |
| GET | /v1/stats | Hit/miss counts and total keys |
