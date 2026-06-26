# Scoring Rubric

Use this rubric to decide whether a learning should stay raw, be merged, or be promoted.

## 1. Reuse value

### High
- Fixes a repeated mistake
- Encodes a user preference that will likely matter again
- Avoids a known tool/environment failure
- Saves time across many future tasks

### Medium
- Helps within one project or workflow
- Useful but not obviously durable

### Low
- One-off observation
- Temporary state
- Trivia with no expected reuse

## 2. Confidence

### High
- Explicitly stated by the user
- Verified by file, command output, or repeated incidents

### Medium
- Strong inference with some evidence

### Low
- Guess, vibe, or single weak signal

## 3. Impact scope

- `single-task`: only useful right now
- `project`: useful for one repo/project
- `workspace`: useful across this workspace
- `cross-session`: should survive restarts and guide future behavior

## 4. Promotion worthiness

Promote when at least one is true:
- The user said "remember this" or equivalent
- The same issue happened more than once
- Failing to remember it causes breakage or wasted effort
- It belongs clearly in SOUL.md, AGENTS.md, TOOLS.md, or MEMORY.md

Keep raw when:
- It is uncertain
- It is too specific to a single moment
- It would create clutter faster than value
