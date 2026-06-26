---
name: agent-templates-system
description: OpenClaw Agent Templates system reference and workflow guide. Use when creating, editing, reviewing, debugging, or extending the built-in Agent Templates feature; when working with template-backed agent creation; or when packaging/documenting the Agent Templates UI, gateway handlers, SQLite storage, workspace file seeding, identity defaults, or create-from-template flow.
---

# Agent Templates System

Use this skill when working on OpenClaw's built-in **Agent Templates** feature.

## What this system does

The Agent Templates system lets OpenClaw store reusable agent blueprints in SQLite, edit them in the Control UI, and materialize real agents from those blueprints.

A template can define:
- identity defaults
- included skills
- partial agent config
- workspace files
- memory seeds

From the UI, a user can:
- list templates
- create templates
- edit templates
- delete templates
- create a real agent from a selected template

## Core workflow

1. Read `references/implementation.md` first.
2. If UI work is involved, also read `references/ui-design.md`.
3. If you need payload examples, read `references/template-schema.md` and inspect `assets/examples/`.
4. When changing behavior, keep storage, gateway methods, and UI state in sync.
5. When validating a bug or feature, test both:
   - template CRUD
   - agent creation from template

## Source of truth files

Read these files in the OpenClaw repo when making code changes:
- `src/agents/templates.ts`
- `src/gateway/server-methods/agent-templates.ts`
- `ui/src/ui/controllers/templates.ts`
- `ui/src/ui/views/templates.ts`

## Important behaviors

- Templates are stored in SQLite under the OpenClaw state dir.
- Template definitions are normalized before storage/use.
- Creating an agent from a template updates OpenClaw config, creates a workspace, writes identity/workspace files, and seeds memory.
- Included skills are merged with template config and create-time overrides.
- Workspace file paths are constrained to stay inside the target workspace.

## Practical guidance

- Prefer small, composable template definitions.
- Put durable persona/role setup in `workspace.files`.
- Put starter memory in `workspace.memorySeeds`.
- Use `definition.skills` for reusable attached skills.
- Keep UI wording aligned with the underlying JSON schema.
- If the UI allows raw JSON editing, make parser errors user-legible.

## Debugging checklist

- Can `agentTemplates.list` return the template?
- Does `agentTemplates.get` return the expected normalized definition?
- Does the UI render the selected template and preserve edits?
- Does `agents.createFromTemplate` create a non-conflicting agent id?
- Were `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, and any seeded files written as expected?
- Did config get updated with workspace, identity, and merged skills?

## References in this skill

- `references/implementation.md` — architecture and code map
- `references/template-schema.md` — practical schema notes and field behavior
- `references/ui-design.md` — Control UI layout and UX notes
- `assets/examples/agent-template-definition.json` — example template payload
