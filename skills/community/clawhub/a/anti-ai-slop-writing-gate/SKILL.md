---
name: "anti-ai-slop-writing-gate"
description: "Detect or minimally edit formulaic AI-style prose while preserving the writer's voice."
author: "Mike Winkler"
---

# Anti AI Slop Writing Gate

Use this skill to edit a draft, identify checkable AI-slop patterns without rewriting it, or run a silent pre-send gate on substantive prose.

Do not use stylistic patterns to claim that AI wrote a text. The skill evaluates the writing, not its authorship.

## Modes

- **Edit:** Make the minimum effective edit. Preserve the writer's point, vocabulary, cadence, humor, uncertainty, edge, and useful roughness.
- **Detect:** Name the patterns present, quote the exact line, and give a short fix. Do not rewrite or assign an AI-likelihood score.
- **Pre-send:** Silently inspect a substantive reply before delivery and fix supported failures. Do not mention the audit unless asked.

Use pre-send mode for interpretations, advice, research synthesis, consequential explanations, and other developed replies. Skip it for acknowledgments, exact factual one-liners, raw tool output, or urgent safety instructions.

## Workflow

1. Read the full draft. Identify the audience, job, core point, intended action, and existing voice signals.
2. Load [references/patterns.md](references/patterns.md).
3. If the audience, format, or reader action is materially unclear, ask one focused question. Otherwise proceed.
4. In detect mode, report the evidence and stop.
5. In edit or pre-send mode:
   - remove filler, fake profundity, corporate abstraction, unsupported puffery, and repetitive cadence;
   - state the useful claim directly instead of staging it with throat-clearing or an unnecessary contrast;
   - preserve strong human sentences, specific facts, and useful roughness;
   - add concreteness, ownership, constraint, mechanism, or tradeoff only when supported by the draft;
   - never invent or silently strengthen claims, examples, numbers, quotations, sources, opinions, or emotion;
   - do not over-compress merely to eliminate a surface pattern.
6. Check the result against [references/evals.md](references/evals.md). Fix every failure before returning or sending it.

## Output

### Edit

- `Clean Version`
- `What Changed` — short and specific
- `Remaining Risk` only when meaning, sourcing, or factual support still needs the writer

### Detect

For each finding:

- pattern name
- exact quoted line
- short fix

Offer to edit after the audit.

### Pre-send

Return only the corrected substantive reply.

## Standard

Passes when the result is clear, specific, natural aloud, and recognizably the writer's.

Fails when it merely swaps buzzwords, erases personality, invents support, turns the piece into generic professional prose, or lets a known pattern through because the skill was treated as passive guidance.
