# Mutation Strategies Reference

## Core Principle

**One small, verifiable change per round.** Large rewrites are not verifiable and will be reverted.

## Mutation Categories

### Type A — Add Constraints
Adding mandatory rules ("must", "never", "always") sharpens vague instructions.

**Examples:**
- "Be careful with X" → "Never use X in production"
- "Try to avoid Y" → "Avoid Y unless explicitly required"
- "Consider Z" → "When Z is detected, you MUST handle it"

### Type B — Strengthen Coverage
Expand trigger conditions and use case coverage.

**Examples:**
- Add new trigger scenario ("When user says X, also handle Y")
- Add boundary condition ("For inputs larger than 1MB, do Z")
- Add error scenario ("If A fails, then B must be called")

### Type C — Add Concrete Examples
Abstract instructions become actionable when illustrated.

**Examples:**
- "Handle errors gracefully" → "When an error occurs: 1) log the error 2) return a user-friendly message 3) preserve state"
- "Optimize for performance" → "Optimize by: a) caching repeated queries b) using lazy loading c) batching where possible"

### Type D — Tighten Vague Language
Replace soft words with firm requirements.

| From | To |
|------|-----|
| "try to" | "must" |
| "consider" | "always check" |
| "might" | "will" |
| "could be" | "is" |
| "may" | "shall" |

### Type E — Improve Error Handling
Add explicit error handling where missing or weak.

**Focus areas:**
- What to do when a tool fails
- What to do when input is malformed
- What to do when external service is unavailable
- What to do when user provides contradictory instructions

### Type F — Remove Redundancy
Eliminate repeated content that adds no new information.

**Signs of redundancy:**
- Same point made with different words
- Over-explaining simple concepts
- Multiple examples covering identical ground
- Lists where natural prose would suffice

### Type G — Improve Transitions
Add connective tissue between sections.

**Before:** "Step 1: Do X. Step 2: Do Y."
**After:** "Step 1: Do X (this prepares for Step 2). Step 2: Using the output from Step 1, do Y."

### Type H — Expand Thin Sections
Identify and elaborate underdeveloped parts.

**Signs of thin sections:**
- Single sentence descriptions
- "TBD" or "to be added" placeholders
- Vague section names with minimal content
- Checklist items without explanation

### Type I — Add Cross-References
Connect related sections so content forms a web, not isolated islands.

**Examples:**
- "See Section X for error handling details"
- "As mentioned in the prerequisites, Y requires Z"
- "This builds on the foundation from Step 1"

### Type J — Adjust Degree of Freedom
Balance constraints vs. flexibility.

**Too constrained:** "Use exactly these 3 tools in this exact order"
**Too loose:** "Use any tools you think are appropriate"
**Balanced:** "Use the appropriate tools for the task. Recommended order: tool A, then B, then C unless D is detected"

## Scoring Matrix

Each mutation type has different risk/reward characteristics:

| Type | Risk | Reward | Best Used When |
|------|------|--------|----------------|
| A | Low | High | Content is vague |
| B | Low | High | Coverage is sparse |
| C | Medium | High | Steps are abstract |
| D | Medium | High | Language is soft |
| E | Low | Medium | Errors missing |
| F | Low | Medium | Content is verbose |
| G | Low | Low | Flow is choppy |
| H | Medium | Medium | Sections are thin |
| I | Low | Low | Sections isolated |
| J | High | High | Balance is off |

## What NOT to Change in One Round

- The fundamental purpose or scope of the content
- More than one section at a time
- Formatting only (adds no testable value)
- Entire rewrites of any section
- Adding content that wasn't requested
