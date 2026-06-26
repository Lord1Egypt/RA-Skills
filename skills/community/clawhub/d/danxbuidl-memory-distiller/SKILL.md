---
name: memory-distiller
description: Distill repeated user preferences, successful patterns, and durable working rules into reusable memory notes or prompt-ready context blocks. Use when a user wants to capture habits, preserve preferences, summarize lessons from prior work, or convert raw conversation/task outcomes into structured memory.
---

# Memory Distiller

## Overview

Use this skill when the user wants to turn raw interaction history into stable,
reusable memory. The goal is not to summarize everything. The goal is to keep
only the parts that are durable enough to improve future work.

Read `references/output-format.md` when the user wants a structured output
template, a prompt-ready context block, or a reusable memory profile format.

Read `references/example-prompts.md` when the user needs prompt examples,
variation ideas, or help choosing the right invocation pattern.

## Quick Start

If the user does not specify a format, default to this flow:

1. extract candidate memories from the source material
2. keep only durable and evidence-backed items
3. rewrite them as future-facing rules
4. return:
   - stable preferences
   - working rules
   - anti-patterns
   - one short reusable context block

If the user already has a memory document, switch into review mode instead of
rebuilding everything from scratch.

## When To Use

Use this skill when the user asks to:

- capture recurring preferences or habits
- preserve successful working patterns
- record constraints, defaults, or anti-patterns
- turn task outcomes into future-facing rules
- clean up or refine an existing memory/profile document
- produce a compact context block for reuse in future prompts

Do not use this skill for:

- one-off conversational summaries
- temporary task state that will expire quickly
- guesses about user preferences that are not supported by evidence
- hidden or background memory injection into runtime code paths

## Output Selection

Choose the narrowest output that matches the user's goal:

- memory profile
  - use when the user wants a compact long-term preference document
- cleaned memory list
  - use when the user already has notes and wants to remove weak items
- prompt-ready context block
  - use when the user wants a short block to reuse in future prompts
- review and rewrite report
  - use when the user wants to know what should be kept, rewritten, or removed

Read `references/output-format.md` before producing any structured output.

## Core Rule

Only preserve information that looks durable.

Good candidates:

- stable preferences
- repeated defaults
- persistent constraints
- explicit dislikes
- reusable procedures
- recurring failure-avoidance rules

Weak candidates:

- one-off requests
- temporary deadlines
- transient debugging state
- personal guesses not explicitly supported by the source material

When a memory candidate is uncertain, mark it as tentative or exclude it.

## Evidence Threshold

Prefer memories that are supported by one of these:

- an explicit user statement
- a repeated pattern across multiple examples
- a successful workflow that clearly generalizes
- a durable constraint that is unlikely to change soon

Prefer to exclude items that are supported only by:

- one weak hint
- a single accidental success
- a temporary environment detail
- a guess about personality or intent

## Workflow

### 1. Gather source material

Start from the material the user provides or points to:

- conversation excerpts
- task outcomes
- prior memory notes
- preference documents
- review summaries

If the source material is large, first compress it into candidate signals rather
than copying everything forward.

### 2. Extract candidate memories

Look for statements that imply stable behavior, such as:

- "always"
- "prefer"
- "do not"
- "default to"
- "use X when Y"
- repeated successful patterns across multiple examples

Group candidates into a small set of categories:

- preferences
- defaults
- constraints
- anti-patterns
- reusable procedures

When possible, tag each candidate mentally as one of:

- confirmed
- tentative
- reject

### 3. Remove weak or noisy items

Drop any item that is:

- purely situational
- contradicted by newer evidence
- too vague to be useful
- likely to cause bad prompt injection if reused blindly

Prefer precision over recall. A small memory set with strong signal is better
than a large noisy list.

### 4. Rewrite into future-facing rules

Rewrite valid items as clear, reusable guidance.

Prefer forms like:

- "Prefer concise technical explanations."
- "Use JSON output when the user asks for machine-readable results."
- "Avoid storing one-off operational incidents as durable preferences."

Avoid forms like:

- "The user once asked..."
- "Yesterday they said..."
- "Maybe they prefer..."

### 5. Produce the requested output

Choose the narrowest useful output for the user:

- memory profile
- cleaned memory list
- prompt-ready context block
- review of existing memory quality

If the user does not specify a format, default to:

1. Stable preferences
2. Working rules
3. Anti-patterns
4. A short reusable context block

## Examples

### Example: conversation to profile

If the source says:

- "Please keep answers concise."
- "I prefer JSON when I ask for structured output."
- "Do not add long background explanations unless I ask."

The distilled result should look like:

- Prefer concise responses by default.
- Use JSON when the user explicitly asks for structured output.
- Avoid long background explanations unless requested.

### Example: task outcomes to rules

If repeated successful tasks show:

- good results when output is checklist-based
- repeated failures when assumptions are not surfaced

The distilled result should look like:

- Prefer checklist-style outputs for execution-heavy tasks.
- Surface assumptions explicitly before committing to a plan.

### Example: weak candidate to exclude

If the only evidence is:

- "Yesterday the user wanted a long poetic answer."

Do not convert that into a durable preference unless there is more support.

## Output Guidance

When producing memory content:

- keep wording concise
- keep claims evidence-based
- prefer durable rules over narrative summaries
- avoid hidden assumptions about the user
- separate "confirmed" from "tentative" when needed

If a prompt-ready context block is requested, keep it short enough that it can
realistically be reused without bloating future prompts.

## Safety And Quality

- Do not invent personal traits or preferences.
- Do not retain sensitive details unless the user clearly wants them preserved.
- Do not turn one failure into a permanent rule without evidence that it is recurring.
- When in doubt, exclude the item or mark it tentative.
- Prefer omission over noisy memory.
