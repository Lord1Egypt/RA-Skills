# Client UI 深度：Slot 协议 / 主题 / 样式（实测 2026-08）

> Slot 树来自运行时 `Slots.listSubTree` 实测。Client 侧**先查树、再选位、后注册**——协议
> （single/list/keyed/chain）决定怎么写注册，选错位会 shadow 出厂 UI。

## 1. Slot 选择脑图（实测树）

```
要放什么 UI？
│
├─ 完整设置页          → settings.section (list, id+order+label)  ← 首选整页
│   └─ 单条偏好(轻)    → settings.general.item (list)
├─ 侧栏脚部小动作      → sidebar.footer.action (list)   ← 不要替换整个 sidebar
├─ 全屏浮层(提示/Toast)→ shell.overlay (list)
├─ 会话头部按钮        → conversation.session.header.actions (list)
├─ 轮次尾部补充内容    → conversation.chat.turnTail (chain, select 选择器)
├─ 输入区小控件        → conversation.input.left / .right (list)
├─ 输入区独立一行      → conversation.input.dock (list)
├─ 工具调用卡片定制    → tool.call.toolview (keyed, key=工具名)  ← 会替换默认卡
├─ 动态插件 Run 卡内   → tool.view.cordis (keyed, key='self' 唯一)
└─ 整列/整会话替换     → sidebar / conversation / conversation.session (single) ⚠️高风险
```

**红线**：
- `single` 位是"一个座位"——占据即**替换出厂 UI**（replaceRisk: shadows-shipped-ui）。默认不碰 root/sidebar/conversation/details。
- `keyed` 位按 key 分发；`tool.call.toolview` 的 key 是工具名，注册已有工具名会替换默认卡片。
- `chain` 位用 `select(owner)` 选择器路由；`conversation.composer` 是 composer 接管链。

## 2. 注册协议速查

```ts
// list 位：id + 可选 order/label（最常用）
slots.inject('settings.section', () => slots.register(
  { name: 'settings.section', id: 'my-page', order: 10, label: '我的页' },
  (props) => React.createElement('div', null, 'page body'),
))

// keyed 位：key 决定显示在哪
slots.inject('tool.call.toolview', () => slots.register(
  { name: 'tool.call.toolview', key: 'my_tool' },
  (props) => React.createElement('div', null, 'my tool card'),
))

// chain 位：select 返回匹配值或 null（null = 不接管）
slots.inject('conversation.chat.turnTail', () => slots.register(
  { name: 'conversation.chat.turnTail', select: (owner) => owner.kind === 'user' ? {} : null },
  (props) => React.createElement('div', null, 'tail'),
))
```

## 3. 从 Host 取数据（host.call）

Client 不能直接碰 Host 服务，走 Package 私有 JSON RPC：

```ts
// Host 半区
harness.handle('get-stats', async (args) => ({ count: 42 }))

// Client 半区
const result = await host.call('get-stats', { scope: 'all' })
```

- 只传 lossless JSON；不传函数/类实例/Context。
- `host.call` 失败先查：Host 方法名、当前 pluginRunId、JSON 参数、handler 内真实服务依赖。

## 3.5. 替代方案：`webServer.register()` HTTP 端点（持久通信）

`host.call` 依赖动态插件 `harness.handle` 桥接，缺点是不持久（重启丢失）。需要**持久化 Client-Host 通信**时，改用 `webServer.register()` 注册 HTTP 端点：

```ts
// Host 侧（源码加载插件，`ctx.get('webServer')` 可选依赖）
const webServer = ctx.get('webServer')
if (webServer) {
  ctx.effect(() => webServer.register({
    kind: 'exact',
    path: '/api/my-plugin/stats',
    handler(_req, res) {
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' })
      res.end(JSON.stringify({ count: 42 }))
    },
  }))
}

// Client 侧（浏览器 fetch，同源无需 CORS）
const response = await fetch('/api/my-plugin/stats')
const data = await response.json()
```

### 适用场景

| 场景 | 推荐方案 |
|------|---------|
| 动态插件内部临时通信 | `harness.handle` + `host.call`（灵活，重启不保留） |
| 生产功能持久通信 | `webServer.register` HTTP 端点（重启不丢，代码在仓库） |
| 实验/热替换 | 动态插件（适合验证想法） |

### 要点

- `webServer` 是**可选服务**，`ctx.get('webServer')` 获取并判空（缺失静默降级）
- `WebRoute` 类型：`{ kind: 'exact' | 'prefix', path: string, handler: (req, res) => void }`
- 路径不能重复（`Registration of duplicate route` 抛异常）
- `register()` 返回 disposer，挂到 `ctx.effect()` 确保 fiber 清理
- Client 用 `fetch()` 同源访问（DSH web GUI 与 webServer 同 host:port），无需 CORS 配置
- `trustedHosts` 限制仅针对 WebSocket 升级路径，不影响 HTTP fetch

## 4. 主题与样式

```ts
// 插件自有样式：styles.insert 返回 disposer，随运行清理
const dispose = styles.insert(`.my-card { color: var(--dsh-text-primary); }`)
ctx.effect(() => dispose)

// 全局主题覆盖（谨慎）：先查 Theme.listTokens，再按 light/dark 提供值
const theme = ctx.get('theme')
if (theme) {
  ctx.effect(() => theme.override('--dsh-brand', { light: '#000', dark: '#fff' }))
}
```

- **不要**操作 `document.body` / `window` / 硬编码产品 DOM 选择器。
- 颜色优先用主题 CSS 变量，而非硬编码色值。

## 5. Client Builtin 清单（实测）

`ctx` / `React`（仅 createElement，无 JSX）/ `host` / `styles` / `console`。
无 `window`/`document`/`fetch`/`process`——需要浏览器能力先查 Client Builtin Provider。

## 6. 常见失败排查

| 症状 | 先查 |
|---|---|
| UI 不出现 | Slot 名/协议查过没？id/key 正确？slots 服务存在（ctx.get）？ |
| 出厂 UI 不见了 | 占了 single 位或 keyed 已占用 key——换 additive 位 |
| 页面报错 | `client-render` 诊断 + stack；错误属于某次 Run，定义新 Package 修复 |
| host.call 失败 | 方法名 / pluginRunId / JSON 参数 / handler 依赖 |

## 7. 实战沉淀

> 来源：DSH-Context-Pro 项目实测

### 7.1 Client 定时刷新模式

当 Client UI 需要随 Host 侧数据增量更新时：

```js
// ✅ 正确：定时轮询确保数据随 analyze() 增量更新
useEffect(() => {
  loadTopics()
  const dispose = timer.interval(loadTopics, 5000)
  return dispose
}, [])

// ❌ 空依赖：话题只加载一次，永不刷新
useEffect(() => { loadTopics() }, [])
```

### 7.2 会话级标志用 Map 替代全局变量

当需要跨会话隔离状态时，用 `Map<sessionId, T>` 替代 `let` 全局变量：

```js
// ❌ 全局标志：第一个会话设置后永久生效
let clientActive = false
markClientActive() { if (!clientActive) clientActive = true }

// ✅ 会话级 Map：每个会话独立
const clientActive = new Map<string, boolean>()
markClientActive(sessionId) { if (!clientActive.get(sessionId)) clientActive.set(sessionId, true) }
dispose(sessionId) { clientActive.delete(sessionId) }  // 会话销毁时清理
```

### 7.3 `markClientActive` 时机

- ❌ **在 `apply()` 里调用**：话题数据尚未就绪，便条通道已关闭，两条通道同时失效
- ✅ **在 topics 首次成功加载后调用**：数据就绪后才关闭便条通道，双通道协同

### 7.4 装载声明：`dsh.client.platform`（坑 #42）

Client bundle 的装载由新的 module-scanner 读取 `package.json` 两个字段；旧的 `dsh.bundle.client` 字段不再被扫描。

```json
// ✅ 正确：同时声明 platform 与 client 入口
{
  "dsh": { "client": { "platform": "web" } },
  "exports": { "./client": "./dist/client.js" }
}
```

**要点**：
- 平台声明用 `dsh.client.platform`，非 `dsh.bundle.client`（旧字段静默失效）。
- 入口路径经 `exports["./client"]` 声明，与声明面一致。
- 全注册面审计：枚举所有 `register/effect/on` 挂载点逐一对照声明面，避免同类问题扩散。

### 7.4 Slot 标准 props 的访问

`conversation.input.dock` 等 slot 注册回调接收 `(props)` 参数，其中 `props.sessionId` 是会话级标准 prop：

```js
// ❌ 不传 props，组件拿不到 sessionId
slots.register(..., () => React.createElement(Widget, { host, timer }))

// ✅ 透传 props.sessionId
slots.register(..., (props) => React.createElement(Widget, {
  host, timer, sessionId: props.sessionId
}))
```
