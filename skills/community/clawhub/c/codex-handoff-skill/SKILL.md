---
name: Codex Handoff
version: 1.1.1
description: |
  Offload finalized coding plans to Codex CLI for automated execution.
  Use when: user says "hand off to codex", "let codex do it", "offload to codex",
  runs /codex-handoff, or has a plan ready for Codex CLI execution.
  Claude Code acts as supervisor/judge in a loop — Codex CLI does the coding.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Codex Handoff — Supervisor Loop

Claude Code is the **supervisor/judge**. Codex CLI is the **executor**. You orchestrate a loop: send plan to Codex, review results, re-run if incomplete, until the task is comprehensively done.

**Announce at start:** "Using codex-handoff to orchestrate Codex CLI execution of the plan."

## Prerequisites

- Codex CLI must be installed (`codex --version`)
- A plan must exist (in `docs/plans/`, `.claude/plans/`, or provided inline)
- The working directory should be a git repo (for diff-based review)

## Quick Start

1. **Locate** the plan (from `docs/plans/`, `.claude/plans/`, or user arguments)
2. **Detect phases** — scan for phase headings; if found, execute phase-by-phase
3. **Build** a structured Codex prompt with plan (or phase) + project context + coding standards
4. **Execute** Codex CLI in `--full-auto` mode
5. **Review** git diff, run tests, audit completion with a scorecard
6. **Decide** — loop with correction prompt if items remain, or advance to next phase / finalize
7. **Report** final status with completed/remaining items and test results

## Reference

| Task | Details |
|------|---------|
| Build Codex prompt | [prompt-templates.md](references/prompt-templates.md) |
| Review & audit results | [review-process.md](references/review-process.md) |
| Handle errors | [error-handling.md](references/error-handling.md) |

## Process

### Step 1: LOCATE THE PLAN

Find the plan to execute. Search in order:

1. If user provided a task description with the command, use that as context to find the relevant plan
2. Check `docs/plans/` for the most recent `.md` file (sorted by date prefix)
3. Check `.claude/plans/` for any recent plan files
4. If no plan found, tell the user: "No plan found. Please create one first using /brainstorming or /writing-plans."

Once found:
- Read the plan file completely
- Present a brief summary to the user
- Ask: "Ready to hand off to Codex CLI?"
- Wait for confirmation before proceeding

### Step 1b: DETECT PHASES

After reading the plan, scan for H2 headings matching: `## Phase N:`, `## Stage N:`, `## Part N:`, or numbered sections like `## 1. Backend`.

- **Phases found** — Report: "Detected {N} phases. Will execute sequentially." Use phased flow.
- **No phases** — Single-pass execution (Steps 2-6 as normal). No changes for simple plans.
- **`--phase N`** — Optional. Re-run only phase N.

### Step 2: BUILD THE CODEX PROMPT

See [prompt-templates.md](references/prompt-templates.md). Use the "Initial Execution Prompt" for single-pass, or "Phase-Scoped Execution Prompt" for phased mode (current phase only + completed phase summaries).

### Step 3: EXECUTE CODEX

Parse optional arguments:
- `--max-iterations N` — max loop iterations (default: 5, per-phase in phased mode)
- `--model MODEL` — pass to codex as `-m MODEL`
- `--phase N` — execute only this phase (phased mode only)

```bash
codex exec --full-auto -s workspace-write [-m MODEL] < /tmp/codex-handoff-{timestamp}.md
```

Let the command run to completion. Capture stdout and exit code. Report: "Codex iteration {N} complete. Reviewing changes..."

**Phased execution flow:** For each phase (or single phase if `--phase N`): build phase-scoped prompt → run Codex → review → correction loop (up to max-iterations) → phase passes: record summary, advance → phase fails at max: ask user to continue or stop.

### Step 4: REVIEW THE RESULTS

See [review-process.md](references/review-process.md) for the review checklist, scorecard, and decision matrix. In phased mode, the scorecard is scoped to current phase items only.

### Step 5: DECIDE — LOOP OR COMPLETE

- **All items DONE + tests pass:** Move to Step 6 (or next phase).
- **Items remain AND iterations < max:** Build correction prompt and re-run Codex.
- **Max iterations reached:** Move to Step 6. In phased mode, ask user to continue or stop.

### Step 6: FINAL REPORT

See report format in [review-process.md](references/review-process.md). In phased mode, report per-phase results then aggregate. If items remain, suggest `--phase N` to retry.

## Key Principles

1. **Never modify code yourself** — Your job is to supervise, not code. Codex does the coding.
2. **Be a strict judge** — Don't pass items as "done" unless they genuinely are.
3. **Correction prompts are specific** — Tell Codex exactly what's wrong and what to fix.
4. **Respect the plan** — Don't add or remove plan items. Execute what was planned.
5. **Keep the user informed** — Report status after each iteration and phase transition.
