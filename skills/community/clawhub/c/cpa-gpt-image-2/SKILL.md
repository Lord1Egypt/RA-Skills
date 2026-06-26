---
name: cpa-gpt-image-2
description: Use a text model such as gpt-5.4 with the image_generation tool over an OpenAI-compatible /v1/responses endpoint, matching the CPA blog example. Do not call gpt-image-2 as a direct model on gateways that do not expose it.
---

# cpa-gpt-image-2

Use this skill when image generation should go through the **CPA blog pattern**: a normal text model invokes the `image_generation` tool over a compatible `/v1/responses` endpoint.

## What this skill does

- sends a request to an OpenAI-compatible `/v1/responses` endpoint
- matches the CPA blog example request shape closely
- uses the `image_generation` tool
- defaults to model `gpt-5.4`
- prefers **non-streaming** mode by default for simpler and more stable parsing
- can switch to streaming mode when needed
- automatically retries short image rate-limit responses
- automatically retries transient `tools: []` text fallbacks from the gateway
- keeps credentials in environment variables, never in the skill files

## Important rule

Do **not** treat `gpt-image-2` as the direct model on gateways that do not expose that model.

Correct pattern:
- use a normal model such as `gpt-5.4`
- pass `tools: [{"type": "image_generation", "output_format": "png"}]`
- let the gateway/tool layer decide whether image generation is available

Wrong pattern for this gateway:
- directly calling model `gpt-image-2` when the provider does not publish that model

## Default environment resolution

The script resolves credentials in this order.

Base URL:
- `IMAGE_GEN_BASE_URL`
- `OTCBOT_BASE_URL`
- `CPA_BASE_URL`
- `OPENAI_BASE_URL`
- fallback to OpenClaw `models.json` otcbot provider baseUrl

API key:
- `IMAGE_GEN_KEY`
- `OTCBOT_API_KEY`
- `CPA_API_KEY`
- `OPENAI_API_KEY`
- fallback to OpenClaw `models.json` otcbot provider apiKey

Model default:
- `IMAGE_GEN_MODEL`
- `OTCBOT_IMAGE_MODEL`
- `CPA_MODEL`
- fallback to current OpenClaw image/default model
- final fallback: `gpt-5.4`

Optional:
- `IMAGE_GEN_OUTPUT_FORMAT` — default `png`
- `CPA_SESSION_ID` — session id header value, default `test-session`
- `CPA_USER_AGENT` — custom user-agent header
- `CPA_VERSION` — request header `version`, default `0.122.0`
- `CPA_ORIGINATOR` — request header `originator`, default `codex_cli_rs`

The script calls:

- `${BASE_URL%/}/v1/responses`

## Default execution path

Use the bundled script:

```bash
python3 skills/cpa-gpt-image-2/scripts/generate_image.py \
  --prompt "画一只可爱的松鼠" \
  --output /tmp/squirrel.png \
  --model gpt-5.4
```

Recommended env contract:

```bash
export IMAGE_GEN_BASE_URL='http://192.168.10.8:8317/v1'
export IMAGE_GEN_KEY='sk-xxxx'
export IMAGE_GEN_MODEL='gpt-5.4'
```

Override model when needed:

```bash
python3 skills/cpa-gpt-image-2/scripts/generate_image.py \
  --prompt "a cinematic fox detective in Bangkok neon rain" \
  --output /tmp/fox.png \
  --model gpt-5.4 \
  --format png
```

## Expected behavior

The script:

1. reads credentials from env or OpenClaw otcbot defaults
2. POSTs to `/v1/responses`
3. sends codex-style headers: `user-agent`, `version`, `originator`, `session_id`
4. requests the `image_generation` tool, defaulting to `stream: false`
5. parses normal JSON, or SSE `data:` payloads when streaming is enabled
6. auto-retries short `rate_limit_exceeded` image responses when the server provides a retry delay
7. auto-retries transient gateway fallbacks where the tool list comes back empty and the response degrades to text
8. extracts the first base64 image from the response
9. writes the file to the requested output path

## Fallback curl patterns

Preferred non-streaming version:

```bash
curl --location "$IMAGE_GEN_BASE_URL/responses" \
  --header "Authorization: Bearer $IMAGE_GEN_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5.4",
    "input": "画一只可爱的松鼠",
    "tools": [
      {
        "type": "image_generation",
        "output_format": "png"
      }
    ],
    "instructions": "you are a helpful assistant",
    "tool_choice": "auto",
    "stream": false,
    "store": false
  }'
```

Streaming version when needed:

```bash
curl --location "$IMAGE_GEN_BASE_URL/responses" \
  --header "Authorization: Bearer $IMAGE_GEN_KEY" \
  --header "user-agent: ${CPA_USER_AGENT:-codex-tui/0.122.0 (Manjaro 26.1.0-pre; x86_64) vscode/3.0.12 (codex-tui; 0.122.0)}" \
  --header "version: ${CPA_VERSION:-0.122.0}" \
  --header "originator: ${CPA_ORIGINATOR:-codex_cli_rs}" \
  --header "session_id: ${CPA_SESSION_ID:-test-session}" \
  --header 'accept: text/event-stream' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5.4",
    "input": "画一只可爱的松鼠",
    "tools": [
      {
        "type": "image_generation",
        "output_format": "png"
      }
    ],
    "instructions": "you are a helpful assistant",
    "tool_choice": "auto",
    "stream": true,
    "store": false
  }'
```

## Notes

- Prefer the bundled script for repeatability.
- Do not hardcode live keys, base URLs, or session ids into workspace docs.
- This skill intentionally mirrors the CPA blog example request shape as closely as practical.
- On this gateway, prefer `gpt-5.4` plus `image_generation` tool instead of direct `gpt-image-2` model calls.
- For the known local otcbot endpoint, prefer setting `OTCBOT_BASE_URL` and `OTCBOT_API_KEY` explicitly when testing.
- If the endpoint returns provider-specific SSE events, extend the SSE parser instead of changing the whole request shape.
- If the user asks to send the generated file back in the current chat, use the normal file-delivery flow after generation.
