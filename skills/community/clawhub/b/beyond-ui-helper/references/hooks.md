# Hooks & Utilities Reference

Beyond-UI ships a set of reusable hooks and helpers designed for dashboards and responsive apps. All are exported from the package root.

## Hooks

- **`useDarkMode`**
  - Persists light/dark preference (localStorage) and toggles data-theme attribute.
  - Returns `{ isDarkMode, toggleDarkMode, enableDarkMode, disableDarkMode }`.
  - Pair with `NightModeSwitch` for UI control.

- **`useDebounce<T>`**
  - Debounces a value with a configurable delay.
  - Signature: `const debounced = useDebounce(value, delayMs);`
  - Handy for search inputs or analytics events.

- **`useLocalStorage<T>`**
  - Syncs state with `localStorage`.
  - Signature: `const [value, setValue] = useLocalStorage(key, initialValue);`
  - Works on the client; guard behind SSR checks when necessary.

- **`useToggle`**
  - Boolean state helper.
  - Returns `[value, toggle, setTrue, setFalse]` for quick toggling in components.

- **`useBreakpoint`**
  - Responsive helper that maps to Tailwind breakpoints.
  - Signature: `const { isAbove, isBelow, current } = useBreakpoint();`
  - `isAbove('md')` returns boolean; use to adjust layout or component props.

- **`useIntersectionObserver`**
  - Wrapper around IntersectionObserver API.
  - Returns `{ ref, entry }` for lazy-loading or scroll-triggered animations.

## Utilities

- **`cn(...classes)`**
  - Tailwind-aware className merger using `tailwind-merge` under the hood.
  - Use when combining variant classes with overrides: `cn(buttonVariants({ variant }), "extra");`

- **`defaultTheme`**
  - Exported theme object containing fallback semantic tokens (used by the compiled CSS).
  - Import when you need raw values or to seed custom theming tools.

## Integration tips

- Hooks work out of the box with the compiled CSS; Tailwind is optional.
- Combine `useBreakpoint` with component `size` props (e.g., adjust Button size across breakpoints).
- Store user preferences (sidebar collapse, theme, tab selection) via `useLocalStorage` to maintain state across reloads.
- When using `useIntersectionObserver`, ensure the component renders client-side to avoid SSR mismatch.

For full examples, open the Storybook stories in the repo (`stories/*.stories.tsx`); each hook-backed component includes interactive demos.
