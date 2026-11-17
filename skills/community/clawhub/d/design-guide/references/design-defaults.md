# Design Defaults

Use these defaults when no project or local preference file overrides them.

## Process Defaults

- Match design depth to uncertainty and reversal cost.
- Use a concise brief and layout/state outline for established products.
- Produce a reviewable artifact and obtain confirmation for exploratory, workflow-changing, or brand-defining work.
- Automatically open local HTML when the agent and user share a desktop; otherwise use a host-accessible link or attached screenshots, never an agent-local loopback URL.
- Once an artifact is presented for approval, pause until the user approves, chooses, or requests changes.
- Use the lowest-cost artifact that resolves the open question; do not create polished mockups by habit.

## Product Defaults

- Build the actual usable screen first for apps, dashboards, editors, and tools.
- Prefer calm density for repeated work: clear hierarchy, compact controls, predictable navigation.
- Use representative domain content. Avoid lorem ipsum unless the user explicitly asks for placeholders.
- Preserve existing product conventions before introducing a new visual language.

## Visual Defaults

- Use one neutral base and one primary accent unless the brand requires more.
- Avoid generic AI-purple/blue gradients as the default.
- Avoid decorative nested cards, oversized hero sections, meaningless glow, and card grids that do not map to real information.
- Keep radius strategy consistent: choose sharp, small, medium, or pill by role and follow it.
- Use real images/assets for product, brand, venue, object, or portfolio work when available.

## Interaction Defaults

- Implement hover, focus, disabled, loading, empty, error, and long-text states where relevant.
- Use icons from the existing icon family. Do not hand-roll SVG icons for common glyphs.
- Use CSS Grid for stable page structure when flex width math would be fragile.
- Keep fixed controls stable across breakpoints.

## Responsive Defaults

- Audit mobile widths for overflow and clipped controls.
- Do not scale font size with viewport width.
- Use stable dimensions for boards, tiles, toolbars, counters, and fixed-format controls.
- Avoid `h-screen` for mobile full-height layouts; prefer dynamic viewport units when supported by the stack.

## Verification Defaults

- Run the existing build/typecheck/lint commands when relevant and affordable.
- Capture desktop, tablet, and mobile screenshots for substantial visual changes.
- Revise before delivery if screenshots reveal overlap, blank regions, illegible contrast, or broken hierarchy.
