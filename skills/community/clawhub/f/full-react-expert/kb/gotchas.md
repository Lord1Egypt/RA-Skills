---
type: cross-cutting
name: gotchas
version: 36
updated: 2026-11-17
---
# 跨领域高频坑点 Top 汇总

每条一句话 + 详情指向。按"踩中概率 × 排查成本"以 Tier 分组（Tier 1 几乎必踩 / Tier 2 高频 / Tier 3 进阶）。**编号为追加序，稳定可引用，不因归组重排**；新增条目按严重度归入对应 Tier 表，编号续接既有最大号。坑点是法则的负样本——对应的约束性条款见 `kb/laws.md` 与各 subdomain kb「法则」小节（可按 `[前缀-N]` 编号引用）。

## Tier 1（几乎必踩）

| # | 坑点 | 一句话 | 详情 |
|---|---|---|---|
| 1 | useEffect 空依赖 + 闭包读 state | effect 捕获定义时的快照，读到旧值 | kb/react-core.md 坑点 1 |
| 2 | Next 缓存语义随版本反转 | 14 缓存→15 不缓存→16 全 opt-in，先查版本再答 | kb/nextjs.md 坑点 3 |
| 3 | Nest DTO 用 interface | class-validator 装饰器全失效且无报错 | kb/nestjs.md 坑点 2 |
| 4 | 'use client' 边界 | 模块级边界，放太高整页变客户端；文件第一行才有效 | kb/nextjs.md 坑点 2 |
| 5 | "can't resolve dependencies" | providers 忘注册 / exports 漏写 / forFeature 漏 import，按五步排查 | kb/nestjs.md 坑点 1 |
| 6 | react-admin 表格 API 双轨 | 新代码 `<DataTable>`（v5.8+ 推荐，npm 锚定 5.15.7）；存量 Datagrid 合法，勿混写 | kb/react-admin.md「表格组件」节 |
| 7 | TanStack Query queryFn 忘 throw | HTTP 非 2xx 不进 error 状态，"成功但空数据" | kb/tanstack-query.md 坑点 2 |
| 8 | `key={index}` | 动态列表状态错位、输入框串行 | kb/react-core.md 坑点 5 |
| 9 | getList 忘返回 `{ data, total }` | react-admin 分页直接崩 | kb/react-admin.md 坑点 1 |
| 10 | Vitest 里写 Jest API | `jest is not defined`，全量换 `vi.*` | kb/testing.md 坑点 1 |
| 100 | Cache Components 下动态路由 generateStaticParams 返回空数组 | **build error**（empty-generate-static-params）[NX-15] | 至少 1 param；未知值 placeholder + `notFound()`；kb/nextjs.md 坑点 23 |

## Tier 2（高频）

| # | 坑点 | 一句话 | 详情 |
|---|---|---|---|
| 11 | `useEffect(async () => ...)` | 返回 Promise 被当 cleanup | kb/react-core.md 坑点 3 |
| 12 | fetch 竞态 | 无 ignore 标志/AbortController，旧响应覆盖新数据 | kb/react-core.md 坑点 4 |
| 13 | Next 16 强制 await | params/searchParams/cookies()/headers() 全异步化 | kb/nextjs.md 坑点 4 |
| 14 | RSC 用 hooks / 传函数 props | Server 组件无状态钩子；边界 props 须可序列化 | kb/nextjs.md 坑点 5 |
| 15 | hydration mismatch | Date.now/localStorage/window 导致服务端客户端不一致 | kb/nextjs.md 坑点 7 |
| 16 | 嵌套校验漏 @Type | class-transformer 不递归，子对象校验静默跳过 | kb/nestjs.md 坑点 3 |
| 17 | interceptor 忘 return next.handle() | 200 但 body 为 undefined | kb/nestjs.md 坑点 4 |
| 18 | authProvider checkError 忘 reject | 401 死循环不登出 | kb/react-admin.md 坑点 3 |
| 19 | useRecordContext() 忘判空 | record 加载期 undefined，自定义组件白屏 | kb/react-admin.md 坑点 2 |
| 20 | 乐观更新漏 cancelQueries | TanStack Query 回滚被在途请求覆盖 | kb/tanstack-query.md 坑点 5 |
| 21 | SSR 单例 QueryClient | Next.js/SSR 跨用户数据泄漏，必须工厂函数 | kb/tanstack-query.md 坑点 6 |
| 22 | Context 级联重渲染 | 无选择器机制，value 变全体 consumer 重渲染 | kb/react-core.md 坑点 7 |
| 23 | TypeORM 事务内混用全局 repository | 事务外操作不回滚，事务形同虚设 | kb/nestjs.md 坑点 6 |
| 24 | 微服务 send() 不订阅 | 冷 Observable，不订阅请求不发出 | kb/nestjs.md 坑点 7 |
| 25 | Vite 环境变量忘 VITE_ 前缀 | `import.meta.env.X` undefined；密钥进 VITE_ 则泄漏 | kb/vite-tooling.md 坑点 1 |
| 26 | TestingModule 忘 .compile() | Nest 测试最高频；override 须在 compile 前 | kb/testing.md 坑点 5 |
| 27 | Playwright waitForTimeout 硬等待 | flaky 之源；web-first assertions 自动重试 | kb/testing.md 坑点 4 |
| 102 | Redis cache store 断连整个应用崩掉 | Keyv 无 `'error'` 监听器抛未捕获异常 [NE-13] | 注册 store 后立即挂 error listener；kb/nestjs.md 坑点 23 |

## Tier 3（进阶）

| # | 坑点 | 一句话 | 详情 |
|---|---|---|---|
| 28 | save vs update / delete vs softDelete | hooks 触发与否、软硬删语义不同 | kb/nestjs.md 坑点 6 |
| 29 | REQUEST scope 传染 | 请求作用域沿注入链传播，性能塌方 | kb/nestjs.md 坑点 9 |
| 30 | parallel routes 缺 default.js | Next 16 构建直接失败 | kb/nextjs.md 坑点 6 |
| 31 | revalidateTag 单参数 | Next 16 起必须 (tag, profile) 双参 | kb/nextjs.md 速查表 |
| 32 | `@react-admin/ra-*` EE 组件误当开源 | ra-realtime/ra-rbac/ra-navigation 属 EE；**CanAccess/useCanAccess 已核心化**（开源可用）——核心授权走 canAccess | kb/react-admin.md 坑点 4 / [RA-7] |
| 33 | enableShutdownHooks 忘调 | SIGTERM 不触发 $disconnect，连接泄漏 | kb/nestjs.md 坑点 8 |
| 34 | NEXT_PUBLIC_ 构建期内联 | Vercel 静态 bundle 运行时换 env 无效 | kb/nextjs.md |
| 35 | setState 后立即读 | 批处理下闭包值不变，用函数式更新 | kb/react-core.md 坑点 8 |
| 36 | Server Action redirect 被 try/catch 吞 | NEXT_REDIRECT 误捕，需重抛 | kb/nextjs.md 坑点 9 |
| 37 | `@Get(':id')` 遮蔽 `@Get('me')` | 通配路由先声明吃掉字面量；v12 有 routeConflictPolicy | kb/nestjs.md 坑点 10 |
| 38 | mutation 加 retry | 写操作自动重试 = 重复创建（默认不重试是有意的） | kb/tanstack-query.md 坑点 7 |
| 39 | import.meta.glob 默认 eager | 本想懒加载全量进主包 | kb/vite-tooling.md 坑点 4 |
| 40 | turbo dependsOn ["build"] vs ["^build"] | `^`=依赖的包先构建；无 `^`=全包同名任务 | kb/monorepo.md 坑点 2 |
| 41 | turbo outputs 漏配 | 缓存命中但 dist 空；`.next/cache` 排除遗忘 | kb/monorepo.md 坑点 3 |
| 42 | 幽灵依赖暴露后 hoist 掩盖 | pnpm 隔离是特性，正解是补声明 | kb/monorepo.md 坑点 1 |
| 43 | 生态包大版本盲答 | TypeORM 1.x（0.3 结束）/ zod v4（`zod/v3` 兼容入口）/ graphql v17（Node ≥22）——生成前查大版本线 | kb/nestjs.md「版本注意」生态锚定 |
| 44 | prisma CLI latest 打 RC | `npm i prisma` 默认装 8.0.0-rc；生产锁 7.x 须显式版本号 | kb/nestjs.md「版本注意」生态锚定 |
| 45 | 选型 @nestjsx/crud | 已停更 4 年+（最后发布 2022-04），新项目勿选 | kb/react-admin.md「版本注意」/ kb/nestjs.md |
| 46 | MUI 版本序列盲答 | **无 v8——v7 直跳 v9**（2026-04-08）；v9 全移除弃用 `component`/`componentsProps`（一律 slots）、布局组件 system props 移除 | kb/react-core.md「版本注意」生态锚定 |
| 47 | msw 根入口导入 | v3 已移除——`http`/`HttpResponse` 走 `msw/http`、GraphQL link-first；**Node ≥22 硬要求** | kb/testing.md「版本注意」/ 坑点 9 |
| 48 | error.tsx 解构 `reset` | Next 16 props 是 `{ error, retry }`——reset 未定义运行时崩 | kb/nextjs.md 速查表 |
| 49 | BullMQ `@Process('name')` | 不支持——WorkerHost.process + `switch (job.name)` 分发；repeat 从 add() 移除→upsertJobScheduler | kb/nestjs.md 场景：队列 |
| 50 | helmet 手动接入 Nest | 12.1+ 内置 `app.useSecurityHeaders()` 同默认值免依赖；listen 前调用 | kb/nestjs.md 场景：安全头与限流 |
| 51 | pnpm 12 CLI 写法盲答 | Rust 重写已 stable：`--frozen-lockfile false` 被拒→`--no-frozen-lockfile`；`--resolution-only` 移除→`pnpm peers check` | kb/monorepo.md 坑点 12-13 |
| 52 | TS 7 盲答升级 | 7.0 无程序化 API；typescript-eslint 不支持（peer <6.1.0）；Vue/MDX/Astro/Svelte（Volar 型）不能上；TS 6.0：baseUrl 移除/types 默认 []/target es5 硬错误 | kb/monorepo.md 坑点 14-16 |
| 53 | turbo 远程缓存签名失败静默降级 | 校验失败按 cache miss 重跑；日志也被缓存 replay——CI 日志确认命中数 | kb/monorepo.md 坑点 17 |
| 54 | Vitest 5 升级双雷 | `clearMocks` 默认 true（清掉 setup 记录的调用）；非顶层 vi.mock/vi.hoisted 从警告升级为抛错 | kb/testing.md 坑点 10-11 |
| 55 | Playwright 组件测试包已移除 | `@playwright/experimental-ct-*` 停发（锁 1.62）；新模式 story gallery + `fixtures.mount()` | kb/testing.md 坑点 13 / [TE-12] |
| 56 | Playwright 系统要求盲答 | Node 仅 22.x/24.x/26.x（**20 已不支持**）+ Windows 11+（或 WSL）+ macOS 14+；CI 镜像核对 | kb/testing.md「版本注意」 |
| 57 | Next 16.3+ dev 慢导航报 error | Cache Components 下未 Stream/Cache 的导航即阻塞——Instant Insights | `<Suspense>`/`'use cache'`/`export const instant = false`；kb/nextjs.md 坑点 14 |
| 58 | 自托管 Next shell 被投毒/持久 404 | `next start` + Cache Components + **Partial Prefetching 未开**（GHSA-pc58） | `partialPrefetching: true` + 升 16.4.6；kb/nextjs.md [NX-12] |
| 59 | use cache 结果跨租户泄漏 | 读 root 参数的 use cache 又被 unstable_cache 包装（GHSA-mfr8 High） | 升 16.4.6/15.5.29；拆开组合；kb/nextjs.md [NX-13] |
| 60 | Activity 隐藏后媒体继续播放 | hidden 保留 DOM（display:none 不停 video/audio/iframe） | `useLayoutEffect` cleanup 暂停；kb/react-core.md 坑点 10 |
| 61 | useEffectEvent 当通用回调用 | 只能 effect/Effect Event 内调用——渲染期/事件处理器/传子组件均报 lint 错 | 通用回调用普通函数/useCallback；kb/react-core.md 坑点 11 |
| 62 | Compiler 项目删手写 memo | 删除会改变编译输出，性能回归无告警 | 存量保留或删前充分测试；新代码依赖编译器；kb/react-core.md 坑点 12 |
| 63 | Nest gateway 写了但不工作 | 未注册进 module providers 数组——不实例化、无报错 | `providers: [EventsGateway]`；kb/nestjs.md 坑点 11 |
| 64 | WS handler 不想回消息却回了 | false/0 等 falsy 返回值仍发送 | 省略 return 或显式 return null；kb/nestjs.md 坑点 12 |
| 65 | CQRS 事件 handler 抛错全局 filter 没接住 | 事件 handler 在 HTTP 请求上下文之外 | try/catch / 补偿 saga / UnhandledExceptionBus；kb/nestjs.md 坑点 13 |
| 66 | 微服务 pattern 匹配不上但代码"正确" | 超 5 层嵌套/20 键/100 总键 → `[TOO_MANY_KEYS]` 标记替换 | pattern 精简扁平；kb/nestjs.md 坑点 14 |
| 67 | 生产环境 GraphiQL 消失 | NODE_ENV=production 自动关；playground 已是弃用别名 | `graphiql: true` 显式开；kb/nestjs.md 坑点 15 |
| 68 | Suspense 页多查询逐个出数据 | 多个 useSuspenseQuery 串行 suspend → 请求瀑布 | useSuspenseQueries 并行；kb/tanstack-query.md 坑点 9 |
| 69 | 持久化缓存提前蒸发 | gcTime（默认 5min）< maxAge（默认 24h），缓存先被 GC | gcTime ≥ maxAge + PersistQueryClientProvider；kb/tanstack-query.md 坑点 10 |
| 70 | invalidateQueries 对某查询无效 | 误用 staleTime: 'static'（连手动失效都阻断） | 可失效数据改 staleTime: Infinity；kb/tanstack-query.md 坑点 11 |
| 71 | tRPC 失效/预取数据永不命中手写 key 的查询 | 手写 queryKey 与 trpc 键体系脱钩 | trpc 工厂 queryOptions/queryFilter/pathFilter；kb/tanstack-query.md [TQ-13] |
| 72 | tRPC 生产环境内部错误信息（表名/查询）直达客户端 | 非 TRPCError 的 message 原样发送（生产也是） | errorFormatter 替换 INTERNAL_SERVER_ERROR message + onError 上报；kb/tanstack-query.md 场景 tRPC |
| 73 | tRPC middleware try/catch 捕不到 procedure 错误 | opts.next() 不抛错，resolve 为 { ok: false, error } | 检查 result.ok 再上报；kb/tanstack-query.md 冲突消解 |
| 74 | zod v4 下 z.record 单参/enum 键缺项报错 | v4 双参强制；enum 键穷尽校验 | `z.record(keySchema, valueSchema)`；部分键用 `z.partialRecord()`；kb/react-core.md 场景 Zod v4 |
| 75 | z.object({ a: z.any() }).parse({}) v4.4+ 失败 | any/unknown 键类型不再可选，parse 时也必填 | 缺键合法须显式 `a: z.any().optional()`；kb/react-core.md 场景 Zod v4 |
| 76 | zod v4 .default() 校验不过或类型不符 | v4 短路语义：默认值须匹配 output 类型且不执行校验 | 旧 parse 默认值行为改用 `.prefault()`；kb/react-core.md 冲突消解 |
| 77 | v4 下对象缺 z.coerce 字段或 safeParse 换 locale 不生效 | 缺键从静默转换变报错；safeParse 错误懒构建（首次读 result.error 才跑 error maps） | coerce 字段显式 `.default()`；locale 在 parse 前配置或用 throwing `.parse()`；kb/react-core.md 场景 Zod v4 |
| 78 | 改了 prisma.config.ts 的 datasource.url 但应用连接没变 | Prisma 7 连接双轨：config URL 只供 CLI，应用连接在驱动适配器构造处 | 同步改适配器 `new PrismaPg({ connectionString })`；kb/nestjs.md 场景 Prisma 7 |
| 79 | React Router v8 下 `from "react-router-dom"` 全挂 | v8 移除 react-router-dom 包 | `RouterProvider`/`HydratedRouter` 改从 `react-router/dom`，其余从 `react-router`；kb/react-core.md 场景 React Router 7/8 |
| 80 | Tailwind v3→v4 升级后样式不报错但视觉全变 | 高危改名静默漂移：shadow-sm/rounded/ring（3px→1px+currentColor）/outline-none→outline-hidden/默认 border 色变 currentColor | `npx @tailwindcss/upgrade` 自动迁移 + 对照改名表人工 review；kb/vite-tooling.md 场景 Tailwind v4 |
| 81 | Drizzle 代码按 v1 API 写在 0.x 项目跑挂（或反之） | **v1.0 过渡期**：stable=0.45.4/kit 0.31.11，v1.0-rc.5 在 RC；relations/casing（`drizzle({casing})` v1 移除）/校验包路径（drizzle-zod→drizzle-orm/zod）/迁移目录结构（journal.json v1 移除）全断裂 | 先 `npm ls drizzle-orm` 确认版本线再写；kb/nestjs.md 场景 Drizzle ORM |
| 82 | Next 16 缓存失效 API 混用（updateTag 传 profile/revalidateTag 单参） | **updateTag(tag) 单参数仅 Server Actions 立即过期**；revalidateTag(tag, profile) 才是双参（'max'=stale-while-revalidate，不传 profile=legacy 立即过期） | read-your-own-writes 用 updateTag；webhook/Route Handler 用 revalidateTag；kb/nextjs.md 场景 'use cache' 编排 |
| 83 | TanStack Start server function 鉴权只做在 beforeLoad | server fn 是独立可达 endpoint，**beforeLoad 不是数据边界**——每个读写私有数据的 fn 自带 authMiddleware；同源校验（Fetch Metadata/Origin/Referer）只是 CSRF 防线 | kb/react-core.md「TanStack Start/Router」场景 |
| 84 | Apollo Client 4 升级后 useQuery/ApolloProvider 导入报错、ApolloError 判型失效 | **React 导出移至 `@apollo/client/react`**（核心入口无 React API）；**ApolloError 类移除**——判型用 `CombinedGraphQLErrors.is(error)`/`ServerError.is(error)`；hooks 的 onCompleted/onError 移除→await promise | kb/tanstack-query.md「GraphQL 客户端（Apollo Client 4）」场景 |
| 85 | Better Auth：server action 里调 signOut 等需设 cookie 的函数，用户没真正登出（静默失效） | Server Actions 须用 Next `cookies()` 设 cookie——Better Auth 的 Set-Cookie 头被忽略 | MUST 加 `nextCookies()` 插件（better-auth/next-js，plugins 数组最后一个） | kb/nextjs.md「鉴权库（Better Auth 1.7）」场景 |
| 86 | Stripe webhook 验签恒失败（签名不匹配），JSON 解析后的 body 再序列化验签也一样 | 签名基于**未改动 raw body**——框架 body parser/中间件改动或重新序列化即破坏签名 | route handler 用 `await req.text()` 原文验签 `constructEvent(rawBody, sig, secret)`；勿让 body parser 先跑 | kb/nextjs.md「支付（Stripe Checkout Sessions）」场景 |
| 87 | dnd-kit 代码生成后 API 对不上（listeners/attributes 不存在 或 event.over undefined） | **双线并存且 API 完全不兼容**：新 @dnd-kit/react（useDraggable 返回 {ref}、DragDropProvider、event.operation.target）/ 旧 @dnd-kit/core（listeners spread、DndContext、event.over） | 先 `npm ls @dnd-kit/react @dnd-kit/core` 确认版本线再写；旧线（2024-12 停更 Legacy）新项目勿选 | kb/react-core.md「拖拽（dnd-kit 新旧双线）」场景 |
| 88 | Sentry 生成代码对不上：sentry.client.config.ts 不被加载、onRequestError 不存在、OTel 配置失效 | **v7-v11 五版本线并存**（dist-tags 各自活跃）；v8+ 改 instrumentation-client.ts 三文件结构；v10/v11 OTel 文档分开不互通 | 先 `npm ls @sentry/nextjs @sentry/nestjs` 确认大版本；v11 按 instrumentation.ts register() + NEXT_RUNTIME 动态导入 + onRequestError 结构写 | kb/nextjs.md「错误监控（Sentry v11）」场景 |
| 89 | Next.js standalone 部署后静态资源全 404（JS/CSS/图片缺失） | `output: 'standalone'` 的 `.next/standalone/` **不含 `public/` 与 `.next/static/`**（设计上交给 CDN） | build 后 MUST 手动 `cp -r public .next/standalone/ && cp -r .next/static .next/standalone/.next/`（Dockerfile 单独 COPY 两层） | kb/nextjs.md「自托管与多实例部署」场景 |
| 90 | Next.js 多实例（K8s/LB）偶发 "Failed to find Server Action"、各实例缓存失效互不可见 | Server Functions 闭包用 **build 时生成的加密 key** 加密——各实例 key 不同无法互解；revalidateTag 默认只失效本实例 | 全实例同 `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`（base64 AES 16/24/32 字节）；共享 cacheHandler + `refreshTags()` 每请求同步 tag 状态 | kb/nextjs.md「自托管与多实例部署」场景 |
| 91 | NestJS 官方一等包（@nestjs/ai·mcp·resilience·idempotency·outbox）代码对不上或 API 不存在 | **一等包大多 0.0.x-0.1.x pre-stable 刚发布**（文档已全量上线、训练记忆主流仍是第三方包或不存在）；版本间 API 变动频繁 | 生成集成代码前 `npm ls @nestjs/ai @nestjs/mcp @nestjs/resilience @nestjs/idempotency @nestjs/outbox` 确认是否已装及版本；未装时默认成熟第三方路线并评估 0.0.x 风险 | kb/nestjs.md「AI 集成与 MCP server」「弹性与可靠性」场景 |
| 92 | NestJS 一等包（idempotency/outbox/workflows/webhooks/locks）生产启动失败 "no store is registered, and NODE_ENV is \"production\""，或不知道生产库 schema 怎么建 | 五包同一契约：默认 InMemory 仅排除本进程，**production 无共享 store 直接拒启动**（allowInMemoryStorage:true 豁免）；schema nest_* 由 store 自建 | 注册各包 Postgres store（executor 用 fromDrizzle/fromTypeOrm/fromPrisma/fromKysely）；dev 启动自迁移，生产跑 `npx <pkg> migrate`（`status` 退出码 1 作 CI 检查）或 migrationSql() 并入自有迁移 | kb/nestjs.md「webhooks、邮件与文件存储」场景共性契约段 |
| 93 | Prisma 项目 `npm i prisma` 后 migrate/generate/db push 全部消失或不读 schema.prisma（CLI.COMMAND_MOVED / "no generate, migrate dev or db push commands"） | **prisma@latest = 8.0.0-rc.34（ORM 8 RC）**：不读 schema.prisma、无 generate/migrate dev/db push，且 v7 项目装 latest 会原地顶掉 v7 CLI；@prisma/client 停在 7.10.1 无 8.x | v7 项目锁 `prisma: "^7"` + `@prisma/client: "^7"`、CI 用 `npx prisma@7`；新 ORM 8 项目用 `@prisma/orm-postgres` + contract.prisma（首行 `// use prisma-8`）+ `contract emit`；生成 Prisma 代码前先 `npm ls prisma @prisma/client` | kb/nestjs.md「Prisma（v7 现役 / v8 RC 双线）」场景 |
| 94 | turbo 旧旗标/命令还在 CI 脚本里（turbo-ignore、--parallel、--no-cache、TURBO_REMOTE_ONLY、--daemon、prune --scope、根级 globalDependencies/globalEnv） | 已全部 Deprecated（support-policy 官方清单）；turbo-ignore → `turbo query affected`；--no-cache → `--cache=local:r,remote:r`；TURBO_REMOTE_ONLY → TURBO_CACHE；根级 global* → globalConfiguration Future Flag | 新代码禁用；存量脚本按弃用清单逐项替换（turbo query affected 旗标映射 --task→--tasks、--fallback→--base） | kb/monorepo.md「架构守护与多技术栈」场景 + 支持策略 |
| 95 | Nest 可观测性代码跑不对：@nestjs/observe 配了却无数据（Fastify）、TracerService 请求外抛错、OTel Nest span 全无、微服务 trace 断链、APM agent 时有时无 | ① FastifyAdapter 下 options 须挪第三参（第二参被静默丢弃 SDK 永不挂上）；② TracerService 从 ambient async context 读 trace——请求外调 createSpan 抛错是故意设计；③ `@opentelemetry/instrumentation-nestjs-core` 仅支持 core <12，Nest 12 上三个 Nest span 全无；④ microservices trace 自动传播有版本门槛（12.0.4 TCP/Redis、12.3.3 NATS/Kafka/RabbitMQ/MQTT 5/gRPC）；⑤ 通用 APM agent 必须 preload 先于 @nestjs/core/AppModule（--require/--import），模块内启动不可靠 | Fastify 用 `create(AppModule, adapter, { instrument })`；请求外只用 currentTraceId()（返 null）/自定义指标/手动 span 包裹；Nest 12 要 Nest 构件级 span 用 Observe（instrument 钩子）或 Sentry；旧版 microservices 手动转发 trace id + 覆写 traceIdGenerator；APM agent 一律 preload（Node 22.12 以下出站 header 注入也要补拦截器） | kb/nestjs.md「可观测性（NestJS Observe 深化 / OpenTelemetry 双轨）」场景 |
| 96 | @nestjs/authentication/authorization 代码对不上或启动即挂：peer 冲突装不上、装上了 NODE_ENV=production 拒启动、AuthenticationModule/AuthorizationModule 顺序错 startup 失败、生产库缺表、graphql-ws/WS 下拿错 user | ① 两包 **peer 仅 @nestjs ^12.0.0（Nest 12 专属）**，Nest 11 装不上是设计不是 bug；② 六 store 契约同 idempotency/outbox 模式——**production 无注册 store 拒启动**（8 张 Drizzle 表自建）；③ **AuthenticationModule 必须在 AuthorizationModule 之前 import**（全局 guard 按模块序跑，反了 startup 失败）；④ WS/graphql-ws 下 client.user/req.user 是**最后一次认证的 user**（可能错人）——defaultGetUser 优先查 `Symbol.for('nestjs.authentication.userOf')` 按消息取对的 user；⑤ 配 mfa 无 encryption 在 startup throw（TOTP secret 须 AES-256-GCM 加密入库） | Nest 11 项目走 @nestjs/passport 既有路线；生产先注册 store + `authenticationStoreContract({ concurrent: true })` 契约测试（PGlite+PG 双跑）；模块顺序固定认证在前；WS 场景勿读 req.user、用包提供的 per-message 取值；MFA 必配 encryption keys（数组新 key 在前可轮换） | kb/nestjs.md「鉴权与授权（@nestjs/authentication+authorization 官方双轨 / Passport 既有路线）」场景 |
| 97 | Drizzle v0→v1 升级踩雷：升完 push/pull 开始动 public 以外的 schema、postgres-js JSON 列数据变双重序列化、db.query 过滤器传 `id: undefined` 直接 throw、迁移没按时间戳顺序被跳过、`push --strict`/`--ignore-conflicts` 报未知旗标 | ① v1 **schemaFilter 默认管理所有 schema**（0.x 仅 public）——升级即碰别人 schema，须显式 `schemaFilter: ['public']`（支持 glob）；② v1 postgres-js 驱动自序列化 JSON——旧手动 `JSON.stringify` 补丁 MUST 删；sql 模板内 JSON 数组包 `sql.param(arr)`；③ v1 关系查询**拒绝显式 undefined**——`id: value ?? EmptyFilter`（`drizzle-orm/relations`）或省略字段；`posts: true/false` 是存在检查、`{ posts: {} }` 是跳过；④ v1 migrator **应用所有缺失迁移**（与时间戳顺序无关）；迁移按文件夹名匹配（迁移表新列 name+applied_at）；⑤ `--strict` 移除（严格成默认，`--force` 跳过）、`--ignore-conflicts` 移除 → `generate --fix-conflicts --explain`（修复删冲突迁移及子代，跑过的库须重置） | 升级走官方三步：`drizzle-kit up` → 改代码 → RQB v2 迁移；schemaFilter 显式收窄；删 JSON 序列化补丁；undefined 过滤改 EmptyFilter；冲突迁移先 --explain 预览再修 | kb/nestjs.md「Drizzle ORM（v1.0 过渡期）」场景 |
| 98 | Drizzle Pulse 实时层启动失败或不生效：连不上/启动报错、复合 PK 表被拒、args 校验用 async refinement 直接 throw、启动后新建 query 不触发、断线重连后 UI 停在旧数据、CDC 副作用重复执行、async listener 偶发进程崩溃 | ① PG **`wal_level = logical` 必须自设**（默认 replica），Pulse 只自建其余 DB 对象；② **源表必须单列 PK**（复合 PK 拒绝；PK 类型白名单 int/serial/text/uuid 族）；③ `.args(schema)` 走 Standard Schema **须同步校验**，async refinement throw；④ **queries 必须启动时一次定义传 createRuntime**——后建的 query runtime 不认识，每请求值用 args 传；⑤ 断线重连 **onChange 不补发丢失变更**——用 state 渲染的代码必须注册 onResync 重发全量；CDC 同 commit 断线后**可重复投递**——副作用用 `(event.pk, lsn)` 幂等键；⑥ listener 同步调用**不等待返回的 Promise**——async listener 内部不自捕获 = unhandled rejection 杀进程 | 渲染列表用 live collection（list()/onChange/onResync 三件套），CDC 流只做反应式副作用；先设 wal_level、确认单列 PK 再接 Pulse | kb/nestjs.md「Drizzle ORM（v1.0 过渡期）」场景 Pulse 段 |
| 99 | Context provider 内联对象/函数 value | 每渲染新引用 → 全体 consumer 重渲染；`memo` 挡不住 context 更新传播 | useMemo 包对象 + useCallback 函数成员 [RC-14]；kb/react-core.md 坑点 19 |
| 101 | Nest 内存缓存 `get()` 返回对象改了，缓存跟着变 | store 存**引用**不存副本，修改即污染缓存 [NE-13] | 缓存值只读或拷贝后修改；kb/nestjs.md 坑点 20 |
| 103 | react-admin alwaysOn 过滤器配 defaultValue 不生效 | 技术限制互斥 [RA-14] | `<List filterDefaultValues>`；kb/react-admin.md 坑点 21 |
| 104 | ReferenceInput 上的 validate/label/format/parse 无效 | 通用 props 归内嵌子组件，传本体静默无效 [RA-13] | 传给子组件；kb/react-admin.md 坑点 17 |
| 105 | metadataBase 未设，OG/canonical URL 拼错 | 相对 URL 无基准 [NX-14] | metadataBase 或 env `NEXT_PUBLIC_METADATA_BASE_URL`；kb/nextjs.md 坑点 20 |
| 106 | 启动钩子里 emit 的事件监听器没收到（静默失效） | bootstrap 前监听器未注册完 [NE-12] | 先 `await readinessWatcher.waitUntilReady()` 再 emit；kb/nestjs.md 坑点 16 |

## 来源索引

- 本文件全部条目汇总自各 subdomain kb 的「高频坑点」章节，逐条来源标注见对应文件（kb/react-core.md、kb/nextjs.md、kb/nestjs.md、kb/react-admin.md、kb/tanstack-query.md、kb/vite-tooling.md、kb/testing.md、kb/monorepo.md）
- [官方文档]/[模型经验] 的划分以详情条目为准，本文件不重复标注

## 冲突消解记录

无独立冲突条目；版本相关坑点（#2/#6/#13 等）的冲突消解见对应 subdomain kb 文件的「冲突消解记录」。

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| R43（第四十三轮） | 补账：新增 #104（RA-13）/#105（NX-14）/#106（NE-12）——原轮漏横切对账，项目评审后补 | 2026-11-17 |
| R44（第四十四轮） | 补账：新增 #99-103（RC-14/NX-15/NE-13×2/RA-14）——原轮漏横切对账，项目评审后补 | 2026-11-17 |
