# UI Color Systems

## Core Rule

- Product color systems succeed when components can reuse them predictably across light mode, dark mode, states, and future rebrands.

## Token Layers

| Layer | Purpose | Example |
|------|---------|---------|
| Primitive | Raw values | `blue-500`, `gray-900` |
| Semantic | Role in product | `text-primary`, `surface-muted`, `status-danger` |
| Component | Local application | `button-primary-bg`, `toast-error-border` |

- Skip direct primitive use in product components when the system is expected to evolve.
- Keep component tokens thin; too many component-only exceptions signal a weak semantic layer.

## Surface Strategy

- Define page, card, elevated, inverse, and overlay surfaces early.
- Surface separation should come from lightness structure first, not decorative shadows alone.
- Tinted surfaces need separate text and border checks; do not assume the default foreground still works.
- Dark mode often needs tighter surface spacing in lightness to feel coherent.

## Semantic States

- Primary, success, warning, error, and info should each have a clear role.
- Define the full state package: fill, text, border, icon, focus ring, and subtle background.
- Warning and error need enough separation from brand accents to avoid ambiguity.
- Do not force one hue to cover CTA emphasis and negative state signaling.

## Interactive States

- Hover, pressed, selected, focused, disabled, and loading states should feel related without becoming indistinguishable.
- Opacity-only disabled states often break contrast or become muddy on tinted surfaces.
- Focus indicators need visibility against both the component and the surrounding layout.
- Selected states need more than a slight background tint when the stakes are high.

## Dark Mode

- Design dark surfaces as a separate system, not a simple inversion.
- True black is sometimes right, but many interfaces benefit from slightly lifted dark neutrals.
- Saturated accents often appear brighter in dark mode and need recalibration.
- Shadows weaken in dark contexts; use surface lightness, borders, and blur intentionally.

## Token Governance

- Document what each semantic token means and what it must not be used for.
- If a token is renamed every time marketing refreshes the palette, the system is too brittle.
- Rebrands should mostly change primitive values and a few semantic mappings, not every component token.
- A good token system can express multiple themes without semantic chaos.

## Common UI Traps

- Letting teams ship components with raw hex values because token work feels slower.
- Reusing brand colors for every semantic need.
- Designing dark mode after the light theme is already component-complete.
- Using subtle border colors that disappear on high-density or low-quality screens.
- Allowing charts, badges, and interactive states to invent new colors outside the system.
