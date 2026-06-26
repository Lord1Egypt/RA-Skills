# Baton model discovery and user selection

Baton must not assume which providers or models exist. Before model routing is enabled in a workspace, Baton should build a local allowlist from the operator's actual `openclaw.json`.

## Goals

1. Discover every concrete model ref that appears in `openclaw.json`.
2. Normalize model refs to OpenClaw's `provider/model` format.
3. Show the discovered models to the user.
4. Let the user select exactly which models Baton may use.
5. Store the selection outside `openclaw.json` to avoid strict-schema failures.
6. Route sub-agents only through this Baton allowlist.

OpenClaw model refs use `provider/model`. `agents.defaults.models` can act as an allowlist when configured, but Baton keeps its own routing allowlist in `.openclaw/baton/model-allowlist.json` so it does not inject unknown keys into `openclaw.json`.

## Files

Recommended local files:

```text
.openclaw/baton/discovered-models.json
.openclaw/baton/model-allowlist.json
.openclaw/baton/model-routing-ledger.jsonl
```

`discovered-models.json` is generated. `model-allowlist.json` is user-selected and should be reviewed before committing.

## Discovery sources

Scan, at minimum:

- `agents.defaults.model.primary`
- `agents.defaults.model.fallbacks[]`
- `agents.defaults.subagents.model`
- `agents.defaults.models` alias maps/arrays/objects
- `agents.list[].model`
- `agents.list[].subagents.model`
- `models.providers.<provider>.models[]`
- `models.providers.<provider>.models{}` object keys
- any string values under `models.providers` that are already valid `provider/model` refs

For provider catalog entries, normalize by joining provider id and model id:

```text
models.providers.openai.models[].id = "gpt-5-mini"
=> openai/gpt-5-mini
```

Accept only normalized refs matching:

```regex
^[A-Za-z0-9_.-]+/[A-Za-z0-9_.:\/-]+$
```

## User selection flow

When Baton has no allowlist yet, or the user asks to change Baton models:

1. Run discovery against the active `openclaw.json`.
2. Present discovered models grouped by provider.
3. Ask the user to choose which models Baton may use.
4. Ask the user to map selected models to routing tiers, or auto-suggest tier mapping:
   - `fast`
   - `balanced`
   - `code`
   - `long_context`
   - `strong_reasoning`
   - `creative`
   - `multimodal`
5. Save `.openclaw/baton/model-allowlist.json`.
6. Use only models in that file for future `sessions_spawn.model` values.

If the user selects no model for a tier, Baton may leave that tier unset. For unset tiers, either use a selected fallback tier or omit `sessions_spawn.model` and rely on OpenClaw's configured default, but only after telling the user that tier-specific routing is incomplete.

## Allowlist schema

```json
{
  "version": 2,
  "updatedAt": "2026-06-13T00:00:00.000Z",
  "allowedModels": [
    "openai/gpt-5-mini",
    "anthropic/claude-sonnet-4-6"
  ],
  "tiers": {
    "fast": { "models": ["openai/gpt-5-mini"], "fallback": "balanced", "maxAttempts": 2 },
    "balanced": { "models": ["anthropic/claude-sonnet-4-6"], "fallback": "strong_reasoning", "maxAttempts": 2 },
    "code": { "models": ["anthropic/claude-sonnet-4-6"], "fallback": "strong_reasoning", "maxAttempts": 2 },
    "long_context": { "models": [], "fallback": "strong_reasoning", "maxAttempts": 2 },
    "strong_reasoning": { "models": ["anthropic/claude-sonnet-4-6"], "fallback": null, "maxAttempts": 2 },
    "creative": { "models": [], "fallback": "balanced", "maxAttempts": 2 },
    "multimodal": { "models": [], "fallback": "long_context", "maxAttempts": 1 }
  },
  "blockedModels": [],
  "notes": "Baton must not use models outside allowedModels."
}
```

## Selection rules

- Never route to a model that is not in `allowedModels`.
- Prefer tier-specific candidates in order.
- If a tier is empty, escalate to `strong_reasoning` if present for safety-critical tasks.
- If no safe selected model exists, ask the user to update the allowlist or omit the model override and use the agent default only for low-risk tasks.
- Validator and Security Reviewer should preferably use a selected model from a different provider or model family than the Implementer.
- When the spawn result includes a resolved model, compare it to the selected requested model. If it differs, record the mismatch and retry or warn depending on risk.

## Prompt to user

Use this format after discovery:

```text
I found these configured OpenClaw models:

openai
1. openai/gpt-5-mini
2. openai/gpt-5.1

anthropic
3. anthropic/claude-sonnet-4-6
4. anthropic/claude-opus-4-6

Reply with the numbers Baton may use, e.g. `1,3,4`, or say `all`.
Optional: add tier mapping, e.g. `fast=1 balanced=3 strong=4 code=3`.
```

## Non-interactive mode

For unattended setup, support:

```bash
node skills/baton/scripts/baton-model-select.mjs --config openclaw.json --all --write
node skills/baton/scripts/baton-model-select.mjs --config openclaw.json --select openai/gpt-5-mini,anthropic/claude-sonnet-4-6 --write
```

## Important OpenClaw compatibility note

Do not write Baton-specific keys into `openclaw.json`. OpenClaw performs strict config validation and may refuse to start when unknown keys are added.

## Rescan and modification commands

Use `baton-model-manager.mjs scan --write` to rescan, `add`/`remove` to modify allowed models, `tier <tier> add|remove` to change routing tiers, and `baton-router.mjs route --lease` to pick a rate-limit-aware model for a child task.
