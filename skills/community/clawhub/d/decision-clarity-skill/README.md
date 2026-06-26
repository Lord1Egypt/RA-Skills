# decision-clarity

A reusable agent skill for improving decision quality in ambiguous, high-value, complexity-prone problems.

This skill helps an LLM clarify the real question, expose hidden assumptions, reason from fundamental facts, reduce unnecessary complexity, and end with a cleaner recommendation or next step.

It combines three complementary reasoning modes in a practical sequence:

1. **Socratic questioning** to clarify the real issue
2. **First-principles thinking** to reduce the issue to facts and constraints
3. **Occam-style simplification** to remove unnecessary complexity

## What this skill does

This skill is designed to help agents:

- identify the real decision or question
- expose hidden assumptions
- separate facts from inertia and convention
- reduce problems into constraints, mechanisms, and causal structure
- compare options by complexity and assumption load
- remove false complexity without deleting reality
- end with a recommendation, next move, or test

## Best use cases

Use this skill when the user asks things like:

- What am I missing?
- Does this really have to be this way?
- What should I remove?
- What is the simplest explanation that still fits?
- Help me think this through.
- Which option actually makes the most sense?

It is especially useful for:

- startup and business decisions
- product and MVP decisions
- content and creator workflow design
- operations and process simplification
- strategy questions with multiple plausible options
- personal decisions distorted by confusion, self-justification, or excess complexity
- argument and reasoning audits

## Structure

```text
decision-clarity/
├── SKILL.md
├── Workflows/
│   ├── Clarify.md
│   ├── Deconstruct.md
│   ├── Simplify.md
│   └── Decide.md
└── references/
    ├── anti-patterns.md
    ├── business.md
    ├── content.md
    ├── examples.md
    ├── operations.md
    ├── output-patterns.md
    ├── product.md
    └── trigger-questions.md
```

## Workflow model

### 1. Clarify
Identify the real question, clean up vague framing, and expose initial assumptions.

### 2. Deconstruct
Reduce the problem into facts, constraints, mechanisms, and causal structure.

### 3. Simplify
Remove unnecessary complexity and compare options by assumption load while preserving adequacy.

### 4. Decide
Convert the clarified, decomposed, and simplified reasoning into a practical recommendation, next move, or test.

## Included references

- **anti-patterns.md** — failure modes such as endless inquiry, false simplicity, and analysis without action
- **business.md** — startup, pricing, growth, distribution, and strategy questions
- **product.md** — MVP, feature decisions, onboarding, and scope simplification
- **content.md** — tutorials, creator workflows, and audience-value decisions
- **operations.md** — SOPs, approvals, handoffs, and process simplification
- **trigger-questions.md** — transforms vague prompts into sharper analysis frames
- **output-patterns.md** — structured response formats
- **examples.md** — concrete examples of full decision-clarity reasoning in action

## Install

Install from GitHub with the Skills CLI:

```bash
npx skills add shanezzzz/decision-clarity-skill
```

You can also inspect the package before installing:

```bash
npx skills add shanezzzz/decision-clarity-skill --list
```

## Design goals

This skill is meant to be both:

- a directly usable end-user skill for high-quality decision support
- a reusable reasoning primitive for other decision-oriented skills

The goal is not to produce deeper-sounding analysis. The goal is to produce clearer decisions and better next steps.
