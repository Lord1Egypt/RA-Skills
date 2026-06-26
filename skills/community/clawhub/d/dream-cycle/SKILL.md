---
name: dream-cycle
description: |
  Implement a nightly "dream cycle" for OpenClaw agents that:
  - Reviews and consolidates memory at night
  - Cleans up bloated workspace files
  - Prepares a morning brief for the user
  
  Use when: User wants to implement Ray Fernando's dream cycle concept,
  reduce memory bloat, or set up automated memory maintenance.
---

# Dream Cycle Skill

Based on Ray Fernando's dream cycle concept for OpenClaw memory management.

## Overview

The dream cycle is a nightly process where the agent:
1. **Dreams** (2-4 AM): Reviews memories, connects dots, prunes bloat
2. **Briefs** (7-8 AM): Delivers a morning summary to the user

This keeps Tier 1 memory lightweight while maintaining searchability via QMD.

## Three-Tier Memory System

| Tier | Cost | What's Here |
|------|------|-------------|
| **Tier 1** | ~600 tokens/turn | `AGENTS.md`, `SOUL.md`, `USER.md` — core identity |
| **Tier 2** | 0 tokens | Memory files indexed via QMD — search on demand |
| **Tier 3** | Tool tokens only | Full disk reads — rarely needed |

**Goal:** Keep AGENTS.md under 2,000 bytes, MEMORY.md under 1,500 bytes.

## Templates

### Morning Brief Template

```
🌅 **Morning Brief** - {date}

**Today:** {current tasks/goals}

**Recent Activityy:**
- {esterday's summary from memory}

**Patterns Noticed:**
- {any}

**Suggested recurring themes Focus:**
- {recommendations for the day}

**Memory Stats:**
- AGENTS.md: {size} bytes
- MEMORY.md: {size} bytes
- Indexed chunks: {count}
```

### Dream Audit Report Template

```
🌙 **Dream Cycle Audit** - {date}

**Files Analyzed:**
- AGENTS.md: {size} bytes → {recommendation}
- MEMORY.md: {size} bytes → {recommendation}
- USER.md: {size} bytes → {recommendation}

**Bloat Detected:**
- {list of bloated sections}

**Actions Taken:**
- {list of optimizations applied}

**QMD Index Status:**
- {indexed files count} files indexed
- {total chunks} chunks
```

## Cron Setup

### Dream Job (Nightly)

```yaml
cron: "0 3 * * *"
mode: run
delivery: none
model: {default or lightweight}
```

### Morning Brief Job

```yaml
cron: "0 7 * * *"
mode: session
delivery: announce
channel: {preferred channel}
```

## Usage

1. **First Run:** Create the skill files and cron jobs
2. **Nightly:** Agent silently reviews memories, optimizes files
3. **Morning:** User receives brief summary

## Commands

- `dream now` — Run dream cycle immediately
- `dream audit` — Audit memory files without changes
- `dream brief` — Generate morning brief without full cycle
- `dream status` — Show current memory stats
