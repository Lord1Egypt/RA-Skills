# 框架专项性能诊断模式

本参考用于已经进入性能优化流程后的专项定位。先建立目标、基线和候选门禁，再按框架读取对应分类；不要从这些清单直接跳到结论。

## React / Client React

- **Waterfall**：独立请求、权限检查、feature flag 或子组件数据是否被串行等待。用 Network waterfall、React Profiler 或用户路径日志确认依赖关系。
- **Bundle**：首屏是否同步引入图表、编辑器、地图、3D、全量图标、重型日期库或 barrel export。用构建产物、source map 或 bundle analyzer 定位 chunk。
- **Rerender**：Context 是否过宽，selector 是否过粗，默认对象/数组 props 是否每次新建，昂贵派生是否在热路径重复执行。用 React Profiler 或可复现交互证明。
- **Effect**：是否用 effect 保存可直接推导的数据，是否把交互逻辑放进 effect，是否缺少取消、清理或稳定依赖。用渲染次数、请求次数或内存/订阅证据确认。
- **Lazy boundary**：Suspense、动态 import、错误 fallback、loading/empty/error 状态是否成对出现，懒加载是否破坏焦点或首屏布局稳定性。

## Vue 3 / Nuxt Client

- **Reactive payload size**：大型对象、表格数据或第三方实例是否被深层响应式代理。用组件更新、内存快照或长任务证据判断是否需要浅响应式或不可变边界。
- **Computed/watch**：本该 computed 的派生值是否用大范围 watcher 手动同步，watch 是否监听过宽对象，异步 watch 是否缺少取消和竞态处理。
- **Template hot path**：`v-for` 中是否混用 `v-if`、内联重计算、缺少稳定 `:key`，或在大列表中渲染非视区节点。
- **Async component boundary**：重型组件是否使用异步组件或路由级动态导入，加载状态是否稳定，错误态是否可恢复。
- **Store fan-out**：Pinia store 是否把高频 UI 临时状态扩散到大范围订阅者，或把服务端缓存复制到全局 store。

## Next.js

- **Dynamic route drift**：cookies、headers、searchParams 或未缓存 fetch 是否让静态路由变动态。用构建输出、响应头或路由行为确认。
- **RSC serialization**：Server Component 是否向 Client Component 传递过大 props、重复数据或不可序列化结构。
- **Fetch/cache policy**：`force-cache`、`no-store`、`revalidate`、tag/path revalidation 是否与数据私有性和更新频率匹配。
- **Client boundary leakage**：根布局或高层客户端边界是否同步带入重型浏览器库、Provider 或不必要状态。
- **Middleware cost**：middleware 是否承载重型查询、日志批处理或可放到 route handler 的业务逻辑。

## Nuxt 3

- **Rendering mode mismatch**：页面是否应为 SSR、SSG、ISR/route rules 或 SPA，实际行为是否和部署目标一致。
- **Data duplication**：`useFetch` / `useAsyncData` 是否重复请求，key 是否稳定，客户端 hydration 是否重复拉取同一数据。
- **Route middleware cost**：路由中间件是否做重型异步工作、重复鉴权请求或不可缓存的全局阻塞逻辑。
- **Client-only islands**：只在浏览器运行的图表、编辑器、地图或 WebGL 是否被隔离到 client-only 或异步边界。

## 输出要求

每个框架专项建议都要写清楚：证据来源、受影响路由/组件/chunk/请求、建议改法、验证命令和可能影响的 loading、error、empty、offline、reduced-motion 或移动端状态。
