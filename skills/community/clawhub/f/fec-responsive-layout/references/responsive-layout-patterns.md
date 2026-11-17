# Responsive layout mode

## Strategy selection

| Scenario | Strategy |
| ---- | ---- |
| Page-level structure | Mobile-first breakpoints |
| Reused components that will be put into unknown parent containers | Container query |
| Card grid | `repeat(auto-fit, minmax())` and set a reasonable minimum width |
| Data tables | Column priority, horizontal scrolling, or mobile summary rows |
| Editor / canvas / dashboard | Stable shell + scrollable workspace |

## CSS Patterns

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: 1rem;
}

.panel {
  min-width: 0;
  container-type: inline-size;
}

@container (min-width: 42rem) {
  .panel-body {
    display: grid;
    grid-template-columns: 16rem minmax(0, 1fr);
  }
}
```

When grid/flex items contain long text, tables, code, charts, or media, set `min-width: 0` to the items.

## Data-intensive interface

- Prioritize mobile columns before coding.
- The main logo, status and main actions remain visible.
- Low priority metadata moved to details row, drawer or expandable panel.
- Small screens must still retain the ability to sort, filter, paging, and select.
- Virtual scrolling only solves the problem of DOM quantity, but cannot solve the problem of information hierarchy.
- The table can be partially scrolled horizontally, but the page as a whole should not have unintentional horizontal overflow.

## Responsive media

- Images and videos must have stable size, `aspect-ratio` or container constraints to avoid pushing the layout after loading.
- Use `srcset`, `sizes` or `<picture>` when you need multi-size resources, and do not let the mobile client download desktop large images.
- Non-first-screen images are lazy-loaded by default; first-screen main images are prioritized clearly based on frame capabilities.
- Media cropping must retain the main information; do not crop key areas of products, people, or charts just to fill the card.

## Touch and viewport inspection

- Interactive targets should be at least 44x44px, space permitting.
- Avoid lowering the font size of the mobile input box below 16px.
- Fixed bottom bars and action bars must consider `env(safe-area-inset-bottom)`.
- Dialog boxes and drawers need to adapt to viewport changes caused by the virtual keyboard.
- Content that only appears on hover must provide click, focus, or permanently visible alternatives.
- After switching between horizontal and vertical screens on iOS/Android, the main operation, focus position and scroll container should still be accessible.
- Areas that require partial scrolling should have a clear maximum height and scrolling boundary to prevent the page and internal containers from competing for scrolling.

## Verification list

- 320-375px: No horizontal overflow at the page level.
- 768px: The reading order is still reasonable after the layout is switched.
- 1024-1440px: The content width is constrained and the scanning path is clear.
- Long labels, translated text, numbers, and empty/error/loading states will not break fixed format controls.
- Switching between horizontal and vertical screens will not trap focus or hide the main operation.
- When the virtual keyboard pops up, the input box, submit button and error prompt are not blocked.
