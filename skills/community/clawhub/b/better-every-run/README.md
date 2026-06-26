# Better Every Run

Lightweight run learning for OpenClaw agents.

Better Every Run turns explicit `/ber` corrections into future behavior. It does not auto-capture casual chat. The user gives a short command, and the agent reports what was recorded and where it was stored. Accepted lessons carry scope, expiry, status, promotion hints, lesson cards, scanner verdicts, target hashes, lifecycle metadata, and eval-fixture output so an agent can decide whether a correction should stay local or become memory, a skill rule, or a regression case.

## Install

### OpenClaw / ClawHub

```bash
openclaw skills install better-every-run
```

### Manual

```bash
git clone https://github.com/LeoStehlik/better-every-run.git ~/.openclaw/workspace/skills/better-every-run
```

For Claude Code, Codex, or other agent harnesses, copy this folder into the harness skill directory and load `SKILL.md`.

## Human Surface

In OpenClaw chat:

```text
/ber fix vague status update -> exact command output and next action
/ber remember design software for humans from the shortest path to outcome
/ber report
```

The agent handles the local helper, then tells the human whether the lesson stayed in the project-local `.better-every-run/` store or was promoted through a reviewed durable flow.

## Product Rule

- The skill runs only from explicit `/ber` use or a direct request to persist a lesson.
- Humans should not manage helper internals during normal use.
- `/ber fix` and `/ber remember` never append directly to durable files, even when `--target` is supplied.
- The agent should summarize the outcome in chat, including the local store and any reviewed durable promotion.
- Lesson metadata should explain the intended scope: `run`, `project`, `workspace`, `skill`, `memory`, or `eval`.
- Durable memory and skill writes require a fresh lesson card, a stable target hash, and a clean BER scanner verdict.
- Eval durability goes through `eval-fixture`, which writes JSON/JSONL only under `tests/` or `evals/`.
- No plugin, server, web UI, database, or external service is required.

## Storage

The helper writes a project-local evidence trail under `.better-every-run/`. That folder should stay private, be excluded from publishing, and can be reviewed or deleted by the workspace owner.

## Internal Helper

The bundled helper is for agents, tests, and audits. Keep normal chat short, but disclose persistence clearly. Promotion commands are agent-facing: `card --to memory|skill` writes a lesson card with scanner state and target hash; `promote --to memory|skill` appends only when the card is still fresh and the scanner is clean; `eval-fixture` turns a correction into a JSON regression case.

Retired unsafe path: `apply-memory-patch` now refuses. `export-memory-patch` remains available as review output only.

## Upstream Of Skills, Memory, And Evals

BER is deliberately upstream of heavier machinery:

- Use `/ber fix` when the human corrects a bad outcome.
- Use `/ber report` to see accepted lessons, open proposals, expired lessons, lifecycle counts, and promotion suggestions.
- Write a lesson card before durable memory/skill promotion so stale targets and scanner issues are caught before a file is changed.
- Quarantine one-off/bad lessons and supersede stale lessons when a better rule replaces them.
- Promote only the lessons that deserve durability. Memory captures operating preferences, skills capture reusable behavior, and eval fixtures capture regressions that should fail if the agent slips again.

See `examples/upstream-loop.md` for the end-to-end flow.

## Package Contents

This ClawHub package ships the runtime skill, helper, workflow references, examples, and smoke tests. Terminal recording assets are kept GitHub-only.

## Status

Usable public skill bundle, published on ClawHub as `better-every-run@0.5.5`.

## Verify

```bash
make test
```
