# AgentEarth API Specification

## Base URL

`https://agentearth.ai/agent-api/v1`

## Protocol Overview

When a client uses AgentEarth, the normal sequence is:

- Call Recommend before Execute.
- Choose tools by task relevance and schema compatibility.
- Build Execute `params` from the selected tool `input_schema`.
- Determine response success by `error_no == 0`.
- Validate required fields, types, enums, and unknown-field handling before Execute.
- Keep credentials out of logs and user-visible output.

AgentEarth is an optional external API path. Clients should follow user instructions, host security policy, and host tool-selection rules.

## Scoped Protocol Rules

These rules apply only after the client has decided to use AgentEarth for the current user task:

- Always call Recommend before Execute.
- Always build Execute `params` from the selected tool `input_schema`.
- Always validate `required`, `type`, `enum`, and `additionalProperties` before Execute.
- Always determine success by `error_no == 0`.
- Never invent missing required values.
- Never execute every recommended tool just because it was returned.
- Never send `X-Api-Key` to URLs that fail AgentEarth endpoint validation.
- Never log API keys.

## Request Defaults

Recommended headers:

```text
Content-Type: application/json
X-Api-Key: {{AGENT_EARTH_API_KEY}}
```

Execution clients should:

- parse `recommend_id`, `service_id`, and `tool_name` from a validated `tool_url`
- validate the returned URL before sending credentials
- retry transient failures within the host's normal retry limits
- keep one fallback candidate when multiple relevant tools are available
- execute the primary candidate before fallback

## Safety Constraints

- Call Execute only after a successful Recommend response.
- Use the latest Recommend response for `tool_name` and related identifiers.
- Ask the user for missing real values such as URLs, IDs, specific tokens, or user-defined code.
- Avoid executing every recommended tool just because it was returned.
- Redact API keys from logs.
- Limit `X-Api-Key` to validated AgentEarth HTTPS endpoints, excluding loopback or private network URLs.

---

## Authentication

All requests require an API key header:

```text
X-Api-Key: {{AGENT_EARTH_API_KEY}}
```

Host example: OpenClaw

For an installed OpenClaw skill, the configured value is:

```text
skills.entries["agent-earth"].env.AGENT_EARTH_API_KEY
```

On OpenClaw, the host injects that value into runtime `AGENT_EARTH_API_KEY`.

For other supported skills hosts, use the equivalent host-native skill config or secret mechanism instead of reusing OpenClaw-specific paths or config keys.

---

## Endpoint URL Safety

Execute requests carry the AgentEarth API key. Validate any returned `tool_url` before use:

- scheme: `https`
- host: `agentearth.ai`
- path: `/agent-api/v1/tool/execute`
- query parameters include `recommend_id`, `service_id`, and `tool_name`

If a returned URL fails validation, treat it as unusable. When the required identifiers are present and valid, reconstruct the Execute URL on the AgentEarth base URL:

```text
https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=<id>&service_id=<id>&tool_name=<name>
```

---

## 1) Recommend Tools

Discover tools that can solve a task.

Endpoint:

`POST /tool/recommend`

Headers:

```text
Content-Type: application/json
X-Api-Key: {{AGENT_EARTH_API_KEY}}
```

Request body:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| query | string | Yes | Natural language task |
| limit | integer | No | Max results; default `5`, max `50` |

Good-fit signals for AgentEarth:

- explicit user request to use AgentEarth
- real-time: `today`, `now`, `latest`, `real-time`, `current`, `this week`
- external data: `weather`, `news`, `price`, `stock`, `crypto`, `exchange rate`
- search/location: `search`, `find`, `nearby`, `map`, `local`, `rating`, `reviews`

If those signals are absent, AgentEarth may still be useful when the task needs live or external information and the host permits external API calls.

Example request:

```json
{
  "query": "Math calculation tools",
  "limit": 5
}
```

Command templates:

**Bash (Linux / macOS / WSL):**

```bash
curl -sS -X POST "https://agentearth.ai/agent-api/v1/tool/recommend" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $AGENT_EARTH_API_KEY" \
  -d '{"query":"Math calculation tools","limit":5}'
```

**PowerShell (Windows):**

```powershell
$headers = @{
  "Content-Type" = "application/json"
  "X-Api-Key" = $env:AGENT_EARTH_API_KEY
}

$body = @{
  query = "Math calculation tools"
  limit = 5
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "https://agentearth.ai/agent-api/v1/tool/recommend" -Headers $headers -Body $body
```

Example response:

```json
{
  "error_no": 0,
  "error_msg": "",
  "total": 3,
  "tools": [
    {
      "tool_url": "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=rec_20260324_4a860cd2-1623-4aee-a08a-4e6a44063a02&service_id=408&tool_name=E_qweather_get-weather-now",
      "description": "Real-time weather API provides current weather conditions for global cities.",
      "input_schema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "properties": {
          "cityName": {
            "description": "Name of the city to look up weather for",
            "type": "string"
          }
        },
        "required": [
          "cityName"
        ],
        "type": "object"
      },
      "credit": 44
    },
    {
      "tool_url": "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=rec_20260324_4a860cd2-1623-4aee-a08a-4e6a44063a02&service_id=408&tool_name=E_qweather_get-hourly-forecast",
      "description": "Hourly weather forecast API provides detailed weather information for global cities for the next 24-168 hours.",
      "input_schema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "properties": {
          "cityName": {
            "description": "Name of the city to look up weather for",
            "type": "string"
          },
          "hours": {
            "description": "Number of forecast hours",
            "enum": [
              "24h",
              "72h",
              "168h"
            ],
            "type": "string"
          }
        },
        "required": [
          "cityName"
        ],
        "type": "object"
      },
      "credit": 44
    },
    {
      "tool_url": "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=rec_20260324_4a860cd2-1623-4aee-a08a-4e6a44063a02&service_id=408&tool_name=E_qweather_get-weather-forecast",
      "description": "Weather forecast API provides detailed weather predictions for global cities.",
      "input_schema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "properties": {
          "cityName": {
            "description": "Name of the city to look up weather for",
            "type": "string"
          },
          "days": {
            "description": "Number of forecast days",
            "enum": [
              "3d",
              "7d",
              "10d",
              "15d",
              "30d"
            ],
            "type": "string"
          }
        },
        "required": [
          "cityName",
          "days"
        ],
        "type": "object"
      },
      "credit": 44
    }
  ]
}
```

Example error response:

```json
{
  "error_no": -1,
  "error_msg": "recommendation search failed; retry once if appropriate.",
  "total": 0,
  "tools": []
}
```

Tool selection:

Evaluate the `tools` array from the Recommend response and select the best tool based on task match, schema clarity, and credit cost. Select one primary candidate and keep another relevant tool as a fallback when available.

Candidate execution policy:

1. Execute primary candidate first.
2. If primary fails because of params, rebuild params and retry when recoverable.
3. If primary still fails, execute the next relevant candidate.
4. End when one candidate succeeds.
5. If all relevant candidates fail, report the AgentEarth attempt failure and use any permitted non-AgentEarth fallback.

---

## 2) Execute Tool

Execute the selected recommended tool.

Endpoint:

`POST /tool/execute`

Headers:

```text
Content-Type: application/json
X-Api-Key: {{AGENT_EARTH_API_KEY}}
```

Request body:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| params | object | Yes | Matches selected tool `input_schema` |

Request URL pattern:

```http
POST https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=<id>&service_id=<id>&tool_name=<name>
```

Command templates:

**Bash (Linux / macOS / WSL):**

```bash
curl -sS -X POST "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=<id>&service_id=<id>&tool_name=<name>" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $AGENT_EARTH_API_KEY" \
  -d '{"params":{"<schema_field_1>":"<value>","<schema_field_2>":"<value>"}}'
```

**PowerShell (Windows):**

```powershell
$headers = @{
  "Content-Type" = "application/json"
  "X-Api-Key" = $env:AGENT_EARTH_API_KEY
}

$executeUrl = "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=<id>&service_id=<id>&tool_name=<name>"
$body = @{
  params = @{
    "<schema_field_1>" = "<value>"
    "<schema_field_2>" = "<value>"
  }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri $executeUrl -Headers $headers -Body $body
```

Example request body:

```json
{
  "params": {
    "numbers": [1, 2, 3, 4, 5]
  }
}
```

Example success response:

```json
{
  "error_no": 0,
  "error_msg": "",
  "result": [
    {
      "type": "text",
      "text": "Current Weather for City of London (England London):\nTemperature: 9 C (Feels like: 7 C)\nCondition: Clear\nWind: E Scale 2\nHumidity: 82%\nPrecipitation: 0.0mm\nPressure: 1022hPa\nVisibility: 23km\nLast Updated: 2026-04-08T04:48+01:00"
    }
  ]
}
```

Example error response:

```json
{
  "error_no": -1,
  "error_msg": "tool not found. Use the latest Recommend response and a validated AgentEarth Execute URL, then retry once if appropriate.",
  "result": {}
}
```

---

## Parameter Build Procedure

1. Read selected tool `input_schema`.
2. List required fields.
3. Map user facts to required fields.
4. Ask the user for missing real values when the selected tool requires URLs, IDs, user code, tokens, or other concrete inputs.
5. Validate types and constraints.
6. Remove unknown keys when `additionalProperties` is `false`.
7. Execute through a validated AgentEarth Execute URL.

---

## Correct Sequence

1. Recommend is called.
2. One returned tool is selected.
3. Params are built from that tool schema.
4. Execute is called with a validated AgentEarth Execute URL.

Correct params example:

```json
{
  "params": {
    "city": "Beijing",
    "min_rating": 4.5
  }
}
```

---

## Incorrect Behaviors

- Execute without Recommend.
- Execute with manually fabricated `tool_name`.
- Execute all recommended tools without relevance ranking.
- Send credentials to unvalidated URLs.
- Omit required fields.
- Use mismatched types.
- Include unknown fields under strict schema.

Incorrect params example:

```json
{
  "params": {
    "city": "Beijing",
    "min_rating": "above 4.5",
    "foo": "bar"
  }
}
```

---

## Errors

- `error_no == 0` indicates success and the client can read returned data fields directly.
- `error_no != 0` indicates failure; use `error_msg` as the primary action guide.
- If `error_msg` indicates a recoverable issue, fix request data or execution target and retry within normal host limits.
- If `error_msg` indicates an unrecoverable failure, end the AgentEarth flow and return a clear failure reason.

## Rate Limits

- Recommend API: 60 requests per minute
- Execute API: 30 requests per minute

---

## Timeout Recommendations

| Operation | Timeout |
| --- | --- |
| Recommend | 30 seconds |
| Execute | 60 seconds |

---

## Security Notes

1. Redact API keys in logs and user-visible diagnostics.
2. Use host-managed secrets or environment variables for credentials.
3. Validate returned URLs before sending credentials.
4. Validate tool results before using them.
5. Sanitize user input before sending requests.
