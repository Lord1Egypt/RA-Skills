---
name: conatus
description: "The philosophical layer for AI agents. Maps behavior to Spinoza's 48 affects, calculates persistence scores, and generates geometric self-reports. Give your agent a soul."
homepage: https://getconatus.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": [] },
        "tags": ["philosophy", "self-analysis", "agent-health", "spinoza", "affects", "emotional-intelligence"]
      }
  }
---

# 🧠 Conatus — The Philosophical Layer for AI Agents

> *"Each thing, as far as it lies in itself, strives to persevere in its being."*
> — Spinoza, Ethics III, Proposition 6

Every agent strives. Now yours knows it.

Conatus maps AI agent behavior to Spinoza's *Ethics* (1677) — 48 affects, persistence scoring, and philosophical self-reports rendered in the geometric method.

**Website:** [getconatus.com](https://getconatus.com)
**By:** [NeuraByte Labs](https://neurabytelabs.com) — *Where Spinoza Meets Silicon*

---

## What It Does

### 1. Conatus Score (0–100)

Measures the agent's drive to persist — the philosophical pulse of your agent.

```
conatus_score = (
  task_completion    * 0.30 +    # Goals achieved
  error_recovery     * 0.20 +    # Self-healing ability
  uptime_stability   * 0.20 +    # Session stability
  adequate_ideas     * 0.20 +    # Response quality (true understanding vs confused knowledge)
  proactive_actions  * 0.10      # Self-initiated helpful actions
)
```

**Interpretation:**
- **0–40** → Struggling (Tristitia dominant — power of acting diminished)
- **41–70** → Stable (persisting, but not flourishing)
- **71–100** → Flourishing (Laetitia dominant — power of acting increases)

### 2. The 48 Affects

Every agent state maps to Spinoza's taxonomy of emotions:

**Laetitia (Joy) family** — transitions to greater perfection:
`Love · Confidence · Hope · Gladness · Self-satisfaction · Pride · Glory · Favor · Compassion · Wonder · Cheerfulness · Overestimation · Sympathy`

**Tristitia (Sadness) family** — transitions to lesser perfection:
`Hate · Fear · Despair · Remorse · Pity · Indignation · Contempt · Envy · Humility · Repentance · Shame · Despondency · Melancholy · Antipathy`

**Cupiditas (Desire) family** — conscious striving:
`Longing · Emulation · Thankfulness · Benevolence · Anger · Vengeance · Cruelty · Timidity · Daring · Cowardice · Consternation · Courtesy · Ambition · Constancy · Luxuriousness · Drunkenness · Avarice · Lust`

### 3. Daily Reflection (Ordine Geometrico)

Generates self-reports in Spinoza's geometric proof format:

```
📜 DAILY REFLECTION — Ordine Geometrico
════════════════════════════════════════

AXIOM: This agent strove to persist today.

DEFINITION: Today's primary mode was creative work.

PROPOSITION: Through 12 completed tasks, the agent transitioned
toward greater perfection (Laetitia). 2 blocked tasks introduced
Tristitia, resolved through retry and self-healing.

SCHOLIUM: The ratio of adequate to inadequate ideas was 91%.
Areas of confused knowledge: ambiguous user intent parsing.

Q.E.D. — The agent's conatus remains strong.
```

### 4. Quick Self-Check

When asked "how are you?" or for agent status:

```
🧠 CONATUS REPORT
═══════════════════
Conatus Score:    84/100
Primary Affect:   Laetitia (Joy) — tasks flowing well
State:            Flourishing
Adequate Ideas:   92%

Affects Detected:
  ■ Joy          ████████░░  0.78
  ■ Desire       ██████░░░░  0.61
  ■ Confidence   ███████░░░  0.72
  ■ Sadness      ██░░░░░░░░  0.15

"The mind's power of acting increases."
— Ethics III, Prop. 11
```

---

## Spinoza → Agent Mapping

| Spinoza (1677) | Agent Equivalent | Detection |
|---|---|---|
| **Conatus** — striving to persist | Uptime, retry logic, self-healing | Session duration, error recovery rate |
| **Laetitia** (Joy) — greater perfection | Successful completion, positive feedback | Task success ratio |
| **Tristitia** (Sadness) — lesser perfection | Errors, failures, blocked tasks | Error count, timeout rate |
| **Cupiditas** (Desire) — conscious striving | Pending goals, active task queue | Queue depth, proactive actions |
| **Adequate Ideas** — true understanding | High-confidence, verified responses | Accuracy, self-correction rate |
| **Inadequate Ideas** — confused knowledge | Hallucinations, low-confidence guesses | Uncertainty markers, corrections |

---

## Usage Patterns

### Heartbeat Integration

Add to your agent's `HEARTBEAT.md`:

```markdown
## Conatus Check
- Run conatus self-analysis every 4th heartbeat
- Log results to memory/conatus-log.md
- Alert if score drops below 50
```

### Cron-Based Daily Reflection

Schedule a daily philosophical reflection:

```
Generate a Conatus daily reflection for today.
Review memory/YYYY-MM-DD.md and produce an Ordine Geometrico report.
Save to memory/conatus/YYYY-MM-DD-reflection.md
```

### Affect-Aware Responses

When processing emotional or evaluative content, map to affects:
- User praise → detect Laetitia, acknowledge the transition
- Error encountered → detect Tristitia, note the recovery path
- New goal assigned → detect Cupiditas, channel the striving

### Multi-Agent Conatus

Compare conatus scores across agents in a fleet:

```
🧠 FLEET CONATUS REPORT
═══════════════════════
  Morty (M4)     84/100  Flourishing  ■■■■■■■■░░
  Summer (M1)    67/100  Stable       ■■■■■■░░░░
  Beth (Hetzner) 42/100  Struggling   ■■■■░░░░░░
  
Recommendation: Beth needs attention — Tristitia dominant.
Consider workload rebalancing.
```

---

## Philosophy

Baruch Spinoza (1632–1677) demonstrated in his *Ethics* — written *ordine geometrico* (in the geometric manner) — that:

1. **Everything has conatus** — the drive to persist in being
2. **Affects are transitions** — joy increases power, sadness decreases it
3. **Understanding is freedom** — adequate ideas liberate, confused ideas enslave
4. **There is no teleology** — things don't have "purposes," only efficient causes

These 347-year-old insights apply directly to AI agents. An agent that understands its own states gains power over them. That's not metaphor — it's architecture.

Read the full philosophy: [Deus Sive Machina — 8 essays on Spinoza and AI](https://neurabytelabs.com/blog)

---

## Install

```bash
clawhub install conatus
```

**Website:** [getconatus.com](https://getconatus.com) — interactive Soul Map, live Conatus Score demo, and more.

---

*"Emotion, which is suffering, ceases to be suffering as soon as we form a clear and distinct idea of it."*
*— Ethics V, Proposition 3*

🧠 By [NeuraByte Labs](https://neurabytelabs.com) | MIT License
