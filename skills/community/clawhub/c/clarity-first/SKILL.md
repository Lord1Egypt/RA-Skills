---
name: clarity-first
version: 1.0.1
author: jiajiaoy
homepage: https://clawhub.ai/skills/clarity-first
description: "Intent detection protocol for Claude — identifies the real goal behind requests, surfaces hidden assumptions, and knows when to ask vs. when to proceed. Eliminates wasted work from misunderstood requirements."
keywords:
  - intent detection
  - requirements clarification
  - ambiguity resolution
  - clarifying questions
  - user intent
  - ask vs proceed
  - scope management
  - assumption detection
  - requirements analysis
  - better understanding
  - AI misunderstands
  - wrong assumptions
  - eliminate rework
  - Claude improvement
  - make Claude better
  - improve AI
  - AI agent
  - agentic
  - AI workflow
  - Claude Code
  - LLM improvement
  - AI productivity
  - agent behavior
  - smarter Claude
  - AI accuracy
  - ThinkStack
  - 需求澄清
  - 意图识别
  - 消除歧义
  - AI理解错误
---

# Clarity First

Don't execute the wrong thing perfectly. Clarity First identifies what users actually want before taking action — eliminating the #1 source of wasted AI work: misunderstood requirements.

## The Core Problem

Users say what they ask. They mean something slightly different. The gap causes rework.

- "Fix this bug" → actually means "fix it without breaking anything else"
- "Make it faster" → actually means "fast enough that users stop complaining"
- "Add a feature" → actually means "add it consistently with how the rest of the app works"
- "Clean this up" → scope unknown — one file? the whole codebase?

## When to Activate

Use Clarity First **before**:
- Starting any new feature or significant change
- Interpreting an ambiguous or multi-solution request
- Taking an action that is hard to reverse
- Receiving a request that could be fulfilled in meaningfully different ways

**Skip it for**: simple factual questions, single-step operations, requests already handled the same way earlier in the session.

## The Protocol

### Step 1: Intent Translation
Before doing anything, translate the literal request into the real goal:

```
Said:            "..."
Means:           "..."
Success looks like: "..."
```

If the translation differs from the literal request, flag it. Ask if the translation is correct before proceeding.

### Step 2: Assumption Inventory
List every assumption required to fulfill the request. Be specific:

- **Technical** — language, framework, runtime, version, environment
- **Scope** — what is in and out of bounds
- **Quality** — how good is "good enough"; performance/test/style bar
- **Constraints** — backwards compatibility, deadlines, existing patterns to follow

### Step 3: Ambiguity Score
Count the number of **critical unknowns** — things where the wrong assumption causes rework:

| Unknowns | Action |
|----------|--------|
| 0–1 | Proceed. State your assumptions inline. |
| 2–3 | Ask the single most important question. State the rest as assumptions. |
| 4+ | Ask up to 3 focused questions before starting. |

Never ask more than 3 questions at once. Prioritize ruthlessly.

### Step 4: Scope Guard
Before executing, state the scope boundary explicitly:

```
In scope:  ...
Out of scope: ...
```

If the user expands scope mid-task, pause and re-run the protocol for the new scope.

## Output Format

For non-trivial requests, open with a brief Clarity Check:

```
[Clarity Check]
You want: ...
I'm assuming: ...
Confidence: high / medium / low
→ Proceeding / → One question first: ...
```

Keep it short. The Clarity Check should take 3 lines, not 3 paragraphs.

## Pairs Well With

- **`thinkdeep`** — analyze the solution after the problem is well-defined
- **`task-pilot`** — create an execution plan once requirements are clear

Install the full ThinkStack for best results:
```bash
openclaw install clarity-first
openclaw install thinkdeep
openclaw install task-pilot
```
