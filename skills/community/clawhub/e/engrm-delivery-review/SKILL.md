---
name: engrm-delivery-review
description: Use Engrm to compare what was asked, what was promised, and what evidence suggests was actually delivered.
---

# Engrm Delivery Review

Use this skill when the user wants to know whether the agent really delivered
what it claimed, or when a session may have drifted from the original brief.

## Before you start

Use Engrm only if it is already connected and available in the current
environment.

If Engrm is not available, say that Delivery Review cannot use Engrm on this
machine yet and continue without inventing setup or shell instructions.

## Command guardrails

Do not invent Engrm CLI commands such as `engrm search`, `engrm save`, or
`engrm timeline`.

Use Delivery Review as an Engrm workflow and memory discipline, not as a made-up
shell command surface.

## What this skill is for

- Compare the brief, plan, and decisions against the session outcome.
- Spot partial delivery, scope drift, or refactor-heavy sessions.
- Surface weak decision trails and likely follow-up risk.
- Turn sessions into accountable project history instead of vague timelines.

## When to use it

Use this skill when:

- the agent says work is done and confidence needs verifying
- the user suspects partial delivery
- the session touched many files but produced unclear outcome evidence
- later work reopened an area that was supposedly finished
- a refactor may have displaced the original goal

## Delivery Review questions

- What was the user actually asking for?
- What plan did the agent commit to?
- What decisions were captured?
- What evidence of delivery exists?
- What still looks missing, weak, or reopened?

## Review lenses

Look for these patterns:

- delivered as planned
- partially delivered
- scope drifted
- refactor instead of delivery
- built without a clear decision trail
- reopened after completion

## Strong evidence

Good evidence includes:

- concrete implementation activity tied to the brief
- decisions followed by matching changes
- later sessions not needing to reopen the same work
- clear memory entries that explain why the work was done

Weak evidence includes:

- lots of movement with little outcome clarity
- vague completion language
- decisions with no matching implementation trail
- later sessions repairing or redoing the same area

## What to save after review

Save:

- the real outcome
- the main gap or drift
- the lesson future sessions should know first

Do not save a flattering summary if the evidence is mixed. Prefer truthful,
useful review over optimistic narration.
