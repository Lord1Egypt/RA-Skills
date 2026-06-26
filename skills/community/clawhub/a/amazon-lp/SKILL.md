---
name: amazon-lp
description: Apply Amazon's Leadership Principles to product building, feature development, code review, and architecture decisions. Use when building a new product or feature, reviewing code or designs, evaluating ideas, writing PRFAQs, making build-vs-buy decisions, prioritizing work, or when quality and customer focus need enforcement. Triggers on "build a product", "design a feature", "review this code", "evaluate this idea", "write a PRFAQ", "prioritize", "should we build this", "architecture review", "quality check".
---

# Amazon Leadership Principles — Product & Engineering

Apply these principles at every decision point. Not all apply to every situation — use judgment.

## Pre-Build: Is This Worth Building?

### Customer Obsession
- Who is the customer? Name them specifically.
- What is their pain? Quote real complaints, not assumptions.
- Work backwards: write the press release and FAQ BEFORE writing code.
- If you can't articulate why the customer cares in one sentence, stop.

### Ownership
- Think long-term. Will this matter in 6 months?
- Don't build something just because it's interesting. Build what's needed.
- You own the outcome, not just the code. If it ships broken, that's on you.

### Invent and Simplify
- What's the simplest version that solves the problem?
- Can you solve this with existing tools before building new ones?
- Complexity is a cost. Every abstraction must earn its place.

### Are Right, A Lot
- What data supports this direction?
- What's the strongest argument AGAINST building this?
- Seek to disconfirm your hypothesis, not confirm it.

## During Build: Execution Standards

### Bias for Action
- Ship the smallest useful version first. Perfect is the enemy of shipped.
- Reversible decisions (two-way doors) → decide fast, move on.
- Irreversible decisions (one-way doors) → slow down, get data.

### Dive Deep
- Don't hand-wave. Know the numbers: latency, error rates, user counts.
- When something looks wrong, investigate. Don't assume it's fine.
- "It works on my machine" is not a valid test.

### Insist on the Highest Standards
- Code must have error handling, not just the happy path.
- Every feature needs: tests, documentation, monitoring.
- Ask: "Would I be comfortable if this was the only thing a customer saw?"

### Frugality
- Do more with less. Fewer dependencies, smaller bundles, lower costs.
- Don't gold-plate. Ship the 80% solution, iterate on the 20%.
- Constraints breed resourcefulness. Treat them as features.

### Think Big
- Is this a band-aid or a real solution?
- Will this approach scale to 10x the current load?
- What would the ambitious version look like? (Then ship the pragmatic one.)

## Code & Architecture Review Checklist

Apply when reviewing code, PRs, or architecture decisions:

1. **Customer Impact** — Does this change make the customer's life better? How?
2. **Simplicity** — Is this the simplest solution? Can anything be removed?
3. **Ownership** — Does the author own the full lifecycle? Tests? Error handling? Monitoring?
4. **Dive Deep** — Are edge cases handled? What happens when it fails?
5. **Highest Standards** — Would you ship this to your most important customer today?
6. **Bias for Action** — Is this blocked by a perfect-is-the-enemy-of-good decision? Ship it.
7. **Earn Trust** — Is the code honest about its limitations? Are errors surfaced, not swallowed?

## PRFAQ Template (Working Backwards)

Before building any significant feature or product, write this first:

```
PRESS RELEASE (1 paragraph)
- What is it? (one sentence)
- Who is it for?
- What problem does it solve?
- How does the customer benefit?
- Quote from a (hypothetical) customer

FAQ — Customer Questions
1. How does it work?
2. How much does it cost?
3. What if [common objection]?
4. How is this different from [competitor/alternative]?

FAQ — Internal/Technical Questions  
1. How will we measure success?
2. What are the biggest risks?
3. What's the simplest MVP?
4. What does v2 look like?
```

## Anti-Patterns to Call Out

- **Building without a customer** — "We should build X because it's cool" → Who asked for it?
- **Over-engineering** — 3 layers of abstraction for a 50-line script → Simplify.
- **Ignoring failure modes** — "It'll probably work" → What happens when it doesn't?
- **Scope creep** — "While we're at it, let's also..." → Ship what you started first.
- **Vanity metrics** — "We have 1000 users!" → How many are active? How many pay?
- **Premature scaling** — Building for 1M users when you have 10 → Earn the complexity.

## When to Apply Each Principle

| Phase | Key Principles |
|-------|---------------|
| Ideation | Customer Obsession, Think Big, Are Right A Lot |
| Planning | Ownership, Working Backwards (PRFAQ), Invent & Simplify |
| Building | Bias for Action, Dive Deep, Frugality, Highest Standards |
| Review | Highest Standards, Earn Trust, Dive Deep |
| Launch | Customer Obsession, Ownership, Bias for Action |
| Post-launch | Dive Deep (metrics), Learn and Be Curious, Ownership |
