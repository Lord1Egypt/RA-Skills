# Audit and visual QA

Use this for an audit or implementation pass. Inspect the system in context, preserve intentional choices, and make the evidence sufficient for another person to assess the finding.

## Audit order

1. **Content and attention:** identify the primary message and tasks; inspect whether decoration competes with them.
2. **Token inventory:** locate primitives, semantic aliases, literals, alpha mixes, and fixed-theme specimens.
3. **Pairs and states:** measure actual foreground/background combinations, including hover, focus, and composited alpha.
4. **Theme hierarchy:** compare canvas, raised surfaces, reading text, boundaries, interactions, and inverse scenes in supported themes.
5. **Typography:** inspect role hierarchy, weight count, measure, line height, zoom, wrapping, and truncation.
6. **Composition and material:** inspect alignment, whitespace, repeated cards, accent area, radius, shadow, glass, and gradients.
7. **Motion and responsiveness:** inspect reading access, state feedback, reduced motion, narrow layouts, and essential information or actions.

Choose relevant checks rather than treating this order as a mandatory exhaustive audit for every edit.

## Findings

For each actionable finding, provide:

| Field | Contents |
| --- | --- |
| Location | screen or component, theme, viewport, state |
| Observation | what is present in the inspected artifact |
| Evidence | screenshot, code/token location, measurement, or reproduction |
| Impact | affected task, reader, or stated design requirement |
| Proposal | smallest coherent correction and its tradeoff |
| Verification | checked result or remaining validation |

Keep facts, interpretation, and proposals distinguishable. “The label/background measures 1.18:1” is measured evidence; “the neutral reads green” is a visual interpretation. A user preference can guide a decisive choice without becoming an accessibility requirement.

## Implementation

Keep the guideline and core tokens in the same change. Start with representative components, then migrate broader use. Preserve fixed-theme examples, branded artwork, and documented exceptions. An audit does not imply permission to replace the product's style; implementation follows the user's authorized scope.

When an unresolved design choice needs review, show a contained specimen or representative screen. Do not demand another approval for a choice already covered by existing authorization.

## Visual verification

Inspect representative pages, not only the guideline page:

- supported light, dark, or fixed themes
- the narrowest supported viewport and a typical wide viewport; for web products, check reflow at 320 CSS px where applicable
- existing rest, hover, active/selected, keyboard focus, disabled, error, and success states
- longest realistic heading, paragraph, URL, and translated or Korean/non-Latin text
- keyboard use, zoom, overflow, focus obscuration, and target behavior
- reduced motion and access to content without waiting for an animation
- print, PDF, social preview, or other exports when present

Check hierarchy, accent coverage, unintended hue casts, local contrast, and whether materials or effects obscure content. Consult the applicable criteria, including [WCAG Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), rather than converting every example viewport into a universal support requirement.

Run build, static checks, and relevant interaction tests in proportion to risk. If rendering or measurement is unavailable, state exactly what remains unverified. Finish with artifact status, changes or findings, verification, and unresolved decisions.
