# debate-research

> Multi-perspective structured debate for complex topics. Spawn parallel subagents with opposing stances, cross-inject arguments for rebuttal, then synthesize via a neutral judge into a consensus report.

## What it does

When you face a decision that has genuine trade-offs — comparing tools, evaluating architectures, choosing strategies — most research approaches give you one perspective at a time. This skill forces adversarial quality: two (or more) agents argue opposing sides, then rebut each other's arguments, and a neutral judge synthesizes a verdict with a concrete recommendation and scenario matrix.

**Example triggers:**
- `Claude Code vs OpenCode`
- `PostgreSQL vs MongoDB for this use case`
- `Buy vs build the auth layer`
- `Claude Code vs OpenCode (gpt-5.4, claude-4.6-sonnet)` ← per-role model override

## How it compares to other approaches

| Approach | Method | Predictability | Output |
|----------|--------|---------------|--------|
| **debate-research (this skill)** | Fixed 3-stage: stance → rebuttal → judgment | ✅ High — fixed rounds, known cost | Formal consensus report |
| **Multi-Agent Debate (MAD)** (Liang et al. 2023) | Agents iterate until convergence | ⚠️ Low — unbounded rounds | Emergent consensus |
| **Constitutional AI Debate** (Anthropic/CMAG) | Agents debate around alignment principles | ✅ Principled | Alignment-focused verdict |
| **Devil's Advocate** (AutoGen/CrewAI) | Dedicated Critic role red-teams the main agent | ⚠️ One-sided | Critique only, no synthesis |
| **Socratic Reasoning** | Continuous questioning to expose premise flaws | ⚠️ Open-ended | Philosophy/ethics oriented |
| **Single-agent pros/cons** | One LLM lists trade-offs | ✅ Fast | Shallow — no adversarial pressure |

**Where debate-research wins:**
- **Reproducible cost** — fixed rounds mean you know the token budget upfront; MAD can spiral
- **Formal output** — structured Markdown report with a scenario matrix, suitable for sharing with a team
- **Evidence discipline** — confidence scores + source tags per argument; neutral judge weights by evidence quality, not rhetoric
- **Socratic pressure in Phase 2** — agents don't just counter, they identify the opponent's *weakest premise* and attack it, producing sharper rebuttals than surface-level point-by-point responses
- **Cross-phase information control** — Phase 1 has `web_search` enabled for fact-gathering; Phase 2 disables it to prevent information drift: rebuttals must challenge the opponent's logic on a fixed evidence base, not patch weak arguments with freshly searched sources

## Pipeline

```
Phase 0  — Pre-flight: model reachability check + plan confirmation
Phase 1  — Stance Investigation (parallel, web_search ON)
Phase 2  — Cross Rebuttal (parallel, web_search OFF)
Phase 2.5— Evidence Audit (optional, auto-triggered for fact-dense topics)
Phase 3  — Neutral Judgment → recommendation + scenario matrix
Phase 4  — Report Assembly → Markdown document
```

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `topic` | required | Debate subject |
| `roles` | Proponent + Opponent | 2-4 roles with name, stance, optional model |
| `goal` | inferred | What question to answer |
| `audience` | "self" | self / team / public |
| `decision_type` | "personal-choice" | personal-choice / team-standardization / market-analysis |
| `evidence_round` | "auto" | false / true / auto |
| `confirm_plan` | true | Show plan and wait before executing |
| `model` | inherit | Global subagent model |
| `output_path` | null | Write report to file; null = return in conversation |

## Install

```bash
npx clawhub@latest install debate-research
```

## Requirements

- OpenClaw with `sessions_spawn` + `sessions_yield` support
- At least one configured LLM provider
- `web_search` tool available (used in Phase 1)
