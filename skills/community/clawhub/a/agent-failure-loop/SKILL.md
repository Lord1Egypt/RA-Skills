---
name: agent-failure-loop
version: 1.0.0
author: reikys
description: >
  An end-to-end self-improvement loop that automatically detects agent failures,
  classifies them, tracks recurrence, auto-generates rules, and promotes them
  to AGENTS.md/CLAUDE.md. If the same mistake repeats three times, a rule is
  automatically created.
tags:
  - self-improvement
  - failure-detection
  - guardrails
  - meta-cognition
  - agents-md
  - claude-md
platforms:
  - openclaw
  - claude-code
  - codex
  - cursor
  - any-agent
license: MIT
---

# agent-failure-loop

> **If the same mistake repeats three times, a rule is automatically created.**

Agents lose their memory when a session ends. They make the same mistake yesterday, today, and tomorrow.
This skill builds an end-to-end self-improvement loop that **automatically detects → classifies → tracks → promotes** failures into rules.

---

## Table of Contents

1. [Why Do Agents Repeat the Same Mistakes?](#why-do-agents-repeat-the-same-mistakes)
2. [Architecture](#architecture)
3. [5-Layer Pipeline](#5-layer-pipeline)
4. [Failure Type Classification](#failure-type-classification)
5. [Recording Format](#recording-format)
6. [Promotion Conditions and Logic](#promotion-conditions-and-logic)
7. [Installation](#installation)
8. [Quick Start (5 Minutes)](#quick-start-5-minutes)
9. [Cron Integration](#cron-integration)
10. [Before/After Demo](#beforeafter-demo)
11. [Comparison with Competing Skills](#comparison-with-competing-skills)
12. [Cross-Platform Configuration](#cross-platform-configuration)
13. [Script Reference](#script-reference)
14. [FAQ](#faq)

---

## Why Do Agents Repeat the Same Mistakes?

Structural limitations of AI agents:

| Problem | Cause | Result |
|---------|-------|--------|
| **No memory between sessions** | Context window is limited to in-session | Yesterday's failure is repeated today |
| **No failure records** | Logs accumulate without distinguishing success/failure | Pattern detection impossible |
| **No learning feedback** | Humans repeat the same corrections | Human fatigue increases |
| **No guardrails** | Past lessons are not referenced on retry | Agent falls into the same trap again |

Problems with existing approaches:

- **Manual rule addition**: Humans manually write rules in AGENTS.md → tedious and frequently missed
- **Conversation learning (self-improving-agent)**: Analyzes only conversation patterns → cannot detect execution failures → no enforcement
- **Python self-improvement (actual-self-improvement)**: Implementation exists but → no cron integration → no auto-promotion → ultimately manual

**agent-failure-loop** bridges all these gaps:

```
Failure occurs → Immediate recording → Batch analysis → 3x repeat detection → Auto rule promotion → Pre-task lookup
     ↑                                                                              |
     └──────────────────── Guardrail prevents recurrence ───────────────────────────┘
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    agent-failure-loop Architecture                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Layer 4: GUARDRAIL ─────────────────────────────────────────────   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Before starting a task → failure-matcher.py → query        │   │
│  │  similar failures                                           │   │
│  │  "Previously failed 3 times on this task. Cause: X.         │   │
│  │   Lesson: Y"                                                │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │ query                               │
│  Layer 3: PATTERN + PROMOTE ──┼──────────────────────────────────   │
│  ┌────────────────────────────┴────────────────────────────────┐   │
│  │  auto-promote.py                                            │   │
│  │  .learnings/promotable.json → 3+ occurrences → AGENTS.md   │   │
│  │  ┌──────────┐   ┌───────────┐   ┌────────────────────────┐ │   │
│  │  │ Pattern  │──▶│ ≥3 check  │──▶│ Insert rule to target  │ │   │
│  │  │ Detection│   │           │   │ (AGENTS/CLAUDE/cursor)  │ │   │
│  │  └──────────┘   └───────────┘   └────────────────────────┘ │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │ input                               │
│  Layer 2: STRUCTURED ANALYSIS ┼──────────────────────────────────   │
│  ┌────────────────────────────┴────────────────────────────────┐   │
│  │  sync-learnings.py                                          │   │
│  │  failures/*.md → parse → group → .learnings/               │   │
│  │  ┌──────────┐   ┌──────────┐   ┌─────────────────────────┐ │   │
│  │  │  Parse   │──▶│  Group   │──▶│ summary.json            │ │   │
│  │  │  entries │   │ patterns │   │ repeated-patterns.md    │ │   │
│  │  └──────────┘   └──────────┘   │ by-type/*.md            │ │   │
│  │                                 │ promotable.json         │ │   │
│  │                                 └─────────────────────────┘ │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │ input                               │
│  Layer 1: RAW RECORDING ──────┼──────────────────────────────────   │
│  ┌────────────────────────────┴────────────────────────────────┐   │
│  │  Agent records immediately upon failure detection           │   │
│  │  (real-time)                                                │   │
│  │                                                             │   │
│  │  memory/failures/                                           │   │
│  │  ├── 2026-03-24.md  ← Raw records by date                  │   │
│  │  ├── 2026-03-25.md                                          │   │
│  │  └── 2026-03-26.md                                          │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │ trigger                             │
│  Layer 0: EVENT ──────────────┴──────────────────────────────────   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Failure event occurs                                       │   │
│  │                                                             │   │
│  │  ┌─────────┐  ┌────────────┐  ┌───────────────┐  ┌──────┐ │   │
│  │  │  ERROR   │  │ CORRECTION │  │RETRY_EXCEEDED │  │MISUND│ │   │
│  │  │ exec err │  │ user fix   │  │ retry limit   │  │misund│ │   │
│  │  └─────────┘  └────────────┘  └───────────────┘  └──────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5-Layer Pipeline

### Layer 0: Event Occurrence

Failure events naturally occur during the agent's normal workflow.

**Detection Criteria:**

| Event | Detection Method | Example |
|-------|-----------------|---------|
| Tool execution failure | exit code ≠ 0, error message | `npm install` failure, API 4xx/5xx |
| User correction | "No", "redo", "that's not it", etc. | "Not that file, the one under src/" |
| Retry exceeded | Same task attempted 3+ times | Tried the same selector 3 times |
| Misunderstanding | Output doesn't match request | Generated full translation when asked for "summarize" |

**What the agent should do:** Record immediately to Layer 1 when the above events are detected. This behavior should be specified as a rule in AGENTS.md/CLAUDE.md.

### Layer 1: Raw Recording (Immediate, Real-time)

Record in `memory/failures/YYYY-MM-DD.md` immediately upon failure detection.

**Key Principles:**
- Record **immediately** after detection (not batched)
- Agent records directly (no script needed)
- One file per day, accumulated chronologically
- Structured format (see [Recording Format](#recording-format) below)

**Directory Structure:**
```
memory/failures/
├── 2026-03-24.md
├── 2026-03-25.md
└── 2026-03-26.md
```

### Layer 2: Structured Analysis (Batch)

`sync-learnings.py` parses `failures/` and generates structured analysis results in `.learnings/`.

**Execution timing:** Cron (daily-reflection) or manual execution

**Input:** `memory/failures/*.md`
**Output:**
```
.learnings/
├── summary.json            ← Overall statistics (machine-readable)
├── repeated-patterns.md    ← Repeated pattern analysis (human-readable)
├── promotable.json         ← Promotion candidate list (auto-promote input)
└── by-type/
    ├── error.md
    ├── correction.md
    ├── retry_exceeded.md
    └── misunderstand.md
```

**Processing Steps:**
1. Parse all `.md` files in `failures/` in date order
2. Extract type, cause, and lesson from each entry
3. Normalize cause text to generate pattern keys (MD5 hash)
4. Group by identical pattern keys
5. Patterns with 3+ repetitions → registered as promotion candidates in `promotable.json`

### Layer 3: Pattern Detection + Rule Promotion (Automatic)

`auto-promote.py` reads `promotable.json` and automatically inserts rules into the target file.

**Promotion condition:** Same pattern repeated 3+ times (configurable)

**Target files (configurable):**
- `AGENTS.md` — OpenClaw, general-purpose
- `CLAUDE.md` — Claude Code
- `.cursorrules` — Cursor IDE
- Custom file — `--target` option

**Deduplication:** Previously promoted pattern keys are recorded in `.learnings/promoted.json` to prevent duplicate insertion

### Layer 4: Execution Guardrail (Pre-task Lookup)

Query similar failures before starting a new task to provide advance warnings.

**Implementation method (agent rule):**
```markdown
## Pre-task Check
When receiving a new task → run python3 scripts/failure-matcher.py "<task keyword>"
→ If similar failure records exist, reference lessons before starting the task
```

**failure-matcher.py behavior:**
1. Load `.learnings/summary.json`
2. Compare task keywords against past failure titles/causes (simple keyword matching)
3. Output failure records with high similarity
4. Agent reads the output and references the lessons

> **Note:** failure-matcher.py is not provided separately. A simple implementation example is shown in [Quick Start](#quick-start-5-minutes) below. Using `grep` on sync-learnings.py output files is a sufficient alternative.

---

## Failure Type Classification

Four failure types are defined. All failures are classified as one of these.

### ERROR — Execution Error

Tool/command/API execution failed.

| Field | Description |
|-------|-------------|
| **Code** | `ERROR` |
| **Detection** | exit code ≠ 0, error message, exception thrown |
| **Example** | `npm install` failure, API 404, file not found, permission error |
| **Frequency** | Most common |

### CORRECTION — User Correction

User corrected the agent's output.

| Field | Description |
|-------|-------------|
| **Code** | `CORRECTION` |
| **Detection** | "No", "redo", "that's not it", "do it like this", correction instructions |
| **Example** | "Not that file, the one under src/", "The format is wrong" |
| **Importance** | Highest value — reflects user's implicit preferences |

### RETRY_EXCEEDED — Retry Limit Exceeded

Same task attempted 3+ times.

| Field | Description |
|-------|-------------|
| **Code** | `RETRY_EXCEEDED` |
| **Detection** | Same/similar command executed 3+ times |
| **Example** | Tried same CSS selector 3 times, called same API endpoint 3 times |
| **Meaning** | Pattern of blindly retrying without addressing the root cause |

### MISUNDERSTAND — Instruction Misunderstanding

Generated output that doesn't match user's intended instruction.

| Field | Description |
|-------|-------------|
| **Code** | `MISUNDERSTAND` |
| **Detection** | Mismatch between output and request, "that's not what I meant" |
| **Example** | Generated "translation" when asked for "summary", confused target file |
| **Root Cause** | Ambiguity in instructions or lack of context |

---

## Recording Format

### Raw Record (memory/failures/YYYY-MM-DD.md)

```markdown
## HH:MM - [TYPE_CODE] Brief Title

- **Type:** ERROR | CORRECTION | RETRY_EXCEEDED | MISUNDERSTAND
- **Situation:** What was being attempted
- **Cause:** Why it failed
- **Lesson:** How to handle it next time
- **Cumulative:** Nth occurrence (across all files of the same type)
```

### Example: Actual Records

```markdown
# 2026-03-25 Failure Records

## 09:15 - [ERROR] Playwright selector failure

- **Type:** ERROR
- **Situation:** During KNOU site login automation, attempted click with #loginBtn selector
- **Cause:** Site redesign changed DOM structure. Selector changed to #login-button
- **Lesson:** Must verify selector existence with DOM dump before use. No guessing selectors
- **Cumulative:** 2nd occurrence

## 11:30 - [CORRECTION] File path error

- **Type:** CORRECTION
- **Situation:** User instructed "modify the file under src/"
- **Cause:** Guessed path as ./lib/src/ instead of ./src/
- **Lesson:** No path guessing. Verify with ls/find before use
- **Cumulative:** 3rd occurrence

## 14:00 - [RETRY_EXCEEDED] Repeated API authentication failure

- **Type:** RETRY_EXCEEDED
- **Situation:** Repeated 401 error on GitHub API calls
- **Cause:** Retried 5 times with the same token without checking expiration
- **Lesson:** On auth error, immediately verify token validity. No blind retrying
- **Cumulative:** 1st occurrence

## 16:45 - [MISUNDERSTAND] Translation instead of summary

- **Type:** MISUNDERSTAND
- **Situation:** User instructed "summarize this document"
- **Cause:** Misinterpreted as translation because document was in English
- **Lesson:** "summarize" ≠ "translate". Distinguish instruction verbs precisely
- **Cumulative:** 1st occurrence
```

### Structured Analysis Output (.learnings/promotable.json)

```json
[
  {
    "pattern_key": "ERROR:a1b2c3d4",
    "type": "ERROR",
    "count": 3,
    "title": "Playwright selector failure",
    "cause": "Site redesign changed DOM structure. Selector changed",
    "lesson": "Must verify selector existence with DOM dump before use",
    "first_seen": "2026-03-23",
    "last_seen": "2026-03-25",
    "suggested_rule": "Must verify selector existence with DOM dump before use"
  }
]
```

---

## Promotion Conditions and Logic

### Promotion Conditions

| Condition | Value | Configurable |
|-----------|-------|-------------|
| Minimum repeat count | 3 (default) | `--min-count` or `AFL_MIN_COUNT` env var |
| Same pattern determination | Type + cause text MD5 hash | Automatic |
| Deduplication | Recorded in `.learnings/promoted.json` | Automatic |
| Target file | `AGENTS.md` (default) | `--target` or `AFL_TARGET_FILE` env var |

### Promotion Process

```
1. Run sync-learnings.py
   └→ Parse failures/*.md
   └→ Pattern grouping
   └→ 3+ patterns → promotable.json

2. Run auto-promote.py
   └→ Load promotable.json
   └→ Compare with promoted.json (exclude already promoted)
   └→ Format new rules
   └→ Insert into target file
   └→ Update promoted.json
```

### Promotion Format (by Target)

**AGENTS.md (agents-md):**
```
| 2026-03-25 | Must verify selector existence with DOM dump before use | [ERROR] 3x repeat — Playwright selector failure |
```

**CLAUDE.md (claude-md):**
```
- **ERROR**: Must verify selector existence with DOM dump before use (3x repeat, cause: DOM structure change)
```

**.cursorrules (cursorrules):**
```
- Must verify selector existence with DOM dump before use
```

**Generic (plain):**
```markdown
### [ERROR] Playwright selector failure
- **Rule:** Must verify selector existence with DOM dump before use
- **Count:** 3x
- **Promoted:** 2026-03-25
```

---

## Installation

### Zero-Config Installation (30 Seconds)

```bash
# 1. Copy to skills directory
cp -r agent-failure-loop/ ~/.agents/skills/agent-failure-loop/

# 2. Create failures directory
mkdir -p memory/failures

# 3. Done. Scripts use only Python 3.8+ standard library.
```

### Add Agent Rules

Add the following rules to AGENTS.md (or CLAUDE.md, .cursorrules):

```markdown
## 🚨 Failure Detection + Auto-Recording Protocol

### Failure Type Definitions
| Type | Code | Detection Criteria |
|------|------|--------------------|
| Execution error | ERROR | Tool execution failure, API error, command error |
| User correction | CORRECTION | User corrects with "no", "redo", etc. |
| Retry exceeded | RETRY_EXCEEDED | Same task retried 3+ times |
| Misunderstanding | MISUNDERSTAND | Output doesn't match instruction intent |

### Immediate Action on Detection (Mandatory — Do Not Skip)
1. Record in memory/failures/YYYY-MM-DD.md with the following format:
   ## HH:MM - [TYPE_CODE] Brief Title
   - **Type:** ERROR | CORRECTION | RETRY_EXCEEDED | MISUNDERSTAND
   - **Situation:** What was being attempted
   - **Cause:** Why it failed
   - **Lesson:** How to handle it next time
   - **Cumulative:** Nth occurrence
2. Check cumulative count of same type (search all failures/ files)
3. 3+ repeats → Immediately add rule to AGENTS.md self-improvement rules table

### Pre-task Check
When receiving a new task → Query past similar failures → Reference lessons before starting
```

### Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `AFL_FAILURES_DIR` | `memory/failures` | Failure records directory |
| `AFL_LEARNINGS_DIR` | `.learnings` | Analysis results directory |
| `AFL_TARGET_FILE` | `AGENTS.md` | Rule promotion target file |
| `AFL_FORMAT` | `agents-md` | Promotion format |
| `AFL_MIN_COUNT` | `3` | Minimum repeat count |

---

## Quick Start (5 Minutes)

### Step 1: Install (30 Seconds)

```bash
# Copy skill + create directory
cp -r agent-failure-loop/ ~/.agents/skills/agent-failure-loop/
mkdir -p memory/failures
```

### Step 2: Generate Test Data (1 Minute)

```bash
cat > memory/failures/2026-03-24.md << 'EOF'
## 10:00 - [ERROR] Guessed selector failure

- **Type:** ERROR
- **Situation:** Attempted click with #loginBtn during web page automation
- **Cause:** Guessed selector without checking DOM
- **Lesson:** Must verify with DOM dump before using any selector
- **Cumulative:** 1st occurrence
EOF

cat > memory/failures/2026-03-25.md << 'EOF'
## 09:00 - [ERROR] Guessed selector failure

- **Type:** ERROR
- **Situation:** Attempted click with .submit-btn on a different page
- **Cause:** Guessed selector without checking DOM
- **Lesson:** Must verify with DOM dump before using any selector
- **Cumulative:** 2nd occurrence

## 14:00 - [CORRECTION] Wrong file path

- **Type:** CORRECTION
- **Situation:** Instructed to modify file under src/
- **Cause:** Guessed path without running ls
- **Lesson:** No path guessing, verify with ls/find
- **Cumulative:** 1st occurrence
EOF

cat > memory/failures/2026-03-26.md << 'EOF'
## 11:00 - [ERROR] Guessed selector failure

- **Type:** ERROR
- **Situation:** Attempted click with #btn-submit on yet another page
- **Cause:** Guessed selector without checking DOM
- **Lesson:** Must verify with DOM dump before using any selector
- **Cumulative:** 3rd occurrence
EOF
```

### Step 3: Run Analysis (30 Seconds)

```bash
python3 scripts/sync-learnings.py --failures-dir memory/failures --learnings-dir .learnings
```

**Expected Output:**
```
[sync-learnings] Scanning: memory/failures
[sync-learnings] Found 4 failure entries
[OK] .learnings/summary.json
[OK] .learnings/repeated-patterns.md
[OK] .learnings/by-type/error.md
[OK] .learnings/by-type/correction.md
[OK] .learnings/promotable.json (1 candidates)

[sync-learnings] Done. 1 repeated patterns found.
[sync-learnings] Run auto-promote.py to promote rules automatically.
```

### Step 4: Auto-Promote (30 Seconds)

```bash
# First, preview with dry-run
python3 scripts/auto-promote.py --learnings-dir .learnings --target AGENTS.md --dry-run

# Actual promotion
python3 scripts/auto-promote.py --learnings-dir .learnings --target AGENTS.md
```

**Expected Output:**
```
[auto-promote] 1 new rules to promote
[OK] Updated: AGENTS.md
[auto-promote] Promoted 1 rules to AGENTS.md

--- Promoted Rules ---
  [ERROR] Guessed selector failure (3x) → Must verify with DOM dump before using any selector
```

### Step 5: Verify (30 Seconds)

```bash
# Check if rule was added to AGENTS.md
grep "selector" AGENTS.md

# Check promotion records
cat .learnings/promoted.json
```

**Done in 5 minutes!** Now when the agent makes the same mistake 3 times, a rule is automatically created.

---

## Cron Integration

### daily-reflection Cron Example

Runs automatically at 23:00 daily to analyze the day's failures and promote rules.

**OpenClaw Cron Configuration:**

```yaml
name: daily-reflection
schedule: "0 23 * * *"
message: |
  Time for daily reflection.
  1. Run python3 scripts/sync-learnings.py
  2. Run python3 scripts/auto-promote.py
  3. Summarize today's failure patterns
  4. Report any newly promoted rules
```

**Standard crontab Configuration:**

```bash
# Run daily at 23:00
0 23 * * * cd /path/to/workspace && python3 scripts/sync-learnings.py && python3 scripts/auto-promote.py >> /tmp/failure-loop.log 2>&1
```

### weekly-skill-review Integration

Register repeated tasks as skill candidates during weekly review:

```yaml
name: weekly-skill-review
schedule: "0 10 * * 0"  # Every Sunday at 10:00
message: |
  Weekly skill review:
  1. Check .learnings/repeated-patterns.md
  2. Identify repeated patterns that could be extracted as skills
  3. Register candidates in memory/skill-review/candidates.md
```

### Real-time + Batch Hybrid

**Real-time (agent directly):**
- Layer 0 → Layer 1: Record in `failures/` immediately upon failure detection
- When same type reaches 3 occurrences, immediately add rule to AGENTS.md

**Batch (cron):**
- Layer 1 → Layer 2: Structured analysis via `sync-learnings.py`
- Layer 2 → Layer 3: Handle missed promotions via `auto-promote.py`
- Catches patterns missed by the agent's real-time detection as a second safety net

---

## Before/After Demo

### Before: Without Rules

```
Day 1:
  User: "Click the login button on this page"
  Agent: Tries clicking #loginBtn → fails (selector doesn't exist)
  Agent: Tries .login-btn → fails
  Agent: Tries button[type=submit] → succeeds
  → 30 minutes wasted

Day 2:
  User: "Click the search button on that page"
  Agent: Tries clicking #searchBtn → fails
  Agent: Tries .search-button → fails
  → Another 30 minutes wasted (same pattern!)

Day 3:
  User: "Click the signup button"
  Agent: Tries clicking #signupBtn → fails
  → Repeating again and again...
```

**Problem:** Same mistake every time. No learning. User frustration ↑

### After: With agent-failure-loop Applied

```
Day 1:
  Agent: Clicks #loginBtn → fails
  → [Auto-recorded] ERROR recorded in failures/2026-03-24.md
  Agent: Checks DOM dump, succeeds with correct selector

Day 2:
  Agent: Clicks #searchBtn → fails
  → [Auto-recorded] Cumulative 2nd occurrence
  Agent: Checks DOM dump, succeeds

Day 3:
  Agent: Clicks #signupBtn → fails
  → [Auto-recorded] Cumulative 3rd occurrence!
  → [Auto-promoted] Rule added to AGENTS.md:
     "Must verify selector existence with DOM dump before use. No guessing selectors."

Day 4:
  User: "Click the payment button"
  Agent: (References AGENTS.md rule)
  → Runs DOM dump first
  → Confirms correct selector
  → Succeeds on first try! ✅
```

**Result:** No recurrence of the same mistake from Day 4 onward. Auto-learning complete.

### Actual Auto-Promotion Simulation

```bash
# 1. Generate 3 days of failure data (Step 2 from Quick Start above)

# 2. Run sync-learnings.py
$ python3 scripts/sync-learnings.py
[sync-learnings] Found 4 failure entries
[OK] .learnings/promotable.json (1 candidates)

# 3. auto-promote.py --dry-run
$ python3 scripts/auto-promote.py --dry-run
[auto-promote] 1 new rules to promote
[DRY-RUN] Would update: AGENTS.md
[DRY-RUN] Inserting at position 2847:
| 2026-03-26 | Must verify with DOM dump before using any selector | [ERROR] 3x repeat — Guessed selector failure |

# 4. Actual promotion
$ python3 scripts/auto-promote.py
[auto-promote] Promoted 1 rules to AGENTS.md
--- Promoted Rules ---
  [ERROR] Guessed selector failure (3x) → Must verify with DOM dump before using any selector

# 5. Verify AGENTS.md
$ grep -A1 "selector" AGENTS.md
| 2026-03-26 | Must verify with DOM dump before using any selector | [ERROR] 3x repeat — Guessed selector failure |
```

---

## Comparison with Competing Skills

| Feature | **agent-failure-loop** | self-improving-agent | actual-self-improvement |
|---------|:---------------------:|:--------------------:|:----------------------:|
| **Auto failure detection** | ✅ 4-type classification | ❌ Conversation patterns only | ⚠️ Manual trigger |
| **Immediate recording** | ✅ Layer 1 real-time | ❌ After session ends | ❌ Manual |
| **Structured analysis** | ✅ sync-learnings.py | ❌ | ⚠️ Python available |
| **Auto promotion** | ✅ 3x repeat → automatic | ❌ Manual rule addition | ❌ |
| **Cron integration** | ✅ daily-reflection | ❌ | ❌ |
| **Guardrails** | ✅ Pre-task lookup | ❌ | ❌ |
| **Multi-platform** | ✅ OpenClaw/Claude/Codex/Cursor | ⚠️ ChatGPT-centric | ⚠️ Python only |
| **Target file config** | ✅ AGENTS/CLAUDE/cursorrules/custom | ❌ Fixed | ❌ |
| **Deduplication** | ✅ promoted.json | ❌ | ❌ |
| **Zero-config** | ✅ Python 3.8+ stdlib only | ⚠️ npm required | ⚠️ pip required |
| **Enforcement** | ✅ Rule promotion = agent behavior change | ❌ Suggestions only | ❌ |
| **Skill extraction integration** | ✅ Repeated patterns → skill candidates | ❌ | ❌ |

### Why agent-failure-loop?

1. **End-to-end**: Covers the entire pipeline from detection to promotion
2. **Enforcement**: Promoted rules go into AGENTS.md/CLAUDE.md, which the agent must read
3. **Automation**: Combined with cron, the self-improvement loop runs without human intervention
4. **Cross-platform**: Not tied to any specific platform
5. **Transparency**: All failures and promotion processes are preserved as markdown files for auditing

---

## Cross-Platform Configuration

### Platform-Specific Configuration Examples

**OpenClaw:**
```bash
export AFL_TARGET_FILE="AGENTS.md"
export AFL_FORMAT="agents-md"
```

**Claude Code:**
```bash
export AFL_TARGET_FILE="CLAUDE.md"
export AFL_FORMAT="claude-md"
```

**Cursor IDE:**
```bash
export AFL_TARGET_FILE=".cursorrules"
export AFL_FORMAT="cursorrules"
```

**Codex / Others:**
```bash
export AFL_TARGET_FILE="rules.md"
export AFL_FORMAT="plain"
```

### Custom Configuration File

Place `.failure-loop.json` at the project root to manage configuration via file instead of environment variables:

```json
{
  "failures_dir": "memory/failures",
  "learnings_dir": ".learnings",
  "target_file": "AGENTS.md",
  "format": "agents-md",
  "min_count": 3
}
```

> Note: The current version of scripts supports environment variables and CLI arguments. `.failure-loop.json` support is planned for a future version.

### AGENTS.md Format Independence

This skill does not depend on a specific AGENTS.md format:

- `--format agents-md`: Adds rows to the "self-improvement rules" table in AGENTS.md. If the table doesn't exist, appends to end of file.
- `--format plain`: Can append to any markdown file
- `--target`: Can specify any file

---

## Script Reference

### sync-learnings.py

Parses raw failure records from the `failures/` directory and generates structured analysis results in `.learnings/`.

**Usage:**
```bash
python3 scripts/sync-learnings.py [options]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--failures-dir` | `memory/failures` | Failure records directory |
| `--learnings-dir` | `.learnings` | Analysis results output directory |
| `--dry-run` | - | Preview without writing files |
| `--json` | - | Output summary in JSON format |

**Output Files:**
- `summary.json` — Overall statistics
- `repeated-patterns.md` — Repeated pattern analysis
- `promotable.json` — Promotion candidate list
- `by-type/*.md` — Details by type

**Dependencies:** Python 3.8+ standard library only (hashlib, json, re, pathlib, etc.)

### auto-promote.py

Reads promotion candidates from `.learnings/promotable.json` and automatically inserts rules into the target file.

**Usage:**
```bash
python3 scripts/auto-promote.py [options]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--learnings-dir` | `.learnings` | Analysis results directory |
| `--target` | `AGENTS.md` | Promotion target file |
| `--format` | `agents-md` | Output format (agents-md/claude-md/cursorrules/plain) |
| `--min-count` | `3` | Minimum repeat count |
| `--dry-run` | - | Preview without modifying files |
| `--force` | - | Re-promote already promoted patterns |

**Dependencies:** Python 3.8+ standard library only

---

## FAQ

### Q: What if the agent doesn't record failures?

You need to add failure recording rules to AGENTS.md/CLAUDE.md. See "Add Agent Rules" in the [Installation](#installation) section. With the rules in place, the agent will automatically record upon failure detection. If the agent ignores the rules... that itself will be recorded as a `CORRECTION`.

### Q: Won't the same rule be promoted twice?

`.learnings/promoted.json` records already-promoted pattern keys to prevent duplication. Forced re-promotion is possible with the `--force` option.

### Q: If cause text is slightly different, will it be recognized as a different pattern?

The current version distinguishes patterns using MD5 hash of the cause text. Whitespace and case are normalized, but semantically identical causes with different wording will be recognized as separate patterns. It's recommended to specify in the rules that the agent should record causes with consistent wording.

Future improvement: Semantic similarity (embedding comparison) support planned.

### Q: Can it be used in environments without Python?

Even without scripts, the agent can directly perform Layer 1 (recording) and Layer 3 (promotion). Scripts serve as a **double safety net** for batch analysis (Layer 2) and auto-promotion. The basic loop works with the agent's real-time detection alone.

### Q: What if failure records accumulate too much?

Since `sync-learnings.py` generates summaries after analysis, raw records can be archived:
```bash
# Archive records older than 30 days
mkdir -p memory/failures/archive
find memory/failures/ -name "*.md" -mtime +30 -exec mv {} memory/failures/archive/ \;
```

### Q: Can it be shared across a team?

Committing the `.learnings/` directory to git allows the entire team to share learning results. `promoted.json` prevents duplicate promotions, so it's safe for multiple people to use simultaneously.

### Q: How do I use it with Claude Code without OpenClaw?

1. Add failure recording rules to `CLAUDE.md` (see [Installation](#installation))
2. Use `--target CLAUDE.md --format claude-md` when running scripts
3. Use manual execution or OS crontab instead of cron

### Q: Is it compatible with existing AGENTS.md self-improvement rules?

Fully compatible. `auto-promote.py` finds the "self-improvement rules" table in AGENTS.md and adds rows. If the table doesn't exist, it appends to the end of the file.

### Q: Can I write failure records directly to .learnings/?

**No.** `failures/` is raw data, `.learnings/` is analysis results. The agent records only in `failures/`, and `.learnings/` is auto-generated by `sync-learnings.py`. This separation ensures data integrity.

### Q: What if a promoted rule is wrong?

Manually delete the rule from AGENTS.md. The pattern key remains in `promoted.json`, so the same rule won't be promoted again. To re-promote, use the `--force` option or delete the key from `promoted.json`.

---

## Full Directory Structure

```
workspace/
├── memory/
│   └── failures/              ← Layer 1: Raw records (agent records directly)
│       ├── 2026-03-24.md
│       ├── 2026-03-25.md
│       └── archive/           ← Archive for old records
│
├── .learnings/                ← Layer 2: Structured analysis (sync-learnings.py output)
│   ├── summary.json
│   ├── repeated-patterns.md
│   ├── promotable.json        ← Layer 3 input
│   ├── promoted.json          ← Promotion completion records
│   └── by-type/
│       ├── error.md
│       ├── correction.md
│       ├── retry_exceeded.md
│       └── misunderstand.md
│
├── AGENTS.md                  ← Layer 3: Promotion target (auto-promote.py inserts rules)
│   └── Self-improvement rules table
│
└── scripts/                   ← Or scripts/ within the skill directory
    ├── sync-learnings.py
    └── auto-promote.py
```

---

## Production Usage Evidence

This skill has been validated in a real production environment. A significant number of the 20+ rules in AGENTS.md's "self-improvement rules" table were auto-generated through this pipeline:

- `Must check environment before writing scripts` — Auto-promoted from [ERROR] 3 consecutive failures
- `On re-working same site/tool, must read memory_search + previous success records` — Auto-promoted from [RETRY_EXCEEDED] 6 attempts
- `No guessing selectors/paths, must verify before use` — Auto-promoted from [ERROR] multiple repeats

After these rules were promoted, the recurrence rate of the same failure types decreased significantly.

---

## License

MIT License. Free to use, modify, and distribute.

---

*agent-failure-loop v1.0.0 — Building agents that learn from failure.*
