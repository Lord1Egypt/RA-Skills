---
subdomain: react-core
version: 26
updated: 2026-11-17
---
# React 核心

## 定位与心智模型

React 是声明式 UI 库：`UI = f(state)`。三条主线覆盖大部分问题：**渲染时机**（state 变化 → 重渲染）、**渲染范围**（谁的 state 谁渲染 + 子树）、**闭包捕获**（每次渲染都是一次快照）。

## 法则

[RC-1] **MUST**: hooks 只在组件顶层无条件调用，依赖数组写全。
- 违反后果: `Rendered fewer hooks than expected` 崩溃；或空依赖 stale closure 静默 bug
- 溯源: Rules of Hooks [官方文档](https://react.dev/reference/react/hooks)

[RC-2] **NEVER**: 派生值不得存 state 再用 effect 同步。
- 违反后果: 双份真相偶发不同步
- 溯源: [官方文档](https://react.dev/learn/you-might-not-need-an-effect)

[RC-3] **NEVER**: 动态列表不得用 index 作 key。
- 违反后果: 删插后输入框/展开态串行到错误行
- 溯源: [官方文档](https://react.dev/learn/rendering-lists)

[RC-4] **MUST**: setState 更新对象/数组必须产生新引用。
- 违反后果: Object.is 相等，UI 静默不更新
- 溯源: [官方文档](https://react.dev/reference/react/useState)

[RC-5] **NEVER**: effect 函数不得声明为 async（async 逻辑放 effect 体内）。
- 违反后果: 返回 Promise 被当 cleanup 调用
- 溯源: [官方文档](https://react.dev/reference/react/useEffect)

[RC-6] **MUST**: 异步 setState 前检查组件是否仍挂载/请求是否过期（ignore 标志或 AbortController）。
- 违反后果: 旧响应覆盖新数据
- 溯源: [模型经验]

[RC-7] **NEVER**: 高频 Context value 不得裸传（不包 useMemo/不拆分读写）。
- 违反后果: value 每渲染新引用，全体 consumer 级联重渲染
- 溯源: [模型经验]

[RC-8] **MUST**: 错误边界只当渲染期兜底；事件回调和异步代码自带 try/catch。
- 违反后果: 异步异常穿透边界直接白屏
- 溯源: [官方文档](https://react.dev/reference/react/Component#static-getderivedstatefromerror) + [模型经验]

[RC-9] **MUST**: 基于旧值更新 state 用函数式更新 `setC(c => c+1)`。
- 违反后果: 批处理下读旧闭包值，更新丢失
- 溯源: [官方文档](https://react.dev/reference/react/useState)

[RC-10] **NEVER**: 服务端数据不得手动复制进全局客户端 store 再手写 loading/error（全局宪法 LAW-2）。
- 溯源: [模型经验]

[RC-11] **MUST**: memo 化优化前先 Profiler 测量（全局宪法 LAW-11）。
- 溯源: [模型经验]

[RC-12] **MUST**: useSyncExternalStore 的 getSnapshot 在 store 未变时必须返回同一引用（缓存值）。
- 违反后果: 每次渲染新对象 → 无限渲染循环 + "The result of getSnapshot should be cached"
- 溯源: [官方文档](https://react.dev/reference/react/useSyncExternalStore)

[RC-13] **MUST**: useActionState 的已知校验错误 return state（可携 FormData 保留值），未知错误才 throw；action 内 await 之后的 setState 须再包 startTransition。
- 违反后果: 未知错误取消全部排队 action 落 Error Boundary；await 后 setState 丢失 pending 上下文
- 溯源: [官方文档](https://react.dev/reference/react/useActionState)

[RC-14] **MUST**: Context provider 的对象/函数值必须用 `useMemo` 稳定引用（函数成员 `useCallback`）或改传原始值；不得依赖 `memo` 阻断 context 更新传播。
- 违反后果: 每次渲染新引用 → 所有消费子树重渲染；`memo(Child)` 对 context 更新无效
- 溯源: [官方文档](https://react.dev/reference/react/useContext)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| 渲染 | React 调用组件函数计算虚拟 DOM 树，不是更新 DOM |
| fiber | 组件实例的内部数据结构，hooks 状态存在链表里 |
| 批处理 | 同一事件中多次 setState 合并为一次渲染 |
| 并发特性 | React 可中断渲染、按优先级调度更新 |
| 错误边界 | 捕获子树**渲染期**错误的组件（class 或 19 的 `<ErrorBoundary>`） |
| React Compiler | 编译期自动 memo 化（v1.0 稳定 2025-10；`"use memo"`/`"use no memo"` 指令控制） |

## 最佳实践

### 场景：状态设计与状态库深面（zustand / RTK Query / XState / Jotai / tRPC）

推荐路径：本地 UI 态 useState → 跨 2~3 层共享用状态提升/context（读多写少）→ 全局客户端态 zustand/RTK → 表单 react-hook-form → 服务端数据 TanStack Query/RSC（[RC-10]）。

```tsx
// don't：派生值存 state + effect 同步（违反 [RC-2]）
const [fullName, setFullName] = useState('');
useEffect(() => setFullName(`${first} ${last}`), [first, last]);

// do：渲染时计算
const fullName = `${first} ${last}`;
```

边界条件：确需"props 变化重置"语义时用 `key` 强制重挂载，而不是 effect 同步。

**zustand 5.1 关键面**（官方文档锚定，2026-11-16）：

- `create((set) => ({...}))`；set 是**浅合并**；无 Provider；selector 订阅（Object.is 判等）
- **useShallow**：`import { useShallow } from 'zustand/react/shallow'`（v5 路径）——计算选择器（Object.keys/过滤）每次新引用必重渲染，用 useShallow 浅比较拦截
- **persist**：`storage` 默认 localStorage（createJSONStorage 惰性 getter，SSR 安全）；`partialize` 字段过滤；`version + migrate` 版本迁移；`merge` 默认**浅合并**（嵌套缺字段需自定义深合并）；`skipHydration: true` + 手动 `rehydrate()`（SSR 用）
- **坑**：createJSONStorage 无运行时校验——JSON.parse 直 cast，生产建议自定义 PersistStorage + Zod 校验（官方明确推荐）
- 来源：[官方文档](https://zustand.docs.pmnd.rs/reference/middlewares/persist)

**RTK Query 关键面**（redux-toolkit.js.org 锚定，2026-11-16）：

- @reduxjs/toolkit 内置；`createApi`（一个 base URL 一个 API slice）+ `fetchBaseQuery`；reducer + middleware 必挂 store；`setupListeners` 启用 refetchOnFocus/Reconnect
- **tagTypes 失效模型**：query 声明 `providesTags`、mutation 声明 `invalidatesTags`；列表用虚拟 id `'LIST'`（新增失效 LIST、更新/删除失效 `{ type, id }` 精确命中）
- `useMutation` 返回 [trigger, result] 元组；trigger promise 带 `.unwrap()`；`fixedCacheKey` 跨组件共享 mutation 结果
- **Standard Schema 运行时校验**：endpoint 可配 `responseSchema/rawResponseSchema/queryArgSchema`（Valibot/Zod 等），TS 下可从 schema 推断类型
- `onQueryStarted` 乐观更新；`onCacheEntryAdded` 流式更新（cacheDataLoaded/cacheEntryRemoved）
- 来源：[官方文档](https://redux-toolkit.js.org/rtk-query/usage/mutations)

**tRPC（v11.28.3）**：TS ≥5.7.2 硬要求；procedure（`.input(zod).query()/.mutation()`）→ `type AppRouter` 客户端 type-only 导入 → 端到端类型安全；React 客户端用 **@trpc/tanstack-react-query 工厂模式**（`trpc.x.queryOptions()`/`mutationOptions()`，官方推荐；经典 `@trpc/react-query` 钩子已弃用下大版本移除）；base procedures 中间件收窄 ctx（authedProcedure 模式）；**非 TRPCError 的 message 生产也发客户端——须 errorFormatter + onError 双件套**（OWASP）；httpBatchLink 自动合并请求；适配 Express/Fastify/Next.js（App Router=fetch adapter）。适合 TS 全栈同仓项目；JS 混合/跨团队 API 边界用 OpenAPI 生态更稳。
- 来源：[官方文档](https://trpc.io/docs/client/tanstack-react-query/setup)

**XState v5（5.33.4，状态机/复杂编排）**：v5 核心抽象是 **actor model**——`createMachine({context, on, states})` → `createActor(m).start()` → `send/subscribe`；**v4→v5 破坏面**：`interpret()`→`createActor()`、services→**actors**（invoke.src 指 fromPromise 逻辑）、onDone 取 **`event.output`**（非 v4 `event.data`）。React 侧：`useMachine(machine)` = `useActor(logic)` → `[snapshot, send, actorRef]`；细粒度优化 `useActorRef`（静态引用不重渲染）+ `useSelector(actorRef, selector, compare)`（**默认严格 ===——非原始值 selector 须 shallowEqual 或稳定引用**）；全局共享 `createActorContext(machine)`；实现注入 `machine.provide({actions, guards, actors})`；嵌套/并行机用 `state.matches(...)` 判（switch(true) 模式）；持久化经 `options.snapshot`。**适用边界**：多步工作流/向导/明确状态迁移场景——简单表单/共享态用 zustand/Jotai 更轻（**6.0 已进 beta——6.0.0-beta.3，未 stable 锁 5.x**）。
- 来源：[官方文档](https://stately.ai/docs/xstate) + [官方文档](https://stately.ai/docs/xstate-react)

**Jotai v3（3.0.2，原子化状态）**：**v3 硬门槛 peer React ≥18**（v2 支持 16.8+）；最小核心 2kb、无字符串 key（对比 Recoil）。模型：`atom(initialValue)` 原始原子 → `useAtom(atom)` 如 useState；派生只读 `atom((get) => get(a) + get(b))`；可写派生 `atom(read, (get, set, arg) => ...)`；只写 `atom(null, write)`（解构 `[, action]`）；异步读 atom 需 Suspense 边界、异步 action ready 后 set。适用：原子间天然派生依赖图、细粒度订阅；自顶向下 store 形态（zustand）更适合。
- 来源：[官方 README]（jotai.org 不可达，经 npm tarball 锚定，2026-11-16）

### 场景：获取异步数据（组件内 fetch 时）

推荐路径：effect 内定义 async IIFE → ignore 标志防竞态（[RC-6]）→ cleanup 置位。数据复杂就升级 TanStack Query。

```tsx
useEffect(() => {
  let ignore = false;
  (async () => {
    const data = await fetchUser(id);
    if (!ignore) setUser(data);
  })();
  return () => { ignore = true; };
}, [id]);
```

边界条件：SSR 首屏数据不要走这条路——用 RSC await 或 TanStack Query 预取（见 `kb/nextjs.md`）。

### 场景：性能优化

推荐路径（LAW-11，从高到低收益）：1) 网络与 bundle（代码分割）2) 避免不必要渲染（context 拆分 [RC-7]、状态下沉、children 组合）3) 渲染变便宜（虚拟化列表）4) memo 微优化——**启用 React Compiler 的项目直接跳过第 4 步手写 memo**（v1.0 稳定，2025-10-07 [官方文档](https://react.dev/blog)；构建链须 Babel 模式，与 Vite SWC 互斥，见 `kb/vite-tooling.md`）。

```tsx
// don't：无脑 memo（props 每次新引用，memo 无效）
<Child data={items.filter(x => x.active)} />

// do：稳定引用；Compiler 项目交给编译器
const activeItems = useMemo(() => items.filter(x => x.active), [items]);
```

**React Compiler 关键面**（官方文档锚定，2026-11-16）：

- **compilationMode**：`'all'` | `'annotation'`（只编译带 `"use memo"` 的函数）| `'infer'`（编译器自判）；指令可函数级覆盖模块级
- **指令**：`"use memo"` opt-in / `"use no memo"` opt-out（调试或兼容问题时用，须注释原因并计划移除）；`ignoreUseNoForget` 配置会无视 opt-out
- **panicThreshold: 'none' 生产推荐**——违规组件跳过编译而非 fail build
- **React 17/18 项目须另装 `react-compiler-runtime` 包**并配 `target: '18'|'17'`；19 零配置
- **构建链**：Babel/Vite/Metro/Rsbuild（Babel plugin 为核心编译器轻包装）；Next.js ≥15.3.1 可用 swc 调用
- **存量手写 memo 不删**（删除会改变编译输出）或删前充分测试；`useMemo`/`useCallback` 保留为 escape hatch（典型：memo 值作 effect 依赖精确控制重跑）
- **gating**：运行时特性开关（source + importSpecifierName）——A/B 测试/渐进放量编译产物
- 昂贵计算 memo **不跨组件共享**——多处复用的真昂贵函数自带 React 外 memoization
- 来源：[官方文档](https://react.dev/learn/react-compiler/introduction) + [官方文档](https://react.dev/reference/react-compiler/configuration) + [官方文档](https://react.dev/reference/react-compiler/directives)

### 场景：显隐切换且保留状态（Activity）

推荐路径：切换显隐且需保留内部 state/DOM（tab 面板草稿、展开态、video 时间码）用 `<Activity mode={show ? "visible" : "hidden"}>`（19.2）；无需保留用条件渲染（卸载语义更干净）。

- **hidden 语义**：`display: none` + **销毁 Effects**（清理订阅）+ 保留 state 与 DOM；再 visible 时恢复 state、重建 Effects——"hidden = 概念上 unmount 但 state 被保存"
- **预渲染**：初始渲染即 `mode="hidden"` → children 低优先级渲染、不挂 Effects，提前加载代码/数据；**只预取 Suspense 激活源的数据（如 `use(promise)`），Effect 内手取的数据不预取**
- **Selective Hydration**：Activity 边界像 Suspense 一样切分水合单元——**恒 visible 的 `<Activity>` 包裹也提升水合性能**（UI 不变）
- **坑**：隐藏后 DOM 副作用存活——`<video>`/`<audio>`/`<iframe>` 继续播放，须 `useLayoutEffect` 返回 cleanup 暂停（勿用 useEffect——可能被 re-suspending Suspense/View Transition 延迟）
- **坑**：hidden 且 children 只渲染纯文本（无 DOM 元素挂 display:none）→ **无输出**
- 位于 `<ViewTransition>` 内且由 startTransition 更新切换显隐 → 触发 `enter`/`exit` 动画
- 来源：[官方文档](https://react.dev/reference/react/Activity)

### 场景：表单

推荐路径：react-hook-form + Zod resolver——`useForm()` → `handleSubmit(onValid)` → `formState.errors`；第三方 UI 库组件用 `Controller` 桥接。非受控 register 直连 DOM，重渲染远少于受控组件每键入 setState。坑：`formState` 属性须解构订阅（`const { errors } = formState`）否则 Proxy 不追踪。
- 来源：[模型经验]

关键语义（RHF 7.92 / @hookform/resolvers 7.0.6 / zod 4.6 官方文档锚定，2026-11-16）：

- **mode 推荐默认 `onTouched`**（首次 blur 报错、之后 change 实时更新）；`onChange` 性能代价大；mode/reValidateMode 自 7.56 起响应式可热更
- **服务端取数填表四路**：① 一次性编辑表单 → 异步 `defaultValues`（mount 跑一次；reject 则 `isLoading` 恒 true——函数内 catch 返回 fallback）；② 持续同步服务端态 → `values` 属性（deep-compare；变化即 reset **覆盖用户已输入**——后台 refetch 场景必配 `resetOptions: { keepDirtyValues: true }`）；③ 全控 → effect 内 `reset(data)`；④ 最简 → 父组件取数后再渲染表单传 defaultValues
- **formState 订阅规则**：渲染期解构才追踪；事件处理器内读 `formState.isValid` 恒 false（未订阅）——需在渲染期解构使用
- **`validate`（7.72+）表单级校验与 resolver 互斥**（两者同设仅 resolver 跑）；resolver 与字段内置校验规则互斥
- **自定义 resolver 错误键必须层级化**（嵌套对象 `{ participants: [null, { name: err }] }`），扁平 `"a.1.b"` 键无法正确 set/clear
- **zod v4 生成规则**（确认项目大版本线）：顶层格式 `z.email()`/`z.iso.date()`（方法版弃用）；错误参数统一 `error`（message/errorMap 弃用）；`.refine()` 后可继续 `.min()`（ZodEffects 包装消失）；`z.discriminatedUnion` 可组合；`z.toJSONSchema()`/`z.prettifyError()` 一方支持；i18n `z.config(zod/locales)`
- **RHF v8 beta（8.0.0-beta.0）已发布**：useFieldArray `id`→`key`（keyName 移除）、`watch(callback)` 重载移除改 `subscribe({ formState, callback })`、`valueAsDate` 空输入返回 null（v7 为 Invalid Date）、React Compiler 支持（register/watch/getValues 引用随 form state 变化）——为 v7 项目生成代码时勿混入 v8 API
- 来源：[官方文档](https://react-hook-form.com/docs/useform) + [官方文档](https://react-hook-form.com/migrate-v7-to-v8) + [官方文档](https://zod.dev/v4)

### 场景：Zod v4 校验（v3→v4 迁移与生成规则）

推荐路径：确认项目 zod 大版本线（v4 主线 4.6.7 / `zod/v3` 兼容入口并存）再生成 [官方文档](https://zod.dev/v4/changelog)。v4 生成规则：顶层格式 API（`z.email()`/`z.uuid()`/`z.iso.date()`）、错误参数统一 `error`、`z.record(keySchema, valueSchema)` 双参、`z.strictObject()`/`z.looseObject()` 替代方法形式。

**v3→v4 破坏面速查（迁移必查）**：

| v3 写法 | v4 结论 |
|---|---|
| `z.record(z.string())` 单参 | **移除**——必须 `z.record(keySchema, valueSchema)` |
| `z.object({ a: z.any() }).parse({})` | **v4.4+ 报错**——any/unknown 键必填，可缺键须显式 `.optional()` |
| `.default(v)`（v = input 类型，parse 默认值） | **短路语义**——默认值须匹配 **output** 类型；旧行为 `.prefault()` |
| 对象缺含 `z.coerce.*` 字段的键 | v3 静默转换 → **v4 报错**（须显式 `.default()`） |
| `message:`/`errorMap`/`invalid_type_error` | 弃用/移除——统一 `error` 参数（可回调返回 string/undefined） |
| `z.nativeEnum(E)` | 弃用——`z.enum(E)` 直接收原生 enum；`.Enum`/`.Values` 移除 |
| `.merge()`/`.strict()`/`.passthrough()` | 弃用——`.extend()`/`z.strictObject()`/`z.looseObject()` |
| `err.format()`/`.flatten()` | 弃用——`z.treeifyError()` |
| `z.string().ip()`/`.cidr()` | 移除——`z.ipv4()`/`z.ipv6()`/`z.cidrv4()`/`z.cidrv6()` |
| `z.function().args().returns().implement()` | 重构——工厂 `{ input, output }` + `.implement()`/`.implementAsync()` |

边界条件：enum 键 record **穷尽校验**（所有枚举键必须存在，部分键 `z.partialRecord()`）；`.uuid()` 严格 RFC 9562/4122（宽松用 `z.guid()`）；`.refine()` 后可继续 `.min()`（ZodEffects 包装消失）；`.refine()` 类型谓词不再收窄类型、`ctx.path` 移除；`.int()` 仅安全整数、`z.number()` 拒 ±Infinity。**4.6 新面**：`.validate()`/`.validateAsync()` 布尔守卫（不构建 ZodError、首个 issue 短路，配 `z.compile()` AOT 比 `safeParse().success` 快至 35x）；`z.withParser()` 安装外部 parser（CSP 禁 `new Function` 环境）；**@zod/mini 自 4.5 独立包**（锁步发版）；**safeParse 错误懒构建**（error maps 首次读 `result.error` 才执行——parse 与 read 之间换 `z.config()` locale 生效新配置；throwing `.parse()` 不受影响）[官方文档](https://zod.dev/blog/zod-4-6)。

**`z.compile()` AOT 编译**（[官方文档](https://zod.dev/compile)，热路径性能面）：

- 编译产物仍是普通 Zod schema（同方法/同类型/同错误）；**容器受益最大**（20 键对象 7.8x、50 键 10.2x、10 元素数组 5.5x；合法输入为主场景才划算——**非法输入付快路径+回退双成本**，提速甚微）
- **编译放最后**：`.refine()/.extend()/.optional()` 等派生方法返回未编译 schema——先派生完再 `z.compile()`（❌ `z.compile(z.string()).refine(...)` 的 refine 不编译）
- 全局模式 `import "zod/compile"`（**须在定义 schema 的模块前**，惰性首 parse 编译）；Node CLI `node --import zod/compile`；**应用可用、库勿用**
- 不支持面原样返回：async refinements/transforms/checks、`z.xor()`、递归 schema、`z.coerce.*`、自定义 `when`、`.catch(callback)`（`.catch(常量)` 可编译）；union 含不支持成员/子树任何 async 整体回退；`z.compile(S, { strict: true })` 可验证真编译（抛 `ZodCompileUnsupportedError`）
- CSP/no-eval：全局模式 `z.config({ jitless: true })` 收手；编译器 **+7KB gzip** 仅使用时进包（tree-shake 完全）

### 场景：React Router 7/8（框架模式）

推荐路径：框架模式（`create-react-router` + Vite 插件 + `app/routes.ts` 配置路由 + Route Module）优先于库模式；确认大版本线（**v8 latest=8.5.1**，要求 **Node ≥22.22 / React ≥19.2.7 / Vite 7+ / ESM-only**；v7 线末版 7.18.5）[官方文档](https://reactrouter.com/changelog)。

- **路由配置**：`route/index/layout/prefix` 助手（`@react-router/dev/routes`）；`layout` 嵌套不加 URL 段、`prefix` 加前缀不引入节点；类型推断 `import type { Route } from "./+types/team"`；**组件 props（loaderData/actionData/params）优先于 hooks**（自动类型化）
- **Route Module 导出**：`loader`（服务端）/`clientLoader`（`hydrate = true as const` 参与首屏水合）/`action`/`clientAction`/`middleware`（服务端链式 `next()` + `context.set`）/`clientMiddleware`/`ErrorBoundary`/`HydrateFallback`/`headers`/`handle`/`links`/`meta`（React 19 起优先原生 `<title>/<meta>` 元素）/`shouldRevalidate`
- **框架模式 SSR 下 loader 每次导航/提交后自动全量重验证**（≠ Data Mode 默认）；按路由退出用 `shouldRevalidate`（不跳父/兄弟），单点退出调用处 `defaultShouldRevalidate={false}`；恒 `false` 会 UI 失同步
- **v8 断裂面**：`react-router-dom` 包**移除**——`RouterProvider`/`HydratedRouter` 改从 **`react-router/dom`** 导入；middleware 恒开（自定义 server 的 `getLoadContext` 必须返回 `RouterContextProvider`）；原始 request 恒传 loader/action（v8_passThroughRequests 转正）；**尾斜杠感知数据请求**（`/a` 与 `/a/` 数据不再共享，v8_trailingSlashAwareDataRequests 转正）；meta 函数 `data` 参数 → `loaderData`；`splitRouteModules` 默认 true；`hasErrorBoundary` 移除
- 生态面：8.1 起 create-react-router 默认装官方 Agent Skill；8.4 内部 context 拆 4 个（**只用 useLocation 不再因 navigation.state 重渲染**）；8.5 起**自带 View Transition API 弃用 → React 19.3+ `<ViewTransition>`**（v9 移除）；非 Node 运行时默认 Web Streams entry
- 来源：[官方文档](https://reactrouter.com/start/framework/routing) + [官方文档](https://reactrouter.com/start/framework/route-module) + [官方文档](https://reactrouter.com/changelog)

### 场景：TanStack Start/Router 1.x（路由选型对照）

推荐路径：**TanStack Start 已 stable**（@tanstack/react-start 1.169.5 / @tanstack/react-router 1.170.46，2026-11 锚定；peer **Vite ≥8**、Node ≥22.12，构建器 Vite 或 Rsbuild）。选型：要 full-document SSR/Streaming/Server Functions → Start；只要类型安全 SPA 路由 → 只用 Router；React 生态路由三选（React Router 8 框架模式 / TanStack Start / Next.js App Router）按团队与生态定。

- **Router 核心卖点**：100% 类型推断（path/search params/context/导航全类型化）；**JSON-first 类型安全 search params**（URL 即 useState：自动 JSON 序列化、继承父路由、useSearch/Link/navigate、细粒度 selector）；file-based 与 code-based 路由**可混用**；内置 loader SWR 缓存（为 TanStack Query/SWR 等外部缓存设计）
- **Server Functions**：`createServerFn({ method }).validator(zodSchema).handler()`（单一 `data` 参数）；组件中 `useServerFn()`；redirect()/notFound() 抛出即达
- **安全红线**：server functions 是**同源 RPC**（Fetch Metadata/Origin/Referer 校验；无头请求默认拒绝）；**每个读写私有数据的 fn 自带 authMiddleware——beforeLoad 不是数据边界**（fn 是独立可达 endpoint）；读 session/identity 的 handler 用 `Cache-Control: public` = **跨租户泄漏**（认证用 `private` + `Vary: Cookie, Authorization`，敏感用 `no-store`）
- 机制：静态 import 安全（构建期换 RPC stub，服务端代码不进浏览器 bundle）；**勿动态 import server functions**；strict 序列化类型检查默认开；文件约定 `.functions.ts`（包装层）/`.server.ts`（仅服务端）/`.ts`（client-safe）
- 来源：[官方文档](https://tanstack.com/start/latest/docs/framework/react/overview) + [官方文档](https://tanstack.com/start/latest/docs/framework/react/guide/server-functions) + [官方文档](https://tanstack.com/router/latest/docs/framework/react/overview)

### 场景：UI 组件与动画生态（shadcn/ui / Base UI / motion）

推荐路径：业务 UI 主选 **shadcn/ui**（CLI 4.23.0）——它不是组件库而是**代码分发平台**：组件代码 copy 进项目（Open Code），用 `<motion>` 做动画（motion 14.14.0）。headless 定制场景备选 Base UI（1.0.0-rc.0，仍 RC）。

- **shadcn/ui 核心面**：`pnpm dlx shadcn@latest init -t next|vite|start|react-router|astro` 脚手架（Laravel 先 `laravel new`）；`shadcn add <component>` 拷组件；别名新模型 **Package Imports**（package.json `imports` 的 `#...` 私有别名替代 tsconfig paths，要求 TS ≥5 + `moduleResolution: "bundler"` + `resolvePackageJsonImports: true`；components.json aliases 同款 `#...` 根）；monorepo 中包内用 `#imports`、跨 workspace 用 package `exports`
- **AI Elements**（agentic 界面 23 pattern：Chat/Reasoning/Tool/Task/Inline Citation 等）：shadcn/ui 组件组合、copy 无包；结构约定 Chat=Message 列表 in Message Scroller、agent 步骤全构建于 **Trace**（同构 step）；chatbot 模板 Next.js + AI SDK（github.com/shadcn-ui/chatbot-template）；**elements.ai-sdk.dev（AI SDK Elements）已并入**——旧 agent.tsx/conversation.tsx 等有映射表，已 copy 代码继续可用
- **Base UI**：@base-ui-components/react 1.0.0-rc.0（MUI 团队，Radix 替代候选；React ^17-^19）——**RC 未 stable**，生产采用需评估
- **motion**：import 路径 **`motion/react`**（前身 framer-motion）；`animate`/`initial`/`exit`+AnimatePresence/手势五件套（whileHover/whileTap/whileFocus/whileDrag/whileInView）；独立 transform 轴（x/y/scale/rotate，硬件加速）；值类型转换（width/height 可动画到 `"auto"`，x/y 跨单位）；transition 默认智能（物理属性 spring、opacity/color duration）；Variants 编排（树传播 + `when`/`delayChildren: stagger()`）；路径动画 `transition.path: arc()`；MotionValue 作 motion 子节点直接渲染（零重渲染）；命令式 `useAnimate`；**布局动画 `layout` prop**（自动检测 size/position/reorder 并 transform 过渡，FLIP 且校正 scale 失真；跨元素共享 `layoutId`）；**scroll-linked：`useScroll()` → scrollYProgress 直接绑 style**（区别于 whileInView scroll-triggered）；**混合引擎**（WAAPI + ScrollTimeline 原生 120fps，需 spring 物理/可中断 keyframes/手势跟踪时回落 JS）；SVG 描边 `animate={{ pathLength: 1 }}`；`initial={false}` 禁用入场；**Motion AI kit `npx motion-ai`**（Motion skill + MCP 供 agent 搜文档）
- 来源：[官方文档](https://ui.shadcn.com/docs) + [官方文档](https://ui.shadcn.com/docs/ai-elements) + [官方文档](https://ui.shadcn.com/docs/package-imports) + [官方文档](https://motion.dev/docs/react-animation)

### 场景：富文本编辑器（TipTap 3）

推荐路径：主选 **TipTap 3.34.0**（@tiptap/react，ProseMirror 封装，headless + 100 扩展生态；React ^17-^19）。备选 Lexical 0.53.0（Meta，**仍 0.x**，生产关键路径慎入）。

```tsx
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";

const editor = useEditor({ extensions: [StarterKit], content: "<p>Hello</p>" });
return <EditorContent editor={editor} />;
```

- **v3 断裂面**（v2→v3 生成代码前必查）：UMD 移除（仅 ESM）；**`shouldRerenderOnTransaction` 默认 false**——编辑器组件不再因 transaction 自动重渲染（状态不同步首查此项）；tippy.js→floating-ui；**History→UndoRedo**（StarterKit 的 history 选项同改）；CollaborationCursor→CollaborationCaret；`getCharacterCount()` 移除→`storage.characterCount.characters()`；工具扩展（Placeholder/CharacterCount/DropCursor/Focus 等 8 个）迁至 **`@tiptap/extensions`** 包；NodeView `getPos()` 可返回 undefined（须判空）；setContent/clearContent 现正确 emit updates
- **v3 推荐写法**：Kit 化注册（TableKit/ListKit/TextStyleKit 一包注册）；**Static Renderer** 无编辑器实例渲染 JSON→HTML/Markdown/React（服务端/预览/RSS）；`unmount()` 复用实例（区别 destroy 全清）；MarkView 自定义 mark 渲染；SSR 可运行不渲染
- **React 集成面**：安装三件套 `@tiptap/react` + **`@tiptap/pm`（ProseMirror 依赖，必装）** + `@tiptap/starter-kit`；FloatingMenu/BubbleMenu 从 **`@tiptap/react/menus` 子路径**导入；`EditorContext.Provider` + `useCurrentEditor()` 跨组件取实例——**仅 EditorProvider 或手动 Provider 生效，裸 useEditor 不提供 context**（Provider value 须 useMemo）；`useEditorState({ editor, selector })` 选择器订阅（避免整组件随 transaction 重渲染）；**SSR（Next.js/流式）必须 `immediatelyRender: false`** 防服务端初始化 + `editor` null 前 return null；**React Composable API**（新）：声明式 `<Tiptap>` 组件 + 自动 context 管理 + 内建子组件，复杂多子组件 UI 适用
- **协作编辑（Collaboration + Yjs）**：`@tiptap/extension-collaboration` + `@tiptap/y-tiptap` + `yjs` + `y-protocols`——共享 Y.Doc 文档模型（非纯文本）；官方云 `TiptapCollabProvider`（`@tiptap-pro/provider` **私有 registry 须先配源**；`name` 文档标识/`appId` Document server ID/JWT token——on-premises 用 `baseUrl` 替代 appId；测试 JWT → 生产自签）。**两个必坑**：① 协作模式下 `content` 选项**每次加载重复添加**——移除 content 改 provider `onSynced` 回调 + `doc.getMap('config').set('initialContentLoaded', true)` 幂等守卫 + `editor.commands.setContent()` 一次性写入；② **协作 MUST `StarterKit.configure({ undoRedo: false })`**——协作扩展自管 history，默认 Undo/Redo 会 revert 他人修改
- 来源：[官方文档](https://tiptap.dev/docs/resources/whats-new) + [官方文档](https://tiptap.dev/docs/editor/getting-started/install/react) + [官方文档](https://tiptap.dev/docs/collaboration/getting-started/install)

### 场景：富文本编辑器备选（Lexical 0.53，Meta）

选型定位：TipTap 主选；**Lexical 0.53.0**（Meta 起家、社区维护；仍 0.x）为备选——Meta/Bloomberg/Payload CMS/Supabase/Proton Docs/MDXEditor 生产在用；**peer React >=18（无 17/16）**、TS >=5.2；全家桶 24+ 包**统一版本**（0.53.0，禁混版）。核心模型：不可变 editor state（非 DOM 为 source of truth）+ `$` 前缀函数只在 `editor.update()/read()` 回调内可用（类比 Hooks 规则）；新架构 **Extensions 体系**（`defineExtension({dependencies, name, namespace, theme})` 一处声明，无 nodes 列表/plugins 需同步）。

- **React 集成（新 Extensions 架构）**：安装 `lexical @lexical/react @lexical/extension @lexical/rich-text @lexical/history @lexical/clipboard @lexical/html`；`<LexicalExtensionComposer extension={appExtension}>` 单 root extension——**root extension MUST 定义在 module scope**（identity 稳定，换引用重建整个 editor）；内置 ContentEditable（`contentEditable={null}` 时自放布局）+ decorator 渲染 + error boundary + unmount 自动 dispose；错误默认 throw（onError 只挂 root extension）；`HMRExtension`（Vite HMR 保 editor state + history，`configExtension(HMRExtension, {hot: import.meta.hot ?? null})`，其他 bundler 省略）；纯文本场景换 `@lexical/plain-text` 的 PlainTextExtension
- **UI 与状态**：`useLexicalComposerContext()` 取 editor（`editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'bold')`）；响应式 UI 用 signals——`useExtensionSignalValue(HistoryExtension, 'canUndo')`；`<ExtensionComponent lexical:extension={TreeViewExtension} />` 渲染扩展 UI（注意 JSX 属性名 `lexical:extension`）；保存：`editor.read('latest', () => JSON.stringify(editor.getEditorState().toJSON()))`；初始内容 `$initialEditorState`（root extension 上）——**非受控**，勿把每次变更塞回 setEditorState
- **协作（Yjs）**：**Yjs 13 线 `@lexical/yjs` + `<CollaborationPlugin>`**；Yjs 14 新绑定 **`@lexical/y`**（YCollabExtension 形态）——**一个文档二选一，不能混用**；y-websocket 唯一官方支持 provider；三必坑：① 协作时 `editorState: null`——editor 不设任何默认状态由 collab plugin 接管；② **初始内容 MUST 服务端 bootstrap**（两客户端同时初始化可致文档损坏，headless `withHeadlessCollaborationEditor`）；③ **换文档必须 remount editor**（LexicalComposer 加 `key`）——运行时改 rootName/getXmlText 无效，只换 plugin 不够（旧内容写入新 root）；多编辑器共享一 Y.Doc 用 `rootName` 或 `getXmlText`（后者优先）+ **每编辑器独立 id**（id 键文档 map 与光标 registry，同 id 互相覆盖）
- **自定义节点属性同步坑**：@lexical/yjs 靠构造器新建实例检查 own enumerable properties——**每个要同步的属性 MUST 在 constructor 显式赋值**（即使 undefined）；TS `foo?: Type` 可选语法不保证 own property（target < ES2022 无 useDefineForClassFields 不产生初始化代码）；用 NodeState 则不受此影响
- headless/测试：`@lexical/headless`（配 happy-dom）；无 root element 不做 DOM 工作，同代码可跑服务端/测试
- 来源：[官方文档](https://lexical.dev/docs/intro) + [官方文档](https://lexical.dev/docs/getting-started/react) + [官方文档](https://lexical.dev/docs/collaboration/react)

### 场景：数据可视化（Recharts 3）

推荐路径：**recharts 3.10.1**（React 16.8-19 全线；Node ≥18；D3 子模块 + 内部 Redux 状态体系；UMD 可用）。

- **v3 断裂面（v2 代码迁移前必查）**：**`<Cell>` 弃用（4.0 移除）**——改各组件 `shape` prop（类型 `PieSectorShapeProps`/`BarShapeProps`/`ScatterShapeProps`；内部形状 Sector/Rectangle/Symbols 导出可用）；**`activeIndex` prop 已移除**——Tooltip 接管交互（`defaultIndex`/`active`/`trigger="click"`/`content={() => null}`/`cursor={false}`；Bar `activeBar`、Pie `activeShape`）
- **响应式（3.3+）**：`<LineChart responsive>` 随父容器自动重排 + CSS `style={{width:'100%', maxWidth, aspectRatio}}`；**<3.3 旧写法**：`<ResponsiveContainer width="100%">` 包裹（父容器 MUST 有确定尺寸）；无 width/height 不渲染
- 新 API：`YAxis width="auto"`、`Legend position="insideTopRight"`（取代 align/verticalAlign）、`@recharts/devtools` 的 `<RechartsDevtools />`（hook inspector，可选）
- **性能**：①隔离频繁变化组件（root state 变化全图重渲染）②**dataKey 引用稳定**——函数式 dataKey 每渲染新引用=全点重算，优先字符串 dataKey，函数用组件外定义/useCallback ③大数据集聚合采样（d3.bin）④鼠标事件 throttle ~50ms
- 来源：[官方文档](https://recharts.github.io/en-US/guide/getting-started) + [官方文档](https://recharts.github.io/en-US/guide/cell) + [官方文档](https://recharts.github.io/en-US/guide/activeIndex) + [官方文档](https://recharts.github.io/en-US/guide/sizes) + [官方文档](https://recharts.github.io/en-US/guide/performance)

### 场景：拖拽（dnd-kit 新旧双线）

选型：先 `npm ls @dnd-kit/react @dnd-kit/core` 确认版本线——**双线 API 完全不兼容**：

- **新线（Latest）`@dnd-kit/react` 0.5.3**（2026-10-31 活跃；peer React 18/19；框架无关核心 @dnd-kit/dom，React 薄层）：`useDraggable({id})` 返回 **{ref}** 直接挂（**无 listeners/attributes spread**）；`DragDropProvider` 取代 DndContext；`onDragEnd` 读 **event.operation.target?.id**（旧线 event.over 已不存在）+ event.canceled；sortable 另装 @dnd-kit/helpers 用 `move`；DragOverlay（dropAnimation 可配）；v0.5 disabled 对象形式 {draggable, droppable}
- **旧线（Legacy）`@dnd-kit/core` 6.3.1 + sortable 10.0.0**（**2024-12 停更、官方标记 Legacy，新项目勿选**；存量项目仍是训练记忆主流）：DndContext + `useDraggable` 返回 {attributes, listeners, setNodeRef, transform}——MUST `{...listeners} {...attributes}` spread + setNodeRef 挂 ref + transform 转 translate3d（`CSS.Translate.toString` from @dnd-kit/utilities）；跨容器用 DragOverlay；@dnd-kit/sortable 的 useSortable + SortableContext + arrayMove
- 新线细节：PointerSensor `PointerActivationConstraints.Delay/Distance`、preventActivation（交互元素阻止激活）、跨同源 iframe 支持；Accessibility plugin + prefers-reduced-motion 全动画尊重；迁移指南 docs.dndkit.com/react/guides/migration
- 来源：[官方文档](https://docs.dndkit.com/react/quickstart) + [官方文档](https://docs.dndkit.com/changelog) + [官方文档](https://docs.dndkit.com/legacy/introduction/getting-started)

### 场景：日期与时间（date-fns 4 / Temporal）

选型：**date-fns 4.4.0**（200+ 纯函数、不可变、100% TS；v5 alpha）为主流；Temporal（TC39 Stage 3）用 **@js-temporal/polyfill 0.5.1** 预研——polyfill **不装 global Temporal**（`import { Temporal } from "@js-temporal/polyfill"`）。

- **v4 = 一等时区，breaking 极少**：ESM-first（`"type": "module"`，.mjs→**.cjs** 反转）；第三方 date-fns-tz 被 **@date-fns/tz（TZDate）** 取代——Date 扩展，全部 date-fns 函数直接兼容
- **归一化规则（v4 核心）**：结果归一到**第一个对象参数的时区**——参数顺序影响结果（`differenceInBusinessDays(laterSG, earlierNY)`=262 / 反序=-261）；显式指定用 context option `{ in: tz("America/Los_Angeles") }`
- **坑：`new TZDate("Asia/Singapore")` 是 Invalid Date**（被当日期字符串）——用静态 `TZDate.tz("Asia/Singapore")`；TZDateMini（761B）无 formatter，内部用 Mini；只要 UTC 用 @date-fns/utc（UTCDateMini 239B）；Hermes 需 Format.JS polyfills
- v5 路线：durations、global locales、Intl 默认 format、**Interim API（Temporal 子集过渡实验）**
- 来源：[官方文档](https://blog.date-fns.org/v40-with-time-zone-support/) + [官方文档](https://github.com/js-temporal/temporal-polyfill)

### 场景：错误兜底

推荐路径：渲染期错误用错误边界（19+ 函数式 `<ErrorBoundary onError/onReset/fallback>`）[RC-8]；事件回调和异步 await 自带 try/catch；全局兜底 `window.onerror`。
- 来源：[官方文档](https://react.dev/reference/react/Component#static-getderivedstatefromerror) + [模型经验]

### 场景：React 19 原生 form actions 与并发原语

**form action 语义**（react.dev/reference/react-dom/components/form，2026-11-17 锚定）：`<form action={fn}>` 在 Transition 中运行 action（可 async、单参 FormData）；成功后自动 reset 非受控字段；action 为函数时 method 被忽略恒 POST；onSubmit 先跑（除非 preventDefault）；formAction 覆盖 form 级 action；JS 加载前显示错误须三条件：Client Component + Server Function + useActionState。

- **useActionState 全语义**：`(state, dispatchAction, isPending) = useActionState(action, initialState, permalink?)`；reducerAction 可 async+副作用（vs useReducer 必须纯）；多次 dispatch **排队串行**、每次收上次返回值为 previousState（设计意图）；**StrictMode 下 action 不双调用**；已知错误 return state、未知错误 throw（取消所有排队 → Error Boundary）；abort 可取消排队 action；render 期间调 dispatchAction 报错；校验错误保留值模式：`return { error, submitted: formData }` + `defaultValue={state.submitted?.get('name') ?? ''}`，成功返回 `submitted: null` 自动清空
- **传额外数据 3 法**：hidden field（进 FormData，渐进增强）/ `.bind()`（保类型、值须可序列化、JS 加载前可提交；bind 后参数序 `productId, previousState, formData`）/ 组件内函数（仅 JS 加载后）
- **多提交类型**：按钮级 `formAction` + `dispatchFormState({ type, data })` 区分
- **useSyncExternalStore**：getSnapshot 必须缓存 [RC-12]；getServerSnapshot 仅 SSR+hydration；subscribe 每渲染变 → 重订阅；Transition 期间 store 变更二次校验不同则重启 blocking update；**不建议基于其值 suspend**（外部 store 变更不能标记非阻塞 → 触发 Suspense fallback 替换已渲染内容）；能用 useState/useReducer 就别用
- **StrictMode**：四类开发检查（额外重渲染/Effect 重跑/ref callback 重跑/弃用 API），无 opt-out——整树强制或下移 StrictMode 位置；仅 dev，生产零开销
- 来源：[官方文档](https://react.dev/reference/react/useActionState) + [官方文档](https://react.dev/reference/react/useSyncExternalStore) + [官方文档](https://react.dev/reference/react/StrictMode)

### 场景：Context 深水（createContext / useContext / Provider）

- **心智模型**：`createContext(defaultValue)` 组件外调用；context 对象**本身不持有信息**——上层 `<SomeContext value={...}>` 提供、下层 `useContext(SomeContext)` 读取最近 provider 的 value；无 provider 才用 defaultValue（静态"最后手段"兜底，永不变化，无意义传 null）
- **React 19 provider 写法**：直接 `<SomeContext value={...}>`；`.Provider` 是 19 前旧写法；`.Consumer` render-props 更旧——新代码一律 `useContext`
- **provider 漏 value 陷阱**：不传 `value` = `value={undefined}`——**不回落 defaultValue**（默认值只在完全没有 provider 时生效）；prop 名拼错同理（控制台有警告）
- **重渲染语义 [RC-14]**：value 变化（`Object.is` 比较）自动重渲染所有消费该 context 的后代；**`memo` 不能阻止子组件接收新 context 值**；优化：`useMemo(() => ({ currentUser, login }), [...])` + 函数成员 `useCallback`
- **同组件陷阱**：`useContext()` 不受同一组件返回的 provider 影响——provider 必须在调用者**上方**
- **重复模块陷阱**：symlink/重复打包使提供方与读取方的 context 对象非 `===` 同一对象 → 传值失效；验证：两边挂 `window` 比较；修构建层去重
- **覆盖与累积**：嵌套同名 provider 覆盖内层子树；可"累积"信息（LevelContext 逐层 +1 的自动标题层级模式）
- **扩展模式**：context + reducer 拆两个 context（state / dispatch 各一），配自定义 hooks（`useTasks`/`useTasksDispatch`）收拢；根部 context "金字塔"可提取 `MyProviders` 组件收拢（state 仍归外层所有）
- **默认值设计**：有意义默认值让组件脱离 provider 不崩、测试免搭 provider 栈
- 来源：[官方文档](https://react.dev/reference/react/createContext) + [官方文档](https://react.dev/reference/react/useContext)

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | effect 里 state 永远是旧值（静默） | 闭包捕获定义时快照，依赖缺失 | 依赖写全 [RC-1]；函数式更新 [RC-9]；19.2+ 用 useEffectEvent 剥离事件逻辑 |
| 2 | `Rendered fewer hooks than expected` | 条件/循环中调用 hooks | hooks 移到顶层 [RC-1] |
| 3 | 控制台警告；异步清理不执行 | `useEffect(async)` 返回 Promise 被当 cleanup | effect 内 IIFE [RC-5] |
| 4 | 快速切换 id 显示旧数据 | 请求无序返回最后 setState 赢 | ignore/AbortController [RC-6] |
| 5 | 删插列表项后输入框串行 | `key={index}` 身份漂移 | 稳定业务 id [RC-3] |
| 6 | 两份真相偶发不同步 | 派生状态存 state | 渲染时计算 [RC-2] |
| 7 | Provider 变化全树卡顿 | Context 无选择器，value 引用变化全通知 | 拆 context/useMemo [RC-7] |
| 8 | `setCount(count+1)` 后打印旧值 | setState 异步批处理 | 函数式更新 [RC-9] |
| 9 | 异步抛错白屏，错误边界没接住 | 边界只捕渲染期错误 | 异步自带 try/catch [RC-8] |
| 10 | Activity 隐藏后 video/audio/iframe 继续播放 | DOM 未销毁，display:none 不停媒体 | `useLayoutEffect` cleanup 暂停（勿用 useEffect） |
| 11 | "can only be called from Effects" lint 报错 | useEffectEvent 渲染期调用/事件处理器中调用/传给子组件 | 仅 effect/其他 Effect Event 内调用；通用回调用普通函数/useCallback |
| 12 | Compiler 项目删手写 memo 后性能回归 | 删除改变编译输出 | 存量 memo 保留或删前充分测试；新代码依赖编译器 |
| 13 | motion 升级后 `framer-motion` import 混乱 / 新文档 API 找不到 | motion 14 起 import 统一 **`motion/react`**（前身 framer-motion） | 新代码 `import { motion } from "motion/react"`；老 import 升级时全量替换；stagger 等新 API 从 motion/react 导入 |
| 14 | "The result of getSnapshot should be cached" + 无限循环 | getSnapshot 每次返回新引用 | store 侧缓存快照 / getSnapshot 返回缓存值 [RC-12] |
| 15 | dev 报 "An async function with useActionState was called outside of a transition" | dispatchAction 在 Action 之外调用 | 仅在 action/form action 内调用 |
| 16 | action 内 await 后 setState 丢 pending / 不批处理 | await 后已处于 Transition 之外 | 再包 `startTransition(() => setTitle(...))` [RC-13] |
| 17 | useSyncExternalStore 值 suspend 后 fallback 闪替已渲染内容 | 外部 store 变更不能标记非阻塞更新 | 官方建议：能 useState/useReducer 就别用；勿基于其值 suspend |
| 18 | useContext 总返回 undefined/旧值 | provider 在调用组件同层或下方；或 provider 漏 value/prop 名拼错（显式 undefined 不回落默认值） | provider 移到调用者上方；value 必传 |
| 19 | 消费子树随父组件每次渲染整体重渲染 | provider value 内联对象/函数每次新引用 | useMemo 包对象 + useCallback 函数成员 [RC-14] |
| 20 | 同一 context 跨模块"失联"（一处提供一处读不到） | 构建产物重复模块（symlink），两边 context 对象非 === | 修构建去重；window 比较验证 |
| 21 | memo 过的子组件仍在 context 变化时重渲染 | memo 不能阻止 context 更新传播 | 拆 context / 消费者下移 [RC-14] |

**Top 展开：坑点 1（stale closure）**

```tsx
// 错误：count 永远是 0（捕获首次渲染快照）
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, []);

// 正确：函数式更新，不依赖外部 count
useEffect(() => {
  const id = setInterval(() => setCount(c => c + 1), 1000);
  return () => clearInterval(id);
}, []);
```

## API 速查表

| API | 签名要点 | 易错点 |
|---|---|---|
| useState | `[s, setS] = useState(init)` | 对象更新展开；函数初始值 `useState(() => fn())` |
| useEffect | `useEffect(fn, deps?)` | 返回值只能是 cleanup；deps 比较 `Object.is` |
| useEffectEvent（19.2+） | 读最新值且不进依赖数组 | **只能 effect/Effect Event 内调用**；身份故意不稳定（防误依赖）；勿用于回避依赖 |
| `<Activity mode>`（19.2） | visible/hidden 隐藏保留 state+DOM，销毁 Effects | 预渲染 `mode="hidden"` 只预取 Suspense 激活源数据；hidden 纯文本组件无输出 |
| useRef | `{ current }` 可变容器 | 改 `.current` **不触发重渲染** |
| useCallback / useMemo | 缓存函数/值引用 | Compiler 项目为冗余 |
| useTransition / useDeferredValue | 非紧急更新 / 延迟昂贵重算 | 输入保持响应 |
| use()（19+） | `use(promise)`/`use(context)` | promise 引用必须稳定 |
| useOptimistic（19+） | action 完成后自动回退 | 配 Server Actions |
| `<ErrorBoundary>`（19+） | `onError/onReset/fallback` | 只捕渲染期 [RC-8] |
| forwardRef | 19 起可省，ref 直接作 prop | ref prop 类型 `Ref<HTMLDivElement>` |
| `<ViewTransition>`（19.3 stable） | enter/exit/update/share 四类动画 | 仅 Transition 更新触发；React 自动调 startViewTransition 勿手调；动画期间新更新排队合并（A→B 中来 C/D → 下段 B→D）；配 Suspense 用 `update="auto" default="none"` |
| `addTransitionType`（19.3） | startTransition 内标注转换成因选动画 | 轮播前进/后退方向动画 |
| Fragment Refs（19.3） | `<Fragment ref>` → FragmentInstance 群组操作子树 | observeUsing/focus/getClientRects；无 wrapper div |
- `use(browser())`（19.3） | SSR 退出：服务端 suspend、客户端不 | 可条件调用；`initialData` 有则参与 SSR |
| shadcn CLI | `shadcn init -t <framework>` / `shadcn add <name>`（**4.23.0**，Node ≥20.18.1） | 代码分发非 npm 组件库；别名用 package imports `#...`（非 tsconfig paths）；模板 next/vite/start/react-router/astro |
| motion | `import { motion } from "motion/react"`（**14.14.0**，前身 framer-motion） | exit 动画须配 AnimatePresence；height: "auto" 可动画；MotionValue 子节点零重渲染；Variants 沿树传播 |
| @base-ui-components/react | headless unstyled 组件（**1.0.0-rc.0**，React ^17-^19） | 仍 RC 未 stable，生产慎入 |
| `<form action>`（19） | action={fn}，fn 收单参 FormData | 恒 POST 忽略 method；成功自动 reset 非受控字段；formAction 覆盖；JS 前报错须 useActionState+Server Function |
| useActionState（19） | `(state, dispatchAction, isPending) = useActionState(action, initState, permalink?)` | dispatchAction 仅 Action 内调用；排队串行；已知错误 return/未知 throw [RC-13]；StrictMode 不双调用 |
| useSyncExternalStore | `(snapshot, subscribe, getServerSnapshot?)` | getSnapshot 必须缓存 [RC-12]；不建议基于其值 suspend |
| createContext | `createContext(defaultValue)`，组件外调用 | default 静态兜底仅无 provider 时用；React 19 起 `<Ctx>` 直接作 provider；`.Consumer` 旧 API |
| useContext | `const value = useContext(SomeContext)` | 读上方最近 provider；memo 不能阻止其更新 [RC-14]；symlink 重复模块破坏 |

## 版本注意

- 当前最新：**React 19.3**（2026-09-09）[官方文档](https://react.dev/blog)
- 19.2（2025-10-01）：`useEffectEvent` 转正、`<Activity>`（隐藏保留状态）、Performance Tracks、`cacheSignal`
- 19.3：`<ViewTransition>`、Fragment Refs、`browser()` + `use(browser())`（SSR 分支）、Trusted Types、Context 可在 RSC 直接渲染
- React Compiler v1.0 稳定（2025-10-07）；React 17/18 项目须另装 `react-compiler-runtime`（19 零配置）；与 swc/oxc 团队合作开发一等支持（当前 Babel plugin 为核心包装）[官方文档](https://react.dev/blog)
- **安全警报**：RSC 存在未认证 RCE + DoS/源码暴露漏洞（2025-12 披露）——SSR/RSC 项目 React 必须 **≥19.2.1**（修复版 19.0.1/19.1.2/19.2.1）[官方文档](https://react.dev/blog)
- React Foundation 成立（2026-02，Linux Foundation 托管）[官方文档](https://react.dev/blog)
- CRA 已弃用（2025-02）；新项目用 Vite / Next.js / Remix
- 18 → 19：`createRoot` 替代 `ReactDOM.render`；forwardRef 可省
- **生态版本锚定**（npm registry，2026-11-15/16）：**zustand 5.1.0**（React ≥18，immer 可选 peer）；**@reduxjs/toolkit 2.14.0**（内置 redux 5/immer 11/reselect 5/redux-t
- **UI 组件生态锚定**（2026-11-16）：**shadcn CLI 4.23.0**（代码分发平台；Package Imports `#...` 别名模型）；**@base-ui-components/react 1.0.0-rc.0**（headless，仍 RC）；**motion 14.14.0**（前身 framer-motion，import `motion/react`）hunk 3——选 Redux 即选 RTK，不裸装 redux）；**react-hook-form 7.92.0**（peer React 16.8-19，Node ≥18；**v8 未 stable：beta=8.0.0-beta.0 + alpha=8.0.0-alpha.5 双通道活跃推进**，官方迁移指南就绪，为 v7 项目生成勿用 v8 API）；**@hookform/resolvers 7.0.6**（peer RHF ^7.55；zod ^3.25||^4 双线；@standard-schema/spec ^1.0 入 peer；支持 20+ 校验库）；**zod 4.6.7（v4 大版本，`zod/v3` 兼容入口并存；`zod/mini` 树摇变体核心 1.88kb）**——生成校验代码前确认项目 zod 大版本；**swr 2.5.1**（peer React 16.11-19；`swr/infinite`、`swr/mutation` 多入口；react-server 条件导出）；**@mui/material 9.5.0（v9，2026-04-08 官宣——无 v8，v7 直跳 v9 对齐 MUI X；新组件 NumberField/Menubar；弃用 `component`/`componentsProps` 全移除改 slots、布局组件 system props 移除；sx 性能 +30%；下大版本方向：移除 Emotion + Tailwind 集成，**v10 alpha 已启（next=10.0.0-alpha.0）**）**——生成 MUI 代码前确认项目大版本（v9 移除项详见官方迁移指南）；**@emotion/react 11.14.0 / @emotion/styled 11.14.1**（v11 线）；**@tanstack/react-table 9.3.1（v9：`useTable({ features, columns, data })` 按需注册特性、tree-shake、TanStack Store 驱动状态——v8 `useReactTable` 时代结束）**；**motion 14.14.0 = framer-motion 14.14.0**（改名完成，motion 为主包名，peer React ^18/^19）；**recharts 3.10.1（v3 线：Cell 弃用→shape、activeIndex 移除→Tooltip、responsive prop 3.3+ 取代 ResponsiveContainer；peer react-is；内部 Redux/es-toolkit/victory-vendor）**；**dnd-kit 双线：新 @dnd-kit/react 0.5.3（2026-10 活跃、ref API、event.operation.target）/ 旧 @dnd-kit/core 6.3.1+sortable 10.0.0（2024-12 停更标记 Legacy、listeners spread API、event.over）——API 完全不兼容**

## 与其他子领域的集成要点

- **Next.js**：App Router 组件默认 RSC；`use()`/`useOptimistic`/`useActionState` 与 Server Actions 配合 → `kb/nextjs.md`
- **TanStack Query**：状态选型第 5 层（[RC-10]）→ `kb/tanstack-query.md`
- **react-admin**：表单层即 react-hook-form；context 渲染语义直接适用 → `kb/react-admin.md`
- **NestJS**：SSR 集成时 hydrateRoot 版本对齐 → `kb/nestjs.md`

## 来源索引

- React 官方博客（19.2/19.3/Compiler v1.0）：https://react.dev/blog [官方文档]
- **XState v5（actor model/createMachine-createActor/包矩阵）**：https://stately.ai/docs/xstate [官方文档]
- **@xstate/react（useMachine/useActorRef/useSelector/createActorContext/provide）**：https://stately.ai/docs/xstate-react [官方文档]
- React 19.3 发布文（ViewTransition/addTransitionType/Fragment Refs/browser()/Trusted Types/RSC 渲染 Context）：https://react.dev/blog/2026/09/09/react-19-3 [官方文档]
- hooks 规则：https://react.dev/reference/react/hooks [官方文档]
- `<Activity>` reference（hidden 销毁 Effects/预渲染/Selective Hydration/DOM 副作用坑）：https://react.dev/reference/react/Activity [官方文档]
- useEffectEvent reference（调用范围/身份故意不稳定/报错速查）：https://react.dev/reference/react/useEffectEvent [官方文档]
- React Compiler introduction（自动 memo 化定位/手写 memo 隐蔽 bug/swc-oxc 路线）：https://react.dev/learn/react-compiler/introduction [官方文档]
- React Compiler configuration + directives（compilationMode/panicThreshold/target/runtime 包/gating/use no memo）：https://react.dev/reference/react-compiler/configuration + https://react.dev/reference/react-compiler/directives [官方文档]
- API 索引（useEffectEvent 确认）：https://react.dev/reference/react [官方文档]
- shadcn/ui Introduction（代码分发平台定位/Open Code/Composition/Distribution 五原则）：https://ui.shadcn.com/docs [官方文档]
- shadcn/ui Installation（init -t 模板/shadcn create/框架支持）：https://ui.shadcn.com/docs/installation [官方文档]
- shadcn/ui AI Elements（23 agentic pattern/Trace 同构/AI SDK Elements 并入迁移映射/chatbot 模板）：https://ui.shadcn.com/docs/ai-elements [官方文档]
- shadcn/ui Package Imports（package.json imports `#...` 别名/monorepo 分工）：https://ui.shadcn.com/docs/package-imports [官方文档]
- Motion React animation（motion/react import/animate-exit-gestures/Variants/useAnimate/MotionValue 子节点）：https://motion.dev/docs/react-animation [官方文档]
- TipTap What's new in V3（UMD 移除/shouldRerenderOnTransaction/UndoRedo 改名/@tiptap/extensions 包/Static Renderer）：https://tiptap.dev/docs/resources/whats-new [官方文档]
- 甩掉不必要 effect：https://react.dev/learn/you-might-not-need-an-effect [官方文档]
- RHF useForm API（mode/values/resetOptions/formState 订阅/validate-resolver 互斥）：https://react-hook-form.com/docs/useform [官方文档]
- RHF v8 迁移指南（beta，id→key/watch callback 移除/Compiler）：https://react-hook-form.com/migrate-v7-to-v8 [官方文档]
- zod v4 发布说明（性能/Mini/JSON Schema/顶层格式/error 统一）：https://zod.dev/v4 [官方文档]
- zod v4 迁移指南（error 参数/顶层格式 API/z.record 双参/.default 短路/any-unknown 键必填/z.function 重构/treeifyError）：https://zod.dev/v4/changelog [官方文档]
- zod 4.6 发布文（.validate() 35x/z.withParser() CSP/@zod/mini 独立包/safeParse 懒错误构建/z.iban）：https://zod.dev/blog/zod-4-6 [官方文档]
- zod AOT 编译（z.compile 快路径/派生后编译/全局 import zod/compile/不支持面/strict 验证/jitless/体积代价）：https://zod.dev/compile [官方文档]
- React Router 框架模式（routes.ts 助手/+types 类型推断/Route Module 导出面/框架模式自动重验证）：https://reactrouter.com/start/framework/routing + https://reactrouter.com/start/framework/route-module [官方文档]
- React Router changelog（v8.0.0 断裂面：Node ≥22.22/React ≥19.2.7/react-router-dom 移除/middleware 恒开/ESM-only；8.5 View Transition 弃用）：https://reactrouter.com/changelog [官方文档]
- zustand persist/useShallow（middleware 选项/深合并/SSR）：https://zustand.docs.pmnd.rs/reference/middlewares/persist [官方文档]
- RTK Query（tagTypes 失效/fixedCacheKey/Standard Schema 校验）：https://redux-toolkit.js.org/rtk-query/usage/mutations [官方文档]
- tRPC 官方文档（procedure/工厂模式客户端/errorFormatter 安全/base procedures）：https://trpc.io/docs/client/tanstack-react-query/setup [官方文档]
- MUI v9 发布公告与迁移指南（v7→v9 跳版/component/componentsProps 移除/sx +30%）：https://mui.com/material-ui/migration/upgrade-to-v9/ [官方文档]
- TanStack Table v9 React 概览（useTable/features 按需注册/TanStack Store）：https://tanstack.com/table/latest/docs/framework/react/overview [官方文档]
- **Recharts 官方文档站（recharts.github.io；Getting Started/Cell 弃用与 shape 迁移/activeIndex 移除与 Tooltip 接管/resizes 与 responsive prop/performance/dataKey 引用稳定）**：https://recharts.github.io/en-US/guide [官方文档]
- **dnd-kit 官方文档（docs.dndkit.com；React Quickstart/Changelog v0.1-0.5/Legacy Getting Started）**：https://docs.dndkit.com/react/quickstart [官方文档]
- **form reference（action Transition 语义/自动 reset/formAction/bind 参数序/JS 前错误三条件/保留值 4 法/dispatchFormState）**：https://react.dev/reference/react-dom/components/form [官方文档]
- **useActionState reference（排队串行/permalink 渐进增强/dispatchAction 限 Action 内/已知错误 return·未知 throw/StrictMode 不双调/校验保留值模式/abort 取消排队）**：https://react.dev/reference/react/useActionState [官方文档]
- **useSyncExternalStore reference（getSnapshot 缓存红线/getServerSnapshot 仅 SSR+hydration/Transition 二次校验/不建议 suspend）**：https://react.dev/reference/react/useSyncExternalStore [官方文档]
- **StrictMode reference（四类开发检查/无 opt-out/树位置决定范围/仅 dev）**：https://react.dev/reference/react/StrictMode [官方文档]
- **createContext reference（context 对象不持有信息/19 `<SomeContext>` 直接 provider/.Consumer 旧法/default 静态兜底/provider 漏 value=undefined）**：https://react.dev/reference/react/createContext [官方文档]
- **useContext reference（最近 provider/Object.is 比较/memo 不能阻断 context 更新/symlink 重复模块===要求/useCallback+useMemo 优化/嵌套覆盖/默认值利于测试）**：https://react.dev/reference/react/useContext [官方文档]
- **date-fns v4 发布文（TZDate/归一化到第一参数时区/context in 选项/ESM-first/v5 路线与 Interim API）**：https://blog.date-fns.org/v40-with-time-zone-support/ [官方文档]
- [模型经验]：坑点 4/7/9 故障模式、状态选型路径、react-hook-form 要点、Compiler 认知校正——适用 React 16.8+ 与版本解耦
- npm registry（zustand 5.1.0 / @reduxjs/toolkit 2.14.0 / react-hook-form 7.92.0 / zod 4.6.7 版本锚定）：https://registry.npmjs.org [官方文档]
- 法则条款来源：corpus/react/react-core/elicited/11-laws.md（法则化萃取）

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| React 印象停留在 19.0/19.1 | 19.3（2026-09） | 采用文档：锚定 19.3 |
| CRA 是默认脚手架 | CRA 已弃用（2025-02） | 采用文档 |
| useEffectEvent 可用性存疑 | 19.2 正式 API（2025-10-01） | 转正入速查表 |
| 手写 memo 是最佳实践 | Compiler v1.0 稳定后启用项目里为冗余 | 按 Compiler 启用与否区分建议 |
| RHF watch(callback)/field.id 长期可用 | v8 beta 已移除/改名（subscribe/key 替代） | 采用文档：v7 生成代码避免 v8 弃用 API |
| zod 错误定制用 message/errorMap | v4 统一为 error 参数（旧版弃用） | 采用文档：v4 项目一律 error 参数 |
| z.record 单参/z.object any 键可用 | v4 双参强制；any-unknown 键 4.4+ parse 时必填 | 采用文档：双参 + 缺键须显式 .optional() |
| .default() 是 parse 默认值 | v4 短路语义，默认值须匹配 output 类型（旧行为 .prefault()） | 采用文档：v4 语义为准 |
| useEffectEvent 可作通用 latest-value 回调 | 官方限定：仅 effect/Effect Event 内调用，不可渲染期调用/传子组件（linter 强制） | 采用文档限定：通用回调用普通函数/useCallback |
| Activity hidden 只是 CSS 隐藏（或只是卸载） | hidden 销毁 Effects（订阅清理）但保留 state+DOM——媒体元素副作用存活 | 采用文档：hidden=概念 unmount+state 保存；DOM 副作用须 useLayoutEffect cleanup |
| useActionState 多次 dispatch 后到先得/最后赢 | 官方排队串行，每次 action 收上次返回值为 previousState | 采用文档：按串行语义设计 action（每次 return 决定下一步输入） |
| StrictMode 下 action/reducerAction 双调用担忧 | 官方明确不双调用（action 非渲染期纯函数调用） | 采用文档：action 内副作用无须双调防护；Effect 内副作用仍须幂等 |
| 依赖 memo(Child) 阻断 context 更新传播 | memo 不能阻止子组件接收新 context 值 | 采用文档 [RC-14]：useMemo/useCallback 稳定 value 引用、拆 context |
| provider 显式 undefined 可回落默认值 | undefined 即值本身；默认值只在完全没有 provider 时生效 | 采用文档：value 必传 |
