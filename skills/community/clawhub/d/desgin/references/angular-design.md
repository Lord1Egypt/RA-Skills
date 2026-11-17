# Angular Design Conventions

Angular favors a more structured, opinionated component model. The design should respect the framework's separation of concerns without being dictated by it.

## Component Boundaries

- One component per responsibility. Split page shells, feature modules, and shared UI into distinct layers.
- Use Angular's `@Component` for visual units. Keep the template focused on layout and binding, not logic.
- Leverage Angular Material or PrimeNG only after a deliberate design decision. Do not let default palettes stand in for brand identity.

## Styling Strategy

- Prefer component-scoped styles with `ViewEncapsulation.Emulated` for UI widgets.
- Use CSS custom properties for the design token layer.
- Global styles should live in `styles.scss` and define the type scale, color, spacing, and grid variables.

## Responsive Patterns

- Use `BreakpointObserver` from `@angular/cdk/layout` to react to breakpoint changes.
- Use `@angular/flex-layout` only if already in the project; the modern path is CSS Grid/Flexbox with custom properties.
- Route-level layouts: keep `app.component` as a shell and let feature components own their responsive behavior.

## Common Traps

- Overusing Angular Material defaults without custom theming.
- Storing design tokens in component files instead of global or token files.
- Creating giant templates with deeply nested `*ngIf`. Break into smaller components.
