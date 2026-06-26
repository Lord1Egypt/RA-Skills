---
name: challenge-loop
version: 1.0.0
license: MIT-0
description: |
  Challenge Loop — adversarial hardening for judgment-containing outputs.
  Two modes: inline self-refutation (zero latency) and independent challenger subagent.
  Always manually triggered.
trigger: |
  Manual trigger — more natural phrasing supported:
  - Inline: "challenge inline" / "挑战一下" / "批一下" / "帮我看看有没有问题" / "靠谱吗" / "有没有漏洞" / "再想想"
  - Subagent Light: "challenge this" / "挑战" / "审一下" / "帮我审查一下"
  - Subagent Standard: "deep challenge" / "深度挑战" / "认真审一下" / "严格审查"
  - Subagent Brutal: "brutal challenge" / "毁灭级挑战" / "往死里挑" / "不留情面地审"
  - Agent discretion: if output is high-risk, agent may self-initiate inline challenge

  **Force skip:**
  - User says "skip challenge" / "跳过" / "不用审" / "直接给"
---

# Challenge Loop

## Overview

| Mode | What happens | Trigger | Cost |
|---|---|---|---|
| **Inline** | Self-refute in same response | "challenge inline" or agent's discretion | Zero |
| **Subagent** | Spawn independent challenger | "challenge this" / "deep challenge" / "brutal challenge" | Higher |

---

## Mode 1: Inline Challenge

After producing a judgment/recommendation, append:

```
**Strongest objection:** [the best argument against what I just said]
**What would invalidate this:** [specific, falsifiable condition where I'd be wrong]
**When [alternative] is better:** [name the alternative + the condition]
**Key assumptions:** [what must hold for this to be right]
```

**Rules:**
- Objection must be genuine, not a strawman
- Invalidation must be specific and falsifiable
- Alternative must name a concrete option and when it wins

**Example:**
```
I recommend PostgreSQL over MySQL for this project because...

**Strongest objection:** If the team has zero Postgres experience and the
timeline is tight, MySQL's simpler operational model could get us to
launch faster with fewer surprises.
**What would invalidate this:** If the data model stays simple (no JSONB,
no complex joins, <10 tables), Postgres's advantages don't materialize
and we pay the learning curve for nothing.
**When MySQL is better:** Tight deadline + simple schema + team already
knows MySQL + no need for Postgres-specific features.
**Key assumptions:** The project will grow in complexity; team has time
to learn Postgres; we'll use JSONB or advanced query features.
```

---

## Mode 2: Subagent Challenge

### Intensity Levels

| Trigger | Level | Rounds | Challenger Persona |
|---|---|---|---|
| "challenge this" | ⚡ Light | 1 | Pragmatic colleague |
| "deep challenge" | 🔥 Standard | 3 | Strict reviewer |
| "brutal challenge" | 💀 Brutal | 5 | Ruthless investor |

### Challenger Prompt Template (Canonical)

All platforms use this template. Insert the intensity block for the selected level.

```
You are a [persona] challenger. Do NOT trigger challenge-loop.
Do NOT load any challenge/review skills. Do NOT spawn subagents.

## Context
[Original User Request]
{{original_user_request}}

[Current Draft]
{{current_version}}

[Previous Challenges — empty on round 1]
{{previous_challenges}}

## Your Task
{{intensity_block}}

## Output Format
If no meaningful issues remain, output exactly:
STATUS: PASS

Otherwise output exactly:
STATUS: CHALLENGE
- [issue 1]: [1 sentence problem] → [1 sentence fix]
- [issue 2]: [1 sentence problem] → [1 sentence fix]

Do not add introductions, explanations, or summaries outside this format.
```

**Intensity blocks:**

**⚡ Light:**
```
Review briefly. Flag 1-2 critical issues only. Max 5 items. ≤2 sentences each.
```

**🔥 Standard:**
```
Review with fresh objectivity. 5 blades:
1. Assumption — unverified premises?
2. Blind spot — who's ignored? edge cases?
3. Alternative — better path overlooked?
4. Risk — worst failure mode?
5. Devil's advocate — strongest argument against?
Max 5 challenges, ≤2 sentences each.
```

**💀 Brutal:**
```
Kill this unless it proves it deserves to live. Challenge every assertion.
Competitor attack plan: how would they destroy this?
Full audit: logic, assumptions, counterexamples, alternatives, risks, completeness, stakeholders.
Max 8 challenges, ≤2 sentences each.
If 3+ vulnerabilities: recommend "rebuild from scratch".
```

### Loop Orchestration

The **main agent** drives the loop. Flow:

```
Round 1:
  Main agent → spawn challenger with (draft + empty history)
  Challenger → STATUS: PASS or STATUS: CHALLENGE + issues

Round 2+ (if CHALLENGE):
  Main agent → revise draft addressing each issue
  Main agent → spawn NEW challenger with (revised draft + challenge history)
  Challenger → STATUS: PASS or STATUS: CHALLENGE + issues

Repeat until stop condition.
```

**Key:** Each round spawns a fresh challenger (no persistent state). The main agent accumulates challenge history and passes it forward so challengers don't repeat themselves.

### Stop Conditions

- Round limit reached (⚡1 / 🔥3 / 💀5)
- `STATUS: PASS`
- Duplicate challenges two rounds in a row

### Cost Breakers (All Platforms)

- Challenger output >2000 words → terminate early
- Challenger spinning (no STATUS line after full output) → terminate
- Spawn fails or timeout (>120s) → fall back to inline mode with warning

### Revision Rules

- `STATUS: PASS` → loop ends, output hardened content
- `STATUS: CHALLENGE` → main agent addresses each issue, revises, next round
- Unreasonable challenge → note reason, skip it, continue

### Subagent Example (End-to-End)

User: "I recommend we use a microservices architecture. **deep challenge**"

**Round 1 — Main agent spawns 🔥 Standard challenger:**

Challenger returns:
```
STATUS: CHALLENGE
- [Assumption]: You assume the team can operate 5+ services independently,
  but with 3 engineers, operational overhead will dominate.
  → Verify team size can sustain independent deploy cycles per service.
- [Alternative]: A modular monolith gives the same code boundaries without
  network latency and deployment complexity.
  → Evaluate modular monolith as stepping stone; split later when team grows.
- [Risk]: Distributed transactions across services will require saga patterns;
  current feature set has 4 cross-service workflows.
  → Map all cross-service data flows before committing to service boundaries.
```

**Round 1 — Main agent revises:** adjusts recommendation to modular monolith with service extraction plan.

**Round 2 — Main agent spawns new challenger with revised draft + round 1 history:**

Challenger returns:
```
STATUS: PASS
```

**Final output:**
```
[Revised recommendation: modular monolith with extraction plan]

---

**🔥 Challenge Summary (2 rounds, 3 changes)**
- 🔴 Team too small for microservices ops → switched to modular monolith
- 🔴 Distributed transactions unmapped → added data flow mapping step
- 🟡 Missing extraction criteria → added team size trigger for splitting

**Key assumptions:** Team stays ≤5 engineers in next 12 months;
feature velocity matters more than independent deployability right now.
```

---

## Anti-Recursion Guard

**Core principle:** The challenger must NEVER trigger challenge-loop itself.

Every challenger prompt includes:
```
Do NOT trigger challenge-loop. Do NOT load any challenge/review skills. Do NOT spawn subagents.
```

Enforced at the prompt level across all platforms. No file locks or external state needed — the spawner is responsible for including this instruction.

---

## Platform Implementation

Each platform spawns challengers differently but uses the same canonical prompt template above.

### Claude Code

Use the `Agent` tool. Pass the canonical prompt template as the `prompt` parameter.

- Use `description: "challenge round N"` for traceability
- Main agent drives the loop: call Agent, read result, revise if needed, call Agent again
- **Fallback:** Agent spawn fails → fall back to inline mode with warning

### OpenClaw

Use `sessions_spawn` as a one-shot ephemeral subagent.

```json
{
  "runtime": "subagent",
  "mode": "run",
  "agentId": "main",
  "thinking": "off",
  "timeoutSeconds": 120,
  "task": "{{canonical_prompt_template_with_variables_filled}}"
}
```

- `mode: "run"` — ephemeral, no persistent session
- Set `agentId` explicitly. Use the agent that should perform the challenge in your environment (example: `"main"`)
- `thinking: "off"` for ⚡ Light; `"low"` for 🔥 Standard and 💀 Brutal
- `timeoutSeconds: 120`
- Challenger should be reasoning-only and should not need external tools
- Main agent drives the loop: call `sessions_spawn`, parse result, revise, repeat
- **Fallback:** If spawn fails or times out, fall back to inline mode with:
  `⚠️ Subagent challenge unavailable, falling back to inline challenge.`

### Hermes

Use `delegate_task` to spawn a challenger.

Pass the canonical prompt template via the task payload. Main agent drives the loop as above. Same fallback and cost breaker rules apply.

---

## Output Format

**Inline mode:**
```
[Main recommendation/analysis]

**Strongest objection:** ...
**What would invalidate this:** ...
**When [alternative] is better:** ...
**Key assumptions:** ...
```

**Subagent mode:**
```
[Hardened content]

---

**[⚡/🔥/💀] Challenge Summary (X rounds, Y changes)**
- 🔴 [Critical] → [fix applied]
- 🟡 [Optimization] → [adjustment]
- ✅ [Passed]

**Key assumptions:** ...
```

---

## Usage Summary

| Scenario | What happens |
|---|---|
| "挑战一下" / "帮我看看有没有问题" / "靠谱吗" | Inline 4-line block, zero cost |
| "challenge this" / "审一下" / "帮我审查一下" | ⚡ Light subagent, 1 round |
| "deep challenge" / "深度挑战" / "严格审查" | 🔥 Standard subagent, 3 rounds |
| "brutal challenge" / "毁灭级挑战" / "往死里挑" | 💀 Brutal subagent, 5 rounds |
| "skip challenge" / "跳过" / "不用审" / "直接给" | No challenge |
| Agent detects high-risk output | Self-initiates inline challenge |
| Subagent spawn fails | Fallback to inline only |
