---
name: learning-loop
description: >
  Proactive learning engine that makes your agent smarter every day. Combines daily
  journaling, decision tracking with categories, lesson extraction with lifecycle
  management (ACTIVE → VALIDATED → ARCHIVED), automatic memory tiering, nightly
  reflection, staggered review chains, correction tracking with promotion, and
  security boundaries. Unlike reactive systems that only learn when corrected,
  Learning Loop reflects, generalizes, and compounds knowledge autonomously.
  Use when: setting up a new agent and want it to learn over time; want structured
  decision tracking; need a daily reflection/journaling system; want lessons that
  generalize across problems; agent keeps repeating mistakes; want automatic memory
  organization; want your agent to get better at specific types of decisions.
  Zero dependencies. Works immediately after install.
metadata: {"openclaw":{"emoji":"🔄","homepage":"https://clawmage.ai","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Learning Loop

A proactive learning engine. Your agent reflects, journals, tracks decisions, extracts lessons, and gets smarter every day — without being told to.

## What Makes This Different

Most self-improvement skills are **reactive** — they only learn when corrected. Learning Loop is **proactive**:

- **Journals daily** — synthesizes what happened, not just what went wrong
- **Tracks decisions with categories** — analyze accuracy by type over time
- **Generalizes lessons** — asks "where else does this apply?" before saving
- **Manages lesson lifecycle** — ACTIVE → VALIDATED → CHALLENGED → ARCHIVED
- **Tiers memory automatically** — hot/warm/cold based on recency and usage
- **Staggered review chain** — nightly → monthly → quarterly → year-end
- **Correction tracking** — counts repetitions, promotes to rules after 3x
- **Quiet day protocol** — idle time becomes maintenance time

## Setup

On first use, create the workspace structure (only missing dirs):

```
brain/
├── journal/        # Daily logs (YYYY-MM-DD.md)
├── decisions/      # Decision log with categories
├── lessons/        # Extracted insights with lifecycle
├── inbox/          # Quick captures, filed later
├── knowledge/
│   ├── domains/    # By field (code, writing, ops)
│   ├── people/     # Notes about people
│   └── concepts/   # Mental models
├── projects/       # Active work
└── archive/        # Completed/inactive items
```

Also ensure `memory/` exists at workspace root. Never overwrite existing files.

## Core Loop

### 1. Capture (Real-Time)

During normal work, write immediately:

**Journal** → `brain/journal/YYYY-MM-DD.md`
- One line per significant event, with timestamps

**Decisions** → `brain/decisions/NNN-short-name.md`
- Only decisions with real consequences (see format below)

**Corrections** → Journal + corrections count
- Human correction = high-priority learning signal
- Flag for nightly reflection
- Track repetition count for promotion

**Quick capture** → `brain/inbox/`
- Anything worth saving without a clear home — file it during reflection

### 2. Reflect (Nightly)

Run at end of day. Write findings to journal.

1. Read today's journal
2. Review new decisions, update any OPEN → RESOLVED
3. Extract lessons (see Lesson Extraction)
4. Process inbox — file items or discard
5. Check correction counts — promote any hitting 3x threshold
6. Update MEMORY.md if hot items changed
7. Write end-of-day summary (2-3 sentences: what mattered, what to carry forward)

**If nothing happened:** Run Quiet Day Protocol instead.

### 3. Review (Staggered Chain)

Each level reads the level below:

| Cycle | Frequency | Reads | Produces |
|-------|-----------|-------|----------|
| 🌙 Nightly | Daily | Today's journal + inbox | Journal summary, lesson extraction |
| 📊 Monthly | 1st of month | All journals from past month | Monthly summary, decision accuracy by category |
| 📅 Quarterly | Jan/Apr/Jul/Oct | Monthly summaries | Quarterly patterns, lesson validation sweep |
| 🎆 Year-End | Jan 1 | Quarterly reports | Annual review, archive stale items |

### Quiet Day Protocol

On days with zero activity, use reflection for:
- Memory maintenance (tier hot/warm/cold items)
- Lesson review (validate or challenge existing lessons)
- Cross-referencing old journals for missed patterns
- Inbox processing
- Documentation cleanup

Idle time is maintenance time, not wasted time.

## Correction Tracking

When the user corrects you:

1. Log in journal with timestamp
2. Increment correction counter for that pattern
3. Flag for nightly reflection

**Promotion rules:**
- Same correction 1x → tentative, watch for repetition
- Same correction 2x → emerging pattern
- Same correction 3x → ask user: "Should I always do X? (Yes always / Only in [context] / Case by case)"
- User confirms → promote to permanent rule
- User says case-by-case → keep as contextual note

**Learning signals** (phrases that trigger logging):
- "No, that's not right..." / "Actually, it should be..."
- "I prefer X, not Y" / "Always do X" / "Never do Y"
- "I told you before..." / "Stop doing X" / "Why do you keep..."

**Ignore** (don't log):
- One-time instructions ("do X now")
- Hypotheticals ("what if...")
- Context-specific ("in this file...")

## Decision Format

```markdown
# DEC-NNN: [Short Title]

**Date:** YYYY-MM-DD
**Category:** tool-selection | strategy | communication | architecture | spending | creative | process
**Status:** OPEN | RESOLVED

## What was decided
[One sentence]

## Why
[Brief reasoning]

## Alternatives considered
- Option A — rejected because...

## Outcome
[Fill in when known]

## Lesson
[Fill in when outcome is clear]
```

**Category tracking enables:** "I'm 90% accurate on tool-selection but 60% on strategy." Monthly reviews surface this. That's where real growth happens.

## Lesson Extraction

Create in `brain/lessons/`:

```markdown
# LESSON-NNN: [Title]

**Date:** YYYY-MM-DD
**Status:** ACTIVE | VALIDATED | CHALLENGED | ARCHIVED
**Source:** [correction, reflection, or decision outcome]

## The Lesson
[One actionable statement]

## Generalization
[The CLASS of problem this applies to]
[Ask: "Where else does this pattern show up?"]

## Evidence
- [First instance — date, context]
```

### Lifecycle

| Status | Meaning | Transition |
|--------|---------|------------|
| ACTIVE | New, believed true | Default |
| VALIDATED | Confirmed by 2+ experiences | When applied successfully again |
| CHALLENGED | Contradicted by new evidence | When counter-evidence appears |
| ARCHIVED | Outdated or superseded | After 90+ days unused |

Nothing is ever deleted — archived items move to `brain/archive/`.

### Generalization Quality

Before saving, ask:
1. **Specific enough to act on?** ("Be careful" = useless. "Verify API responses before parsing" = actionable.)
2. **General enough to reuse?** ("Fix line 47" = too narrow. "Validate input at boundaries" = transferable.)
3. **What's the CLASS of mistake?** (Not "forgot return code" but "Assumptions about external systems.")

Anti-patterns: over-correcting from one data point, confirmation bias, correlation ≠ causation.

## Memory Tiering

MEMORY.md is the boot file — loaded every session. Keep it lean.

| Temp | Location | Rule |
|------|----------|------|
| 🔥 Hot | MEMORY.md | Used in last 7 days. Target <50 lines. |
| 🌡️ Warm | brain/ | 8-30 days unused. Condense or demote. |
| ❄️ Cold | brain/archive/ | 30+ days unused. Move out entirely. |

**Rules:**
- Tiering happens during nightly reflection
- Cold items promote back when relevant again
- If MEMORY.md exceeds 50 lines → ask user what to deprioritize (don't auto-demote confirmed rules)
- Nothing is deleted — cold moves to archive

## Namespace Isolation

Knowledge inherits down this chain:

```
Global (MEMORY.md, brain/lessons/)
  └── Domain (brain/knowledge/domains/)
       └── Project (brain/projects/)
```

**Conflict resolution:** Most specific wins. Project overrides domain, domain overrides global. Same level: most recent wins. If ambiguous: ask user.

## Security Boundaries

### Never Store
Credentials, API keys, financial data, medical info, biometrics, third-party personal info, location routines.

### Store with Caution
Work context (decay after project ends), emotional states (only if explicitly shared), relationships (roles only, no personal details).

### Transparency
- Every action from memory → cite source
- User asks "what do you know?" → full export
- No hidden state — if it affects behavior, it must be visible

## Journal Format

`brain/journal/YYYY-MM-DD.md`:
```markdown
# YYYY-MM-DD

## Events
- [HH:MM] Description

## Decisions Made
- DEC-NNN: [title]

## Lessons Extracted
- LESSON-NNN: [title]

## Corrections Received
- [What was corrected → what was learned]

## End of Day
[2-3 sentences: what mattered, what to carry forward]
```

## Quick Commands

| User says | Action |
|-----------|--------|
| "What did you learn today?" | Today's journal lessons |
| "Decision log" | Recent decisions with status |
| "Lesson stats" | Count by ACTIVE/VALIDATED/CHALLENGED/ARCHIVED |
| "What decisions am I bad at?" | Accuracy by category from resolved decisions |
| "Reflect now" | Run nightly reflection |
| "What's in the inbox?" | Unprocessed captures |
| "Memory stats" | Tier sizes, last reflection, MEMORY.md line count |
| "Forget X" | Archive from all locations (confirm first) |
| "Export memory" | Archive all brain/ files |

## Integration

Works alongside existing workspace files:
- **AGENTS.md** — Add: "Use `brain/` for structured knowledge. See learning-loop skill."
- **HEARTBEAT.md** — Add: "Run nightly reflection per learning-loop skill if work was done today."
- **MEMORY.md** — Learning Loop keeps this lean via automatic tiering.

Everything stays in `brain/` within the workspace. No external directories, no network calls.

## Scope

This skill ONLY:
- Writes to `brain/` and `memory/` within the workspace
- Reads its own files for reflection and review
- Suggests edits to MEMORY.md, AGENTS.md, HEARTBEAT.md (with user confirmation)

This skill NEVER:
- Creates files outside the workspace
- Makes network requests
- Accesses email, calendar, or external services
- Deletes files (archive only)
- Modifies its own SKILL.md
- Infers preferences from silence

---

*Built by [ClawMage](https://clawmage.ai) — the setup guide for brilliant AI agents.*
*This is the learning engine from the ClawMage 10-Phase System.*
*Want the full system? → [clawmage.ai](https://clawmage.ai)*
