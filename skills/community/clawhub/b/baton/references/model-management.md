# Baton model management

Baton model access is managed outside `openclaw.json`.

## Commands

```bash
node skills/baton/scripts/baton-setup.mjs --config openclaw.json
node skills/baton/scripts/baton-model-manager.mjs scan --config openclaw.json --write
node skills/baton/scripts/baton-model-manager.mjs list
node skills/baton/scripts/baton-model-manager.mjs add anthropic/claude-sonnet-4-6 --write
node skills/baton/scripts/baton-model-manager.mjs remove openai/gpt-5-mini --write
node skills/baton/scripts/baton-model-manager.mjs tier strong_reasoning add anthropic/claude-sonnet-4-6 --write
node skills/baton/scripts/baton-model-manager.mjs tier code remove openai/gpt-5-mini --write
node skills/baton/scripts/baton-model-manager.mjs prune-missing --write
```

## Conversation patterns

The main agent should translate natural language to these operations:

- "Rescan models" -> `scan --write`.
- "Allow Baton to use X" -> `add X --write`.
- "Remove X" -> `remove X --write`.
- "Use X for coding" -> `tier code add X --write`.
- "Use X for writing" -> `tier creative add X --write`.
- "Don't use OpenAI for Baton" -> remove or block `openai/*` from Baton allowlist after confirming broad provider removal if destructive.

## Add/remove policy

- Adding a model does not modify OpenClaw's own allowlist. If OpenClaw rejects the model, add it through OpenClaw's supported config command first.
- Removing a model from Baton prevents Baton from explicitly selecting it. It does not remove it from OpenClaw.
- Rescans preserve allowed models unless `prune-missing` is requested.

## Agent-specific overlays

Use per-agent config when multiple main agents need different model policies:

```text
.openclaw/baton/agents/<agentId>/model-allowlist.json
.openclaw/baton/agents/<agentId>/baton.config.json
```

The overlay may add stricter blocks and different tier order. It should not silently expand beyond the global allowlist unless the user has explicitly opted into per-agent expansion.
