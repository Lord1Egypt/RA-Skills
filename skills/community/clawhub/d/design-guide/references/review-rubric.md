# Frontend Review Rubric

Use this when auditing a frontend artifact before delivery or when the user asks whether the UI is good.

For existing product/page reviews, use this rubric together with `references/product-design-review.md`. When visual polish, redesign, or generic AI-looking UI is in scope, also use `references/anti-ai-design-tells.md`.

## Score

Score each category from 0 to 10. Anything below 8 needs revision unless the user asked for a rough prototype.

- Direction fit: the UI matches the stated product, audience, and reference anchors.
- Task flow: the primary workflow, information priority, states, and recovery paths support the user's job.
- Visual hierarchy: the eye path is obvious; primary actions and key data dominate.
- Craft: alignment, spacing, color count, typography, radius, shadow, and icon style are consistent.
- Usability: common states exist; workflows are efficient; controls are recognizable.
- Responsiveness: desktop, tablet, and mobile are usable without overlap or text clipping.
- Originality: avoids generic AI gradients, repeated equal cards, vague hero copy, and decorative filler.

## Mode Extensions

Add the relevant mode-specific checks from `references/product-design-review.md`:

- Product workbench: workflow speed, density, table/list operations, state coverage, decision safety, and data trust.
- Marketing page: message clarity, proof, trust, CTA path, copy quality, and conversion focus.
- Data dashboard: chart legibility, comparison model, freshness, filtering, uncertainty, and data states.
- Form flow: field order, validation, recovery, progress, autofill, and exit safety.
- Mobile/webview: thumb reach, keyboard viewport, fixed controls, safe areas, and intentional reflow.

For deeper evidence and acceptance criteria, load the matching file under `references/review-templates/`: `data-tables.md`, `dashboards.md`, `complex-forms.md`, `mobile-navigation.md`, or `high-risk-batch-actions.md`.

## Critical Issues

Fix these before delivery:

- Text overlaps, clips, or escapes its container.
- Mobile layout requires horizontal scrolling unless intentionally designed.
- Primary action is unclear.
- Contrast prevents comfortable reading.
- Dynamic content changes element sizes in a jarring way.
- Decorative layout makes an operational tool harder to use.
- Placeholder assets are presented as finished assets.
- The style drifts across sections.
- The implementation materially contradicts the approved design contract.

## Fast Visual Audit

Run this mental checklist against screenshots:

1. Squint test: can you identify the primary region and action in two seconds?
2. Grid test: do major edges align consistently?
3. Density test: does the amount of information match the usage context?
4. Palette test: is there one dominant neutral system and one accent?
5. Component test: do buttons, inputs, cards, tabs, and menus share one visual language?
6. Breakpoint test: does mobile look intentionally designed, not merely squeezed?
