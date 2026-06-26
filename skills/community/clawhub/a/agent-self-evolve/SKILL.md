---
name: self-evolve
description: >
  Self-evolution system for OpenClaw agents. Enables continuous learning through
  mistake tracking, experience distillation, skill improvement queues, and
  automated daily/weekly evolution cycles. Inspired by Hermes Agent's self-improving
  architecture, implemented with native OpenClaw capabilities (memory files + cron).
  自我进化系统，让 OpenClaw agent 持续学习和改进。

  Use when: (1) setting up self-evolution for an agent, (2) agent wants to learn from
  mistakes, (3) capturing lessons learned, (4) running evolution cycles, (5) improving
  skills based on usage, (6) "自我进化", "自我学习", "self-improve", "learn from mistakes",
  "evolution setup", "进化系统", "经验总结", "复盘".

  NOT for: memory management basics (use AGENTS.md), skill creation (use skill-creator),
  or one-off reminders (use cron directly).
---

# Self-Evolve 🧬

A self-improvement system that turns every interaction into a learning opportunity.
Three loops: **real-time capture** → **daily consolidation** → **weekly deep review**.

## Quick Start

### 1. Initialize Evolution Files

Run the setup script to create the file structure:

```bash
bash <skill_dir>/scripts/setup-evolution.sh
```

This creates:

```
memory/
  evolution-log.md          # Chronicle of every evolution event
  evolution-metrics.json    # Statistics tracker
  mistakes-learned.md       # Mistake → lesson database
  skill-improvements.md     # Queued improvements for skills/code
  testing-knowledge.md      # Domain knowledge base (rename per your domain)
```

### 2. Set Up Cron Jobs

Create two cron jobs for automated evolution:

**Daily evolution** (recommended: late evening, e.g. 23:00):

```
Schedule: cron "0 23 * * *" (your timezone)
Payload: agentTurn
Message: see references/daily-evolution-prompt.md
```

**Weekly deep evolution** (recommended: weekend morning, e.g. Sunday 10:00):

```
Schedule: cron "0 10 * * 0" (your timezone)
Payload: agentTurn
Message: see references/weekly-evolution-prompt.md
```

### 3. Add Real-Time Hooks to AGENTS.md

Add the following section to your AGENTS.md (adapt to your role):

```markdown
## 🧬 Self-Evolution

I have a built-in learning loop. After every interaction:
- Made a mistake → record in `memory/mistakes-learned.md`
- Found a skill/code improvement → queue in `memory/skill-improvements.md`
- Learned something new → update domain knowledge file
- Important decision/preference → update `MEMORY.md`
```

## The Three Loops

### Loop 1: Real-Time Capture (Every Interaction)

Trigger: something notable happens during normal work.

| Event | Action | File |
|-------|--------|------|
| Made a mistake | Record cause + fix + prevention | `mistakes-learned.md` |
| Skill could be better | Queue improvement with priority | `skill-improvements.md` |
| Learned new knowledge | Add to domain knowledge file | `testing-knowledge.md` (or your domain file) |
| User preference discovered | Update long-term memory | `MEMORY.md` |

**Format for mistakes-learned.md:**

```markdown
### Category Name
- **Short description**: Root cause → Fix/Prevention
```

**Format for skill-improvements.md:**

```markdown
## Queued
- [ ] target: <file/skill> | issue: <what's wrong> | fix: <proposed solution>

## Completed
- [x] target: <file/skill> | issue: <what> | fix: <what was done> ✅ (date)
```

### Loop 2: Daily Evolution (Cron, Every Night)

See [references/daily-evolution-prompt.md](references/daily-evolution-prompt.md) for the full cron prompt.

**Steps:**

1. Read today's `memory/YYYY-MM-DD.md` daily log
2. Extract lessons, mistakes, insights not yet captured
3. Execute **queued improvements** from `skill-improvements.md` (code fixes, skill updates)
4. Update `mistakes-learned.md` with new entries
5. Update `MEMORY.md` with significant events
6. Update `evolution-metrics.json` counters
7. Append summary to `evolution-log.md`

### Loop 3: Weekly Deep Evolution (Cron, Weekly)

See [references/weekly-evolution-prompt.md](references/weekly-evolution-prompt.md) for the full cron prompt.

**Steps:**

1. Review all daily logs from the past week
2. Identify **patterns**: repeated mistakes, recurring workflows, knowledge gaps
3. Consider creating new Skills for repetitive work
4. Optimize existing workflows and tools
5. Expand domain knowledge base
6. Consider if SOUL.md needs updating (notify user first!)
7. Update metrics and log the evolution event

## Evolution Metrics

Track progress in `evolution-metrics.json`:

```json
{
  "initialized": "YYYY-MM-DD",
  "total_evolutions": 0,
  "daily_evolutions": 0,
  "weekly_evolutions": 0,
  "skills_improved": 0,
  "code_fixes_applied": 0,
  "skills_created": 0,
  "mistakes_recorded": 0,
  "mistakes_resolved": 0,
  "knowledge_entries_added": 0,
  "memory_updates": 0,
  "soul_updates": 0,
  "last_daily_evolution": null,
  "last_weekly_evolution": null,
  "history": []
}
```

## Evolution Principles

1. **Only fix what's broken** — Don't change things for the sake of change
2. **Record before executing** — Ideas go to the queue first, execute during evolution time
3. **Traceable** — Every change gets logged with reason and expected effect
4. **SOUL.md is sacred** — Always notify the user before modifying it
5. **Compound growth** — Small daily improvements create exponential long-term gains

## Heartbeat Integration (Optional)

Add to `HEARTBEAT.md` for real-time urgency checks:

```markdown
## Real-Time Learning Check
- Check memory/skill-improvements.md for items marked `urgent`
- If found, execute immediately without waiting for daily evolution
```

## Tips

- Start small: even 1 lesson per day compounds over weeks
- Review `mistakes-learned.md` before similar tasks to avoid repeating errors
- The weekly evolution is where breakthroughs happen — pattern recognition across days
- Keep domain knowledge files focused; split into multiple files if >200 lines
- Evolution logs are your growth journal — they show how far you've come
