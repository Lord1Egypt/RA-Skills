---
name: ai-video
description: Build and execute skills.video video generation REST requests from OpenAPI specs. Use when user needs to create, debug, or document video generation calls on open.skills.video.
license: MIT
metadata:
  openclaw:
    author: skills-video
    os:
      - linux
      - darwin
    requires:
      env:
        - SKILLS_VIDEO_API_KEY
      bins:
        - python3
        - curl
    primaryEnv: SKILLS_VIDEO_API_KEY
    cliHelp: |
      Configure API key:
      export SKILLS_VIDEO_API_KEY="your_api_key_here"
      Verify:
      python scripts/ensure_api_key.py
    config:
      stateDirs:
        - ~/.openclaw
      example: "Required env vars: SKILLS_VIDEO_API_KEY. Store the key in OpenClaw skill env or shell env and do not hardcode it in files."
    links:
      repository: https://github.com/skills-video/skills
      homepage: https://skills.video
---

# ai-video

## Overview
Use this skill to turn OpenAPI definitions into working video-generation API calls for `skills.video`.
Prefer deterministic extraction from `openapi.json` instead of guessing fields.

## Prerequisites
1. Obtain an API key at: `https://skills.video/dashboard/developer`
2. Configure `SKILLS_VIDEO_API_KEY` before using the skill.

Preferred OpenClaw setup:

- Open the skill settings for `ai-video`
- Add an environment variable named `SKILLS_VIDEO_API_KEY`
- Paste the API key as its value

Equivalent config shape:

```json
{
  "skills": {
    "entries": {
      "ai-video": {
        "enabled": true,
        "env": {
          "SKILLS_VIDEO_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

Other valid ways to provide the key:

- **Shell**: `export SKILLS_VIDEO_API_KEY="your_api_key_here"`
- **Tool-specific env config**: any runtime that injects `SKILLS_VIDEO_API_KEY`

## Workflow
1. Check API key and bootstrap environment on first use.
2. Identify the active spec.
3. Select the SSE endpoint pair for a video model.
4. Extract request schema and generate a payload template.
5. Execute `POST /generation/sse/...` as default and keep the stream open.
6. If SSE does not reach terminal completion, poll `GET /generation/{id}` to terminal status.
7. Return only terminal result (`COMPLETED`/`SUCCEEDED`/`FAILED`/`CANCELED`), never `IN_PROGRESS`.
8. Apply retry and failure handling.

## 0) Check API key (first run)
Run this check before any API call.

```bash
python scripts/ensure_api_key.py
```

If `ok` is `false`, tell the user to:

- Follow the setup in `Prerequisites`

Example:

```bash
export SKILLS_VIDEO_API_KEY="<YOUR_API_KEY>"
```

## 1) Identify the spec
Load the most specific OpenAPI first.

- Prefer model-specific OpenAPI when available (for example `/v1/openapi.json` under a model namespace).
- Fall back to platform-level `openapi.json`.
- Use `references/open-platform-api.md` for base URL, auth, and async lifecycle.

## 2) Select a video endpoint
If `docs.json` exists, derive video endpoints from the `Videos` navigation group.
Use `default_endpoints` from the script output as the primary list (SSE first).

```bash
python scripts/inspect_openapi.py \
  --openapi /abs/path/to/openapi.json \
  --docs /abs/path/to/docs.json \
  --list-endpoints
```

When `docs.json` is unavailable, pass a known endpoint directly (for example `/generation/sse/kling-ai/kling-v2.6`).
Use `references/video-model-endpoints.md` as a snapshot list.

## 3) Extract schema and build payload
Inspect endpoint details and generate a request template from required/default fields.

```bash
python scripts/inspect_openapi.py \
  --openapi /abs/path/to/openapi.json \
  --endpoint /generation/sse/kling-ai/kling-v2.6 \
  --include-template
```

Use the returned `request_template` as the starting point.
Do not add fields not defined by the endpoint schema.
Use `default_create_endpoint` from output unless an explicit override is required.

## 4) Execute SSE request (default) with automatic fallback
Prefer the helper script. It creates via SSE and keeps streaming; if stream ends before terminal completion, it automatically switches to polling fallback.

```bash
python scripts/create_and_wait.py \
  --sse-endpoint /generation/sse/kling-ai/kling-v2.6 \
  --payload '{"prompt":"A cinematic dolly shot of neon city rain at night"}' \
  --poll-timeout 900 \
  --poll-interval 3
```

Treat SSE as the default result channel.
Do not finish the task on `IN_QUEUE` or `IN_PROGRESS`.
Return only after terminal result.

## 5) Fall back to polling
Use polling only if SSE cannot be established, disconnects early, or does not reach a terminal state.
Use `GET /generation/{id}` (or model-spec equivalent path if the OpenAPI uses `/v1/...`).

```bash
curl -X GET "https://open.skills.video/api/v1/generation/<GENERATION_ID>" \
  -H "Authorization: Bearer $SKILLS_VIDEO_API_KEY"
```

Stop polling on terminal states:

- `COMPLETED`
- `FAILED`
- `CANCELED`

Recommended helper:

```bash
python scripts/wait_generation.py \
  --generation-id <GENERATION_ID> \
  --timeout 900 \
  --interval 3
```

Return to user only after helper emits `event=terminal`.

## 6) Handle errors and retries
Handle these response codes for create, SSE, and fallback poll operations:

- `400`: request format issue
- `401`: missing/invalid API key
- `402`: possible payment/credits issue in runtime
- `404`: endpoint or generation id not found
- `422`: schema validation failed

Classify non-2xx runtime errors with:

```bash
python scripts/handle_runtime_error.py \
  --status <HTTP_STATUS> \
  --body '<RAW_ERROR_BODY_JSON_OR_TEXT>'
```

If category is `insufficient_credits`, tell the user to recharge:

- Open `https://skills.video/dashboard` and go to Billing/Credits
- Recharge or purchase additional credits
- Retry after recharge

Optional balance check:

```bash
curl -X GET "https://open.skills.video/api/v1/credits" \
  -H "Authorization: Bearer $SKILLS_VIDEO_API_KEY"
```

Apply retries only for transient conditions (network failure or temporary `5xx`).
Use bounded exponential backoff (for example `1s`, `2s`, `4s`, max `16s`, then fail).
Do not retry unchanged payloads after `4xx` validation errors.

## Rate limits and timeouts
Treat rate limits and server-side timeout windows as unknown unless documented in the active OpenAPI or product docs.
If unknown, explicitly note this in output and choose conservative client defaults.

## Resources
- `scripts/ensure_api_key.py`: validate `SKILLS_VIDEO_API_KEY` and show first-run setup guidance
- `scripts/handle_runtime_error.py`: classify runtime errors and provide recharge guidance for insufficient credits
- `scripts/inspect_openapi.py`: extract SSE/polling endpoint pair, contract, and payload template
- `scripts/create_and_wait.py`: create via SSE and auto-fallback to polling when stream does not reach terminal status
- `scripts/wait_generation.py`: poll generation status until terminal completion and return final response
- `references/open-platform-api.md`: SSE-first lifecycle, fallback polling, retry baseline
- `references/video-model-endpoints.md`: current video endpoint snapshot from `docs.json`
