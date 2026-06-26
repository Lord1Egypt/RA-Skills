---
name: debate-research
description: "Multi-perspective structured debate for complex topics. Spawn parallel subagents with opposing stances, cross-inject arguments for rebuttal, then synthesize via neutral judge into a consensus report with recommendations and scenario matrix. Use when: (1) user asks for deep comparison, pros/cons, or X vs Y analysis, (2) user asks for multi-angle research on a controversial or complex topic, (3) user explicitly requests debate, dialectical analysis, or adversarial research. NOT for: simple factual lookups, single-perspective deep research (use academic-deep-research), or quick opinion questions."
---

# Debate Research

## Input Parameters

Collect from user before starting. Only `topic` is required; all others have defaults.

| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `topic` | yes | — | Debate subject |
| `roles` | no | Proponent + Opponent | 2-4 role objects: `{name, stance, model?}`. Default: Proponent (argue for) and Opponent (argue against). Model inherits from global. |
| `goal` | no | inferred | What question to answer |
| `audience` | no | "self" | Who reads the report: self / team / public |
| `decision_type` | no | "personal-choice" | personal-choice / team-standardization / market-analysis |
| `evidence_round` | no | "auto" | false / true / auto (enable when topic is fact-dense) |
| `confirm_plan` | no | true | Show plan and wait for user OK before execution |
| `model` | no | inherit | Global subagent model; role-level override takes priority |
| `output_path` | no | null | File path for report; null = return in conversation |

**Implicit parameter:** `language` — inferred from the user's topic/conversation language. All subagent prompts output in this language.

## Example User Prompt

- `Claude Code vs OpenCode (gpt-5.4, claude-4.6-sonnet)`

## Execution Pipeline

### Phase 0 — Pre-flight

**Step 0a: Model reachability check**

Collect all unique models (global + per-role + judge). For each unique model,
probe via `sessions_spawn` with a minimal one-sentence task (e.g. "Reply OK")
and `model: <target>`. Do NOT use curl or external HTTP — all models route
through OpenClaw's provider config.

If any probe fails:
- If user explicitly specified the failed model → **abort**, report failure, suggest alternatives
- If model was default-assigned → warn user, fall back to session default model, continue

**Step 0b: Plan presentation** (if `confirm_plan: true`)

Present to user:
- Topic
- Role × model assignment table
- Evidence round: on/off/auto (with rationale if auto)
- Estimated subagent call count
- Goal / audience / decision_type interpretation

**[STOP — wait for user confirmation]**

If `confirm_plan: false`, skip directly to Phase 1.

### Phase 1 — Stance Investigation (parallel)

Spawn one subagent per role, **all in parallel**.

Each agent receives a prompt built from:
- Role name + stance
- Topic
- **web_search: enabled**

**Required output format per agent:**
```
Core arguments (3-5):
  - [argument] | confidence: 0.0-1.0 | source: [official-docs/community-feedback/personal-blog/academic-paper]
Opponent weaknesses (2-3)
Predicted counter-attacks (1-2)
```

Use `sessions_spawn` + `sessions_yield` to wait for all completions.

**Error handling:**
- Agent timeout → mark output `[INCOMPLETE]`, continue pipeline

### Phase 2 — Cross Rebuttal (parallel)

Spawn one subagent per role, **all in parallel**.

Each agent receives:
- Its original stance
- **All other roles' Phase 1 output** (cross-injected)
- **web_search: disabled**

**Required output format per agent:**
```
Rebuttals (one per opponent argument):
  - [rebuttal] | confidence: 0.0-1.0
Weakest premise attack:
  - Identify opponent's single weakest assumption and challenge it  ← Socratic element
New attacks (2):
  - [attack]
```

**Word limit:** `300 × number_of_opponents` words per agent.

**Error handling:**
- Agent timeout → mark `[INCOMPLETE]`, continue

### Phase 2.5 — Evidence Audit (optional)

Triggered when `evidence_round: true`, or when `auto` and topic involves
measurable claims. Auto-enable heuristic: topic contains performance benchmarks,
cost comparisons, security assessments, market data, or quantitative metrics.
When in doubt with `auto`, skip (false positive costs more than false negative).

Spawn 1 subagent as "evidence auditor":
- Input: all Phase 1 + Phase 2 output
- **web_search: disabled**
- Task: extract every factual claim, tag each as:
  `[official-docs] [community-feedback] [personal-blog] [no-source] [exaggerated]`
- Output: concise fact checklist

### Phase 3 — Neutral Judgment

Spawn 1 subagent as neutral judge:
- Input: Phase 1 + Phase 2 + Phase 2.5 (if available)
- **web_search: disabled**
- Weigh arguments by confidence scores AND source quality tags

**Required output structure:**
1. Strong arguments per side
2. Exaggerated claims per side
3. Shared limitations (problems neither option solves)
4. Core disagreements (value-level, not just factual)
5. Consensus points
6. **Recommendation** — explicit directional advice, adapted to `decision_type`
7. **Open Questions** — unresolved unknowns that could change the conclusion
8. Scenario selection matrix (table: scenario × recommendation × rationale)
9. One-sentence summary

### Phase 4 — Report Assembly

Orchestrator (main conversation) assembles all outputs into Markdown:

```markdown
# [topic]: Debate Research Report

> **Date**: YYYY-MM-DD
> **Method**: Multi-agent structured debate (debate-research skill)
> **Roles**: [role1 (model)] | [role2 (model)] | ...
> **Audience**: [audience] | **Decision type**: [decision_type]
> **Completion**: [success | degraded-success | aborted]

## Core Arguments by Side
[Phase 1 output, organized by role]

## Cross Rebuttals
[Phase 2 output, organized by role]

## Evidence Audit
[Phase 2.5 output, or "Not requested"]

## Neutral Judgment
[Phase 3 sections 1-5]

## Recommendation
[Phase 3 section 6]

## Open Questions
[Phase 3 section 7]

## Scenario Matrix
[Phase 3 section 8]

> **One-line summary**: [Phase 3 section 9]
```

If `output_path` specified → write file.
Otherwise → return in conversation.

## Completion States

| State | Condition | Behavior |
|-------|-----------|----------|
| `success` | All phases completed normally | Full report |
| `degraded-success` | 1+ agents timed out or returned `[INCOMPLETE]` | Report with degradation note |
| `aborted` | Model pre-check failed / user cancelled plan | No report; return error summary |

## Prompt Templates

See `references/prompts.md` for the exact prompt templates used in each phase.
Orchestrator builds prompts dynamically from parameters + these templates.
