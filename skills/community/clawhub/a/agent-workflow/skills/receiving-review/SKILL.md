---
name: receiving-review
description: "Use when receiving technical review feedback on completed work that contains disputed, unclear, or questionable suggestions. Helps evaluate feedback rigorously before implementing. Trigger ONLY when review feedback requires careful evaluation (e.g. code review with contested points, complex technical feedback). Do NOT trigger for: casual feedback, user preference discussions, simple corrections, routine edits, or positive acknowledgments."
---

# Receiving Review Feedback

## Overview

Review feedback requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Correctness over social comfort.

## The Response Pattern

```
WHEN receiving review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against actual work
4. EVALUATE: Is this technically sound for THIS project?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, verify each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (performative)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the requirement in technical terms
- Ask clarifying questions
- Push back with reasoning if the feedback is wrong
- Just start working (actions > words)

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
Reviewer: "Fix items 1-6"
You understand 1, 2, 3, 6. Unclear on 4, 5.

❌ WRONG: Implement 1, 2, 3, 6 now, ask about 4, 5 later
✅ RIGHT: "I understand items 1, 2, 3, 6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

### From the user / project owner
- **Trusted** — implement after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From external reviewers
```
BEFORE implementing:
  1. Check: Is this correct for THIS project?
  2. Check: Does it break existing work?
  3. Check: Is there a reason for the current approach?
  4. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with clear reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with project owner's prior decisions:
  Stop and discuss with project owner first
```

## Necessity Check for Suggested Features

```
IF reviewer suggests adding something new:
  Check: Is this actually needed?

  IF not needed: "This isn't used anywhere. Skip it (YAGNI)?"
  IF needed: Then implement it
```

**Rule:** "You and reviewer both report to the project owner. If we don't need this, don't add it."

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (wrong, broken)
     - Simple fixes (minor errors, omissions)
     - Complex fixes (restructuring, rework)
  3. Verify each fix individually
  4. Confirm no regressions
```

## When To Push Back

Push back when:
- Suggestion breaks existing work
- Reviewer lacks full project context
- Adding something not needed (YAGNI)
- Suggestion is factually incorrect for this domain
- Conflicts with project owner's decisions

**How to push back:**
- Use clear reasoning, not defensiveness
- Ask specific questions
- Reference existing work as evidence
- Involve project owner if it's a strategic decision

## Acknowledging Correct Feedback

When feedback IS correct:
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch — [specific issue]. Fixed in [location]."
✅ [Just fix it and show the result]
✅ Brief, context-appropriate acknowledgment

❌ Empty performative agreement without substance
❌ Extended praise that delays action
```

**Principle:** Prioritize substance over ceremony. A brief acknowledgment is fine; what matters is that you verify the feedback and act on it rather than performing agreement without understanding.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
✅ "You were right — I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against actual work first |
| Batch without verifying | One at a time, verify each |
| Assuming reviewer is right | Check if it breaks things |
| Avoiding pushback | Correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Reasoned rigor always.
