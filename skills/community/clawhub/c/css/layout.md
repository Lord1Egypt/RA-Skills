# Layout Patterns

## Flexbox Patterns

- `display: flex; gap: 1rem` for spaced rows—clean and simple
- `justify-content: space-between` for nav/footer with logo and links
- `flex-wrap: wrap` + `flex: 1 1 300px` for card grids—responsive without media queries
- `align-items: stretch` is default—children fill height unless explicitly sized

## Grid Patterns

- `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))` for responsive cards
- `grid-template-areas` for complex layouts—visual and maintainable
- `grid-column: 1 / -1` for full-width items in grid
- Subgrid for aligned nested content—parent grid lines extend to children

## Centering Patterns

- `place-items: center` on grid—centers both axes
- `margin: auto` on flex child—pushes to edges or centers
- `position: absolute; inset: 0; margin: auto` for overlay centering
- Grid/flex on parent, auto margins on child—most robust approach

## Sticky Patterns

- `position: sticky; top: 0` for sticky headers—needs scrolling ancestor
- Sticky doesn't work with `overflow: hidden` on ancestor—clips the sticky area
- Multiple stickies can stack—adjust `top` values to account for each other
- Use `z-index` with sticky—it stacks above siblings

## Overflow Handling

- `overflow: hidden` clips content—use `overflow: clip` if you don't need scroll
- `overflow: auto` vs `scroll`: auto only shows scrollbar when needed
- `text-overflow: ellipsis` needs `overflow: hidden` AND `white-space: nowrap`
- `overflow-x: clip; overflow-y: visible` is tricky—often becomes `overflow-x: clip; overflow-y: auto`

## Box Model Patterns

- `box-sizing: border-box` on everything—width includes padding and border
- Margin collapse only vertical, only block—flex/grid children don't collapse
- `padding: max(1rem, 5vw)` for responsive padding—clamped minimum
- `outline` doesn't affect layout—useful for debugging without side effects

## Logical Properties

- `margin-inline`, `padding-block` for writing-mode aware spacing
- `inset-inline-start` instead of `left`—respects RTL
- `inline-size` instead of `width`—adapts to writing direction
- Use logical properties for international-ready CSS

## Common Layout Bugs

- 100% height not working—parent chain must also have defined height or use flexbox
- Content overflows container—`min-width: 0` on flex children
- Footer not at bottom—use flexbox or grid on body, `margin-top: auto` on footer
- Unexpected scrollbar—check for content slightly bigger than container
