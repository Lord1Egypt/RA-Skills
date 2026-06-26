# Auth and Provider — Deep Infra

## Goal

Connect an OpenAI-compatible workflow to DeepInfra with explicit auth checks and zero secret leakage in notes.

## Verification Flow

1. Confirm `DEEPINFRA_API_KEY` is present in the environment.
2. Run a lightweight models request to confirm API availability.
3. Record only pass/fail and timestamp in memory.

## Minimal Request Pattern

```bash
curl -sS https://api.deepinfra.com/v1/openai/models | jq '.data | length'
```

## Provider Wiring Checklist

- Endpoint uses `https://api.deepinfra.com/v1/openai/`.
- Authorization header uses bearer token from environment variable.
- API is OpenAI-compatible; most OpenAI SDKs work by switching the base URL.
- Client timeout and retry strategy are explicit.
- Default model is set per workload class, not globally for all tasks.

## OpenClaw CLI Setup

```bash
openclaw onboard --deepinfra-api-key <key>
```

Or set the environment variable directly:

```bash
export DEEPINFRA_API_KEY="<your-deepinfra-api-key>"
```

## Common Auth Failures

- Missing key in current shell session -> source environment and retry.
- Wrong header format -> enforce `Authorization: Bearer ...`.
- Silent proxy mismatch -> test direct path before debugging client wrappers.
- Expired or revoked key -> rotate key at https://deepinfra.com/ dashboard and re-run minimal verification.
