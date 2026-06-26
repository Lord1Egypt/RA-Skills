---
name: design-systems
description: Deep design systems workflow—tokens, components, accessibility, documentation, governance, and adoption. Use when scaling UI consistency across teams or evolving a component library (Figma + code parity).
---

# Design Systems (Deep Workflow)

A design system is **shared UI infrastructure**: tokens, components, patterns, and governance so products feel cohesive without freezing innovation.

## When to Offer This Workflow

**Trigger conditions:**

- Multiple apps diverging visually; mounting accessibility debt
- Launching or rebooting a component library; token refresh
- Figma and production code drifting apart

**Initial offer:**

Use **six stages**: (1) strategy & principles, (2) design tokens, (3) components & API, (4) accessibility & content, (5) docs & tooling, (6) governance & adoption). Confirm framework (React/Vue/Svelte) and design tooling.

---

## Stage 1: Strategy & Principles

**Goal:** Why the system exists (speed, a11y, brand); explicit non-goals (not every pixel must be centralized).

**Exit condition:** One-page principles: density, tone, motion philosophy.

---

## Stage 2: Design Tokens

**Goal:** Semantic color, type, space, radius, motion—names like `surface.default` instead of raw hex everywhere.

### Practices

- Plan light/dark and density themes early

---

## Stage 3: Components & API

**Goal:** Composable primitives vs bloated “kitchen sink” widgets; stable props API with semver discipline.

### Practices

- Prefer composition / slots over prop explosion

---

## Stage 4: Accessibility & Content

**Goal:** WCAG baseline per component: focus rings, labels, error patterns, live regions where needed.

---

## Stage 5: Docs & Tooling

**Goal:** Storybook or equivalent; usage guidelines; code snippets; do/don’t examples.

---

## Stage 6: Governance & Adoption

**Goal:** Contribution guide; deprecation policy; champions or office hours per product line.

---

## Final Review Checklist

- [ ] Strategy and principles agreed
- [ ] Token layer semantic and themeable
- [ ] Component APIs stable and composable
- [ ] Accessibility baseline per component
- [ ] Documentation and live examples
- [ ] Contribution and deprecation governance

## Tips for Effective Guidance

- Figma ↔ code parity needs owners and a sync cadence.
- Do not ship a component without keyboard and screen-reader checks.

## Handling Deviations

- Small teams: start with tokens + a few primitives—defer full catalog.
