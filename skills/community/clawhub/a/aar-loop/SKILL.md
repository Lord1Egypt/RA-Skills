---
name: aar-loop
description: AAR with folder-based lessons, auto-trigger for all tasks, US Army 4-question method for AI agents.
version: 2.0.0
---

# AAR Loop

A human-run version of the Army's After Action Review, pointed at an AI agent's own session. Ask the same 4 questions the Army asks after every rotation at the National Training Center, answer them honestly about what the agent just did, and write down what changed as a result. Do this every session and the agent accumulates real, checkable lessons instead of starting from zero each time.

## Where this comes from

The US Army formalized the After Action Review in the mid-1970s, after Vietnam, as a structured debrief for training exercises. Became official doctrine in 1993 with field manual TC 25-20. Fifty years of practice on one method because it works on a simple mechanism: separate the debrief from blame, and the same mistake gets caught before it repeats.

This skill borrows that mechanism for AI agent sessions. Research parallel: Reflexion (Shinn et al., 2023) showed agents that generate a verbal self-reflection after a failed attempt and carry that reflection into the next attempt outperform agents with no memory of what went wrong.

## The 4 questions

Ask all four, in order, about the task or session just finished. Answer briefly and honestly.

1. **What was supposed to happen?** The plan, the instruction, the expected outcome.
2. **What actually happened?** The real outcome, including partial completions, errors, silent failures.
3. **Why was there a difference?** The actual mechanism, not a mood. "The API caps batch writes at 100" is a why. "I should have been more careful" is not.
4. **What do we do the same or differently next time?** The concrete rule that would have prevented the gap.

If the answer to question 3 is "nothing went wrong, this worked exactly as planned," that is a valid AAR. Write down what worked as a lesson too.

## Folder Structure

Lessons are stored as individual files for scalability:

```
workspace/
├── LESSONS.md              # Index file (like MEMORY.md)
└── lessons/
    ├── 2026-07-31_aar-skill-install.md
    ├── 2026-07-30_thinking-leak.md
    └── 2026-07-29_config-override.md
```

### Individual Lesson File Format

Each lesson file in `lessons/` folder:

```markdown
---
date: 2026-07-31
tags: [config, bug]
task: "Fix thinking leak"
fix_applied: true
---

## What Was Supposed To Happen?
[Expected outcome]

## What Actually Happened?
[Actual outcome]

## Why Was There A Difference?
[Root cause analysis]

## What Can We Learn?
[Concrete, checkable lesson]

## Fix Plan (if applicable)
**Target:** `AGENTS.md`
**Edit:** Add rule about agent-level config override
```

### Index File (LESSONS.md)

`LESSONS.md` serves as an index (like `MEMORY.md`):

```markdown
# Lessons Index

## 2026-07-31 — AAR Skill Installation
- Task: Install AAR skill dari GitHub
- Lesson: Skill dari GitHub perlu manual install, ClawHub belum ada
- Detail: [lessons/2026-07-31_aar-skill-install.md](lessons/2026-07-31_aar-skill-install.md)
- Tags: skill, install

## 2026-07-30 — Thinking Leak Fix
- Task: Fix internal monolog bocor ke chat
- Lesson: Agent-level override bisa nge-bypass global config
- Detail: [lessons/2026-07-30_thinking-leak.md](lessons/2026-07-30_thinking-leak.md)
- Tags: config, bug
```

## Auto-Trigger for ALL Tasks

AAR runs after EVERY task, not just big ones:

| Task Size | AAR Format | Example |
|-----------|------------|---------|
| **Small** (< 5 min, read-only, simple edits) | 1-sentence quick capture | "Lesson: Config override di agent-level bisa bypass global setting" |
| **Medium** (multi-step, file edits, deployments) | Full AAR with fix plan | Complete 4-question analysis |
| **Large** (infra, production, client-facing, irreversible) | Full AAR + verifier review | Complete analysis + second pair of eyes |

**Trigger:** After Verify phase in RPDV workflow.

## Extracting a concrete lesson

Question 4 only pays off if the lesson is specific enough to check later. Test every lesson: could a different agent, six months from now, read this line and know exactly what to do or not do?

**Concrete, checkable (ship these):**
- "Batch size over 100 rows fails with silent timeout; cap batch writes at 100."
- "Agent-level config override bypasses global setting; always check both levels."

**Vague, do not ship:**
- "Write better code."
- "Be more careful with APIs."

## Using the script

```bash
# Create new lesson
python3 scripts/append_lesson.py \
  --task "Task name" \
  --expected "Expected outcome" \
  --actual "Actual outcome" \
  --why "Root cause" \
  --lesson "Lesson learned" \
  --tags "tag1,tag2" \
  --fix-target "file.md" \
  --fix-edit "exact edit"

# List all lessons
python3 scripts/append_lesson.py --list

# Search lessons
python3 scripts/append_lesson.py --search "keyword"
```

The script:
1. Creates individual lesson file in `lessons/` folder
2. Auto-updates `LESSONS.md` index
3. Prevents duplicate entries

## Workflow

1. Finish the task.
2. Ask and answer the 4 questions (out loud or in thinking).
3. Extract 1-3 concrete, checkable lessons.
4. For each lesson, decide if it needs a durable fix. If yes, write fix plan.
5. Run `scripts/append_lesson.py` to create lesson file + update index.
6. Report back: the 4 answers, fix plan status, lesson(s) written.

## Rules

- Every lesson names a specific tool, command, number, file, or condition.
- Every fix plan names an exact target file and exact edit.
- Never apply a fix plan without approval, unless user said "apply" or "fix it".
- Run AAR on ALL tasks, not just big ones. Quick capture for small tasks.
- Check for duplicates before writing.
- Lessons folder structure: `lessons/YYYY-MM-DD_{topic-slug}.md`
- Index file: `LESSONS.md` (like MEMORY.md)

## Loading lessons next session

Two ways to make lessons automatic:

1. **Project-local:** AGENTS.md has pointer: "Read LESSONS.md before starting work."
2. **On demand:** Before similar task, run `python3 scripts/append_lesson.py --search <keyword>`

A lessons file nobody loads is a diary, not a loop. The loop only closes when the next session actually reads it before acting.
