---
name: agent-memory-loop
version: 2.1.0
description: >
  Lightweight self-improvement loop for AI agents. Capture errors,
  corrections, and discoveries in a fast one-line format, dedup them,
  queue recurring or critical lessons for human-approved promotion, and
  review relevant learnings before major work.
metadata:
  openclaw:
    homepage: https://clawhub.ai/agent-memory-loop
    repository: https://github.com/donzurbrick/agent-memory-loop
    requires:
      bins:
        - grep
        - date
    platforms:
      - darwin
      - linux
author: Don Zurbrick
license: MIT
---

# Agent Memory Loop

Lightweight learning for agents that reset between sessions.

## Use this when

- you want a low-friction way to log mistakes, corrections, and discoveries
- you need recurring lessons without bloating core instructions
- you want human-reviewed promotion instead of auto-writing to instruction files
- you want a quick pre-task scan for known failure patterns

## Do not use it for

- autonomous self-modification
- external content promotion
- heavy multi-section incident writeups by default
- dashboards, registries, or process ceremony

## Core workflow

```text
error / correction / discovery
        ↓
log one line in .learnings/
        ↓
dedup by id, then keyword
        ↓
count:3+ or severity:critical → promotion-queue
        ↓
human reviews promotion
        ↓
check relevant learnings before major work
        ↓
increment prevented:N when a learning actually changed behavior
```

## Install

```bash
bash scripts/install.sh
```

Creates:

```text
.learnings/
  errors.md
  learnings.md
  wishes.md
  promotion-queue.md
  details/
  archive/
```

## Minimal instruction snippet

Add this to your agent instructions:

```markdown
## Self-Improvement
Before major tasks: grep .learnings/*.md for relevant past issues.
After errors or corrections: log a one-line entry using agent-memory-loop.
Never auto-write to SOUL.md, AGENTS.md, TOOLS.md, or similar instruction files.
Stage candidate rule changes in .learnings/promotion-queue.md for human review.
```

## The format, in short

One incident or discovery per line. Extra fields are optional.

```text
[YYYY-MM-DD] id:ERR-YYYYMMDD-NNN | COMMAND | what failed | fix | count:N | prevented:N | severity:medium | source:agent
[YYYY-MM-DD] id:LRN-YYYYMMDD-NNN | CATEGORY | what | action | count:N | prevented:N | severity:medium | source:agent
[YYYY-MM-DD] CAPABILITY | what was wanted | workaround | requested:N
[YYYY-MM-DD] id:LRN-YYYYMMDD-NNN | proposed rule text | target: AGENTS.md | source:agent | evidence: count:N prevented:N | status: pending
```

Key fields:
- `count:N` tracks recurrence
- `prevented:N` tracks loop closure
- `severity:critical` forces review even at count 1
- `source:external` is never promotable

## Operating rules

1. Log fast; prefer a one-line entry over a perfect writeup
2. Dedup before appending
3. Queue recurring or critical lessons for review
4. Humans approve promotions; agents do not
5. Before major work, scan for relevant prior failures
6. If a learning prevented a repeat mistake, record that with `prevented:N`

## References

- `references/logging-format.md` — canonical line formats, fields, examples, source labels
- `references/operating-rules.md` — dedup, review queue, pre-task review, trimming rules
- `references/promotion-queue-format.md` — queue entry structure and status lifecycle
- `references/detail-template.md` — optional detail-file template for complex failures
- `references/design-tradeoffs.md` — why this stays lean instead of turning into a system

## Assets and scripts

- `assets/errors.md`
- `assets/learnings.md`
- `assets/wishes.md`
- `assets/promotion-queue.md`
- `scripts/install.sh`
- `scripts/setup.sh`
- `scripts/review.sh`

## Success condition

The loop is working if agents actually use it:
- learnings are cheap to log
- duplicates stay low
- recurring lessons reach the queue
- promotions stay human-approved
- `prevented:N` starts climbing on real work
