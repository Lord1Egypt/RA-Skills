---
subdomain: nextjs
version: 17
updated: 2026-11-17
---
# Next.js（App Router）

## 定位与心智模型

Next.js 是 React 全栈框架。App Router 心智模型三句话：1) **组件默认 Server Components**（服务端执行、可直接 async/连库）2) **`'use client'` 是模块级边界声明** 3) **props 跨边界只能传可序列化数据**。**版本敏感性极高**：缓存语义 14→15→16 三次反转（[NX-1]/LAW-1）。16.x 主线演进：**16.3 Instant Navigations（Stream/Cache/Block + Partial Prefetching）→ 16.4 官方推荐 Cache Components 用于所有应用（Next 17 默认）**。

## 法则

[NX-1] **MUST**: 回答缓存/数据获取问题前先确认项目 next 版本（全局宪法 LAW-1）。
- 违反后果: 缓存语义三次反转，方案整体错误
- 溯源: [官方文档](https://nextjs.org/blog)

[NX-2] **MUST**: `'use client'` 必须是文件第一行，且边界下沉到交互叶子组件。
- 违反后果: 位置无效；或整页进客户端 bundle、服务端直取尽失
- 溯源: [官方文档](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns)

[NX-3] **NEVER**: Server Component 里不得使用 hooks；跨边界 props 必须可序列化。
- 违反后果: `useState only works in Client Components` / `Functions cannot be passed directly to Client Components`
- 溯源: [官方文档](https://nextjs.org/docs)

[NX-4] **MUST**: Next 16 起 params/searchParams/cookies()/headers() 必须 await。
- 违反后果: 拿到 Promise 或报错
- 溯源: [官方文档](https://nextjs.org/blog/next-16)

[NX-5] **NEVER**: App Router 项目不得写 Pages Router API（getServerSideProps 等）。
- 违反后果: 永不执行，页面数据为空
- 溯源: [模型经验]

[NX-6] **MUST**: Server Action 是公开 HTTP 端点——每个 action 必须服务端鉴权 + 入参校验（全局宪法 LAW-5）。
- 违反后果: 拿到 action id 即可直调；FormData 注入
- 溯源: [模型经验]

[NX-7] **MUST**: redirect()/notFound() 不得被外层 try/catch 吞（catch 重抛）。
- 违反后果: NEXT_REDIRECT 被当异常，跳转失效
- 溯源: [模型经验]

[NX-8] **MUST**: 16 项目中间层用 proxy.ts（middleware.ts 已弃用）；parallel routes 必须有 default.js。
- 违反后果: 弃用警告；构建失败
- 溯源: [官方文档](https://nextjs.org/blog/next-16)

[NX-9] **MUST**: revalidateTag 16 起双参数 `(tag, profile)`。
- 溯源: [官方文档](https://nextjs.org/blog/next-16)

[NX-10] **NEVER**: render 期不得读 localStorage/window/Date.now()。
- 违反后果: `Hydration failed because the server rendered HTML didn't match the client`
- 溯源: [模型经验]

[NX-11] **MUST**: 首屏/SEO 数据在 RSC 直取（await），交互式数据才下沉 client。
- 违反后果: client useEffect 首屏请求瀑布，丧失流式与 SEO
- 溯源: [模型经验]

[NX-12] **MUST**: 自托管 `next start` + Cache Components 必须开 `partialPrefetching: true`；敏感 cookie 勿用 `NextResponse.cookies.set()`（Edge routes）——改 `cookies().set()`。
- 违反后果: shared shell 被未认证请求投毒（GHSA-pc58，2026-11 已修）；`x-middleware-set-cookie` 内部头泄漏 cookie 绕过 HttpOnly（GHSA-f3mh）
- 溯源: [官方文档](https://nextjs.org/blog/november-2026-security-release)

[NX-13] **NEVER**: 同一读 root 参数（租户/locale）的 `'use cache'` 函数不得同时被 `unstable_cache` 包装调用。
- 违反后果: 冷填充期并发调用跨租户缓存泄漏（GHSA-mfr8，High，16.4.5 修复）
- 溯源: [官方文档](https://nextjs.org/blog/november-2026-security-release)

[NX-14] **MUST**: metadata/generateMetadata 仅在 Server Components 导出（同段二者互斥）；URL 类 metadata 字段用相对路径必须配 `metadataBase`。
- 违反后果: `'use client'` 文件的 metadata 导出被忽略；相对 URL 构建错误
- 溯源: [官方文档](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)

[NX-15] **MUST**: Cache Components 下动态路由的 generateStaticParams 必须返回至少一个 params 对象（空数组是 build error）。
- 违反后果: empty-generate-static-params 构建失败
- 溯源: [官方文档](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| RSC | 服务端执行的 React 组件，输出序列化 UI 描述 |
| Server Action | `'use server'` 函数，可作表单 action；**公开端点** |
| Cache Components | 16 起：默认全动态，`'use cache'` 显式缓存；**16.4 起官方推荐所有应用**（Next 17 默认） |
| proxy.ts | 16 起请求中间层（Node.js 运行时） |
| Streaming | RSC payload 分块流式，Suspense 边界即流式边界 |
| Instant Navigations | 16.3：Stream/Cache/Block 三选让导航 SPA 级即时（Instant Insights dev 慢导航报错） |
| Partial Prefetching | 16.3：每 route 预取一个可复用 shell（客户端缓存），替代每 link 一请求 |
| ensureStatic | 16.4 route/layout 段配置：`'navigation'`/`'prefetch'`/`'shell'` 保证静态，动态混入 build 失败 |
| 路由段文件约定 | `_folder` 私有（不参与路由）、`(group)` 分组（不影响 URL）、`[param]` 动态段、`@slot` parallel routes（MUST 有 default.js [NX-8]） |

## 最佳实践

### 场景：数据获取分层（[NX-11]）

推荐路径：首屏/SEO 数据 RSC await 直取 → 交互式数据（筛选/无限列表/仪表盘）TanStack Query（+ HydrationBoundary 预取）→ 写操作 Server Action。

```tsx
// don't：client 组件 useEffect 首屏请求（瀑布 + 无流式）
'use client';
useEffect(() => { fetch('/api/users').then(r => r.json()).then(setUsers); }, []);

// do：RSC 直接 await
async function Page() {
  const users = await db.user.findMany();
  return <UserList users={users} />;
}
```

### 场景：Server/Client 组件组合（[NX-2]/[NX-3]）

推荐路径：边界下沉 → Server 内容用 `children` 组合传入 Client 组件 → 函数逻辑下放为 Server Action。

```tsx
// don't：Server 组件当 render props 传
<ClientComp renderHeader={() => <ServerHeader />} />

// do：children 组合
<ClientComp><ServerHeader /></ClientComp>
```

### 场景：Server Action 表单（[NX-6]）

推荐路径：`'use server'` → 鉴权 → zod 校验 FormData → 业务 → `updateTag`（16 read-your-writes）→ 乐观 UI 用 useActionState + useOptimistic。渐进增强：无 JS 也能提交。

```tsx
'use server';
async function createPost(formData: FormData) {
  await requireUser();                                    // 鉴权（LAW-5）
  const { title } = schema.parse(Object.fromEntries(formData));  // 校验
  await db.post.create({ data: { title } });
  updateTag('posts');                                     // read-your-owns-writes：单参数，立即过期
}
```

### 场景：'use cache' 缓存编排（cacheLife/cacheTag/updateTag 深度，16 稳定 API）

推荐路径（[官方文档](https://nextjs.org/docs/app/api-reference/directives/use-cache)）：`cacheComponents: true` 下用 `'use cache'`（函数/组件/文件级，**必须 async**）显式缓存 → 每个作用域**显式 `cacheLife(profile)`** → 按需失效按语境选 `updateTag`/`revalidateTag`。

- **cache key 四要素**：Build ID（`deploymentId` 覆盖）+ Function ID（代码位置 hash）+ 序列化参数 + dev HMR hash；**闭包变量自动捕获进 key**——**key 含 build id，新部署缓存全部失效**（跨部署持久用 `unstable_cache`/fetch cache）
- **请求时 API 禁入**：`cookies()/headers()/searchParams` 及其调用链均抛 `next-request-in-use-cache`；动态路由可过 build 在 start 才炸——正解：作用域外读值、按参数传入；**React.cache 在 use cache 边界内隔离**（外部存值不可见，传数据只能用参数）
- **序列化不对称**：参数走 RSC 序列化（更严），返回值可含 JSX；class 实例/函数/URL 不支持；children/Server Action 可 pass-through（不内省即可）
- **cacheLife 三属性**：`stale`（客户端直用）/ `revalidate`（后台再生成，ISR 式）/ `expire`（超时同步再生成；须 > revalidate）；**预设**：default 5m/15m/never、seconds 30s/1s/1min、minutes 5m/1m/1h、hours 5m/1h/1d、days 5m/1d/1w、weeks 5m/1w/30d、max 5m/30d/1y；自定义 profile 在 next.config `cacheLife`（可重定义内置名；**类型签名由 config 生成**）；cacheLife **不可在模块顶层调用**
- **prerender 参与阈值**：`revalidate: 0` 或 `expire < 5min` → 动态洞（请求时解析）；`stale < 30s` → 排除出 prerender；`stale` 30s~5min → 进 prerender 不进 App Shell——预设中仅 `seconds` 全中
- **嵌套规则**：外层显式 cacheLife 恒赢；外层未显式 → default（15min），**内层更短可拉短外层、更长不能延长**；**短命 cache 嵌进未显式 cacheLife 的外层 → prerender 报错**（可能在第三方依赖里）——修法：外层补显式 cacheLife
- **失效三 API 语境选型**：`updateTag(tag)`（**单参数**，仅 Server Actions，立即过期下一请求同步等新——read-your-own-writes）/ `revalidateTag(tag, profile)`（SA+Route Handler，`'max'` stale-while-revalidate，**不传 profile = legacy = 立即过期**）/ `refresh`；Server Action 内调任一失效 API → **整个客户端缓存立即清空**（绕过 stale）
- `cacheTag` 限制：单调用 ≤128 tag、每个 ≤256 字符（超限静默跳过 + console 警告）；外部 API 用 `fetch(url, { next: { tags } })`
- **运行时缓存随宿主变**：默认内存 LRU——**serverless 不跨请求持久**（build 时缓存正常）；自托管持久（`cacheMaxMemorySize`）；要 Redis/KV 用 `'use cache: remote'`（网络往返+平台费）；**proxy.ts 不做指令转换**——use cache 在 proxy 无效、cacheLife/cacheTag 抛错
- 客户端 `x-nextjs-stale-time` 头同步寿命；客户端 stale 最低强制 30 秒

### 场景：Streaming / Suspense 编排

推荐路径：慢数据包 `<Suspense>`（shell 先行）→ 路由级用 `loading.tsx` → 每语言/每区块一个边界。**官方推荐 Suspense 边界尽量靠近 runtime/uncached 数据访问点**（细粒度优于 loading.js）。坑：generateMetadata 慢查询在 15.2+ streaming metadata 下**不再阻塞 shell**（metadata 追加 body，仅 htmlLimitedBots 等待——见「场景：Metadata/SEO」）；勿把整页包一个 Suspense（失去流式粒度）；**layout 访问 uncached 数据（cookies()/headers()/未缓存 fetch）不会 fallback 到同段 loading.tsx——阻塞整个导航**（该访问单独包 Suspense 或移到 page.js）；Bots/crawlers 不流式（等完整渲染）。
- 来源：[官方文档](https://nextjs.org/docs/app/getting-started/fetching-data) + [模型经验]

### 场景：Instant Navigations（16.3+，Stream/Cache/Block）

推荐路径（[官方文档](https://nextjs.org/blog/next-16-3)）：开 `cacheComponents: true` + `partialPrefetching: true` → 每个慢数据点做 **Stream**（`<Suspense>` 包裹即见 loading）或 **Cache**（`'use cache'` 即见缓存 UI）→ 个别路由要服务端绑定就 **Block**（`export const instant = false`）。导航体验 SPA 级即时；Partial Prefetching 每 route 预取一个可复用 shell（客户端缓存整个会话），`<Link prefetch>` + `'use cache'` 追加按 link 深度预取（渲染到同步可用/URL 已知/cached 内容为止）。

```ts
// 防回归：instant() Playwright helper（@next/playwright）
import { instant } from '@next/playwright';
await instant(page, async () => {
  await page.click('a[href="/products/hats"]');
  await expect(page.locator('h1')).toContainText('Baseball Cap');  // 无网络即断言
});
```

边界条件：dev 下慢导航是 **error**（Instant Insights 面板给出修复 prompt）；`navigation()`/`prefetch()`（`next/cache`）在 `'use cache'` 组件内 await 可把重内容从预取中排除；ISR 增强——`generateStaticParams` 未覆盖页首访出即时 shell 后台升级；Navigation Inspector 在 DevTools 暂停于 shell 检查预取内容；试验性 `experimental.useOffline` 断网保 pending 重连重试（`useOffline()` hook from `next/offline`）。

### 场景：保证静态（ensureStatic，16.4+）

推荐路径（[官方文档](https://nextjs.org/blog/next-16-4)）：营销页/博客/电商等要控制成本的路由 `export const ensureStatic = 'navigation'`（layout 设置=作用于全部子页，可下推）——动态组件（如 UserAvatar）混入直接 **build 失败**；`'prefetch'`/`'shell'` 更细粒度档位。Migration/升级：`npx next@canary upgrade --agent=latest` 让 agent 执行版本升级（含 codemod 与验证）。

### 场景：AI SDK 7 流式聊天（Vercel AI SDK 集成）

推荐路径（[官方文档](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot)，**ai latest=7.0.173 / @ai-sdk/react 4.0.177**，2026-11-13 锚定）：先确认版本线——**v4/v5/v6/v7 四线并存且断裂面极大**（v5 客户端大断裂、v7 ESM-only），生成代码前必查 package.json 的 ai 大版本。

```tsx
// app/api/chat/route.ts（v7 无状态助手）
import { convertToModelMessages, createUIMessageStreamResponse, streamText, toUIMessageStream, UIMessage } from 'ai';
export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const result = streamText({ model: 'anthropic/claude-sonnet-5.5', instructions: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages) });
  return createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream }) });
}
// app/page.tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
const { messages, sendMessage, status, stop, regenerate } = useChat({
  transport: new DefaultChatTransport({ api: '/api/chat' }),
}); // input 自管（useState）；status: submitted|streaming|ready|error
```

- **版本线断裂速查**：v5——useChat 移至 `@ai-sdk/react`、Message→UIMessage（content→**parts**）、append→**sendMessage({text})**、reload→regenerate、isLoading→status、客户端 maxSteps 移除（→服务端 `stopWhen: isStepCount(N)/hasToolCall`）、tool parameters→**inputSchema**、args/result→input/output、transport 架构（DefaultChatTransport）、zod peer ≥4.1.8；v7——**ESM-only/Node ≥22**、`system`→**`instructions`**（messages 含 system 角色默认拒绝，存量用 `allowSystemInMessages: true` 仅限可信输入）、onFinish→**onEnd**（core 面）、fullStream→stream、请求/响应体默认不进结果（`include` 显式开）、telemetry 拆至 `@ai-sdk/otel` + registerTelemetry（注册即默认开）、工具 context 走 `contextSchema`+`toolsContext`/`runtimeContext`、needsApproval→`toolApproval`；codemod：`npx @ai-sdk/codemod v7`
- 消息渲染用 **parts**（text/reasoning/file/tool-` ${toolName}`/dynamic-tool/reasoning-file）；工具流：`onToolCall` + **`addToolOutput`（勿在 onToolCall 内 await——死锁）**、自动续发 `sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls`、tool part 状态机 input-streaming→input-available→output-available/output-error
- 动态请求值用 **sendMessage 第二参请求级配置**（transport 级 body 是静态捕获）；流恢复 `resumeStream: true`；直连 agent 免 HTTP 用 `DirectChatTransport({ agent })`
- 来源：[官方文档](https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0) + [官方文档](https://ai-sdk.dev/docs/migration-guides/migration-guide-7-0)

### 场景：i18n（next-intl 4）

推荐路径：动态段 `app/[locale]/` + 每语言根 layout（`<html lang>`）→ **next-intl 4**（peer Next 12-16 全线）→ 字典惰性动态 import 按语言分割。**`next/root-params`（新）**：`const locale = await lang()` 任意 Server Component 免 prop drilling 读 root 段；**不可用于 Client Components/Server Actions/Route Handlers**。类型：`PageProps<'/[lang]'>` + `await params`。坑：`generateStaticParams` 忘列 locale 则 SSG 其他语言 404。

**next-intl 4 集成四件套**：① `i18n/routing.ts`（`defineRouting({locales, defaultLocale})`）② `i18n/request.ts`（约定路径 src/ 或根；`getRequestConfig` 返回 `{locale, messages}`，可远程加载）③ `proxy.ts`（**Next 16 名；16 前叫 middleware.ts**）`createMiddleware(routing)` ④ 根 layout 包 **NextIntlClientProvider**（v4 无需显式传 messages/locale）。消费：Client/同步组件 `useTranslations('Namespace')`；async RSC `await getTranslations`（`next-intl/server`）。**locale 协商优先级（prefix 路由）**：pathname 前缀 → cookie → accept-language（best fit，@formatjs/intl-localematcher，en-GB 可匹配 en-US）→ defaultLocale。matcher 排除 `api|trpc|_next|_vercel|.*\\..*`；含点动态段（`/users/jane.doe`）须显式 matcher。**无 locale 时 next-intl 调 `notFound()` 中止渲染——须配 not-found 页**；static export（`output: 'export'`）下 proxy 不跑：localePrefix 恒 always、不可用 pathnames。
- 来源：[官方文档](https://nextjs.org/docs/app/guides/internationalization) + [官方文档](https://next-intl.dev/docs/getting-started/app-router) + [官方文档](https://next-intl.dev/docs/routing/middleware)

### 场景：文件上传（UploadThing 7 托管 / Server Actions 自管）

推荐路径双轨：**托管选 UploadThing 7.7.4**（托管 S3 + presigned URL，客户端 bundle ~25kB；注意该包 2025-08 后未再发版，选用前评估维护风险）；**自管走 Server Actions + FormData**（小文件直传自有存储/DB，大文件仍需分片或直传 S3）。

**UploadThing 7 集成（App Router）**：① `app/api/uploadthing/core.ts` 定义 FileRouter：`createUploadthing()`（`uploadthing/next` 入口）→ `f(routeConfig).input(schema).middleware(鉴权+metadata).onUploadComplete(...)`（builder 链 onUploadComplete MUST 最后）→ `satisfies FileRouter` ② `route.ts` 导出 `createRouteHandler` 的 `{GET, POST}`（`uploadthing/next` 仍返回具名导出；`uploadthing/server` 版 v7 起返回单 handler）③ 客户端 `generateUploadButton<OurFileRouter>()` / `generateUploadDropzone`（`@uploadthing/react`，类型化 re-export）④ **SSR 免 loading**：根 layout `<NextSSRPlugin routerConfig={extractRouterConfig(router)} />`（children 前；ppr/dynamicIO 下包 Suspense + `await connection()`）。
- **v7 破坏性**：`UPLOADTHING_SECRET` → **`UPLOADTHING_TOKEN`**（base64 JSON 合一：appId+region+API key；presigned URL 改自家服务端生成）；genUploader → `{uploadFiles, createUpload}`（断点续传）；skipPolling → 服务端 `awaitServerData`（默认 true）；input 校验 7.4+ 支持 **Zod/Effect Schema/Standard Schema**（Valibot/ArkType），**MUST JSON 可序列化**（z.date() 不行）；middleware 抛 `UploadThingError` 的 message 会下发客户端，**其他 error 一律转通用消息防泄漏**
- routeConfig 默认上限：image 4MB / video 16MB / audio 8MB / blob 8MB / pdf 4MB / text 64kB；maxFileCount 1；上传结果取 `file.ufsUrl`
- 来源：[官方文档](https://docs.uploadthing.com/getting-started/appdir) + [官方文档](https://docs.uploadthing.com/v7) + [官方文档](https://docs.uploadthing.com/file-routes)

### 场景：鉴权与 proxy.ts（[NX-8]）

推荐路径：proxy 层做**路由级粗粒度**（未登录重定向）→ 页面/布局做**细粒度**（`auth()` + `redirect()`）→ API 与页面鉴权双轨对齐。**官方立场：Proxy 是 "last resort"**——官方明确建议除非别无选择不用它。坑：proxy 里勿查库重活（每请求执行拖慢全站）；matcher 漏静态资源；**Server Function 不是独立路由（POST 到所在 route）——matcher 排除路径 = 同时跳过该路径 Server Function 调用，鉴权必须在每个 Server Function 内部验证**（不能只靠 Proxy）；`use cache`/`use server` 指令在 proxy 中无效；fetch 缓存选项（cache/next.revalidate/next.tags）不缓存 proxy 响应。工具面：`NextProxy` 类型 shorthand 自动推断 request/event 参数类型；后台任务 `event.waitUntil(promise)`；单测（experimental）用 `next/experimental/testing/server` 的 `unstable_doesMiddlewareMatch`/`isRewrite`/`getRewrittenUrl`。
- 来源：[官方文档](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) + [模型经验]

### 场景：鉴权库（Better Auth 1.7）

选型：**Better Auth 1.7.25**（2026-11-14，活跃；框架无关 TS auth 框架；2FA/passkey/multi-tenancy/SSO 全插件化）为主流新选——**next-auth 4.24.15 为另一线但 v5 长期 beta（5.0.0-beta.32）未 stable，新项目不推荐**。

- 集成：env `BETTER_AUTH_SECRET`（≥32 字符高熵；轮换用 `BETTER_AUTH_SECRETS` 复数渐进切换）+ `BETTER_AUTH_URL`；`auth.ts` 导出 `betterAuth({...})`（导出名 MUST `auth` 或 default）；数据库 drizzle/prisma/mongodb adapter（`better-auth/adapters/*`，须 provider 参数）或内置 Kysely 直连；无库可 stateless session（多数插件需库）
- 挂载：App Router `/api/auth/[...all]/route.ts` 导出 `toNextJsHandler(auth)` 的 {GET, POST}（`better-auth/next-js`）；Pages Router `toNodeHandler` + `bodyParser: false`；schema 用 `npx auth@latest generate|migrate`
- 消费：client `createAuthClient`（`better-auth/react`；useSession hook nanostores 响应式）；RSC/Server Action `auth.api.getSession({headers: await headers()})`
- **坑：server action 中调需设 cookie 的函数（signOut 等）静默不生效——MUST `nextCookies()` 插件（plugins 数组最后一个）**；RSC 不能设 cookie → cookie cache 不刷新直到客户端经 Server Actions/Route Handlers 交互
- 鉴权分层（对齐 [NX-8]）：proxy 只查 cookie 存在性做乐观重定向（`getSessionCookie()` **只查存在不验证——非安全，页面/路由 MUST 再验 session**）；Next 16+ proxy Node runtime 可全量验证；Next 16 迁移 codemod `npx @next/codemod@canary middleware-to-proxy .`（Better Auth 方法全部不变）
- 来源：[官方文档](https://www.better-auth.com/docs/installation) + [官方文档](https://www.better-auth.com/docs/integrations/next)

### 场景：支付（Stripe Checkout Sessions）

选型：**stripe 23.1.0**（服务端 SDK；Node ≥20）+ **@stripe/stripe-js 10.3.0 / @stripe/react-stripe-js 7.1.0**（客户端）。**官方立场：Checkout Sessions API + Payment Element 优于 Payment Intents**——"Don't use the Payment Intent API unless the user explicitly asks"（Adaptive Pricing 仅 Checkout Sessions；训练记忆中的 ElementsProvider/PaymentElement/useElements/confirmPayment 是 PaymentIntents 旧路线，双轨注意防混淆）。

- **建 Session（服务端）**：POST /v1/checkout/sessions（ui_mode=elements + line_items + mode=payment + return_url 含 `{CHECKOUT_SESSION_ID}` 占位）→ 返回 client_secret 传客户端；**Session 24h 过期**
- **收银台（客户端，新 API）**：`@stripe/react-stripe-js/checkout` 子路径导出 **CheckoutElementsProvider**（stripe + options.clientSecret）→ 内部 **useCheckoutElements()**（loading/error/success 判别联合）+ PaymentElement/ContactDetailsElement/ShippingAddressElement + `checkout.confirm()`；`checkout.on('change', session)` 监听 canConfirm 控制 Pay 按钮
- **坑：Session 创建端点防滥用（官方四控制 MUST）**——①参数服务端构建（勿转发客户端任意 Session 参数）②访问控制 ③限频（**幂等 key 不是防滥用**）④bot 检查服务端验证（前端 CAPTCHA 不保护可直连端点）
- **坑：Payment Element iframe 勿嵌套另一 iframe**（部分支付方式需重定向确认）；Apple/Google Pay 须 iframe `allow="payment *"`；**生产必须 HTTPS**
- **Webhook 履约**：`stripe.webhooks.constructEvent(rawBody, sig, secret)` 验签——**raw body 必须是未改动原始请求体**（App Router route handler 用 `await req.text()` 原文；**body parser 先跑会破坏签名**）；Stripe-Signature 含 t/v1/v0（**v0 sandbox 伪签名必须忽略**）；默认 tolerance 5 分钟；**事件无顺序保证——用 event ID 幂等去重**；快速返回 2xx 再做复杂逻辑；CSRF 豁免 webhook 路由；本地测试 `stripe listen --forward-to localhost:3000/api/webhook` + `stripe trigger`
- 测试卡：4242424242424242 成功 / **4000002500003155 需 SCA 3DS** / 4000000000009995 declined；**`stripe sandbox create` 免注册匿名 sandbox（为 coding agent 设计）**
- 来源：[官方文档](https://docs.stripe.com/payments/accept-a-payment?payment-ui=elements&api-integration=checkout) + [官方文档](https://docs.stripe.com/webhooks)

### 场景：邮件（React Email + Resend）

选型：**@react-email/components 1.0.12**（React 组件邮件模板，1.0 stable；主流邮件客户端全测）+ **resend 6.38.1**（同团队，Node ≥20）。

- **Resend SDK 红线**：返回 **`{ data, error }` 不 throw**（勿 try/catch 代替错误检查）；参数 camelCase（replyTo/scheduledAt）；包名 `resend` 类 `Resend`；**react 参数 MUST 函数调用**：`react: EmailTemplate({ name: 'John' })`（非 JSX）；template 与 html/text/react 互斥
- Next.js 集成：App Router `app/api/send/route.ts` POST route handler；前提 RESEND_API_KEY + 域名验证（**onboarding@resend.dev 仅测试**）；**rate limit 10 req/s（429）**；**idempotencyKey 防重发**（`<event-type>/<entity-id>` 模式，24h 过期）
- React Email：`render(<Template/>)` → HTML（`react-email` 包，另有 pretty/toPlainText）；**浏览器跑 render 需 web-streams-polyfill（Safari/iOS ReadableByteStreamController）**；`data-skip-in-text="true"` 排除纯文本输出
- 测试地址族（不损域名声誉）：delivered@/bounced@/complained@/suppressed@resend.dev；Webhooks 有 replay/验签/CLI 监听/MCP server
- 来源：[官方文档](https://react.email/docs) + [官方文档](https://resend.com/docs/send-with-nextjs)

### 场景：错误监控（Sentry v11）

选型：**@sentry/nextjs 11.12.0**（Node ≥20.19.0；peer Next 14-16；**五版本线并存 v7-v11——先 `npm ls @sentry/nextjs` 确认版本线**；@sentry/nestjs 11.12.0 peer Nest 8-12）。

- **三文件初始化（v11）**：`instrumentation-client.ts`（浏览器）+ `sentry.server.config.ts`（Node）+ `sentry.edge.config.ts`（Edge）；`instrumentation.ts` 的 `register()` 按 `NEXT_RUNTIME` 动态导入 + **`export const onRequestError = Sentry.captureRequestError`**（捕获 RSC/route handler/proxy 错误）
- App Router 渲染错误：`app/global-error.tsx` 内 `Sentry.captureException(error)`
- `withSentryConfig` 包装 next.config（build 插桩 + source maps 上传 + `tunnelRoute: "/monitoring"` 防广告拦截——**tunnel route 只转发 body 有版本门槛 v10≥10.77.1 / v11≥11.9.0**）；source maps：CI 用 `SENTRY_AUTH_TOKEN`
- Logs：`Sentry.logger.info/warn/error`（console/Pino/Winston 集成自动捕获）；Metrics：`Sentry.metrics.count/gauge/distribution`；**Agent Tracing：AI 库自动插桩（AI SDK/LangChain token usage）+ MCP Monitoring**
- 数据控制：内置 denylist（auth/password 键发 `[Filtered]`）；`dataCollection: { userInfo: false }`；坑：浏览器 devtools 触发的错误被沙箱化不进 Sentry
- 来源：[官方文档](https://docs.sentry.io/platforms/javascript/guides/nextjs/)

### 场景：自托管与多实例部署（self-hosting / standalone）

- **反向代理**：nginx 前置而非直暴 Next server（畸形请求/慢连接/限流由代理承担）
- **standalone 镜像**：`output: 'standalone'` → `.next/standalone/` + 最小 `server.js`（`node server.js` 免装 node_modules；PORT/HOSTNAME env）；**MUST 手动复制 `public/` 与 `.next/static/`（设计上交给 CDN）**；Windows symlink 需开发者模式，junction fallback 不可重定位
- **多实例三件套（MUST）**：① `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` 全实例同 key（base64 AES 16/24/32 字节——不同 key → "Failed to find Server Action"）② `deploymentId` 版本倾斜保护（`?dpl=` 参数 + `x-deployment-id` header，mismatch 触发 hard navigation；build ID 可 `generateBuildId` 定制（如 GIT_HASH）保持多容器一致）③ 共享缓存 handler（`cacheMaxMemorySize: 0` + 自定义 handler：共享存储/有界/**序列化 Buffer+Map（否则 `segmentData.get is not a function`）**/按 tag 索引/**`refreshTags()` 每请求同步 tag 状态**）
- **env 分界**：NEXT_PUBLIC_ 构建期内联；服务端 env 运行时读（`await connection()` 后）→ 单镜像多环境晋升
- **流式**：nginx 禁缓冲 `X-Accel-Buffering: no`；LB/代理须透传 chunked（AWS ALB+Lambda 默认缓冲）；PPR 必须流式否则失去 TTFB 优势；after() 优雅停机 drain 10-30s
- trace 补漏：`outputFileTracingRoot`（monorepo 外部文件）+ `outputFileTracingIncludes/Excludes`（键=route glob、只作用 server trace——Edge Runtime 路由与纯静态页不受影响）；sharp/aws-crt 等 native 资产常见需显式 include
- 来源：[官方文档](https://nextjs.org/docs/app/guides/self-hosting) + [官方文档](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)

### 场景：Metadata/SEO 与静态资产（generate-metadata / image / font）

- **导出规则**：`metadata`/`generateMetadata` 仅 Server Components（`'use client'` 段被忽略）[NX-14]；同段二者互斥；file-based metadata（favicon.ico/opengraph-image.* 等）优先于 config
- **title 层级**：`template: '%s | Acme'` 只应用于**子段**、对自身无效；`default` 兜底整树；`absolute` 逃逸父 template；无 title 的段不渲染 `<title>`
- **URL 组合**：metadataBase + 相对 canonical/openGraph.url 拼绝对；metadataBase 默认取 env `NEXT_PUBLIC_METADATA_BASE_URL` > VERCEL_URL > localhost
- **streaming metadata（15.2+）**：慢 generateMetadata 不阻塞 UI——shell 先流式、metadata 追加 body；**htmlLimitedBots（facebookexternalhit/WhatsApp/Twitterbot 等）例外**：等待完整渲染一次返回
- **浅合并**：父 layout 与子段按字段浅合并——`openGraph` 对象被**子段整对象覆盖**（父 OG 图片丢失），子段须重声明
- **Cache Components 交互**：generateMetadata 内调用 `'use cache'` 函数不缓存页面；metadata 内 fetch 自动去重（同参数集仅一次请求）
- **viewport/themeColor**：14+ 从 metadata 移除，须 `viewport`/`generateViewport` 导出，否则构建警告且不生效
- **next/image**：16 起 `priority` **弃用，改 `preload`**；`fill` 必配 `sizes`；`qualities` 默认 `[75]`（其他 q 值须 next.config 声明）；remotePatterns 支持通配；SVG 图源须三件套（`dangerouslyAllowSVG` + `contentDispositionType` + `unoptimized`/CSP）；静态导入自动带 blurDataURL；多 art direction/背景图用 `getImageProps`（`<img>` 手写属性，不绕过优化）
- **next/font**：Google 字体**构建时自托管**（运行时零网络请求）；`subsets` 仅控制预加载子集，省略发警告；多 weight/变体用字体定义文件；预加载范围=声明段及其子树（layout 声明=全站预载，页面声明=仅该页）
- 来源：[官方文档](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) + [官方文档](https://nextjs.org/docs/app/api-reference/components/image) + [官方文档](https://nextjs.org/docs/app/api-reference/components/font)

### 场景：动态段静态化与按路径失效（generateStaticParams / revalidatePath）

- **generateStaticParams 基础**：配合动态段构建期静态生成路由（pages/layouts/route handlers 皆可），取代 Pages Router `getStaticPaths`；返回 params 对象数组（catch-all 为 `{ slug: string[] }[]`）；**必须恒返回数组**（否则该路由动态渲染）；`next build` 时在 Layouts/Pages 生成前运行；**ISR revalidation 时不再调用**
- **dynamicParams 语义**：默认 true（未列路径运行时首访按需生成）；`export const dynamicParams = false` 后未列路径 404（catch-all 按规则匹配）
- **三种策略**：全量（返回全列表）/ 子集+false（其余 404）/ 全运行时（返回 `[]` 或 `export const dynamic = 'force-static'`）
- **Cache Components 硬约束 [NX-15]**：动态路由至少返回一个 param——空数组 build error；构建期未知真实值用占位（`[{ slug: '__placeholder__' }]`）+ 页面内 `notFound()`（会削弱构建期校验）；`ensureStatic = 'navigation'` 路由须至少一个含全部动态参数的 params 对象
- **多动态段**：自底向上（page 同时生成两段）或自顶向下（父 layout 先生成，子段 generateStaticParams 收父 params、每套父参数执行一次）；**只能生成当前段及上方段，不能生成下方段**；root parameter 可经 `next/root-params` getter 读
- **请求去重**：fetch 在所有 generate 前缀函数/layouts/pages/RSC 间自动 memoized；fetch 不可用用 React `cache`
- **revalidatePath 调用面**：仅 Server Functions 与 Route Handlers（Client/Proxy 不可）；Server Function 中立即更新 UI（当前还刷新所有已访问页——临时行为）；Route Handler 中仅**标记**路径、下次访问再生效
- **revalidatePath 参数**：`revalidatePath(path, 'page'|'layout'?)`——字面量路径免 type；**含动态段必须传 type**；path 指路由文件结构（大小写敏感、≤1024 字符、无尾斜杠）；layout 失效该段 layout+嵌套+下方全部页；`('/', 'layout')` 清 Client Cache 全失效；**rewrites 下传 destination（真实路由路径）非浏览器地址**
- **与 tag 系互补**：revalidatePath=路径维度（其他用同数据的页面**仍旧缓存**）；revalidateTag=标 stale；updateTag=过期——组合 `revalidatePath` + `updateTag` 保证全站一致
- 来源：[官方文档](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) + [官方文档](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | `getServerSideProps` 不执行 | App Router 项目混写 Pages Router API | [NX-5] |
| 2 | bundle 巨大全进客户端 | `'use client'` 放太高层 | 边界下沉 [NX-2] |
| 3 | 缓存行为与预期完全不符 | 按旧版本语义答（14/15/16 反转） | 先查版本 [NX-1]，对照下表 |
| 4 | `const { id } = params` 报错 | 16 起全异步化 | `await params` [NX-4] |
| 5 | `useState only works in Client Components` | RSC 用 hooks / 传函数 props | [NX-3] |
| 6 | 16 构建/开发报 parallel route 错 | `@slot` 缺 default.tsx | [NX-8] |
| 7 | `Hydration failed ... didn't match` | render 期读 Date.now/localStorage/window | [NX-10]；CSS 分支用 `use(browser())` |
| 8 | 控制台 middleware 弃用警告 | 16 应 proxy.ts | [NX-8] |
| 9 | 表单提交后不跳转，日志 `NEXT_REDIRECT` 被捕 | redirect 被 try/catch 吞 | 重抛 [NX-7] |
| 10 | Server Action 未鉴权被直调 | 当可信内部函数 | [NX-6]/LAW-5 |
| 11 | 导航卡住无 loading（layout 有 cookies()/未缓存 fetch） | 同段 loading.tsx 不覆盖 layout uncached 访问 | 单独 Suspense 包该访问/移到 page.js |
| 12 | error.tsx 里 `reset` 未定义 | 现行签名 `{ error, retry }`（retry 取代 reset） | 改用 `retry()`；组件级边界用 `catchError`（next/error） |
| 13 | Client Component import `next/root-params` 构建失败 | root 段 getter 仅限 Server Component/服务端工具 | locale 经 props/context 传入 client |
| 14 | 16.3+ dev 报慢导航 error（Instant Insights） | Cache Components 下未 Stream/Cache 的阻塞导航 | `<Suspense>`/`'use cache'`；个别路由 `export const instant = false` |
| 15 | 自托管 Cache Components 页面 shell 被污染/持久 404 | `next start` + Partial Prefetching 未开（GHSA-pc58） | `partialPrefetching: true` + 升 16.4.6 [NX-12] |
| 16 | 跨租户缓存泄漏（use cache 结果串租户） | 读 root 参数的 use cache 又被 unstable_cache 包装（GHSA-mfr8） | 升 16.4.6/15.5.29；拆开组合 [NX-13] |
| 17 | Edge route 的 HttpOnly cookie 被 same-origin JS 读到 | `NextResponse.cookies.set()` 序列化进 `x-middleware-set-cookie` 内部头（GHSA-f3mh） | `cookies().set()`；升 16.4.6 [NX-12] |
| 18 | Stripe webhook 验签恒失败（签名不匹配） | raw body 被解析器改动/重新序列化 | `await req.text()` 原文验签 [场景：支付] |
| 19 | metadata/generateMetadata 不生效 | `'use client'` 文件导出被忽略 | 移到 Server Component 导出 [NX-14] |
| 20 | 构建警告未设 metadataBase / OG 链接拼错 | 相对 URL 无基准 | 设 metadataBase 或 env `NEXT_PUBLIC_METADATA_BASE_URL` [NX-14] |
| 21 | 子页面丢失父段 openGraph 图片 | metadata 浅合并——openGraph 被子段整对象覆盖 | 子段重声明完整 openGraph |
| 22 | image 16 弃用警告 / SVG 图源不渲染 | `priority` 已弃用；SVG 默认被安全拦截 | `preload` 替代；SVG 三件套 `dangerouslyAllowSVG`+`contentDispositionType`+`unoptimized` |
| 23 | Cache Components 动态路由构建报 empty-generate-static-params | 返回了空数组 | 至少一个 param；未知值用 placeholder + `notFound()` [NX-15] |
| 24 | 动态段 revalidatePath 报错要求 type | 含动态段必须传 `'page'`/`'layout'` | 动态段路径必传 type；字面量路径免传 |
| 25 | 被 rewrite 的页面 revalidatePath 无效 | 缓存按路由文件打 tag，非浏览器地址 | 传 destination（真实路由路径） |
| 26 | revalidatePath 后其他用同数据的页面仍旧 | 路径维度失效，不碰 tag | 组合 `updateTag`/`revalidateTag` 保证一致 |

**缓存对照表（[NX-1] 硬事实）** [官方文档](https://nextjs.org/blog)：

| 版本 | fetch 默认 | GET route handler |
|---|---|---|
| ≤14 | 缓存（force-cache） | 静态 |
| 15 | 不缓存（no-store） | 动态 |
| 16（cacheComponents） | 全动态，`'use cache'` 显式缓存 | 动态 |

**Top 展开：坑点 7（hydration mismatch）**：分层处理——CSS 类切换 `use(browser())`（服务端 suspend、客户端不）；纯客户端组件下沉 `'use client'`；禁止 render 期读 localStorage [NX-10]。

## API 速查表

| API | 签名要点 | 易错点 |
|---|---|---|
| layout.tsx | 跨导航持久，`await params` | active 态需 client + usePathname |
| loading.tsx / error.tsx | Suspense fallback / ErrorBoundary | error.tsx 必须 `'use client'`；props 为 `{ error, retry }` |
| catchError（next/error） | 组件级错误边界工厂 `catchError(Fallback)` | Fallback 签名 `(props, { error, retry })` |
| next/root-params | root 动态段 getter：`await lang()` | 仅 RSC/服务端工具；禁 Client/Action/RouteHandler |
| generateMetadata | async，props 收 params/searchParams；与 metadata 导出互斥 | 仅 RSC；streaming（15.2+）不阻塞 shell（htmlLimitedBots 除外）；浅合并 [NX-14] |
| metadataBase | 基准 URL，相对 canonical/OG 拼绝对 | env `NEXT_PUBLIC_METADATA_BASE_URL` 优先；默认 localhost 兜底 |
| viewport / generateViewport | themeColor/colorScheme 等 | 14+ 从 metadata 移除；旧写法构建警告不生效 |
| next/image | src/width/height 或 fill+sizes；`preload`（16，替代 priority） | fill 必配 sizes；qualities 默认 [75]；SVG 源三件套 |
| next/font | localFont / Google 字体构建时自托管 | subsets 省略警告；预加载范围=声明段子树 |
| `'use cache'`（16 稳定） | 函数/组件/文件级显式缓存（须 async） | 内禁 cookies()/headers()/searchParams 及其调用链；React.cache 隔离；key 含 build id |
| cacheLife（16 稳定） | stale/revalidate/expire 三属性；预设 seconds~max | expire 须 > revalidate；不可模块顶层调用；短命嵌套未显式外层 prerender 报错 |
| revalidateTag | 16 双参 `(tag, profile)`；`'max'` stale-while-revalidate | 不传 profile = legacy = 立即过期 [NX-9] |
| updateTag / refresh | `updateTag(tag)` **单参数**；仅 Server Actions | read-your-writes 立即过期；下一请求同步等新 |
| useActionState | `[state, formAction, isPending]` | action 签名 `(prevState, formData)` |
| redirect / notFound | server 端跳转/404 | try/catch 中重抛 [NX-7] |
| proxy.ts（16） | `export default function proxy(req)` | Node 运行时；勿重活 |
| route.ts | GET/POST 导出；15 起默认动态 | `force-static` 才构建时执行 |
| ensureStatic（16.4） | `'navigation'`/`'prefetch'`/`'shell'` | 动态混入 build 失败；layout 级作用全子页 |
| navigation() / prefetch()（16.4） | `'use cache'` 组件内 await，排除预取内容 | from `next/cache` |
| instant()（16.3） | `await instant(page, fn)` Playwright helper | from `@next/playwright`；防导航回归 |
| export const instant | `= false` 退出即时导航（Block） | 仅个别服务端绑定路由用 |
| useOffline（实验） | `useOffline()` + `experimental.useOffline` | 断网 pending 重试 |
| import.meta.glob（16.3） | Turbopack 内建 Vite 兼容 glob 导入 | .md 等需注册 loader |
| next upgrade --agent（16.4） | `npx next@canary upgrade --agent=latest` | agent 执行升级+codemod+验证 |
| generateStaticParams | 恒返回 params 数组（catch-all 为 `string[]`）；`dynamicParams=false` 未列 404 | Cache Components 至少 1 param [NX-15]；ISR revalidation 不再调用；多段只能生成自身及上方段 |
| revalidatePath | `(path, 'page'\|'layout'?)`；含动态段必传 type | 仅 SF/RH 可调；SF 立即生效 vs RH 标记下次生效；rewrites 传 destination；与 updateTag/revalidateTag 互补 |
| dynamicParams | `export const dynamicParams = false` | 默认 true：未列路径运行时按需生成 |

## 版本注意

- 当前最新：**Next.js 16.4.6**（docs `@doc-version: 16.4.6` 精确锚定，2026-11-15）[官方文档](https://nextjs.org/docs/llms.txt)；安全线：2026-11-03 安全发布 **16.4.5/15.5.29**（npm latest 16.4.6 含修复）；月度安全发布节奏（2026-07 起正式 security release program）[官方文档](https://nextjs.org/blog/november-2026-security-release)
- **16.4（2026-10-06）** [官方文档](https://nextjs.org/blog/next-16-4)：**官方推荐 Cache Components 用于所有应用（Next 17 默认）**；`ensureStatic` 三档；`navigation()`/`prefetch()` 预取排除 API；`next upgrade --agent`；experimental.agentUpgrade（'security' 默认）/agentFeedback；Turbopack 磁盘缓存 Zstd -20~25%/lazy server HMR/runtime 单 chunk/CSS Module 短类名+export mangling；实验族：turbopackRustReactCompiler（fast skip 内存 -30% 编译 -15%）/turbopackGc/turbopackLazyDynamicImports/turbopackPluginRuntimeStrategy workerThreads（**Node 24.13.1+ 回退子进程**）/turbopackAdditionalRoots（pnpm global virtual store 手动集成）；**React 19.3 stable View Transitions、Fragment Refs、browser() API**；next-bundle-optimizer agent skill
- **16.3（2026-08-03）** [官方文档](https://nextjs.org/blog/next-16-3)：**Instant Navigations**（Stream/Cache/Block + Instant Insights dev error + `instant()` helper + Navigation Inspector + ISR 即时 shell 增强）；dev 内存 -90%（memory eviction+磁盘缓存默认开）；`next build` 磁盘缓存默认开（CI 最高 5.5×）；**`next build` 可用 TypeScript 7**（useTypeScriptCli）；SSR native Node streams +22% 吞吐；`catchError` 自定义错误边界（retry() 可重取 Server Components）；`import.meta.glob`（Turbopack 内建）；root params（`next/root-params`）；prefetchInlining；AGENTS.md 版本匹配文档自动维护；实验 Rust React Compiler（冷 -34% 热 -46%）/useOffline
- 16.2（2026-03-18）：Adapter API stable + Verified Adapters 测试套件 [官方文档](https://nextjs.org/blog/next-16-2)
- **2026-11 安全发布 7 CVE**（16.4.5/15.5.29 修复）[官方文档](https://nextjs.org/blog/november-2026-security-release)：High——unstable_cache×use cache 跨租户泄漏（GHSA-mfr8）；Medium——嵌套 use cache 跨根参数（GHSA-vc7v）/二进制参数 cache 身份碰撞跨用户（GHSA-rhh4）/**自托管 shared shell 投毒（Partial Prefetching 未开即中招，GHSA-pc58）**/stale 压缩 framing 跨客户端注入（HTTP/1.1 pipelining）/x-middleware-set-cookie 泄漏（Edge NextResponse.cookies.set，GHSA-f3mh）/SVG AVIF 误分类绕过（GHSA-7qx7）
- **16 缓存模型（Cache Components，硬事实）** [官方文档](https://nextjs.org/docs/app/getting-started/caching)：
  - create-next-app 新项目**默认已启用** Cache Components + Partial Prefetching；存量项目 next.config.ts 显式 `cacheComponents: true` + `partialPrefetching: true`（不设后者会警告；下个大版本两者默认全开、选项移除）
  - **`'use cache'` 三变体**：通用 / `'use cache: private'`（直读 cookies/headers/searchParams，结果存浏览器）/ `'use cache: remote'`（durable cache handler 共享，高命中才划算）
  - 每个 cache 指令建议配 `cacheLife`；参数与闭包捕获值自动进 cache key；**cache key 含 build id——新部署缓存全部失效**
  - 缓存存储三处：prerendered HTML（CDN）/ 共享存储（默认 per-instance 内存，serverless 易失）/ 浏览器（RSC payload）
  - PPR 是 Cache Components 默认行为；runtime API 访问 → `<Suspense>` 包裹或提取值传给 cached 函数；随机值/时间戳 → `await connection()` 或 use cache
- Next 16（2025-10-21）[官方文档](https://nextjs.org/blog/next-16)：Cache Components、proxy.ts、Turbopack 默认、强制 await、`default.js`、移除 `next lint`/AMP；Node 20.9+、TS 5.1+
- Next 15 线仅安全维护（2026-10）[官方文档](https://nextjs.org/blog)
- **部署模型** [官方文档](https://nextjs.org/docs/app/getting-started/deploying)：Node.js server（`next build`+`next start`，全特性）/ Docker（`output: "standalone"` 最小镜像，全特性）/ static export（`output: "export"`，受限且**不支持 proxy**）/ Adapters；**Verified Adapters**（跑官方兼容测试套件）：Vercel、Bun；Cloudflare/Netlify 在建，其余平台集成未经官方验证
- **React 19.3（Next 16 锁 React 19 线）** [官方文档](https://react.dev/blog/2026/09/09/react-19-3)：ViewTransition/addTransitionType/Fragment Refs/`use(browser())`/Trusted Types/RSC 直接渲染 Context；**安全警报：RSC 存在未认证 RCE（2025-12 披露），React 必须 ≥19.2.1**（19.0.1/19.1.2/19.2.1 修复）
- 15 回顾：fetch 默认 no-store、GET handler 默认动态、router cache staleTime=0、React 19
- **Metadata 流式（15.2+）**：慢 generateMetadata 不阻塞 UI（shell 先发、metadata 追加 body）；仅 htmlLimitedBots 等完整渲染；`priority` 16 弃用改 `preload`；viewport/themeColor 走 `generateViewport` [官方文档](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)
- AI SDK 集成：**ai 7.0.173 / @ai-sdk/react 4.0.177**（2026-11-13；v4-v7 四线并存；v7 ESM-only、Node ≥22；zod peer ^3.25.76 || ^4.1.8）[官方文档](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot)
- i18n 集成：**next-intl 4.15.1**（2026-11-12；peer Next 12-16 全线 + React 16.8-19；App/Pages Router 双支持）[官方文档](https://next-intl.dev/docs)
- 上传集成：**uploadthing 7.7.4**（2025-08-17 后未再发版——选用前评估维护风险；v7 起 UPLOADTHING_TOKEN 单环境变量、presigned URL 自家服务端生成）[官方文档](https://docs.uploadthing.com/v7)
- 鉴权集成：**better-auth 1.7.25**（2026-11-14，活跃；peer Next 14-16/React 18-19）；**next-auth 4.24.15（v5 长期 beta 未 stable，新项目不推荐）**
- 支付集成：**stripe 23.1.0 / @stripe/stripe-js 10.3.0 / @stripe/react-stripe-js 7.1.0**（2026-11；官方推荐 Checkout Sessions + Payment Element，Payment Intents 仅显式要求时用）[官方文档](https://docs.stripe.com/payments/accept-a-payment?payment-ui=elements&api-integration=checkout)
- 邮件集成：**@react-email/components 1.0.12 / resend 6.38.1**（同团队；SDK `{data, error}` 不 throw、react 参数函数调用、10 req/s、idempotencyKey 防重发）[官方文档](https://resend.com/docs/send-with-nextjs)
- 监控集成：**@sentry/nextjs 11.12.0 / @sentry/nestjs 11.12.0**（2026-11-10；**v7-v11 五版本线并存**；Node ≥20.19.0）[官方文档](https://docs.sentry.io/platforms/javascript/guides/nextjs/)

## 与其他子领域的集成要点

- **react-core**：App Router 内 React 版本由框架锁定（16 = React 19）→ `kb/react-core.md`
- **NestJS**：Nest 承担业务 API，Next 只做 BFF/页面 → `kb/nestjs.md`
- **react-admin**：可跑 Next.js 上，但 `<Admin>` 所在文件必须 `'use client'` → `kb/react-admin.md`
- **TanStack Query**：交互式数据 useQuery + HydrationBoundary；SSR 工厂模式（LAW-3）→ `kb/tanstack-query.md`

## 来源索引

- Next.js 官方博客：https://nextjs.org/blog [官方文档]
- **Next 16.4 发布文（ensureStatic/navigation()/agent 工具/Turbopack 优化/实验族）**：https://nextjs.org/blog/next-16-4 [官方文档]
- **Next 16.3 发布文（Instant Navigations/TS 7/内存与构建优化/catchError/import.meta.glob/root params）**：https://nextjs.org/blog/next-16-3 [官方文档]
- **Instant Navigations 专题（Stream/Cache/Block/Partial Prefetching 设计）**：https://nextjs.org/blog/next-16-3-instant-navigations [官方文档]
- **2026-11 安全发布（7 CVE/GHSA 清单）**：https://nextjs.org/blog/november-2026-security-release [官方文档]
- Next 16 升级指南：https://nextjs.org/blog/next-16 [官方文档]
- Next.js 文档：https://nextjs.org/docs [官方文档]
- **Caching 指南（Cache Components 全模型）**：https://nextjs.org/docs/app/getting-started/caching [官方文档]
- **'use cache' 指令（cache key 四要素/请求时 API 禁入/序列化不对称/React.cache 隔离/宿主相关运行时缓存/proxy 不转换）**：https://nextjs.org/docs/app/api-reference/directives/use-cache [官方文档]
- **cacheLife（三属性/预设表/prerender 阈值/嵌套规则/自定义 profile）**：https://nextjs.org/docs/app/api-reference/functions/cacheLife [官方文档]
- **cacheTag + updateTag（128×256 限制/updateTag 仅 SA 单参/revalidateTag profile 语义）**：https://nextjs.org/docs/app/api-reference/functions/cacheTag 、https://nextjs.org/docs/app/api-reference/functions/updateTag [官方文档]
- **Proxy（getting-started + file-conventions API 参考）**：https://nextjs.org/docs/app/api-reference/file-conventions/proxy [官方文档]
- **错误处理（retry/catchError/error.tsx）**：https://nextjs.org/docs/app/getting-started/error-handling [官方文档]
- **数据获取与 Streaming（loading.js 坑/preload/React.cache）**：https://nextjs.org/docs/app/getting-started/fetching-data [官方文档]
- **i18n（next/root-params/PageProps）**：https://nextjs.org/docs/app/guides/internationalization [官方文档]
- **部署（standalone/Verified Adapters）**：https://nextjs.org/docs/app/getting-started/deploying [官方文档]
- React 19.3 发布文（ViewTransition/browser()/RSC 安全修复）：https://react.dev/blog/2026/09/09/react-19-3 [官方文档]
- **文档全量索引**：https://nextjs.org/docs/llms.txt [官方文档]
- 组合模式：https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns [官方文档]
- [模型经验]：坑点 1/5/9/10 故障模式、streaming/i18n/proxy 鉴权路径——适用 App Router 全版本
- 法则条款来源：corpus/react/nextjs/elicited/10-laws.md


- **Vercel AI SDK 7 useChat 全流（sendMessage/status/transport/parts/工具流/throttle/queue）**：https://ai-sdk.dev/docs/ai-sdk-ui/chatbot [官方文档]
- **AI SDK 4→5 迁移（UIMessage.parts/sendMessage/stopWhen/inputSchema/transport 架构）**：https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0 [官方文档]
- **AI SDK 6→7 迁移（ESM-only/instructions/onEnd/无状态响应助手/toolApproval/toolsContext/@ai-sdk/otel）**：https://ai-sdk.dev/docs/migration-guides/migration-guide-7-0 [官方文档]

### 第八轮新增（next-intl 4）

- **next-intl App Router 集成（四件套/getRequestConfig/useTranslations/getTranslations）**：https://next-intl.dev/docs/getting-started/app-router [官方文档]
- **next-intl Proxy/middleware（locale 协商优先级/best fit/matcher/static export 限制/notFound 兜底）**：https://next-intl.dev/docs/routing/middleware [官方文档]

### 第八轮新增（文件上传）

- **UploadThing 索引与 File Routes（builder 链/routeConfig 默认上限/input 校验器矩阵）**：https://docs.uploadthing.com/file-routes [官方文档]
- **UploadThing Next.js App Router（createRouteHandler/NextSSRPlugin）**：https://docs.uploadthing.com/getting-started/appdir [官方文档]
- **UploadThing v6→v7 迁移（UPLOADTHING_TOKEN/genUploader 对象/awaitServerData/具名导出移除）**：https://docs.uploadthing.com/v7 [官方文档]

### 第九轮新增（Better Auth）

- **Better Auth 安装（env/数据库 adapter/CLI generate-migrate/多框架挂载/Express v5 通配符）**：https://www.better-auth.com/docs/installation [官方文档]
- **Better Auth 基础用法（signUp 自动登录/useSession/auth.api 服务端/插件三步）**：https://www.better-auth.com/docs/basic-usage [官方文档]
- **Better Auth Next.js 集成（toNextJsHandler/nextCookies/鉴权分层/getSessionCookie/Next 16 codemod）**：https://www.better-auth.com/docs/integrations/next [官方文档]

### 第九轮新增（Stripe 支付）

- **Stripe Accept a payment（Checkout Sessions + Payment Element/CheckoutElementsProvider/防滥用四控制/测试卡/stripe sandbox）**：https://docs.stripe.com/payments/accept-a-payment?payment-ui=elements&api-integration=checkout [官方文档]
- **Stripe Webhooks（验签/raw body 红线/thin vs snapshot 事件/幂等去重/重试语义/CLI listen）**：https://docs.stripe.com/webhooks [官方文档]

### 第十轮新增（邮件）

- **React Email 文档（组件集合/render/pretty/toPlainText/data-skip-in-text/浏览器 polyfill/17 ESP 集成）**：https://react.email/docs [官方文档]
- **Resend Next.js 快速开始（{data,error} 模式/react 函数调用非 JSX/idempotencyKey/测试地址族/Webhooks/MCP）**：https://resend.com/docs/send-with-nextjs [官方文档]

### 第十一轮新增（Sentry）

- **Sentry Next.js SDK v11（三文件初始化/instrumentation register/onRequestError/global-error/withSentryConfig/tunnelRoute 版本门槛/Sentry.logger/metrics/Agent Tracing）**：https://docs.sentry.io/platforms/javascript/guides/nextjs/ [官方文档]

### 第十一轮新增（自托管部署）

- **Next.js Self-Hosting v16（反向代理/env 分界/NEXT_SERVER_ACTIONS_ENCRYPTION_KEY/deploymentId 版本倾斜/cacheHandler 五要求+refreshTags/X-Accel-Buffering/after 优雅停机）**：https://nextjs.org/docs/app/guides/self-hosting [官方文档]
- **standalone 输出（server.js/手动复制 public+static/Windows symlink/outputFileTracing 三件套/Turbopack nft 扩展）**：https://nextjs.org/docs/app/api-reference/config/next-config-js/output [官方文档]

### 第十二轮新增（Metadata/SEO 与静态资产）

- **generate-metadata（title template/default/absolute、metadataBase+URL 组合、streaming metadata+htmlLimitedBots、浅合并、Cache Components 交互、fetch 去重、file-based 优先、viewport/themeColor 迁移）**：https://nextjs.org/docs/app/api-reference/functions/generate-metadata [官方文档]（lastUpdated 2026-11-06）
- **next/image（fill+sizes、16 priority→preload、qualities 默认 [75]、remotePatterns 通配、SVG 三件套、blurDataURL 静态导入自动、getImageProps）**：https://nextjs.org/docs/app/api-reference/components/image [官方文档]（lastUpdated 2026-11-06）
- **next/font（构建时自托管 Google 字体、subsets 警告、字体定义文件、预加载范围随使用位置）**：https://nextjs.org/docs/app/api-reference/components/font [官方文档]（lastUpdated 2026-11-06）

### 第十三轮新增（动态段静态化与按路径失效）

- **generate-static-params（pages/layouts/route handlers 皆可/恒返回数组/dynamicParams 语义/Cache Components 至少 1 param/placeholder+notFound/ensureStatic='navigation' 约束/自底向上自顶向下/只能生成自身及上方段/ISR revalidation 不再调用/fetch 去重）**：https://nextjs.org/docs/app/api-reference/functions/generate-static-params [官方文档]（lastUpdated 2026-10-01）
- **revalidatePath（仅 SF/RH 可调/SF 立即 vs RH 标记下次/含动态段必传 type/'/'+'layout' 清 Client Cache/rewrites 传 destination/与 updateTag·revalidateTag 互补/≤1024 字符无尾斜杠）**：https://nextjs.org/docs/app/api-reference/functions/revalidatePath [官方文档]（lastUpdated 2026-06-25）

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| fetch 默认缓存 | 15 起默认 no-store，16 cacheComponents 全反转 | 按版本对照表回答 [NX-1] |
| middleware.ts 是当前方案 | 16 起 proxy.ts 取代 | 采用文档 |
| revalidateTag 单参数 | 16 起双参数 | 采用文档 |
| Server Action 可信（服务端函数不可被外部调用） | 实为公开 HTTP 端点 | [NX-6]/LAW-5 |
| `next/dynamic` + `ssr:false` 通用 | Server Components 中禁止 | 采用文档 |
| 慢导航仅是体验问题 | 16.3 Cache Components 下 dev 是 error（Instant Insights） | 采用文档：Stream/Cache/Block 三选 [场景：Instant Navigations] |
| 预取 = 每 link 一个 prefetch 请求（16.2 及以前） | 16.3 Partial Prefetching = 每 route 一个可复用 shell | 采用文档 |
| Cache Components 仅适合静态站 | 16.4 官方推荐所有应用（Next 17 默认） | 采用文档 |
| updateTag 双参 `(tag, profile)`（本 kb 此前误写） | **updateTag 单参数**（仅 Server Actions，立即过期）；双参是 revalidateTag | 已修正场景代码；速查表区分两 API |
| generateMetadata 慢查询必阻塞 shell（本 kb 此前结论） | 15.2+ streaming metadata：UI 先流式、metadata 追加 body；仅 htmlLimitedBots 等待 | 已修正「场景：Streaming」旧结论 [场景：Metadata/SEO] |
| image `priority` prop 现行 | 16 弃用 priority，改 `preload` | 采用文档：新代码统一 preload |
| themeColor/viewport 写进 metadata | 14+ 移入 `viewport`/`generateViewport` 导出 | 采用文档 |
| 返回空数组是「全运行时生成」的通用写法 | Cache Components 下动态路由空数组是 build error（至少 1 param） | 采用文档 [NX-15]：placeholder + notFound() 或占位策略 |
| revalidatePath 一次性失效所有使用该数据的页面 | 路径维度失效；同数据其他页面仍留缓存 | 采用文档：路径+tag 组合（revalidatePath + updateTag）保证一致 |
