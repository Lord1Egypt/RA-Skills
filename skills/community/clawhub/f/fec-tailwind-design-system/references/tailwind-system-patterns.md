# Tailwind system mode

## Token mapping

Prefer using semantic names:

| Need | Recommend | Avoid |
| ---- | ---- | ---- |
| Brand color | `brand.600`, `--color-brand-primary` | Copy everywhere `blue-600` |
| Surface level | `surface.canvas`, `surface.panel` | One-time gray value |
| rounded corners | `radius.control`, `radius.panel` | optionally repeated specific values |
| Shadow | `shadow.floating`, `shadow.focus` | Decorative shadow with no state meaning |

If the project already has CSS variables, map Tailwind tokens to these variables instead of repeatedly maintaining literals.

## Variant Attribution

Long class combinations should converge to one of the following locations:

- Shared components with `variant`, `size`, `tone`, `density`, `state` props.
- Slot mapping table of composite components.
- Typed helpers such as CVA, tailwind-variants or local `classNames` mappings.
- Use local constants when reusing them within only one module.

Don't splice class names based on uncontrolled user input. Use explicit mapping:

```ts
const toneClass = {
  neutral: "bg-slate-100 text-slate-900",
  danger: "bg-red-600 text-white",
  success: "bg-emerald-600 text-white",
} as const;
```

## Dark mode

- Prefer a single project-level strategy: `class`, `data-theme` or CSS variables.
- If the application supports manual theme switching, initialize the selected theme before the body is drawn to avoid flickering of the first screen that first lights up and then darkens or first darkens and then lights up.
- Test disabled, focus, selected, invalid, chart and skeleton states in both light and dark themes.
- Don't use lowering transparency as the only hint of disabled; preserve contrast and perceptibility.
- When the Tailwind project uses `darkMode: "class"` or equivalent configuration, the theme switching logic should maintain the root node class / data attribute and persist user preferences.
- In the CSS variable scheme, Tailwind token should refer to semantic variables; do not scatter two sets of utility literals for light and dark colors.
- When placing a minimal synchronization initialization script in `<head>` or a framework equivalent entry, only local theme preferences and system preferences are read, no business logic is executed, and no server-side data is accessed.
- In dark mode, you need to review the image brightness, shadow level, form controls, third-party components, chart color palette and focus ring; don't just add the background color.

## Responsive tool class

- The default class list starts with mobile layout.
- Only add larger breakpoint prefixes when the information architecture changes.
- Recurring responsive blocks should be precipitated into layout components or CSS container queries, and do not duplicate the same string of breakpoints repeatedly.
- Controls, tabs, dashboards and data cells use stable sizes to avoid layout jumps caused by hover and loading states.

## Review Checklist

- Token values have semantic roles and do not fork existing design rules.
- Component variants cover loading, disabled, selected, invalid, focus-visible and dark mode.
- Dynamic classes can be recognized by static scans, or have been safely added to the safelist.
- Tailwind utility classes have no accessibility-breaking, click-targeting, or reduced-motion requirements.
- Final UI checked in mobile, tablet and desktop widths.
