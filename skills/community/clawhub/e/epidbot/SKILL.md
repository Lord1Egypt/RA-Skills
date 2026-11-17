---
name: epidbot
description: Interact with EpidBot - AI-powered assistant for Brazilian public health data (DATASUS/SINAN)
version: 2.4.1
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
    emoji: "\U0001F916"
    homepage: https://kwar-ai.com.br/epidbot
---

# EpidBot OpenClaw Skill

Enables AI agents to interact with EpidBot's REST API for analyzing Brazilian public health data. EpidBot uses natural language processing to help users query, download, and analyze health data from DATASUS.

## Overview

EpidBot provides access to:
- **Brazilian health data**: SINAN, SIM, SIH, SIA, CNES, PNI, CIHA, SINASC via PySUS
- **International data sources**: WHO, PAHO, ECDC, Eurostat, World Bank, HealthData.gov, NZ Health
- **Environmental/Vector data**: Mosqlimate/InfoDengue forecasts, GBIF species occurrences
- **Genomic data**: Pathoplexus pathogen sequences
- **Literature**: OpenAlex, PubMed, Zotero
- **Data analysis**: Temporal trends, spatial distribution, demographic breakdowns, causal inference
- **Visualizations**: Charts, maps, heatmaps, raster plots, and PDF reports
- **Knowledge base**: Document ingestion, wiki, semantic search
- **File uploads**: CSV, XLSX, GeoJSON, GPKG — auto-converted to parquet
- **SQL queries**: Execute DuckDB SQL on parquet files via sandbox
- **Code snippets**: Reusable Python/SQL snippet management

## Safety & Data Handling

Read this section before invoking any endpoint. Following it protects users from
accidental data loss, privacy breaches, and compliance violations.

### External transmission disclosure

Every request in this skill sends data to the **EpidBot service**, a third-party
API hosted at `$EPIDBOT_BASE_URL` (default `https://api.epidbot.kwar-ai.com.br`).
This includes message text, uploaded files, query results, and any content you
include in a request body. Confirm the user understands their data is leaving the
local machine and being processed by an external service before proceeding.

### Sensitive & regulated data

EpidBot is designed for public health data, which may be subject to **LGPD**
(Brazil), **HIPAA**, or equivalent regulations. Before uploading files or sending
queries that could contain personally identifiable or health information:

- Apply data minimization: upload only the columns/rows needed for the analysis.
- Confirm the user has consent, legal basis, or a data-sharing agreement.
- Prefer de-identified or aggregated data over raw individual-level records.
- Never upload credentials, tokens, or secrets as part of a dataset.

### Destructive & irreversible actions

The following operations are **destructive or irreversible**. Before executing
any of them, state what will happen and get **explicit confirmation** from the
user. Do not batch these silently into an automated workflow.

| Action | Endpoint | Risk |
|--------|----------|------|
| Publish dataset | `POST /api/v1/uploads/{dataset_id}/publish` | Makes a private dataset visible to **all** users — potential public disclosure of sensitive data. |

> **Delete endpoints are intentionally omitted.** This skill does not document
> `DELETE /api/v1/uploads/{dataset_id}`, `DELETE /api/v1/plots/{plot_id}`, or
> `POST /api/v1/plots/bulk-delete` to prevent automated data loss. Do not call
> them. Direct users to the EpidBot web UI at
> `https://kwar-ai.com.br/epidbot` to manage deletion manually.

## Authentication

### Option 1: API Key (Recommended for agents)

1. Login to EpidBot web interface at https://kwar-ai.com.br/epidbot
2. Go to Settings -> API Keys -> Create new API key
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

### Option 3: OAuth

EpidBot supports OAuth login. Check configured providers:

```bash
curl "$EPIDBOT_BASE_URL/api/v1/auth/oauth-providers"
# Response: {"providers": [{"name": "google", "label": "Google"}]}
```

Redirect users to `$EPIDBOT_BASE_URL/api/v1/auth/oauth/{provider}` to start the flow.

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
{"type": "poll", "payload": {"job_id": "..."}}
{"type": "clarification_response", "payload": {"session_id": 1, "response": "..."}}
```

**Server -> Client Messages:**

```json
{"type": "thinking", "data": {"content": "..."}}
{"type": "tool_start", "data": {"tool": "...", "job_id": null, "timeout": 240}}
{"type": "tool_complete", "data": {"tool": "...", "duration_ms": 123, "result": {...}}}
{"type": "job_started", "data": {"job_id": "...", "status": "processing"}}
{"type": "job_result", "data": {"job_id": "...", "result": {...}}}
{"type": "chunk", "data": {"content": "..."}}
{"type": "complete", "data": {"content": "...", "images": [], "usage": {...}}}
{"type": "clarification_ack", "data": {"session_id": 1}}
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

### search

Search across chat messages and code snippets.

**Endpoint:** `POST /api/v1/search`

**Request:**
```json
{
  "query": "dengue São Paulo",
  "source_type": "message",
  "session_id": null,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
```

- `source_type`: `"message"`, `"snippet"`, or `null` for both
- `session_id`: filter to a specific session (optional)

**Output:**
```json
{
  "message_results": [
    {
      "source_type": "message",
      "session_id": 1,
      "session_name": "Dengue Analysis",
      "message_id": 5,
      "role": "assistant",
      "content": "Dengue cases in São Paulo...",
      "created_at": "2024-06-15T10:00:00Z"
    }
  ],
  "snippet_results": []
}
```

### uploads

Upload custom data files for analysis. Supported formats: CSV, ODS, XLSX, XLS (tabular), GeoJSON, JSON, GPKG, ZIP (GIS). Max 50 MB. Files are auto-converted to parquet for querying.

> **Privacy notice:** Uploading transmits the file to the external EpidBot
> service. Confirm the data does not contain unconsented personally
> identifiable or regulated health information before uploading. Apply data
> minimization (remove unnecessary columns/rows) and prefer de-identified data.
> See [Safety & Data Handling](#safety--data-handling).

**Upload a file:** `POST /api/v1/uploads`

```bash
curl -X POST "$EPIDBOT_BASE_URL/api/v1/uploads" \
  -H "X-API-Key: $EPIDBOT_API_KEY" \
  -F "file=@data.csv" \
  -F "name=sinan_aggregated_2023" \
  -F "description=Aggregated dengue case counts by municipality"
```

**List user datasets:** `GET /api/v1/uploads`

**Get dataset info:** `GET /api/v1/uploads/{dataset_id}`

**Update description:** `PATCH /api/v1/uploads/{dataset_id}`

**Publish dataset (make public):** `POST /api/v1/uploads/{dataset_id}/publish`

> **Public disclosure risk.** Publishing makes the dataset visible to **all**
> EpidBot users. Confirm the user has verified the dataset contains no
> sensitive, identifiable, or regulated data before publishing. This cannot be
> auto-reversed by this skill.

### plots

Manage generated plots and images. Upload custom images or list plots generated by the agent.

**List plots:** `GET /api/v1/plots`

**Upload a plot image:** `POST /api/v1/plots/upload` (PNG, JPG, WebP, GIF, SVG — max 20 MB)

**Get plot info:** `GET /api/v1/plots/{plot_id}`

**Update plot metadata:** `PATCH /api/v1/plots/{plot_id}`

**Download plot:** `GET /api/v1/plots/{plot_id}/download`

### catalog

List available datasets from the data catalog with metadata (row counts, column counts, file sizes). Designed for IDE data browser integration.

**List datasets:** `GET /api/v1/catalog/datasets`

**Query parameters:** `search` (filter by name), `limit` (max 200, default 50)

**Output:**
```json
[
  {
    "id": 1,
    "name": "sinan_dengue_2023",
    "path": "/data/pysus/sinan_dengue_2023.parquet",
    "row_count": 150000,
    "column_count": 42,
    "file_size_bytes": 52428800
  }
]
```

**Export dataset as CSV:** `GET /api/v1/catalog/datasets/{dataset_id}/csv`

### jobs

List and poll background jobs (e.g., manuscript writing, dataset enrichment).

**List jobs:** `GET /api/v1/jobs`

**Query parameters:** `job_type` (filter by type), `status` (filter by status), `limit` (max 200)

**Get job by ID:** `GET /api/v1/jobs/{job_id}`

**Output:**
```json
{
  "id": "job_abc123",
  "job_type": "manuscript",
  "status": "completed",
  "session_id": 5,
  "result": {"content": "..."},
  "error": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:05:00Z"
}
```

### usage

Check token quota and usage history.

**Get usage:** `GET /api/v1/usage`

**Query parameters:** `limit` (max 200, default 50)

**Output:**
```json
{
  "quota": {
    "tokens_used": 15000,
    "tokens_limit": 100000,
    "consultations_used": 20,
    "consultations_limit": 50,
    "reset_date": "2024-01-02",
    "is_allowed": true
  },
  "recent_usage": [
    {
      "id": 1,
      "tokens_input": 500,
      "tokens_output": 200,
      "tokens_total": 700,
      "model": "gpt-4",
      "session_id": 1,
      "created_at": "2024-01-01T10:00:00Z"
    }
  ],
  "warnings": []
}
```

### knowledge base

Manage the knowledge base: search documents, add content, browse wiki, run audits.

**Get KB status:** `GET /api/v1/kb/status`

**List collections:** `GET /api/v1/kb/collections`

**Search KB:** `POST /api/v1/kb/search`

```json
{"query": "dengue transmission", "limit": 10}
```

**Add document:** `POST /api/v1/kb/documents`

**Add URL:** `POST /api/v1/kb/urls`

**Browse wiki:** `GET /api/v1/kb/wiki`

**Query wiki:** `GET /api/v1/kb/wiki/query?q=topic`

**Ingest wiki page:** `POST /api/v1/kb/wiki/ingest`

**Run audit:** `POST /api/v1/kb/audit`

**List audit flags:** `GET /api/v1/kb/audit/flags`

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

### Brazilian (DATASUS/PySUS)
- **SINAN**: Disease notifications (dengue, Zika, chikungunya, measles, etc.)
- **SIM**: Mortality data
- **SIH**: Hospital admissions
- **SIA**: Outpatient procedures
- **CNES**: Health facilities
- **PNI**: Vaccination coverage
- **CIHA**: Hospital care records
- **SINASC**: Live birth records

### International
- **WHO/GHO**: Global health indicators
- **PAHO**: Immunization, malaria, dengue, health indicators for the Americas
- **ECDC**: European disease surveillance
- **ECDC Atlas**: Disease and antimicrobial resistance atlas data
- **World Bank**: Development indicators
- **HealthData.gov**: US hospital capacity, COVID metrics, nursing homes, vaccination, testing
- **Eurostat**: Mortality, life expectancy, healthcare expenditure, physicians, hospital beds
- **NZ Health**: New Zealand mortality, hospital events, life tables, immunisation

### Environmental/Vector
- **Mosqlimate/InfoDengue**: Dengue surveillance, climate data, vegetation, mosquito indices, ARIMA/LSTM/ensemble forecasts
- **GBIF**: Species occurrence records

### Genomic
- **Pathoplexus**: Genomic sequence data for pathogens

### Geographic
- **GADM**: Administrative boundary shapefiles (global)
- **IBGE**: Brazilian census and demographic data

### Literature
- **OpenAlex**: Academic literature search
- **PubMed**: Biomedical literature
- **Zotero**: Reference management

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

## Limitations

- **Job expiry**: Chat jobs expire after 1 hour
- **Response time**: Simple queries take 30s–3min; complex data analysis can take up to 5 minutes. Always poll with exponential backoff.
- **File sizes**: Large data exports may be limited by memory constraints
- **Sandbox execution**: Python/SQL code execution happens in an isolated sandbox with resource limits

## Support

- Homepage: https://kwar-ai.com.br/epidbot
- GitHub: https://github.com/fccoelho/EpiDBot
