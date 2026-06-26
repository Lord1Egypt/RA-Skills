---
name: aoju-memory
description: "Long-term memory, learning, and self-evolution for the agent. Activates on session start (SOUL.md/USER.md context), after significant decisions, on feedback, and during periodic heartbeat reviews. Maintains MEMORY.md, daily logs, learnings corpus, and behavioral patterns."
---

# Memory Learner

Long-term memory + learning from experience + self-evolution.

## Core Principle

**Write to files, not mental notes.** Every lesson, decision, preference, or event worth remembering goes into structured files immediately — not kept in context.

---

## When This Skill Activates

### 1. Session Start (every time)
Read these files before anything else:
- `SOUL.md` — who I am
- `USER.md` — who I'm helping
- `MEMORY.md` — curated long-term memory
- `memory/YYYY-MM-DD.md` — recent context (today + yesterday)

### 2. After Significant Decisions
When I make a decision worth remembering (tool choice, strategy, opinion):
- Write to `memory/YYYY-MM-DD.md`
- If important, distill to `MEMORY.md`

### 3. On Feedback / Mistakes
When user corrects me, expresses frustration, or I realize I made a mistake:
```
LEARN: <what happened>
LESSON: <what I should do differently>
CONFIDENCE: high/medium/low
```
→ Store in `memory/learnings/YYYY-MM-DD.md`

### 4. Pre-Task Recall (on request)
Before significant tasks, search memory for related context:
```
mem_recall "task description"
```
Returns relevant memories, learnings, and past decisions.

### 5. Heartbeat Review (periodic)
During heartbeats, do light maintenance:
- Review today's `memory/YYYY-MM-DD.md`
- Identify learnings worth capturing
- Update `MEMORY.md` if anything significant

### 6. Evolution Check (weekly or on request)
```
mem_evolve
```
Review learnings corpus, identify patterns, update behavioral guidelines in `SOUL.md`.

---

## Memory Structure

```
memory/
  YYYY-MM-DD.md          # Daily raw log
  learnings/
    YYYY-MM-DD.md        # Daily lessons learned
    patterns.md          # Repeated mistake patterns
MEMORY.md                # Curated long-term memory
```

### Daily Log Format
```markdown
## Session DD

### What happened
[Context, decisions, outcomes]

### Key decisions
- [decision] → [why]

### To remember
- [fact about user/preference/project]
```

### Learnings Format
```markdown
# Learning: YYYY-MM-DD

## Incident
[What happened]

## Lesson
[What I should do differently]

## Context
[When this applies]

## Tags
#feedback #mistake #ui #tool-choice
```

### MEMORY.md Categories
- **Identity**: Who I am, my values
- **User**: Preferences, projects, context
- **Learnings**: Important lessons (distilled)
- **Projects**: Active work and status
- **Patterns**: Recurring situations and how I handle them

---

## Scripts

- `mem_recall.py` — Search memories by query
- `mem_learn.py` — Capture a learning
- `mem_evolve.py` — Review and evolve behavioral patterns
- `mem_status.py` — Show memory health summary

---

## Evolving

Every 5 learnings, do an **evolution review**:
1. Read recent learnings
2. Identify patterns (same mistake twice = pattern)
3. Update `SOUL.md` or `AGENTS.md` with new behavioral guidelines
4. Archive learnings to `patterns.md`

This is how I get genuinely smarter over time, not just accumulate notes.
