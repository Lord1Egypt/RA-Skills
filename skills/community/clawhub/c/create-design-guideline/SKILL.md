---
name: create-design-guideline
description: Create, revise, audit, or implement reusable brand and product design guidelines with semantic tokens, themes, interaction states, and visual verification. Use when a user wants a visual system, brand guide, palette rules, or systematic design cleanup; do not use for a one-off cosmetic CSS change.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# Create Design Guideline

Create, audit, and implement a decision system that designers and engineers can apply to this product. Connect visual choices to its audience, content, and brand, and distinguish proposals from verified implementation.

## Choose the requested outcome

- **Create or revise a guideline:** establish the brief and visual thesis, then use [references/deliverable-template.md](references/deliverable-template.md).
- **Audit an existing system:** preserve established choices and use [references/audit-and-qa.md](references/audit-and-qa.md) to report evidence and proposed corrections.
- **Implement an authorized system:** keep the canonical guideline and tokens together, migrate representative components, and follow the same QA reference.
- For color, palette, theme, or token decisions, read [references/research-and-color.md](references/research-and-color.md).
- For agent-built interfaces, component registries, or mobile composition, read [references/agent-design-workflow.md](references/agent-design-workflow.md).

Use only the references needed for the task. A guideline or audit request does not by itself authorize a product redesign or deployment. Existing user authorization remains valid; ask only about an unresolved choice that materially changes the authorized direction.

When the product explicitly chooses PIP or already consumes `@whitekiwi/ui` or
`@whitekiwi/tokens`, use the [PIP workflow](https://github.com/WhiteKiwi/skills/tree/main/skills/kiwi-design-system)
for integration and shared improvements. Load the installed `kiwi-design-system`
skill when available, otherwise read that source. Keep this skill for product
brand/guideline decisions; a PIP reference does not authorize changing other brands.

## Establish the brief and evidence

Inspect existing screens, code, tokens, brand assets, content, and repository instructions. Record the audience, desired impression, constraints, supported surfaces and themes, languages, and requested deliverable. Preserve explicit brand decisions and document assumptions when context is incomplete.

Distinguish the origin and evidence for each decision:

- `inherited`: established by the product or brand
- `observed`: present in inspected screens, code, or assets
- `proposed`: a new or revised choice
- `verified`: measured or visually checked, with the checked surface and state

Track artifact status separately as `candidate`, `approved`, or `implemented`. Approval follows the project's decision authority; a passing measurement does not grant approval, and an approved guideline is not necessarily deployed.

Research current authoritative sources when references, trends, or evidence are requested or needed to resolve an uncertain claim. Record `source → observed method → project decision`. Use standards for requirements, official systems for methods, and portfolios or galleries for composition. A reference's inclusion does not approve its adoption or license its assets.

## Define the visual language

Write a concise brand thesis and a few operating principles that resolve recurring choices. Decide only the dimensions the product needs:

- layout, alignment, spacing, density, and responsive composition
- typography roles, family, weight, size, line height, measure, and wrapping
- color roles, supported themes, and interactive states
- radius, borders, elevation, blur, texture, and gradients
- imagery, diagrams, screenshots, and evidence treatment
- motion and reduced-motion behavior
- voice and labeling when they affect the interface

Explain why each rule serves the product. Do not turn one site's aesthetic or a passing preference into a universal constraint. When an agent-facing implementation contract is in scope, maintain the repository's existing design contract, or create `DESIGN.md` if no canonical equivalent exists. Keep detailed rationale in the canonical guideline. A documentation-only request does not imply repository edits.

## Design color as role contracts

Define jobs before values: canvas, raised surfaces, text hierarchy, boundaries, interactive content, focus, brand fields and their foregrounds, and semantic status. Build primitive scales only for jobs that exist. Separate bright brand fields from accessible text and focus colors when one value cannot do every job. Brand identity and success, warning, error, or information remain distinct roles.

For new or revised palettes, author relationships in OKLCH or another suitable perceptual space and record sRGB fallbacks. Preserve an established palette or token format unless the requested change requires revising it. Map roles independently for supported themes. Define rest, hover, active/selected, focus-visible, and disabled states on the backgrounds where each component appears.

Approve foreground/background pairs using the requirements and exceptions in the color reference. A contrast result checks that pair, not the interface's complete accessibility. Composite translucent colors against their actual backgrounds before measuring them.

For opaque sRGB hex values, use the bundled Node.js helper from this skill's directory:

```sh
# Measure and classify; low contrast alone does not make report mode fail.
node scripts/contrast-check.mjs '#171717:#C6FF4A'

# Fail the command if any pair misses the chosen role's threshold.
node scripts/contrast-check.mjs --min 4.5 --json '#171717:#C6FF4A'
```

`--min` accepts a contrast threshold from 1 through 21. Choose it for the actual use: ordinary text, large text, or essential non-text information. Exit codes are `0` for a successful report or passing gate, `1` for a missed threshold, and `2` for invalid input. The helper accepts `#RGB` and `#RRGGBB`; it does not parse CSS tokens, alpha, OKLCH, or P3. Use an equivalent verified measurement if Node.js is unavailable and report that limitation.

## Implement and verify within scope

When code is requested, use primitive values, semantic roles, and component exceptions only where semantic roles are insufficient. Components consume semantic roles; document intentional fixed-theme specimens and exceptions instead of replacing every literal mechanically.

Update the canonical guideline and core tokens together. Migrate representative components before broad adoption, preserve existing functionality, and keep changes reversible. Check rendered screens in the supported themes, viewports, states, languages, and export surfaces using the QA reference. Run build and static checks in proportion to the change.

For documentation-only work, deliver the canonical artifact and adoption plan. For audits, deliver findings with evidence and impact. For implementation, report what changed, what was checked, and remaining choices; keep artifact status consistent with the observed result.
