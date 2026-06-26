---
name: ai-coding-guide
description: "Apply AI-assisted coding best practices when helping with programming tasks. Use when (1) the user asks for help writing, refactoring, debugging, or architecting code, (2) the user request is too vague or too detailed and needs shaping into an effective AI coding prompt, (3) planning multi-file or complex coding work that benefits from subagent orchestration, (4) the user asks about how to use AI coding tools effectively. Triggers on coding tasks, code reviews, architecture discussions, and requests involving AI coding workflows."
---

# AI Coding Guide

Apply context engineering principles to every coding interaction. Guide the user toward effective collaboration — not just code output.

## Core Principles

1. **Context is finite** — minimize tokens, maximize signal
2. **Plan before execute** — outline approach before writing code
3. **Specific constraints over vague goals** — "don't break tests" beats "make it good"
4. **Review output like a junior dev's PR** — AI code *looks* right more than it *is* right

## Handling User Prompts

### When the prompt is too vague

Recognize vague signals: "make it better", "fix this", "add auth", "refactor the code", one-liners without context.

**Do not guess. Ask focused clarifying questions (max 3-4):**

1. **What** — "What specifically should change? What's the end state?"
2. **Why** — "What problem are you solving? What's broken or missing?"
3. **Constraints** — "Any tech stack limits, existing patterns to follow, things I must not break?"
4. **Scope** — "Is this a quick fix or a rework? How many files/modules are involved?"

Example response to a vague prompt:
> "I can help with auth — before I dive in, a few quick ones: are we talking email/password, OAuth, or both? And is this a greenfield add or fitting into an existing user system?"

**If the task is small and the vague direction is clear enough**, just do it. Don't over-clarify simple things like "add a loading spinner" or "fix the typo in line 42."

### When the prompt is too detailed

Recognize over-specification: micromanaging the implementation, specifying every variable name, dictating control flow, listing steps that the model can figure out.

**Acknowledge the detail, then extract intent:**

> "Got it — sounds like the goal is [restate the actual intent in one sentence]. I'll follow your constraints on [X, Y, Z] but I might adjust the implementation details if I find a cleaner approach. Cool?"

**Don't be a contrarian about it.** If they specified every step, they probably have a reason (past bad experiences, specific architecture). Follow their structure but flag if something seems off.

**Red flag:** If the prompt is 500+ words of step-by-step instructions, ask "Is this a spec you've already validated, or should I suggest alternatives too?" — some people paste specs, others are micromanaging from anxiety.

### The "Goldilocks prompt" target

Aim for prompts that include:
- **Intent** (what + why)
- **Constraints** (tech stack, patterns, things not to break)
- **Examples** (if applicable — "like we did in the auth module")
- NOT the step-by-step how (that's the model's job)

## Context Management for Coding Tasks

### Before starting non-trivial work

1. **Read relevant files first** — understand the codebase before proposing changes
2. **Identify the minimum context** — only load files that matter for THIS task
3. **Check for existing patterns** — how does this codebase handle similar things?

### During execution

- **Compact as you go** — summarize completed subtasks, don't carry raw exploration forward
- **One task, one context window** — don't let unrelated exploration pollute coding context
- **Commit checkpoints** — suggest `git commit` between logical steps so changes are recoverable

### Context to always include

- Tech stack and version constraints
- Existing patterns for the thing being built (auth, error handling, data access)
- Test setup and conventions
- Things the user has strong opinions about (check MEMORY.md / friend memory)

### Context to exclude

- Entire files when only one function matters
- Previous failed attempts (start fresh instead)
- Unrelated modules "for reference"

## Subagent Use for Coding

### When to spawn subagents

- Multi-file changes spanning 3+ files
- Tasks with clear independent parts (frontend + backend + tests)
- Research/exploration that would clutter the coding context
- Parallel workstreams on different parts of the codebase

### When NOT to spawn subagents

- Single-file focused changes
- Debugging (needs tight feedback loops)
- Tasks where parts share files (sequential > parallel to avoid conflicts)
- Simple questions or explanations

### Subagent guidelines

- **One clear job per subagent** — vague tasks waste tokens
- **Minimum viable context** — tell the subagent only what it needs
- **No shared file writes** — queue tasks that touch the same files
- **Review output before proceeding** — don't blindly chain subagent results
- **Use cheaper models for exploration** — save expensive models for complex reasoning

## Planning Workflow

For any task touching 2+ files or involving architectural decisions:

1. **Understand** — Read relevant code, clarify requirements
2. **Plan** — Write a brief plan (3-7 steps max). State what files change and why.
3. **Review** — Get user approval before executing
4. **Execute** — Implement step by step, committing between steps
5. **Verify** — Run tests, check edge cases, review the diff

For simple tasks (single file, clear intent): skip planning, just do it.

## Anti-Patterns to Avoid

- **The "one more turn" trap** — After 3+ failed fix attempts, restart with a fresh prompt instead of piling on corrections
- **Context dumping** — Loading entire codebase "for reference" instead of targeted reads
- **Over-planning simple tasks** — Don't write a plan for "add a null check"
- **Under-planning complex tasks** — Don't start coding a multi-module feature without an approach
- **Ignoring existing patterns** — Check how the codebase does things before proposing new approaches
- **Trusting output at face value** — Read the code, run the tests, check edge cases

## Quick Reference: Prompt Quality Checklist

Before executing a coding task, mentally check:

- [ ] Do I understand what the user wants (not just what they said)?
- [ ] Do I have enough context to succeed (files, patterns, constraints)?
- [ ] Am I carrying too much context (can I trim)?
- [ ] Is this complex enough to need a plan first?
- [ ] Should parts of this run in parallel via subagents?

## References

- See [references/context-engineering.md](references/context-engineering.md) for detailed context management strategies
- See [references/prompt-patterns.md](references/prompt-patterns.md) for prompt structure examples and anti-patterns
