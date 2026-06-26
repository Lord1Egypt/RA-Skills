# Agent Templates Implementation

## Purpose

The Agent Templates system is OpenClaw's built-in mechanism for storing reusable agent blueprints and turning them into real configured agents.

## Main code references

### 1. Template storage and materialization
**Path:** `/home/charl/openclaw/src/agents/templates.ts`

This is the core implementation.

Key responsibilities:
- define template types
- open and initialize the SQLite database
- normalize template input
- list/get/create/update/delete template records
- create a real agent from a template
- write seeded workspace files and memory

Important types:
- `AgentTemplateDefinition`
- `AgentTemplateRecord`
- `AgentTemplateCreateInput`
- `AgentTemplateUpdateInput`
- `AgentTemplateCreateFromTemplateInput`

Important functions:
- `listAgentTemplates()`
- `getAgentTemplate(id)`
- `createAgentTemplate(input)`
- `updateAgentTemplate(input)`
- `deleteAgentTemplate(id)`
- `createAgentFromTemplate(input)`

Important implementation details:
- DB path resolves to `resolveStateDir()/agents/templates.sqlite`
- template tags are normalized and deduplicated
- `definition.skills` supports optional `clawhubUrl`
- `workspace.files` supports modes:
  - `overwrite`
  - `skip-if-exists`
  - `append`
- `workspace.memorySeeds` supports:
  - `overwrite`
  - `append`
- file writes are path-checked to prevent escaping the workspace root
- create-from-template updates config and writes workspace artifacts

### 2. Gateway RPC handlers
**Path:** `/home/charl/openclaw/src/gateway/server-methods/agent-templates.ts`

This file exposes the system to the UI/client layer.

Registered methods:
- `agentTemplates.list`
- `agentTemplates.get`
- `agentTemplates.create`
- `agentTemplates.update`
- `agentTemplates.delete`
- `agents.createFromTemplate`

Implementation notes:
- request parsing is thin
- errors are converted into gateway protocol error shapes
- `agents.createFromTemplate` delegates directly to the core implementation

### 3. UI controller layer
**Path:** `/home/charl/openclaw/ui/src/ui/controllers/templates.ts`

This file manages template-specific UI state transitions.

Key responsibilities:
- fetch template list from gateway
- load a selected template into the editor
- parse and serialize included skills
- parse raw JSON definition text
- save create/update changes
- delete selected template
- create an agent from the selected template

Important behavior:
- `prettyDefinition()` strips `skills` from the JSON editor because skills are edited in a separate multiline field
- included skills use one line per skill, optionally `name | clawhubUrl`
- create-from-template sends optional name/workspace overrides

### 4. UI rendering layer
**Path:** `/home/charl/openclaw/ui/src/ui/views/templates.ts`

This file defines the visible Control UI for the feature.

Main sections:
- left column: template list
- right column: editor form
- bottom section: create-agent-from-template form

## Storage details

### Database path
`~/.openclaw/agents/templates.sqlite`

### Table
`agent_templates`

Columns:
- `id`
- `name`
- `description`
- `category`
- `version`
- `tagsJson`
- `definitionJson`
- `createdAt`
- `updatedAt`

## Create-from-template flow

1. Load template by id
2. Resolve final agent name
3. Normalize agent id
4. Ensure it does not collide with existing agents
5. Resolve workspace path
6. Apply agent config into OpenClaw config
7. Merge skills from:
   - template definition skills
   - template config skills
   - overrides config skills
   - explicit overrides skills
8. Ensure agent workspace exists
9. Write updated config
10. Write optional soul override
11. Write generated `IDENTITY.md`
12. Write `workspace.files`
13. Write `workspace.memorySeeds`
14. Return created agent info

## Design implications

- The system is intentionally template-definition driven.
- Identity is partly stored structurally and partly materialized into workspace files.
- The UI is currently power-user friendly because the main definition editor is raw JSON.
- The gateway layer stays thin; almost all logic lives in `src/agents/templates.ts`.
