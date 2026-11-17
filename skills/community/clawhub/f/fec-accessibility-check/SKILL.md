---
name: fec-accessibility-check
description: Use when reviewing or improving frontend accessibility, semantic structure, keyboard support, focus management, ARIA labels, screen reader behavior, WCAG 2.2 issues, touch accessibility, or assistive-technology regressions; Chinese triggers include accessibility, accessibility, a11y, WCAG, screen reader.
---

# Accessibility Implementation Specification (WCAG 2.2 AA)

## Purpose

Ensure the front-end UI is accessible to users with disabilities, meets the core requirements of WCAG 2.2 AA, and is stable for keyboard, screen reader, touch, and zoom users.

## Procedure

1. Check the semantic structure: landmark, title level, form label, button/link accessible name, table semantics and image alt.
2. Check the keyboard path: Tab order, Enter/Space/Esc behavior, focus visible, focus restored after closing.
3. Check the ARIA status of complex components: dialog boxes, menus, tabs, trees, drawers, tables, and custom controls.
4. Check dynamic status: loading, empty, error, toast and asynchronous updates need to be perceived by screen readers.
5. Check visual and touch readability: text/background contrast, focus ring, zoom to 200%, reduced animation preference, touch target size, and mobile virtual keyboard behavior.
6. Use the real keyboard path to review the key process, and if necessary, add a screen reader or browser accessibility tree observation; see [references/screen-reader-testing.md](references/screen-reader-testing.md) for the screen reader process.
7. Review the new high-frequency risks in WCAG 2.2: the visible focus is not blocked, the drag operation has alternative paths, the target size is too small, and the help entrance and authentication process do not rely on memory burden.
8. Output the classification report; see [references/report-template.md](references/report-template.md) for the report format.

## Detailed reference

When writing an accessibility review report, load [references/report-template.md](references/report-template.md). Load [references/screen-reader-testing.md](references/screen-reader-testing.md) when you need to verify screen reader announcements, focus pronunciations, and dynamic areas.

## Constraints

- Prefer semantic HTML over ARIA.
- `role` should not override native semantics.
- Interactive elements must be keyboard accessible.
- Form errors must be associated with fields.
- Color contrast risks need to be pointed out for specific text/background combinations.
- Don't use ARIA to make up for problems that can be solved with native HTML.
- Do not treat automatic browser accessibility trees as final; critical paths need to be verified with the keyboard and at least one assistive technology or equivalent check.

## Expected Output

Interactive elements are keyboard accessible, semantics and ARIA are used correctly, and focus management is stable; accessibility check reports are saved as `reports/accessibility-review-YYYY-MM-DD-HHmmss.md`.
