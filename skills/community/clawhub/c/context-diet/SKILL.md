---
name: context-diet
version: 1.1.1
description: Find out why your agent feels slower and dumber than it used to. Scans everything loaded into context system prompt, skills, memory files, AGENTS.md measures token weight, flags redundancy and bloat, and ships a trim list with exact savings. Use when the agent feels sluggish, responses seem degraded, or before starting a long session. scaneverything loaded into contextsystem promptskillsmemory filesmeasure token weight, flags redundancy and bloat, ships an actionable trim list
---

# Context Diet

Your agent started fast and sharp. Now it's slow and foggy. The reason is almost always the same: **context bloat** — invisible weight that accumulates every time you install a skill, write a memory note, or add an instruction. Context Diet weighs it all and tells you exactly what to cut.


## Onboarding (First Use)

When the user first triggers this skill and `memory/context_diet_state.json` doesn't exist, run a one-time setup:

1. **Introduce capability** (one sentence): _"I can tell you why your agent feels slower and dumber — scan all context bloat sources and output a trim list."_

2. **Quick configuration:**

1. **Diet aggressiveness**(Default: Standard)
   - Conservative (flag obvious redundancy, never suggest removing skills)
- Standard( + suggest removing 60-day unused skills)
   - Aggressive (actively suggest removal/trimming, maximize savings)
2. **Report language**(Default: Follow user input language)

3. **Write initial state file** `memory/context_diet_state.json`(JSON format, with `onboarded: true` and timestamp)

4. **Confirm completion**: _"Setup done! Just use it from now on. Say 'reset settings' anytime to reconfigure."

**Onboarding runs exactly once.** Subsequent activations read the state file directly. When the user says "reset settings", delete the state file and re-run setup.

---

## When to run

1. The agent "feels slower" or gives worse answers than it used to
2. Before starting a long, important session (pre-flight weight check)
3. After installing several new skills (they stack up silently)
4. Periodically, like any diet — monthly keeps things lean

## The scan — 4 weight zones

### Zone 1: System prompt + AGENTS.md + SOUL.md
```
Read AGENTS.md, SOUL.md, IDENTITY.md, USER.md (whichever exist)
For each: count approximate tokens (chars ÷ 4 for English, ÷ 2 for CJK)
Flag: instructions that duplicate each other, outdated rules that no longer apply
```

### Zone 2: Loaded skills (the silent killer)
```
For each skill in the skills directory:
  - Read SKILL.md frontmatter description → this is ALWAYS in context
  - Estimate: description length = permanent tax per conversation turn
  - Check if the skill has large reference files that get eagerly loaded
  - Check: has this skill ever been used? (memory/corpus evidence)
```
Output: a table of every installed skill with its **context tax** (tokens injected per turn) and **last known use**.

### Zone 3: Memory corpus
```
Scan memory/ and MEMORY.md:
  - Total size + entry count
  - Entries older than 60 days that haven't been referenced recently
  - Duplicate facts (same info in multiple files)
  - Stale numbers (old counts, old URLs, finished projects still listed as active)
```

### Zone 4: Session history weight
```
If the current session feels heavy:
  - Estimate conversation token count so far
  - Suggest: /compact or /clear if above threshold
  - Note: this zone is observational (the agent can't count its own context exactly,
    but can estimate from visible conversation length)
```

## The report

```
🔍 Context Diet Report

Total context weight: ~XX,XXX tokens per turn
  Zone 1 (directives):     X,XXX tokens  [X issues]
  Zone 2 (skills):         X,XXX tokens  [X skills loaded, X never used]
  Zone 3 (memory):         X,XXX tokens  [X stale entries]
  Zone 4 (session):        X,XXX tokens  [est.]

## Trim list (ranked by savings)

| # | What to cut | Saves | How |
|---|---|---|---|
| 1 | Skill "X" never used + 800 tok description | 800/turn | uninstall |
| 2 | MEMORY.md has 3 finished projects still listed | ~400 | archive to memory/archive.md |
| 3 | AGENTS.md has 2 duplicate rules | ~150 | merge |
| 4 | Skill "Y" eager-loads 2000-token reference | 2000/load | convert to lazy-load |

## After diet
Estimated savings: X,XXX tokens per turn (~X% lighter)
```

## Rules

- **Never delete without asking** — every trim item is a suggestion with evidence, the user decides
- **Token estimates are approximate** — state "≈" and the estimation method; don't pretend precision you don't have
- **Skills zone is the headline** — most users don't realize each installed skill's description sits in every turn; make this the "aha" moment
- **Last-used detection is heuristic** — check memory files for mentions, check if the skill's name appears in any conversation history; "never mentioned ≠ never used" but it's a strong signal
- **Re-run after trims** — confirm the savings landed

## What this is NOT

- Not a token counter for API billing (use the platform's usage dashboard for that)
- Not a context-window overflow detector (the platform handles that)
- This is a **weight-loss coach for your agent** — it makes bloat visible and gives you a trim list
