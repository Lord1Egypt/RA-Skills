# GC Provider Install Guide

This reference condenses the public GrowthCircle AI Console docs and the
`gc-provider` plugin README into an operator runbook.

## Public References

- GrowthCircle AI Console: `https://d.growc.id/llms/ai-console.md`
- Member dashboard: `https://growthcircle.id/app/ai`
- Inference API: `https://ai.growthcircle.id`
- OpenClaw plugin source: `https://github.com/Growth-Circle/gc-provider`

## Key And Model Discovery

GrowthCircle AI keys are created in the member AI Console. Plaintext keys are
shown once. Store them in an environment variable, OpenClaw auth flow, Hermes
secret store, or another private runtime secret mechanism.

Discover model IDs with the same key that will be used for inference:

```sh
curl https://ai.growthcircle.id/v1/models \
  -H "Authorization: Bearer $GROWTHCIRCLE_API_KEY"
```

Use returned model IDs exactly. Free, Paid, and Team/Patungan keys can return
different catalogs. For OpenClaw text model refs, prefix the returned model id:

```text
growthcircle/<model-id-from-v1-models>
```

Important Team/Patungan rule: do not use Free or Paid fallback IDs with a team
key unless the exact ID is returned by `/v1/models` for that same team key.

## OpenClaw Native Install

Requirements:

- OpenClaw `2026.5.4` or newer.
- Node.js 20 or newer in environments that install from npm/source.
- `GROWTHCIRCLE_API_KEY` configured through the OpenClaw auth flow or runtime
  environment.

Recommended update-or-install path:

```sh
(openclaw plugins update gc-provider || openclaw plugins install clawhub:gc-provider --force)
openclaw plugins enable gc-provider
openclaw gateway restart
openclaw configure --section=model
```

Npm fallback:

```sh
openclaw plugins install gc-provider@latest --force
openclaw plugins enable gc-provider
openclaw gateway restart
openclaw configure --section=model
```

Local source development:

```sh
npm install
npm run build
openclaw plugins install -l . --force
openclaw plugins enable gc-provider
openclaw gateway restart
openclaw configure --section=model
```

Verify:

```sh
openclaw plugins list
openclaw models list --provider growthcircle
```

If plugin allowlist blocks non-bundled plugins:

```sh
openclaw config set plugins.allow '["gc-provider"]' --strict-json
openclaw gateway restart
```

If other plugins are already allowed, preserve them in the same JSON array.

## Hermes Manual Configuration

`gc-provider` is an OpenClaw plugin. In Hermes, configure GrowthCircle as a
manual OpenAI-compatible provider.

Example Hermes-style config:

```yaml
providers:
  growthcircle:
    base_url: https://ai.growthcircle.id/v1
    api_key_env: GROWTHCIRCLE_API_KEY
    models:
      - model-id-from-v1-models
provider: growthcircle
model: model-id-from-v1-models
```

Then keep the key private:

```sh
export GROWTHCIRCLE_API_KEY="<growthcircle-ai-key>"
```

Verify with a small API request:

```sh
curl https://ai.growthcircle.id/v1/chat/completions \
  -H "Authorization: Bearer $GROWTHCIRCLE_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "model-id-from-v1-models",
    "messages": [
      { "role": "user", "content": "Reply with one short sentence." }
    ]
  }'
```

## Hermes To OpenClaw Migration

OpenClaw migration can import Hermes model configuration and skills with a
`SKILL.md` file under `skills/<name>/`. It does not automatically trust Hermes
plugin state as executable OpenClaw code.

Preview first:

```sh
openclaw migrate hermes --dry-run
```

Apply after review:

```sh
openclaw migrate apply hermes --yes
openclaw doctor
openclaw gateway restart
openclaw status
```

After migration, install the native provider:

```sh
openclaw plugins install clawhub:gc-provider --force
openclaw plugins enable gc-provider
openclaw gateway restart
openclaw configure --section=model
```

## Common Errors

- `401`: missing, invalid, or revoked AI key.
- `403`: key scope, plan, policy, or model entitlement does not allow the
  request.
- `429`: rate limit, quota, cooldown, or rolling free quota window.
- `503`: requested model or generation path is temporarily unavailable.
- OpenClaw model picker does not update after install: restart gateway and
  rerun model discovery.
- Team image/video model mismatch: use only the exact model IDs returned by
  that team key.
