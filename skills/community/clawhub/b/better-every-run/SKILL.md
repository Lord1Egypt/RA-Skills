---
name: ber
description: "Better Every Run: turn explicit /ber corrections into preferred future outcomes through a small fix, remember, and report flow."
user-invocable: true
metadata:
  version: "0.5.5"
---
# Better Every Run

Use this skill only when the user explicitly invokes `/ber`, names Better Every Run, or directly asks to persist a lesson for future runs. Do not auto-capture ordinary corrections, casual preferences, or words like "remember", "always", "never", or "next time" unless the user clearly wants durable learning.

The human path is deliberately small:

```text
/ber fix bad outcome -> desired outcome
/ber remember simple rule
/ber report
```

The agent runs the bundled local helper and reports the result in chat. `fix` and `remember` record only to the local `.better-every-run/` evidence store. Durable memory/skill changes require the reviewed `card` + `promote` flow; eval regression cases require `eval-fixture`.

## When To Use

- The user explicitly types `/ber fix ... -> ...`.
- The user explicitly types `/ber remember ...`.
- The user explicitly asks for a Better Every Run report.
- The user asks the agent to record a reusable correction as durable memory.

## Human Commands

```text
/ber fix agent wrote vague status -> agent gives exact command output and next action
/ber remember use the approved development host for active code work
/ber report
```

## Rules

- Report CLI output back in chat; do not build web pages or dashboards.
- Do not silently edit `MEMORY.md`, `AGENTS.md`, `SOUL.md`, or other durable instruction files.
- Do not pass `--target` to `/ber fix` or `/ber remember`; direct durable writes are disabled and must refuse.
- Only promote to durable memory or skill files after an explicit review decision using `card` then `promote`.
- Memory promotions must target an existing `memory/*.md` file.
- Skill promotions must target `SKILL.md` in the current skill project.
- Eval fixtures must use `eval-fixture` and target `.json` or `.jsonl` under `tests/` or `evals/`.
- Scanner hard blocks and warnings both block promotion. Adjust, quarantine, or supersede the lesson instead of forcing it through.
- Keep corrections factual: bad outcome, desired outcome, and scope.
- Use scope metadata when it helps decide whether a lesson belongs only to this run, the project, the workspace, a skill, memory, or an eval.
- Avoid private data unless the user explicitly wants it captured.
- Keep the user-facing flow short, but disclose persistence: local store, durable target file if promoted, and how it was reviewed.
- Design for the shortest path to the user's outcome.
- Never publish `.better-every-run/` state, local lessons, event logs, or private corrections.

## Workflow

For normal chat use, keep the visible flow to one command:

```text
/ber fix bad outcome -> desired outcome
```

For simple one-line preferences:

```text
/ber remember simple rule
```

Use `/ber report` to show what was learned, including open proposals and promotion suggestions.

## Agent Implementation

Keep low-level helper commands out of normal chat unless debugging, but never hide persistence. A normal answer should say whether the lesson was recorded only in `.better-every-run/` or promoted to a named durable file through a lesson card.

Read `references/workflow.md` for the full workflow.
Read `references/report-template.md` for expected chat output shape.

Before publishing or packaging, verify:
- `.better-every-run/` is excluded
- `make test` passes
- direct `fix --target`, `remember --target`, and `apply-memory-patch` attempts refuse without changing target files
- lesson-card, lifecycle, and eval-fixture demos are generic and contain no private workspace paths, chat IDs, tokens, or hostnames
- examples contain no private workspace paths, chat IDs, tokens, or hostnames
- docs say activation is explicit-only and persistence is disclosed
