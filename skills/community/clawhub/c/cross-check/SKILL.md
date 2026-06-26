---
name: cross-check
description: "Inline assumption checker that challenges your agent's thinking before responding. Detects complex queries and runs independent verification rounds, identifies blind spots and logical flaws. Two modes: Reinforced (same model, 2 rounds default) and Cross-Check (second model as verifier via sessions_spawn). Compact output by default, detailed on request. Use when: (1) 'cross-check this', (2) 'challenge your assumptions', (3) 'am I missing something?', (4) complex decisions, (5) long prompts where accuracy matters, (6) 'get a second opinion', (7) 'stress-test this idea'. Homepage: https://clawhub.ai/skills/cross-check"
metadata:
  openclaw:
    configPaths:
      - HEARTBEAT.md
    capabilities:
      - sessions_spawn
---

# Cross-Check v2.1

**Install:** `clawhub install cross-check`

Verify assumptions in your responses. Opt-in — the agent suggests verification, you decide.

## Capabilities Used

- **sessions_spawn** — For 2-model verification mode (optional). Requires a second configured model. Only used when user explicitly requests "cross-check 2-model".
- **HEARTBEAT.md** — Reads (never writes) to check if user has enabled auto-suggestions.

## Language

Detect from the user's message language. Default: English.

## How It Works

### Default: Suggest, Don't Auto-Run

When the agent detects a complex response (3+ assumptions), it appends a one-line suggestion:

```
💡 Cross-Check available — reply "cross-check" to verify these assumptions.
```

The user chooses whether to activate. No silent auto-invocation.

### User Activates

| Command | Action |
|---------|--------|
| "cross-check" / "sjekk dette" | Lite mode (2 rounds) |
| "cross-check deep" | Deep mode (3 rounds or 2-model) |
| "cross-check 2-model" | 2-model mode (requires sessions_spawn + second model) |
| "cross-check off" | Disable suggestions for this session |

### Opt-In Auto-Suggestions via HEARTBEAT

If the user adds the following to their `HEARTBEAT.md`:

```markdown
## Cross-Check
- auto-suggest: true
```

...then the agent will suggest Cross-Check when it detects 3+ assumptions, without the user needing to trigger it first. **This is still a suggestion — the user must reply "cross-check" to actually run it.**

## Three Output Levels

### Default — Confidence Note

For responses with 1-2 assumptions, append:
```
Confidence: [High / Medium / Low]
Key assumption: [the main assumption]
```

### Lite — 2 Rounds (same model)

Round 1 "The Analyst": Solve fully, extract assumptions.
Round 2 "The Challenger": Solve from scratch, different angles.

**Output (max 8 lines):**
```
Cross-Check (Lite):
  Agreement: [what both agreed on]
  Difference: [where they disagreed]
  Blind spot: [thing neither considered]
  Confidence: [High / Medium / Low]
```

### Deep — 3 Rounds or 2-Model

**Option A: Reinforced (same model, 3 rounds)**
Round 3 "The Synthesizer": Both answers visible, finds consensus/divergence/blind spots. Includes pre-mortem.

**Option B: Cross-Check (second model)**
Uses `sessions_spawn` to run a verifier sub-agent. Requires a second configured model.
- Step 1: Primary solves, extracts assumptions
- Step 2: Verifier challenges each assumption from 4 perspectives (Skeptic, Expert, Beneficiary, Contrarian)
- Step 3: Primary integrates challenges

**Output (max 15 lines):**
```
Cross-Check (Deep):
  Mode: [Reinforced / Cross-Check]
  Consensus: [findings all rounds agree on]
  Divergence: [where rounds disagreed + resolution]
  Blind spots: [things none considered]
  Assumptions:
    - [assumption]: [confidence] — [confirmed/challenged/revised]
  Confidence: [High / Medium / Low]
```

## Assumption Tracking

Every round tracks: core assumptions, confidence (High/Medium/Low), unknowns, biases.

## Guidelines for Agent

1. **Suggest, don't auto-run** — show "Cross-Check available" line, let user decide
2. **Respect "cross-check off"** — disable suggestions for the session
3. **Check HEARTBEAT.md** — if auto-suggest is enabled, suggest proactively
4. **Compact output** — max 8 lines lite, 15 deep
5. **Never modify files** — reads HEARTBEAT.md only
6. **2-model is optional** — only mention if user asks or has multiple models
7. **Cost awareness** — lite = ~2x tokens, deep = ~3x tokens

## Privacy and Safety

- Session-only — nothing persisted
- No personal data written anywhere
- Verifier receives only problem context + assumptions
- No file writes, no web searches unless user requests
- Uses only OpenClaw's configured providers via sessions_spawn

## What This Skill Does NOT Do

- Does NOT auto-run verification without user opt-in
- Does NOT modify any files
- Does NOT replace the primary model
- Does NOT persist anything
- Does NOT send raw user data externally

## More by TommoT2

- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **context-brief** — Persistent context survival across sessions
- **tommo-skill-guard** — Security scanner for installed skills
- **locale-dates** — Format dates/times for any locale

Install the full suite:
```bash
clawhub install setup-doctor context-brief tommo-skill-guard locale-dates
```
