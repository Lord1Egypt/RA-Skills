---
subdomain: testing
version: 12
updated: 2026-11-17
---
# 测试

## 定位与心智模型

React 全栈测试栈：**Vitest 5.1.0**（vitest.dev 锚定，Vite 原生、Jest 兼容、Oxc 驱动；**v5 硬门槛 Vite ≥6.4.0 + Node ≥22.12.0**）+ **Testing Library**（React 组件）+ **Vitest Browser Mode**（组件进真实浏览器，v5 正式场景）+ **Playwright 1.65.1**（E2E；**系统要求 Node 22.x/24.x/26.x、Windows 11+、macOS 14+**）+ `@nestjs/testing`（后端，**Nest 12 新项目默认 Vitest**）。分层心智模型：**单元（逻辑）→ 集成（组件/DI 模块）→ E2E（用户旅程）**，越往上越少越慢，只测关键路径。

两库共同哲学：**以用户方式查询**（role/label 优先，TestId 最后手段）、**测行为不测实现**（断言 DOM 输出与可观测效果，不断言内部 state/mock 调用次数）。

## 法则

[TE-1] **MUST**: Vitest 项目全量使用 `vi.*` 命名空间（vi.mock/vi.fn），不写 jest.*。
- 违反后果: `jest is not defined`。
- 溯源: [官方文档](https://vitest.dev)（Jest 兼容但命名空间独立）

[TE-2] **MUST**: 查询按用户视角优先级：getByRole > getByLabelText > getByText > getByTestId（最后手段）。
- 违反后果: TestId 满天飞，测试与可访问性脱钩、重构即碎。
- 溯源: [官方文档](https://testing-library.com)

[TE-3] **MUST**: 交互用 userEvent（真实事件链），fireEvent 仅兜底。
- 违反后果: fireEvent 单事件派发，测试通过但真实浏览器交互失败。
- 溯源: [模型经验]

[TE-4] **MUST**: 异步断言必须 await（waitFor/findBy）；Playwright 用 web-first assertions，NEVER 用 waitForTimeout 硬等待（全局宪法 LAW-13）。
- 违反后果: 假绿；CI 随机 flaky。
- 溯源: [官方文档](https://playwright.dev)

[TE-5] **MUST**: Nest TestingModule 必须 `.compile()` 后才 get；override 链在 compile 之前完成。
- 违反后果: 拿到未编译实例；override 静默无效。
- 溯源: [官方文档](https://docs.nestjs.com/fundamentals/testing)

[TE-6] **MUST**: 测行为不测实现——断言 DOM 输出与用户可感知结果，NEVER 断言内部 state/mock 调用次数。
- 违反后果: 重构即碎，测试成为重构阻力。
- 溯源: [官方文档](https://testing-library.com)

[TE-7] **MUST**: 测试间不得共享可变状态；每测试自造数据。
- 违反后果: 顺序依赖、并行污染、单独跑过全量跑挂。
- 溯源: [模型经验]

[TE-8] **MUST**: e2e 必须跑真实链路（真服务真库），NEVER 全程 mock。
- 违反后果: 白测——测的是 mock 不是系统。
- 溯源: [模型经验]

[TE-9] **MUST**: snapshot 变更必须逐个人工审查后更新，NEVER 无脑 `-u`。
- 违反后果: 掩盖真实回归。
- 溯源: [模型经验]

[TE-10] **MUST**: Playwright 失败排查先开 Trace Viewer（DOM 快照+网络+console），NEVER 只看截图。
- 违反后果: 定位低效，flaky 难复现。
- 溯源: [官方文档](https://playwright.dev)

[TE-11] **MUST**: Vitest 5 异步断言（`resolves`/`rejects`/`toMatchFileSnapshot`/`expect.poll`）必须完整 await 并处理其 Promise；vi.mock/vi.unmock/vi.hoisted 必须顶层调用。
- 违反后果: v5 起未 await 异步断言直接 fail 测试；非顶层 vi.mock 从警告升级为抛错。
- 溯源: [官方文档](https://vitest.dev/guide/migration)

[TE-12] **MUST**: Playwright 组件测试用 story gallery + 内建 `fixtures.mount()`；NEVER 安装 `@playwright/experimental-ct-*`（已移除停发）。
- 违反后果: experimental-ct-* 无法安装/升级，锁死 Playwright 1.62。
- 溯源: [官方文档](https://playwright.dev/docs/test-components)

[TE-13] **MUST**: 时间依赖测试用 `vi.useFakeTimers` + `advanceTimersByTime(+Async)` 显式驱动（`vi.waitFor`/`vi.waitUntil` 自动推进假定时器），NEVER 真等待。
- 违反后果: fake timers 下测试挂到超时（假时钟不自己走）。
- 溯源: [官方文档](https://vitest.dev/api/vi)

[TE-14] **MUST**: 组件渲染/交互更新须在 act 内（RTL render/userEvent 已自动包裹）；手写 ReactDOM 测试须设 `global.IS_REACT_ACT_ENVIRONMENT = true` 并 `await act(async () => ...)`（同步 act 将弃用）。
- 违反后果: "not wrapped in act(...)" 警告；"The current testing environment is not configured to support act(...)"。
- 溯源: [官方文档](https://react.dev/reference/react/act)

[TE-15] **MUST**: 多配置测试项目用 `test.projects`（旧 `workspace` 键已弃用）；项目名必须全仓唯一；coverage/reporters/resolveSnapshotPath/attachmentsDir 仅根级配置。
- 违反后果: 项目重名直接报错；项目级 coverage/reporters 配置静默无效（defineProject 类型报错）。
- 溯源: [官方文档](https://vitest.dev/guide/workspace)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| web-first assertions | Playwright 断言自动重试至超时（替代手写等待） |
| auto-wait | Playwright 操作前自动等元素可交互 |
| userEvent | RTL 生态模拟真实事件链（pointer/keyboard），比 fireEvent 真实 |
| TestingModule | Nest `Test.createTestingModule()` DI 测试容器 |
| storageState | Playwright 保存/复用登录态，免逐测试登录 |
| Trace Viewer | Playwright 失败回放（DOM 快照+网络+console 时间线） |
| Browser Mode | Vitest 在真实浏览器跑组件测试（CDP 真实事件），v5 正式能力 |
| story gallery | Playwright 组件测试新模式：dev server 渲染 story 页 + `mount()` fixture |
| fixture | Playwright 按需 setup/teardown 的测试环境单元（test/worker 两作用域） |
| projects | `test.projects` 多项目配置（内联/glob/配置文件三形态；旧 `workspace` 键弃用）[TE-15] |
| pool | 测试进程池：**forks（默认，child_process）**/threads（worker_threads）/vmThreads/childProcess |
| coverage provider | v8（默认：不预插桩、快、仅 V8 运行时）/ istanbul（任意运行时、预插桩、慢、内存高） |

## 最佳实践

### 场景：React 组件测试（RTL）

推荐路径：`render` → 用户视角查询（[TE-2]）→ userEvent 交互（[TE-3]）→ 断言 DOM 输出（[TE-6]）。

```tsx
// don't：TestId 当默认、fireEvent、断言 mock 调用次数
fireEvent.click(screen.getByTestId('submit-btn'));
expect(onSubmit).toHaveBeenCalledTimes(1);

// do：用户视角 + 真实事件链 + 行为断言
const user = userEvent.setup();
await user.click(screen.getByRole('button', { name: /submit/i }));
expect(await screen.findByText('Saved')).toBeInTheDocument();
```

边界条件：hooks 专用 `renderHook`；异步内容用 findBy（= getBy + waitFor），同步 getBy 断异步内容必假绿（[TE-4]）。

### 场景：模块 mock（Vitest）

推荐路径：`vi.mock('./api', () => ({ fetchX: vi.fn() }))`（[TE-1]）——factory 返回形状必须完整（缺导出在引用处报 undefined）；边界拦截用 `vi.spyOn`。

### 场景：mock 深水区（hoisting/部分 mock/环境桩）

推荐路径（[官方文档](https://vitest.dev/api/vi)，v5.1.0 锚定）：vi.mock **提升到文件顶部**——工厂不能引用外部变量（提升后闭包断裂，"Cannot access ... before initialization"）；共享值用 `vi.hoisted(() => ...)`；部分 mock 用 `importActual` 展开。

```ts
// do：vi.hoisted 共享 + importActual 部分 mock
const { mockFn } = vi.hoisted(() => ({ mockFn: vi.fn() }));
vi.mock('./api', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./api')>()),   // 保留其余导出
  fetchX: mockFn,
}));
// 环境桩：stubEnv 同时改 process.env 与 import.meta.env
vi.stubEnv('VITE_API_BASE', '/mock-api');
vi.stubGlobal('IntersectionObserver', MockObserver);
```

边界条件：不传工厂自动找 `__mocks__` 目录（相邻目录=源文件旁优先于根目录）；setup files 的 import 不被 mock；`{ spy: true }` 保留实现并把全部导出转 spy（Browser Mode ESM sealed 的正解，坑点 12）；运行时条件 mock 用 `vi.doMock`（不提升，只影响后续动态 import，配 `vi.resetModules`）；`vi.when(fn)`（v5+）按参行为级 mock——`vi.when(fn).calledWith(1).thenReturn(2)`，支持 thenResolve/thenThrow/times/onUnmatched/toHaveBeenExhausted，后定义先失效（LIFO）；`vi.stubEnv` **同时改 process.env 与 import.meta.env**；unstubEnvs/unstubGlobals 恢复。

### 场景：fake timers 与时间控制（[TE-13]）

推荐路径：`vi.useFakeTimers()` + 显式推进 `await vi.advanceTimersByTimeAsync(ms)`；断言等待用 `vi.waitFor`/`vi.waitUntil`（**自动推进假定时器**）。

```ts
vi.useFakeTimers();
user.type(input, 'ab');                      // debounce 500ms
await vi.advanceTimersByTimeAsync(500);      // [TE-13]
expect(await screen.findByText('Result')).toBeInTheDocument();
```

边界条件：基于 @sinonjs/fake-timers；**默认不 mock `process.nextTick`/`queueMicrotask`**（要 mock 须显式 `toFake`；`--pool=forks` 下 nextTick 完全不支持）；`runAllTimers` 遇无限 interval 10000 次循环上限后抛错（改 advanceToNextTimer/setSystemTime）；`setSystemTime` 控制 Date.now；`getTimerCount`/`setTimerTickMode` 辅助；v5 起 fake timers 亦 mock Temporal（版本注意）。

### 场景：act 与渲染边界（[TE-14]）

推荐路径：RTL 的 render/userEvent 已自动包 act——**手写 ReactDOM 测试**才需要：`global.IS_REACT_ACT_ENVIRONMENT = true` + `await act(async () => { ... })`（react.dev：同步 act 将弃用移除，一律 async 版）。

边界条件："not wrapped in act(...)" 警告 = 有更新发生在 act 之外——优先 findBy/waitFor 而非手包 act；缺 IS_REACT_ACT_ENVIRONMENT 报 "The current testing environment is not configured to support act(...)"（jsdom setup 置 true）。

### 场景：API mock（msw 3）

推荐路径：handler 级网络拦截——浏览器 `setupWorker`（`msw/browser`）/Node `setupServer`（`msw/node`）。**msw 3 入口分模块**：`http/HttpResponse` 从 `msw/http`、GraphQL 从 `msw/graphql`、WS 从 `msw/ws`、SSE 从 `msw/sse`；GraphQL 先 `graphql.link(url)` 再 `api.query()`（link-first）；工具函数（`delay`/`bypass`/`passthrough`/`isCommonAssetRequest`）从 `msw/utils/*`。未拦截告警用 `onUnhandledFrame`；Vite 项目用 `msw/vite` 插件（自动 serve worker 脚本 + `virtual:msw` 虚拟模块，免拷贝 mockServiceWorker.js）。

```ts
// do：msw 3 分模块入口 + link-first
import { http, HttpResponse } from 'msw/http';
import { graphql } from 'msw/graphql';

const api = graphql.link('https://api.example.com/graphql');
export const handlers = [
  http.get('https://api.example.com/users', () => HttpResponse.json(users)),
  api.query('GetUser', () => ({ data: { user } })),
];
```

边界条件：**Node.js ≥22 硬要求**；`worker.stop()` 返回 Promise 须 await，重复 start/stop 抛错（无隔离并行测试判 readyState）；WS 用 `msw/ws`（事件 `websocket:connection`）。

### 场景：Nest 单元/集成测试（[TE-5]）

推荐路径：TestingModule + mock provider；override 链（overrideProvider/overrideGuard/overrideInterceptor/overrideFilter/overridePipe）全部在 `.compile()` 之前；依赖多时用 `useMocker((token) => ...)` 批量 auto-mock（**REQUEST/INQUIRER 不能被 auto-mock**，须 overrideProvider 覆盖）。

```ts
const moduleRef = await Test.createTestingModule({
  providers: [UsersService, { provide: getRepositoryToken(User), useValue: mockRepo }],
}).compile();                              // [TE-5]
const service = moduleRef.get(UsersService);
```

边界条件：`get()` 只取静态实例，request/transient 作用域用 `resolve(token, contextId)`（**每次 resolve 返回各自 DI 子树实例，引用不相等**）；request-scoped 测试先 `vi.spyOn(ContextIdFactory, 'getByRequest').mockImplementation(() => contextId)` 固定上下文再 resolve；**全局注册 enhancer（APP_GUARD 等）默认不可 override**——注册须改为 `{ provide: APP_GUARD, useExisting: JwtAuthGuard }` + 同注册 JwtAuthGuard 为普通 provider，才能 `overrideProvider(JwtAuthGuard)`；`overrideModule` **按引用匹配**——动态模块须传入共享的注册结果对象，重新调用 `CatsModule.register(...)` 会静默无效；compile 后 `HttpAdapterHost#httpAdapter` 仍 undefined，需要适配器用 `createNestApplication()`。

### 场景：Nest e2e（supertest）

推荐路径：AppModule 全量装配 → `app.init()` → supertest 断言状态码与响应体。Fastify 项目 `createNestApplication<NestFastifyApplication>(new FastifyAdapter())` 后用 `app.inject({ method, url })` 免监听端口发请求（Nest 12 Node adapter 同有 `inject()`）。

```ts
beforeAll(async () => {
  const moduleRef = await Test.createTestingModule({ imports: [AppModule] }).compile();
  app = moduleRef.createNestApplication();
  await app.init();
});

it('POST /users', () =>
  request(app.getHttpServer()).post('/users').send({ name: 'a' }).expect(201));
```

### 场景：Playwright E2E

推荐路径：`playwright.config.ts`（projects + webServer 启动 dev server）→ setup project 登录存 `storageState`（免逐测试登录）→ 按用户目标拆测试 → web-first assertions（[TE-4]）→ 失败开 Trace Viewer（[TE-10]）。数据自造（直调 API），数据库隔离分层：testcontainers 真库 > sqlite 内存 > 全 mock（[TE-7]/[TE-8]）。

```ts
// don't：硬等待（flaky 之源 [TE-4]）
await page.waitForTimeout(3000);

// do：web-first assertions 自动重试
await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();
```

**Playwright best practices 增补**（[官方文档](https://playwright.dev/docs/best-practices)，2026-11-15 深度补强）：不测第三方依赖（`page.route` + `route.fulfill` mock 外部响应）；**CI trace 策略 = 首次重试失败才录**（不要 `on`——性能重）；CI 只装所需浏览器（`npx playwright install chromium --with-deps`）+ Linux 更便宜；ESLint `@typescript-eslint/no-floating-promises` 防漏 await；`expect.soft()` 不中断汇总失败；多断言同测用 soft，sharding `--shard=1/3` 提速。

### 场景：Vitest Browser Mode（组件进真实浏览器）

推荐路径（[官方文档](https://vitest.dev/guide/browser/)）：`browser: { enabled: true, provider, instances: [{ browser: 'chromium' }] }` → `page`/`userEvent` 从 `vitest/browser` 导入 → `expect.element()` 断言。供给器：`preview`（仅预览）/ **`playwright`（推荐，支持并行）** / `webdriverio`；v5 函数式 API `provider: playwright()`（`@vitest/browser-playwright` 导入）。

```ts
// do：vitest/browser 的 userEvent（CDP 真实事件）
import { userEvent } from 'vitest/browser';
const user = userEvent.setup();
await user.click(page.getByRole('button'));
```

边界条件：**Vitest 3.2 起无 browser 配置传 `--browser` 直接失败**；**勿用 @testing-library/user-event**（模拟事件，官方明示）；混合项目 `test.projects` 分 unit（node）/browser 双轨；**浏览器原生 ESM 命名空间 sealed——`vi.spyOn(module, 'x')` 抛错**，改 `vi.mock('./m.js', { spy: true })`；渲染器装 vitest-browser-react（内建 fork jest-dom 断言 `expect.element()`）。

### 场景：Playwright 组件测试（story gallery，[TE-12]）

推荐路径（[官方文档](https://playwright.dev/docs/test-components)）：`*.story.tsx` 每具名导出一个场景（story 持有状态/回调/Provider）→ gallery 页（自有 dev server 渲染，暴露 `window.mount/unmount`）→ `mount('components/Button/Primary', props)` 返回根 Locator → 用户视角断言。**状态记录模式**：story 把可观察结果写进 `<form hidden><input data-testid readOnly>`，测试断言 `toHaveValue('true')`（web-first 自动重试）——替代跨 Node/浏览器边界的回调 marshalling。

```tsx
// story：状态 + 隐藏表单记录可观察结果
export const Stateful = () => {
  const [expanded, setExpanded] = useState(false);
  return <>
    <Expandable expanded={expanded} setExpanded={setExpanded} />
    <form hidden><input data-testid='expanded' readOnly value={String(expanded)} /></form>
  </>;
};
// 测试
const component = await mount('components/Expandable/Stateful');
await component.getByRole('button').click();
await expect(component.getByTestId('expanded')).toHaveValue('true');
```

边界条件：配置 `baseURL` 指向 gallery + `serviceWorkers: 'block'`（防 SW 缓存遮蔽 page.route mock）+ `reuseContext: true` 提速；`component.update(newProps)` 不重挂载保留状态；story id 是字符串（重命名运行时才炸），用 `mount<typeof Story>` 换编译期 props 检查；网络 mock 在 `mount()` 前注册（mount 会导航）；脚手架 `npx playwright init-skills`。

### 场景：Storybook 10（组件工作台 + addon-vitest 组件测试）

推荐路径（[官方文档](https://storybook.js.org/docs)）：**当前线 storybook 10.6.7（@storybook/react 10.6.7，peer react ^16.8-^19；11.0-beta 在途）**。新装 `npm create storybook@latest`（自动识别 renderer/builder/meta-framework）；升级 `npx storybook@latest upgrade`（全仓库项目发现 + automigrations）；排障 `storybook doctor`。

- **v10 断裂面**（[迁移指南](https://storybook.js.org/docs/releases/migration-guide)）：**ESM-only 包分发**——`.storybook/main.js|ts` 与所有 preset 必须是合法 ESM；**Node ≥20.19 或 ≥22.12**；新面 CSF Next preview + tags 过滤改进；8.x 前须先升 9 再升 10
- **组件测试主线 addon-vitest**（[官方文档](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon/index)，取代 test-runner）：Vitest 插件把 stories 转成真实 Vitest 测试（portable stories），**无需运行 Storybook 实例**（test-runner 须实例 + Jest）；每 story 跑 smoke + play function 断言
- 硬要求：**Vite-based framework**（react-vite / **nextjs-vite**（Next ≥14.1 专用）/ sveltekit 等）+ **Vitest ≥3.0** + 默认 **Vitest browser mode（Playwright Chromium 真浏览器）**；MSW 若装须 ≥2.0
- 配置形态：Vitest 4+ 用 `test.projects`（story 项目 `extends: true` 继承根 Vite 配置）跑 `vitest --project=storybook`；插件选项 `storybookTest({ configDir, storybookScript, storybookUrl, tags: { include: ['test'], exclude, skip }, initialGlobals })`
- 边界条件：`tags.exclude` 优先于 include；单元测试 setupFiles 移进 unit project（防干扰 story）；CI 大并发 "Cannot connect to the iframe" → `isolate: false` 或 `--shard=1/3`；React 非 18 报 `m.createRoot is not a function` → alias `@storybook/react-dom-shim/dist/react-16`

### 场景：Playwright fixtures 扩展

推荐路径（[官方文档](https://playwright.dev/docs/test-fixtures)）：`test.extend<T>()` 自定义/覆盖内建 fixture；worker 级共享（服务/账号）用 `[fn, { scope: 'worker' }]`；全局 hooks 用 automatic fixture（`{ auto: true }`）；配置化选项用 option fixture（`['default', { option: true }]` + `defineConfig<MyOptions>`）。

```ts
// 覆盖内建 page fixture：自动导航 baseURL
export const test = base.extend({
  page: async ({ baseURL, page }, use) => {
    await page.goto(baseURL);
    await use(page);
  },
});
```

边界条件：**option 传数组必须额外包一层** `persons: [actualArray, { scope: 'test' }]`（直接传数组被当元组语法解析）；fixture setup/teardown 计入测试超时（慢 fixture 单独 `{ timeout: 60000 }`）；`resolve()` 取 request/transient 作用域实例；`mergeTests(a, b)` 合并多模块 fixtures；`{ box: true }` 报告降噪；`test.use({ opt: undefined })` 重置回 config 值。

### 场景：Agent 浏览器自动化（Playwright MCP / Agent CLI）

推荐路径（[官方文档](https://playwright.dev/mcp/introduction)）：**按 token 预算与场景选型**——**MCP server**（`npx @playwright/mcp@latest` 接入 MCP 客户端；**默认 headed**；工具 schema + snapshot 占上下文，token 成本高；适合专门 agentic loop、探索性自动化）；**Agent CLI**（`npm i -g @playwright/cli`；**默认 headless**；精简输出 + skills 按需加载 + **daemon 架构**（浏览器进程常驻，命令零启动开销）；适合大型代码库 coding agent）。两者都基于 **accessibility snapshot + 元素 ref**（如 `e5` 作为下次调用 target）——确定性交互，**无需视觉模型**；坐标级操作仅为可选项（MCP `--caps=vision`）。

```bash
# MCP：mcpServers 配置接入（VS Code/Cursor/Windsurf/Claude Code/Claude Desktop）
{ "mcpServers": { "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] } } }

# CLI：命令式驱动；snapshot 落盘 .playwright-cli/*.yml 不占上下文
playwright-cli open https://demo.playwright.dev/todomvc --headed
playwright-cli type "Buy groceries" && playwright-cli press Enter
playwright-cli screenshot
```

边界条件：MCP 工具面 70+，按 `--caps=network|storage|testing|devtools|pdf|vision|config` 能力旗标分组（Core 恒启用：navigate/snapshot/find/click/type/fill_form/route mock/storage_state/tracing/video 等）；MCP **持久会话**（登录态/cookie 默认跨会话保留）；CLI 多隔离会话 `-s=<name>`、全局 `--json`/`--raw` 机器可读输出；**@playwright/mcp 0.0.85 与 @playwright/cli 0.1.24 均 0.x pre-stable（API 可变）**，Node ≥18。

### 场景：Vitest 配置复用

推荐路径：复用 vite.config 加 `/// <reference types="vitest/config" />` + `test` 属性；独立 `vitest.config.ts` 优先级更高但**完全覆盖**（非合并）vite.config；跨配置复用 `mergeConfig(viteConfig, defineConfig({ test: {...} }))`。`process.env.VITEST` 与 `mode === 'test'` 条件分支 [官方文档](https://vitest.dev/config/)。

### 场景：测试项目划分（projects，[TE-15]）

推荐路径：`test.projects` 三形态——内联配置对象 / 配置文件路径 / glob（`'packages/*'` 每目录一项目，`!` 否定）；类型安全用 `defineProject`（项目级）/`defineConfig`（根级）；CLI 过滤 `vitest --project=unit --project='!e2e'`（多值、`*` 通配、`!` 排除）。

```ts
// vitest.config.ts（根）
export default defineConfig({
  test: {
    projects: [
      { test: { name: 'unit', environment: 'node' } },   // 内联（extends 默认 true 继承根）
      'packages/*',                                       // glob：每目录一项目
      'apps/web/vitest.config.e2e.ts',                   // 配置文件引用
    ],
  },
});
```

边界条件：**根配置默认不是项目**（只影响全局项——要跑必须显式列进 projects）；**项目名必须唯一**（重名报错；glob 项目默认取最近 package.json name 或目录名）；项目配置**不支持** coverage/reporters/resolveSnapshotPath/attachmentsDir（[TE-15]）；继承规则——内联项目 extends 默认 true（Vitest 5 起），setupFiles 等**数组拼接不覆盖**、tags 替换、name/projects 永不继承、根级 globalSetup 不继承；**glob/文件引用的项目不继承根配置**（须手动 `mergeConfig`）；嵌套项目仅配置文件可声明（名字自动带前缀，如 "app (unit)"）；排障 `DEBUG=vitest:projects vitest`。

### 场景：覆盖率（coverage）

推荐路径：provider 默认 **v8**（@vitest/coverage-v8；v3.2 起 AST remapping 精度与 istanbul 一致——不预插桩、快、低内存；**仅 V8 运行时**：Node/Chromium，Firefox/Bun/Cloudflare Workers 不支持）；任意运行时需求才用 istanbul（@vitest/coverage-istanbul）。

```ts
coverage: {
  provider: 'v8',
  include: ['src/**'],        // 未被测试 import 的文件默认不进报告——必须显式 include
  exclude: ['src/**/*.d.ts'],
}
```

边界条件：**默认只统计测试运行中被 import 过的文件**（未覆盖文件不进报告——门禁覆盖率虚高）；忽略注释须含 `-- @preserve` 关键词（TS 转译剥非 legal 注释，普通 `/* v8 ignore */` 被剥掉）；自定义 reporter（@vitest/istanbul-lib-report 接口）与自定义 provider（`provider: 'custom'` + customProviderModule）；**Agent 环境自动调整**（检测 AI coding agent：text reporter 自动 skipFull: true + 追加 text-summary——token 友好）。

### 场景：并行与过滤策略（pool/过滤）

推荐路径：两级并行——文件级默认并行（每文件隔离环境，pool 默认 **forks**；共享外部资源如 DB 时 `fileParallelism: false`）；文件内默认串行，需要时 `test.concurrent`/`sequence.concurrent: true`。过滤家族：文件名子串 → `-t` 正则（describe 与 test 名以 ' > ' 连接的全名）→ 行号 → tags。

```bash
vitest utils -t "handles empty input"    # 过滤务必带文件路径（-t 须逐文件发现匹配）
vitest foo.test.ts:10 foo.test.ts:25     # 行号：完整文件名+扩展名、空格分隔、不支持范围
vitest --project=unit --tags-filter=frontend
```

边界条件：**concurrent 不建额外 worker（同文件单线程）——只对含 await 的测试有收益**（maxConcurrency 上限，`{ concurrent: false }` 逐个退出；hooks 并发：beforeAll/afterAll 组内一次，beforeEach/afterEach 每测试可能重叠）；`.only` 调试完必须删——**CI（process.env.CI）下遇 .only 默认直接 fail 整跑**（allowOnly 控制；配 no-focused-tests ESLint 规则提前拦截）；`-t`/`--tags-filter`/`.only` 均逐文件发现匹配（大仓过滤慢——带上文件路径或 `--experimental.preParse` 免执行解析测试名）；`.skip`（报告可见）/.todo（无函数体占位）。

### 场景：Rstest（Rspack 驱动 Jest 兼容测试框架，Vitest 对位）

选型定位：**@rstest/core 0.12.6**（ByteDance，MIT；**仍 0.x**）——Rspack+Rsbuild 驱动测试编译（Rust/SWC），**Jest 与 Vitest API/CLI 双兼容**（describe/test/expect/snapshot/globals/projects/coverage + 官方迁移指南）；engines Node ^20.19||>=22.12（LTS 线内）；peer jsdom >=15 / happy-dom ^20.8.3 可选。适用：Rstack 系项目（Rsbuild/Rspack/Rslib/Lynx/Modern.js——**adapters 复用构建配置**：插件/别名/SWC 选项）或 Jest 存量迁移；Vite 系项目仍主选 Vitest。

- **Browser Mode**：Playwright 启真实浏览器（Chromium/Firefox/WebKit）——Canvas/WebGL 原生、CSS computed styles 真渲染、Web Workers 原生、跨浏览器；**Playwright-style Locator**：`page.getBy*` 语义查询 + **`expect.element(locator)` auto-waiting 断言**；官方决策树（需真实浏览器 API/跨浏览器/jsdom 意外行为→Browser Mode）且**官方推荐即使 jsdom 通过也用 Browser Mode**
- **E2E in the same runner**：browser/context/page/request Playwright fixtures——单测与 E2E 共享 runner/config/报告
- **配置兼容例外**（Browser Mode 下）：coverage v8 仅 headless 非 watch Chromium + Playwright provider 稳定（Firefox/WebKit 必须 istanbul）；`isolate: false` 时 headless worker 复用 context/page（worker fixtures 跨文件存活，headed 保持隔离）；pool.type/testEnvironment/detectAsyncLeaks/logHeapUsage **忽略**；bail 仅 headless 支持；`rs.mock` 模块 mock 同 Node 模式（`rs.mockRequire` 为 CJS interop，浏览器测试优先 `rs.mock`/`rs.doMock`）
- 坑：未处理 rejection 泄漏到 page → **整个测试文件失败**（即使全部 test 通过；expected rejection 须 await 或挂 handler）
- 来源：[官方文档](https://rstest.rs/) + [官方文档](https://rstest.rs/guide/browser-testing/)

### 场景：CI 裁剪

推荐路径：`turbo run test --filter=...[origin/main]` 只跑受影响包；与 monorepo 任务图集成（见 `kb/monorepo.md`）。

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | `jest is not defined` | Jest API 写进 Vitest | `vi.*` 命名空间 [TE-1] |
| 2 | 测试通过但真实浏览器交互失败 | fireEvent 只派发单事件 | userEvent [TE-3] |
| 3 | 断言在响应到达前执行（假绿） | 异步断言不 await | waitFor/findBy [TE-4] |
| 4 | CI 随机挂；慢机器永远不够 | `page.waitForTimeout(3000)` 硬等待 | web-first assertions [TE-4] |
| 5 | `module.get()` 拿到未编译实例报错 | 忘 `.compile()`；override 在 compile 后 | [TE-5] |
| 6 | Nest 12 ESM + Jest 报 `ERR_REQUIRE_ASYNC_MODULE` | Jest 加载 v12 ESM 需 Node 24.9+ | 新项目 Vitest（ESM） |
| 7 | 单独跑过、全量跑挂；顺序敏感 | 测试间共享状态 | 每测试自造数据 [TE-7] |
| 8 | 重构内部实现测试全红，行为没变 | 断言 mock 调用次数/内部 state | 测行为 [TE-6]/[TE-8] |
| 9 | msw 报 `Package subpath './http' is not exported` 或 Node 版本错 | 用了 msw 2 根入口；Node <22 | msw 3 分模块入口；Node ≥22 |
| 10 | v5 升级后 vi.mock 条件调用/嵌套函数内直接抛错 | 非顶层 vi.mock 从警告升级为抛错（hoist 语义） | 移到模块顶层；运行时条件 mock 用 vi.doMock [TE-11] |
| 11 | setup/beforeAll 记录的 mock 调用计数全为 0 | Vitest 5 `clearMocks` 默认 true，每测试前清历史 | 断言前重置计数或配置 `clearMocks: false` |
| 12 | Browser Mode `vi.spyOn(exportedModule, 'fn')` 抛错 | 浏览器原生 ESM 命名空间 sealed | `vi.mock('./m.js', { spy: true })` |
| 13 | `@playwright/experimental-ct-*` 装不上/锁死 1.62 | 包已移除停发，组件测试重写为 story gallery | fixtures.mount() 模式 [TE-12] |
| 14 | overrideModule 对动态模块静默无效 | 模块按引用匹配，重复调用工厂产生新对象 | 导出共享注册结果对象传入 [TE-5] |
| 15 | overrideProvider(JwtAuthGuard) 不生效（全局守卫照旧执行） | APP_GUARD 用 useClass 注册，实例藏在 token 后 | 注册改 useExisting + 同注册该类 [TE-5] |
| 16 | CI 管道拿不到 Vitest json/junit 输出 | v5 报告默认写文件（.vitest 目录），不打印 stdout | `['json', { stdout: true }]` |
| 17 | Playwright option 数组值设不上（被当元组解析） | `test.extend` 元组语法歧义 | `persons: [actualArray, { scope: 'test' }]` 额外包一层 |
| 18 | Storybook 10 升级后 main.ts 解析失败 | v10 ESM-only：`.storybook/main.js|ts` 与 preset 必须合法 ESM；Node <20.19 | main.ts 改 ESM（`import`/`export default`）+ Node ≥20.19/22.12 |
| 19 | addon-vitest CI 大并发报 "Cannot connect to the iframe" | 资源耗尽，逐文件隔离放大开销 | `isolate: false` 或 `vitest run --shard=1/3` |
| 20 | vi.mock 工厂引用外部变量报 "Cannot access ... before initialization" | hoist 提升后闭包断裂 | `vi.hoisted(() => ...)` 共享 [TE-11] |
| 21 | fake timers 下 userEvent/findBy 挂到超时 | 假时钟不自己走，忘显式推进 | `advanceTimersByTime(+Async)`；vi.waitFor 自动推进 [TE-13] |
| 22 | mock 了 setTimeout 但 process.nextTick 仍真实（或 forks pool 下 nextTick mock 失败） | 默认不 mock nextTick/queueMicrotask | `toFake` 显式加入 [TE-13] |
| 23 | "The current testing environment is not configured to support act(...)" | 手写 ReactDOM 测试缺 IS_REACT_ACT_ENVIRONMENT | setup 置 true 或改 RTL [TE-14] |
| 24 | "not wrapped in act(...)" 警告 | 更新发生在 act 之外 | 优先 findBy/waitFor；手写 `await act(async)` [TE-14] |
| 25 | projects 两项目重名报错 | 项目名必须全仓唯一 | 显式命名（glob 默认取 package.json name/目录名）[TE-15] |
| 26 | 项目配置里 coverage/reporters 不生效 | 这些键仅根级支持 | 移到根配置 [TE-15] |
| 27 | 覆盖率报告缺未测文件、百分比虚高 | 默认只统计被 import 过的文件 | coverage.include 显式纳入 |
| 28 | v8 覆盖率在 Firefox/Bun 不工作 | v8 provider 仅 V8 运行时 | 换 istanbul provider |
| 29 | 提交了 .only 后 CI 全红 | CI 下 .only 默认 fail 整跑（allowOnly） | 删 .only；no-focused-tests lint |
| 30 | -t/大仓过滤奇慢 | 过滤逐文件发现匹配 | 过滤带文件路径；--experimental.preParse |

**Top 展开：坑点 4（Playwright 硬等待，flaky 之源）**：`waitForTimeout` 拍脑袋定时长——快机器浪费、慢机器不够、CI 随机挂。Playwright 的 auto-wait + web-first assertions 就是为消灭它设计：操作前自动等元素可交互，断言自动重试至超时（[TE-4]/LAW-13）。

**Top 展开：坑点 10+11（Vitest 5 升级双雷）**：v5 把两类「曾经过得去」的写法变成硬失败——非顶层 `vi.mock`（hoist 语义强制，改抛错）与依赖旧行为的 mock 计数（`clearMocks` 默认 true，每测试前清历史）。升级前 grep 全仓 `vi.mock` 的条件/嵌套调用点，并审计「在 setup 阶段记录、在测试阶段断言调用次数」的用例。

## API 速查表

| API | 签名要点 | 易错点 |
|---|---|---|
| render / screen | `render(<X/>); screen.getByRole('button')` | getBy 多匹配抛错；getByRole 优先 [TE-2] |
| userEvent | `const user = userEvent.setup(); await user.click(x)` | 忘 setup/await [TE-3] |
| waitFor / findBy | 异步断言 | 同步 getBy 断言异步内容（假绿）[TE-4] |
| vi.mock | `vi.mock('./api', () => ({ fetchX: vi.fn() }))` | factory 返回形状不全；v5 必须顶层 [TE-11] |
| vi.doMock | 运行时条件 mock（不 hoist） | 顶层 vi.mock 的运行时替代 |
| vi.hoisted | 提升期共享值工厂 | vi.mock 工厂闭包引用外部变量的唯一正解 [坑点 20] |
| vi.importActual | 部分 mock 取真实模块 | 整模块替换丢副作用 |
| vi.useFakeTimers / advanceTimersByTime(+Async) | 假定时器 + 显式推进 | 默认不 mock nextTick/queueMicrotask（toFake 显式）[TE-13] |
| vi.stubEnv / vi.stubGlobal | 环境与全局桩 | stubEnv 同时改 process.env 与 import.meta.env |
| vi.waitFor / vi.waitUntil | 轮询断言（自动推进假定时器） | fake timers 场景首选 [TE-13] |
| vi.when | 按参行为级 mock（v5+）：calledWith/thenReturn/times | LIFO；toHaveBeenExhausted 校验 |
| renderHook | hooks 专用 render | — |
| page / userEvent（`vitest/browser`） | Browser Mode 真实事件 | 误用 @testing-library/user-event |
| expect.element | Browser Mode DOM 断言（内建 jest-dom fork） | — |
| Test.createTestingModule | Nest DI 测试容器 | 忘 compile；override 在 compile 后 [TE-5] |
| useMocker | 批量 auto-mock 依赖 | REQUEST/INQUIRER 不可 auto-mock |
| resolve(token, contextId) | request/transient 作用域实例 | 每次 resolve 子树实例不相等 |
| request(app.getHttpServer()) | supertest e2e | `await app.init()` 前置 |
| app.inject({ method, url }) | Fastify/Node adapter 免端口发请求 | 须 `createNestApplication<T>(new XxxAdapter())` |
| page.getByRole / getByLabel | Playwright 用户视角定位 | getByTestId 当默认（应最后手段）[TE-2] |
| expect(locator).toBeVisible() | web-first assertion | expect 同步值 + waitForTimeout 反模式 [TE-4] |
| storageState | `use: { storageState: 'auth.json' }` | 逐测试登录拖慢全组 |
| test.extend / mergeTests | 自定义/合并 fixtures | option 数组须额外包一层 [坑点 17] |
| mount / component.update | Playwright 组件测试 story gallery | story id 是字符串；route 在 mount 前注册 [TE-12] |
| setupWorker/setupServer | `msw/browser` / `msw/node` | 重复 start/stop 抛错；stop() 须 await |
| storybookTest（@storybook/addon-vitest） | Vite 插件：stories → Vitest 测试 | 仅 Vite framework；tags.exclude 优先；CI 大并发 isolate: false/--shard |
| graphql.link(url) | msw 3 GraphQL link-first | 根命名空间 graphql.query 已移除 |
| test.projects / defineProject | 内联/glob/配置文件三形态；`--project` 过滤（多值/*通配/!排除） | 项目名唯一；coverage/reporters 仅根级 [TE-15] |
| coverage | provider v8（默认）/istanbul；include/exclude | 未 import 文件默认不统计（include 显式）；ignore 注释须 -- @preserve |
| -t / 行号 / --tags-filter | 全名正则 / foo.test.ts:10 / 标签过滤 | 过滤带文件路径；行号须完整文件名、不支持范围 |
| test.concurrent / sequence.concurrent | 文件内并发（同线程） | 只对含 await 的测试有收益 |
| pool / fileParallelism | forks（默认）/threads/vmThreads/childProcess；maxWorkers 上限 | 共享外部资源场景 fileParallelism: false |

## 版本注意

- **Vitest 5.1.0**（vitest.dev 锚定，2026-11-15）：**v5 硬门槛 Vite ≥6.4.0 + Node ≥22.12.0**（vite 为 peer dependency，**Yarn 须显式装 vite**）；v5 breaking：**clearMocks 默认 true**；**非顶层 vi.mock/vi.unmock/vi.hoisted 抛错**；**未 await 的异步断言（resolves/rejects/toMatchFileSnapshot）直接 fail**；`expect.poll` 超时 reject（回调收 AbortSignal）；**移除 test.sequential/describe.sequential → `concurrent: false`**；**产物统一 `.vitest` 目录（一个 gitignore）**，**json/junit 报告默认写文件不打印 stdout**（管道消费加 `{ stdout: true }`）；VITEST_POOL_ID/VITEST_WORKER_ID 改 1-based；标题插值 pretty-format（`$` 值不再带引号）；fake timers mock Temporal；config 不再向上级目录查找（子目录跑须 `--config`）；内联 projects 默认 `extends: true` 继承根配置且默认共享 Vite server [官方文档](https://vitest.dev/guide/migration)
- **Vitest 5 Browser Mode**：provider preview/playwright/webdriverio；v5 函数式 `provider: playwright()`；--browser 无配置即失败（3.2 起）；CI 默认 headless；浏览器 Chrome ≥87/Firefox ≥79/Safari ≥15.4 [官方文档](https://vitest.dev/guide/browser/)
- **Vitest vi API 锚定**（[官方文档](https://vitest.dev/api/vi)，v5.1.0，2026-11-17）：vi.mock 提升/工厂闭包限制、vi.hoisted、`{ spy: true }`、__mocks__ 相邻优先、vi.doMock 不提升、vi.stubEnv 双环境（process.env + import.meta.env）、vi.stubGlobal、fake timers 默认集（不含 nextTick/queueMicrotask；10000 循环上限）、vi.waitFor/waitUntil 自动推进、**vi.when（5.0+）按参行为级 mock**
- **React act 锚定**（[官方文档](https://react.dev/reference/react/act)，2026-11-17）：推荐 `await act(async fn)`（同步版将弃用移除）；须 `IS_REACT_ACT_ENVIRONMENT` 全局；RTL render/userEvent 已自动包裹 [TE-14]
- **Playwright 1.65.1**（npm `@playwright/test` 锚定，2026-11-15；Chromium 159/Firefox 159；月更节奏，项目内 `npm ls @playwright/test` 确认）；`npx playwright install --with-deps` 装浏览器；**系统要求：Node latest 22.x/24.x/26.x（Node 20 已不支持）+ Windows 11+（或 WSL）+ macOS 14+ + Ubuntu 22.04/24.04/26.04（x86-64/arm64）**；**组件测试 `@playwright/experimental-ct-*` 已移除停发**（在用者锁 Playwright 1.62 再迁 story gallery）[官方文档](https://playwright.dev/docs/intro)
- Nest 12：新项目默认 **Vitest（ESM）**/ Jest（CJS）+ oxlint；Jest 加载 v12 ESM 需 Node 24.9+；Nest 12 Node adapter 测试须传 `new NodeAdapter()`（不传默认建 Express 应用，未装 @nestjs/platform-express 会失败）[官方文档](https://docs.nestjs.com/migration-guide)
- **生态版本锚定**（npm registry，2026-11-15，硬事实）：
  - **@testing-library/react 16.3.3**（peer React 18/19 + **@testing-library/dom ^10 硬 peer**——升级 RTL 16 时 dom 须同步 major，React 17 项目须留 RTL 旧线；Node ≥18）
  - **@testing-library/user-event 14.6.10**（peer @testing-library/dom ≥7.21.4，零运行时依赖）
  - **supertest 7.3.2**（superagent 10 驱动，Node ≥14.18）
  - **testcontainers 12.2.1**（**Node ≥22.22 门槛**，CI 镜像需核对；dockerode 5 驱动）
  - **msw 3.0.6**（2026-11-16 锚定；**v3 已 stable，v2 时代结束**；peer vite ≥6/graphql ≥16/TS ≥5.9；**Node ≥22 硬要求**；2.x→3.x codemod https://app.codemod.com/registry/@mswjs/v3）[官方文档](https://mswjs.io/docs/migrations/2.x-to-3.x)
- **Playwright Agent 工具链**（2026-11-16 锚定）：**@playwright/mcp 0.0.85**（MCP server；默认 headed；70+ 工具按 `--caps` 分组；持久会话；Node ≥18）[官方文档](https://playwright.dev/mcp/introduction)；**@playwright/cli 0.1.24**（`playwright-cli`；默认 headless；daemon 架构；snapshot 写 `.playwright-cli/*.yml`；Node ≥18）[官方文档](https://playwright.dev/agent-cli/introduction)——两者均 **0.x pre-stable（API 可变）**
- **Storybook 10.6.7**（storybook.js.org + npm registry 锚定，2026-11-16；**@storybook/react 10.6.7 同版**，peer react ^16.8-^19/TS ≥4.9；11.0-beta 在途）：**v10 = ESM-only 维护版**——main.ts/preset 须合法 ESM、Node ≥20.19/22.12、CSF Next preview；组件测试主线 **addon-vitest**（Vitest 插件 + portable stories，无需跑 Storybook 实例；要求 Vite framework + Vitest ≥3 + browser mode）取代 test-runner [官方文档](https://storybook.js.org/docs/releases/migration-guide)
- **Vitest projects/coverage/过滤/并行锚定**（v5.1.0，2026-11-17）：`test.projects` 三形态与继承规则（内联 extends 默认 true、数组拼接、根级 globalSetup 不继承、glob/文件引用不继承根配置、嵌套项目前缀名）+ 项目名唯一 + `--project` 过滤 + DEBUG=vitest:projects 排障 [官方文档](https://vitest.dev/guide/workspace)；coverage v8（默认，仅 V8 运行时）vs istanbul、include 纳入未覆盖文件、`-- @preserve` 忽略注释、自定义 reporter/provider、Agent 环境自动调整 [官方文档](https://vitest.dev/guide/coverage)；过滤家族（文件/-t 全名/行号/tags/.only CI 默认 fail/preParse；过滤须带文件路径）[官方文档](https://vitest.dev/guide/filtering)；两级并行（pool 默认 forks、maxWorkers、fileParallelism、concurrent 仅对 await 测试有收益、hooks 并发语义）[官方文档](https://vitest.dev/guide/parallelism)

## 与其他子领域的集成要点

- **NestJS**：TestingModule/supertest 模板；Nest 12 ESM 项目测试器选型（Vitest/Jest）→ 见 `kb/nestjs.md`
- **react-core**：测行为不测实现（[TE-6]）；错误边界只捕渲染期错误（测试别期望它兜事件回调异常）→ 见 `kb/react-core.md`
- **vite-tooling**：Vitest 复用 Vite 配置（同源 transform，插件共享）；**Vitest 5 硬门槛 Vite ≥6.4.0 + Node ≥22.12.0，vite 为 peer dependency（Yarn 须显式装）** → 见 `kb/vite-tooling.md`
- **monorepo**：测试放 turbo 任务图（`turbo run test`）+ CI `--filter=[origin/main]` 裁剪 → 见 `kb/monorepo.md`

## 来源索引

- Vitest 官网（Vite 原生/Jest 兼容/5.1.0 版本锚定）：https://vitest.dev [官方文档]
- Vitest Browser Mode 指南（provider 函数式 API/userEvent from vitest/browser/ESM sealed/混合 projects）：https://vitest.dev/guide/browser/ [官方文档]
- Vitest 5.0 迁移指南（clearMocks/vi.mock hoist/未 await 异步断言/.vitest 产物目录全清单）：https://vitest.dev/guide/migration [官方文档]
- Playwright 官网（auto-wait/web-first assertions/storageState/Trace Viewer/定位器哲学/系统要求）：https://playwright.dev [官方文档]
- npm @playwright/test（版本 1.65.1 锚定）：https://www.npmjs.com/package/@playwright/test [官方文档]
- Playwright Fixtures（worker-scoped/automatic/option fixture/mergeTests/box/执行顺序）：https://playwright.dev/docs/test-fixtures [官方文档]
- Playwright Component Testing（story gallery/状态记录模式/experimental-ct-* 移除迁移）：https://playwright.dev/docs/test-components [官方文档]
- NestJS 测试文档（useMocker/overrideModule 引用匹配/APP_GUARD useExisting/request-scoped contextId）：https://docs.nestjs.com/fundamentals/testing [官方文档]
- Testing Library（查询优先级哲学）：https://testing-library.com [官方文档]
- npm registry（@testing-library/react 16.3.3 / @testing-library/user-event 14.6.10 / supertest 7.3.2 / testcontainers 12.2.1 / msw 3.0.6 生态版本锚定）：https://registry.npmjs.org [官方文档]
- msw 2.x→3.x 迁移指南（分模块入口/link-first/onUnhandledFrame/msw/vite）：https://mswjs.io/docs/migrations/2.x-to-3.x [官方文档]
- Playwright Best Practices（trace 策略/mock 第三方/soft assertions）：https://playwright.dev/docs/best-practices [官方文档]
- Storybook 官方文档（10.6 线/CSF Next/addon 生态）：https://storybook.js.org/docs ；Storybook 10 迁移指南（ESM-only/main.ts ESM/Node 门槛/test-runner→addon-vitest）：https://storybook.js.org/docs/releases/migration-guide ；addon-vitest（portable stories 原理/插件选项/tags 过滤/CI 隔离与分片）：https://storybook.js.org/docs/writing-tests/integrations/vitest-addon/index [官方文档]
- Playwright MCP（snapshot/ref 交互/70+ 工具/caps 旗标/MCP vs CLI 对比/持久会话）：https://playwright.dev/mcp/introduction [官方文档]
- Playwright Agent CLI（token 高效/daemon 架构/skills/命令全集/多隔离会话）：https://playwright.dev/agent-cli/introduction [官方文档]
- Vitest 配置参考（vitest.config 覆盖语义/mergeConfig）：https://vitest.dev/config/ [官方文档]
- Vitest vi API 全参考（v5.1.0：mock 提升/hoisted/importActual/spy:true/__mocks__/doMock/stubEnv·stubGlobal/fake timers 默认集与上限/waitFor 自动推进/vi.when）：https://vitest.dev/api/vi [官方文档]
- React act 参考文档（await act(async) 推荐/同步 act 弃用计划/IS_REACT_ACT_ENVIRONMENT）：https://react.dev/reference/react/act [官方文档]
- Vitest Test Projects 指南（projects 三形态/继承规则/defineProject 类型安全/嵌套项目/--project 过滤/DEBUG 排障；旧 workspace 键 3.2 起弃用）：https://vitest.dev/guide/workspace [官方文档]
- Vitest Coverage 指南（v8 vs istanbul 对比/coverage.include 未覆盖文件/-- @preserve 忽略注释/自定义 reporter·provider/Agent 环境自动调整）：https://vitest.dev/guide/coverage [官方文档]
- Vitest Test Filtering 指南（文件/-t 全名正则/行号语法/tags/.only CI fail/preParse；注意 /guide/test-filtering 为 404，实际路径 /guide/filtering）：https://vitest.dev/guide/filtering [官方文档]
- Vitest Parallelism 指南（两级并行/forks 默认池/concurrent 仅 await 有收益/hooks 并发语义）：https://vitest.dev/guide/parallelism [官方文档]
- [模型经验]：坑点 2/3/5/7/8 的故障模式与修复、fireEvent/userEvent 差异、数据库隔离分层、e2e 骨架——适用全版本
- 法则条款来源：corpus/react/testing/elicited/05-laws.md（法则化萃取）
- [推断]：无

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| fireEvent 是 RTL 标准交互方式 | userEvent 走真实事件链，为推荐 | userEvent 为主，fireEvent 兜底 |
| Playwright 需手写等待（waitForSelector/waitForTimeout） | auto-wait + web-first assertions 自动重试 | 采用文档：禁 waitForTimeout 反模式 |
| getByTestId 是首选查询 | role/label 优先（两库一致哲学） | 采用文档：查询优先级 |
| Nest 测试默认 Jest | Nest 12 新项目默认 Vitest（ESM）/Jest（CJS） | 迁移指南锚定：按项目模块制选 |
| Playwright 组件测试用 `@playwright/experimental-ct-react`（JSX 内联 mount） | 包已移除停发；新模式 story gallery + `fixtures.mount()` | 采用文档：[TE-12] story gallery 模式 |
| Vitest `clearMocks` 默认 false、mock 可条件调用 | v5 默认 true；非顶层 vi.mock 抛错 | 采用文档：升级前专项审计（坑点 10/11） |
| 全局 APP_GUARD 注册后可 overrideProvider 直接替换 | useClass 注册的实例藏在 token 后不可达 | 采用文档：useExisting 注册模式（坑点 15） |
| Playwright 组件测试与 E2E 是两套运行时 | 同一 @playwright/test，mount 是内建 fixture | 采用文档：一套工具两种 fixture |
| Agent 浏览器自动化依赖视觉模型/截图猜坐标 | accessibility snapshot + 元素 ref 确定性交互（vision 坐标仅 --caps=vision 可选） | 采用文档：snapshot-based 为主 |
| 同步 act(...) 可用 | react.dev：推荐 `await act(async fn)`，同步版将弃用移除 | 采用文档 [TE-14] |
| fake timers 默认接管全部异步原语 | 默认不 mock process.nextTick/queueMicrotask（toFake 显式；forks pool 下 nextTick 不支持） | 采用文档 [TE-13] |
| vi.stubEnv 只改 process.env | 同时改 process.env 与 import.meta.env | 采用文档 |
| vi.spyOn 可直接 spy ES 模块导出 | Node 环境 vi.spyOn 对导出对象可行，但浏览器原生 ESM 命名空间 sealed 抛错 | 分环境：Browser Mode 用 `vi.mock(..., { spy: true })`（坑点 12） |
| 多项目配置用 `test.workspace`（workspace 文件） | 3.2 起 workspace 键弃用 → `test.projects`（同功能） | 采用文档 [TE-15] |
| Vitest 默认 pool 为 threads | 默认 **forks**（child_process） | 采用文档 |
| .only 在 CI 只是静默跳过其余测试 | CI（process.env.CI）下 .only 默认 **fail 整跑**（allowOnly 控制） | 采用文档：调试完必删（坑点 29） |
| 覆盖率默认统计全量源文件 | 默认只统计被测试 import 过的文件——未测文件须 coverage.include | 采用文档（坑点 27） |
