# UI/UX pre-delivery inspection

## Serious

- Text contrast: at least 4.5:1 for main text and 3:1 for large fonts.
- Keyboard accessible: menus, pop-up windows, tabs, drawers and custom controls can all be operated by the keyboard.
- Focus visible: focus ring cannot be removed by global styles.
- Icon button: must have an accessible name.
- Touch targets: Primary interactions on mobile should be at least 44x44px; use 48px when space allows.

## High priority

- First screen: The tool-based interface directly displays the core workspace, without the need for marketing hero replacement functions.
- Above the fold: Marketing, portfolio, and brand pages display body, CTA, and next-screen cues within common small notebook heights.
- CTA: The button copy does not wrap on the desktop, the contrast is acceptable, and consistent labels are used for the same purpose.
- Navigation: Keep a single line on the desktop, and the main path can still be reached after folding on the mobile version.
- Responsive: 375px, 768px, 1024px, 1440px No horizontal overflow, occlusion or text truncation.
- Performance: images have size or aspect-ratio; images below the first screen are lazy loaded; virtualization is used when the list is too large.
- Animation: only animate transform/opacity, respecting `prefers-reduced-motion`.
- Status: loading, empty, error, disabled, hover, focus, and selected are all designed.

## Medium priority

- Font: The main text should not be smaller than 16px; use tabular nums for numerical columns, amounts, and timers.
- Color: Error, success, and warning are not only expressed by color.
- Form: label is resident, errors are close to fields, and there will be loading/success/error after submission.
- Navigation: The current route is identifiable, the return behavior is predictable, and deep pages can still return to the main path.
- Charts: replaced by titles, units, legends, tooltips or detailed tables, and the colors do not rely on the distinction between red and green.

## Anti-pattern

- Use decorative light spots, purple gradients, and card stacks to cover up the lack of information structure.
- Reuse three cards, left and right interleaving, split header or the same reveal animation for more than three consecutive paragraphs.
- Visual pages have only text and gradients, no real products, real status, brand applications or inspectable media.
- Bento uses empty grids to complete the composition, or feature grid. Each grid has the same weight, background, and rhythm.
-Hover causes layout displacement.
- `transition: all`、`will-change: all`。
- Low-contrast gray text, meaningless transparency, and single-hue interface.
- The empty status is only "No data yet" and there is no next action.
