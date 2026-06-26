---
name: eva-ui
description: Use this skill when creating, reviewing, or extending interfaces inspired by Evangelion monitor, tactical screen, and control-room aesthetics. It guides color selection, typography, pattern language, data density, motion, and component composition so outputs keep EVA's industrial red-orange instrument feel instead of drifting into generic sci-fi or SaaS dashboards.
version: 1.0.1
---

# EVA UI Skill

Current version: `1.0.1`

Use this skill for EVA-inspired UI design systems, frontend implementation, component generation, prompt authoring, or design review.

## Workflow

1. Start with `references/style-principles.md` to lock the visual direction.
2. Apply the system rules from `references/tokens.md`, `references/typography.md`, and `references/motion.md`.
3. Use `references/pattern-language.md` and `references/data-elements.md` to build the non-typographic visual grammar.
4. Build or review UI against `references/component-rules.md`.
5. Use `references/prompt-recipes.md` to generate new pages or components.
6. Reject outputs that match any failure mode in `references/anti-patterns.md`.

## Required Style Principles

- High information density
- Hard-edged framing
- Red-orange status-driven color system
- Technical condensed typography
- Instrument-style motion
- Pattern language built from stripes, ticks, brackets, meshes, and calibration motifs
- Borders, rails, labels, and measurement marks should do more visual work than spacing or soft shadows

## Reference Map

- `references/style-principles.md`
- `references/tokens.md`
- `references/typography.md`
- `references/motion.md`
- `references/pattern-language.md`
- `references/data-elements.md`
- `references/component-rules.md`
- `references/prompt-recipes.md`
- `references/anti-patterns.md`

## Assets

- `assets/example-lab/index.html`
- `assets/example-lab/styles.css`

Use the example lab as a starting point for prototypes, demos, or component extraction.

## Output Constraints

- Avoid soft SaaS cards, large radii, and friendly product-dashboard spacing.
- Avoid relying on typography alone; reinforce hierarchy with stripe bands, ticks, reticles, threshold bars, and rails.
- Treat red and orange as primary EVA command colors; use other hues only when they communicate a specific data mode.
- Prefer repeated structured modules over hero-card layouts.
- Decorative gradients are allowed only when they communicate field state, heat, scan, or energy behavior.
