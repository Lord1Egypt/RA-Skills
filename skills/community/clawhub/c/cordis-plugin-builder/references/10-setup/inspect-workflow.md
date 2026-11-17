# cordis_inspect_* 实时查询方法论（文档是地图，Inspect 是真相源）

> 本技能最重要的开发纪律：**技能文档（SKILL.md + references）是静态地图**——告诉你"有什么概念、
> 往哪走"；`cordis_inspect_*` 是**实时 GPS**——每次写代码前问一遍当前运行时，拿到此刻真实存在的
> 契约。DSH 版本会演进，文档会滞后，**Inspect 永远为真**。

## 1. 核心思想脑图

```
技能文档（静态地图）                cordis_inspect_*（实时 GPS）
   "有什么概念、往哪走"                   "此刻路口长什么样"
        │                                    │
        │ 概念/方法/入口                      │ 精确签名/参数/模式/类型
        ▼                                    ▼
   ┌──────────────────────────────────────────────────┐
   │  写代码前：先查 Inspect 确认契约 → 再动手          │
   │  不猜 API · 不凭文档印象 · 不缓存业务数据          │
   └──────────────────────────────────────────────────┘
```

## 2. 三件工具的分工

| 工具 | 作用 | 类比 |
|---|---|---|
| `cordis_inspect_list` | 列出当前所有 Provider 及方法清单 | "看有哪些柜台" |
| `cordis_inspect_query` | 查询某个 Provider 的**精确契约**（签名/参数/返回/模式）| "要具体服务条款" |
| `cordis_inspect_self` | 查看**当前会话**的动态插件（源码/版本指针/诊断）| "查我自己的档案" |

- `inspect_list` / `inspect_query`：Host 侧（Service/Event/Builtin/Tool）与 Client 侧（Service/Event/Builtin/Slots/Theme）。
- `inspect_self`：当前会话动态插件专属（无参 = 插件摘要；pluginId = 版本指针；pluginId+packageId = 源码+诊断）。

## 3. 标准查询流程（4 步，写代码前执行）

```
① cordis_inspect_list ──► 拿到 Provider 目录（Service/Event/Builtin/Slot/Theme/Tool）
        │
② 无 input 查询 ────────► 紧凑目录（服务清单 / 事件清单 / Slot 树）
        │                 Service.listService / Event.listEvents / Slots.listSubTree
        │
③ 带 input 精确查询 ────► 完整契约（参数/返回/模式/访问规则/类型）
        │                 {service:"tools"} / {event:"tools/pre-execute"} / {root:"settings.section"}
        │
④ 对照契约写代码 ───────► 不猜 API，不凭文档印象
```

**Provider 名/方法名/input schema 一律来自 list 结果**——不硬编码、不跳步。

## 4. 典型实例

### 例 1：注册模型工具前

```text
① cordis_inspect_list                      # 发现 host Service Provider
② cordis_inspect_query(host/Service, listService)
                                           # 目录：tools → register(definition) / execute / guard...
③ cordis_inspect_query(host/Service, listService, {service:"tools"})
                                           # 精确契约：register 返回 disposer、保留名 run_code、
                                           # 作用域注册 shadow 全局、可选/硬依赖访问方式
④ 写 ctx.tools.register(defineTool({...}))
```

### 例 2：监听事件前

```text
① list 找 Event Provider
② listEvents 无 input → 目录（agent/status、tools/pre-execute…带模式 emit/waterfall）
③ listEvents {event:"tools/pre-execute"} → 精确 payload 类型 + waterfall 监听器签名
④ 写 ctx.on('tools/pre-execute', (exec, next) => ...)
```

### 例 3：Client UI 注册前

```text
① Slots.listSubTree 无 root → 紧凑树（root → sidebar/conversation/details → ...）
② 选 additive 位（settings.section / sidebar.footer.action 等，replaceRisk:none）
③ Slots.listSubTree {root:"settings.section"} → 完整注册协议（id/order/label）与占用者
④ 写 slots.register({ name:'settings.section', id:'my-page', ... }, ...)
```

### 例 4：动态插件排障

```text
cordis_run 失败
   │
   ▼
cordis_inspect_self(pluginId, packageId)   # 读失败版本源码 + 精确诊断/stack
   │
   ▼
涉及未知能力？ ──是──► 重新 list/query Provider
   │否
   ▼
同 Plugin 追加新 Package → cordis_run 修复
```

## 5. 关键纪律（避免踩坑）

1. **先用 list，再 query，不跳步**——Provider 名/方法名/input schema 都从 list 结果来，不能猜。
2. **目录 ≠ 业务数据**——Inspect 结果只用来确认契约，不能缓存成"业务数据"反复用；每次写新代码前重查。
3. **运行时为准**——技能文档说"有 5 种事件模式"是真的，但**具体事件名/payload** 以 `listEvents` 实时结果为准。
4. **Client 查询可能等待**——查 Client 侧（Slots/Theme）要等页面响应，可能 pending。
5. **inspect_self 用于排障**——插件加载失败时读源码+报错，是动态插件修复流程第 ① 步（见 [dynamic-plugins.md](../30-capability/dynamic-plugins.md) 第 6 节流程图）。
6. **不把 Inspect 当业务 API**——Inspect Provider 是只读契约目录；真正的业务调用走运行时 Service（`ctx.xxx`）。

## 6. 与技能文档的配合

| 场景 | 用文档 | 用 Inspect |
|---|---|---|
| 建立概念地图 / 学习流程 | ✅ SKILL.md / references | — |
| 写具体代码前确认 API | — | ✅ list → query |
| 事件/服务/Slot 精确契约 | 目录（events-catalog）| ✅ 精确 payload/签名 |
| 插件加载失败排障 | 坑库（traps）| ✅ inspect_self 读诊断 |
| 版本演进后 API 变更 | 可能滞后 | ✅ 永远为真 |

## 7. 实战沉淀

> 来源：DSH-Context-Pro 项目实测

### 7.1 事件契约先查再写（不猜 API）

在写任何事件监听器之前，先用 `cordis_inspect_query` 查询事件的精确 payload 类型和模式：

```text
cordis_inspect_query(Event/listEvents, {event:"agent/pre-step"}) → 精确 payload/模式
```

实测结果：`agent/pre-step` 是 waterfall 模式，payload 含 `{agent, messages, turn, step, signal}`，监听器返回 `PreStepDecision`。类型定义在 `@deepseek-ai/dsh-agent` 的 runtime-types。

### 7.2 waterfall `next(新值)` 传参被静默忽略

- **现象**：监听器写 `next(新值)`，但下游收到的是原始 args，新值丢失。
- **根因**：`next` 闭包捕获分发时的 args 数组，你传给 `next()` 的参数不参与 `cb(...args)`。
- **规避**：`const result = next()` 取下游返回值，包装后 `return`。

```ts
// ✅ 正确：取下游返回值再包装
ctx.on('agent/pre-step', async (payload, next) => {
  const decision = await next()
  return { ...decision, messages: injectContext(decision.messages) } as PreStepDecision
})

// ❌ 错误：next(新值) 被静默忽略
ctx.on('agent/pre-step', async (payload, next) => next({ ...decision, messages: [...] }))
```
