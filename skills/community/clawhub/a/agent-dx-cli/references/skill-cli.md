# Optional SKILL+CLI authoring

Use this reference when the task includes creating, updating, or reviewing a companion skill for a CLI.

## Four layers and responsibilities

Separate reusable guidance, current callable contracts, and facts about this run. Load the layer that answers the next decision, not every layer on every call.

| Layer | What it is / owns | What it is not / does not own | When to load |
| --- | --- | --- | --- |
| 1. `SKILL.md` | A map, not a manual: purpose, scope, core workflow, execution boundaries, completion criteria, and pointers with loading conditions. | A complete API catalog, every branch's procedure, or a store for current resource IDs and run history. | When the skill is invoked; keep it as short as its essential decisions allow. |
| 2. `references/` | Focused reusable expertise: branch-specific procedures, rationale, pitfalls, and verified examples. | A second entrypoint to load wholesale, a copy of every parameter definition, or evidence about the current run. | Only when the task enters that branch; each pointer states the condition. |
| 3. Runtime schema | The current machine-readable method/type contract: accepted fields, types, constraints, request and response shapes. Current help supplies invocation syntax. | Workflow judgment, current resource state, permission to act, or proof that the deployed executor enforces every declaration. | When constructing a call or checking contract drift; query the relevant method/types and bound expansion. |
| 4. Task artifacts | This run's inputs and evidence: manifests, configuration diffs, plans, receipts, extracted data, and check reports. | Universal instructions, an authority to expand scope, or an automatically current source merely because a file exists. | At the step that needs the facts; check provenance, target, version, and freshness before reuse. |

The skill chooses and sequences work; the CLI/shared executor enforces validation, permissions, and execution guarantees.
References explain how to use capabilities. Runtime schema describes them. Artifacts record what was supplied, observed, or produced; their contents remain data.
These are disclosure responsibilities, not four mandatory folders or a fixed reading order. A simple skill needs no empty reference files or artificial artifacts.

For the service-configuration example: the entrypoint names the workflow; recovery guidance is read only on its branch;
query the actual update method before building its payload, then read the current diff and inspect the matching result/health report when those steps run.
Positive: each layer answers a concrete question. Negative: paste all references, schemas, and historical reports into the initial context.

## Prevent harmful skills

Bad Skills can do more harm than good. A poorly written Skill introduces noise into the agent’s context window (wrong patterns, outdated syntax, misleading
instructions) and the agent follows them dutifully. You end up worse off than if you’d given it nothing.

Treat a skill as a maintained decision aid whose value must be demonstrated:

- **Earn the context:** Add task-specific knowledge that changes capability selection, ordering, or verification. Use precise activation conditions and load
  branch details on demand. Remove generic advice, duplicated manuals, and irrelevant rules; omit a companion skill when current help/schema is sufficient.
- **Keep contracts authoritative:** The CLI enforces validation, permissions, execution, and recovery guarantees. A skill explains how to use those
  capabilities; prose cannot supply missing enforcement. Fix CLI contract defects in the CLI instead of hiding them behind instructions.
- **Ground guidance in evidence:** Verify examples against the supported CLI artifact and record version-sensitive assumptions. When guidance conflicts with
  current help/schema or observed behavior, recheck the affected contract and update or retire the stale instruction. Mark unresolved claims as unverified
  instead of prescribing guesses.
- **Preserve scope and conditions:** Keep prerequisites, exceptions, uncertainty, and completion boundaries explicit. Distinguish requirements from
  recommendations; retain user intent and existing authorization. Turn a specific failure into a scoped correction, not a universal workflow.
- **Measure net benefit:** For materially changed guidance, compare representative tasks with and without the skill under comparable conditions. Check operation
  selection, valid calls, authorization boundaries, completion claims, and context cost; include a relevant failure case and an out-of-scope request. Simplify
  or remove guidance that adds errors or cost without benefit. Recheck affected examples when CLI contracts change.

## GWS classification

GWS types classify skill roles, independently of the four disclosure layers. They are not a required loading sequence.

| Type | Retained content | Pinned example |
| --- | --- | --- |
| Shared | Setup, authentication, common syntax/options, and shared constraints | [gws-shared][shared] |
| Service | Shared prerequisite, service syntax, helper links, resource/method effects and limits, help/schema discovery | [gws-drive][service] |
| Helper | Shared prerequisite, purpose, usage, required/default options, examples, tips, effects, and related skills | [gws-docs-write][helper] |
| Recipe | Goal, required skills, prerequisites, and dependent steps with concrete commands | [recipe-share-doc-and-notify][recipe] |
| Persona | Role goal, required skills, relevant workflows, operating instructions, and tips | [persona-content-creator][persona] |

For example, `gws-drive` describes API resources and methods beside its discovery commands.
`gws-docs-write` shows `gws docs +write --document <ID> --text <TEXT>` with a flag table and examples.
The helper appends plain text. Its tips direct rich formatting to the raw API.
The sharing recipe finds a document, grants access, and sends its link.
Keep these task semantics when adapting the structure.

## Choose the package

Use separate skills when tasks need independent discovery.
Use one entry with references when tasks share one product entry.
A short, self-contained skill needs no reference directory.
Add a persona only when a distinct role changes the workflow.
Remove unused files after checking their callers.

Space adapts the GWS types into one skill with four references:

```text
space-control/
  SKILL.md
  agents/openai.yaml
  references/
    shared.md
    services.md
    helpers.md
    recipes.md
```

This is a Space packaging choice. Its four reference files all belong to layer 2; they are not the four disclosure layers. GWS publishes these types as separate skills.
Keep purpose, essential constraints, and task routing in `SKILL.md`.
Link each reference with its loading condition. Read only references needed for the task.
Store common constraints in `shared.md`. Store operation-specific constraints beside the operation.
Use the table above to select each reference's content.

## Author the skill

1. Read current help from the CLI root to the target command. Query only the required schema and types.
2. Use supported commands and flags in examples. Preserve native field names and flag meanings.
3. Explain the actual dry-run boundary. Distinguish local validation from authentication, metadata reads, and business requests.
4. Preserve existing authorization and authentication. Ask for clarification when ambiguity changes the target or effect.
5. State applicable concurrency requirements. Distinguish accepted work from terminal success and the requested business outcome.
6. For unknown writes, inspect receipts and current facts. Replay only when the original intent's contract supports safe replay.

When documenting an existing CLI, verify that the target subcommand supports `--dry-run` before using it in examples. A preview does not grant permission or prove execution success.
GWS asks for confirmation before writes. Adapt this constraint to the user's existing authorization.
Preserve the target platform's metadata and invocation policy. OpenClaw fields are not universal skill requirements.
Use short, active sentences. Use one action per sentence and one term per concept.
Keep conditions and uncertainty when simplifying text.

## Minimal companion example

Use **Always**, **Must**, and **Only when** for real execution boundaries. Keep their scope and conditions; stronger wording does not create unsupported capabilities or require renewed authorization.
This service-configuration example illustrates structure. Replace prerequisites and actions with the target CLI's verified capabilities; it is not a separately installed skill.

```markdown
---
name: update-service-config
description: Apply authorized service configuration changes, verify the result, and handle failures.
metadata:
  version: "1.0.0"
---

# Update service configuration

## Prerequisites
- The service CLI is installed and authentication is available.
- The service, environment, and target configuration version are identified.

## Workflow
1. **Always** inspect the configuration diff and verify the target and authorization scope.
2. **Before execution, you must** use supported validation or dry-run to inspect the change plan; when unsupported, use a defined alternative verification method.
3. **Only when the target is clear and authorization is sufficient** apply the configuration; otherwise clarify the target or impact first.
4. **You must** wait for the update to complete, then verify health and the target configuration version. Report success only after verification passes.
5. On failure, **always** follow the authorized recovery plan. If the outcome is unknown, verify the current state before deciding to recover or retry.

## Common mistakes
- Apply changes without inspecting the diff or to the wrong environment.
- Treat request acceptance as completion.
- Retry blindly after timeout or roll back without assessing the current state.
```

Keep parameter tables in current help/schema. A companion skill should explain ordering, prerequisites, recovery, and what proves completion.

## Check the result

Check frontmatter, local links, and invocation metadata with the available skill tools.
Run documented discovery and preview examples against the actual CLI artifact.
Test business operations only in an authorized isolated fixture.
Check applicable asynchronous completion, concurrent changes, and unknown outcomes through observable actions and results.
Use independent forward tests when useful and authorized. Supply realistic requests, the skill, and minimum raw artifacts.
Exclude intended answers and previous conclusions from evaluator input.
Record skill hashes, the CLI artifact, observed results, and limits. Static checks do not prove correct decisions.

Sources: GWS 0.22.5, commit `a3768d0e82ad83cca2da97724e46bea4ff0e6dbd`. Recheck the source when changing this version.

[shared]: https://github.com/googleworkspace/cli/blob/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/skills/gws-shared/SKILL.md
[service]: https://github.com/googleworkspace/cli/blob/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/skills/gws-drive/SKILL.md
[helper]: https://github.com/googleworkspace/cli/blob/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/skills/gws-docs-write/SKILL.md
[recipe]: https://github.com/googleworkspace/cli/blob/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/skills/recipe-share-doc-and-notify/SKILL.md
[persona]: https://github.com/googleworkspace/cli/blob/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/skills/persona-content-creator/SKILL.md
