# Vue 3 performance patterns

This file keeps lightweight Vue project-standard performance guidance. Use the frontend performance workflow when the task needs metrics, traces, profiles, bundle analysis, network evidence, or a formal performance report.

## Performance

- Use `shallowRef` / `shallowReactive` to optimize large objects
- Use virtual scrolling for large lists
- Avoid using `v-if` in `v-for` (extract to computed filtering)
- Use `defineAsyncComponent` to lazily load heavy components
- `v-for` must have a stable `:key`
- Routing components are loaded on demand using dynamic `import()`

