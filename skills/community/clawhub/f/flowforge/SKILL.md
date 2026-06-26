---
name: flowforge
description: Autonomous AI coding pipeline that breaks any task into a structured Spec → Plan → Code → QA loop and executes it via Claude Code. Use when: (1) starting any new feature, refactor, or bug fix, (2) given a GitHub issue to implement, (3) asked to "run FlowForge", "forge this", "plan and build", or "auto-implement". Routes ALL heavy work through Claude Code. Supports multi-account rotation to handle rate limits automatically.
---

# FlowForge

Autonomous spec → plan → code → QA pipeline powered by Claude Code.
All heavy computation runs through Claude Code (Max subscription). OpenClaw only orchestrates.

## Architecture

```
Flo (minimal tokens) → shell pipeline → Claude Code (all heavy work)
                                              ↓
                                   Account rotation on rate limit
```

## Workflow Types

Classify the task before planning — each type has a different phase structure:

| Type | When | Phase Order |
|------|------|-------------|
| `feature` | New capability | Backend → Worker → Frontend → Integration |
| `refactor` | Restructure existing code | Add New → Migrate → Remove Old → Cleanup |
| `investigation` | Bug hunt | Reproduce → Investigate → Fix → Harden |
| `migration` | Move data/infra | Prepare → Test → Execute → Cleanup |
| `simple` | Single-file change | Just subtasks, no phases |

## Steps

### 1. Setup workspace

```bash
bash ~/clawd/skills/flowforge/scripts/init_forge.sh "<task_description>" "<repo_path>"
```

Creates `~/.forge/<timestamp>/` with `task.md`.

### 2. Clarification checkpoint (required before spec)

Before running the pipeline, ask 2–4 targeted questions to resolve ambiguity. Do not ask for information already in `task.md`. Focus on:

- **Scope edge cases** — "Does this include X, or is that a separate shape?"
- **Constraints** — "Any files that are frozen / must not be touched?"
- **Integration points** — "Which existing module owns this responsibility?"
- **Success definition** — "What does passing look like — a test, a manual check, a metric?"

Present questions in a numbered list. Wait for answers before proceeding. If the task is unambiguous (e.g., a single-file fix from a clear issue), skip this step and note "No clarification needed."

Save answers to `~/.forge/<timestamp>/clarifications.md` for reference during spec + plan phases.

### 3. Run the pipeline

```bash
bash ~/clawd/skills/flowforge/scripts/run_forge.sh ~/.forge/<timestamp>/
```

This chains 4 Claude Code calls:
1. **Spec** — generates `spec.md` incorporating clarifications (high thinking)
2. **Plan** — generates `implementation_plan.json` (high thinking)
3. **Code** — executes each subtask with verification (medium thinking)
4. **QA** — reviews output, scores against spec (high thinking)

Each step saves output to the workspace directory. Claude Code does ALL the work.

### 4. Monitor

Poll workspace for completion:
```bash
tail -f ~/.forge/<timestamp>/progress.log
cat ~/.forge/<timestamp>/qa_report.md
```

## Account Rotation

Three Claude Max accounts rotate automatically on rate limit:

```
account-1@gmail.com  →  account-2@gmail.com  →  account-3@gmail.com  →  retry
```

Configure your accounts in `~/.flowforge/accounts.txt` (one email per line).
Save credentials per account in `~/.claude/accounts/<email>.json`.
Switch accounts with: `bash <skill-dir>/scripts/rotate_account.sh`

## GitHub Issues

To pull a task from a GitHub issue:

```bash
gh issue view <number> --repo <owner>/<repo> --json title,body | \
  jq -r '"# " + .title + "\n\n" + .body' > ~/.forge/<timestamp>/task.md
```

Then run the pipeline normally.

## Output

On completion, workspace contains:
- `clarifications.md` — pre-spec Q&A (scope, constraints, integration points)
- `spec.md` — full specification (incorporates clarifications)
- `implementation_plan.json` — phases + subtasks with status
- `qa_report.md` — QA review and score
- `project-context.md` — session handoff note (decisions made, patterns established, what next session needs to know)
- `progress.log` — timestamped execution log

## Optional: Rubric Scoring (200 criteria)

Add `--rubric` flag for high-stakes runs. Scores against a universal 200-criterion quality rubric after the spec-based QA pass:

```bash
bash ~/clawd/skills/flowforge/scripts/run_forge.sh ~/.forge/<timestamp>/ --rubric
```

Rubric covers: Architecture (40), Code Quality (40), Testing (40), Error Handling (30), Security (20), Documentation (15), Observability (15).

Verdict thresholds: **≥180 = Ship it** | **150–179 = Needs work** | **<150 = Major rework**

Skip `--rubric` for quick tasks. Use it before shipping to production.

## Prompts

See `references/spec-prompt.md`, `references/planner-prompt.md`, `references/qa-prompt.md`, `references/rubric-prompt.md` for the full Claude Code prompts used at each stage.
