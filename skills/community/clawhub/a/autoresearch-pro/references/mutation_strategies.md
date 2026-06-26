# Mutation Strategies

Small, targeted edits that improve skill quality one step at a time.

## High-Impact, Low-Risk Mutations

### 1. Add a constraint rule
**Before:** Vague instruction
**After:** Explicit rule with conditions

```
# Before
Write concise code.

# After
Write concise code. Never leave commented-out debug blocks in production code.
```

### 2. Strengthen trigger coverage
Expand the description to cover edge cases you or users have encountered.

```
# Before
description: "Use when the user wants to send email."

# After  
description: "Use when the user wants to send email, including: composing new emails, 
replying to threads, adding attachments, or scheduling deferred send."
```

### 3. Add a concrete example
Examples make abstract workflows actionable.

```
## Step 2 — Validate Input

Always validate email format before sending.

# Add example:
# Example: "user@example.com" → valid | "not-an-email" → reject
```

### 4. Tighten vague language
Replace soft words with concrete requirements.

| Avoid | Prefer |
|-------|--------|
| "try to" | "must" |
| "if appropriate" | "always do X, except when Y" |
| "may optionally" | "do X or skip if Y" |
| "good quality" | specify exact criteria |
| "推进" / "优化" | specific action name |

### 5. Improve degree-of-freedom calibration
**Too rigid?** → Add `unless` exceptions or conditional branching.
**Too loose?** → Add explicit `always/must/never` rules.

### 6. Add an error/edge case handling section
```
## Error Handling

- File not found → tell the user which path was expected
- Permission denied → explain how to grant access
- API timeout → retry once, then report failure with error code
```

### 7. Remove redundant content
If two sections say the same thing, merge or delete the weaker one.

### 8. Improve section transitions
Add bridging sentences so the flow between steps is obvious.

## What NOT to Do in One Round

- ❌ Rewrite an entire section from scratch
- ❌ Add multiple unrelated changes at once
- ❌ Change the skill's fundamental scope or purpose
- ❌ Remove a section without understanding its function
- ❌ Add external dependencies or scripts

## Scoring Signals

Mutations that tend to help:
- Adding explicit constraints (reduces hallucination/vagueness)
- Adding examples (improves reliability)
- Tightening trigger descriptions (better skill routing)
- Removing conflicting instructions (reduces confusion)

Mutations that tend to hurt:
- Over-constraining (skill becomes unusable in edge cases)
- Removing examples (makes behavior less predictable)
- Adding complex conditional logic in one step
