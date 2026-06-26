# Quick Reference

## One-Command Install

```bash
docker run -d \
  --name cursor-api \
  -p 3010:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN=YOUR_TOKEN \
  waitkafuka/cursor-api:latest
```

## Environment Setup

```bash
# Add to ~/.zshrc
export ANTHROPIC_BASE_URL="http://localhost:3010/v1"
export ANTHROPIC_API_KEY="YOUR_TOKEN"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
source ~/.zshrc
openclaw gateway restart
```

## Token Refresh

```bash
# Check validity
curl -s -o /dev/null -w "%{http_code}" \
  -H "Cookie: WorkosCursorSessionToken=YOUR_TOKEN" \
  https://api2.cursor.com/v1/me

# If expired: log out/in on cursor.com, get new token, restart container
docker stop cursor-api && docker rm cursor-api
docker run -d --name cursor-api -p 3010:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN=NEW_TOKEN \
  waitkafuka/cursor-api:latest
```

## Status Check

| Check | Command |
|-------|---------|
| Container | `docker ps \| grep cursor-api` |
| Logs | `docker logs cursor-api` |
| API test | `curl http://localhost:3010/health` |

## Endpoints

| Use Case | Endpoint |
|----------|----------|
| OpenClaw / Claude Code | `http://localhost:3010/v1/messages` |
| CC Switch / Universal | `http://localhost:3010/v1/chat/completions` |

## Uninstall

```bash
docker stop cursor-api && docker rm cursor-api
# Remove env vars from ~/.zshrc
```
