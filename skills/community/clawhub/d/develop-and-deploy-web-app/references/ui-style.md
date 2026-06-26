# UI Style Guide

Use this guide to shape the frontend visual language.

Source basis: the public `huashu-design` repository README and its documented web-oriented principles. Reuse the design thinking, not the original assets, logos, or branded demo content.

## Core Direction

Aim for a polished editorial-product feel rather than a generic SaaS dashboard.

The target characteristics are:

- strong visual hierarchy
- magazine-like typography
- deliberate layout rhythm
- restrained but high-contrast color use
- real content blocks instead of placeholder chrome
- interfaces that feel authored, not template-generated

## Positive Rules

- Prefer a clear hero section with asymmetry or intentional negative space.
- Prefer CSS Grid over repetitive card stacks when the content benefits from structure.
- Use expressive display typography for major headings and a clean sans-serif for UI text.
- Use 1 or 2 accent colors with a mostly neutral base.
- Use subtle tonal surfaces, borders, and depth instead of heavy shadows everywhere.
- Use real section purposes: summary, list, detail, activity, status, filters, or form.
- Use `text-wrap: pretty` where supported for large headings and dense copy.
- Keep animation meaningful and sparse: entrance sequencing, panel reveal, number transitions, or view switching.
- Make the page responsive, but keep the desktop composition intentional rather than collapsing immediately into uniform stacked cards.

## Negative Rules

- Avoid purple-gradient-on-white default aesthetics.
- Avoid emoji-first UI decoration.
- Avoid oversized rounded rectangles used everywhere without hierarchy.
- Avoid generic left-border highlight cards repeated across the full page.
- Avoid fake-illustration placeholders when the layout can be solved with typography and composition.
- Avoid relying on Inter as the only visual voice for display text.
- Avoid the "AI slop" pattern of equal cards, shallow hierarchy, and decorative gradients with no content logic.

## Composition Patterns

For a simple CRUD app, prefer one of these structures:

1. Editorial workspace
   - large heading and short framing copy
   - primary creation panel
   - structured content board with list and detail zones

2. Product operations board
   - compact top summary
   - central high-density list
   - side panel for filters, state, or quick edits

3. Narrative utility app
   - strong opening headline
   - one emphasized core action
   - supporting list or timeline beneath

## Typography Guidance

- Pair a characterful serif or display face for large titles with a practical sans-serif for controls and body text.
- Tighten headline line-height and keep body copy calmer.
- Let typography carry part of the visual brand so the interface does not depend on gradients or illustrations.

## Color Guidance

- Prefer neutrals with one warm or vivid accent.
- If using modern CSS color functions such as `oklch`, keep contrast and browser support in mind.
- Reserve the accent color for calls to action, selected states, charts, or key metrics.

## Component Guidance

- Buttons should feel intentional and high-contrast.
- Inputs should be clean and quiet.
- Tables or lists should use spacing, typography, and alignment before adding decoration.
- Empty states should still feel designed, with framing copy and one next action.

## Practical Translation For React Apps

When implementing the frontend:

- Define CSS variables for color, spacing, radius, and typography.
- Centralize the page shell and section rhythm in one main stylesheet.
- Keep component count low; prefer a few strong primitives over many weak variants.
- If the feature set is simple, spend the design energy on hierarchy and layout, not on adding extra widgets.

## Verification Checklist

Before delivery, confirm:

1. The page does not look like a stock Vite starter.
2. The typography has a visible point of view.
3. The layout has at least one intentional composition decision beyond stacked cards.
4. The primary action is obvious within 3 seconds.
5. The mobile layout still feels designed rather than merely compressed.
