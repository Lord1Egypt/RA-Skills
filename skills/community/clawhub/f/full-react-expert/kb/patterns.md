---
type: cross-cutting
name: patterns
version: 29
updated: 2026-11-17
---
# 通用模式与选型决策

跨子领域通用：全栈选型、项目结构、性能分层、测试策略、monorepo 策略。约束性原则（MUST/NEVER）不在此文件——统一见 `kb/laws.md`（全局宪法）与各 subdomain kb「法则」小节；本文件提供**建设性路径**（场景 → 选型/结构）。

## 全栈架构选型（do/don't）

典型 React 全栈组合与职责切分 [模型经验]：

| 层 | 选型 | 职责边界 |
|---|---|---|
| 页面/渲染 | Next.js App Router | 页面、路由、SEO、BFF（薄） |
| 业务 API | NestJS | 业务逻辑、校验、事务、认证、微服务 |
| 管理后台 | react-admin（独立 SPA） | CRUD 后台，对接 Nest API |
| 客户端态 | zustand（小） / Redux Toolkit（大团队） | 仅客户端 UI 态 |
| 服务端数据 | TanStack Query / RSC 直取 | 缓存、失效、去重 |
| 表单 | react-hook-form + Zod | 非受控、schema 校验 |
| 构建 | Vite（SPA/库）/ Turbopack（Next 内置） | 纯 SPA 与库用 Vite 8 |
| Monorepo | pnpm + Turborepo + changesets | 依赖/任务/发布三分 |

- don't：Next API Routes 里写业务逻辑 + Nest 里再写一遍（双写漂移）
- do：业务逻辑只住一处（Nest），Next 只做转发/聚合 [模型经验]

## 现代运行时与轻量后端选型（Bun / Hono）

**Bun（1.4.4）**：all-in-one 单二进制——runtime + PM（30× npm，global cache + workspaces）+ 测试跑器（Jest 兼容）+ 打包器 + `bun check`（全核并行类型检查）/`bun lint`（1000 内建规则零配置）/`bun fmt`。Rust 编写、**JavaScriptCore 引擎（非 V8）**、启动 4× Node、TS/JSX 直接执行、ESM+CJS 双兼容、Web 标准 API（fetch/WebSocket/ReadableStream；Headers/URL 直用 Safari 实现）、`bunx` 执行包。定位：**Node drop-in 替代**——但 **Node 兼容（node: 模块/process/Buffer）是进行中努力，重度依赖 Node 原生生态的项目迁移前必查 compat 表**；团队工具链混用（pnpm 工作流）时仅作运行时即可受益。

**Hono（4.13.19；5.0 在 RC 未 stable，next tag=5.0.0-rc.1）**：Web Standards 极简超快后端框架。多运行时一份代码（Cloudflare Workers/Fastly Compute/Deno/Bun/Vercel/Netlify/AWS Lambda/Lambda@Edge/Node 经 @hono/node-server 2.1.8——Node ≥20）；**三路由器**：RegExpRouter（单一大正则派发最快）/LinearRouter（注册快——适合每次初始化的环境如 serverless 冷启动）/PatternRouter（最小），SmartRouter 组合派发；hono/tiny <14KB（对照 Express 572KB）；内建中间件面：JWT/bearer-auth/basic-auth/CORS/secure-headers/body-limit/cache/compress/etag/logger/pretty-json/streaming/SSG/GraphQL server；Context 对象 + 路径参数字面量类型；**RPC 模式**（Validator + `hc` client）端到端类型安全，tRPC 同类但跨 runtime；`npm create hono@latest` 脚手架。

选型判定 [模型经验]：

| 需求 | 选 | 理由 |
|---|---|---|
| 企业级业务 API（DI/模块/微服务/GraphQL/队列） | NestJS | 结构化重框架，生态完整 |
| Edge/CDN/Workers 后端、代理、轻 API | Hono | Web Standards、冷启动零负担 |
| 全栈 TS 同仓类型安全 API（Node 单一运行时） | tRPC 或 Hono RPC | 端到端类型无需 schema 双写 |
| 运行时/工具链提速 | Bun | PM/测试/打包一体化 |
| 混合部署（同代码多平台） | Hono | 多 runtime 适配器成熟 |

- 来源：[官方文档](https://bun.sh/docs) + [官方文档](https://hono.dev/docs) + registry 锚定（2026-11-16 锚定、2026-11-17 复核 hono 4.13.19 补丁无语义变化）

## Node.js 运行时版本基座（2026-11 锚定）

现行 LTS 三线（生产只用 Active/Maintenance LTS）：

| 线 | 代号 | 首发 | 最新 patch（2026-11） | 状态 |
|---|---|---|---|---|
| **v26** | Lithium | 2026-05-05 | 26.13.1 | **最新 LTS** |
| **v24** | Krypton | 2025-05-06 | 24.22.3 | LTS |
| **v22** | Jod | 2024-04-24 | 22.23.5 | LTS（多数工具 engines 下限） |
| v20 | Iron | 2023-04-17 | 20.20.2 | **已 EOL（2026-03-24）** |
| v27 | - | 2026-10-29 | 27.0.0-alpha | Alpha |

- **Node 20 已 EOL 是关键基座事实**：Vite 8/Rspack/Vitest/Storybook 的 engines `^20.19||>=22.12` 中 **20 线已死**——生产基座应取 22/24/26（Playwright 1.65「仅 Node 22/24/26」即现行 LTS 三线；msw 3 `Node >=22`；testcontainers `>=22.22` 均为 LTS 线内 patch 门槛）
- **发布周期变更**：至 Node 26 为止历史模式（奇数 6 个月不支持、偶数进 Active LTS）；**从 Node 27 起改年度发布**——每个大版本 6 个月 Current + 6 个月 Alpha 后进 LTS；LTS 总计 30 个月支持
- 来源：[官方文档](https://nodejs.org/en/about/previous-releases)（nodejs.org 可抓，2026-11-17）

## 服务端状态 vs 客户端状态（最重要的一条架构线）

- **服务端状态**（API 数据）：交给 TanStack Query / SWR / RSC 直取——缓存失效、去重、重试是库的职责，**永远不要**手动塞进全局 store 再手写 loading/error [模型经验]
- **客户端状态**（UI 态）：useState 起步，跨组件共享才上 zustand/context
- 混用是最大架构坑：Redux 里存 API 响应 + 手动同步 = 永远修不完的 stale bug
- RSC 分层（Next App Router）：首屏/SEO 数据 RSC await 直取（不进 queryClient）；交互式数据（筛选/无限列表/仪表盘）才 TanStack Query → 见 kb/tanstack-query.md

## Next.js + NestJS 对接模式

- Nest 全局前缀 `/api` 或独立域名；CORS 白名单 `app.enableCors({ origin: [webOrigin] })`
- 错误契约：Nest 统一 exception filter 输出 `{ statusCode, message, error }`；前端按结构化格式提示
- 环境变量分侧：Nest 侧 DB 密钥不进前端仓库；前端只碰 `NEXT_PUBLIC_*` [模型经验]

## react-admin + NestJS 对接契约

- 实现 DataProvider 映射层：`page`=从 1 起、`sort.order`='ASC'|'DESC'、getList → `{ data, total }`
- 错误必须非 2xx + JSON（react-admin `checkError({ status })` 依赖 status 驱动登出/通知）
- 先用 Guesser 生成再定制，勿从零手写全部列表组件 [官方文档](https://marmelab.com/react-admin/Tutorial.html)

## 性能优化分层（从高到低优先级）

1. **网络/数据**：bundle 拆分（next/dynamic）、代码删减、HTTP 缓存——收益最大
2. **避免不必要渲染**：context 拆分、状态下沉、组合模式（children）
3. **渲染变便宜**：虚拟化列表（react-window/TanStack Virtual）
4. **memo 微优化**：React Compiler（1.0 已稳定）自动 memo 化优先于手写 [官方文档](https://react.dev/blog)

- 纪律：**先 Profiler 测量再优化**；"重渲染了"不等于"有性能问题" [模型经验]

## 项目结构参考 [模型经验]

```
apps/
  web/            # Next.js App Router
    app/(routes)/...
    components/
  api/            # NestJS
    src/modules/{user,order}/
      user.{controller,service,module,dto}.ts
  admin/          # react-admin SPA
    src/resources/{posts,users}/
packages/
  shared-types/   # 前后端共享 DTO/类型（单一来源）
```

- 关键：**共享类型包**（packages/shared-types）由后端 DTO 生成或手写，前端 import——契约漂移在编译期暴露
- monorepo 化：pnpm-workspace.yaml 声明 apps/packages；`workspace:*` 互引；turbo 编排 build/dev/test → 见 kb/monorepo.md

## 测试策略 [模型经验]

| 层 | 工具 | 测试对象 |
|---|---|---|
| React 组件 | Testing Library + Vitest | 交互行为，不测实现细节 |
| hooks | renderHook | 依赖数组/竞态场景 |
| Nest 单元 | Vitest（Nest 12 ESM 默认）/ Jest（CJS） | Service 纯逻辑，mock repository |
| Nest e2e | Supertest + Test.createTestingModule | 路由 + 校验管道 + DI 全链 |
| 全链 | Playwright | 关键用户旅程（storageState 复用登录态） |

- Nest 测试高频坑：TestingModule 忘 `.compile()`；overrideProvider 顺序在 compile 前 [模型经验]
- Jest 加载 Nest 12 ESM 需 Node 24.9+（`ERR_REQUIRE_ASYNC_MODULE`），新项目选 Vitest [官方文档](https://docs.nestjs.com/migration-guide)

## 版本联动检查表

升级前核对（硬事实锚点见各 kb「版本注意」）：

| 组件 | 当前锚定 | 联动要求 |
|---|---|---|
| React | 19.3 | Next 16 锁 React 19；react-admin 需 React 18+ |
| Next.js | 16.4.6 | Node 20.9+、TS 5.1+；15 线仅安全维护；16 缓存模型 Cache Components（**16.4 官方推荐所有应用，Next 17 默认**）；16.3 Instant Navigations（Stream/Cache/Block）；安全线 16.4.5/15.5.29（2026-11 七 CVE） |
| next-intl | 4.15.1 | peer Next 12-16 全线 + React 16.8-19；App/Pages Router 双支持；**proxy.ts 是 middleware.ts 在 Next 16 的新名字**；无 locale 时 notFound() 中止渲染（须配 not-found 页） |
| better-auth / next-auth | 1.7.25 / 4.24.15 | Better Auth 活跃（2026-11）；**next-auth v5 长期 beta 未 stable——新项目选 Better Auth**；Better Auth peer Next 14-16/React 18-19；Express v5 挂载通配符 `/{*any}` |
| xstate / @xstate/react | 5.33.4 | **v5 actor model**（interpret→createActor/services→actors/onDone event.output）；**6.0 已进 beta（6.0.0-beta.3）仍未 stable，锁 5.x**；useSelector 默认严格 === |
| jotai | 3.0.2 | **v3：peer React ≥18 硬门槛**（v2 支持 16.8+）；原子化状态（最小核心 2kb，无字符串 key）；jotai.org 文档站不可达 |
| bun | 1.4.4 | Rust+**JavaScriptCore（非 V8）**；Node drop-in 但 **node: 模块兼容进行中**；PM 30× npm；bun check/lint/fmt 内建 |
| hono / @hono/node-server | 4.13.19 / 2.1.8 | **5.0 在 RC 未 stable（锁 4.x）**；多运行时一份代码；RegExpRouter；Node 适配 ≥20；RPC 模式（hc + Validator）端到端类型安全 |
| uploadthing | 7.7.4 | **2025-08 后未再发版（评估维护风险）**；v7：UPLOADTHING_TOKEN 单环境变量、presigned URL 自家服务端生成、awaitServerData 默认 true；客户端 bundle ~25kB |
| multer / @nestjs/platform-express | 2.5.0 / 12.5.0 | **Multer 默认不限大小 + 默认 memoryStorage——MUST limits.fileSize**；Fastify 侧（@fastify/multipart）fileSize 默认 1 MiB 更严；12.5 起 limits.parts 默认 1000 |
| stripe / @stripe/react-stripe-js | 23.1.0 / 7.1.0 | **官方推荐 Checkout Sessions + Payment Element（Payment Intents 仅显式要求时）**；新 React API 走 `@stripe/react-stripe-js/checkout` 子路径（CheckoutElementsProvider/useCheckoutElements/checkout.confirm）；Session 24h 过期；webhook 验签 MUST raw body（`await req.text()`）；事件无顺序保证——event ID 幂等去重；Node ≥20 |
| recharts | 3.10.1 | **v3 断裂面：Cell 弃用→shape、activeIndex 移除→Tooltip、responsive prop（3.3+）取代 ResponsiveContainer**；peer react-is；内部 Redux/es-toolkit/victory-vendor（D3） |
| dnd-kit（新线 @dnd-kit/react / 旧线 @dnd-kit/core） | 0.5.3 / 6.3.1 | **双线 API 完全不兼容**：新线 ref API + event.operation.target（活跃）/ 旧线 listeners spread + event.over（2024-12 停更 Legacy，新项目勿选）；新线 peer React 18/19、框架无关核心 |
| date-fns / @date-fns/tz | 4.4.0 / 1.5.0 | v4 一等时区（breaking 极少：ESM-first .cjs 反转）；**结果归一到第一个对象参数的时区（参数顺序影响结果）**；`{ in: tz(...) }` 显式指定；`new TZDate("Asia/Singapore")` 是 Invalid Date（用 TZDate.tz()）；v5 alpha |
| @react-email/components / resend | 1.0.12 / 6.38.1 | 同团队推荐搭配；SDK `{data, error}` 不 throw；react 参数函数调用非 JSX；10 req/s；idempotencyKey `<event-type>/<entity-id>`；Node ≥20 |
| @sentry/nextjs / @sentry/nestjs | 11.12.0 | **v7-v11 五版本线并存（先 npm ls 确认）**；v11 三文件初始化（instrumentation-client.ts + server/edge config）+ instrumentation.ts register() 按 NEXT_RUNTIME 动态导入 + onRequestError；tunnel route 版本门槛 v11≥11.9.0；Node ≥20.19.0 |
| NestJS 部署与一等包（nest deploy / Mau / Observe / 可靠性 AI MCP 系列） | v12 CLI / observe 0.3.26 / ai 0.0.2 / mcp 0.0.4 / resilience 0.0.3 / idempotency 0.0.4 / outbox 0.1.4 | **文档站已重构**（application/http/observability/reliability/mcp/ai 分区）；**一等包大多 pre-stable 0.0.x——生产选用前评估（gotchas #91）**；@nestjs/ai 绑 AI SDK 7 + Node ≥22；IdempotencyModule 先于 ResilienceModule；outbox MUST 传事务句柄；`nest deploy` + @nestjs/mau 官方 AWS 平台；**Observe 需 core ≥11.1.4 instrument 钩子（Fastify 下 options 第三参），通用 APM agent 必须 preload 先于 AppModule（gotchas #95）** |
| NestJS | 12 | Node 20.19+/22.12+（运行）；TS 6；`nest upgrade` 逐级升 |
| react-admin | 5.15.7 | React 18+；v5.8 起推荐 DataTable |
| React Router | 8.5.1（v7 线 7.18.5） | **v8：Node ≥22.22 / React ≥19.2.7 / Vite 7+ / ESM-only**；react-router-dom 包移除（`react-router/dom`）；middleware 恒开；8.5 弃用自带 View Transition API → React 19.3+ `<ViewTransition>` |
| TanStack Query | 5.107.1 | v5 对象语法 |
| Vite | 8.3.8（**8.4.0-beta.1 通道推进中**） | Rolldown+Oxc 全链；v8 移除 manualChunks 对象形式、`rollupOptions`→`rolldownOptions`；Node 20.19+/22.12+ |
| Vitest | 5.1.0 | **v5 硬门槛 Vite ≥6.4 + Node ≥22.12（vite 为 peer dep，Yarn 显式装）**；clearMocks 默认 true；非顶层 vi.mock 抛错；json/junit 默认写 .vitest 目录 |
| Playwright | 1.65.1（Chromium 159） | **Node 仅 22.x/24.x/26.x（20 已弃）+ Windows 11+**；`playwright install --with-deps`；月更节奏；`experimental-ct-*` 已移除（组件测试走 story gallery + `fixtures.mount()`） |
| Turborepo | 2.11.11 | turbo.json 用 `tasks` 键；Remote Cache 产物签名 remoteCache.signature（HMAC-SHA256，校验失败按 cache miss）；CI 裁剪用 `turbo query affected`（turbo-ignore 已弃用）；支持策略弃用清单见 gotchas #94 |
| pnpm | 12.21.0 | **Rust 重写已 stable**：`--frozen-lockfile false` 被拒→`--no-frozen-lockfile`；`--resolution-only` 移除→`pnpm peers check`；供应链默认防护（minimumReleaseAge 24h 等）；`catalog:`/`catalogs:` 定义于 pnpm-workspace.yaml；catalogMode（12.3+） |
| changesets | 3.0.3 | Node ^22.11/^24+、pnpm ≥10；v3：`access` 默认 restricted、空 `version` 退出码 1、`tag`→`git-tag` |
| zustand | 5.1.0 | React ≥18 门槛 |
| @reduxjs/toolkit | 2.14.0 | 内置 redux 5/immer 11/reselect 5/redux-thunk 3 |
| react-hook-form | 7.92.0 | peer React 16.8-19；Node ≥18 |
| zod | 4.6.7 | **v4 大版本**；`zod/v3` 兼容入口；v4 面：error 参数/顶层格式 `z.email()`/`z.record` 双参/`.default()` 短路（旧行为 `.prefault()`）/any-unknown 键必填（4.4+）/`z.treeifyError()`/4.6 `.validate()` 守卫 + `z.withParser()`/`@zod/mini` 4.5 起独立包；Nest 12 Zod 直挂按项目 zod 大版本核对 API |
| @mui/material | 9.5.0 | **v9（2026-04-08，无 v8——v7 直跳 v9）**；弃用 `component`/`componentsProps` 全移除（用 slots）；react-admin 5.15.7 依赖区间支持 5/6/7/9 |
| @tanstack/react-table | 9.3.1 | **v9**：`useTable({ features })` 按需注册特性（v8 useReactTable 结束）；TanStack Store 驱动状态；peer React ≥18 |
| @tanstack/react-virtual | 3.14.26 | headless 虚拟化（useVirtualizer/getVirtualItems/绝对定位+translateY 模式）；peer React ^16.8-^19 |
| @tanstack/react-form | 1.33.5 | headless 类型安全表单（form.Field render props/Subscribe selector/异步校验防抖内建）；**peer React ^17-^19 无 16**；表单主选仍 RHF |
| @tanstack/react-pacer | 0.24.1 | 执行时机控制五模式（debounce/throttle/rate-limit/queue/batch）；**beta API 可变**；库发布用 @tanstack/pacer-lite |
| @tanstack/react-hotkeys | 0.27.0 | 类型安全键盘快捷键（**官方 beta，API 可变**）；useHotkey/useHotkeys + `Mod` 跨平台（⌘/Ctrl）+ Vim 序列 + scopes/`exclusive` 独占 + useFormatForDisplay（SSR 设 provider `platform`）；peer React >=18 |
| tRPC（@trpc/*） | 11.28.3 | peer TS ≥5.7.2、React ≥18.2、@tanstack/react-query ^5.106；客户端 **@trpc/tanstack-react-query 工厂模式**（queryOptions/mutationOptions）；经典 @trpc/react-query 与 @trpc/next createTRPCNext/withTRPC 已弃用下大版本移除；非 TRPCError message 生产也发客户端须 errorFormatter |
| motion | 14.14.0 | = framer-motion 14.14.0 同版本（改名完成，motion 为主包）；peer React ^18/^19；import `motion/react` |
| ai（AI SDK）/ @ai-sdk/react | 7.0.173 / 4.0.177 | **v7：ESM-only、Node ≥22**；system→instructions、onFinish→onEnd、fullStream→stream、telemetry→@ai-sdk/otel、toolApproval；v4/v5/v6/v7 四线并存（速查见 `kb/nextjs.md`）；peer zod ^3.25.76\|\|^4.1.8 |
| @tanstack/react-router / react-start | 1.170.46 / 1.169.5 | **Start 已 stable**；peer Vite ≥8、React ≥18、Node ≥22.12；构建器 Vite 或 Rsbuild；server fn 安全边界见 `kb/react-core.md` |
| @apollo/client | 4.3.8（legacy 3.14.1） | **v4：React 导出移至 `@apollo/client/react`、rxjs 新 peer、ApolloError 移除、hooks onCompleted/onError 移除**；先升 3.14 再迁 4.0；codemod `@apollo/client-codemod-migrate-3-to-4` |
| shadcn（CLI） | 4.23.0 | **代码分发平台，非 npm 组件库**；Node ≥20.18.1；`shadcn init -t next\|vite\|start\|react-router\|astro`；别名新模型 Package Imports `#...` |
| @base-ui-components/react | 1.0.0-rc.0 | headless unstyled（MUI 团队，Radix 替代候选）；**仍 RC 未 stable**；peer React ^17-^19 |
| @emotion/react / @emotion/styled | 11.14.0 / 11.14.1 | v11 线；MUI 默认样式引擎（MUI 下大版本方向为移除 Emotion） |
| TypeORM | 1.1.3 | **1.x 大版本（0.3 时代结束）**；Node ≥20.19 |
| Prisma | CLI prisma 8.0.0-rc.34（latest=RC，prev=7.10.1）；@prisma/client 7.10.1（无 8.x）；ORM 8 库=@prisma/orm-postgres 8.0.0-rc.23（与 CLI 分开发版） | `npm i prisma` 默认拿到 8 RC 且不读 schema.prisma；v7 锁 ^7（gotchas #93）；ORM 8=contract+手写 db.ts+链式查询，$extends/P2002/migrate dev 全没了（middleware/sqlState 23505/contract emit） |
| drizzle-orm / drizzle-kit | 0.45.4 / 0.31.11（stable）；v1.0-rc.5 在 RC（`npm i drizzle-orm@rc`） | **v1.0 过渡期**：升级三步 `drizzle-kit up`→改代码→RQB v2；RQB v1 移除→`defineRelations()`（`drizzle(url, { relations })`）；校验包并入主包（drizzle-orm/zod、typebox 双包）；casing→`snakeCase.table`；**schemaFilter 默认全 schema（0.x 仅 public）须显式收窄**；push 默认严格（--force 跳过）；迁移表 name+applied_at 按文件夹名匹配；postgres-js JSON 补丁 MUST 删——先确认版本线再写代码（gotchas #81/#97） |
| drizzle-pulse | 0.5.0（latest 稳定线） | Drizzle Pulse realtime：**PG only + Node ≥20**，peer drizzle-orm ^1.0.0-rc.5 + zod ^4 + hono ^4.6 + react >=18；进程内嵌入式（无额外服务）；live collection（list/onChange/onResync）+ CDC 事件流（(pk,lsn) 幂等键）；前置 `wal_level = logical` 自设、源表单列 PK、queries 启动时一次定义（gotchas #98） |
| class-validator / class-transformer | 0.15.1 / 0.5.1 | 0.x 线未出 1.0；Nest 12 下与 Standard Schema 双轨并存 |
| @nestjs/graphql | 14.2.1 | peer graphql ^16.11/^17、Nest 12；订阅走 graphql-ws |
| graphql | 17.1.0 | v17 大版本；Node ≥22 |
| @nestjs/passport / @nestjs/jwt | 12.0.2 / 12.0.5 | passport 0.5-0.7；jsonwebtoken 9 基座；**Nest 12 官方鉴权新路线为 @nestjs/authentication+authorization（下两行）**，Passport 为既有/特殊策略路线 |
| @nestjs/authentication / @nestjs/authorization | 0.1.6 / 0.1.4 | **peer 仅 Nest ^12（Nest 12 专属）**；node ≥20.19；sessions/密码 scrypt/MFA TOTP/OIDC/magic link/API keys/JWT+refresh 全家桶 + policy 默认拒绝；六 store 契约 production 拒内存；模块序 AuthenticationModule 先于 AuthorizationModule |
| @nestjs/swagger | 12.1.2 | Node ≥20.19/22.12；依赖 @standard-schema/spec |
| @nestjs/config | 12.1.1 | dotenv 18；validationSchema 支持 Standard Schema（Zod/Valibot） |
| @nestjs/websockets / ws | 12.5.0 / 8.23.0 | gateway 模型；ws 可选加速件 bufferutil/utf-8-validate |
| @testing-library/react | 16.3.3 | peer React 18/19 + **@testing-library/dom ^10 硬 peer**（须同步 major） |
| @testing-library/user-event | 14.6.10 | peer @testing-library/dom ≥7.21.4 |
| supertest | 7.3.2 | superagent 10 驱动；Node ≥14.18 |
| testcontainers | 12.2.1 | **Node ≥22.22 门槛**（CI 镜像核对）；dockerode 5 |
| swr | 2.5.1 | peer React 16.11-19；`swr/infinite`/`swr/mutation` 多入口 |
| @vitejs/plugin-react | 6.3.0 | **peer 仅 vite ^8**；React Compiler 走 babel-plugin-react-compiler ^1.0 |
| @vitejs/plugin-legacy | 8.2.4 | peer vite ^8 + terser ^5.16（ES5 双构建靠 terser） |
| msw | 3.0.6 | **v3（v2 时代结束）**；Node ≥22 硬要求；分模块入口 `msw/http` 等；GraphQL link-first |
| helmet | 8.3.0 | Nest 12.1+ 优先内置 `app.useSecurityHeaders()`（同默认值免依赖） |
| @nestjs/throttler | 6.7.1 | peer Nest 7-12；ttl 毫秒；分布式用 @nest-lab/throttler-storage-redis 1.2.0 |
| @nestjs/bullmq / bullmq | 12.0.2 / 6.7.6 | peer bullmq ^3-^6；BullMQ 6 可插拔 PG 后端免 Redis；@nestjs/bull（Bull）维护模式 |
| typescript | **7.0.2（latest）/ 6.0.3 双线** | **TS 7 = Go 原生 10×；7.0 无程序化 API（**7.1.0-beta 已发布**——beta 通道推进中，程序化 API 即将到位）**；TS 6.0 硬错误：baseUrl 移除（paths 相对项目根）、types 默认 []、target es5/moduleResolution node 不再支持；兼容包 @typescript/typescript6（tsc6）；Volar 型框架（Vue/Svelte/Astro/MDX）暂不能上 TS 7 |
| eslint | 10.15.0 | **v10 大版本**；Node ^20.19/^22.13/>=24；maintenance 线 9.39.5 |
| typescript-eslint | 8.73.0 | peer eslint ^8.57/^9/^10 + **typescript >=4.8.4 <6.1.0（支持 TS 6.0、不支持 TS 7）** |
| @biomejs/biome | 2.6.8 | 单二进制 lint+format（eslint+prettier 一体替代选项） |
| oxlint | 1.93.0 | Rust linter；TS 规则配套 oxlint-tsgolint |
| prettier | 3.10.1 | 3.x 线稳定 |
| Rspack / Rsbuild（Rstack） | @rspack/core 2.3.2 / @rsbuild/core 2.3.2 | **webpack 兼容 Rust bundler（v2）/ 其上零配置构建工具（Vite 竞品）**；Node ^20.19\|\|≥22.12（同 Vite 8）；全家桶域名均迁 **.rs**（rspack.rs/rsbuild.rs/rstest.rs 等）+ **Rstack CLI（rstack.rs，dev/build/test/lint/format 一体）**；benchmark：dev 冷启远快于 Vite、build 略慢；Rstack 全家桶（Rslib/Rspress/Rsdoctor/Rstest 0.12.6/Rslint 未发布）；见 `kb/vite-tooling.md` 替代线场景、`kb/testing.md` Rstest 场景 |

---
来源：标注见各条目；[官方文档] 条目 URL 详见对应 kb 文件「来源索引」。
