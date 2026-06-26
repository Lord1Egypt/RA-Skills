---
name: agent-resilience
description: "Agent resilience patterns for surviving context loss, capturing critical details, and self-improvement. Use when: starting complex/long sessions, asked to 'remember' something important, working on multi-step tasks that may span context limits, implementing WAL/write-ahead logging, setting up working buffers, or improving agent behavior after errors/corrections. Triggers on 'remember this', 'don't forget', 'WAL', 'context loss', 'working buffer', 'compaction recovery', or when implementing proactive agent patterns."
---

# Agent Resilience

Patterns for surviving context loss, capturing corrections, and continuously improving.

## WAL Protocol (Write-Ahead Logging)

**The Law:** Chat history is a buffer, not storage. Files survive; context doesn't.

**Trigger — scan every message for:**
- ✏️ Corrections — "It's X, not Y" / "Actually..." / "No, I meant..."
- 📍 Proper nouns — names, places, companies, products
- 🎨 Preferences — styles, approaches, "I like/don't like"
- 📋 Decisions — "Let's do X" / "Go with Y"
- 🔢 Specific values — numbers, dates, IDs, URLs

**If any appear:**
1. **WRITE FIRST** → update `memory/SESSION-STATE.md`
2. **THEN** respond

The urge to respond is the enemy. Write before replying.

## SESSION-STATE.md

Active working memory for the current task. Create at `memory/SESSION-STATE.md`:

```markdown
# Session State
**Task:** [what we're working on]
**Key decisions:** [decisions made]
**Details:** [corrections, names, values captured via WAL]
**Next step:** [what happens next]
```

Reset when starting a new unrelated task.

## Working Buffer (Danger Zone)

When context reaches ~60%, start logging every exchange to `memory/working-buffer.md`:

```markdown
# Working Buffer
**Status:** ACTIVE — started [timestamp]

## [time] Human
[their message]

## [time] Agent
[1-2 sentence summary + key details]
```

Clear the buffer at the START of the next 60% threshold (not continuously).

## Compaction Recovery

Auto-trigger when session starts with a summary tag, or human says "where were we?":

1. Read `memory/working-buffer.md` — raw danger-zone exchanges
2. Read `memory/SESSION-STATE.md` — active task state
3. Read today's + yesterday's daily notes
4. Extract key context back into SESSION-STATE.md
5. Respond: "Recovered from buffer. Last task was X. Continue?"

Never ask "what were we discussing?" — read the buffer first.

## Verify Before Reporting

Before saying "done", "complete", "finished":
1. STOP
2. Actually test from the user's perspective
3. Verify the outcome, not just that code exists
4. Only THEN report complete

Text changes ≠ behavior changes. When changing *how* something works, identify the architectural component and change the actual mechanism.

## Relentless Resourcefulness

Try 10 approaches before asking for help or saying "can't":
- Different CLI flags, tool, API endpoint
- Check memory: "Have I done this before?"
- Spawn a research sub-agent
- Grep logs for past successes

"Can't" = exhausted all options. Not "first try failed."

## Self-Improvement Guardrails

When updating behavior/config based on a lesson:

**Score the change first (skip if < 50 weighted points):**
- High frequency (daily use?) → 3×
- Reduces failures → 3×
- Saves user effort → 2×
- Saves future-agent tokens/time → 2×

**Ask:** "Does this let future-me solve more problems with less cost?" If no, skip it.

Forbidden: complexity for its own sake, changes you can't verify worked, vague justifications.

## Quick Start Checklist

For long/complex tasks:
- [ ] Create `memory/SESSION-STATE.md` with task + context
- [ ] Apply WAL: write corrections/decisions before responding
- [ ] At ~60% context: start working buffer
- [ ] After any compaction: read buffer before asking questions
- [ ] Before reporting done: verify actual outcome
