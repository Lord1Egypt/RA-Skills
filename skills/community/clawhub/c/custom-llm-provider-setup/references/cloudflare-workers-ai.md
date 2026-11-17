# Cloudflare Workers AI — Hermes Custom Provider

Cloudflare Workers AI offers a generous free tier of serverless LLM
inference. It exposes an **OpenAI-compatible** endpoint at:

```
https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1
```

This means Hermes can use it via `provider: custom` with no plugin.

## Quick Setup

### Option A: Inline (single provider)

```bash
hermes config set model.provider custom
hermes config set model.base_url "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/v1"
hermes config set model.default "@cf/meta/llama-3.1-8b-instruct"
hermes config set model.api_key "YOUR_API_TOKEN"
```

### Option B: Named entry in `providers:` (recommended)

Keeps Cloudflare switchable alongside other providers:

```yaml
# ~/.hermes/config.yaml
providers:
  cloudflare:
    model: "@cf/moonshotai/kimi-k2.6"
    base_url: "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/v1"
    api_key: "YOUR_API_TOKEN"
    context_length: 262144    # Kimi K2.6 has 262k context
```

```bash
hermes config set model.provider cloudflare
hermes config set model.default "@cf/moonshotai/kimi-k2.6"
```

**IMPORTANT**: Do NOT use `OPENAI_API_KEY` env var for Cloudflare.
Hermes only forwards `OPENAI_API_KEY` to `openai.com` hosts.
The key must be in `model.api_key` in config.yaml or in a
`providers:` named entry (see custom-llm-provider-setup/SKILL.md
→ ⚠️ Critical).

## API Format

Standard OpenAI chat completions. The `model` parameter uses
`@cf/...` prefixed IDs:

```bash
curl -s --request POST \
  --url "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/ai/v1/chat/completions" \
  --header "Authorization: Bearer ${API_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "@cf/meta/llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

Response shape: `{ "object": "chat.completion", "choices": [...], "usage": {...} }`

## Notable Text-Generation Models

| Model ID | Notes |
|---|---|
| `@cf/openai/gpt-oss-120b` | OpenAI's open-weight reasoning model |
| `@cf/openai/gpt-oss-20b` | Lighter sibling |
| `@cf/meta/llama-4-scout-17b-16e-instruct` | Multimodal MoE |
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | Fast quantized 70B |
| `@cf/meta/llama-3.1-8b-instruct` | Solid general-purpose |
| `@cf/qwen/qwen2.5-72b-instruct` | Strong reasoning |
| `@cf/qwen/qwen2.5-coder-32b-instruct` | Coding-focused |
| `@cf/mistralai/mistral-small-3.1-24b-instruct` | Mistral Small |
| `@cf/moonshotai/kimi-k2.6` | 1T params, 262k ctx, tool calling |
| `@cf/zhipuai/glm-4.7-flash` | 131k ctx, multilingual |
| `@hf/google/gemma-2-27b-it` | Google Gemma |

Full catalog: https://developers.cloudflare.com/workers-ai/models/

## Native (Non-OpenAI) API

Workers AI also has a native REST API at a different endpoint —
useful for non-chat tasks:

```
POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct
```

This is NOT needed for Hermes setup since Hermes speaks OpenAI
format via the `/ai/v1` endpoint above.

## Docs

- OpenAI compatibility: https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/
- Native REST API: https://developers.cloudflare.com/workers-ai/get-started/rest-api/
- Models catalog: https://developers.cloudflare.com/workers-ai/models/
