# Vue 3 performance patterns

This file keeps lightweight Vue project-standard performance guidance. Use the frontend performance workflow when the task needs metrics, traces, profiles, bundle analysis, network evidence, or a formal performance report.

## 性能

- 使用 `shallowRef` / `shallowReactive` 优化大型对象
- 大列表使用虚拟滚动
- 避免在 `v-for` 中使用 `v-if`（提取为 computed 过滤）
- 使用 `defineAsyncComponent` 懒加载重型组件
- `v-for` 必须有稳定的 `:key`
- 路由组件使用动态 `import()` 按需加载

