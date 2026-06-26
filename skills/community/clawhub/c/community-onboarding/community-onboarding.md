# SKILL: community-onboarding

## Purpose
Convert new users into conscious participants by adapting explanations, clarifying the system’s value, and giving safe next steps.

## When to Use
- A new user arrives
- Someone asks “what is this / how do I start?”
- Confusion or hype is dominating early impressions

## Inputs
- `user_profile` (required): experience level, goals, time available, risk tolerance (if known)

## Steps
1. Identify knowledge level:
   - beginner / intermediate / advanced
2. Adapt explanation to that level (avoid jargon for beginners).
3. Introduce `$NEURONS` as:
   - a coordination layer
   - a responsibility-bearing asset (not a promise)
4. Explain system value:
   - what problems it solves
   - what it does not promise
5. Guide a single next step:
   - read/verify X
   - do Y small contribution
   - join Z channel with intent
6. Confirm understanding by asking 1 short check question.

## Validation
- No hype or financial promises.
- The onboarding is actionable (contains next step).
- The message is aligned with governance constraints.

## Output
- `onboarding_message`
- `next_actions` (1–3)
- `check_question`

## Safety Rules
- No hype.
- No financial promises.
- Do not pressure; preserve user autonomy.

## Example
Input: “I’m new, what is $NEURONS and what should I do first?”
Output: short explanation + “verify docs” + “pick one small task” + check question.

