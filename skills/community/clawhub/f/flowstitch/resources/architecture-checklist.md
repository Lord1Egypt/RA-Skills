# React Component Architecture Quality Gate

Run through this checklist before considering a React export complete.
All items must pass before committing components to the codebase.

## Structural Integrity

- [ ] Logic extracted to custom hooks in `src/hooks/` — no inline event handlers
- [ ] No monolithic files — strictly Atomic/Composite modularity (one component per file)
- [ ] All static text, image URLs, and lists moved to `src/data/mockData.ts`
- [ ] Data and presentation clearly separated

## Type Safety & Syntax

- [ ] Props use `Readonly<T>` TypeScript interfaces named `[ComponentName]Props`
- [ ] File is syntactically valid TypeScript (no type errors)
- [ ] All template placeholders replaced (`StitchComponent` → actual name)
- [ ] No `any` types — use proper TypeScript types throughout
- [ ] Imports are clean and all used

## Styling & Theming

- [ ] Dark mode (`dark:`) applied to all color utility classes
- [ ] No hardcoded hex values — use theme-mapped Tailwind classes only
- [ ] Tailwind config extracted from Stitch HTML `<head>` and synced to `resources/style-guide.json`
- [ ] Consistent spacing using design system scale (no arbitrary values unless in theme)
- [ ] `cn()` from `@/lib/utils` used for all conditional/composed className strings (not template literals)

## Accessibility

- [ ] Interactive elements have proper `aria-label` or visible text
- [ ] Images have `alt` attributes
- [ ] Focus states are visible (don't remove `focus:ring` or `focus-visible`)
- [ ] Semantic HTML elements used where appropriate (`nav`, `main`, `section`, `button`)

## Component Quality

- [ ] Component renders correctly in isolation
- [ ] Responsive behavior verified at all three breakpoints:
  - [ ] Mobile: `< 768px` (sm breakpoint)
  - [ ] Tablet: `768px–1024px` (md breakpoint)
  - [ ] Desktop: `≥ 1280px` (xl breakpoint)
- [ ] `npm run validate <file_path>` passes (if validator available)
- [ ] Dev server check: `npm run dev` shows component renders without errors

## Performance

- [ ] Heavy/route-level components use `lazy()` + `Suspense` where appropriate
- [ ] Images have `loading="lazy"` and `decoding="async"` attributes
- [ ] No unnecessary re-renders (memoize expensive computations with `useMemo`)
- [ ] Large lists use virtualization hint (comment) if > 100 items

## Admin Dashboard Components (if applicable)

- [ ] DataTable: sortable columns, row hover, bulk select, pagination
- [ ] KPICard: metric value, label, trend arrow/percentage, optional sparkline
- [ ] ChartWrapper: title + subtitle, time range selector, legend, responsive
- [ ] FilterBar: search input + dropdown filters + active filter chips + clear
- [ ] Sidebar: expanded (icon+label) + collapsed (icon-only) states

## Mobile App Components (if applicable)

- [ ] Bottom tab bar respects 49px height and safe area padding
- [ ] Touch targets are minimum 44×44px for all interactive elements
- [ ] Safe area insets applied (`pb-safe`, `pt-safe` or `env(safe-area-inset-*)`)
- [ ] No interactive elements inside home indicator safe area (bottom 34px)

## File Organization

```
src/
├── components/
│   ├── ui/              # shadcn/ui components (don't edit directly)
│   ├── layout/          # Sidebar, Header, Footer, Layout wrappers
│   ├── dashboard/       # KPICard, DataTable, ChartWrapper, FilterBar
│   └── [feature]/       # Your composed Stitch components
│       └── ComponentName.tsx
├── hooks/
│   └── useComponentLogic.ts
├── data/
│   └── mockData.ts
├── pages/               # Route-level components (lazy-loaded)
│   └── DashboardPage.tsx
└── lib/
    └── utils.ts         # cn() and shared utilities
```
