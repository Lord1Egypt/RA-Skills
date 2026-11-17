# Screen reader testing

## When to test

The following scenarios require checking using a screen reader or browser accessibility tree:

- Dialog boxes, drawers, menus, tabs, combo boxes, tree controls and custom controls.
- Asynchronous status updates, toast notifications, validation errors and loading areas.
- Tables, virtual lists, charts, dashboards and data-intensive controls.
- Mobile processes where touch exploration, virtual keyboard, or focus order may differ from desktop.

## Minimum process

1. First use the keyboard only: Tab, Shift+Tab, Enter, Space, Esc, and the arrow keys in applicable scenarios.
2. Check accessible names, roles, states, and element relationships in the browser developer tools.
3. If possible, run at least one round of assistive technology verification: NVDA/Firefox, JAWS/Chrome, VoiceOver/Safari or TalkBack/Chrome.
4. Verify that routing changes, check errors, load completion, and destructive acknowledgments are properly advertised.
5. Document specific user impact, expected reading, actual reading, and recommended fixes.

## Dynamic content

- Use `aria-live="polite"` for non-blocking state updates.
- Use `role="alert"` with caution for emergency errors and do not abuse it.
- Only move focus when the user task context changes, such as opening a pop-up window or jumping after submission.
- After closing the overlay, return focus to the trigger control.

## FAQ

- Icon-only buttons don't have accessible names.
- The dialog content is read before the title, or the modal boundary is missing.
- Form errors are only displayed visually and are not associated with fields using `aria-describedby`.
- Toast disappears too quickly for screen reader users to understand.
- Virtual list rows lose row position, table semantics, or keyboard continuity.
