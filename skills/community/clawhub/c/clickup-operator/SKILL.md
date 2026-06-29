---
name: clickup-operator
description: Route ClickUp ideas, to-dos, and project work with operator-style defaults. Use when the user wants tasks or ideas created, moved, assigned, due-dated, promoted into project lists, or read back from ClickUp without unnecessary confirmation.
---

# ClickUp Operator

Operate inside ClickUp with a fast, low-friction routing model.

## Entry Order

`SKILL.md` is the entrypoint and traffic controller for this skill.

Use this execution order:

1. Determine whether the user needs first-run onboarding, safe validation, or normal operation.
2. If ClickUp is not connected or the user's defaults are not known, read the onboarding/setup references first.
3. Once setup is complete, read the routing and operating references before acting on live ClickUp requests.
4. If the setup is new or uncertain, run validation before treating the skill as production-ready.

## Phase Routing

### Phase 1. First-run onboarding

Use this phase when:

- the user just installed the skill
- ClickUp MCP is not confirmed working yet
- the user's routing defaults are not known yet
- the user asks to set up ClickUp Operator

Read in this order:

1. [references/guided-onboarding.md](references/guided-onboarding.md)
2. [references/internal-install.md](references/internal-install.md)
3. [references/structure-discovery.md](references/structure-discovery.md)
4. [templates/guided-onboarding-checklist.md](templates/guided-onboarding-checklist.md)
5. [templates/structure-discovery-worksheet.md](templates/structure-discovery-worksheet.md)
6. [references/configuration.md](references/configuration.md)
7. [templates/config.template.yaml](templates/config.template.yaml)

Then:

- confirm the discovered defaults back to the user
- save config only after confirmation
- run a smoke test before declaring setup complete

### Phase 2. Safe validation against an already-live setup

Use this phase when:

- ClickUp is already working
- the user does not want the current setup disturbed
- the goal is to confirm the packaged skill matches the live behavior

Read in this order:

1. [references/safe-live-validation.md](references/safe-live-validation.md)
2. [examples/safe-live-smoke-test.md](examples/safe-live-smoke-test.md)
3. [references/configuration.md](references/configuration.md)

### Phase 3. Normal operation

Use this phase when:

- ClickUp MCP is already working
- routing defaults are already known
- the user wants normal ClickUp task/idea/read behavior

Read in this order:

1. [references/routing-rules.md](references/routing-rules.md)
2. [references/configuration.md](references/configuration.md)

Use validation references only if behavior seems uncertain or newly configured.

## Use this skill when

- the user wants a ClickUp task, reminder, or idea created
- the user wants an item moved to a different list or project
- the user wants an assignee or due date changed
- the user wants to know what is due, active, or on today's list
- the user wants ClickUp handled directly instead of discussing how it should be handled

## Core behavior

1. Execute obvious ClickUp actions immediately.
2. Separate reusable logic from account-specific config.
3. Ask a follow-up only when the missing detail would materially change the correct outcome.
4. Keep responses short and outcome-focused after the ClickUp action is complete.

## Routing rules

- General idea, not tied to a project: send to the configured ideas list.
- General to-do, reminder, or action item: send to the configured general to-do list.
- Item explicitly tied to a project: send to that project list.
- Item that has grown into a real multi-step initiative: promote it into its own dedicated project list.

Read [references/routing-rules.md](references/routing-rules.md) for the detailed decision rules and response standards during normal operation.

## Configuration

This skill is intentionally not hardcoded to one account. Load the user's config before acting.

Required config categories:

- workspace and space defaults
- general list IDs
- member IDs or assignee resolution defaults
- active status filters for read queries
- due-date policy defaults

Use [references/configuration.md](references/configuration.md) and [templates/config.template.yaml](templates/config.template.yaml) as the setup contract.

For internal installation and live account setup, use [references/internal-install.md](references/internal-install.md).
For safe testing against an already-live workspace, use [references/safe-live-validation.md](references/safe-live-validation.md).
For onboarding an already-organized ClickUp workspace, use [references/structure-discovery.md](references/structure-discovery.md).
For the full end-to-end user onboarding flow, use [references/guided-onboarding.md](references/guided-onboarding.md).

## Read behavior

- Ignore completed items by default.
- For action-oriented reads, only surface active statuses from config unless the user explicitly asks otherwise.
- For "what's on my list today" style requests, default to:
  - tasks assigned to the configured default assignee
  - tasks due today only
  - no tomorrow-or-later spillover unless the user asks

## Validation

Before calling the package solid, run the example prompts in [examples/test-cases.md](examples/test-cases.md) against the configured account and verify the outputs match the expected routing and default behavior.

Use [examples/internal-smoke-test.md](examples/internal-smoke-test.md) for the full internal validation pass.
Use [examples/safe-live-smoke-test.md](examples/safe-live-smoke-test.md) for the lowest-risk live validation flow.

Known current nuance:

- exact same-day `due_date_from` + `due_date_to` filtering in the current ClickUp MCP surface may be unreliable for "today" reads
- if the exact same-day filter behaves strangely, use a safer read strategy instead of assuming the routing logic is wrong

## Product framing

If the package is being prepared for external sharing, use [references/public-packaging.md](references/public-packaging.md) to keep the public story, boundaries, and setup expectations clear.
