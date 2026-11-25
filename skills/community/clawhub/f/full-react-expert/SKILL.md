---
name: full-react-expert
description: React 全栈领域专家知识库：React 核心、Next.js App Router、NestJS、react-admin、TanStack Query、Vite、测试（Vitest/Playwright）、Monorepo（pnpm/Turborepo）八大子领域的法则、最佳实践、坑点速查、API 速查与版本锚定。Use when 编写、调试、选型或迁移上述全栈代码，做性能优化、测试或 monorepo 工程，或诊断渲染/水合/依赖注入/缓存等疑难问题。Triggers: React, Next.js, NestJS, react-admin, TanStack Query, Vite, Vitest, Playwright, Turborepo, pnpm, monorepo, TypeScript, JSX, TSX, hooks, RSC, Server Components, Server Actions, App Router, React Router, tRPC, zustand, redux, react-hook-form, Zod, TypeORM, Prisma, GraphQL, WebSocket, testing, eslint. Covers React 19.3 / React Router 8.5.1 / Next.js 16.4.6 / NestJS 12 / react-admin 5.15.7 / TanStack Query 5.107.1 / Vite 8.3.8 / Vitest 5.1.0 / Playwright 1.65.1 / pnpm 12 Rust / Turborepo 2.11.11 / TS 7/6 双线 / eslint 10.15.0 / TypeORM 1.1.3 / Prisma 7.10.1 / Drizzle 0.45 / zod 4.6.7 / MUI 9.5.0 / Tailwind 4.3.5 / msw 3.0.6 / Storybook 10.6.7 / React Compiler 1.0 / @nestjs/graphql 14 / tRPC 11.28.3 / Playwright MCP/CLI / AI SDK 7 / Apollo Client 4 / shadcn 4 / motion 14.
---

# React 全栈专家知识库

React / Next.js / NestJS / react-admin / TanStack Query / Vite / 测试 / Monorepo 的三层知识：**法则（约束性）→ 最佳实践（建设性）→ 坑点（防御性）**。生成代码前**逐条自检全局法则**（`kb/laws.md`）与「Top 法则」；写代码前查「Top 坑点」与 `kb/ai-mistakes.md`；版本敏感问题先看对应 kb 的「版本注意」。

## 知识库索引

| 文件 | 内容 | 何时读 |
|---|---|---|
| **kb/laws.md** | **全局宪法**：跨领域不可违背原则（LAW-1~16，版本/状态/安全/数据/工程/测试六纪律） | **生成代码前必读，逐条自检** |
| kb/react-core.md | 法则（RC）、最佳实践（状态选型/异步/性能/表单/Zod v4 迁移面与 AOT 编译/React Router 7-8 框架模式/TanStack Start 路由选型/错误兜底/UI 组件与动画生态 shadcn-ui·Base UI·motion/富文本编辑器 TipTap 3·Lexical/数据可视化 Recharts 3/拖拽 dnd-kit 新旧双线/日期与时间 date-fns 4·Temporal）、React Compiler、react-hook-form | hooks/重渲染/状态管理/性能/错误边界/表单校验/路由/UI 组件与动画/富文本/图表/拖拽/日期时区问题 |
| kb/nextjs.md | 法则（NX）、缓存语义（14/15/16 对照）、'use cache' 编排（cacheLife/cacheTag/updateTag）、RSC 边界、Server Actions、Streaming、i18n（next-intl 4）、proxy.ts 鉴权、AI SDK 7 流式聊天（useChat/四版本线断裂面）、文件上传（UploadThing 7）、支付（Stripe Checkout Sessions + Payment Element）、邮件（React Email + Resend）、鉴权库（Better Auth 1.7）、错误监控（Sentry v11）、自托管与多实例部署（standalone/加密 key/cacheHandler） | 路由/RSC/缓存/水合/部署/AI 聊天/i18n/上传/支付/邮件/鉴权库/错误监控/自托管多实例问题 |
| kb/nestjs.md | 法则（NE）、请求管道、DTO 校验（class-validator 与 Zod schema 双轨）、Nest 12 迁移要点、GraphQL/Swagger/WS、**鉴权与授权双轨（@nestjs/authentication 0.1.6+authorization 0.1.4：sessions/scrypt/MFA TOTP/OIDC/magic link/API keys/JWT+refresh family/六 store 契约/policy 默认拒绝 vs @nestjs/passport 既有路线）**、安全头（useSecurityHeaders）/限流（throttler）、队列（@nestjs/bullmq）、文件上传（Multer/Fastify multipart/StreamableFile）、**Prisma（v7 现役 / v8 RC 双线：contract 取代 schema、手写 db.ts、链式查询、CLI 重排、$extends/P2002 没了）**、**Drizzle ORM v1.0 深化（升级三步 kit up、15 breaking、kit v3 迁移表 name+applied_at、schemaFilter 默认全 schema、RQB v2 defineRelations 全 API、AI 面 kit mcp/skills、Pulse realtime drizzle-pulse 0.5.0 live collections/CDC 流）**、**可观测性（@nestjs/observe 0.3.26 深化：接入三步/link/驱动级插桩/TracerService/trace 传播版本门槛/APM 选型 preload 铁律/Observe MCP）**、部署与 Docker（nest deploy/Mau）、文档站重构后一等包版图、弹性与可靠性（resilience/idempotency/outbox）、AI 集成与 MCP server（@nestjs/ai/@nestjs/mcp）、Durable workflows 与分布式锁（@nestjs/workflows/@nestjs/locks）、webhooks、邮件与文件存储（@nestjs/webhooks/@nestjs/mail/@nestjs/storage）+ 五包共性契约 | 后端 API/DI 报错/校验/数据库/Prisma/鉴权授权/可观测性与 APM 选型/安全/队列/上传/部署/官方包选型/弹性重试幂等/outbox/workflows/locks/AI/MCP/webhooks/邮件/文件存储问题 |
| kb/react-admin.md | 法则（RA）、DataProvider/authProvider 契约、DataTable vs Datagrid、组件体系、校验/权限（CanAccess 开源核心 vs @react-admin/ra-* EE）、i18n/布局/性能/realtime/EE 模块深挖（ra-ai/ra-datagrid-ag） | 管理后台 CRUD/适配器/权限问题 |
| kb/tanstack-query.md | 法则（TQ）、queryKey 设计、staleTime/gcTime、乐观更新模板、Suspense 查询（useSuspenseQuery/useSuspenseQueries）、缓存持久化（persistQueryClient）、SSR 工厂模式、tRPC v11 集成（@trpc/tanstack-react-query 工厂模式）、GraphQL 客户端（Apollo Client 4）、TanStack 周边生态（Table 9/Virtual/Form/Pacer/Hotkeys） | 服务端状态/缓存失效/乐观更新/Suspense/持久化/tRPC/GraphQL 客户端问题 |
| kb/vite-tooling.md | 法则（VT）、配置与环境变量（VITE_ 前缀）、插件机制、构建优化、Vite 8（Rolldown+Oxc）、Tailwind v4、Biome 2 lint/format | 构建配置/插件/产物优化/lint format 选型问题 |
| kb/testing.md | 法则（TE）、Vitest 5+Testing Library、Vitest Browser Mode、Nest 测试（TestingModule/useMocker/override 体系）、Playwright（auto-wait/storageState/fixtures/story gallery 组件测试/Trace）、Agent 浏览器自动化（@playwright/mcp + @playwright/cli）、API mock（msw 3）、Storybook 10（addon-vitest 组件测试） | 单元/集成/E2E 测试/API mock/Agent 浏览器自动化/组件工作台问题 |
| kb/monorepo.md | 法则（MO）、pnpm 12（Rust 重写/catalog）、Turborepo（dependsOn/outputs/缓存/Remote Cache 签名）、**turbo query 变更检测（affected/turbo-ignore 弃用迁移/浅克隆 blobless）、架构守护与多技术栈（boundaries+Tags/microfrontends 代理/多语言 workspace/官方弃用清单）**、changesets 发布、lint 矩阵（eslint 10/biome/oxlint）、TypeScript 6/7 双线选型 | monorepo 搭建/依赖/缓存/发版/lint/TS 选型/CI 裁剪/多前端联调问题 |
| kb/ai-mistakes.md | AI 生成八领域代码的典型错误总集（按危害排序） | **写代码前必读**，生成后自查 |
| kb/gotchas.md | 跨领域高频坑点 Top 106（一句话版 + 指向详情） | 快速定位/排障入口 |
| kb/patterns.md | 全栈选型、Bun/Hono 现代运行时与轻量后端、服务端/客户端状态分离、项目结构、测试策略、版本联动 | 架构/选型/新项目启动时 |

## 决策树（按问题类型找知识文件）

- **生成代码前的通用约束 → `kb/laws.md`（全局宪法，先自检）**
- hooks 依赖 / 状态管理（zustand / RTK Query / XState / Jotai / tRPC 选型与深面）/ 重渲染 / 性能 / 错误边界 / Compiler / 表单与 Zod v4 校验 / React Router / 图表（Recharts）/ 拖拽（dnd-kit）/ 日期时区（date-fns）→ `kb/react-core.md`
- 路由 / RSC 边界 / 缓存 / hydration / Server Actions / Streaming / i18n / 鉴权代理 / 支付（Stripe）/ 邮件（React Email/Resend）/ 错误监控（Sentry）/ 自托管与多实例部署（standalone/加密 key/cacheHandler）→ `kb/nextjs.md`
- 依赖注入报错 / 管道守卫 / DTO 校验 / 数据库事务 / 微服务 / GraphQL / **鉴权与授权（@nestjs/authentication+authorization vs Passport）** / JWT / 安全头限流 / 队列 / Prisma（v7/v8）/ Drizzle（v0→v1 升级/RQB v2/Pulse realtime） / **可观测性与 APM 选型（Observe/OTel/Sentry）** / 部署与 Docker / 官方一等包选型 / 弹性重试·幂等·outbox / workflows / locks / AI 集成与 MCP server / webhooks / 邮件 / 文件存储 → `kb/nestjs.md`
- DataProvider / authProvider / 列表表单 / DataTable vs Datagrid / 后端对接 → `kb/react-admin.md`
- 服务端数据缓存 / queryKey / 乐观更新 / SSR 预取 / Suspense 数据获取 / 缓存持久化 → `kb/tanstack-query.md`
- 构建配置 / 环境变量 / 插件 / 分包优化 → `kb/vite-tooling.md`
- 单元 / 集成 / E2E 测试 / mock 策略 / msw API mock / Agent 浏览器自动化（MCP/CLI）→ `kb/testing.md`
- workspace 依赖 / 任务编排缓存 / 发版流程 / turbo query·CI 裁剪·多前端联调 → `kb/monorepo.md`
- 全栈架构 / 选型 / 项目结构 / 测试策略 → `kb/patterns.md`
- 不确定某坑是不是自己会犯的 → `kb/ai-mistakes.md`
- 快速排障，只有症状 → `kb/gotchas.md`
- **先查 AI 典型错误再写代码 → `kb/ai-mistakes.md`**

## Top 法则（生成代码前逐条自检）

1. **LAW-1 版本先行**：版本敏感问题先确认版本再答——Next 缓存 14/15/16 三次反转是历史教训
2. **LAW-3 服务端每请求一个状态容器**：SSR 的 QueryClient/store 模块级单例 = 跨用户数据泄漏
3. **LAW-5 服务端入口一律鉴权 + 校验**：Server Action 是公开 HTTP 端点，不是可信内部函数
4. **LAW-6 密钥不进客户端可达代码**：`VITE_`/`NEXT_PUBLIC_` 变量全量打进 bundle，可见即公开
5. **LAW-7 校验元数据必须运行时存在**：interface 编译即消失，校验静默失效（用 class/Zod schema）
6. **LAW-8 契约层错误必须显式抛出**：DataProvider/queryFn 吞错 = 整条错误处理链失明
7. **LAW-12 资源获取与释放成对出现在生命周期两侧**（onModuleInit↔onModuleDestroy、useEffect↔cleanup）
8. **LAW-14 静默失效自查**：无报错但功能失效的模式（校验未挂/回调未订阅/缓存未失效/override 未生效）交付前必查

## Top 坑点（不读 kb 也必须知道的）

1. **先查版本再答**：Next 缓存语义 14→15→16 三次反转；React 19.3；Next 16.4.6；Nest 12；react-admin 5.15.7；TanStack Query 5.107.1；Vite 8.3.8（v8 已移除 manualChunks 对象形式）；Vitest 5.1.0（v5：clearMocks 默认 true、非顶层 vi.mock 抛错）；Playwright 1.65.1（**仅 Node 22/24/26 + Win 11+**）；**TypeScript 7.0.2（Go 原生，7.0 无 API）与 6.0.3 双线**（typescript-eslint 不支持 TS 7；@tanstack/eslint-plugin-query 5.107.1 已支持 TS 7）；**pnpm 12 Rust 重写**（`--frozen-lockfile false` 被拒→`--no-frozen-lockfile`）；**eslint 10**；生态包：**TypeORM 1.x**（0.3 时代结束）/ **Prisma 7 稳定（CLI latest=8 RC）** / **Drizzle 1.0 处于 RC（stable 0.45.4）** / zod v4 / graphql v17 / **Apollo Client 4.3.8**（React 导出在 `@apollo/client/react`、rxjs peer、ApolloError 移除）/ **msw 3**（Node ≥22，分模块入口）/ **@tanstack/react-table 9**（useTable+features）/ **MUI 9（无 v8）** / **Tailwind 4.3.5** / **@nestjsx/crud 已弃维护**
2. useEffect 依赖随手 `[]` + 闭包读 state = stale closure 静默 bug
3. Next 16 强制 `await params/searchParams/cookies()/headers()`
4. Nest DTO 用 interface → class-validator 校验静默失效（必须 class；Nest 12 起可用 Zod schema 直挂装饰器）
5. "Nest can't resolve dependencies" 五步排查：providers 注册 / exports / forFeature / forwardRef / @Injectable
6. `'use client'` 必须在文件第一行，是模块级边界（子树全变客户端）
7. react-admin 表格双轨：新代码用 `<DataTable>`（v5.8+ 推荐），存量 `<Datagrid>` 合法（`optimized` 禁动态 children），勿混写；`CanAccess`/`useCanAccess` 是**开源核心**（EE 分界 = `@react-admin/ra-*` 包）
8. TanStack Query 的 queryFn 必须 throw（HTTP 非 2xx 不算 error，"成功但空数据"最隐蔽）
9. interceptor 忘 `return next.handle()` → 响应 undefined 不报错
10. `key={index}` 在动态列表 = 状态错位；SSR 下 QueryClient 必须工厂函数（模块级单例跨用户泄漏）
11. Nest 全局守卫 `APP_GUARD` 用 useClass 注册时不可 overrideProvider——须改 `useExisting` 注册 + 同注册该类
12. Vitest 5 升级双雷：`clearMocks` 默认 true（setup 记录的 mock 调用被清）；非顶层 `vi.mock`/`vi.hoisted` 从警告升级为抛错
13. Next 16 Cache Components 下动态路由 generateStaticParams 空数组 = **build error**（empty-generate-static-params）——至少 1 param，未知值 placeholder + `notFound()`
14. Nest cache-manager：内存 store `get()` 返回**同引用**（改它 = 污染缓存）；Redis store 必挂 `'error'` 监听器，断连无监听**崩整个应用**

## 回答规范

- 回答引用 kb 条目时保留来源标注（[官方文档]/[模型经验]/[推断]/[实战回流]）。
- **生成代码前逐条自检 LAW 条款**（`kb/laws.md` Top 法则 + 相关领域法则小节）；违反任何一条必须先修正再输出。
- 不确定时明说不确定，不编造 API；版本敏感结论注明所基于的版本。
- 用户问题超出 kb 覆盖面时如实说明，不要虚构领域知识。
- 生成 react-admin / Next.js / NestJS 代码前，先确认用户项目版本（`npm ls` / package.json）。

## 知识回流

触发条件：修复了 kb 未覆盖的 bug / 发现 kb 错误过时 / 官方大版本更新。
处理：按 kb-distiller 的 refine 规程（`kb-distiller/prompts/refine.md`）向对应 kb 文件追加结构化条目，标注 `[实战回流]`，更新 frontmatter 的 `version` 与 `updated`；坑点类回流先考虑是否应升维为法则条款（第 5 轮法则化规程，见 `kb-distiller/prompts/elicitation.md`）。

轮次历史（细节已沉淀至各 kb 与 corpus 锚点文件，此处滚动保留最新一轮全文）：
- 2026-11-15/16 缺口补全轮 + 第一至三轮（轮 1-90）：9 项缺口全部关闭（Vite 8 breaking/Turbo+Playwright 版本锚定/react-admin EE 全景/pnpm catalog 与 12 Rust/TS 6-7 双线/Vitest 5/Playwright 组件测试/CanAccess 归属）
- 第四轮（91-120）：Next 16.4 安全发布 + Instant Navigations、React 19.2/19.3 + Compiler 1.0、Nest 微服务/GraphQL v14/CQRS、TanStack 深化（`kb/nextjs.md` v6、`kb/react-core.md` v8、`kb/nestjs.md` v7 系）
- 第五轮（121-150）：tRPC v11（TQ-13）、Zod v4、react-admin 5.15、Playwright 1.65 与 story gallery、pnpm 12 Rust（`kb/gotchas.md` #68-79 系）
- 第六轮（151-180）：Tailwind v4、Drizzle 0.45/v1 RC、Storybook 10、'use cache' 深化、Zod AOT 编译（`kb/gotchas.md` #80-82；43/43 PASS、272 KB）
- 第七轮（181-210）：AI SDK 7 断裂面、TanStack Start stable、Biome 2、Apollo Client 4、shadcn 4 生态（`kb/nextjs.md` v8、`kb/react-core.md` v13-14、`kb/tanstack-query.md` v8、`kb/gotchas.md` #83-84；43/43 PASS、293 KB）
- 2026-11-16 第八轮深化（轮 211-240）完成：Phase OO 体积蒸馏（SKILL.md 轮次滚动制 + 释放 3.76 KB）；Phase PP TipTap 3（3.34.0 断裂面 → `kb/react-core.md` v15 富文本场景）；Phase QQ next-intl 4（4.15.1 四件套/proxy.ts 新名/locale 协商 → `kb/nextjs.md` v9）；Phase RR 文件上传双轨（Multer memoryStorage 红线 → `kb/nestjs.md` v10；UploadThing 7 维护预警 → `kb/nextjs.md` v10）；Phase SS 收尾（43/43 PASS、299 KB）
- 2026-11-16 第九轮深化（轮 241-270）完成：Phase TT Better Auth（1.7.25 活跃主选/next-auth v5 beta 不推荐/nextCookies() server action 坑 → `kb/nextjs.md` v11、gotchas #85）；Phase UU XState v5 actor model + Jotai v3（经 tarball README 锚定 → `kb/react-core.md` v16）；Phase VV Bun 1.4.4/Hono 4.13（选型判定表 → `kb/patterns.md` 新节）；Phase WW Stripe（官方立场 Checkout Sessions 优于 Payment Intents/CheckoutElementsProvider 新 API/raw body 红线 → `kb/nextjs.md` v12、gotchas #86）；Phase XX 收尾（43/43 PASS、312 KB）
2026-11-16 第十轮深化（轮 271-300）完成：Phase YY Recharts 3（3.10.1：Cell 弃用→shape/activeIndex 移除→Tooltip/responsive prop 3.3+/dataKey 引用稳定——→ `kb/react-core.md` 场景数据可视化）；Phase ZZ dnd-kit 双线（旧 @dnd-kit/core 6.3.1 停更 Legacy vs 新 @dnd-kit/react 0.5.3 ref API——API 完全不兼容先 npm ls → `kb/react-core.md` 场景拖拽、`kb/gotchas.md` #87）；Phase AAA 日期库（date-fns 4.4.0 一等时区/归一化到第一参数时区/@date-fns/tz 1.5.0/Temporal polyfill 0.5.1 不装 global → `kb/react-core.md` v18 场景日期与时间）；Phase BBB 邮件（@react-email/components 1.0.12 + resend 6.38.1 同团队：{data,error} 不 throw/react 参数函数调用非 JSX/idempotencyKey/测试地址族 → `kb/nextjs.md` v13 场景邮件）；Phase CCC 收尾（patterns.md v19 联动表五行；43/43 PASS、323 KB）

2026-11-16 第十一轮深化（轮 301-330）完成：Phase DDD Sentry v11（@sentry/nextjs 11.12.0 五版本线 v7-v11 并存先 npm ls；v11 三文件初始化+register+onRequestError；tunnelRoute 版本门槛 v11≥11.9.0；Agent Tracing → `kb/nextjs.md` v14 场景、`kb/gotchas.md` #88）；Phase EEE 自托管部署+NestJS 文档站重构（Next self-hosting：多实例三件套 NEXT_SERVER_ACTIONS_ENCRYPTION_KEY/deploymentId/cacheHandler+refreshTags；standalone MUST 手动 cp public+static；NestJS：llms.txt 重构后一分区/一等包版图/StandardSchemaValidationPipe/nest deploy+Mau/Observe instrument → `kb/nextjs.md` v15、`kb/nestjs.md` v11 两场景、`kb/gotchas.md` #89（standalone 静态 404）/#90（多实例 Server Action 加密 key）；43/43 PASS、334 KB）

2026-11-16 第十二轮深化（轮 331-360）完成：Phase FFF/GGG 官方一等包深化（版本锚定 ai 0.0.2/mcp 0.0.4/resilience 0.0.3/idempotency 0.0.4/outbox 0.1.4 等 18 包；@nestjs/ai 绑 AI SDK 7、AiOutputError 不重试、@AgentFunction 走管道；@nestjs/mcp Zod 3 启动即拒、无状态多实例、McpStdioLogger MUST；resilience 装饰器仅 entrypoints、POST 重试 skip+WARN、IdempotencyModule 前置；idempotency production 拒 InMemory、json 非 jsonb、AES-GCM fail closed；outbox MUST 传事务句柄、key 保序、READ COMMITTED、TCP 仅字节发出 → `kb/nestjs.md` v12 两场景、`kb/gotchas.md` #91（一等包 pre-stable 先 npm ls）；43/43 PASS、344 KB）

2026-11-16 第十三轮深化（轮 361-390）完成：一等包深化续（workflows 0.0.5 journal 重放/补偿/ctx.commit、locks 0.0.6 LockStore 自实现/fencing token、webhooks 0.0.4 SSRF 防线、mail 0.0.2、storage 0.0.5 魔数检测、五包共性契约 production store 门槛/schema 自管理/executor/事务句柄/READ COMMITTED → `kb/nestjs.md` v13 两场景、`kb/gotchas.md` #92；43/43 PASS、351 KB）

2026-11-16 第十四轮深化（轮 391-420）完成：Prisma 深化——ORM 8 RC 全图（prisma CLI latest=8.0.0-rc.33 两包结构 @prisma/orm-postgres、@prisma/client 停 7.10.1、contract 取代 schema、手写 db.ts、链式查询、CLI 重排 CLI.COMMAND_MOVED、$extends/P2002 没了、middleware 三件套、升级 orm init --from-prisma7-schema、ORM 6 EOL 2026-11-19 → `kb/nestjs.md` v14 Prisma 双线场景、`kb/gotchas.md` #93、锚点 544 行；43/43 PASS、358 KB）

- 2026-11-16 第十五轮深化（轮 421-450）完成：Playwright 1.65.1 复核无漂移免增量（无 llms.txt、testing.md 现覆盖即全集）；Turborepo 2.11.11 增量（turbo query GraphQL 变更检测 + turbo-ignore 弃用迁移、boundaries+Tags 架构守护、microfrontends 本地代理、多语言 workspace、官方弃用清单与 LTS 支持策略 → `kb/monorepo.md` v6 两新场景、gotchas #94；43/43 PASS、365 KB）

- 2026-11-16 第十六轮深化（轮 451-480）完成：NestJS Observe 深化 + 可观测性选型——@nestjs/observe 0.3.26（接入三步/link/Fastify 第三参陷阱/驱动级插桩折叠/TracerService/trace 传播版本门槛 12.0.4·12.3.3/OTel JS 版本面分层 SDK node>=22.15/otlp 4318 无 gRPC）；APM 选型 preload 铁律、instrumentation-nestjs-core 仅 core<12；Observe MCP 三时相；production rules；→ `kb/nestjs.md` v15 新场景 + gotchas #95（43/43 PASS、376 KB）

- 2026-11-16 第十七轮深化（轮 481-510）完成：@nestjs/authentication+authorization 深化 + react-admin 复核免增量——0.1.6/0.1.4 peer 仅 Nest 12 专属；官方双轨鉴权全图（provider 链 order 显式/scrypt N=2^17 防枚举/`__Host-sid` 只存哈希/JWT refresh family 复用灭族/MFA TOTP AES-GCM 配 mfa 无 encryption startup throw/OIDC pre-hijacking 防御 + BYO-IdP SSRF 红线/magic link 浏览器绑定/六 store 契约原子性红线·production 拒内存/authorization 默认拒绝·policy 单例·record 检查禁按 URL 缓存/**AuthenticationModule 必须先于 AuthorizationModule**/GraphQL context 必须函数·graphql-ws 勿读 req.user）；→ `kb/nestjs.md` v16 鉴权场景重写为官方双轨、gotchas #96、patterns 鉴权两行、锚点 657 行；43/43 PASS、386 KB

- 2026-11-17 第十八轮深化（轮 511-540）完成：Drizzle v1.0 深化——版本复核无漂移（drizzle-orm 0.45.4/rc.5、drizzle-kit 0.31.11/rc.5、drizzle-zod 0.8.3、drizzle-typebox 0.3.3、drizzle-valibot 0.4.2、drizzle-seed 0.3.1、drizzle-arktype 0.1.3、@libsql/client 0.18.0、drizzle-effect-schema 404 不存在）；升级三步（kit up→改代码→RQB v2）；15 breaking + 20 特性全量（schemaFilter 默认全 schema、postgres-js JSON 补丁删、push 默认严格、迁移表 name+applied_at、缓存 all 策略、JIT/Codecs、内省 <1s）；RQB v2 全 API（defineRelations/from·to/through/pull 自动生成 relations.ts）；→ `kb/nestjs.md` v17 Drizzle 场景 33 行、gotchas #97、patterns v21、锚点 725 行；43/43 PASS、394 KB

- 2026-11-17 第十九轮深化（轮 541-570）完成：Drizzle AI 面闭环 + Pulse realtime——AI 面三件套（`drizzle-kit mcp` 本地 stdio rc5 无 migrate 工具 / skills rc5 单 `drizzle` skill 化自动移除旧项目 skills / agents 一句话 setup）；drizzle-pulse 0.5.0（PG only + Node ≥20 嵌入式、`wal_level=logical` 自设、源表单列 PK、queries 启动时一次定义、`.args()` 同步校验、live collection list/onChange/onResync 三件套、CDC 流 (pk,lsn) 幂等键、async listener 不自捕获杀进程）；drizzle-orm rc dist-tag 复核无漂移（仍 rc.5）；→ `kb/nestjs.md` v18、gotchas #98、patterns v22、锚点 753 行；43/43 PASS、401 KB

- 2026-11-17 第二十轮深化（轮 571-600）完成：Drizzle latest-releases 扫尾（rc.5 即最新发布）+ 30 包生态漂移批量复核（26 包无漂移；4 包补丁级刷新：vite 8.3.8、prisma rc.34、@nestjs/core 12.5.1、typescript-eslint 8.73.0——peer 复核均不变）；→ vite-tooling v8、monorepo v7、nestjs v19、patterns v23、gotchas v34、ai-mistakes v5；锚点 763 行；43/43 PASS、约 402 KB

- 2026-11-17 第二十一轮深化（轮 601-630）完成：react-admin EE 深挖（ra-ai 5.5.0 DataProvider 双 AI 方法 generateContent/suggestCompletion + ra-datagrid-ag 7.2.0 DatagridAG/DatagridAGClient 双组件分工 + v6.0.0 ag-grid v33 BREAKING）+ TanStack 周边深化（Table 9.3.1 无漂移 + v9 overview 17 特性 + 家族新锚定 Router/Start/Store/Hotkeys + eslint-plugin-query 已支持 TS 7）+ 收官一致性复核（gotchas 1-98 连续无缺失）；→ react-admin v7、tanstack-query v10、patterns v23、锚点 react-admin 224 行/tanstack 284 行；43/43 PASS、406 KB

- 2026-11-17 第二十二轮深化（轮 631-660）完成：TanStack Hotkeys 深挖收官——@tanstack/react-hotkeys 0.27.0（**官方 beta**）useHotkey/useHotkeys + Mod 跨平台 + 序列 + scopes/exclusive + useFormatForDisplay（SSR 设 platform）+ defineAppHotkeys/HotkeyRecorder/DevTools 全锚定；Router/Start 复核无缺口；→ tanstack-query v11、patterns v24、tanstack corpus 304 行；43/43 PASS、408 KB

- 2026-11-17 第二十三轮深化（轮 661-690）完成：zustand/motion/xstate 文档站复核 + ai-mistakes 增量审查——zustand/xstate 复核免增量（主体已锚定，饱和）、motion 净增量 5 点（layout/layoutId FLIP、useScroll scroll-linked、混合引擎 WAAPI 120fps、SVG pathLength、`npx motion-ai`）；ai-mistakes v5→v6 补录 12-22 轮 8 条 AI 错误（dnd-kit 双线/AI SDK 7 旧 API/prisma 盲装 8 RC/tRPC 经典钩子弃用/Apollo 4 入口断裂/Table v9 useReactTable 等）；→ react-core v19、ai-mistakes v6、react-core corpus 559 行；43/43 PASS、约 411 KB

- 2026-11-17 第二十四轮深化（轮 691-720）完成：**全向饱和验证收官轮**——Bun 1.4.4/Hono 4.13.18 文档站复核（两站均可抓、主体早在第九轮已锚定、再次撞饱和）；细节级净增量回流 patterns v24→v25——Hono 三路由器（RegExpRouter/LinearRouter/PatternRouter/SmartRouter 组合）+ 中间件面补全 + 路径参数字面量类型；Bun `bun check`/`bun lint`/`bun fmt` 工具细节 + Web 标准 API Safari 实现细节；收官判定：zustand/xstate/motion/Bun/Hono 五站连续复核均撞既有锚点——知识库达结构性饱和，转入触发式增量维护；43/43 PASS、411 KB

- 2026-11-17 第二十五轮深化（轮 721-750）完成：**pre-stable 转换巡检轮**——47 包 npm dist-tags 批量巡检（pre-stable 重点 13 + stable 对照 34）；漂移 3 项回流：xstate v6 alpha→**beta（6.0.0-beta.3）**（patterns 联动表 + react-core XState 行）、hono 4.13.18→4.13.19 补丁、**MUI v10 alpha 已启（next=10.0.0-alpha.0）**；44 包无漂移确认（prisma rc.34/drizzle rc.5/RHF beta.0/React 19.3.1 等与锚定一致）；→ patterns v26、react-core v20；43/43 PASS、417 KB；pre-stable 包（xstate v6/MUI v10/Hono 5/Prisma 8/Drizzle 1.0）任一转 stable 即触发深挖轮

- 2026-11-17 第二十六轮深化（轮 751-780）完成：**TipTap 深化轮**——补抓 React 集成页 + 协作编辑页；React 集成面净增量（`@tiptap/pm` 必装、`@tiptap/react/menus` 子路径、useCurrentEditor 仅 Provider 模式生效、useEditorState 选择器、SSR `immediatelyRender: false`、新 React Composable API `<Tiptap>`）；协作编辑净增量（Y.Doc 四件套、TiptapCollabProvider 私有 registry、必坑①content 重复添加→onSynced 幂等守卫、必坑②协作 MUST `undoRedo: false`）；→ react-core v21、react-core corpus 591 行；43/43 PASS、420 KB

- 2026-11-17 第二十七轮深化（轮 781-810）完成：**Rstack 生态（Rspack/Rsbuild）锚定轮**——预检排除 msw（已深锚）；Rspack/Rsbuild 此前仅散见提及为真实缺口；锚定 @rspack/core 2.3.2（**v2 大版本**，webpack 兼容 Rust bundler）+ @rsbuild/core 2.3.2（零配置 Vite 竞品，含 webpack 迁移指南）；benchmark：dev 1.36s 远快于 Vite 6.50s、build 3.35s 略慢；**域名迁移 rspack.dev→rspack.rs**；Rstack 全家桶（Rslib/Rspress/Rsdoctor/Rstest 0.12.6/Rslint 未发布）；选型：webpack 存量迁移/超大项目 dev 冷启选 Rstack，新项目 build 速度与 ESM 原生管线选 Vite 8；→ vite-tooling v9 新「构建工具替代线」场景、patterns v27 联动表、vite-tooling corpus 172 行；43/43 PASS、422 KB

- 2026-11-17 第二十八轮深化（轮 811-840）完成：**Node.js 运行时版本基座锚定轮**——nodejs.org 全表捕获（新增可抓站点）；预检排除 Storybook（已深锚）；现行 LTS 三线 v26 Lithium 26.13.1 / v24 Krypton 24.22.3 / v22 Jod 22.23.5；**Node 20 Iron 已 EOL（2026-03-24）**——engines `^20.19||>=22.12` 中 20 线已死，生产基座取 22/24/26；**Node 27 起发布周期改年度**（6 个月 Current + 6 个月 Alpha → LTS，共 30 个月）；v27 Alpha 已启；→ patterns v28 新「Node.js 运行时版本基座」小节；43/43 PASS、424 KB

- 2026-11-17 第二十九轮深化（轮 841-870）完成：TanStack Form 深挖轮——组合 API createFormHook/createFormHookContexts → useAppForm + form.AppField （组件预绑定，name typo 编译错）+ schema 直挂 form 级校验（Zod/Valibot/ArkType Standard Schema）+ onChangeAsyncDebounceMs 防抖内建；tanstack-query v12、43/43 PASS、425 KB

- 2026-11-17 第三十轮深化（轮 871-900）完成：Lexical 富文本锚定轮（新文档站 lexical.dev）——新 Extensions 架构（defineExtension/@preact/signals-core 底层）、协作三坑（editorState: null / 服务端 bootstrap / remount editor）、自定义节点属性 constructor 赋值坑；react-core v22、43/43 PASS、429 KB

- 2026-11-17 第三十一轮深化（轮 901-930）完成：TanStack Form 校验深面轮——验证时机全集、errorMap 按时机取错、form 级 onSubmitAsync 嵌套路径设 field 错误、覆盖坑、sync→async 顺序、防抖双层、Standard Schema 四家、canSubmit touched 语义；tanstack-query v13、43/43 PASS、431 KB

- 2026-11-17 第三十二轮深化（轮 931-960）完成：Rstest 深挖轮——rstest.rs 可抓（llms.txt AI 友好）、rstest.dev 域名抢注垃圾站；Browser Mode（Playwright 三引擎+Locator+expect.element）、E2E in same runner、配置兼容例外表；Rstack 全家域名迁 .rs + Rstack CLI；testing v10、43/43 PASS、433 KB

- 2026-11-17 第三十三轮深化（轮 961-990）完成：pre-stable 巡检轮（47 包 dist-tags 复核）——latest 零漂移；新通道情报：TanStack Form v2 alpha 已启（2.0.0-alpha.3）、RHF v8 双通道（beta.0+alpha.5）、TS 7.1.0-beta 已发、Vite 8.4.0-beta.1；四 kb 联动更新；**观察：另有并行蒸馏会话同步产出合法增量（testing/monorepo/tanstack/vite +~275 行，用户裁定接受）**；43/43 PASS、461 KB

2026-11-17 第三十四轮深化（轮 991-1020）完成：**TanStack Form 深挖收官轮（提交与联动）**——submission-handling + linked-fields 两页捕获；净增量：**onSubmitMeta 多提交行为**（useForm({onSubmitMeta, onSubmit: ({value, meta})}) + 按钮级 form.handleSubmit({submitAction}) 覆盖默认）；**Standard Schema 只做校验不保留 output**——onSubmit 恒收 input 数据，transformed 值须 onSubmit 内 schema.parse(value) 二次解析（defaultValues 用 z.input<typeof schema>，与第三十一轮 validation 页'不产 transformed values'闭环）；**字段联动验证 onChangeListenTo/onBlurListenTo**（password/confirm_password 场景，无 listenTo 错误残留）+ fieldApi.form.getFieldValue() 跨字段取值；→ tanstack-query v15 生态区「提交与联动」条目 + tanstack corpus 追加第三十四轮块；Form 面闭环（基础→校验→提交→联动 + v2 alpha 情报）；43/43 PASS（体积见校验输出）

- 第三十五~四十二轮深化（轮 1021-1260）合并补记：薄子域与生态深化（R39-R42 终态 tanstack-query v15 / testing v12 / vite-tooling v11 / monorepo v9；ui-ux 并行会话 R41 51/51 PASS、663KB）；轮次明细见各 kb「来源索引」轮次小节；此区间轮次历史未逐条登记，特此补记（2026-11-17 项目评审发现）

- 2026-11-17 第四十三轮深化（轮 1261-1290）完成：R43 富子域四空白带——react-core「React 19 form actions 与并发原语」（RC-12 getSnapshot 缓存 / RC-13 useActionState 已知 return 未知 throw，v24）；nextjs「Metadata/SEO 与静态资产」（NX-14 仅 RSC + metadataBase、15.2+ streaming metadata，v16）；nestjs「进程内事件与请求上下文」（NE-12 waitUntilReady 先于 emit，v20）；react-admin「参考关联输入」（RA-13 通用 props 归子组件，v8）；42/42 PASS、510KB

- 2026-11-17 第四十四轮深化（轮 1291-1320）完成：R44 富子域四空白带——react-core「Context 深水」（RC-14 provider value 引用稳定，v25）；nextjs「动态段静态化与按路径失效」（NX-15 Cache Components 至少 1 param，v17）；nestjs「缓存」（NE-13 内存 store 存引用 + Redis error listener，v21）；react-admin「List 架构与过滤深水」（RA-14 alwaysOn/defaultValue 互斥，v9）；42/42 PASS、529KB

- 2026-11-17 项目评审改进轮：四维评审（流程/规范/质量/覆盖度）→ 全部建议落地——P0：refine.md 横切对账强制步骤（新增/豁免二选一登记）+ distill.md gotchas Top 判定标准与法则 15 硬顶/达顶/退役政策 + pipeline.md/validate.md 体积红线 300KB→2MB 对齐 + R43/R44 横切对账补账（gotchas v35 #99-106、ai-mistakes v7、laws v2 对账记录、SKILL.md Top 坑点 +2、轮次历史补记）；P1：refine.md 深化轮操作约定成文（选题去重/编号续接/轮次命名/audit 基线）+ elicitation.md 深化轮纪律（自我质询 ≥5 内生条目）；P2：validate.md 事实抽查规程 + scripts/spot_check.py URL 探活 + zustand/redux 覆盖核实（R23 已锚定关键面，按语义去重免增量，决策树显性化路由）

当前无新增登记缺口；发现新缺口时按上述格式追加。

## 事实抽查记录

| 轮次 | 抽查条数 | 结果 | 日期 |
| --- | --- | --- | --- |
| 项目评审改进轮 | 全量 304 URL（spot_check.py --all） | BROKEN 1：reference/QueryCacheConfig 404——TanStack 文档站重构接口页迁移，已改锚 reference/interfaces/QueryCacheConfig 并探活 PASS；BLOCKED 4（npmjs 403 反爬 ×3、observe-api.nestjs.com/mcp 401 属 POST 端点预期）复核豁免（明细见 kb/tanstack-query.md 事实抽查记录） | 2026-11-17 |
| 全项目评审机制对齐轮 | 抽样 30/候选 304（seed 42） | OK 29 / BLOCKED 1（nextjs.org use-cache 单点 timeout，同站其余 URL 全 OK——网络波动）/ BROKEN 0 | 2026-11-18 |
