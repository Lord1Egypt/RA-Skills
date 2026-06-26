# Scoring Heuristics

Do not treat efficiency as only "shorter is better".

Use these ideas when interpreting logs and producing recommendations:

## Signals That Matter

- completion quality
- outcome quality
- interruption count
- time-slot fit
- duration stability

## Practical Interpretation

- A shorter session is not always better.
- A slightly longer focused session may be more valuable than a rushed short session.
- Repeated interruptions are a stronger warning sign than a single long duration.
- A good recurring window is often more useful than one lucky peak result.

## Current Code Reality

The current implementation still leans heavily on duration comparisons.

When speaking to users, prefer language like:
- "historically smoother"
- "more sustainable"
- "better fit for focused work"

Prefer not to overclaim:
- "you are exactly 23% more efficient"

## Suggested Future Composite Score

If the implementation grows, a stronger score should combine:
- completion
- outcome quality
- interruption penalty
- slot fit
- duration fit

Example weighting:

`0.30 completion + 0.20 outcome + 0.20 interruptionPenalty + 0.15 slotFit + 0.15 durationFit`
