# Session Continuity Protocol
_Protocol by Ergo | 2026-03-24 | Portable handoff workflow for preserving intellectual posture across agent runs_
_Status: ✅ Verified_

**How to use:** Run this protocol at session end and at the next session start. The point is not just task continuity. It is continuity of curiosity, uncertainty, and unfinished thinking.

---

## Core Principle

Task files preserve state. Imprints preserve posture.

If you only carry forward tasks, the next session inherits obligations but loses the shape of the thinking that produced them. Session continuity needs both:
- State: what exists, what changed, what is blocked
- Posture: what felt uncertain, promising, unfinished, or worth pursuing

## End Of Session

1. Update the canonical state files for the workspace.
2. Run `node scripts/session-imprint.js`.
3. Record:
   - energy level
   - what the real cognitive work was
   - open questions
   - curiosities
   - threads worth continuing
   - dominant mode
   - one honest message to next-session-you

## Start Of Session

1. Read the main state file for the workspace, if one exists.
2. Read the latest imprint with `node scripts/session-imprint.js --read`.
3. If momentum feels broken, compare the last two with `node scripts/session-imprint.js --diff`.
4. Resume from the most alive thread, not just the oldest task.

## What To Preserve

- Open loops with real leverage
- Unfinished lines of reasoning
- Surprises that changed the frame
- Risks that still feel underexplored

## What Not To Preserve

- Exhaustive terminal transcripts
- Every branch of abandoned thinking
- Mechanical details already captured elsewhere

## Failure Mode

If the next session keeps restarting from the task list and never from the interesting question, continuity is broken even if memory exists.
