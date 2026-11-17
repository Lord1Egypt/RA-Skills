---
name: custom-llm-provider-setup
description: "Wire any OpenAI-compatible LLM API into Hermes Agent as a custom provider — Cloudflare Workers AI, self-hosted vLLM, Ollama, LM Studio, or any service that implements /v1/chat/completions."
version: 1.0.0
author: Hermes Agent (agent-created)
tags: [hermes, providers, openai-compatible, custom-endpoint, configuration]
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
    requires:
      bins: [curl]
---

# Custom LLM Provider Setup

Wire any OpenAI-compatible API endpoint into Hermes Agent. The
`provider: custom` path works with any service that implements
`/v1/chat/completions` — Cloudflare Workers AI, Ollama, vLLM,
LM Studio, Portkey, AI/ML API, and dozens more.

## When to Use

- The provider is **not** in Hermes's built-in list (OpenRouter,
  Anthropic, Gemini, etc.)
- It speaks OpenAI wire-format (`/v1/chat/completions`)
- You just need a base URL + API key — no custom auth flow

If the provider has its own auth (OAuth refresh, token exchange,
non-Bearer scheme), you need a built-in provider or a plugin
instead — see `hermes-agent/SKILL.md` → Adding Providers.

## ⚠️ Critical: API Key Location

**The `custom` provider only reads `OPENAI_API_KEY` from `.env` when
the endpoint host is `openai.com` or `openai.azure.com`.** This is a
deliberate host-gated credential guard to prevent leaking your OpenAI
key to arbitrary endpoints (source: `hermes_cli/runtime_provider.py`).

For any other endpoint (Cloudflare, Ollama, vLLM, LM Studio, etc.)
the API key MUST be in `model.api_key` inside `config.yaml`, or in a
named entry under `providers:`.

### Option A: Inline `model.api_key` (simple, single provider)

```yaml
# ~/.hermes/config.yaml
model:
  provider: custom
  default: "your-model-id"
  base_url: "https://your-endpoint/v1"
  api_key: "your-api-token"
```

Set via CLI:

```bash
hermes config set model.provider custom
hermes config set model.base_url "https://your-endpoint/v1"
hermes config set model.default "your-model-id"
hermes config set model.api_key "your-api-token"
```

### Option B: Named `providers:` entry (recommended for multiple)

Keeps several endpoints switchable without rewriting config each time:

```yaml
# ~/.hermes/config.yaml
providers:
  my-provider:
    model: "your-model-id"
    base_url: "https://your-endpoint/v1"
    api_key: "your-api-token"
    context_length: 131072   # optional: override context window
```

Switch to it:

```bash
hermes config set model.provider my-provider
hermes config set model.default "your-model-id"
```

Both `providers:` (newer dict format) and `custom_providers:` (legacy
list format) are supported.

### Context length

If your model has a non-standard context window (e.g. Kimi K2.6 has
262k), set it explicitly so Hermes doesn't truncate or use defaults:

```bash
hermes config set model.context_length 262144
```
Or per-provider in the `providers:` entry.

## Verify the Endpoint

Before wiring it into Hermes, confirm the endpoint speaks OpenAI
format:

```bash
curl -s --request POST \
  --url "https://your-endpoint/v1/chat/completions" \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "Say hello in one word"}],
    "max_tokens": 10
  }' | python3 -m json.tool
```

Expected: `{"object": "chat.completion", "choices": [...]}`.

If the endpoint has a non-standard URL path (e.g. requires an
account ID in the path, or uses a different prefix), inspect
the provider's OpenAI-compatibility docs — see `references/`
for per-provider guides.

## Switching Models After Setup

```bash
hermes config set model.default "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
```

Or use `/model` inside a running Hermes session.

## Caveats

- **API key host-gating**: The `OPENAI_API_KEY` env var is ONLY
  forwarded to `openai.com` / `openai.azure.com` hosts. For any
  other endpoint, use `model.api_key` in config.yaml or a
  `providers:` named entry (see ⚠️ Critical above).
- **Model id format**: Some providers require a prefix (`@cf/...`,
  `@hf/...`). Use whatever the provider's docs say for model ID.
- **Fresh session needed**: Config changes need a new Hermes
  session (`/reset` or start a new `hermes` process).
- **Non-chat endpoints**: Embeddings and text completions are not
  covered here — Hermes uses chat completions for the agent loop.

## Free-tier and multi-model validation

- A model catalog — the provider's own or a third-party's — proves visibility, not callability. Families may need one-time registration, deployments may be missing for your account, and "free" listings can turn out paid. Probe every candidate model with a minimal chat completion before building any configuration around it.
- Probe big reasoning models with `"stream": true` — on free tiers they can queue for minutes before the first byte, and a non-streaming probe dies with a meaningless timeout. `000` = no HTTP answer at all (inconclusive — retry streaming with a longer cap); `403` = model family not registered for your key (register it via the provider's model page); `404` = deployment not found for your account (dead — exclude the model).
- A `200` probe does not prove the model is usable in agent practice. The authoritative tests are `hermes chat -Q --provider <p> -m <model> -q "Reply with the single word OK"` (the prompt MUST go through `-q`; a bare positional prompt after `-Q` is rejected as an unrecognized argument) and, above that, the user's own interactive trials. The user owns the roster decision — present probe results and wait; never auto-commit multi-model architecture (MOA presets, fallback chains) onto models that have not passed a live probe, because a council of models that hang is pure added latency.
- The inverse also holds: a `500` on a bare probe does NOT prove a model is broken. A minimal probe (no tools, no streaming, tiny `max_tokens`) is not representative of agent traffic — models behind a Responses-API-only transport fail `chat_completions` probes while working fine in real sessions. Before declaring a model unreachable, check the provider's own model list (absence there is a real verdict; a 500 alone is not), try the other endpoint (`/responses` vs `/chat/completions`), and weight real in-session traffic above any probe. Probe failures are probe-scoped findings until corroborated — label them as such in any report, because wrongly calling a working model dead silently removes it from the fleet.
- Announce expected wall-time before launching sequential probe loops — each probe can consume its full `--max-time`, so a six-model loop can run 10+ minutes.
- When migrating an existing stack, sweep every LLM consumer, not just `model.*` — the full procedure is in `references/provider-migration-sweep.md`.
- When a provider exposes several tiers under one key, price-shape the fleet before picking models: check which models are flat-priced versus peak/off-peak (DeepSeek-style 2x peak penalties), then route the highest-volume slots (delegation defaults, aux tasks) through flat-priced models. A model with a usage cap or promo allowance is a natural delegation default — short child contexts fit its limits. Confirm slot changes with `hermes config set` and re-read the final config.yaml to verify every key landed (the CLI silently refuses some protected global keys — retry with `--force` and diff against your intended values).

## See Also

- `references/` — per-provider setup recipes and model identity tracing
- `references/provider-model-tracing.md` — how to discover the underlying model behind an opaque alias (proxy providers, server-routed names, and when to give up)
- `references/provider-migration-sweep.md` — full-stack provider migration: backup, sweeping aux/delegation/cron/moa/profile pins, RPM sizing, and the verification chain
- `hermes-agent/SKILL.md` — general Hermes configuration reference
- [Hermes Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)
