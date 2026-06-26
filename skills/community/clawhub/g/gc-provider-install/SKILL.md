---
name: gc-provider-install
description: Install, repair, or manually configure the GrowthCircle.id gc-provider for OpenClaw and Hermes. Use this whenever a user asks to connect GrowthCircle AI Console keys, install gc-provider, configure GrowthCircle as an OpenAI-compatible provider, migrate from Hermes to OpenClaw, verify GrowthCircle model discovery, or troubleshoot GrowthCircle free/paid/team model access.
metadata:
  growthcircle:
    ai_console_docs: https://d.growc.id/llms/ai-console.md
    plugin_package: gc-provider
    provider_id: growthcircle
    endpoint: https://ai.growthcircle.id/v1
    openclaw_min_version: "2026.5.4"
---

# GC Provider Install

Use this skill to guide an operator through installing or repairing
`gc-provider` and configuring GrowthCircle.id AI keys safely. Keep the
instructions practical and key-aware: GrowthCircle model availability depends on
the exact AI key used.

## Source Of Truth

Use these public sources before inventing behavior:

- GrowthCircle AI Console docs: `https://d.growc.id/llms/ai-console.md`
- Plugin README/source: `https://github.com/Growth-Circle/gc-provider`
- In this skill, read `references/install-guide.md` for the compact install and
  troubleshooting runbook.

## Safety Rules

- Never ask the user to paste a GrowthCircle AI key into public chat, a public
  repo, logs, screenshots, or frontend code.
- Tell the user to create, rotate, label, and revoke keys from
  `https://growthcircle.id/app/ai`.
- Always discover models with the same key that will make requests:
  `GET https://ai.growthcircle.id/v1/models`.
- Do not guess Free, Paid, or Team model IDs. Team/Patungan keys must use only
  model IDs returned by that team key.
- Do not map a Team/Patungan key to Free/Paid fallback IDs. If the team model is
  missing, fail closed and ask the operator to check the team package.
- Prefer `gc-provider` in OpenClaw. Use a manual OpenAI-compatible provider only
  for Hermes or as a temporary fallback before the native plugin is installed.

## Workflow

1. Identify the target runtime.
   - OpenClaw: install or update the native `gc-provider` plugin.
   - Hermes: configure GrowthCircle manually as an OpenAI-compatible provider,
     because `gc-provider` is an OpenClaw plugin.
   - Hermes to OpenClaw migration: keep the skill under
     `skills/gc-provider-install/SKILL.md`, migrate skills, then install the
     native OpenClaw plugin after migration.

2. Confirm the key source.
   - Ask the user to create the key in GrowthCircle AI Console.
   - Keep secrets in environment variables or the runtime's credential store.
   - Use `GROWTHCIRCLE_API_KEY` for OpenClaw native plugin installs.

3. Discover valid model IDs.
   - Run `/v1/models` with the same key.
   - Use returned IDs exactly.
   - For OpenClaw text models, refs use `growthcircle/<model-id>`.

4. Install or configure.
   - For OpenClaw, use the update-or-install command in
     `references/install-guide.md`.
   - For Hermes, use the manual OpenAI-compatible provider notes in
     `references/install-guide.md`.

5. Verify.
   - OpenClaw: check plugin state, restart gateway, and list GrowthCircle
     models.
   - Hermes: send a small chat/completion request with the configured base URL,
     key, and a model returned by `/v1/models`.

## OpenClaw Quick Path

Use this idempotent path for a new install, tracked update, or repair of a stale
copy:

```sh
(openclaw plugins update gc-provider || openclaw plugins install clawhub:gc-provider --force)
openclaw plugins enable gc-provider
openclaw gateway restart
openclaw configure --section=model
openclaw models list --provider growthcircle
```

If OpenClaw says `plugins.allow is empty`, add the provider to the allowlist
without removing other plugins:

```sh
openclaw config set plugins.allow '["gc-provider"]' --strict-json
openclaw gateway restart
```

## Hermes Quick Path

Hermes can use GrowthCircle through a manual OpenAI-compatible provider
configuration:

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

Keep the API key in the environment or Hermes secret mechanism:

```sh
export GROWTHCIRCLE_API_KEY="<growthcircle-ai-key>"
curl https://ai.growthcircle.id/v1/models \
  -H "Authorization: Bearer $GROWTHCIRCLE_API_KEY"
```

If the user is migrating Hermes to OpenClaw, do not treat Hermes plugins as
trusted executable code in OpenClaw. Import skills/config through the migration
flow, then install `gc-provider` through OpenClaw:

```sh
openclaw migrate hermes --dry-run
openclaw migrate apply hermes --yes
openclaw plugins install clawhub:gc-provider --force
openclaw plugins enable gc-provider
openclaw gateway restart
```

## Troubleshooting Priorities

- `401`: missing, invalid, or revoked GrowthCircle key.
- `403`: key scope, plan, policy, or model entitlement does not allow the
  request.
- `429`: quota, rate limit, cooldown, or rolling free window.
- `503`: model/path temporarily unavailable.
- OpenClaw install looks updated but model list is stale: restart
  `openclaw-gateway` and re-run model discovery.
- Team key does not show expected model: verify `/v1/models` with that exact
  team key before blaming the plugin.

## Output Style

When helping a user:

- Give commands in the order they should be run.
- Redact secrets in examples.
- State whether the path is OpenClaw-native or Hermes-manual.
- Include verification commands, not only install commands.
- If the user asks for a one-shot fix, execute the install/update and
  verification when you have shell access.
