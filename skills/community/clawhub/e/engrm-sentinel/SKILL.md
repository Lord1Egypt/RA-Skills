---
name: engrm-sentinel
description: Use Engrm packs and Sentinel context to surface likely mistakes, risky patterns, and lessons that would have prevented them.
---

# Engrm Sentinel

Use this skill when code is entering a risky area and the goal is to prevent
mistakes, not just remember past work.

## Before you start

Use Engrm only if it is already connected and available in the current
environment.

If Engrm is not available, say that Engrm Sentinel context is not connected on
this machine and continue without inventing setup steps or shell commands.

## Command guardrails

Do not invent Engrm shell commands like `engrm search`, `engrm save`, or
`engrm timeline`.

Treat Sentinel guidance as Engrm workflow knowledge, not as an excuse to guess
at extra CLI syntax.

## What this skill is for

- Surface risky patterns before they turn into bugs or security issues.
- Reuse pack knowledge and standards during active coding work.
- Explain what is going wrong, not just that something looks unusual.
- Keep prevention practical and grounded in project context.

## When to use it

Use this skill when the task involves:

- authentication or secrets
- input handling or API boundaries
- security-sensitive data
- major refactors
- deployment or config changes
- code that has caused repeated issues before

## Sentinel mindset

Ask:

- What could go wrong here?
- Which pack lessons are relevant?
- Is this repeating a known mistake?
- Is the implementation drifting into a risky shortcut?
- Would a future session benefit from a new standard or lesson here?

## Good outputs

Helpful Sentinel guidance should:

- name the likely mistake clearly
- explain why it matters
- connect it to a reusable lesson or pack
- suggest the safer path

Avoid:

- generic fearmongering
- abstract policy language without code relevance
- blocking everything just because it feels risky

## Pack-aware review

Remember:

- packs are available on free plans too
- the point is not to hide lessons behind paid access
- the real value is turning those lessons into smarter review, stronger
  prevention, and better follow-through

## What success looks like

The agent catches meaningful mistakes early, explains them well, and leaves
behind a sharper memory or standard for the next session.
