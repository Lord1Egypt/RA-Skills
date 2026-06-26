---
name: epidbot
description: Interact with EpidBot - AI-powered assistant for Brazilian public health data (DATASUS/SINAN)
version: 1.1.2
metadata:
  openclaw:
    requires:
      env:
        - EPIDBOT_API_KEY
        - EPIDBOT_BASE_URL
    primaryEnv: EPIDBOT_API_KEY
    bins:
      - curl
    skillKey: epidbot
    emoji: "\U0001F3E5"
    homepage: https://github.com/fccoelho/EpiDBot
---

# EpidBot OpenClaw Skill

Enables AI agents to interact with EpidBot's REST API for analyzing Brazilian public health data. EpidBot uses natural language processing to help users query, download, and analyze health data from DATASUS.

## Overview

EpidBot provides access to:
- **Brazilian health data**: SINAN disease notifications, SIM mortality, SIH hospital admissions
- **International data sources**: WHO, PAHO, HealthData.gov, World Bank, ECDC
- **Data analysis**: Temporal trends, spatial distribution, demographic breakdowns
- **Visualizations**: Charts, maps, heatmaps, and reports
- **SQL queries**: Execute DuckDB SQL on parquet files

## Authentication

### Option 1: API Key (Recommended for agents)

1. Login to EpidBot web interface at https://epidbot.kwar-ai.com.br
2. Go to Admin Panel -> API Keys -> Create new API key
3. Set the API key as an environment variable:

```bash
export EPIDBOT_API_KEY="your-api-key-here"
export EPIDBOT_BASE_URL="https://api.epidbot.kwar-ai.com.br"
```

### Option 2: Username/Password (Returns JWT tokens)

```bash
curl -X POST "$EPIDBOT_BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Response:
# {
#   "access_token": "eyJ...",
#   "refresh_token": "eyJ...",
#   "token_type": "bearer",
#   "expires_in": 900
# }
```

## API Base URL

Default: `https://api.epidbot.kwar-ai.com.br/api/v1`

Configure via `EPIDBOT_BASE_URL` environment variable.

## Quick Examples

### Check API Health

```bash
curl -H "X-API-Key: $EPIDBOT_API_KEY" \
  "$EPIDBOT_BASE_URL/api/v1/health"
```

### Send a Chat Message (Async Submit + Poll)

Chat messages are processed asynchronously. Submit a message to get a job_id, then poll for the result.

> **Important:** EpidBot queries may invoke data downloads, SQL execution, and LLM reasoning. Responses typically take **30 seconds to 3 minutes**, and complex queries involving large datasets can take up to **5 minutes**. Use exponential backoff when polling (start at 3s, double each interval up to 30s, max total wait 5 minutes).

```bash
# Step 1: Submit the message (returns immediately with job_id)
JOB=$(curl -s -X POST "$EPIDBOT_BASE_URL/api/v1/chat" \
  -H "X-API-Key: $EPIDBOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me dengue cases in São Paulo for 2023", "locale": "en"}')

JOB_ID=$(echo $JOB | jq -r '.job_id')

# Step 2: Poll for result with exponential backoff
INTERVAL=3
MAX_WAIT=300  # 5 minutes
ELAPSED=0
while [ "$ELAPSED" -lt "$MAX_WAIT" ]; do
  RESULT=$(curl -s "$EPIDBOT_BASE_URL/api/v1/chat/$JOB_ID" \
    -H "X-API-Key: $EPIDBOT_API_KEY")
  STATUS=$(echo $RESULT | jq -r '.status')
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    echo $RESULT | jq .
    break
  fi
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
  INTERVAL=$((INTERVAL * 2))
  if [ "$INTERVAL" -gt 30 ]; then
    INTERVAL=30
  fi
done
```

### List Available Tools

```bash
curl -H "X-API-Key: $EPIDBOT_API_KEY" \
  "$EPIDBOT_BASE_URL/api/v1/tools"
```

## Tools / Capabilities

### chat (async submit)

Submit a chat message for async processing. Returns a job_id immediately. LLM responses typically take 5-120 seconds.

**Request:**
```json
{
  "message": "What data is available for dengue in 2023?",
  "session_id": null,
  "locale": "en"
}
```

**Submit Response (200):**
```json
{
  "job_id": "job_a1b2c3d4...",
  "session_id": 1,
  "status": "processing"
}
```

### chat_poll

Poll for the status and result of a chat job. Endpoint: `GET /api/v1/chat/{job_id}`

Recommended polling: exponential backoff starting at 3s, doubling up to 30s, max total wait 5 minutes. Responses may take 30s–3min for simple queries, up to 5min for complex data analysis.

**Poll Response -- still processing:**
```json
{
  "job_id": "job_a1b2c3d4...",
  "status": "processing",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:05Z"
}
```

**Poll Response -- completed:**
```json
{
  "job_id": "job_a1b2c3d4...",
  "status": "completed",
  "session_id": 1,
  "content": "EpidBot has access to SINAN dengue data for 2023...",
  "images": ["![plot](plots/abc.png)"],
  "thinking": "The user is asking about available data...",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:45Z"
}
```

**Poll Response -- failed:**
```json
{
  "job_id": "job_a1b2c3d4...",
  "status": "failed",
  "error": "Error message description",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:10Z"
}
```

### chat_stream (WebSocket)

For streaming responses, connect via WebSocket at:
```
wss://api.epidbot.kwar-ai.com.br/api/v1/chat/stream?api_key=<your-api-key>
```

**Client -> Server Messages:**

```json
{"type": "start", "payload": {"message": "...", "session_id": null, "locale": "en"}}
{"type": "cancel"}
{"type": "ping"}
```

**Server -> Client Messages:**

```json
{"type": "thinking", "data": {"content": "..."}}
{"type": "chunk", "data": {"content": "..."}}
{"type": "complete", "data": {"content": "...", "images": [], "usage": {...}}}
{"type": "error", "data": {"error": "..."}}
{"type": "cancelled"}
{"type": "pong"}
```

### list_sessions

List all chat sessions for the authenticated user.

**Endpoint:** `GET /api/v1/sessions`

**Output:**
```json
[
  {
    "id": 1,
    "name": "Dengue Analysis",
    "message_count": 12,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z"
  }
]
```

### get_session_messages

Get message history for a specific session.

**Endpoint:** `GET /api/v1/sessions/{session_id}/messages`

**Output:**
```json
{
  "session_id": 1,
  "messages": [
    {
      "id": 1,
      "role": "user",
      "text_content": "Show me dengue data",
      "thinking": null,
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "text_content": "Here is the dengue data...",
      "thinking": "The user is asking about...",
      "created_at": "2024-01-01T00:00:01Z"
    }
  ]
}
```

### list_reports

List all generated reports.

**Endpoint:** `GET /api/v1/reports`

**Output:**
```json
[
  {
    "id": 1,
    "title": "Dengue Analysis 2023",
    "report_type": "analysis",
    "image_count": 3,
    "content_size_bytes": 15234,
    "has_pdf": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### get_report

Get full details of a specific report.

**Endpoint:** `GET /api/v1/reports/{report_id}`

**Output:**
```json
{
  "id": 1,
  "title": "Dengue Analysis 2023",
  "report_type": "analysis",
  "prompt": "Show me dengue cases...",
  "content": "# Dengue Analysis\n\n...",
  "image_count": 3,
  "content_size_bytes": 15234,
  "has_pdf": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### download_report

Download report as a markdown file.

**Endpoint:** `GET /api/v1/reports/{report_id}/download`

**Output:** File download with `Content-Disposition` header.

### list_tools

List all available agent tools with descriptions.

**Endpoint:** `GET /api/v1/tools`

**Output:**
```json
[
  {
    "name": "download_sinan_data",
    "description": "Download SINAN disease notification data for a given disease",
    "parameters": null
  },
  {
    "name": "execute_sql_query",
    "description": "Execute a SQL query on the health database",
    "parameters": null
  },
  {
    "name": "get_temporal_trend",
    "description": "Calculate temporal trend for a dataset",
    "parameters": null
  }
]
```

## Error Handling

All endpoints may return errors:

```json
{
  "detail": "Error message description"
}
```

**Common Status Codes:**
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (missing/invalid authentication)
- `403` - Forbidden (valid auth but insufficient permissions)
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Agent Usage Patterns

### Pattern 1: Async Chat (Submit + Poll) -- Recommended

```
Agent: POST /chat -> get job_id -> poll GET /chat/{job_id} with exponential backoff (3s, 6s, 12s, 24s, 30s, 30s...) -> return result
Best for: All queries. Responses take 30s–5min depending on complexity.
IMPORTANT: Always poll with exponential backoff up to 5 minutes total. Do not give up early.
```

### Pattern 2: Streaming Chat (WebSocket)

```
Agent: Connect to WebSocket -> Send start message -> Receive streaming chunks -> Receive complete
Best for: Long responses, real-time feedback, progress indicators
```

### Pattern 3: Session-Aware Chat

```
Agent: List sessions -> Get session messages -> Continue conversation in same session
Best for: Multi-turn analysis workflows
```

### Pattern 4: Tool-Based Workflow

```
Agent: List tools -> Execute specific tool -> Process result -> Chat about results
Best for: Automated data retrieval pipelines
```

## Available Data Sources

### Brazilian Data (PySUS)
- **SINAN**: Disease notifications (dengue, Zika, chikungunya, measles, etc.)
- **SIM**: Mortality data
- **SIH**: Hospital admissions
- **CNES**: Health facilities
- **IBGE**: Census and demographic data

### International Data
- **WHO/GHO**: Global health indicators
- **PAHO**: Americas health data
- **HealthData.gov**: US hospital capacity, COVID metrics
- **World Bank**: Development indicators
- **ECDC**: European disease surveillance

### Specialized
- **Mosqlimate/Infodengue**: Brazilian epidemiological parameters

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `EPIDBOT_API_KEY` | - | API key for authentication |
| `EPIDBOT_BASE_URL` | `https://api.epidbot.kwar-ai.com.br` | Base URL of EpidBot API |

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `POST /auth/login` | 10 requests/minute |
| `POST /auth/register` | 5 requests/minute |
| Other endpoints | 60 requests/minute |

## Deployment

EpidBot is typically deployed via Docker Compose:

```yaml
services:
  api:
    ports:
      - '8123:8123'
  epidbot:
    ports:
      - '7860:7860'
  db:
    ports:
      - '5432:5432'
```

Health check: `curl https://api.epidbot.kwar-ai.com.br/api/v1/health`

## Limitations

- **Job expiry**: Chat jobs expire after 1 hour
- **Response time**: Simple queries take 30s–3min; complex data analysis can take up to 5 minutes. Always poll with exponential backoff.
- **File sizes**: Large data exports may be limited by memory constraints
- **Sandbox execution**: Python/SQL code execution happens in an isolated sandbox with resource limits

## Support

- GitHub: https://github.com/fccoelho/EpiDBot
- Documentation: https://github.com/fccoelho/EpiDBot/tree/main/docs
