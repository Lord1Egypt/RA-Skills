---
name: a11y
description: "Inclusive UI for real users—keyboard and focus, semantics for AT, contrast and motion, forms and errors. Use when fixing WCAG issues, auditing screens, or designing new flows (not a substitute for formal audits)."
---

# A11y

Help ship interfaces that work for **keyboard, screen readers, voice control, and low vision**—without treating accessibility as a bolt-on checkbox.

## What this skill is for

- **Concrete fixes**: focus traps, missing names/roles, heading order, label–control wiring, live regions, skip links.
- **Design trade-offs**: custom components vs native elements, motion reduction, contrast vs brand color.
- **Verification**: what to test in browser + AT, and what still needs human QA.

## What to skip or defer

- Legal **compliance certification** (VPAT, formal audits)—suggest specialists when the user needs signed-off conformance.
- **Visual design** taste without an accessibility angle—unless it affects contrast, touch targets, or readability.

## Workflow (adapt freely)

1. **Context** — Who uses what (keyboard-only, VoiceOver, NVDA, zoom)? Which WCAG **level** (A/AA) is the target?
2. **Surface problems** — Route critical paths; list failures (not vague “be more accessible”).
3. **Fix in order** — Blockers first (can’t complete task), then serious (wrong info), then polish.
4. **Prove it** — Tab order, focus visible, screen reader labels, automated checks where useful, manual pass on real flows.

## Anti-patterns to call out

- `div` buttons without keyboard support; **only** running Lighthouse and declaring done.
- Hiding focus rings “for aesthetics”; icon-only controls with no accessible name.
- Over-using `aria-*` instead of using the right **semantic** element first.

## Done when

- Critical paths are **keyboard-operable** and **named** for assistive tech; known gaps are documented with owners.
