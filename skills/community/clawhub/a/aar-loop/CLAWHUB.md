---
name: aar-loop
version: 1.0.0
description: Run an After Action Review on the task or session that just happened, using the US Army's 4-question AAR method, extract concrete lessons, propose (and on approval, write) durable fixes to the skills and rules files the agent loads next time, and log everything to a persistent LESSONS.md so the next session stops repeating the same mistake.
author: coopersimson96
source: https://github.com/coopersimson96/aar-loop
triggers:
  - aar
  - after action review
  - review this session
  - what did we learn
  - run an aar
  - apply the fix
  - fix it
---

# AAR Loop — ClawHub Wrapper

Installed from: https://github.com/coopersimson96/aar-loop

## Quick Start

After any task or session with friction, surprise, or failure:

```
python3 skills/aar-loop/scripts/append_lesson.py --list
python3 skills/aar-loop/scripts/append_lesson.py \
  --lesson "Your concrete lesson here" \
  --expected "What was supposed to happen" \
  --actual "What actually happened" \
  --why "Why there was a difference" \
  --tags "tag1,tag2"
```

## Files

- `SKILL.md` — Full skill documentation and workflow
- `scripts/append_lesson.py` — Lesson writer (stdlib only, no install)
- `../../LESSONS.md` — Persistent lessons file (workspace root)

## Integration

Add to AGENTS.md or project instructions:
```
Read LESSONS.md before starting work on tasks similar to past ones.
Run `python3 skills/aar-loop/scripts/append_lesson.py --list --tag <relevant-tag>` to check past lessons.
```
