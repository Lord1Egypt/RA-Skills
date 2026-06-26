---
name: cognitive-debt-guard
version: 1.0.0
description: Cognitive Debt Guard - Prevent the 23.5% incident spike from AI-generated code. Comprehension gates, review frameworks, and AI-free zones. Based on 2026 research.
emoji: 🧠
tags: [cognitive-debt, code-quality, ai-safety, review, comprehension]
---

# Cognitive Debt Guard 🧠

Prevent the 23.5% incident spike from AI-generated code.

## The Problem (2026 Research)

| Metric | Impact |
|--------|--------|
| Incident rate | +23.5% per PR with AI code |
| Code churn | 3.1% → 5.7% (nearly doubled) |
| Developer speed | -19% slower with AI tools (experienced devs) |
| Trust in AI output | 33% (down from higher) |

**Root cause:** Teams ship code faster than they understand it.

**Definition:** Cognitive debt = the gap between what your codebase does and what your team comprehends about it.

Unlike technical debt (code you know is bad), cognitive debt is code you don't even know is bad — because you never understood it.

## The Solution: 5 Patterns

### Pattern 1: Maintain MEMORY.md 🔒

**Living architecture context** for humans and AI agents.

```markdown
# MEMORY.md Template

## Architecture Decisions
- [Decision 1]: Why we chose X over Y
- [Decision 2]: Trade-offs we accepted

## AI-Free Zones (human must own completely)
- Authentication & authorization
- Payment processing
- Data deletion
- Database migrations
- Security-critical paths

## Conventions
- Naming: [rules]
- Error handling: [pattern]
- Testing: [requirements]

## Known Constraints
- [Performance requirement]
- [Compliance requirement]
- [Integration dependency]
```

**Rule:** MEMORY.md is open in editor at all times when working with AI.

### Pattern 2: Comprehension Gate 🔒

**3 questions before accepting AI-generated code:**

```
Before you click "Accept" on AI output:

1. Can I explain what this code does in plain language?
   [ ] Yes → Continue
   [ ] No → STOP. Read until you can.

2. Can I trace the data flow from input to output?
   [ ] Yes → Continue
   [ ] No → STOP. Add comments or simplify.

3. If this breaks in production, would I know where to look?
   [ ] Yes → Accept
   [ ] No → STOP. Add logging or documentation.
```

**Rule:** All 3 must be YES before merge.

### Pattern 3: Pair with Agents, Don't Delegate 🔒

| Active Use ✅ | Passive Use ❌ |
|--------------|----------------|
| Prompt → Read → Understand → Modify → Ship | Prompt → Accept → Ship → Forget |
| You steer, AI fills | AI decides, you accept |
| Comprehension maintained | Cognitive debt accumulates |

**Rule:** Never accept >50 lines of AI code without reading and understanding every line.

### Pattern 4: Shrink the Blast Radius 🔒

**AI-assisted PR limits:**

| Constraint | Limit |
|------------|-------|
| Max lines per AI PR | 200 |
| Concerns per PR | 1 |
| Test coverage on AI paths | 100% |
| Files touched | ≤5 |

**Why:** Smaller PRs = easier to comprehend = less cognitive debt.

### Pattern 5: Quarterly Comprehension Audit 🔒

**90-minute sprint ceremony:**

```
## Cognitive Debt Audit Agenda

1. Review top 5 AI-heaviest PRs from last quarter
2. For each PR, ask:
   - Can we still explain what it does?
   - Have we had incidents related to it?
   - Is documentation up to date?
3. Identify cognitive debt hotspots
4. Plan debt reduction for next sprint
5. Update MEMORY.md with new learnings
```

## Code Review Framework (5 Layers)

When reviewing AI-generated code:

```
Layer 1: Comprehension
- Can I understand this without running it?
- Is naming clear?
- Is complexity justified?

Layer 2: Correctness
- Does it do what it claims?
- Edge cases covered?
- Error handling present?

Layer 3: Integration
- Fits existing patterns?
- No duplicate functionality?
- Dependencies appropriate?

Layer 4: Security
- No exposed secrets?
- Input validation?
- AI-free zone respected?

Layer 5: Maintainability
- Tests included?
- Documentation added?
- Will I understand this in 6 months?
```

## Trigger Phrases

This skill activates when:
- User accepts AI-generated code
- User asks about code review
- User mentions "AI code", "generated code", "copilot wrote"
- User is about to merge AI-assisted PR
- User asks "should I accept this?"

## Quick Reference Card

```
Before Accepting AI Code:
1. Read it (all of it)
2. Explain it (out loud if needed)
3. Trace data flow
4. Check AI-free zone
5. Limit: 200 lines, 1 concern
```

## Integration

- **EVR Framework** — Verify comprehension before claiming "reviewed"
- **Systematic Debugging** — When cognitive debt causes incidents
- **Memory Guard** — MEMORY.md persists across sessions

## Statistics (cite in discussions)

- METR 2025: -19% speed for experienced devs using AI
- Cortex 2026: +23.5% incidents per PR
- GitClear: Code churn 3.1% → 5.7%
- Stack Overflow 2025: 33% trust in AI output

## License

MIT
