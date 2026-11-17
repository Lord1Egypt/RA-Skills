# Component Patterns

Components are the building blocks of the interface. Each one should have a clear job, consistent states, and a predictable relationship with the design tokens.

## Cards

- One idea per card. Do not overload with actions.
- Use `surface` color, `md` padding, and `sm` border-radius.
- On mobile, cards can be full-bleed. On desktop, keep them in a grid or list.

## Forms

- Label every input clearly. Place labels above the field.
- Helper text below the field, not inside the placeholder.
- Error messages explain how to fix the problem.
- Primary action is obvious; secondary actions are visually quieter.

## Navigation

- Mobile: priority+ or hamburger with a visible primary CTA.
- Desktop: horizontal or sidebar, depending on the number of items.
- Active state is visible without relying on color alone.

## Tables and Lists

- Mobile: turn wide tables into cards or stacked rows.
- Desktop: keep tables with clear headers and zebra striping.
- Lists use consistent padding and clear separators.

## Buttons

- One primary action per screen or section.
- Disabled states must look disabled.
- Loading states preserve layout width to prevent shift.
- Touch target minimum 44x44px.

## Empty and Error States

- Empty: explain what is missing and what to do next.
- Error: say what happened and how to recover.
- Loading: show a skeleton or progress that matches the final shape.
