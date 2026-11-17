<!--
本文件是**手工维护**的 curated 参考，不由 scripts/build_dsh_skill.sh 生成。
（生成器只产出 01~13 号文件；本文件已在脚本的 KEEP 白名单内，重跑不会被删。）
所有断言均对 DSH `dsh-v0.2.2-alpha.2` / commit `f3803c9697`（2026-10-28）逐条源码核验，
复现脚本：`scripts/verify_absorbed_claims.py <DSH 仓库路径>`。
-->

# 第 17 章 入站 HTTP 路由、定时器与客户端产物格式

> **本文件用途**：补三块原有 references 没覆盖的能力——① 在插件里**注册 HTTP 路由**（入站，被别人调用）；② **定时任务**的正确写法；③ **浏览器半侧产物**到底要打成什么格式。
> 这三块都是「写的时候必须查、写错了不报错或报得很晚」的类型。
> **写代码前先过第 0 步版本闸门**——本文件同样是快照。

---

## 17.1 `ctx.webServer`：宿主提供的浏览器 HTTP 载体

**它不是一个核心服务，而是一个插件提供的服务。** 源码 `packages/host/webserver/src/index.ts`，在 Web 组合里由补丁行认领：

```yaml
# packages/bundle/web-app/cordis.patch.yml:127-128
- id: webserver
  name: '@deepseek-ai/dsh-host-webserver'
```

官方定位（`docs/subsystems/web-server.zh.md:5`，逐字）：

> `dsh-host-webserver` 是 GUI Host 的浏览器 HTTP 载体：它是一个提供 `ctx.webServer` 的 `node:http` 插件……它不属于 agent loop，也不是能力 seam；它不了解任何 harness 概念。**其他插件负责注册所有功能路由**，包括 `/api` 桥接、插件 bundle 和 HMR 事件流。该服务器只服务浏览器：Electron 通过 `file://` 加载已构建文件，并经 IPC 桥接发送 fetch 请求，不使用本服务器。

### 🔴 第一个结论：`webServer` 只在 Web 组合里存在

| 事实 | 后果 |
|---|---|
| 提供者是一行**补丁行**（`id: webserver`），只在 `dsh-web-app` bundle 层 | 在 TUI / headless / 自建精简 profile 里 `ctx.webServer` **不存在** |
| 严格注入下 `inject = ['webServer']` 而提供者缺失 | 该插件**永久 PENDING**，启动时报 `<name>: pending (waiting for service: webServer)` |

**所以**：纯后端插件如果只是「顺带」想暴露一个接口，要么接受「仅 Web 组合可用」，要么用 `ctx.get('webServer')` 做可选分支，并在 README 里写明前置要求。

### 真实 API（逐字，`packages/host/webserver/src/index.ts`）

```ts
/** Route match kind: 'exact' matches the pathname verbatim; 'prefix' p matches p and p/<anything>. */
type WebRouteKind = 'exact' | 'prefix'

/** One named route registration. */
interface WebRoute {
  kind: WebRouteKind
  /** Absolute pathname, no trailing slash. */
  path: string
  /** Owns the full response lifecycle (may hold the response open, e.g. SSE). */
  handler: (req: IncomingMessage, res: ServerResponse) => void | Promise<void>
}

/**
 * `0.2.2-alpha.2` 新增的第二种路由形态：不自己写 handler，而是交出一个
 * Fetch 风格的 resource，由服务负责写回（内容编码 / 缓存 / 范围响应等统一处理）。
 * 判据：packages/host/webserver/src/index.ts:65（WebResource）、:68（WebResourceRoute）
 */
type WebResource = (request: Request, peer?: PeerScope) => Promise<Response>

interface WebResourceRoute {
  kind: WebRouteKind
  path: string
  /** Answers HTTP GET and HEAD requests and in-process reads. */
  resource: WebResource
}

// ctx.webServer（WebServer 服务）的方法：
register(route: WebRoute | WebResourceRoute): () => void  // 注册具名路由，返回 disposer；重复 (kind, path) 抛异常
registerUpgrade(route: WebUpgradeRoute): () => void  // HTTP upgrade 路由；同一 socket 只能有一个协议所有者
registerFallback(fallback: WebRoute['handler'] | Pick<WebResourceRoute, 'resource'>): () => void  // 认领回退席位；只有一个所有者，第二次注册抛异常
tapIndex(transform: (html: string) => string): () => void    // 原始 index.html 转换（逃生口）
applyIndexTaps(html: string): string
collectIndexInjections(): IndexInjection[]
renderIndex(html: string): string
readonly port: number                              // 监听端口（config.port 为 0 时是 OS 分配的）
```

**匹配顺序固定**：先查 `exact` 表 → 再取**最长匹配前缀** → 最后落到已注册的回退（发布的 Web 组合由 `dsh-host-frontend-static` 认领该席位，即 SPA dist 服务器）。

**handler 自己拥有整个响应**：`webServer` 不提供「返回 JSON 对象」的便捷 API，你要自己写 `res`。它内部只在符合条件时包一层 gzip，不影响你持有 `ServerResponse`。

### 可抄的最小路由

```ts
// {plugin-name} 宿主半侧
export const inject = ['webServer']          // ← 严格注入：用了就必须声明

export function apply(ctx) {
  ctx.effect(() => {
    // register() 返回 disposer；放在 effect 里则由 fiber 生命周期自动回收
    ctx.webServer.register({
      kind: 'prefix',
      path: '/{plugin-name}',
      handler: (req, res) => {
        const url = new URL(req.url ?? '/', 'http://localhost')
        if (url.pathname === '/{plugin-name}/health') {
          res.writeHead(200, { 'content-type': 'application/json' })
          res.end(JSON.stringify({ ok: true }))
          return
        }
        res.writeHead(404)
        res.end()
      },
    })
  })
}
```

要点：

- `path` 是 **绝对路径且不带尾斜杠**；`kind: 'prefix'` 表示同时匹配 `/p` 与 `/p/<任意>`。
- **自己加插件前缀**（`/{插件名}/...`）。路由是全局命名空间，撞车 = 配置错误（重复注册直接抛）。
- 抛异常不会杀进程：源码把处理中抛出的异常记为警告并应答 400（响应头已发出则销毁 socket），但这不意味着你可以不写 try/catch。
- 冒烟：`curl` 或浏览器打一次你注册的路径，看到 200 与预期响应体才算通。

---

## 17.2 定时任务：用 `ctx.interval` / `ctx.timeout`

来源 `vendor/timer/README.md`（逐字）：

> Timer handles are registered on the current fiber, so they are cleared automatically when the plugin that created them is disposed.

| API | 说明 |
|---|---|
| `ctx.timeout(callback, delay)` | 执行一次，**返回 disposer** |
| `ctx.timeout(delay)` | 返回 `delay` 后 resolve 的 Promise |
| `ctx.interval(callback, delay)` | 周期执行，**返回 disposer** |
| `ctx.interval(delay)` | 返回按时序 yield 的 async iterator |
| `ctx.throttle(callback, delay, noTrailing?)` | 返回带 `.dispose()` 的节流函数 |
| `ctx.debounce(callback, delay)` | 返回带 `.dispose()` 的防抖函数 |

> `ctx.setTimeout()` and `ctx.setInterval()` are kept as **deprecated aliases** for `ctx.timeout()` and `ctx.interval()`.

**三条硬知识**：

1. **用 `ctx.interval` / `ctx.timeout`，不要用 `setInterval` / `setTimeout` 别名**——后者是 deprecated。
2. **返回的是 disposer（函数），不是 Node 的 `Timeout` 对象**。所以 `clearInterval(timer)` 是错的类型；要主动停就 `timer()`，或者干脆不管——handle 绑在当前 fiber 上，插件卸载时自动清。
3. **它同样来自一个插件**：`@deepseek-ai/cordis-plugin-timer`，在 base 层有一行

   ```yaml
   # packages/bundle/base/cordis.patch.yml:16-17
   - id: timer
     name: '@deepseek-ai/cordis-plugin-timer'
   ```

   它已随 base 提供，但**缺了会永久 PENDING 且不报错**（本 skill `06-workflow.md` 坑 2 记过同一现象：HMR 依赖它）。

正确写法：

```ts
export function apply(ctx) {
  const timer = ctx.interval(() => {
    // 周期任务……
  }, 60_000)

  // 需要时可以主动停：
  // timer()
  // 不需要时什么都不用写 —— fiber 卸载时自动清
}
```

---

## 17.3 浏览器半侧的产物格式（lazy-CJS factory）

官方（`docs/cookbook/adding-a-settings-card.zh.md:60`）：

> 构建出的 `./client` 文件必须是客户端模块系统的 **lazy-CJS factory** 格式：一段脚本，向页面的模块加载器登记包名和一个 `factory(require)`。

同段还写明：生成它的 `clientBundle` tsdown 预设位于 `packages/client/tsdown.client.ts`，**而不在任何已发布的包里**，因此仓库之外的包要自己复刻这一步构建（本手册 `04` §9.6 已就此展开）。

**格式契约**（源码 `packages/client/tsdown.client.ts:930-936`，逐字）：

```js
banner: (chunk) => {
  const registration = `window.__ModuleLoader__.load({ id: ${JSON.stringify(id)}, ${chunk.isEntry ? '' : `chunk: ${JSON.stringify(chunk.fileName)}, `}factory: (require) => {`
  const prefix = clientBanner?.(chunk.fileName)
  return prefix === undefined ? registration : `${prefix}\n${registration}`
}
footer: 'return module.exports; } });'
intro:  'var module = { exports: {} }; var exports = module.exports;'
```

配套的构建设置：`format: 'cjs'`、`platform: 'browser'`、**默认**产物路径是 `lib/client.js`。

**入口合同没变，但 0.1.6-alpha.2 起多了「包内分块」这一层**（新增能力，旧版没有）：

| 项 | 值 | 源码出处 |
|---|---|---|
| 分块文件名 | 默认 `client.<name>.js`（入口默认 `client.js`） | `packages/client/tsdown.client.ts:917,920` |
| 分块的 banner | 对**非入口**分块多写一个 `chunk: "<fileName>",` 字段（入口 chunk 的 banner 与旧版逐字相同） | 同上 `:931` |
| 动态加载 | 包内动态 import 编译成 `require.async('./client.x.js')`，由 loader 按需拉取 | 同上 `:471`（`asyncChunkRequirePlugin`） |
| 分块名校验 | `/^client\.[A-Za-z0-9][A-Za-z0-9._-]*\.js$/`；不合法抛 `client-modules: invalid package-local chunk` | `packages/client/modules/src/client/system.ts:39,169` |
| 法务 / 署名 banner | `clientBundle(id, libEntry, { clientBanner: (fileName) => string \| undefined })` 按产物文件名注入前缀文本 | `packages/client/tsdown.client.ts`（`ClientBundleOptions.clientBanner`） |

> **对第三方作者的意思**：只发一个 `client.js` 的插件**不受影响**（入口 banner 未变）；但如果你复刻产物格式又想用代码分割，注册对象里必须补 `chunk` 字段，否则 `id` 会与入口撞名，抛 `duplicate factory registration`。

### 17.3.1 `0.2.1-alpha.3` 新增的两条产物通道：`dualClient` 与 `staticLinked`

事实基线 `dsh-v0.2.1-alpha.3` 起，`clientBundle` 的产出**不再只有一种命名**。两条新通道都是**可选**的，默认行为不变：

| 通道 | 触发方式 | 产物命名 | 源码出处 |
|---|---|---|---|
| 浏览器面（默认） | 不传 `dualClient`（`dualClient = false`） | 入口 `client.js`、分块 `client.<name>.js` | `packages/client/tsdown.client.ts:917,920`（三元式的 else 分支） |
| 浏览器面（双面模式） | `clientBundle(…, { dualClient: true })` | 入口 **`client.browser.js`**、分块 **`client.browser.<name>.js`** | 同上 `:917,920`（三元式的 then 分支） |
| **Node 面**（仅在双面模式下额外构建） | 同上；`clientFaces` 变成 `[nodeClientConfig(...), client]` 两个面 | 入口 **`client.node.js`**、分块 **`client.node.<name>.js`**；`conditionNames: ['node', 'import', 'module', 'default']` | 同上 `:145-152`（组装）与 `:756-771`（`nodeClientConfig`） |

选项类型是 **`readonly dualClient?: boolean`**（`:237`）。另有一条独立的 **`staticLinked(packageDir, libEntry): BuildFaceConfig`**（`:186`，内部走 `staticLinkedConfig`，`:303`），并导出 **`isStaticLinkedConfig()`**（`:204`，返回「至少有一个 config 由 `staticLinked` 构建」）。

> 🔴 **对第三方作者的意思**：① **默认仍叫 `client.js`**，只发单面 `client.js` 的插件**不用改**；② 但如果你的构建脚本、`files` 清单或发布校验**写死了 `client.js` 这个字面量**，而你在用（或被上游预设带着用）`dualClient`，产物会变成 `client.browser.js` + `client.node.js`，**旧的字面量会找不到文件**；③ 分块白名单校验 `/^client\.[A-Za-z0-9][A-Za-z0-9._-]*\.js$/` 仍然匹配 `client.browser.x.js` 与 `client.node.x.js`（点号在字符类里），所以**改名不会触发 `invalid package-local chunk`** —— 这类改名是**静默**的，只有发布校验/`files` 清单能抓住它。

注册侧契约（`packages/client/modules/src/client/system.ts`）：

- `window.__ModuleLoader__.load(registration)`，`registration = { id, chunk?, factory }`（`chunk` 仅包内非入口分块才带）；
- `factory(require)` 返回 `module.exports`；
- `id` **必须等于包名**；同一 bundle 执行两次会抛
  `client-modules: duplicate factory registration for "<id>" (bundle executed twice without invalidate?)`。

### 两条路：仓库内 vs 仓库外

| 场景 | 怎么做 |
|---|---|
| 在 DSH 仓库内加包 | 调共享 preset：`clientBundle('<包名>', ['lib/types/index.js'])`（3 行 `tsdown.config.ts`） |
| **在仓库外做第三方插件** | ⚠️ 官方明确说：**没有已发布的预设暴露该包，本仓库之外的包得自行复刻同样的输出格式**（同上文档第 102 行）。用 esbuild/rolldown 自己拼上面那三行 banner/intro/footer 即可 |

### 什么能 import，什么必须 external

`dsh.client` 可声明的字段：

| 字段 | 值 | 含义 |
|---|---|---|
| `platform` | `"web"` | **必填** |
| `inject` | 包名数组 | **信息性**依赖边（preflight 显示 / HMR diff），**不决定激活顺序** |
| `external` | 模块表 specifier 数组 | 该包额外请求的模块表行（子路径要精确写） |

**平台模块种子表**（`packages/client/web/src/platform.ts:8-14`，逐字 9 个）：

```
react                       react/jsx-runtime
react-dom                   react-dom/client
@deepseek-ai/cordis
@deepseek-ai/dsh-client-store
@deepseek-ai/dsh-client-ui-slots
@deepseek-ai/dsh-client-ui-primitives
@deepseek-ai/dsh-client-ui-dockkit
```

`PRELOADED_CLIENT_EXTERNALS` 当前为**空数组**。

规则（构建期有**纯度门禁**硬拦）：

- 上表 specifier + `dsh.client.external` 里请求的 → **保持 import（external）**；
- 其余 `@deepseek-ai/*` 的**值导入一律构建失败**，报 `client bundle purity: "..." is not in the default client externals ...`；跨插件协作走 Cordis 服务或插槽；
- `import type` 会被擦除，不进这道门禁——所以**跨包只允许 type-only import**；
- 其它非 `@deepseek-ai/*` 的依赖（zod、clsx 等）一律**内联**。

---

## 17.4 插槽注册的真实签名（顺带纠正一个高频混淆）

```ts
// packages/client/ui-renderer/src/client/registry.ts:172
inject(key: keyof SlotMap & string, callback: () => SlotInjectionEffect): () => void

// packages/client/ui-slots/src/index.ts:1207（实现签名）/ 1161,1188（两个重载）
register(options: ErasedOptions, component: unknown): () => void
```

两处容易搞错：

1. **组件是第二个参数**，不是放进 options：`ctx.slots.register({ name, id, order }, Component)`。
2. **`options.inject` 不是 Cordis 的 inject**。它是一个**业务面工厂**（`() => I`），返回值以 props 形式进组件；跟「声明依赖哪些服务」的 `inject = ['slots', ...]` 是两件事（后者仍然写在模块顶层）。

> 官方推荐的贡献姿势是包一层 `inject`：`ctx.slots.inject('<key>', () => ctx.slots.register({...}, Component))`——owner 尚未声明该 key 时它会等待，owner 折叠时自动回收。

---

## 17.5 反面教材：一套「看着很合理、实际全错」的写法

调研同类方案（`dsh-plugin-studio`）时收集到一组高频错误写法，**逐条对源码核验后确认全部不成立**，列在这里防止被二次引入：

| 错误写法 | 源码事实 |
|---|---|
| `ctx.webServer.register((router) => { router.get('/x', h) })` | **没有 router 对象**。`register(route: WebRoute \| WebResourceRoute)` 接收单个对象：`WebRoute` 是 `{kind, path, handler(req,res)}`；`WebResourceRoute` 是交出一个 `resource` 让服务写回（`0.2.2-alpha.2` 新增，`packages/host/webserver/src/index.ts:68`） |
| `ctx.command('hello <name>').alias().option().action()` | 命令注册是 `ctx.commands.register({...})`（`api-claims.md` M07） |
| `ctx.tool?.register?.({ params: {...} })` | 工具注册是 `ctx.tools.register(defineTool({...}))`（M06） |
| `ctx.slots.register({ name, component })` | 组件是**第二个参数**：`ctx.slots.register({ name, id, order }, Component)`（M08） |
| 插槽名 `'settings'` / `'status'` / `'workspace'` | 三个键在源码中**都不存在**（`settings` 只以 `settings.*` 形式存在）。向未声明 slot 注册会在激活时抛：`slot "<name>" is not declared (a parent entry's children table must declare it)`（`packages/client/ui-slots/src/index.ts:1210`） |
| `ctx.setInterval(cb, ms)` + `clearInterval(timer)` | 定时器是 `ctx.interval`（`setInterval` 仅为 deprecated 别名），返回 **disposer** 而非 `Timeout` |
| `ctx.ui?.request?.('/path')` | **没有 `ui` 这个服务**。浏览器侧做 HTTP 就用平台自带的 `fetch` |
| `inject = ['slots', 'sessions', 'workspaces', ...]`（client） | 这些服务名**确实存在**（如 `ui-workspace` 的 client inject），但「用不用得到」要按自己的代码定，不能照抄别人的清单 |

**通用教训**：同类方案里**结构值得借，代码必须逐条核验**——尤其当它自称「完整可运行配方」时。上面 8 条里有 6 条属于「不报错但永远不生效」型，比直接报错更难查。

---

## 17.6 本文件相关的核验命令

```bash
# 一次跑完全部断言（含正/负向自检，证明它真的能失败）
python <skill>/scripts/verify_absorbed_claims.py <DSH 仓库路径>

# 手工抽查任一事实
grep -n "register(route: WebRoute | WebResourceRoute)" <DSH>/docs/subsystems/web-server.zh.md
grep -n "id: webserver" -A 1 <DSH>/packages/bundle/web-app/cordis.patch.yml
grep -n "setTimeout.*deprecated aliases" -B 2 <DSH>/vendor/timer/README.md
grep -n "PLATFORM_MODULES" -A 7 <DSH>/packages/client/web/src/platform.ts
grep -n "banner:" -A 2 <DSH>/packages/client/tsdown.client.ts
grep -n "register(options: ErasedOptions" <DSH>/packages/client/ui-slots/src/index.ts
grep -n "inject(key: keyof SlotMap" <DSH>/packages/client/ui-renderer/src/client/registry.ts
grep -n "id: ui-layout" -A 1 <DSH>/packages/bundle/web-app/cordis.patch.yml
```
