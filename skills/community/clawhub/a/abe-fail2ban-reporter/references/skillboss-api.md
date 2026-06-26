# SkillBoss API Hub Reference

Base URL: `https://api.heybossai.com/v1`

## Authentication

```
Authorization: Bearer $SKILLBOSS_API_KEY
```

Header: `Authorization: Bearer <api-key>`
Content-Type: `application/json`

## /v1/pilot — Intelligent Routing (Recommended)

```
POST /v1/pilot
```

### Search (IP Threat Intelligence Lookup)

```bash
curl -s "https://api.heybossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "search", "inputs": {"query": "IP reputation threat report 1.2.3.4"}, "prefer": "balanced"}'
```

Response path: `.data.result`

### Chat (AI Analysis)

```bash
curl -s "https://api.heybossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "chat", "inputs": {"messages": [{"role": "user", "content": "Analyze this IP: 1.2.3.4"}]}, "prefer": "balanced"}'
```

Response path: `.data.result.choices[0].message.content`

## Response Format

| Type | Result Path |
|------|-------------|
| search | `data.result` |
| chat | `data.result.choices[0].message.content` |
| image | `data.result.image_url` |
| tts | `data.result.audio_url` |

## Environment Variable

| Variable | Description |
|----------|-------------|
| `SKILLBOSS_API_KEY` | SkillBoss API Hub authentication key |
