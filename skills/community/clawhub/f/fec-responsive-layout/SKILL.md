---
name: fec-responsive-layout
description: Use when designing, implementing, or reviewing responsive frontend layouts, mobile-first breakpoints, container queries, fluid grids, data-dense tables, touch targets, safe areas, orientation changes, viewport overflow, or cross-device UI behavior; Chinese triggers include responsive layouts, mobile-side adaptation, breakpoints, container queries, horizontal and vertical screens, touch targets.
---

# Responsive layout

Suitable for front-end tasks that require pages, tool interfaces, tables, dashboards or components to work stably on multiple devices. Load [references/responsive-layout-patterns.md](references/responsive-layout-patterns.md) when layout patterns and checklists are required.

## Purpose

Design responsive layouts in a content-first, mobile-first, and container-aware manner to avoid relying solely on fixed breakpoints to fix overflow.

## Procedure

1. Clarify the priority of information: On small screens, core tasks, key operations and feedback are retained first; secondary information is folded, postponed or moved to the detail layer.
2. Choose a layout strategy: use mobile-first breakpoints for simple pages; give priority to container query for nested components, card grids and sidebars.
3. Design flow size: use `minmax()`, `clamp()`, `aspect-ratio`, `max-width`, `min-width: 0` and stable grid track to control scaling.
4. Handle data-intensive interfaces: tables, lists, boards, and editors need to explicitly support horizontal scrolling, column prioritization, frozen columns, or mobile summary views.
5. Ensure touch and keyboard: touch targets, focus paths, hover substitutions, virtual keyboards, safe areas, and horizontal and vertical screen switching should all be reviewed.
6. Correlate performance and resources: The mobile terminal reduces first-screen large images, heavy charts, synchronized animations and unnecessary column rendering.
7. Verify between breakpoints: check 375px, 768px, 1024px, 1440px, and whether the intermediate value of the breakpoint overflows, blocks, or jumps.

## Constraints

- Don’t treat the desktop version downsized as a mobile design.
- Don’t make key features rely solely on hover or widescreen sidebars.
- Do not use fixed height to cover content changes; use stable constraints and scrollable areas when fixed format is required.
- Do not use viewport font scaling instead of real typography hierarchy.
- Do not make mobile horizontal overflow the default solution; only explicit scenes such as data tables, canvases or editors can partially scroll.

## Expected Output

Outputs responsive information prioritization, breakpoint or container strategies, key component layout patterns, touch/keyboard requirements, data-intensive area handling options, and validation results. After completion, the page will not overflow, not be blocked, and is operable under common viewports and input methods.
