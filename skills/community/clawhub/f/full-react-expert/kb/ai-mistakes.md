---
type: cross-cutting
name: ai-mistakes
version: 7
updated: 2026-11-17
---
# AI 生成 React 全栈代码的典型错误总集

各 subdomain 自我质询轮的汇总。按领域分节，按危害排序。修复模式见对应 kb 文件；其中可升维为约束性条款的已提炼进 `kb/laws.md`（全局宪法）与各 subdomain kb「法则」小节。

## React（详见 kb/react-core.md）

1. **hooks 依赖随手 `[]`**——闭包里读了 state 仍给空数组，stale closure 静默 bug（最高频）
2. **派生计算写成 effect + setState**——应 render 时直接算
3. **`useEffect(async () => {...})`**——返回 Promise 被当 cleanup
4. **`key={index}`**——动态列表状态错位
5. **原地 mutation：`items.push(x); setItems(items)`**——Object.is 比较，不更新
6. **fetch 竞态不处理**——无 ignore 标志/AbortController
7. **编造 API**——幻觉 hooks、props、参数顺序
8. **版本混写**——React 17 项目写 18/19 API 或反之；class 与 hooks 混风格
9. **无差别 useCallback/useMemo**——Compiler 项目里是冗余噪音
10. **错误边界当万能兜底**——事件回调/异步错误它捕不到
11. **dnd-kit 双线混写**——新 `@dnd-kit/react`（ref API、`event.operation.target`）与旧 `@dnd-kit/core`+sortable（listeners spread、`event.over`）API 完全不兼容，先查项目用哪条线
12. **useActionState action 里未知错误也 return state**——已知校验错误 return（可携 FormData），未知错误必须 throw 落 Error Boundary；await 之后的 setState 须再包 startTransition
13. **Context provider 内联对象/函数 value**——每渲染全体 consumer 重渲染，memo 挡不住；useMemo/useCallback 稳定引用

## Next.js（详见 kb/nextjs.md）

1. **Pages Router / App Router 混写**——`getServerSideProps` 写进 App Router 项目
2. **缓存按旧版本语义答**——14/15/16 三次反转，不查版本就给方案（最高危）
3. **`'use client'` 位置错**——import 之后/函数上方（必须文件第一行）
4. **同步访问 params/searchParams/cookies()**——16 起强制 await
5. **Server Component 写 hooks**——useState 信手写进 RSC
6. **RSC 边界传函数 props**——序列化失败
7. **middleware.ts 时代错位**——16 应 proxy.ts
8. **revalidateTag 单参数调用**——16 起双参数
9. **Server Action 中 redirect 被 try/catch 吞**——NEXT_REDIRECT 误捕
10. **Server Action 无鉴权/无校验**——当可信内部函数（实为公开端点）
11. **AI SDK 7 旧 API**——system→instructions、onFinish→onEnd、fullStream→stream；v7 ESM-only + Node ≥22（四线 v4-v7 并存，先查版本）
12. **Cache Components 下 generateStaticParams 返回空数组**——build error；至少 1 param，未知值 placeholder + notFound()
13. **revalidatePath 含动态段忘传 type / rewrite 页面按浏览器地址失效**——动态段必传 `'page'|'layout'`；rewrites 传 destination（真实路由路径）

## NestJS（详见 kb/nestjs.md）

1. **DTO 写成 interface**——class-validator 静默失效（最高频、最隐蔽）
2. **Service 忘注册 providers**——can't resolve dependencies
3. **忘 `TypeOrmModule.forFeature([Entity])`**——Repository 注入失败
4. **interceptor 忘 `return next.handle()`**——响应 undefined
5. **`app.useGlobalPipes()` 用于需 DI 的全局组件**——应 APP_PIPE token provider
6. **forwardRef 只写一侧**
7. **忘 `@Injectable()`**
8. **微服务 `send()` 返回的 Observable 不订阅**——请求没发出
9. **imports 了模块但其 provider 未 exports**——依旧解析失败
10. **`@Get(':id')` 遮蔽 `@Get('me')`**——通配路由先声明把字面量路由吃掉
11. **`npm i prisma` 盲装**——默认拿到 8 RC 且不读 schema.prisma；v7 项目须锁 `^7`（`@prisma/client` 无 8.x）
12. **Drizzle 0.x/rc 线混写**——v1.0 过渡期：老 relations 写法/schemaFilter 默认全 schema/push 默认严格，先确认版本线（stable 0.45.4 vs `@rc` 1.0.0-rc.5）
13. **@nestjs/authentication / authorization 装进 Nest 11**——一等包仅 Nest 12 专属；且 AuthenticationModule 必须先于 AuthorizationModule
14. **cache-manager 内存缓存当副本修改 / miss 只判一种空值**——内存 store 存引用（改返回对象 = 污染缓存）；get miss 新版返 undefined、v6 返 null，两者都当 miss；Redis store 忘挂 'error' 监听器断连崩应用

## react-admin（详见 kb/react-admin.md）

1. **表格 API 双轨不分**——新代码应 `<DataTable>`（v5.8+ 推荐）；存量 `<Datagrid>` 合法但别混写（最高危）
2. **DataProvider 方法签名凭记忆写**——getList 参数结构/target 与 id 用反
3. **getList 忘返回 total**——分页崩
4. **自定义组件忘 `useRecordContext()` 判空**——白屏
5. **checkError/checkAuth 语义颠倒**
6. **authProvider 方法同步返回 boolean**——契约是 async + reject
7. **把 `@react-admin/ra-*` EE 组件（ra-rbac/ra-realtime/ra-navigation）当开源版用**——注意 CanAccess/useCanAccess 已核心化（开源可用）
8. **Field/Input 混用**
9. **source 点路径错 + label 忘传**——静默空白
10. **`optimized` Datagrid 里放动态 children**——静态约束破坏
11. **ReferenceInput 通用 props（validate/label/format/parse）写在本体上**——归内嵌子组件，传本体静默无效
12. **alwaysOn 过滤器配 defaultValue**——技术限制互斥，默认值走 `<List filterDefaultValues>`

## TanStack Query（详见 kb/tanstack-query.md）

1. **v4 位置参数语法**——v5 必须对象语法 `useQuery({ queryKey, queryFn })`
2. **queryFn 忘 throw**——HTTP 非 2xx 不报错，error 永远 null（最隐蔽）
3. **isLoading/isPending 混写**——v5 语义拆分
4. **gcTime 当 staleTime 调**——过期策略与回收策略混淆
5. **乐观更新漏 `cancelQueries`**——回滚被在途请求覆盖
6. **SSR 模块级单例 QueryClient**——跨请求/跨用户数据泄漏
7. **mutation 加 retry**——写操作自动重试 = 重复创建
8. **queryKey 塞不稳定引用/函数**——缓存永不命中
9. **enabled: false 忘写**——params 未就绪就请求
10. **RSC 里 useQuery**——Server 组件无 hooks
11. **tRPC 经典钩子 `trpc.x.useQuery()`**——已弃用（下大版本移除）；官方推荐 @trpc/tanstack-react-query 工厂 `trpc.x.queryOptions()`；手写 queryKey 失效过滤/预取永不匹配
12. **Apollo Client 4 按旧入口写**——React hooks 在 `@apollo/client/react`；hooks onCompleted/onError 已移除；ApolloError 已移除（`CombinedGraphQLErrors.is` 判型）；rxjs 新 peer
13. **Table v9 写 `useReactTable`**——v9 是 `useTable({ features, columns, data })` 按需注册特性（v8 时代结束）；状态底层 TanStack Store

## Vite（详见 kb/vite-tooling.md）

1. **版本盲写**——按 Vite 5/6 记忆生成（当前 8.3.8；v8 breaking 已锚定：Rolldown+Oxc 全链、`manualChunks` 对象形式→`codeSplitting`、`rollupOptions`→`rolldownOptions`、Oxc 不支持原生装饰器）
2. **环境变量忘 `VITE_` 前缀**——`import.meta.env.X` undefined
3. **密钥进 VITE_ 变量**——全打进客户端 bundle（安全）
4. **`server.proxy` 期望生产生效**——仅 dev
5. **vite.config 用 CJS**——ESM only
6. **`import.meta.glob` 默认 eager**——本想懒加载全量进主包
7. **manualChunks 按包名全量分组**——chunk 关系混乱
8. **React Compiler + SWC 硬凑**——需 Babel 模式
9. **忘 `vite/client` types**——`import.meta.env` TS 报错
10. **`base` 部署子目录忘配**——资产 404

## 测试（详见 kb/testing.md）

1. **Jest API 写进 Vitest**——`jest.*` 应 `vi.*`
2. **fireEvent 优先**——userEvent 才走真实事件链
3. **异步断言不 await**——假绿
4. **`waitForTimeout` 硬等待**——Playwright flaky 之源（web-first assertions 自动重试）
5. **getByTestId 当默认查询**——role/label 优先
6. **Nest TestingModule 忘 `.compile()`**——最高频 Nest 测试报错
7. **测实现细节**——断言内部 state/mock 调用次数（重构即碎）
8. **e2e 全程 mock**——白测
9. **测试间共享状态**——顺序依赖、并行污染
10. **snapshot 无脑更新**——`-u` 掩盖真实回归
11. **Vitest 5 升级雷区盲答**——`clearMocks` 默认 true（清掉 setup 记录）；非顶层 `vi.mock`/`vi.hoisted` 抛错；未 await 异步断言直接 fail；json/junit 默认写文件不打印 stdout
12. **Playwright 组件测试用 `@playwright/experimental-ct-*`**——包已移除停发；新模式 story gallery + `fixtures.mount()`
13. **Nest 全局守卫直接 overrideProvider**——APP_GUARD 用 useClass 注册时实例藏在 token 后不可达，须改 useExisting 注册
14. **overrideModule 对动态模块重复调工厂**——按引用匹配，静默无效（须传共享注册结果对象）

## Monorepo（详见 kb/monorepo.md）

1. **npm workspaces 字段与 pnpm-workspace.yaml 双轨混写**
2. **幽灵依赖暴露后 shamelessly-hoist 掩盖**——应补声明
3. **`workspace:^` 发布语义想当然**——`*`→精确、`^`→^
4. **turbo `dependsOn: ["build"]` 滥用**——多数场景要 `["^build"]`
5. **outputs 漏配**——缓存命中但 dist 空（`!.next/cache/**` 排除遗忘）
6. **dev 任务忘 `persistent: true`**——挂死
7. **缓存 env 漏声明**——环境变量变了旧缓存复用
8. **根 package.json 放运行时依赖**——子包隐式依赖
9. **发版忘 build / 私有包漏 `private: true`**
10. **lerna 肌肉记忆**——2026 主流 pnpm + turbo + changesets

## 共性模式（跨领域）

- **版本盲答**：八个子领域全部存在——React 19.3、Next 16.4.6、Nest 12、react-admin 5.15.7、TanStack Query 5.107.1、Vite 8.3.8、Vitest 5.1.0（Playwright/Turborepo 项目内 `npm ls` 确认）。**生态包同样存在**——TypeORM 1.x（0.3 时代结束）、Prisma 7/8RC、Drizzle 1.0 RC（stable 0.45.4 双线）、zod v4、graphql v17、Apollo Client 4（入口/错误类/hooks 三重断裂）、TanStack Table v9（useReactTable→useTable）、AI SDK 7、@nestjsx/crud 已弃维护。**生成代码前先确认版本**（package.json / npm ls）
- **契约方法同步化**：react-admin authProvider、Nest lifecycle、TanStack Query queryFn throw——凡框架要求 async + reject/throw 的地方，AI 爱写 return boolean / 静默返回
- **静默失效类**（无报错但功能失效）最危险：interface DTO、hooks 空依赖、queryFn 忘 throw、source 拼写、interceptor 忘 return、compile() 忘调、outputs 漏配——生成后必须自查这类（已升维为全局宪法 `kb/laws.md` LAW-14）
- **来源**：[模型经验]（全部来自自我质询轮，为 AI 代码生成的真实高频错误）

## 来源索引

- [模型经验]：本文件全部内容来自八领域自我质询轮的汇总——AI 生成代码的真实高频错误及其修复模式，与框架版本解耦（版本敏感条目已注明先查版本）
- 各条目详情与修复代码见对应 subdomain kb 文件（kb/react-core.md、kb/nextjs.md、kb/nestjs.md、kb/react-admin.md、kb/tanstack-query.md、kb/vite-tooling.md、kb/testing.md、kb/monorepo.md）

## 冲突消解记录

无文档对照（自我质询轮产物为模型内省，无文档来源可冲突）。

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| R43（第四十三轮） | 补账：新增 React 12（useActionState 未知错误）/ Next 12 关联 / Nest 14 关联 / RA 11（ReferenceInput props）——原轮漏横切对账，项目评审后补 | 2026-11-17 |
| R44（第四十四轮） | 补账：新增 React 13（Context 内联 value）/ Next 12-13（staticParams/revalidatePath）/ Nest 14（缓存引用与空值）/ RA 12（alwaysOn+defaultValue）——原轮漏横切对账，项目评审后补 | 2026-11-17 |
