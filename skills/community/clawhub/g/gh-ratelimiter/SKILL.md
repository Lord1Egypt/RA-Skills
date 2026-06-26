---
name: gh-ratelimiter
description: "In-memory sliding window rate limiter for AI agents. Create rate limits per API key, check quota before calling, consume requests, reset, and list all limits. Keeps agents from hitting rate limits on external APIs."
metadata: {"openclaw":{"emoji":"⏱️","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# RateLimiter

Track and enforce rate limits so your agent doesn't get throttled.

## Start the server

```bash
uvicorn ratelimiter.app:app --port 8012
```

## Create a rate limit

```bash
curl -s -X POST http://localhost:8012/v1/limits \
  -H "Content-Type: application/json" \
  -d '{"key": "openai-api", "max_requests": 60, "window_seconds": 60}' | jq
```

## Check before calling

```bash
curl -s http://localhost:8012/v1/check/openai-api | jq '.allowed'
```

## Consume after calling

```bash
curl -s -X POST http://localhost:8012/v1/consume/openai-api | jq
```

Returns `allowed` (true/false), `remaining`, and `retry_after_seconds` (how long to wait if exhausted).

## List all limits

```bash
curl -s http://localhost:8012/v1/limits | jq
```

## Reset quota

```bash
curl -s -X POST http://localhost:8012/v1/reset/openai-api | jq
```

## Delete a limit

```bash
curl -s -X DELETE http://localhost:8012/v1/limits/openai-api | jq
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/limits | Create/update a rate limit |
| GET | /v1/limits | List all rate limits |
| GET | /v1/check/{key} | Check if next request is allowed |
| POST | /v1/consume/{key} | Use one request from quota |
| POST | /v1/reset/{key} | Reset quota to full |
| DELETE | /v1/limits/{key} | Delete a rate limit |
