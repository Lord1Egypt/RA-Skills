# React performance patterns

This file keeps lightweight React project-standard performance guidance. Use the frontend performance workflow when the task needs metrics, traces, profiles, bundle analysis, network evidence, or a formal performance report.

### Performance (in conjunction with the "Performance Optimization" section)

- **useMemo**: Expensive derivation, large list sorting/filtering; pay attention to immutable data, such as `useMemo(() => [...list].sort(...), [list])`, and avoid directly `sort` the mutable original array.
- **useCallback**: passed to **`React.memo`** sub-component or used as a callback for other Hook dependencies, used when there is a stable reference requirement.
- **React.memo**: An acceptable component with pure display and shallow props; do not apply memo globally.
- **Virtual List**: For very long lists, use **TanStack Virtual**, **react-window**, etc., and only render nodes in the viewport (see "Suspense and Lazy Loading" for routing-level and component-level lazy loading).

## Performance optimization

Consider performance optimization in the following scenarios:

- Large list/large table
- High frequency re-rendering components
- Complex trees passed with a large number of props
- Heavy-duty third-party components
- High frequency changing context

### Recommended means

- Use `React.memo` appropriately
- Use `useMemo` / `useCallback` only when necessary
- List uses stable `key`
- Use virtual scrolling for large lists
- Code splitting at routing level
- Avoid putting high-frequency changing values into the top-level context
- Avoid meaninglessly creating a large number of new objects/new functions/new arrays in render
- Heavy charting, editor, map, 3D and media processing capabilities into leaf components or route-level lazy loading boundaries
- Lazy loading components must be equipped with loading, error, empty or downgraded UI to avoid only optimizing the package body but destroying the user state

---

