---
name: autooptimise
description: "Autonomously optimise any OpenClaw skill using a benchmark-driven experiment loop. Scores skill outputs 0-10 across 4 dimensions, identifies the lowest-scoring pattern, proposes a targeted SKILL.md change, re-tests, and keeps or discards based on measured improvement. Use when asked to: optimise my [skill] skill, run autooptimise on [skill], benchmark my [skill] skill, improve my skill overnight."
homepage: https://github.com/WealthVisionAI-Source/autooptimise
metadata: { "openclaw": { "emoji": "🔬" } }
---

# autooptimise

Autonomous benchmark-driven skill optimisation for OpenClaw. Inspired by Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) — the same modify → test → score → keep/discard loop, applied to agent skill quality instead of GPU training.

## Trigger Phrases

- `"optimise my weather skill"`
- `"run autooptimise on [skill-name]"`
- `"benchmark my [skill-name] skill"`
- `"improve my skill overnight"`

## Key Files

| File | Purpose |
|------|---------|
| `benchmark/tasks.json` | Test task suite (prompts + expected qualities) |
| `benchmark/scorer.md` | LLM judge scoring rubric |
| `runner/run_experiment.md` | Autonomous loop instructions (load this next) |
| `runner/experiment_log.md` | Auto-created run log (gitignored) |

## How to Run

1. Read `runner/run_experiment.md` — it contains the full loop instructions
2. Confirm the target skill with the user if not specified
3. Execute the loop (max 3 iterations)
4. Present proposed changes for human approval — **never auto-apply**

## Scoring

Use the best available LLM judge model (prefer a strong reasoning model). Score each task 0–10 on:
- **Accuracy** — correct answer / correct tool called
- **Conciseness** — no padding, no unnecessary text
- **Tool usage** — right tool, right parameters
- **Formatting** — output matches expected format

Full rubric: `benchmark/scorer.md`

## Safety Rules

- **Never auto-apply changes.** Always present a diff and wait for explicit human approval.
- **Never modify** `benchmark/tasks.json` or `benchmark/scorer.md` during a run.
- **Never exceed 3 iterations** per run in v0.1.
- Log every action to `runner/experiment_log.md`.
