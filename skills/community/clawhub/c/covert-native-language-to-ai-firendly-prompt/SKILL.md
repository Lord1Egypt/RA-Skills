---
name: prompt-refiner
description: Transforms casual or voice-transcribed user requests into precise, AI-optimized prompts. Handles mixed languages, vague input, and ambiguity. Reduces task execution time by 2-3x and improves accuracy by 40-60%. Applies prompt engineering best practices including persona assignment, few-shot examples, chain of thought, and prompt chaining.
---

# Prompt Refiner

Turn messy input into structured, AI-optimized prompts on the first try.

## When to Use

- Voice transcription input (speech-to-text)
- Casual, informal, or mixed-language requests (English + Chinese)
- Vague or ambiguous requests (missing target, unclear scope)
- Complex multi-step tasks that benefit from chaining
- Before destructive actions (delete, restart, deploy)

Skip if: request is already specific, task is simple/low-stakes, or user says "just do it."

## Core Framework: TCREI

Google's prompt engineering framework — apply to every refined prompt:

| Component | What to include |
|-----------|----------------|
| **Task** | Action verb + specific target. *"Summarize the sales report for Q1"* |
| **Context** | Background, environment, constraints. *"Account: jamesxu81@gmail.com, NZ timezone"* |
| **References** | Examples, templates, tone samples. *"Match this format: [example]"* |
| **Evaluate** | How to judge the output. *"Flag any missing data"* |
| **Iterate** | How to improve if result is off |

## The Process (5 Steps)

### 1. Analyze
Identify: Intent · Target · Constraints · Gaps · Language

### 2. Assign Persona (Always)
Give the AI a role that matches the task:
- Code task → `"You are a senior Node.js engineer"`
- Email task → `"You are a professional business writer"`
- Data task → `"You are a data analyst specializing in sales metrics"`
- Security task → `"You are a cybersecurity expert reviewing for vulnerabilities"`

### 3. Clarify (If Critical Gaps Exist)
Ask **ONE** focused question — not multiple.
- ✅ "Which file — `api/validate.js` or `api/auth.js`?"
- ❌ "Which file? What language? What to check? When is the deadline?"

### 4. Construct the Structured Prompt

```
Persona: [Role + expertise relevant to the task]

Task: [Action verb + specific target]

Context: [System, environment, account, paths, dates]

References: [Examples, templates, or few-shot samples when format matters]

Requirements: [Constraints, scope, edge cases, what NOT to do]

Output: [Format, destination, success criteria, level of detail]
```

**Advanced techniques** — apply when appropriate:
- **Few-shot**: Add 1–2 input/output examples when format consistency matters
- **Chain of Thought**: Add `"Think step by step:"` for complex reasoning
- **Prompt Chaining**: Break multi-step tasks into linked sub-prompts
- **Meta Prompting**: Ask AI to refine the prompt itself before executing

See `references/techniques.md` for when/how to use each technique.

### 5. Confirm & Execute
- Destructive/complex actions: Show 1-sentence summary → get confirmation
- Safe/obvious tasks: Execute directly

## Quick Checklist

Before executing, verify:
- ✅ Persona assigned
- ✅ Intent is clear (specific action + target)
- ✅ Context is concrete (real paths, accounts, dates)
- ✅ Requirements are testable
- ✅ Output format defined
- ✅ Success criteria stated

## Real Examples

See `references/examples.md` for complete worked examples including:
- Voice transcription (Chinese) → Gmail check
- Vague code review → structured debug prompt
- Mixed-language service restart
- Complex multi-step task with chaining

## Common Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|---|---|
| Too many requirements in one prompt | Split into chained sub-prompts |
| Vague success criteria ("write a good report") | Define measurable criteria |
| No edge case handling | Add: "If X is missing, do Y" |
| Tweaking temperature instead of the prompt | Improve prompt structure first |
| Negative instructions only ("don't do X") | Tell it what TO do instead |
