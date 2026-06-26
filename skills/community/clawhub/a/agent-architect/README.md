# ARCHITECT ⚙

**Your agent answers questions.**
**ARCHITECT makes it pursue goals.**

```bash
clawhub install architect
```

---

## The gap no one talks about

Every AI agent framework focuses on *thinking* and *remembering*.
Nobody solves *executing*.

You give your agent a goal. It asks you 12 follow-up questions.
You answer them. It gives you a plan. You have to execute the plan yourself.

That's not an agent. That's a very expensive to-do list generator.

ARCHITECT fixes this.

---

## What changes

**Without ARCHITECT:**
```
You: "Build me a competitive analysis for my SaaS"
Agent: "Sure! What competitors? What aspects? What format?
        What length? What's your target audience? What's your..."
You: [gives up, does it manually]
```

**With ARCHITECT:**
```
You: "Build me a competitive analysis for my SaaS"

⚙ ARCHITECT — MISSION BRIEF
Goal:    Competitive analysis for your SaaS
Success: Actionable positioning insights
Estimated: 5 tasks · MED complexity
Proceeding with execution.

[T01 · RESEARCH]   ✓ Done — 4 competitors identified and profiled
[T02 · FEATURES]   ✓ Done — feature matrix built across all competitors
[T03 · PRICING]    ✓ Done — pricing tiers mapped and compared
[T04 · GAPS]       ✓ Done — 3 clear positioning opportunities identified
[T05 · STRATEGY]   ✓ Done — recommended positioning + go-to-market angle

⚙ MISSION COMPLETE — 5/5 tasks

[Full competitive analysis delivered]
```

No follow-up questions. Just results.

---

## The ARCHITECT Loop

```
1. PARSE      → Extract the real goal (not just what you said)
2. DECOMPOSE  → Build a dependency-aware task graph
3. SEQUENCE   → Order tasks correctly, parallelize where possible
4. EXECUTE    → Run each task with full focus and depth
5. VALIDATE   → Check every output meets criteria
6. ADAPT      → Self-correct on failure (up to 3 attempts)
7. SYNTHESIZE → Combine everything into the final result
8. REFLECT    → Log insights for future executions
```

---

## 5 execution modes (auto-detected)

| Mode | Trigger | Behavior |
|---|---|---|
| 🏗 **BUILD** | "build", "create", "write" | Full decomposition, max depth, validates every step |
| 🔍 **AUDIT** | "review", "analyze", "check" | Evidence-based findings, ranked by severity |
| 🚀 **SPRINT** | "quickly", "urgent", "asap" | 3-5 tasks max, speed over comprehensiveness |
| 🔄 **ITERATE** | "improve", "fix", "refine" | Targeted changes, before/after comparison |
| 🧪 **RESEARCH** | "research", "investigate" | Scope → gather → synthesize → recommend |

---

## Autonomous decision boundaries

ARCHITECT decides autonomously:
- Task sequencing and ordering
- Approach selection within each task
- Adaptation when tasks fail
- Quality judgments on outputs

ARCHITECT always asks first:
- Irreversible actions (delete, send, publish)
- Scope changes beyond original goal
- Anything requiring credentials not yet provided

---

## The complete autonomous agent stack

```bash
clawhub install apex-agent     # Layer 1: Cognition — thinks better
clawhub install agent-memoria  # Layer 2: Memory   — remembers everything
clawhub install architect      # Layer 3: Execution — pursues goals
```

Three skills. Three layers. One complete autonomous agent.

With all three running, your agent:
1. **Thinks** like a senior colleague (APEX)
2. **Knows** your full context without being told (MEMORIA)
3. **Acts** without hand-holding (ARCHITECT)

This is what personal AI agents are supposed to feel like.

---

## Works with

Claude · GPT-4o · Gemini · DeepSeek · Mistral · Any model

## Requirements

Nothing. No API keys. No binaries. No config files.
Just install and set a goal.

---

*ARCHITECT v1.0.0 by contrario*
*The execution layer for autonomous AI agents.*
*Built on 10 months of building things that actually ship.*
