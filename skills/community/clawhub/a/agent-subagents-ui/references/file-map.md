# File map

## Primary UI files

- `ui/src/ui/views/agents-panel-subagents.ts`
  - renderer for the Subagents panel
  - owns controls for model, fallbacks, thinking, and shared limits
- `ui/src/ui/views/agents.ts`
  - adds the `subagents` panel type
  - renders the new tab/panel and threads handlers through props
- `ui/src/ui/app.ts`
  - holds any added app state needed by the panel wiring
- `ui/src/ui/app-view-state.ts`
  - mirrors app state/types used by render helpers
- `ui/src/ui/app-render.ts`
  - wires the panel into the config form update/save flow
  - applies mutations to per-agent subagent config and shared defaults
- `ui/src/ui/views/agents.test.ts`
  - focused UI test coverage for the Agents page and Subagents tab

## Runtime source of truth

- `src/agents/model-selection.ts`
  - `resolveSubagentConfiguredModelSelection(...)`
  - `resolveSubagentSpawnModelSelection(...)`

These functions define the precedence the UI must reflect.

## Practical editing notes

- Reuse existing helpers from `agents-utils.ts` when working with model primary/fallback parsing.
- Keep the panel inside the existing Agents page instead of adding a separate top-level nav tab.
- Reuse existing card, field, chip, and select UI patterns already present in the Agents UI.
- If the selected agent has no override, show inherited/default state clearly in the control labels.
