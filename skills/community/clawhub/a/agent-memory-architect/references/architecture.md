# Memory Architecture

## Overview

Agent Memory uses a 3-tier storage model inspired by CPU cache hierarchies:
fast access for frequently used data, bulk storage for everything else.

```
┌─────────────────────────────────────────────┐
│  🔥 HOT — hot.md (≤100 lines)              │
│  Always loaded. Confirmed preferences +     │
│  high-frequency patterns. Never decays      │
│  unless reversed by user.                   │
├─────────────────────────────────────────────┤
│  🌡️ WARM — projects/, domains/, agents/     │
│  ≤200 lines each. Loaded on context match.  │
│  Decays to COLD after 90 days unused.       │
├─────────────────────────────────────────────┤
│  ❄️ COLD — archive/                         │
│  Unlimited. Historical reference only.      │
│  Loaded on explicit user query.             │
└─────────────────────────────────────────────┘
```

## Directory Structure

```
~/agent-memory/
├── hot.md              # 🔥 HOT: Always loaded, ≤100 lines
├── corrections.log     # Recent corrections (last 50)
├── index.md            # File manifest with line counts
├── projects/           # 🌡️ Per-project patterns
│   ├── my-app.md
│   └── side-project.md
├── domains/            # 🌡️ Domain-specific knowledge
│   ├── code.md         #    Coding patterns
│   ├── writing.md      #    Writing style
│   └── comms.md        #    Communication rules
├── agents/             # 🌡️ Per-agent HOT memory (multi-agent)
│   ├── coder.md
│   ├── writer.md
│   └── daily.md
└── archive/            # ❄️ COLD: Decayed patterns
    ├── 2025.md
    └── 2026-q1.md
```

## File Formats

### hot.md (HOT Tier)

```markdown
# HOT Memory — Always Loaded

## Preferences
<!-- Confirmed by user. Format: key-value with source. -->
- format: bullet points over prose (confirmed 2026-01-15)
- tone: direct, no hedging (confirmed 2026-01-15)
- code_style: tabs, no semicolons (confirmed 2026-02-01)

## Patterns
<!-- Applied 3+ times. Track last_used for decay. -->
- "looks good" = approval to proceed (used 15x, last: 2026-02-14)
- single emoji = acknowledged, no action needed (used 8x, last: 2026-02-10)

## Recent
<!-- New corrections pending confirmation. Max 10. -->
- prefer SQLite for MVPs (corrected 2026-02-14, 1/3)
- use pnpm not npm (corrected 2026-02-15, 2/3)
```

### corrections.log

```markdown
# Corrections Log

[2026-02-15 14:32] verbose explanation → bullet summary
  Type: communication
  Context: chat response
  Count: 1/3
  Status: pending

[2026-02-14 09:15] Postgres → SQLite for MVP
  Type: technical
  Context: database discussion
  Count: 1/3
  Status: pending
```

### projects/{name}.md

```markdown
# Project: my-app

Inherits: global → domains/code

## Patterns
- Use Tailwind (project standard)
- No Prettier (eslint only)
- Deploy via GitHub Actions

## Overrides
- semicolons: yes (overrides global no-semi for this project)

## Meta
- Created: 2026-01-15
- Last active: 2026-02-15
- Corrections: 12
```

### index.md

```markdown
# Memory Index

| Tier | File | Lines | Updated |
|------|------|-------|---------|
| HOT | hot.md | 42 | 2026-02-15 |
| WARM | projects/my-app.md | 28 | 2026-02-15 |
| WARM | domains/code.md | 67 | 2026-02-10 |
| COLD | archive/2025.md | 189 | 2026-01-01 |

Last compaction: 2026-02-01
```

## Lifecycle Rules

### Correction → Preference Pipeline

```
Correction received
  ↓
Log to corrections.log (count: 1/3)
  ↓
Same correction again → bump count (2/3)
  ↓
Third time → ask user: "Make this permanent?"
  ↓
User confirms → move to hot.md Preferences
User declines → mark as "case-by-case", stop counting
```

### Decay Pipeline

```
Pattern unused 30 days
  ↓
Move from HOT → WARM (domains/ or projects/)
  ↓
Pattern unused 90 days
  ↓
Move from WARM → COLD (archive/)
  ↓
Never auto-delete. User can "forget X" explicitly.
```

### Compaction Pipeline

```
File exceeds line limit (100 for HOT, 200 for WARM)
  ↓
Step 1: Merge similar entries
  "Use tabs" + "Indent with tabs" + "Tab indentation" → "Indentation: tabs (3x)"
  ↓
Step 2: Summarize verbose entries
  "When emailing Marcus, use bullets, ≤5 items, no jargon, BLUF, AM"
  → "Marcus emails: bullets ≤5, no jargon, BLUF, AM"
  ↓
Step 3: Archive oldest unused patterns
  ↓
Step 4: Update index.md
```

## Namespace Inheritance

```
global (hot.md)
  └── domain (domains/code.md)
       └── project (projects/my-app.md)
```

- More specific overrides more general
- Project inherits domain inherits global
- Explicit overrides documented with reason

## Context Loading Strategy

### On Session Start
1. Always load `hot.md`
2. Check `index.md` for context hints
3. If project detected → preload matching `projects/*.md`
4. If domain detected → preload matching `domains/*.md`

### Context Budget Exceeded
1. Load only `hot.md` (minimum viable memory)
2. Load relevant namespace on demand via search
3. Tell user: "Memory partially loaded — HOT only"

## Reversal Protocol

When user changes their mind:

```
1. Archive old pattern (keep history, never delete)
2. Log reversal with timestamp and reason
3. Add new preference as tentative (starts at 1/3)
4. Confirm: "Got it. Changed X → Y. (Previous archived)"
```
