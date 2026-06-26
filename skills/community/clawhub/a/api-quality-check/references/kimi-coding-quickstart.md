# Kimi Coding Quickstart

Use this for Moonshot Kimi coding endpoints that expose an OpenAI-compatible API root such as:

- `https://api.kimi.com/coding/v1`

If you start from the Kimi coding base address `https://api.kimi.com/coding`, use the OpenAI-compatible form by appending `/v1`.

## Known requirement

For Kimi coding addresses under `https://api.kimi.com/coding`, add a client-like `User-Agent` header or the endpoint may return `403`.

Working example:

```json
{
  "headers": {
    "User-Agent": "KimiCLI/2.0.0"
  }
}
```

## Minimal provider.json

```json
{
  "provider": "OpenAI-Compatible",
  "base_url": "https://api.kimi.com/coding/v1",
  "api_key": "YOUR_KIMI_KEY",
  "model_id": "kimi-k2.5",
  "headers": {
    "User-Agent": "KimiCLI/2.0.0"
  }
}
```

## Generate the config from CLI

```bash
python "$APIQ" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://api.kimi.com/coding/v1" \
  --api-key "$API_KEY" \
  --model-id "kimi-k2.5" \
  --headers-json '{"User-Agent":"KimiCLI/2.0.0"}' \
  --config-output ./provider.json
```

## Smoke test

```bash
python "$APIQ" smoke \
  --config ./provider.json \
  --output ./smoke.json \
  --html-output ./smoke.html
```

Expected result for a usable endpoint:

- `b3it_supported=true`
- `lt_supported=true`
- `recommended_detector=LT-lite+B3IT-lite`

## Daily drift check

```bash
bash "$APIQ_DAILY" ./provider.json ./daily-out kimi-k2.5
```

This creates:

- stable baselines under `./daily-out/kimi-k2.5/baselines/`
- dated runs under `./daily-out/kimi-k2.5/runs/YYYY-MM-DD/`

## Notes

- Anthropic-compatible Kimi endpoints in this skill remain B3IT-only.
- If the endpoint still returns `403`, verify the key, model name, that the base URL is `https://api.kimi.com/coding/v1`, and that `User-Agent` is present.
- If B3IT is too noisy for your endpoint, keep the lower-false-positive defaults from the current script.
