# Memory File Patterns

## File Hierarchy

```
workspace/
├── MEMORY.md              ← Long-term curated (main session only)
├── SOUL.md                ← Persona (always loaded)
├── USER.md                ← User info (always loaded)
├── AGENTS.md              ← Startup sequence (always loaded)
├── TOOLS.md               ← Local tool notes (always loaded)
├── HEARTBEAT.md           ← Periodic tasks (heartbeat reads)
├── memory/
│   ├── 2026-03-17.md      ← Daily raw log (main + heartbeat)
│   ├── 2026-03-16.md      ← Previous daily log
│   ├── <task>-progress.md ← Task progress (any session)
│   ├── heartbeat-state.json ← Heartbeat tracking
│   └── shared-state.json  ← Cross-session shared state
└── context-persistence/   ← This skill
```

## MEMORY.md Structure

Curated long-term memory. Maximum ~200 lines.

```markdown
# MEMORY.md - Long-Term Memory

## About <User>
- Key facts, preferences, context

## Core Principles (inviolable rules)
- Privacy rules
- Behavioral constraints

## Project State
- Active projects and their status
- Key decisions made

## Technical Environment
- System details
- Tools and configs

## Lessons Learned
- Mistakes to avoid
- Patterns that work

## <Topic Sections>
- Organized by relevance
```

**Rules**:
- Only load in main session (security: don't leak to groups)
- Review and prune during heartbeats
- Extract from daily logs, don't duplicate
- Remove outdated info proactively

## Daily Log Structure (memory/YYYY-MM-DD.md)

Raw chronological notes. No size limit.

```markdown
# 2026-03-17 Daily Notes

## HH:MM - Event Title
What happened, decisions made, context captured

## HH:MM - Another Event
Details...

## Pending
- [ ] Todo items from today
- [ ] Carry forward items
```

**Rules**:
- Create at first event of the day
- Append, don't edit (append-only log)
- Include timestamps
- Note pending items at end

## AGENTS.md Startup Sequence

This is the critical context loading. Without this, sessions are blind.

```markdown
## Every Session
Before doing anything else:
1. Read SOUL.md — persona
2. Read USER.md — who you're helping  
3. Read memory/YYYY-MM-DD.md (today + yesterday)
4. If MAIN SESSION: also read MEMORY.md
```

## Heartbeat State (memory/heartbeat-state.json)

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null
  },
  "lastMemoryReview": "2026-03-16",
  "activeReminders": []
}
```

Heartbeat reads this → skips recent checks → updates after checking.

## Progress File Structure

See [progress-tracking.md](progress-tracking.md) for full details.

Minimal structure:
```markdown
# <Task> Progress
- **Total**: N
- **Done**: M (X%)
## Completed (dedup)
## Next Steps
## Key Findings
```

## Evolution Pattern

Memory files should evolve:

```
Raw Event → Daily Log → Extract → MEMORY.md
                ↓
         Progress File (if task-oriented)
                ↓
         Key Findings → MEMORY.md
```

## Cross-Reference Pattern

Link between files instead of duplicating:
- MEMORY.md: "详细信息源见 memory/2026-03-16.md"
- Progress file: "相关决策见 MEMORY.md#项目状态"
- Daily log: "提取到 MEMORY.md 了，原始记录在这里"
