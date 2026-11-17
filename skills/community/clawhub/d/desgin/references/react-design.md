# React Design Conventions

React is unopinionated about styling, which means design discipline must come from the design system, not the framework.

## Component Boundaries

- Favor small, composable components. A component should own one visual unit or one interaction pattern.
- Use composition over configuration: props like `variant` and `size` are better than long prop lists.
- CSS-in-JS, CSS Modules, Tailwind, or plain CSS are all valid; pick one and stay consistent.

## Styling Strategy

- Define tokens in one source of truth (CSS variables, a theme object, or a Tailwind config).
- Use utility-first CSS only when the team has agreed on the constraints. Do not let class name soup replace design thinking.
- Keep responsive styles with the component, not scattered across media queries.

## Responsive Patterns

- Use container queries when a component needs to adapt to its parent, not the viewport.
- Use CSS Grid for page layout and Flexbox for component-level alignment.
- `useMediaQuery` and `useResizeObserver` are useful for JS-driven layout decisions, but prefer CSS-first.

## Common Traps

- Inline styles for layout. Use class-based design tokens instead.
- Prop drilling theme values. Lift tokens to a shared context or CSS variables.
- Letting Tailwind defaults define the brand. Override the scale, colors, and spacing explicitly.
