# Challenge Loop

Adversarial hardening for AI agent outputs. Two modes: inline self-refutation (zero cost) and independent challenger subagent.

## The Problem

AI agents have two bad habits:
- **Sycophancy** — agreeing with everything you say
- **Overconfidence** — believing their own output is flawless

Challenge Loop adds adversarial scrutiny to catch both.

## Modes

| Mode | What happens | Cost | When to use |
|---|---|---|---|
| **Inline** | 4-line self-refutation appended to response | Zero | Default, quick check |
| **Subagent** | Independent challenger reviews the output | Higher | Deep review, high-stakes decisions |

### Inline Mode

Append a self-refutation block to any judgment-containing output:

```
**Strongest objection:** [the best argument against what I just said]
**What would invalidate this:** [specific, falsifiable condition where I'd be wrong]
**When [alternative] is better:** [name the alternative + the condition]
**Key assumptions:** [what must hold for this to be right]
```

No subagent spawned. No latency. No cost. Just structured self-criticism.

### Subagent Mode

Spawn an independent challenger to attack the output. Three intensity levels:

| Level | Rounds | Challenger persona | Trigger |
|---|---|---|---|
| ⚡ Light | 1 | Pragmatic colleague | "challenge this" / "审一下" |
| 🔥 Standard | 3 | Strict reviewer | "deep challenge" / "深度挑战" |
| 💀 Brutal | 5 | Ruthless investor | "brutal challenge" / "毁灭级挑战" |

The main agent drives the loop: spawn challenger → receive feedback → revise → spawn again → until `STATUS: PASS` or round limit.

## How It Works

```
User triggers challenge
    ↓
[Inline] → Agent appends 4-line self-refutation → Done
    ↓
[Subagent] → Agent spawns challenger subagent
    ↓
Challenger returns STATUS: PASS or STATUS: CHALLENGE + issues
    ↓
If CHALLENGE → Agent revises → Spawn new challenger with history
    ↓
Repeat until PASS or round limit → Output hardened result + summary
```

## Platform Support

All platforms use the same canonical prompt template. Only the spawn mechanism differs.

| Platform | Mechanism |
|---|---|
| **Hermes** | `delegate_task` |
| **OpenClaw** | `sessions_spawn` (mode: run, thinking: off, timeout: 120s) |
| **Claude Code** | `Agent` tool |

## Installation

### Hermes
```bash
cp SKILL.md ~/.hermes/skills/challenge-loop/SKILL.md
```

### OpenClaw / Claude Code
Include `SKILL.md` as a skill or system prompt instruction.

## Trigger Phrases

| Action | English | Chinese |
|---|---|---|
| Inline | "challenge inline" / "any issues?" | "挑战一下" / "批一下" / "靠谱吗" |
| ⚡ Light | "challenge this" / "review this" | "审一下" / "帮我审查一下" |
| 🔥 Standard | "deep challenge" / "strict review" | "深度挑战" / "严格审查" |
| 💀 Brutal | "brutal challenge" | "毁灭级挑战" / "往死里挑" |
| Skip | "skip challenge" / "just give it" | "跳过" / "不用审" / "直接给" |

## Example

User: _"I recommend we use microservices. deep challenge"_

**Round 1 — Challenger returns:**
```
STATUS: CHALLENGE
- [Assumption]: Team can operate 5+ services independently, but 3 engineers
  means operational overhead will dominate.
  → Verify team size can sustain independent deploy cycles.
- [Alternative]: Modular monolith gives same code boundaries without
  network latency and deployment complexity.
  → Evaluate as stepping stone; split later when team grows.
- [Risk]: 4 cross-service workflows require saga patterns.
  → Map all cross-service data flows before committing.
```

**Round 2 — Revised challenger returns:**
```
STATUS: PASS
```

**Final output:**
```
[Revised recommendation: modular monolith with extraction plan]

**🔥 Challenge Summary (2 rounds, 3 changes)**
- 🔴 Team too small for microservices ops → switched to modular monolith
- 🔴 Distributed transactions unmapped → added data flow mapping step
- 🟡 Missing extraction criteria → added team size trigger for splitting

**Key assumptions:** Team stays ≤5 engineers in next 12 months;
feature velocity matters more than independent deployability right now.
```

## Anti-Recursion

The challenger must NEVER trigger challenge-loop itself. Every challenger prompt includes:

```
Do NOT trigger challenge-loop. Do NOT load any challenge/review skills. Do NOT spawn subagents.
```

Enforced at the prompt level. No file locks or external state.

## License

MIT-0 — free to use, modify, and redistribute. No attribution required.
