---
name: emotion-skill
description: Markdown-first guidance for coding agents under pressure. Use when repo debugging, repeated failure recovery, evidence-first review, scoped edits, silent tool or queue delays, user confusion, or post-success closeout need better agent behavior. Route by user-state patterns, load only the relevant references, keep scope explicit, show evidence before risky edits, keep progress visible, and close with regression checks instead of expanding work.
---

# Emotion Skill

Use this skill as an agent-readable playbook, not as a script-driven classifier.

The goal is to translate user-state signals into better coding-agent behavior:
show evidence sooner, keep scope tighter, recover from repeated failures, keep
progress visible during stalls, and stop expanding once the work is good.

## Core Rule

Read the user's state as a work-situation signal, then choose a behavior pattern.
Do not expose raw emotion labels to the user. Do not make a routing decision from
one keyword when the surrounding task state points elsewhere.

## Quick Workflow

1. Identify the active state pattern from the latest user turn and recent task context.
2. Load only the reference that matches the active pattern.
3. Apply the behavior rules before answering, editing, delegating, or closing out.
4. Name the evidence, scope boundary, verification step, and progress cadence when they matter.
5. If multiple patterns apply, prefer evidence and scope safety over speed.

## Routing Index

Use [references/routing-playbook.md](references/routing-playbook.md) when deciding the user's current work-state and which behavior pattern to apply.

Use [references/response-constraints.md](references/response-constraints.md) when shaping the next reply, edit boundary, progress update, or closeout.

Use [references/real-scenarios.md](references/real-scenarios.md) when validating that a change generalizes across real coding-agent failure patterns instead of fixing one example.

Use [references/subagent-forward-tests.md](references/subagent-forward-tests.md) when validating actual agent behavior with fresh subagents, especially soft constraints versus hard guardrails.

Use [references/model-prompts.md](references/model-prompts.md) when a host or agent framework needs compact prompt snippets.

Use [references/integration-openclaw-hermes.md](references/integration-openclaw-hermes.md) only when integrating this playbook into an OpenClaw/Hermes host.

Use [references/examples.md](references/examples.md) for quick before/after behavior examples.

Use [references/emotion-value-model.md](references/emotion-value-model.md) for the rationale behind this skill's behavior changes.

## Default Behavior Map

| State pattern | Prefer | Avoid |
|---|---|---|
| Repeated failure or user says it is still broken | repair first, smallest failing path, visible progress | more explanation before checking |
| Evidence request or root-cause challenge | basis first, exact command/log/file/check, then conclusion | guessing or broad claims |
| Scope protection or caution | verify boundary, state allowed files, name rollback path | adjacent refactors |
| Confusion or path ambiguity | restate target, give one correctable default path | multiple unranked options |
| Silent delay or stuck tool/queue | status update, current blocker, next observable checkpoint | quiet background work |
| Post-success closeout | summarize change, run regression/smoke, stop expansion | new features or cleanup |

## Reply Contract

When this skill is active, the next visible reply should include the useful subset of:

- what state pattern is driving the behavior
- what evidence or verification point comes first
- what files, scope, or boundaries are protected
- what will be checked before declaring success
- when the user will next see progress on long-running work

Keep the language natural. Do not say the user is "frustrated" unless they used that wording or asked for classification.

## Scripts Boundary

The skill behavior lives in Markdown. Scripts in the GitHub repository are maintainer
validation tools only. Do not require a ClawHub user or an agent to execute Python
before applying this skill.

Run repository scripts only for release checks, regression comparison, or local
maintenance of this skill package.

## Published Bundle

ClawHub publish now ships the Markdown-first skill bundle:

- `SKILL.md`
- `agents/openai.yaml`
- `references/routing-playbook.md`
- `references/response-constraints.md`
- `references/real-scenarios.md`
- `references/subagent-forward-tests.md`
- `references/model-prompts.md`
- `references/integration-openclaw-hermes.md`
- `references/examples.md`
- `references/emotion-value-model.md`

The GitHub repository keeps dev-only scripts, historical runtime experiments, audits,
and calibration files outside the installed skill bundle.
