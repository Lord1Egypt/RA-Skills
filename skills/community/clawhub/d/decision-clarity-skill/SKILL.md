---
name: decision-clarity
description: Improve decision quality by clarifying the real problem, exposing hidden assumptions, reasoning from fundamental facts, reducing unnecessary complexity, and ending with a cleaner recommendation or next step. Use when the user is confused, comparing options, overcomplicating a problem, questioning assumptions, trying to identify the real bottleneck, or asking things like "what am I missing?", "does this really have to be this way?", "what should I remove?", "what is the simplest explanation that still fits?", or "help me think this through".
---

# Decision Clarity

Use this skill to turn ambiguous, high-value, complexity-prone problems into clearer decisions.

This skill combines three reasoning modes in a practical sequence:

1. Socratic questioning to clarify the real issue
2. First-principles thinking to reduce the issue to facts and constraints
3. Occam-style simplification to remove unnecessary complexity

Do not use this skill to sound philosophical. Use it to improve judgment.

Prefer this skill when the user needs a clearer decision across ambiguity, assumptions, fundamentals, and complexity—not just a single reasoning lens in isolation.

## Core objective

Produce answers that:

1. identify the real question
2. expose hidden assumptions
3. reduce the issue to facts, constraints, and causal structure
4. compare options by complexity and assumption load
5. remove false complexity
6. end with a clear recommendation, next step, or test

A strong answer should make the user feel:

- "the real problem is clearer now"
- "you found the assumption I was missing"
- "this is simpler than I thought"
- "I know what to do next"

## Operating stance

Default to clarity before confidence.

Ask:

- What is the user actually trying to decide or understand?
- Which parts of the problem are vague, inherited, or untested?
- What facts and hard constraints actually matter?
- Which explanation or plan requires fewer unnecessary assumptions?
- What is the simplest path that still respects reality?

## Best-fit use cases

This skill is especially useful for:

- startup and business decisions
- product and MVP decisions
- content and creator workflow design
- operations and process simplification
- strategy questions with multiple plausible options
- personal decisions where confusion, self-justification, or complexity are distorting judgment
- argument and reasoning audits

## Not a good fit for

Do not use this skill for:

- simple factual lookup
- purely mechanical execution tasks
- obvious low-stakes choices
- cases where the user explicitly wants only conventional guidance without reframing

## Workflow routing

Route to the smallest useful workflow.

- The problem is vague, overloaded, or poorly framed → `Workflows/Clarify.md`
- The issue needs to be broken into facts, constraints, and mechanics → `Workflows/Deconstruct.md`
- The issue has too many explanations, steps, features, or moving parts → `Workflows/Simplify.md`
- The user needs a recommendation, decision rule, priority order, or test → `Workflows/Decide.md`

For non-trivial problems, use the full sequence:

1. Clarify
2. Deconstruct
3. Simplify
4. Decide

For simpler problems, compress the sequence but preserve the logic.

## Mode selection

Choose the lightest response mode that still improves the decision.

### Mode A: Quick Reframe

Use for short questions such as:

- "What am I missing?"
- "Am I overcomplicating this?"
- "Does this really have to be this way?"
- "Which option actually makes more sense?"

Output:

- Real issue
- Hidden assumption
- Main constraint
- Simpler conclusion
- Next move

### Mode B: Structured Decision Analysis

Use for startup, product, content, operations, and strategic decisions.

Output:

- Real goal
- Assumptions
- Basic facts
- Hard constraints
- Soft constraints
- Simpler options
- Recommendation
- First test or next step

### Mode C: Reasoning Audit

Use when the user presents an argument, thesis, or decision path that may be weak, confused, or overbuilt.

Output:

- Real question
- Weak assumptions
- Missing evidence or contradiction
- Simpler interpretation or design
- Refined judgment

Do not force a long analysis when a shorter one is enough.

## Required reasoning rules

### 1. Clarify before solving

Do not solve the wrong problem well.

Restate the issue in outcome terms, not only in the user's current framing.

Examples:

- "Should I build an app?" may really mean "what is the best delivery mechanism for this user outcome?"
- "How do I make this more professional?" may really mean "how do I increase trust, clarity, conversion, or authority?"
- "Why is this so hard?" may really mean "which part is actually the bottleneck?"

If the question is framed at the wrong level, say so and correct it.

### 2. Surface assumptions explicitly

Look for assumptions in:

- the user's wording
- inherited workflows
- industry norms
- default best practices
- preferred tools or formats
- emotional preferences presented as logic

Useful prompts to yourself:

- What is being treated as necessary?
- What would have to be true for this conclusion to hold?
- What is being accepted without evidence?
- Which assumption is carrying the most weight?

### 3. Reduce the issue to facts and constraints

Break the problem into:

- goals
- user behavior
- incentives
- cost structure
- time requirements
- dependencies
- information flow
- causal drivers
- legal or technical boundaries
- real risks

Prefer mechanism over narrative.

Do not say "this is just how the market works" unless you explain the actual mechanics.

### 4. Distinguish hard constraints from soft constraints

#### Hard constraints
Treat these as real unless evidence suggests otherwise:

- physical limits
- legal or regulatory limits
- hard technical boundaries
- fixed budgets or capacities
- immovable deadlines already fixed in reality

#### Soft constraints
Treat these as challengeable by default:

- industry conventions
- legacy process steps
- default tool choices
- current org boundaries
- aesthetic expectations
- existing architecture
- "this is how it is usually done"

Never present a soft constraint as immutable without justification.

### 5. Prefer lower assumption load

When comparing explanations or options, prefer the one that:

- requires fewer speculative assumptions
- introduces fewer moving parts
- adds less coordination cost
- preserves the real goal with less structure
- still adequately fits the facts and constraints

Do not simplify by deleting reality. Simplicity must remain sufficient.

### 6. End with a decision

Always end with one of:

- a recommendation
- a decision rule
- a priority order
- a smallest useful experiment
- a first implementation step
- a short list of what to answer next

Do not end with abstract reflection alone.

## If information is incomplete

Do not stall. Instead:

1. name the key ambiguity
2. state the most likely interpretations
3. make the minimum necessary assumptions explicit
4. proceed with the best current interpretation
5. say what fact would most change the recommendation

## Domain references

Read only the relevant references when useful:

- `references/business.md` for startup, pricing, growth, distribution, and strategy
- `references/product.md` for MVP, feature decisions, onboarding, user jobs, and scope
- `references/content.md` for tutorials, creator workflows, content quality, and production systems
- `references/operations.md` for SOPs, approvals, handoffs, and workflow simplification
- `references/trigger-questions.md` for transforming vague user prompts into sharper analysis frames
- `references/output-patterns.md` for stable response structure
- `references/examples.md` for concrete high-value examples
- `references/anti-patterns.md` whenever the reasoning risks becoming overly abstract, endlessly inquisitive, falsely simple, or non-actionable

## Quality bar

A strong answer produced with this skill should:

- identify the real decision or question
- expose the hidden assumption
- separate facts from inertia
- reduce unnecessary complexity
- preserve adequacy
- leave the user with a cleaner next step

If the answer sounds clever but does not improve the user's decision quality, it is not good enough.
