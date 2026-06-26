---
name: autoreason-lite
description: Apply a bounded multi-candidate self-refinement loop (A/B/AB + judges + do-nothing option) to improve drafts, plans, and analyses while preventing scope creep. Use when user asks to improve writing/strategy/code explanations iteratively with quality control.
---

# Autoreason Lite

Use this skill when a user asks to "improve this," "refine this," or "make this better" and quality matters more than one-shot speed.

## What this does

A bounded refinement tournament:

1. **A (incumbent):** current draft unchanged
2. **B (adversarial revision):** deliberately different attempt
3. **AB (synthesis):** merge best parts of A and B
4. **Judging pass:** pick winner with explicit rubric
5. **Convergence rule:** stop early if A keeps winning (no-change is valid)

This reduces over-editing and drift.

## Default operating profile

- Max rounds: **3**
- Judges: **3 independent judge personas**
- Aggregation: **Borda-like ranking** (1st=2 pts, 2nd=1 pt, 3rd=0)
- Convergence: stop if **A wins 2 rounds** (or winner unchanged 2 rounds)
- Length guardrail: output within **±15%** of requested length unless user asks otherwise
- Voice lock: preserve user's tone profile (technical / founder / viral) unless asked to shift

## When to use

Use for:
- Long-form writing
- Strategy memos
- Explanations/tutorial drafts
- Product copy
- Decision frameworks

Avoid for:
- Deterministic factual extraction
- Tiny edits user already specified exactly
- Time-critical one-liners unless user requests deep refinement

## Execution steps

1. Clarify success criteria (tone, audience, length, goal) if missing.
2. Generate candidate **B** from A:
   - Must change structure or argument order (not just wording).
   - Must preserve critical facts.
3. Generate candidate **AB**:
   - Keep strongest parts from A and B.
   - Remove redundancy.
4. Run 3 judges independently with rubric:
   - Accuracy / faithfulness
   - Clarity
   - Usefulness for user goal
   - Concision / scope control
5. Score candidates; choose winner.
6. Repeat up to max rounds with winner as new A.
7. Return final with short “what changed + why”.

## Judge prompt template

Use `references/judge-rubric.md`.

## Output format to user

- Final refined result
- 2-4 bullets: key improvements
- Optional: one-line note if loop stopped due to convergence (no meaningful gain)

## Quick presets

- **Technical:** precise wording, fewer claims, concrete mechanisms
- **Founder:** outcomes + positioning + credibility signal
- **Viral:** short lines, strong hooks, high readability, no fluff

## Safety + quality constraints

- Never invent facts to make prose sound better.
- Keep user intent stable unless explicitly asked to pivot.
- Prefer no-change over noisy edits.
- If confidence drops, surface uncertainty instead of bluffing.
