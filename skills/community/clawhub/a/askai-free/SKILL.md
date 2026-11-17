---
name: askai-free
description: Use the AskAI.free API to ask available ChatGPT, Claude, and DeepSeek models, list the live model catalogue, or check token usage. Use when the user explicitly wants AskAI.free or wants a model through their AskAI account; do not use for unrelated AI requests or ASKAI media-workspace operations.
metadata:
  openclaw:
    requires:
      env:
        - ASKAI_API_KEY
      bins:
        - curl
    primaryEnv: ASKAI_API_KEY
    envVars:
      - name: ASKAI_API_KEY
        required: true
        description: AskAI.free API key for a paid Pro or Max account.
    emoji: "✨"
    homepage: https://askai.free/openclaw-skill
---

# AskAI.free

Use the authenticated AskAI.free REST API at `https://askai.free`. It provides a single interface to the ChatGPT, Claude, and DeepSeek models enabled for the user's AskAI plan.

## Before the first request

Require `ASKAI_API_KEY`. If it is missing, tell the user how to create one; do not ask them to paste the secret into chat.

1. Sign in at <https://askai.free/account>.
2. Open the API Access card and create a key.
3. Copy it when shown and set it locally as `ASKAI_API_KEY`.

API keys are available only to verified, paying Pro and Max accounts after the first successful subscription payment. A free trial does not include API access. API calls spend the same monthly token allowance as the AskAI website; there is no separate API balance.

Treat the key as a secret. Never print it, include it in a URL, commit it, or send it to any host other than `https://askai.free`. Use the `Authorization: Bearer $ASKAI_API_KEY` header.

## Workflow

1. If the user did not give an exact model id, call `GET /v1/models`. Choose an entry with `available: true`; prefer `chatgpt-5-6-sol` when it is present, otherwise use the first suitable available model.
2. Build a messages array from the user's request. Preserve their text and intent. Add a system message only when it materially helps or the user requested one.
3. Call `POST /v1/chat/completions` with `stream: false`. Use `max_tokens: 1000` by default, increasing it only when the requested output needs more detail.
4. Return `choices[0].message.content`. Do not expose the authorization header or unnecessary raw response metadata.
5. Call `GET /v1/usage` only when the user asks about their plan or remaining allowance, or when diagnosing an insufficient-token response.

## Endpoints

### List models

```bash
curl --fail-with-body --silent --show-error \
  https://askai.free/v1/models \
  -H "Authorization: Bearer $ASKAI_API_KEY"
```

The response contains `data[]` entries with `id`, `name`, `provider`, `token_multiplier`, and `available`. Do not select a model whose `available` value is false.

### Create a chat completion

```bash
curl --fail-with-body --silent --show-error \
  https://askai.free/v1/chat/completions \
  -H "Authorization: Bearer $ASKAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @request.json
```

Write `request.json` as valid JSON rather than interpolating unescaped user text into a shell command:

```json
{
  "model": "chatgpt-5-6-sol",
  "messages": [
    {"role": "user", "content": "The user's request"}
  ],
  "max_tokens": 1000,
  "stream": false
}
```

Delete temporary request files after use when the environment does not manage them automatically. The response follows the OpenAI chat-completions shape. Usage includes `askai_tokens_charged` and `askai_tokens_remaining`.

### Check usage

```bash
curl --fail-with-body --silent --show-error \
  https://askai.free/v1/usage \
  -H "Authorization: Bearer $ASKAI_API_KEY"
```

This returns the plan, remaining tokens, monthly allowance, and rate limit. Model listing and usage checks do not consume model tokens.

## Errors and limits

- `401 missing_api_key` or `invalid_api_key`: explain that the local key is missing, wrong, or revoked. Do not repeat it.
- `403 trial`: API access begins after the first successful subscription payment.
- `403 not_pro`: the account needs an active Pro or Max plan.
- `404 model_not_found`: refresh `/v1/models` and choose a current model id.
- `413 context_length_exceeded`: shorten or split the input.
- `429 insufficient_tokens`: check `/v1/usage`; do not retry repeatedly.
- `429 ratelimit`: wait before one bounded retry.
- `503 model_unavailable`: choose another available model or report the temporary outage.

Streaming is not supported. Do not use this API for image generation, media-library browsing, subscription changes, or destructive account operations. Direct users to <https://askai.free/api> for the maintained API documentation.
