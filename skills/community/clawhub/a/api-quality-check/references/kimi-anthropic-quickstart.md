# Kimi Anthropic Quickstart

Use this for Moonshot Kimi coding endpoints that expose an Anthropic-compatible API root such as:

- `https://api.kimi.com/coding/`

## Important limitation in this skill

Anthropic mode is treated as `B3IT-only` in this skill.

That means:

- `smoke` can verify whether the endpoint returns usable first-token text
- `b3it-baseline` and `b3it-detect` can run if first-token text is usable
- `lt-baseline` and `lt-detect` do not apply here

## Minimal provider.json

```json
{
  "provider": "Anthropic",
  "base_url": "https://api.kimi.com/coding/",
  "api_key": "YOUR_KIMI_KEY",
  "model_id": "kimi-k2.5"
}
```

## Generate the config from CLI

```bash
python "$APIQ" init-config \
  --provider "Anthropic" \
  --base-url "https://api.kimi.com/coding/" \
  --api-key "$API_KEY" \
  --model-id "kimi-k2.5" \
  --config-output ./provider.json
```

## Smoke test

```bash
python "$APIQ" smoke \
  --config ./provider.json \
  --output ./smoke.json \
  --html-output ./smoke.html
```

Interpret the result like this:

- if `b3it_supported=true`, you can continue with B3IT
- if `first_token_text` is empty, the endpoint is not usable for this skill's B3IT flow
- `lt_supported` will stay `false` by design in Anthropic mode here

## B3IT baseline and detect

```bash
python "$APIQ" b3it-baseline \
  --config ./provider.json \
  --output ./b3it-baseline.json \
  --html-output ./b3it-baseline.html
```

```bash
python "$APIQ" b3it-detect \
  --config ./provider.json \
  --baseline ./b3it-baseline.json \
  --output ./b3it-report.json \
  --html-output ./b3it-report.html \
  --detection-repeats 5 \
  --min-stable-count 2 \
  --min-stable-ratio 0.35 \
  --confirm-passes 1
```

## Daily drift check

```bash
bash "$APIQ_DAILY" ./provider.json ./daily-out kimi-k2.5-anthropic
```

## Notes

- If the endpoint returns empty text blocks, this skill will treat it as unsupported for B3IT.
- If you need LT-style logprob tracking, use the OpenAI-compatible Kimi coding endpoint instead.
