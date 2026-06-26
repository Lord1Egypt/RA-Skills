# Installation Guide

## Prerequisites

- Docker installed and running
- Cursor account with active AI subscription
- Valid `WorkosCursorSessionToken`

## Docker Deployment

### Option A: Docker Run (Recommended)

```bash
docker run -d \
  --name cursor-api \
  -p 3010:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN=your_token \
  waitkafuka/cursor-api:latest
```

### Option B: Docker Compose (For Long-term Use)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  cursor-api:
    image: waitkafuka/cursor-api:latest
    container_name: cursor-api
    ports:
      - "3010:3000"
    environment:
      WORKOS_CURSOR_SESSION_TOKEN: your_token
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Start:
```bash
docker compose up -d
```

## Verify Deployment

**Check container status:**
```bash
docker ps | grep cursor-api
```

**Test API endpoints:**

OpenAI format:
```bash
curl -X POST http://localhost:3010/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

Anthropic Messages API format:
```bash
curl -X POST http://localhost:3010/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_token" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container won't start | Run `docker logs cursor-api` — usually invalid token |
| API returns 401 | Token expired, retrieve new one |
| Port conflict | Change `-p 3011:3000` and update config accordingly |
