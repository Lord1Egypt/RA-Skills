---
name: aistatus
description: Check real-time AI provider status, search model availability, get trending models, LLM benchmark leaderboard, and recent outage incidents. Use when the user asks about AI service status, whether a provider is down, model availability, or AI rankings.
user-invocable: true
allowed-tools: WebFetch
argument-hint: [provider-or-model-name]
---

# AI Status - Real-time AI Provider Status & Model Availability

You have access to the aistatus.cc API to check real-time AI provider status, model availability, trending usage, and benchmark scores. All endpoints are free, public, and require no authentication.

**Base URL:** `https://aistatus.cc`

## When to Use

- User asks if an AI provider (Anthropic, OpenAI, Google, DeepSeek, etc.) is up or down
- User wants to check model availability or pricing
- User asks about trending AI models or usage rankings
- User asks about LLM benchmark scores or leaderboard
- User wants to know about recent AI outages or incidents
- Before making API calls to a provider, check if it's operational

## Available Endpoints

### 1. All Data (recommended first call)

```
GET https://aistatus.cc/api/all
```

Returns everything in one call: provider status, trending models, MMLU leaderboard, and recent incidents. Use this when the user asks a general question or you need multiple data points.

### 2. Provider Status

```
GET https://aistatus.cc/api/status
```

Returns operational status for each AI provider. Status values:
- `operational` - All systems healthy
- `degraded` - Minor issues reported
- `down` - Major/critical outage
- `unknown` - Insufficient data

Providers tracked: Anthropic, OpenAI, Google, DeepSeek, Meta, Mistral, xAI, Qwen, MiniMax, StepFun, Moonshot, ByteDance.

### 3. Model Search

```
GET https://aistatus.cc/api/model?q={query}
```

Search for models by name or ID. Returns matching models with provider status, pricing, and context length. Supports fuzzy matching. Up to 20 results.

Examples:
- `?q=claude-sonnet` - Find Claude Sonnet models
- `?q=gpt-4o` - Find GPT-4o models
- `?q=deepseek-chat` - Find DeepSeek models

### 4. Trending Models

```
GET https://aistatus.cc/api/trending
```

Top 10 most-used AI models this week by token volume on OpenRouter.

### 5. LLM Leaderboard (Benchmarks)

```
GET https://aistatus.cc/api/mmlu
```

Top 10 models by benchmark score from HuggingFace Open LLM Leaderboard (average of IFEval, BBH, MATH, GPQA, MUSR, MMLU-PRO).

### 6. Recent Incidents

```
GET https://aistatus.cc/api/incidents
```

Recent provider status change events (outages, degradations, recoveries). Stored in-memory, up to 50 events.

## How to Respond

1. Use `WebFetch` to call the appropriate endpoint
2. Parse the JSON response
3. Present the information clearly:
   - For status checks: show each provider with a status indicator
   - For model search: show matching models with provider, pricing, and availability
   - For trending: show the ranked list with token volumes
   - For leaderboard: show the ranked list with scores
   - For incidents: show a timeline of recent events

If the user provides `$ARGUMENTS`, use it to determine what to check:
- If it looks like a provider name (e.g., "anthropic", "openai"), fetch `/api/status` and highlight that provider
- If it looks like a model name (e.g., "claude-sonnet", "gpt-4o"), fetch `/api/model?q={name}`
- If it's "trending" or "rankings", fetch `/api/trending`
- If it's "leaderboard" or "benchmark", fetch `/api/mmlu`
- If it's "incidents" or "outages", fetch `/api/incidents`
- Otherwise, fetch `/api/all` for a comprehensive overview

## Example Output Format

When showing provider status:

```
AI Provider Status (as of HH:MM UTC):

  Anthropic    - operational (13 models)
  OpenAI       - degraded    (58 models) - Partial System Degradation
  Google       - operational (45 models)
  DeepSeek     - operational (12 models)
  ...

310 models tracked total.
```

When showing model search results:

```
Found 3 models matching "claude-sonnet":

1. anthropic/claude-sonnet-4.6
   Provider: Anthropic (operational)
   Context: 1,000,000 tokens
   Pricing: $3.00/M input, $15.00/M output

2. ...
```
