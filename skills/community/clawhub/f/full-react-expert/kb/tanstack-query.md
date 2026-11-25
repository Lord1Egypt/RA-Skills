---
subdomain: tanstack-query
version: 17
updated: 2026-11-17
---
# TanStack Query

## 定位与心智模型

TanStack Query（当前 **5.107.1**，npm 锚定 2026-11-15）是**服务端状态**管理库：获取、缓存、同步、更新服务器数据 [官方文档](https://tanstack.com/query/latest/docs/framework/react/overview)。心智模型一句话：**把"异步服务端数据"当作带过期语义的缓存管理**，而不是当作"发请求的 hook"。

默认行为五件套（无需配置）：stale-while-revalidate、窗口聚焦重取、同 key 并发去重、自动 GC、Devtools。理解两条主线即可覆盖大部分问题：**queryKey 结构 = 缓存键结构**（数组层级序列化比较）、**staleTime（多久算旧）vs gcTime（多久回收）**。

## 法则

[TQ-1] **MUST**: v5 必须对象语法 `useQuery({ queryKey, queryFn })`。
- 违反后果: v4 位置参数在 v5 类型报错/运行时错乱。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/overview)

[TQ-2] **MUST**: queryFn 对非 2xx 必须显式 throw（全局宪法 LAW-8 契约层错误显式抛出）。
- 违反后果: error 永远 null，"成功但空数据"静默故障。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/overview)

[TQ-3] **NEVER**: mutation 不得默认加 retry（写操作非幂等）。
- 违反后果: 超时自动重试 = 重复创建订单。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/overview)（mutation 默认语义）

[TQ-4] **MUST**: queryKey 用可序列化结构化数组（层级 = 失效粒度），不塞不稳定引用。
- 违反后果: 缓存永不命中或失效粒度失控。
- 溯源: [模型经验]

[TQ-5] **MUST**: SSR 环境的 QueryClient 必须每请求工厂创建（浏览器端可单例缓存）（全局宪法 LAW-3）。
- 违反后果: 模块级单例跨请求/跨用户数据泄漏。
- 溯源: [模型经验]（框架 SSR 官方模式为工厂）

[TQ-6] **MUST**: 乐观更新三步缺一不可：onMutate 快照+cancelQueries → onError 回滚 → onSettled 失效。
- 违反后果: 漏 cancelQueries 回滚被在途请求覆盖；漏回滚 UI 停在假状态。
- 溯源: [模型经验]

[TQ-7] **MUST**: staleTime（过期策略）与 gcTime（回收策略）分开决策，不得混调。
- 违反后果: 调错对象——重取不减少或缓存提前蒸发。
- 溯源: [模型经验]

[TQ-8] **MUST**: isPending（无缓存数据）与 isFetching（请求中）按 UI 语义选用；v5 isLoading = isPending && isFetching。
- 违反后果: 骨架屏该显示时不显示；按钮该禁用时没禁。
- 溯源: [模型经验]

[TQ-9] **NEVER**: RSC 页面数据不得再包一层 useQuery 双轨缓存。
- 违反后果: 两套真相各失效各的，状态漂移。
- 溯源: [模型经验]

[TQ-10] **MUST**: mutation 后以 invalidateQueries（前缀匹配）同步真值，不得只 setQueryData 了事。
- 违反后果: 本地写入与服务端真值脱节。
- 溯源: [模型经验]

[TQ-11] **MUST**: 同组件多个 Suspense 查询须用 useSuspenseQueries 并行，不得罗列多个 useSuspenseQuery。
- 违反后果: 逐个 suspend 串行请求瀑布。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/reference/useSuspenseQuery)

[TQ-12] **MUST**: 缓存持久化 gcTime 必须 ≥ maxAge；React 侧必须用 PersistQueryClientProvider，禁止模块级调用 persistQueryClient。
- 违反后果: 缓存先被 GC 持久化提前失效；模块级订阅永不释放 + 恢复竞态。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/plugins/persistQueryClient)

[TQ-13] **MUST**: tRPC 项目的查询选项与缓存键必须用 trpc 工厂（`queryOptions()`/`mutationOptions()`/`queryFilter()`/`pathFilter()`），NEVER 手写 queryKey。
- 违反后果: 手写 key 的查询能跑但与 tRPC 键体系脱钩——失效过滤与服务端预取数据永不匹配。
- 溯源: [官方文档](https://trpc.io/docs/client/tanstack-react-query/setup)

[TQ-14] **MUST**: Apollo Client 4 的 React API 必须从 `@apollo/client/react` 导入，NEVER 从核心入口导入；判错误类型用 `CombinedGraphQLErrors.is()` 等判型方法（`ApolloError` 类已移除）；hooks 的 `onCompleted`/`onError` 回调必须移除（改 await promise + try/catch）。
- 违反后果: 核心入口无 React 导出，直接编译报错；残留 v3 写法（ApolloError 判型、hooks 回调、构造器内 uri/credentials）在 v4 全部失效。
- 溯源: [官方文档](https://www.apollographql.com/docs/react/migrating/apollo-client-4-migration)

[TQ-15] **MUST**: 键切换/分页保留旧数据用 `placeholderData: keepPreviousData`（配 `isPlaceholderData` 判定）；initialData 仅作既有数据的"种子"（**持久化进缓存且默认视为 stale**）。NEVER 用 initialData 做加载过渡。
- 违反后果: 分页闪 loading；initialData 污染缓存并触发多余重取。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/reference/useQuery)

[TQ-16] **MUST**: 真取消必须 queryFn 消费 `{ signal }` 并透传给请求层（fetch 直接传；axios ≥0.22 传 signal）；编程式取消用 `cancelQueries`（乐观更新 `revert` 默认 true）。
- 违反后果: 默认只有 UI 状态回退、网络请求照发（流量浪费）；乐观更新留下半旧数据。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation)

[TQ-17] **MUST**: useQueries 的 `combine` 必须稳定引用（useCallback/模块级提取——内联箭头函数每次渲染重跑）；queries 内联 select 推断回退 unknown——显式注解 select 参数或 queryOptions 包装。
- 违反后果: combine 每渲染重算 + 重渲风暴；select 结果 unknown 丢失类型（数组整体推断的 TS 限制）。
- 溯源: [官方文档](https://tanstack.com/query/latest/docs/framework/react/reference/useQueries)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| queryKey | 结构化缓存键：`['posts', { page: 1 }]`，**确定性哈希**序列化比较非引用比较 |
| queryFn | 数据获取函数；**必须 throw** 才产生 error 状态 |
| staleTime | 数据多久内算新鲜（不触发重取）；默认 0 |
| gcTime | 无观察者后多久回收；默认 5 分钟 |
| QueryClient | 缓存与配置中枢；SSR 必须**每请求新建**（工厂） |
| invalidateQueries | 按前缀失效缓存，触发活跃查询重取 |
| mutation | 写操作；**默认不重试**（query 默认重试 3 次） |
| placeholderData / keepPreviousData | 加载期占位数据（**不进缓存**）；分页保留旧数据 `placeholderData: keepPreviousData` [TQ-15] |
| initialData | 缓存真实初始数据（**持久化进缓存**，默认视为 stale）[TQ-15] |
| networkMode | 离线行为：online（默认，断网暂停）/ always（永不暂停）/ offlineFirst [TQ-12] |
| fetchStatus | fetching / paused（断网暂停，配 isPaused）/ idle |
| useQueries | 可变数量并行查询；`combine` 合并结果为单值（结构共享保引用稳定，但 combine 函数本身须稳定引用）[TQ-17] |
| QueryCache | 查询存储中枢；全局回调 onError/onSuccess/onSettled（每查询必调、不可覆盖、fire-and-forget） |

## 最佳实践

### 场景：缓存键设计（[TQ-4]/[TQ-10]）

推荐路径：层级结构 = 失效粒度——`[资源, 子视图, 参数]`；mutation 后按前缀失效。

```ts
// don't：扁平无结构，无法失效 'posts' 前缀
useQuery({ queryKey: ['post-1'], queryFn: fetchPost });

// do：层级结构 = 失效粒度
useQuery({ queryKey: ['posts', 'detail', id], queryFn: fetchPost });
// invalidateQueries({ queryKey: ['posts'] }) 全失效；['posts','detail',id] 精确
```

边界条件：key 是**确定性哈希**（[官方文档](https://tanstack.com/query/latest/docs/framework/react/guides/query-keys)）——对象键顺序无关（`{status, page}` == `{page, status}` == `{page, status, other: undefined}`，**undefined 值被忽略**）；**数组元素顺序敏感**；`['posts', { page: 1 }]` 每次新对象字面量也命中同键（不是引用比较）；但函数/类实例等不稳定引用不要进 key。queryFn 依赖的会变变量必须进 key（变量变 → 自动重取）。依赖查询（params 未就绪不发请求）配 `enabled: false`。

### 场景：queryFn 封装（[TQ-2]）

推荐路径：统一 api 层——fetch + 非 2xx 显式 throw + 解析；Nest 后端的错误格式（含 status）在 queryFn 转译为 throw。

```ts
queryFn: async () => {
  const res = await fetch('/api/todos');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);  // 必须显式 throw [TQ-2]
  return res.json();
}
```

### 场景：乐观更新（[TQ-6]）

标准模板（三步缺一不可）：

```ts
onMutate: async (newTodo) => {
  await queryClient.cancelQueries({ queryKey: ['todos'] });  // 1. 取消在途请求
  const prev = queryClient.getQueryData(['todos']);           // 2. 快照
  queryClient.setQueryData(['todos'], patchWith(newTodo));    // 3. 乐观写入
  return { prev };
},
onError: (_e, _v, ctx) => queryClient.setQueryData(['todos'], ctx.prev),  // 回滚
onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),  // 同步真值 [TQ-10]
```

### 场景：无限列表（useInfiniteQuery）

推荐路径：`initialPageParam` 必填 + `getNextPageParam` 返回下一页 cursor——**返回 null/undefined 即无更多页**（hasNextPage/hasPreviousPage 据此判定）；cursor 缺失时用 pageParam 自算（第三参 lastPageParam 可用）。双向列表：`getPreviousPageParam` + `fetchPreviousPage`；倒序展示用 `select` 反转 pages/pageParams。`maxPages` 限制内存驻留页数（双向列表按滚动方向逐出旧页）。

### 场景：SSR / Next.js 集成（[TQ-5]/[TQ-9]）

推荐路径：QueryClient 工厂 + 浏览器端缓存单例；RSC 首屏数据不进 queryClient，交互式数据预取用 prefetchQuery + dehydrate + `<HydrationBoundary state={dehydratedState}>`（忘传则预取白做）。

```ts
function makeQueryClient() {
  return new QueryClient({ defaultOptions: { queries: { staleTime: 60_000 } } });
}
let browserClient: QueryClient | undefined;
function getQueryClient() {
  return typeof window === 'undefined'
    ? makeQueryClient()
    : (browserClient ??= makeQueryClient());
}
```

```tsx
// don't：RSC 里 useQuery（Server 组件无 hooks），或 RSC 数据再包 useQuery 双轨 [TQ-9]
// do：首屏 RSC await 直取；交互式数据 'use client' 子树内 useQuery
async function Page() {
  const posts = await db.post.findMany();
  return <InteractiveList initialPosts={posts} />;
}
```

### 场景：缓存调优（[TQ-7]/[TQ-8]）

推荐路径：减少重取调 `staleTime`；延长缓存存活调 `gcTime`；静态字典数据 `staleTime: Infinity`（仍响应手动 invalidateQueries）；**运行期不可变数据**（启动时 feature flags、登录时权限、静态参照表）用 `staleTime: 'static'`——更严：连手动失效和 `refetchOnMount/WindowFocus/Reconnect: 'always'` 都阻断 [官方文档](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)。UI 状态按语义选：首屏骨架屏 isPending、请求中禁用按钮 isFetching、后台刷新 isFetching 且 !isPending。另注意 **structuralSharing 仅对 JSON 兼容值生效**——响应含 Date/Map 等引用类型时恒视为已变更（引用不稳定），大响应性能问题可 `structuralSharing: false` 关闭；**`refetchInterval` 轮询与 staleTime 相互独立**（设了轮询别忘 staleTime 仍控制其余重取路径）。

### 场景：查询取消（[TQ-16]）

推荐路径：真取消 = queryFn 消费 `{ signal }` 并透传给请求层；默认 unmount **不取消**（数据仍写入缓存供复用）；编程式取消 `queryClient.cancelQueries({ queryKey })`。

```ts
useQuery({
  queryKey: ['todos'],
  queryFn: async ({ signal }) => {
    const res = await fetch('/api/todos', { signal });  // 真取消：透传 [TQ-16]
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
});
```

边界条件：取消后 query **回退前一状态**（乐观更新不留半旧数据）；`cancelQueries` 选项：`{ silent: true }` 不触发回调、`{ revert: true }`（默认）回滚乐观更新；**取消分两层**——UI 状态层默认有、网络层必须手动接 signal；axios <0.22 用 CancelToken；**Suspense hooks 下取消不工作**（[TQ-11]）。

### 场景：数据过渡与初始数据（[TQ-15]）

placeholderData vs initialData（最高频混淆，一表定夺）：

| 维度 | placeholderData | initialData |
|---|---|---|
| 进缓存 | 否（纯展示占位） | **是** |
| 默认新鲜度 | 不适用（不算缓存数据） | **视为 stale**（除非设 staleTime） |
| 类型层 | data 仍可 undefined（`isPlaceholderData` 标识） | DefinedInitialDataOptions 重载：data 非空 |
| 适用 | 加载过渡 / 分页保留旧数据 | 已有数据"种子"（列表 → 详情） |

```ts
// 分页过渡：键切换不闪 loading（v5 写法；v4 的 keepPreviousData: true 布尔选项已废弃）
import { keepPreviousData } from '@tanstack/react-query';
const { data, isPlaceholderData } = useQuery({
  queryKey: ['posts', page],
  queryFn: fetchPosts,
  placeholderData: keepPreviousData,        // [TQ-15]
});
// isPlaceholderData 为 true 时禁用翻页按钮

// 种子模式：列表缓存喂详情（携带新鲜度）
useQuery({
  queryKey: ['posts', id],
  queryFn: fetchPost,
  initialData: () => queryClient.getQueryData(['posts'])?.find(p => p.id === id),
  initialDataUpdatedAt: () => queryClient.getQueryState(['posts'])?.dataUpdatedAt,
});
```

边界条件：函数式占位 `placeholderData: (previousData, previousQuery) => ...` 可跨键借数据；有 placeholderData 时 status 即 success 且 **isPending 为 false**（加载判定改用 isPlaceholderData）；条件查询类型安全跳过用 `queryFn: id != null ? fetchX : skipToken`——**skipToken 期间 refetch() 无效**（需手动触发改 `enabled: false`）。

### 场景：离线与网络模式（networkMode）

| 模式 | 行为 | 适用 |
|---|---|---|
| online（默认） | 断网 fetchStatus: 'paused'（isPaused: true），恢复**继续**而非重新请求；重试也暂停 | 常规在线应用 |
| always | 永不 paused | queryFn 自带离线存储（AsyncStorage） |
| offlineFirst | 执行一次后暂停重试 | service worker 本地回源 |

边界条件：判定"暂停"须 `fetchStatus === 'pending' && isPaused`（只查 pending 不够）；`always` 模式下 refetchOnReconnect 默认变 false；离线挂起的 mutation 恢复用 `queryClient.resumePausedMutations()`（配 PersistQueryClientProvider onSuccess，[TQ-12]）。

### 场景：Suspense 数据获取（[TQ-11]）

推荐路径：fetch-as-you-render 模式用 `useSuspenseQuery`（data 保证 defined，无 isPending 分支）；同组件多查询**必须** useSuspenseQueries 并行。

```tsx
// don't：同组件多个 useSuspenseQuery 逐个 suspend → 串行请求瀑布
const a = useSuspenseQuery({ queryKey: ['a'], queryFn: fetchA });
const b = useSuspenseQuery({ queryKey: ['b'], queryFn: fetchB });

// do：useSuspenseQueries 并行
const [a, b] = useSuspenseQueries({
  queries: [
    { queryKey: ['a'], queryFn: fetchA },
    { queryKey: ['b'], queryFn: fetchB },
  ],
});
```

边界条件：选项同 useQuery 但**移除 `throwOnError`/`enabled`/`placeholderData`**；queryFn **不可为 skipToken**；**cancellation 不工作**（reference 明示）；fetch 失败且无缓存 → throw 进**最近 Error Boundary**（外层必须配错误边界，配 `QueryErrorResetBoundary` + `onReset` 做重试恢复）；**已有缓存时后台刷新失败不 throw，照常渲染缓存数据**；retry 默认客户端 3 / 服务端 0。

### 场景：动态并行查询与全局错误处理（useQueries/QueryCache，[TQ-17]）

推荐路径：数量可变的并行查询用 `useQueries`（Suspense 场景仍用 useSuspenseQueries，[TQ-11]）；`combine` 把结果数组合并为单值（结构共享保证 combine 输出引用稳定——但 **combine 函数本身必须稳定引用**）；全局错误日志/上报用 QueryCache 回调；组件级降级 isError 分支；错误边界兜底 throwOnError。

```ts
// do：稳定引用的 combine（内联箭头函数每次渲染重跑 [TQ-17]）
const combined = useQueries({
  queries: ids.map((id) => postOptions(id)),        // queryOptions 工厂包装
  combine: useCallback((results) => ({
    data: results.map((r) => r.data),
    isPending: results.some((r) => r.isPending),
    isError: results.some((r) => r.isError),
  }), []),
});
```

```ts
// 全局错误处理：new QueryClient({ queryCache }) —— onError 每查询必调
const queryCache = new QueryCache({
  onError: (error, query) => reportError(error, { queryKey: query.queryKey }),
});
```

边界条件：同一 queryKey 在 queries 数组出现多次→查询间**数据共享**（去重后 map 回原结构）；顶层 `subscribed: false` 退订缓存更新（纯快照读取）；useQueries 的 placeholderData 与 useQuery 不同——占位函数收到的 previousData/previousQuery **恒为 undefined**（查询数量可变，无从借前值）；**内联 select 推断回退 unknown**（useQueries 一次性推断整个数组的 TS 限制）——显式注解 select 参数或 queryOptions 包装（spread queryOptions 再覆写 select 仍 unknown，须把 spread 再包进 queryOptions）；QueryCache 全局回调与 defaultOptions 不同——**不可被单查询覆盖、每查询必被调用**，且 fire-and-forget（返回值不被 await，与 MutationCache 回调不同）；`queryCache.find`（filters）默认 exact: true；直接改 query.state 不通知订阅者（subscribe 只报 added/removed/updated）。

### 场景：缓存持久化（[TQ-12]）

推荐路径：`PersistQueryClientProvider` 一体化（替代 QueryClientProvider：内建订阅生命周期 + 恢复期间阻塞 fetching，恢复后非 fresh 数据自动重取）。

```tsx
<PersistQueryClientProvider
  client={queryClient}
  persistOptions={{
    persister,                    // createSyncStoragePersister / createAsyncStoragePersister / 自定义
    maxAge: 24 * 60 * 60 * 1000,  // 默认 24h
    buster: APP_VERSION,          // schema/版本变更时缓存 busting
  }}
  onSuccess={() => queryClient.resumePausedMutations()}  // 恢复离线期间挂起的 mutation
>
  <App />
</PersistQueryClientProvider>
```

边界条件：**gcTime 必须 ≥ maxAge**（maxAge 默认 24h > gcTime 默认 5min，不显式调 gcTime 则持久化提前失效）；过期/buster 不匹配/恢复错误 → 自动 removeClient 丢弃重取；`useIsRestoring` 查询恢复中状态（恢复期间 fetching 被阻塞）；IndexedDB 自定义 persister 可存 Date/File 原生对象（免序列化、>5MB）；**gcTime 上限 ~24 天**（浏览器 setTimeout 32-bit 上限，`timeoutManager.setTimeoutProvider` 可突破）；命令式 API `persistQueryClientSave/persistQueryClientRestore/persistQueryClientSubscribe`（subscribe 返回 unsubscribe）——**禁止模块级调用 persistQueryClient**（永不取消订阅 + 竞态），React 用 PersistQueryClientProvider。

### 场景：tRPC 集成（@trpc/tanstack-react-query）（[TQ-13]）

推荐路径：**@trpc/tanstack-react-query（11.28.3）是官方推荐客户端**——经典 `@trpc/react-query`（`trpc.x.useQuery()` 钩子）只修 bug，下大版本移除。工厂模式把 procedure 映射为 TanStack Query 原生接口。

```tsx
import { useTRPC } from './trpc';  // createTRPCContext<AppRouter>() 产物
const trpc = useTRPC();

const users = useQuery(trpc.user.list.queryOptions());          // 工厂 → queryOptions
const creator = useMutation(trpc.user.create.mutationOptions({
  onSuccess: async (user) => {
    queryClient.setQueryData(trpc.user.byId.queryKey({ id: user.id }), user);
    await queryClient.invalidateQueries(trpc.user.pathFilter());  // router 子树全失效
  },
}));
```

边界条件：**失效三助手**——`queryFilter(input?)`（单 procedure，省 input 匹配全部输入）/ `pathFilter()`（router 子树）/ `trpc.pathFilter()`（全部 tRPC 查询）；**router 上无 queryFilter/queryOptions/queryKey**（用 pathKey/pathFilter）；无 React context 的 SPA 用 `createTRPCOptionsProxy` 单例；预取用 Handles API（`loadHandles`/`ensureEntry`/`fromHandle`/`HydrateClient`）；`useTRPC()` 在 TRPCProvider 外调用 throw；服务端（tRPC 侧）**非 TRPCError 的原始 message 生产环境也会发给客户端**——须配 `errorFormatter` 替换 INTERNAL_SERVER_ERROR message + `onError` 上报（OWASP 信息泄漏）[官方文档](https://trpc.io/docs/server/error-handling)；**跨网络 Date 等复杂类型**：links/服务端配 superjson data transformer 保留类型（默认 JSON 序列化 Date 变字符串）[官方文档](https://trpc.io/docs/quickstart)；server-side call：`createCaller(await createContext())`，Next SSR 用 `createServerSideHelpers`。

### 场景：GraphQL 客户端（Apollo Client 4）（[TQ-14]）

选型定位：GraphQL 项目主选 **Apollo Client 4.3.8**（legacy 线 3.14.1）——normalized cache、`@defer`、乐观 UI、codegen 生态是 TanStack Query 覆盖不到的面；TanStack Query 跑 GraphQL 只剩"传输层是 GraphQL"的场景。安装 `npm install @apollo/client@latest graphql rxjs`（**rxjs 是 v4 新 peer**）。

v4 最小骨架（v3 写法在 v4 全部编译报错）：

```tsx
import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";
import { ApolloProvider, useQuery } from "@apollo/client/react"; // React 导出移至此入口

const client = new ApolloClient({
  link: new HttpLink({ uri: "/api/graphql", credentials: "include" }), // v4：uri/credentials 移入 HttpLink
  cache: new InMemoryCache(),
});
```

v3→v4 断裂速查（生成代码前先查 @apollo/client 大版本）：

- **导入**：React API 全走 `@apollo/client/react`（核心 `@apollo/client` 无 React 导出）；`@apollo/client/core`→`@apollo/client`
- **构造器**：uri/headers/credentials→显式 HttpLink；connectToDevTools→devtools.enabled；disableNetworkFetches→prioritizeCacheValues；resolvers→localState（@client 本地状态 opt-in）
- **错误**：`ApolloError` 类移除——判型用 `CombinedGraphQLErrors.is(error)`/`ServerError.is(error)`/`CombinedProtocolErrors.is(error)`；统一 `error` 属性（`errors` 移除）；网络错误原样返回不再包裹
- **hooks**：`onCompleted`/`onError` 从所有 hooks 移除→await promise + try/catch；useLazyQuery 的 variables/context 移入 execute()；render 期间调 execute throw（改 useQuery+skip）；useMutation ignoreResults 移除→client.mutate
- **Observable**：zen-observable→rxjs（fromPromise→from、toPromise→firstValueFrom）；ObservableQuery 不再继承 Observable（`from(observableQuery)` 转换）
- **迁移工具**：`npx @apollo/client-codemod-migrate-3-to-4 src`（TS 项目 ts/tsx 分开跑：`--parser ts --extensions ts` / `--parser tsx --extensions tsx`）

边界条件：`notifyOnNetworkStatusChange` 默认 true（refetch 时 loading 更频繁，回退 v3 用 defaultOptions.watchQuery）；网络错误遵守 errorPolicy 且**不终止 ObservableQuery**（错误走 next 的 result.error，error 回调可删）；subscription 去重默认开——依赖服务器连接初始值的服务器须 `context: { queryDeduplication: false }`；MockedProvider 默认随机 20-50ms 延迟（测试必须处理 loading 态）；codegen 生成 hooks 官方建议弃用（缺函数重载丢类型安全）→直接 hooks + TypedDocumentNode；defaultOptions 用 errorPolicy/returnPartialData 须在 DeclareDefaultOptions（apollo.d.ts）类型级声明。

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | v4 语法类型报错/key 错乱 | 位置参数写 v5 | 对象语法 [TQ-1] |
| 2 | HTTP 4xx/5xx 却显示"成功但空数据" | queryFn 未 throw | [TQ-2] |
| 3 | 骨架屏/禁用逻辑不对 | isPending/isFetching/isLoading 混写 | v5 语义拆分 [TQ-8] |
| 4 | 调 gcTime 不减重取；切页闪 loading | staleTime/gcTime 混淆 | 分开决策 [TQ-7] |
| 5 | 乐观更新并发回滚被覆盖 | 漏 cancelQueries | 三步模板 [TQ-6] |
| 6 | SSR 用户 A 偶见用户 B 数据 | 模块级单例 QueryClient | 工厂模式 [TQ-5] |
| 7 | 接口超时订单创建两次 | mutation 加了 retry | 保持默认 [TQ-3] |
| 8 | 缓存永不命中 | key 塞不稳定引用 | 可序列化 key [TQ-4] |
| 9 | Suspense 页多查询逐个出数据 | 多个 useSuspenseQuery 串行 suspend | useSuspenseQueries 并行 [TQ-11] |
| 10 | 持久化缓存 24h 内提前蒸发 | gcTime（5min）< maxAge（24h） | gcTime ≥ maxAge [TQ-12] |
| 11 | invalidateQueries 对某查询无效 | 误用 staleTime: 'static'（手动失效也被阻断） | 可失效数据改 Infinity [TQ-7] |
| 12 | Apollo v4 升级后 useQuery/ApolloProvider 等导入报错 | React 导出移至 `@apollo/client/react`，核心入口无 React API | 从 react 入口导入 + codemod [TQ-14] |
| 13 | 分页闪 loading；用 initialData 填后多余重取 | initialData 持久化进缓存且默认 stale | `placeholderData: keepPreviousData` [TQ-15] |
| 14 | 「取消」后请求仍发出去 | queryFn 未透传 signal（只有 UI 状态回退） | signal 透传 [TQ-16] |
| 15 | 断网查询挂起/恢复行为与预期不符 | networkMode 语义不明 | 默认 online 暂停+恢复继续；判定 pending && isPaused |
| 16 | skipToken 条件查询调 refetch() 无效 | skipToken 期间手动 refetch 不工作 | 需手动触发改 enabled: false |
| 17 | useQueries 结果频繁重算/重渲 | 内联 combine 每次渲染重跑 | useCallback/稳定引用 [TQ-17] |
| 18 | useQueries 内联 select 的 data 为 unknown | 数组整体推断的 TS 限制 | 显式注解或 queryOptions 包装 [TQ-17] |
| 19 | 以为 QueryCache onError 可被单查询关闭/覆盖 | 全局回调每查询必调、不可覆盖（defaultOptions 才可被覆盖） | 全局回调只做日志/上报，查询级行为用 defaultOptions |

**Top 展开：坑点 2（queryFn 忘 throw，最隐蔽）**：TanStack Query 不检查 HTTP status，只认 Promise rejection——`fetch` 对 4xx/5xx 不 reject，error 永远 null，页面"成功但空数据"且无任何报错。修复见最佳实践 queryFn 封装（[TQ-2]）。

**Top 展开：坑点 6（SSR 单例泄漏，最高危安全事故）**：服务端一个进程处理多请求，模块级单例共享缓存 → 跨用户数据泄漏。工厂模式修复见最佳实践 SSR 集成（[TQ-5]/LAW-3）。

## API 速查表

| API | 签名要点 | 易错点 |
|---|---|---|
| useQuery | `{ queryKey, queryFn, enabled?, staleTime?, select?, placeholderData? }` | v5 对象语法 [TQ-1]；queryFn 必须 throw [TQ-2] |
| useInfiniteQuery | `{ queryKey, queryFn, initialPageParam, getNextPageParam?, maxPages? }` | **initialPageParam 必填**（v5）；`data.pages`/`data.pageParams` 结构；refetch 逐页**串行**；同一 entry 单飞行——后台刷新中 fetchNextPage 可能覆盖刷新数据，触发前查 `!isFetching` 或 `cancelRefetch: false`；`maxPages` 限页优化内存/网络；手动 setQueryData 须保持 pages/pageParams 同构 |
| useMutation | `{ mutationFn, onMutate?, onError?, onSuccess?, onSettled? }` | 默认不重试 [TQ-3]；`mutate` 实例回调只对本次生效 |
| invalidateQueries | `{ queryKey }` 前缀匹配 | 想精确匹配加 `exact: true` |
| setQueryData | `(key, updater)` 直写缓存 | 写后忘 invalidate（真值不同步）[TQ-10] |
| cancelQueries | 取消在途请求 | 乐观更新必配 [TQ-6]；silent/revert 选项 [TQ-16] |
| placeholderData / keepPreviousData | `placeholderData: keepPreviousData` 分页保留旧数据 | NEVER 用 initialData 做过渡 [TQ-15] |
| networkMode | online（默认）/ always / offlineFirst | 暂停判定 fetchStatus==='pending' && isPaused |
| skipToken | 条件查询类型安全跳过 | 期间 refetch() 无效（手动触发改 enabled: false） |
| useIsFetching / useIsMutating | 全局进行中计数 | [模型经验]（未单独文档复核） |
| HydrationBoundary | `<HydrationBoundary state={dehydratedState}>` | 服务端 prefetch 后忘传则预取白做 |
| useQueryClient | 获取 client 实例 | SSR 单例泄漏 [TQ-5] |
| useSuspenseQuery | 同 useQuery 减 throwOnError/enabled/placeholderData | data 保证 defined；无缓存 fetch 失败 throw 进 Error Boundary（有缓存时后台刷新失败不 throw）；**cancellation 不工作**；queryFn 不可 skipToken [TQ-11] |
| useSuspenseQueries | `{ queries: [...] }` 并行 Suspense 查询 | 同组件多 Suspense 查询唯一并行解 [TQ-11] |
| useQueries | `{ queries, combine?, subscribed? }` 可变数量并行查询 | combine 须稳定引用；内联 select 推断 unknown；同 key 多次出现数据共享 [TQ-17] |
| QueryCache / QueryCacheConfig | `new QueryCache({ onError, onSuccess, onSettled })` 全局回调；find/findAll/subscribe | 每查询必调不可覆盖；fire-and-forget；find 默认 exact: true |
| PersistQueryClientProvider | 替代 QueryClientProvider 的持久化 Provider | gcTime ≥ maxAge；onSuccess 配 resumePausedMutations；禁模块级 persistQueryClient [TQ-12] |
| Devtools | `@tanstack/react-query-devtools` | 排障第一入口：fresh/stale/inactive 状态可视 |
| @trpc/tanstack-react-query | **11.28.3**（peer @tanstack/react-query ^5.106、React ≥18.2、TS ≥5.7.2） | 工厂模式 queryOptions/mutationOptions [TQ-13]；失效用 queryFilter/pathFilter；经典 @trpc/react-query（trpc.x.useQuery()）已弃用下大版本移除；@trpc/next 的 createTRPCNext/withTRPC/ssr:true 同步弃用 |
| @apollo/client | **4.3.8**（React 导出在 `@apollo/client/react`；peer：graphql + rxjs） | v4：ApolloError 移除（CombinedGraphQLErrors.is 判型）；hooks onCompleted/onError 移除；uri/credentials 移入 HttpLink；useLazyQuery variables 移入 execute() [TQ-14] |

## 版本注意

- 当前最新：**5.107.1**（npm，2026-11-15 锚定）[官方文档](https://www.npmjs.com/package/@tanstack/react-query)
- v5 为现行大版本：对象语法、isPending/isLoading 拆分、TS 全面泛型化
- v4 → v5 迁移：位置参数 → 对象语法；`isLoading` 语义变化；`cacheTime` → `gcTime` [官方文档](https://tanstack.com/query/latest/docs/framework/react/overview)
- **TanStack 生态周边**（registry + 官方文档锚定，2026-11-16）：
  - **@tanstack/react-virtual 3.14.26**（virtual-core 3.19.11；peer React ^16.8-^19）：headless 虚拟化——`useVirtualizer({ count, getScrollElement, estimateSize })` → getTotalSize/getVirtualItems；绝对定位 + translateY 渲染模式；vertical/horizontal/双轴网格；聊天反向流有专门 guide [官方文档](https://tanstack.com/virtual/latest/docs/framework/react/overview)
  - **@tanstack/react-form 1.33.5**（form-core 同版；**peer React ^17-^19，无 React 16**；六框架适配器 React/Vue/Angular/Solid/Svelte/Lit；**v2 alpha 已启：alpha=2.0.0-alpha.3（2026-11-17 巡检）——v2 未 stable 前 1.x API 为生成基线**）：headless 类型安全表单——form.Field render props / form.Subscribe selector 细粒度订阅 / **onChangeAsyncDebounceMs 异步校验防抖内建**；统一 DevTools（@tanstack/react-devtools + react-form-devtools）；**组合 API（官方长期推荐）**：`createFormHookContexts()` + `createFormHook({ fieldComponents, formComponents, fieldContext, formContext })` 定义一次 → `useAppForm` + `form.AppField`（组件预绑定 `field.TextField`，**name typo 编译错**、减生产样板）；**schema 直挂 form 级校验**：`validators: { onChange: z.object({...}) }`（Zod/Valibot/ArkType 等 Standard Schema 均可，field 级亦可）；one-off 场景用 `useForm` + `form.Field`（AppField 全兼容 Field 属性）；reset 按钮 `e.preventDefault()` + `form.reset()`（防 select 意外重置）[官方文档](https://tanstack.com/form/latest/docs/overview) + [官方文档](https://tanstack.com/form/latest/docs/framework/react/quick-start)
  - **TanStack Form 校验深面**：验证时机全集 onChange/onInput/onBlur/onSubmit + Async 变体；`field.state.meta.errors[]`（当前全错）与 `errorMap['onChange']`（按时机取错）**类型自动匹配 validator 返回类型**（返回对象亦可）；**form 级设置 field 错误**：form `onSubmitAsync` 返回 `{ form: 'msg', fields: { age: '...', 'details.email': '...', 'socials[0].url': '...' } }` 嵌套路径（单 API 端点校验全表单）；**覆盖坑**：form 级 field 错误可被 field 级验证覆盖（form "Too young" + field "Must be odd" → 只显示后者）；**sync 先跑，async 仅在 sync 成功后跑**（`asyncAlways: true` 破例）；防抖双层：`asyncDebounceMs={500}` 字段级统一 + `onChangeAsyncDebounceMs: 1500` 单验证器覆盖；Standard Schema 四家 Zod/Valibot/ArkType/**Effect/Schema**（form 级 errorMap 类型不同：函数→string，schema→`Record<string, StandardSchemaV1Issue[]>` 按 field name 键控；**schema 校验不产 transformed values**）；混合模式 `fieldApi.parseValueWithSchema(schema)`；**`canSubmit` touched 语义**（未触碰时即使字段技术性无效仍 true，触碰后任一无效即 false）；禁提交用 `!canSubmit || isPristine`；disabled 按钮不可访问用 `aria-disabled` [官方文档](https://tanstack.com/form/latest/docs/framework/react/guides/validation)
  - **@tanstack/react-pacer 0.24.1**（pacer core 0.23.1；peer React >=16.8）：执行时机控制（debounce/throttle/rate-limit/queue/batch 五模式）——**0.x 早期版本，API 可变**（2026-11-17 复核：无 beta dist-tag）；全异步 + retry/abort；库发布用 @tanstack/pacer-lite [官方文档](https://tanstack.com/pacer/latest/docs/overview)
  - **@tanstack/react-hotkeys 0.27.0**（hotkeys core 0.32.0；peer React >=18；**官方 beta，API 可变**）：类型安全键盘快捷键——`useHotkey('Mod+S', cb)` / `useHotkeys([{ hotkey, callback }, ...])`（**`Mod` = macOS ⌘ / Win+Linux Ctrl**；Vim 式序列 `useHotkey(['G','G'], cb)` 步进默认 1s）；**快捷键随组件 mount/unmount 注册注销**（对话框 Escape 只在打开时生效）；`{ enabled }` 条件启用、ref `target` 限定元素；`useFormatForDisplay()` 平台标签（⌘ S / Ctrl+S）——**SSR（Start/Next.js）须从请求设 provider `platform` 防 hydration 错误**；`HotkeysProvider` scope 分组 + **`exclusive` 独占键盘**（对话框关闭后外部快捷键恢复）；默认阻止浏览器默认动作 + 文本输入时忽略单键；app hotkeys（`defineAppHotkeys` 前置声明 + 用户可重绑定）与 `HotkeyRecorder` 录制为进阶面 [官方文档](https://tanstack.com/hotkeys/latest/docs/framework/react/quick-start)
  - **@tanstack/react-table 9.3.1**（table-core 同版；peer React >=18；v9 stable——2026-11-17 复核无漂移）：headless 表格引擎（官方明确"非预构建组件"）——`useTable({ features, columns, data })` → getHeaderGroups()/getRowModel() 渲染自有 markup；**17 内建特性按需注册**（Cell Selection/Cell Spanning、Column Filtering/Grouping/Ordering/Pinning/Resizing/Sizing/Visibility、Faceting、Global Filtering、Row Aggregation/Expanding/Pagination/Pinning/Selection/Sorting），全量 ~25KB Brotli、tree-shake 后基础表只打包核心；**任一状态切片（sorting/filters/pagination）可外提到框架状态/全局 store/URL** [官方文档](https://tanstack.com/table/latest/docs/framework/react/overview)
  - 家族新锚定（2026-11-17 复核）：**@tanstack/react-router 1.170.46**（react-start 1.169.5；peer React >=18）、**@tanstack/store 0.11.2**（react-store 同版；**Table v9 状态底层即 Store 驱动**——传自有 atoms 可接管任一状态切片）、@tanstack/eslint-plugin-query 5.107.1（peer eslint ^8.57||^9||^10 + **typescript ^5.6||^6||^7 已支持 TS 7**——对比 typescript-eslint 8.73.0 尚不支持）
  - **TanStack Form 提交与联动**：**onSubmitMeta** 多提交行为——`useForm({ onSubmitMeta: defaultMeta, onSubmit: ({ value, meta }) => ... })`，按钮各自 `form.handleSubmit({ submitAction: 'continue' })` 覆盖默认（无 meta 调用用默认值）；**Standard Schema 只做校验不保留 output**——onSubmit 恒收 **input 数据**，要 transformed 值须 onSubmit 内 `schema.parse(value)` 二次解析（`z.input<typeof schema>` 定 defaultValues）；**字段联动验证**：`onChangeListenTo: ['password']`——对方字段变化时重跑本字段验证（password/confirm_password 场景，无 listenTo 则错误残留不重跑）+ 对应 `onBlurListenTo`；跨字段取值 `fieldApi.form.getFieldValue('password')` [官方文档](https://tanstack.com/form/latest/docs/framework/react/guides/submission-handling) + [官方文档](https://tanstack.com/form/latest/docs/framework/react/guides/linked-fields)
  - 选型注意：表单主选 react-hook-form（生态成熟）；TanStack Form 为 TS 极致类型安全场景备选；Pacer 处于 beta 慎入生产关键路径
- **Apollo Client（GraphQL 客户端）**：**4.3.8**（npm，2026-11-09；legacy 线 3.14.1 仅维护）——v4 大改：React 导出移至 `@apollo/client/react`、rxjs 新 peer、ApolloError 移除（CombinedGraphQLErrors.is 判型）、hooks onCompleted/onError 移除、Observable 换 rxjs；官方 codemod `@apollo/client-codemod-migrate-3-to-4`，推荐先升 3.14 再迁 4.0 [官方文档](https://www.apollographql.com/docs/react/migrating/apollo-client-4-migration)

## 与其他子领域的集成要点

- **react-core**：状态选型第 5 层——服务端数据缓存首选，**不要**手动塞全局 store（LAW-2）→ 见 `kb/react-core.md`
- **Next.js**：RSC 首屏不进 queryClient（[TQ-9]）；交互式数据预取用 prefetchQuery + dehydrate + HydrationBoundary → 见 `kb/nextjs.md`
- **react-admin**：react-admin 底层即 TanStack Query——开源版 realtime DIY、staleTime 调优直接操作 queryClient → 见 `kb/react-admin.md`
- **NestJS**：queryFn 对接 Nest API；Nest 错误格式（含 status）需在 queryFn 转译为 throw（[TQ-2]）→ 见 `kb/nestjs.md`

## 来源索引

- TanStack Query 官方 overview（v5 对象语法、queryFn throw、server state 定位）：https://tanstack.com/query/latest/docs/framework/react/overview [官方文档]
- npm @tanstack/react-query（版本 5.107.1 锚定）：https://www.npmjs.com/package/@tanstack/react-query [官方文档]
- Query Keys 指南（确定性哈希语义：对象键序无关/undefined 忽略/数组序敏感；依赖变量进 key）：https://tanstack.com/query/latest/docs/framework/react/guides/query-keys [官方文档]
- useSuspenseQuery reference（选项差异/串行瀑布/Error Boundary 语义/cancellation 不工作）：https://tanstack.com/query/latest/docs/framework/react/reference/useSuspenseQuery [官方文档]
- persistQueryClient 插件（PersistQueryClientProvider/gcTime ≥ maxAge/buster/24 天上限）：https://tanstack.com/query/latest/docs/framework/react/plugins/persistQueryClient [官方文档]
- Important Defaults（staleTime 'static' vs Infinity/structuralSharing 仅 JSON/重取触发点）：https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults [官方文档]
- tRPC procedures/context/middlewares/error-handling（base procedures/ctx 收窄/next() 不抛错/错误码表/errorFormatter 安全）：https://trpc.io/docs/server/procedures、https://trpc.io/docs/server/context、https://trpc.io/docs/server/middlewares、https://trpc.io/docs/server/error-handling [官方文档]
- @trpc/tanstack-react-query setup（工厂模式/失效三助手/handles 预取/手写 key 陷阱/经典客户端弃用）：https://trpc.io/docs/client/tanstack-react-query/setup [官方文档]
- tRPC Next.js 集成（App Router=fetch adapter+RSC 预取；@trpc/next createTRPCNext/withTRPC 弃用）：https://trpc.io/docs/client/nextjs [官方文档]
- Apollo Client 4 迁移指南（入口点重命名/构造器变更/新错误类/hooks 重写/rxjs/TypeScript/codemod）：https://www.apollographql.com/docs/react/migrating/apollo-client-4-migration [官方文档]
- registry @apollo/client（版本 4.3.8 / 3.14.1 双线锚定）：https://registry.npmjs.org/@apollo%2Fclient [官方文档]
- Query Cancellation 指南（signal 透传/双层取消/cancelQueries silent·revert/乐观更新回退）：https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation [官方文档]
- Network Mode 指南（online/always/offlineFirst、paused/isPaused、恢复继续而非重取）：https://tanstack.com/query/latest/docs/framework/react/guides/network-mode [官方文档]
- useQuery reference（三重载 data 可空性/placeholderData vs initialData/keepPreviousData 分页模式/skipToken/refetchOnReconnect 联动）：https://tanstack.com/query/latest/docs/framework/react/reference/useQuery [官方文档]
- useQueries reference（combine 结构共享/内联 combine 每渲染重跑/内联 select 推断 unknown/同 key 数据共享/subscribed 顶层退订/placeholderData 前值恒 undefined）：https://tanstack.com/query/latest/docs/framework/react/reference/useQueries [官方文档]
- QueryCache reference（subscribe 事件 added·removed·updated/find exact 默认 true/直接改 state 不通知订阅者）：https://tanstack.com/query/latest/docs/framework/react/reference/QueryCache [官方文档]
- QueryCacheConfig reference（全局 onError/onSuccess/onSettled 每查询必调语义/fire-and-forget 对比 MutationCache 回调）：https://tanstack.com/query/latest/docs/framework/react/reference/interfaces/QueryCacheConfig [官方文档]
- [模型经验]：坑点 3/4/5/6/7/8 的故障模式与修复、乐观更新模板、SSR 工厂模式、缓存键设计——适用 v5 全线
- 法则条款来源：corpus/react/tanstack-query/elicited/05-laws.md（法则化萃取）
- TanStack 生态周边锚定（Virtual 3.14.26 / Form 1.33.5 / Pacer 0.24.1 / Table 9.3.1）：https://tanstack.com/virtual/latest/docs/framework/react/overview、https://tanstack.com/form/latest/docs/overview、https://tanstack.com/pacer/latest/docs/overview、https://tanstack.com/table/latest/docs/framework/react/overview [官方文档]
- Table v8→v9 官方迁移指南（useReactTable→useTable/features 注册）：https://tanstack.com/table/latest/docs/framework/react/guide/migrating [官方文档]
- [推断]：无

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| useQuery 位置参数语法 | v5 起必须对象语法（overview 示例锚定） | 采用文档：全部示例对象语法 |
| queryFn 返回非 2xx 响应即报错 | 仅 Promise rejection 算 error，HTTP status 需手动 throw | 采用文档：示例显式 `if (!res.ok) throw` |
| mutation 默认重试 3 次 | mutation 默认**不重试**（query 才默认 3 次） | 采用文档语义 |
| queryKey 引用比较 | 结构化序列化比较（同构字面量即同键） | 采用文档语义 |
| staleTime: Infinity = 完全不可重取 | Infinity 仍响应手动 invalidateQueries；'static' 才连手动失效都阻断 | 采用文档：Infinity=可手动失效；'static'=运行期不可变数据专用 |
| Suspense 查询支持请求取消 | useSuspenseQuery 集成下 cancellation 不工作（reference 明示） | 采用文档 |
| persistQueryClient 任意位置可调 | React 须 PersistQueryClientProvider；模块级调用禁止（订阅永不释放） | 采用文档 |
| tRPC 客户端用经典 `trpc.x.useQuery()` 钩子 | @trpc/tanstack-react-query 工厂模式为官方推荐；classic 只修 bug 下大版本移除 | 采用文档：queryOptions/mutationOptions 工厂 [TQ-13] |
| tRPC 里手写 queryKey 调 vanilla client 等价 | key 非 tRPC 键体系——失效过滤与预取数据永不匹配 | 采用文档：必须 trpc 工厂 [TQ-13] |
| 分页保留旧数据用 `keepPreviousData: true` 布尔选项（v4 记忆） | v5 改为 `placeholderData: keepPreviousData`（官方具名导出） | 采用文档 [TQ-15] |
| initialData 只是"初始展示值" | initialData 持久化进缓存且默认视为 stale | 采用文档：加载过渡用 placeholderData（不进缓存），initialData 仅作种子 [TQ-15] |
| unmount 自动取消网络请求 | 默认不取消（数据仍入缓存）；真取消须 queryFn 消费 signal | 采用文档 [TQ-16] |
| guides/pagination、guides/placeholder-data 为独立指南 | 两页 404——分页/占位内容并入 useQuery reference | 采用文档结构：锚 useQuery reference |
| useQueries 的内联 select 能从同级 queryFn 自动推断 | 推断回退 unknown（数组整体推断的 TS 限制） | 采用文档：显式注解或 queryOptions 包装 [TQ-17] |
| useQueries 占位函数可像 useQuery 一样借 previousData | previousData/previousQuery 恒 undefined（查询数量可变） | 采用文档 |
| QueryCache 全局 onError 等同 defaultOptions.onError（可被单查询覆盖） | 全局回调每查询必调、不可覆盖，且 fire-and-forget（返回值不被 await） | 采用文档：全局回调做日志/上报，查询级行为用 defaultOptions |
| （规范登记）TQ 法则 17 条超 distill.md 硬顶 15 | 达顶政策新立晚于既有 TQ 基线 17 | grandfather 冻结：不再追加新编号，后续修订按三选一收敛至 ≤15（2026-11-17 第三轮项目评审） |

## 事实抽查记录

| 轮次 | 抽查条数 | 结果 | 日期 |
| --- | --- | --- | --- |
| 项目评审改进轮 | 全量 304 URL（spot_check.py --all） | BROKEN 1：reference/QueryCacheConfig 404——TanStack 文档站重构，接口页迁至 reference/interfaces/ 子路径（自 reference 索引页发现新链接），已改锚 reference/interfaces/QueryCacheConfig 并探活 PASS；BLOCKED 4（npmjs 403 反爬 ×3、observe-api.nestjs.com/mcp 401 属 POST 端点预期）经复核豁免 | 2026-11-17 |
