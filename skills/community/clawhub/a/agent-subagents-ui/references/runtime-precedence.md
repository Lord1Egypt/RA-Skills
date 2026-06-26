# Runtime precedence

Keep the Subagents panel aligned with the actual model-selection code.

## Current precedence

From `src/agents/model-selection.ts`:

### `resolveSubagentConfiguredModelSelection(...)`
Order:
1. `agentConfig?.subagents?.model`
2. `cfg.agents?.defaults?.subagents?.model`
3. `agentConfig?.model`

### `resolveSubagentSpawnModelSelection(...)`
Order:
1. explicit spawn-time model override
2. configured subagent model selection from the function above
3. `resolveAgentModelPrimaryValue(cfg.agents?.defaults?.model)`
4. runtime default provider/model

## UI implications

- Per-agent subagent model override should be shown as the highest-priority editable value.
- Shared `agents.defaults.subagents.model` should be shown as inherited fallback, not as the selected agent's primary model.
- The selected agent primary model should be shown as the next inherited value when no subagent-specific model is configured.
- Do not claim that subagents always use the global default model. They do not.

## Limits

The current UI feature intentionally keeps these as shared defaults:
- `maxConcurrent`
- `maxSpawnDepth`
- `maxChildrenPerAgent`

If backend schema later adds per-agent limits, update the panel and this reference together.
