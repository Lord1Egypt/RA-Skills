---
name: axion
description: "Forecast the probability of a future event with the Axion API. Use when asked the odds, likelihood, or a prediction for an uncertain or future event."
version: 1.0.2
license: MIT
metadata: { "openclaw": { "primaryEnv": "AXION_API_KEY", "requires": { "env": ["AXION_API_KEY"], "bins": ["curl"] }, "emoji": "🔮", "homepage": "https://axion.eternis.ai/docs" }, "hermes": { "tags": ["Forecasting", "Predictions", "Research", "Markets"], "requires_toolsets": ["terminal"] } }
required_environment_variables:
  - name: AXION_API_KEY
    prompt: Axion API key
    help: Create one at https://axion.eternis.ai → API Keys (any account; add credits first)
    required_for: Calling the Axion forecasting API
---

# Axion forecasting

Axion answers a question by running an orchestrator and a team of research agents (web search, market data, SEC filings, Fermi estimates) that cite their evidence and return graded probabilistic forecasts.

## When to use

Use Axion when the user wants the odds of a future event, a deal or scenario evaluated, or a research-backed estimate: "how likely is X", "forecast whether Y", "what are the odds of Z", elections, markets, deals, geopolitics, product launches.

## Setup

1. Create an account at https://axion.eternis.ai and create an API key on the API Keys page. Any account can create keys.
2. Add credits. API usage is prepaid and billed separately from the monthly plan; new accounts start at zero.
3. Provide the key as the `AXION_API_KEY` environment variable.

Before calling, confirm the key is present. If `AXION_API_KEY` is empty, stop and ask the user to set it. Do not proceed.

## Procedure

Forecasts run asynchronously: start one, then poll until it reaches a terminal status. Base URL `https://api.axion.eternis.ai`; the key is a Bearer token on every request.

1. Start a forecast:

```bash
curl -s https://api.axion.eternis.ai/forecasts \
  -H "Authorization: Bearer $AXION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "Will the Fed cut rates in June 2026?", "effort": "high"}'
```

Returns `{"id": "<token>", "status": "starting"}` — `id` is an opaque token (e.g. `L2d5qNdtxXjyjXGKTmKVMX`), no fixed prefix. Use it to poll. Set `effort` `low`/`medium`/`high` and `max_forecasts` 1–10 to widen the run.

2. Poll until `status` is `completed` or `failed`, backing off a few seconds between calls:

```bash
curl -s https://api.axion.eternis.ai/forecasts/<id> \
  -H "Authorization: Bearer $AXION_API_KEY"
```

3. Read `forecasts[]`. Each carries `forecast_text`, `probability` (0–1), `confidence_lower`/`confidence_upper`, `resolution_date`, and `reasoning`. Present the probability and the reasoning behind it.

Full request and response fields, webhooks, and credit rates: see [references/axion-api.md](references/axion-api.md), mirrored from https://axion.eternis.ai/docs.md.

## Pitfalls

- A positive credit balance is required to start a forecast. A 402 with an insufficient-credits message means add credits at https://axion.eternis.ai.
- A run takes roughly 15 seconds to 3 minutes. Poll with backoff; do not block.
- Maximum 10 concurrent in-progress threads per account (429 otherwise).
- The key is read from the environment. Never print or hard-code it. In sandboxed runs, make sure `AXION_API_KEY` is provided to the sandbox, not only to the host.
- Successful responses are valid JSON, but a transient `5xx` (an upstream reset at the ingress) can return a short plain-text body instead of the usual `{"error": ...}` envelope. Check the HTTP status before parsing; on a non-2xx, retry the same request a few times with backoff rather than parsing the body as JSON.

## Verification

A successful run ends with `status` `completed` and a non-empty `forecasts[]` array carrying probabilities between 0 and 1.
