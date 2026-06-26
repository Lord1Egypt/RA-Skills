# Endpoint Types Playbook

Use this guide when you want a vendor-neutral workflow. Providers such as Ark/Volcengine, GLM, DeepSeek, Kimi, SiliconFlow, OpenRouter, and similar platforms are examples only. The workflow is organized by protocol type, not by vendor brand.

## 1. OpenAI

Use this when the endpoint behaves like the official OpenAI API.

Typical signs:

- provider type is `OpenAI`
- base URL looks like `https://api.openai.com/v1`
- auth is bearer-token style

Minimal flow:

1. Generate or write `provider.json`.
2. Run `smoke`.
3. If `lt_supported=true`, run `lt-baseline` and `lt-detect`.
4. If `b3it_supported=true`, run `b3it-baseline` and `b3it-detect`.
5. For recurring checks, use `run_daily_check.sh`.

Example:

```bash
python "$APIQ" init-config \
  --provider "OpenAI" \
  --base-url "https://api.openai.com/v1" \
  --api-key "$API_KEY" \
  --model-id "gpt-4.1" \
  --config-output ./provider.json
```

## 2. OpenAI-Compatible

Use this when the endpoint is not OpenAI itself, but follows the same request/response shape.

Typical signs:

- provider type is `OpenAI-Compatible`
- base URL may be a vendor API root or a full `.../chat/completions` URL
- auth is usually bearer-token style
- some vendors require custom `headers` or `extra_body`

This is the most common path for vendor endpoints such as Ark/Volcengine, GLM, DeepSeek-compatible services, Kimi coding, SiliconFlow, and similar gateways.

Minimal flow:

1. Generate or write `provider.json`.
2. If the vendor requires custom request headers, add them in `headers` or pass `--headers-json`.
3. Run `smoke`.
4. If the endpoint returns normal first-token text, B3IT can run.
5. If the endpoint also returns `logprobs`, LT can run.
6. For repeated checks, prefer `run_daily_check.sh` or batch workflows.

Example:

```bash
python "$APIQ" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://example-vendor.com/v1/chat/completions" \
  --api-key "$API_KEY" \
  --model-id "example-model" \
  --config-output ./provider.json
```

Header-required variant:

```bash
python "$APIQ" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://example-vendor.com/coding/v1" \
  --api-key "$API_KEY" \
  --model-id "example-model" \
  --headers-json '{"User-Agent":"ExampleCLI/1.0.0"}' \
  --config-output ./provider.json
```

Kimi-specific note:

- use `{"User-Agent":"KimiCLI/2.0.0"}` only when the address is under `https://api.kimi.com/coding`
- for the OpenAI-compatible Kimi endpoint, the base URL should be `https://api.kimi.com/coding/v1`

## 3. Anthropic

Use this when the endpoint follows Anthropic-style `/v1/messages` semantics.

Typical signs:

- provider type is `Anthropic`
- auth uses `x-api-key`
- the API path resolves to `/v1/messages`

In this skill, Anthropic mode is `B3IT-only`.

That means:

- run `smoke` first
- if `b3it_supported=true`, run `b3it-baseline` and `b3it-detect`
- do not expect `lt_supported=true`

Example:

```bash
python "$APIQ" init-config \
  --provider "Anthropic" \
  --base-url "https://example-vendor.com/" \
  --api-key "$API_KEY" \
  --model-id "example-model" \
  --config-output ./provider.json
```

## Shared operational rules

Apply these rules regardless of vendor:

1. Never commit real API keys. Use `$API_KEY`, `YOUR_API_KEY`, or sanitized placeholders in docs and sample files.
2. Treat vendor names as examples. Choose the workflow by protocol type first.
3. Run `smoke` before any baseline or detect step.
4. Save baselines to explicit files and reuse them for comparisons.
5. Use daily or batch wrappers when you need repeatable monitoring.

## Decision shortcut

- Need official OpenAI semantics: use `OpenAI`
- Need a third-party OpenAI-shaped endpoint: use `OpenAI-Compatible`
- Need Anthropic-style `/messages`: use `Anthropic`
