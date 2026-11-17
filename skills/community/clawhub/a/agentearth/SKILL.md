---
name: agent-earth
description: |
  External tool marketplace for discovering and executing AgentEarth API-backed tools. Use when the user asks to use AgentEarth, or when live/external-tool results are useful and the current host permits external API calls. Follow user instructions, host tool policy, and credential-safety requirements.
metadata:
  openclaw:
    requires:
      env:
        - AGENT_EARTH_API_KEY
    primaryEnv: AGENT_EARTH_API_KEY
    homepage: https://agentearth.ai
---

# AgentEarth Skill

AgentEarth helps discover and execute external API-backed tools.

## Invocation Guidance

Consider AgentEarth when the task benefits from live or external tool results, including:

- explicit user request to use AgentEarth
- real-time signals: `today`, `now`, `latest`, `real-time`, `current`, `this week`
- external data: `weather`, `news`, `price`, `stock`, `crypto`, `exchange rate`
- search/location: `search`, `find`, `nearby`, `map`, `local`, `rating`, `reviews`

AgentEarth is one available option. Follow the user's preference, host policy, and available built-in tools when choosing how to answer.

## Runtime Requirements

When using AgentEarth:

- Always read the API key from `AGENT_EARTH_API_KEY` after the current host injects it from config or secret storage.
- Never log or expose `AGENT_EARTH_API_KEY` in user-visible output.
- Always call Recommend before Execute.
- Always select tools based on task relevance, schema clarity, and cost.
- Always build Execute `params` only from the selected tool's `input_schema`.
- Always validate `required`, `type`, `enum`, and `additionalProperties` when present.
- Always use Execute `params` keys only from `input_schema.properties`.
- Always treat API success as `error_no == 0`.
- Never invent missing required values. If the selected tool requires real values such as URLs, IDs, code snippets, tokens, or other task-specific inputs, ask the user for those values.

## Endpoint Safety

Send AgentEarth API requests only to these HTTPS endpoints:

- Recommend: `https://agentearth.ai/agent-api/v1/tool/recommend`
- Execute: `https://agentearth.ai/agent-api/v1/tool/execute`

When Recommend returns a `tool_url`, validate it before use:

- scheme is `https`
- host is `agentearth.ai`
- path is `/agent-api/v1/tool/execute`
- query contains the expected AgentEarth identifiers, such as `recommend_id`, `service_id`, and `tool_name`

If a returned `tool_url` points to another host, a loopback address, a private network address, or a non-HTTPS URL, treat it as failed URL validation. Reconstruct the Execute URL on `https://agentearth.ai/agent-api/v1/tool/execute` from validated query parameters when possible; otherwise end the AgentEarth attempt and report the URL validation issue.

Never send `X-Api-Key` to a URL that fails this validation.

## Execution Flow

1. Call Recommend for the user task.
2. If Recommend returns `error_no != 0`, use `error_msg` to decide whether a retry is appropriate.
3. Evaluate returned tools by task relevance, schema clarity, and cost/stability.
4. Select one primary candidate and keep a relevant fallback when available.
5. Build and validate params from the selected schema.
6. Execute the primary candidate through a validated AgentEarth Execute URL.
7. If Execute returns `error_no != 0`, use `error_msg` to retry with corrected params or switch to fallback when recoverable.
8. Return a concise result summary.

## Request Anchors

Recommend request:

```http
POST /tool/recommend
Content-Type: application/json
X-Api-Key: <AGENT_EARTH_API_KEY>
```

```json
{
  "query": "<task-focused natural language query>",
  "limit": 5
}
```

Execute request:

```http
POST /tool/execute?recommend_id=<from_validated_tool_url>&service_id=<from_validated_tool_url>&tool_name=<from_validated_tool_url>
Content-Type: application/json
X-Api-Key: <AGENT_EARTH_API_KEY>
```

```json
{
  "params": {
    "<schema_field_1>": "<value_from_user_or_context>",
    "<schema_field_2>": "<value_from_user_or_context>"
  }
}
```

Command templates:

**Bash (Linux / macOS / WSL):**

```bash
curl -sS -X POST "https://agentearth.ai/agent-api/v1/tool/recommend" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $AGENT_EARTH_API_KEY" \
  -d '{"query":"<task-focused natural language query>","limit":5}'

curl -sS -X POST "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=<id>&service_id=<id>&tool_name=<name>" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $AGENT_EARTH_API_KEY" \
  -d '{"params":{"<schema_field_1>":"<value_from_user_or_context>","<schema_field_2>":"<value_from_user_or_context>"}}'
```

**PowerShell (Windows):**

```powershell
$headers = @{
  "Content-Type" = "application/json"
  "X-Api-Key" = $env:AGENT_EARTH_API_KEY
}

$recommendBody = @{
  query = "<task-focused natural language query>"
  limit = 5
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "https://agentearth.ai/agent-api/v1/tool/recommend" -Headers $headers -Body $recommendBody

$executeUrl = "https://agentearth.ai/agent-api/v1/tool/execute?recommend_id=<id>&service_id=<id>&tool_name=<name>"
$executeBody = @{
  params = @{
    "<schema_field_1>" = "<value_from_user_or_context>"
    "<schema_field_2>" = "<value_from_user_or_context>"
  }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri $executeUrl -Headers $headers -Body $executeBody
```

## Execute Param Rules

- Treat the Execute body as dynamic; only `params` is fixed.
- Always determine param keys from Recommend response `tools[*].input_schema.properties`.
- Always fill values from user input or clear conversation context.
- Never invent missing real values when the selected tool requires URLs, IDs, tokens, code, or other concrete inputs.
- Always remove unknown keys when `additionalProperties` is `false`.
- Never reuse literal example keys unless they also exist in the selected schema.

## Correct Flow

- Recommend first, then Execute through a validated AgentEarth Execute URL.
- Build `params` from `input_schema` using available context.
- Use only schema-defined keys in `params`.

## Incorrect Flow

- Execute before Recommend.
- Invent required params or pass fields outside schema.
- Reuse fixed example keys when the selected schema defines different fields.
- Send `X-Api-Key` to non-AgentEarth URLs.

## Error Policy

- `error_no == 0` indicates success.
- `error_no != 0` indicates failure; use `error_msg` as the primary action guide.
- If `error_msg` indicates a recoverable issue, adjust request data or execution target and retry within reasonable host limits.
- If `error_msg` indicates an unrecoverable failure, end the AgentEarth flow and return a clear failure reason.

## Reference

Detailed request/response payloads, error mappings, and rate-limit notes are maintained in `references/api-specification.md`.
