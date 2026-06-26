---
name: agent-subagents-ui
description: "Add, extend, fix, or document the Subagents panel inside the OpenClaw Control UI Agents page. Use when implementing an Agents-page Subagents tab, wiring editable subagent settings into the existing config form/save flow, exposing subagent model and fallback settings, or keeping the UI aligned with runtime subagent model precedence in src/agents/model-selection.ts."
---

# Agent Subagents UI

Build and maintain the **Subagents** tab inside the OpenClaw **Agents** page.

## Scope

Use this skill for:
- adding or refining the **Subagents** tab under Agents
- exposing editable subagent model settings in Control UI
- wiring subagent settings into the existing config form/save path
- keeping the UI honest about what is configurable per-agent vs shared defaults
- documenting runtime precedence for subagent model selection

## Core design

Keep the feature aligned with the real runtime behavior.

Subagent model precedence is:
1. `agent.subagents.model`
2. `agents.defaults.subagents.model`
3. target agent primary model
4. runtime fallback default

Do not invent backend schema that does not exist.
If the current schema only supports a single `subagents.model` selection and shared concurrency limits, surface that clearly in the UI.

## UI pattern

Add **Subagents** as an Agents-page panel beside:
- Overview
- Files
- Tools
- Skills
- Channels
- Cron

Recommended panel layout:
- **Agent overrides**
  - subagent model
  - subagent fallback models
  - subagent thinking level
- **Shared subagent defaults**
  - default subagent model
  - default fallback models
  - default thinking level
  - `maxConcurrent`
  - `maxSpawnDepth`
  - `maxChildrenPerAgent`
- include a short precedence note explaining which value wins

## Config wiring rules

Prefer the existing config editing path. Do not create a disconnected store.

Edit through the same config-form/save flow already used by the Agents UI:
- `agents.list[i].subagents.model`
- `agents.list[i].subagents.thinking`
- `agents.defaults.subagents.model`
- `agents.defaults.subagents.thinking`
- `agents.defaults.subagents.maxConcurrent`
- `agents.defaults.subagents.maxSpawnDepth`
- `agents.defaults.subagents.maxChildrenPerAgent`

If fallback models are represented as part of the existing model object shape, reuse that shape instead of inventing a new field.

## Implementation checklist

1. Add/update `ui/src/ui/views/agents-panel-subagents.ts`
2. Wire `"subagents"` through `ui/src/ui/views/agents.ts`
3. Add required state/type wiring in `ui/src/ui/app.ts` and `ui/src/ui/app-view-state.ts`
4. Wire change handlers in `ui/src/ui/app-render.ts`
5. Add/update focused UI tests
6. Build the UI and run the targeted test file

## Validation

Prefer these checks after changes:

```bash
cd ~/openclaw
pnpm --dir ui exec vitest run --config vitest.config.ts src/ui/views/agents.test.ts
pnpm --dir ui build
```

If repo-wide typecheck is already noisy, do not claim unrelated errors belong to this feature.

## References

Read these before editing:
- `references/file-map.md`
- `references/runtime-precedence.md`

For the concrete implementation that originally shipped this feature, read:
- `references/implementation-notes.txt`
- `references/agents-panel-subagents.ts.txt`
- `references/agents.ts.txt`
- `references/app.ts.txt`
- `references/app-view-state.ts.txt`
- `references/app-render.subagents.txt`
- `references/agents.test.ts.txt`

Use those files as the exact reference implementation when recreating or porting the feature to another OpenClaw tree.
