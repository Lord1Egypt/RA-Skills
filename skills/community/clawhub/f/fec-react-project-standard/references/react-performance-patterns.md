# React performance patterns

This file keeps lightweight React project-standard performance guidance. Use the frontend performance workflow when the task needs metrics, traces, profiles, bundle analysis, network evidence, or a formal performance report.

### 性能（与「性能优化」一节配合）

- **useMemo**：昂贵派生、大列表排序/过滤；注意不可变数据，例如 `useMemo(() => [...list].sort(...), [list])`，避免直接 `sort` 可变原数组。
- **useCallback**：传给 **`React.memo`** 子组件或作为其他 Hook 依赖的回调，在确有稳定引用需求时使用。
- **React.memo**：纯展示、props 浅比较可接受的组件；不要全局套 memo。
- **虚拟列表**：超长列表用 **TanStack Virtual**、**react-window** 等，只渲染视区内节点（路由级与组件级懒加载仍见「Suspense 与懒加载」）。

## 性能优化

在以下场景考虑性能优化：

- 大列表 / 大表格
- 高频重渲染组件
- 大量 props 传递的复杂树
- 重型第三方组件
- 高频变化 context

### 推荐手段

- 合理使用 `React.memo`
- 只在必要时使用 `useMemo` / `useCallback`
- 列表使用稳定 `key`
- 大列表使用虚拟滚动
- 路由级做 code splitting
- 避免将高频变化值放进顶层 context
- 避免在 render 中无意义创建大量新对象 / 新函数 / 新数组
- 重型图表、编辑器、地图、3D 和媒体处理能力放到叶子组件或路由级懒加载边界
- 懒加载组件必须配套 loading、error、empty 或降级 UI，避免只优化包体却破坏用户状态

---

