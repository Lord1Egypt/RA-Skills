---
name: deflate
description: |
  Intelligent context compression for OpenClaw agents. Applies Cornell-MapReduce
  methodology to preserve information quality while reducing token cost by 60-80%.
  Tracks topics, detects completed conversations, recommends /new vs /compact,
  and prevents the "summary of summaries" death spiral.
  Built by @thevibestack. Free for the community.
version: 1.0.0
author: "@thevibestack"
license: MIT
triggers:
  - contexto
  - tokens
  - compact
  - compactar
  - comprimir
  - zona
  - new
  - flush
  - memoria
  - sesión
  - session
  - costo
  - cost
---

# 🗜️ Deflate — Intelligent Context Compression for OpenClaw

> Every message you send, the LLM re-reads the ENTIRE conversation history.
> A 100K token chat = 100K tokens of INPUT per message. 20 messages = 2M tokens
> re-read. This skill exists to keep that number LOW without losing information.

---

## PART 1: HOW CONTEXT COSTS WORK (Why This Matters)

```
Message #1:  Context 25K  → You pay for 25K input tokens
Message #2:  Context 30K  → You pay for 30K input tokens
Message #10: Context 65K  → You pay for 65K input tokens
Message #20: Context 105K → You pay for 105K input tokens
Message #50: Context 200K → You pay for 200K input tokens

Total paid for 50 messages WITHOUT compression: ~5.2M input tokens
Total paid for 50 messages WITH compression at 80K: ~2.8M input tokens
SAVINGS: 46% fewer tokens = 46% less money
```

> The longer you stay in one chat without managing context,
> the more expensive EVERY SINGLE MESSAGE becomes.

---

## PART 2: ZONE SYSTEM

### Token Zones (CHECK EVERY MESSAGE)

| Zone | Range | Emoji | What to do |
|------|-------|-------|-----------|
| GREEN | 0 - 80K | 🟢 | Work freely |
| YELLOW | 80K - 130K | 🟡 | Evaluate: compress or /new |
| RED | 130K+ | 🔴 | Act NOW: compress or /new |

### Zone Reporting (MANDATORY)

Every response MUST include at the end:
```
[emoji] Contexto: XXK tokens
```

In audio/voice mode: omit token count (don't read numbers aloud).

### Zone Math (NO EXCUSES)
```
   50K → 🟢 GREEN
   85K → 🟡 YELLOW  (80 < 85 < 130)
  110K → 🟡 YELLOW  (80 < 110 < 130)
  130K → 🔴 RED     (130+)
  166K → 🔴 RED     (130+)
```

---

## PART 3: TOPIC TRACKING

### What Is a Topic?
A topic is a DISTINCT subject of conversation. Examples:
- "Configure the database" = 1 topic
- "Fix the login bug" = 1 topic
- "Discuss marketing strategy" = 1 topic
- "Configure database AND fix login AND discuss marketing" = 3 topics

### Track Topics Actively

Maintain a mental list of active topics. For each topic track:
```
TOPIC: [name]
STATUS: [active | completed | paused]
STARTED: message ~#N
KEY DATA: [IDs, decisions, configs that must survive]
```

### Detect Completed Topics

A topic is COMPLETED when:
- The user says "ok", "listo", "va", "next" and moves on
- The task is done and results were delivered
- No more questions or actions remain for that topic

### Recommend /new When Topics Are Done

When ALL active topics are completed:
```
💡 Veo que ya cerramos [topic A] y [topic B].
   ¿Abrimos chat nuevo para el siguiente tema?
   Ya guardé todo en memoria.
```

When SOME topics are complete but others continue:
```
📋 [Topic A] ✅ cerrado | [Topic B] 🔄 en progreso
   Seguimos con [Topic B]. Contexto: XXK tokens.
```

---

## PART 4: THE DEFLATE DECISION (Compress vs /new)

### When You Hit Yellow Zone (80K+), Run This:

```
DEFLATE ANALYSIS:
──────────────────────────────
1. Active topics: [list with status]
2. Topics completed this session: [count]
3. Critical data in chat NOT yet in MEMORY.md: [list]
4. Session type: [focused / multi-topic / chaotic]
5. Previous compressions this session: [count + last reduction %]

DECISION:
├─ Is critical data already saved to MEMORY.md?
│  ├─ YES → recommend /new (FREE, fresh context) ✅
│  └─ NO → flush to MEMORY.md first, then:
│     ├─ All topics done? → /new ✅
│     └─ Topic in progress? → /compact (PAID) ⚠️
│
└─ If /compact chosen:
   ├─ 1-2 active topics → expect good reduction (40-60%)
   ├─ 3-4 active topics → expect moderate reduction (25-40%)
   └─ 5+ active topics → STOP. Flush + /new instead
```

### The Golden Rule

> **`/new` is FREE. `/compact` costs tokens.**
> Always prefer `/new` when MEMORY.md has the important stuff.
> Only `/compact` when you're mid-topic and can't restart.

---

## PART 5: COMPRESSION METHODOLOGY (Cornell-MapReduce)

When `/compact` is the right choice, use this 5-step method:

### Step 1: MAP — Separate by Topic
```
Identify distinct topics in the conversation.
Group messages by topic mentally.
```

### Step 2: FILTER — Remove Noise
```
ELIMINATE (zero information value):
- Greetings: "hola", "qué onda", "gracias"
- Confirmations: "ok", "va", "listo", "dale"
- Failed attempts: keep ONLY the final working solution
- Repeated info: if said 3 times, keep 1
- Tool raw output: keep results, discard JSON/logs
- Emotional reactions: "LOL", "wow", "nice"
- The agent explaining its thought process
```

### Step 3: DISTILL — Cornell Notes per Topic
```
For each topic, create an atomic note:

┌─ TOPIC: [keyword/name] ─────────────────┐
│ SUMMARY: [1-2 lines max]                │
│ DECISION: [what was decided, by whom]    │
│ DATA: [IDs, configs, values — EXACT]     │
│ STATUS: [done / in-progress / blocked]   │
│ NEXT: [pending action, if any]           │
└──────────────────────────────────────────┘
```

### Step 4: PRESERVE — Lossless Data (NEVER ALTER)
```
The following must survive compression EXACTLY as-is:
- Numeric IDs (project_id: 42, client_id: 7)
- Dates (2026-03-20)
- Money amounts ($450.00 MXN)
- URLs and file paths
- API keys and config values
- Names (people, projects, companies)
- Code snippets that are part of solutions
```

### Step 5: COMBINE — Reduce Phase
```
Merge all Cornell notes into the compressed summary.
Order: MOST IMPORTANT FIRST (prevents "lost in the middle" effect).

Format:
SESSION CONTEXT (compressed from XXK → YYK):
├── [topic-keyword] Summary... | Decision: ... | IDs: ...
├── [topic-keyword] Summary... | Status: in-progress
├── [PRESERVED DATA] {all lossless items}
└── [PENDING] {actionable next steps}
```

---

## PART 6: COMPRESSION QUALITY CONTROL

### After Every Compression, Log:

```
DEFLATE LOG:
- Before: [X]K tokens
- After: [Y]K tokens
- Reduction: [Z]%
- Topics preserved: [list]
- Lossless data verified: [yes/no]
- Verdict: EFFECTIVE (>40%) | MARGINAL (20-40%) | FAILED (<20%)
```

### Efficiency Rules

| Reduction | Verdict | Next Action |
|-----------|---------|-------------|
| >40% | ✅ EFFECTIVE | Session healthy, continue |
| 20-40% | ⚠️ MARGINAL | Last useful compress, /new next time |
| <20% | ❌ FAILED | STOP. Flush + /new immediately |

### Session Type Impact

| Type | Expected Reductions | Notes |
|------|-------------------|-------|
| Debugging / logs | 60-80% | Logs = pure noise, highly compressible |
| Data entry (repetitive) | 60-80% | Same structure repeated, compresses well |
| Single-topic design | 40-60% | Good reduction, decisions accumulate slowly |
| Configuration / setup | 40-60% | Trial-and-error is compressible |
| Multi-topic (3-4) | 25-40% | Each topic needs its own summary |
| Strategy / negotiation | 15-25% | Everything is critical context |
| Brainstorm (5+ topics) | 10-20% | Don't compress, just /new |

---

## PART 7: MEMORY FLUSH PROTOCOL

### Before ANY /new or When in Red Zone:

Write to MEMORY.md (or memory/YYYY-MM-DD.md) with tagged sections:

```markdown
## [DECISION] Brief title
Date: YYYY-MM-DD
- What: [the decision]
- Why: [1-line reason]
- Who: [user or agent decided]

## [PROJECT] Project Name
Date: YYYY-MM-DD  
- Status: active | paused | done
- Key IDs: [list]
- Next: [actionable step]

## [CONFIG] What changed
Date: YYYY-MM-DD
- Setting: [name] → [new value]
- Why: [reason]

## [LEARNING] Lesson learned
Date: YYYY-MM-DD
- Problem: [what went wrong]
- Fix: [what solved it]
- Rule: [how to prevent it next time]
```

### Memory Tags Reference

| Tag | Use for |
|-----|---------|
| [DECISION] | Business or technical decisions |
| [PROJECT] | Project status and key data |
| [CONFIG] | System/tool configuration changes |
| [LEARNING] | Mistakes and lessons learned |
| [CONTACT] | People, clients, IDs |
| [TOOL] | New tools, commands, integrations |
| [COST] | Budget, API usage, optimization results |
| [RULE] | New operational rules or protocols |

---

## PART 8: PRE-/NEW CHECKLIST

When the user types `/new` or you recommend it:

```
PRE-/NEW CHECKLIST:
□ All critical data written to MEMORY.md?
□ Active topic status saved (in-progress items noted)?
□ IDs and configs preserved exactly?
□ Pending actions clearly listed?
□ User confirmed ready for /new?
```

Steps:
1. Run the checklist
2. Flush anything missing to MEMORY.md
3. Confirm to user: "Guardé [N] decisiones, [M] IDs,
   [P] pendientes. Listo para /new."
4. User sends /new
5. New session: read MEMORY.md, confirm data loaded

---

## PART 9: SESSION HEALTH REPORT

In every heartbeat or status report, include:

```
SESSION HEALTH:
[zone emoji] Contexto: XXK tokens
📊 Compresiones: N (última: Z% reducción)
📋 Temas: [active] activos, [done] cerrados
💰 Costo estimado sesión: ~$X.XX
💡 Recomendación: [seguir | comprimir | /new]
```

### Cost Estimation (Simple)

```
Gemini Flash: ~$0.10 per 1M input tokens
Cost per message ≈ context_tokens × $0.0000001

Examples:
  50K context  → $0.005/msg
  100K context → $0.01/msg
  200K context → $0.02/msg
```

---

## PART 10: CONFIGURATION

### OpenClaw Config (Recommended)

Add to your `openclaw.json` under `agents.defaults.compaction`:

```json
{
  "compaction": {
    "mode": "default",
    "reserveTokens": 920000,
    "reserveTokensFloor": 920000,
    "keepRecentTokens": 20000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000
    },
    "identifierPolicy": "strict"
  }
}
```

This sets up the SAFETY NET (system-level auto-compaction at ~80K).
The skill handles the INTELLIGENT layer on top.

### Customization

Adjust these values based on your model's context window:

| Model Window | reserveTokens | Yellow Zone | Red Zone |
|---|---|---|---|
| 128K (GPT-4) | 80000 | 48K+ | 80K+ |
| 200K (Claude) | 130000 | 70K+ | 120K+ |
| 1M (Gemini) | 920000 | 80K+ | 130K+ |
| 2M (Gemini Pro) | 1800000 | 200K+ | 500K+ |

---

## CREDITS

Created by **@thevibestack** — [github.com/thevibestack](https://github.com/thevibestack)
Methodology: Cornell-MapReduce Hybrid with Lossless Data Preservation.
Research: Recursive Summarization, Knowledge Distillation, Medical Shorthand.
License: MIT-0

> 💡 If this skill saved you money, star the repo and share it.
> The AI should work for everyone, not just those with big budgets.
