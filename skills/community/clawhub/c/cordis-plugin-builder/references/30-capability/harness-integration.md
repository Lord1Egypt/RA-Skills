# 能力挂载：把插件能力真正挂进 DSH（实测契约）

> 前面的模板解决"插件结构"，本节解决"插件产出什么能力"——DSH 插件的价值最终体现在
> 模型可调用的工具、注入的提示词、注册的技能。契约来自运行时 inspect 实测（2026-08）。

## 能力挂载全景

```
                    ┌────────────── 插件产出什么能力 ──────────────┐
                    │                                             │
         ┌──────────▼──────────┐   ┌─────────────────────────────┐
         │ ① 模型工具 (Host)    │   │ ② 提示词 (Host)             │
         │ ctx.tools.register  │   │ ctx.systemPrompt            │
         │  defineTool(...)    │   │  .section / .variable / .tools│
         │  → 模型可调用        │   │  → 每次 step 前注入          │
         └──────────┬──────────┘   └──────────────┬──────────────┘
                    │                             │
         ┌──────────▼──────────┐   ┌──────────────▼──────────────┐
         │ ③ 技能 (Host)        │   │ ④ Client UI (浏览器)         │
         │ ctx.skills.register │   │ slots.register / styles      │
         │  → 会话目录可见      │   │ host.call ↔ harness.handle   │
         └────────────────────┘   └─────────────────────────────┘
```

**选择口诀**：模型要"调用"→ 工具；模型要"知道"→ 提示词/技能；用户要"看到/操作"→ Client UI。

## 1. 注册模型可调用工具（最常用，ctx.tools）

`ctx.tools` 是工具注册表 + 执行管线。插件用 `register(definition)` 注册，返回 disposer。

```ts
import { defineTool } from '@deepseek-ai/dsh-tools'

export function apply(ctx: Context) {
  // inject: ['tools']（硬依赖）或 ctx.get('tools') 探测后注册
  const dispose = ctx.tools.register(defineTool({
    name: 'my_tool',
    description: '一句话说清工具做什么（模型按此决定调用）',
    parameters: {
      // JSON Schema 风格：required 字段显式声明
      query: { type: 'string', required: true, description: '查询文本' },
      topK: { type: 'number', description: '数量上限（默认 5）' },
    },
    output: {
      schema: { type: 'object', additionalProperties: false, properties: { ... }, required: [...] },
      render: (_args, value) => [{ type: 'text', text: JSON.stringify(value, null, 2) }],
    },
    async execute(args) {
      // args 已被 defineTool 校验；返回 lossless JSON
      return { hits: [...] }
    },
  }))
  ctx.effect(() => dispose) // 注册必须挂 effect，卸载自动摘除
}
```

要点（实测）：
- `parameters` / `output.schema` 用 **JSON Schema 风格**（type/properties/required/additionalProperties），不是 schemastery。
- `output.render` 决定模型与 UI 看到的展示；`execute` 是业务结果——两者分离。
- `ctx.tools.register` 返回**精确 disposer**（取消注册），挂 `ctx.effect()` 托管。
- 重复注册同名工具、保留名 `run_code` 会失败；作用域内注册 shadow 全局。
- 可选依赖：`ctx.get('tools')` + undefined 检查；硬依赖：`inject: ['tools']`。

## 2. 注入提示词片段（ctx.systemPrompt）

`ctx.systemPrompt` 在每次模型 step 前组装提示词。插件可注册 section / variable / tools provider。

```ts
export function apply(ctx: Context) {
  // 注册一段提示词片段（可排序）
  ctx.effect(() => ctx.systemPrompt.section({
    name: 'my-plugin-guidance',
    order: 50,                 // 控制片段顺序（先注册先渲染，或用 order）
    content: '当用户问 X 时，优先使用 my_tool。',
  }))

  // 注册动态变量（每次组装时求值）
  ctx.effect(() => ctx.systemPrompt.variable('currentMode', (ctx) => 'creative'))
}
```

要点（实测）：
- `section()` / `variable()` 都返回**精确 disposer**，挂 `ctx.effect()`。
- 同层重复名称、非有限 order 抛错；作用域内 shadow 全局。
- `variable` 名字必须 `[a-z][a-z0-9_]*`；provider 返回 `undefined` 时引用该变量的 section 渲染失败。
- `systemPrompt.tools(provider)` 可注入工具 schema（高级场景）。

## 3. 注册技能（ctx.skills）：双通道架构

### 3.0 双通道架构（工具 + 技能配对）

```
完整插件 = 执行通道 + 指导通道
  ├─ 工具（ctx.tools）  → 模型调用："做什么"
  └─ 技能（ctx.skills） → 模型先读文档："怎么做"
```

> 工具给能力，技能给方法。dsh-memory 即此模式：18 个 `memory_*` 工具 +
> agent-memory 技能（SKILL.md + references 双通道）。模型按需加载技能文档（渐进披露），
> 配合工具执行——比"提示词常驻注入"省 token，比"静态 docs/ 目录"模型可读。

### 3.1 生产级注册（完整契约，动态读文件）

把本地 SKILL.md 注册为模型可见技能（详见 [traps.md](../90-experience/traps.md) #30；完整实现见 dsh-memory 的 skill-provider.ts）：

```ts
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

export async function apply(ctx: Context, config: { skillRoot?: string }) {
  const skills = ctx.get('skills')   // 可选依赖：缺失静默跳过（勿 inject）
  const skillRoot = config.skillRoot
  if (!skills || !skillRoot) return

  try {
    const content = await readFile(join(skillRoot, 'SKILL.md'), 'utf-8')
    await skills.register({
      name: 'agent-memory',                       // 技能名（目录名一致）
      description: '触发句式：当需要长期记忆时使用',  // 目录只暴露 name+description
      whenToUse: '需要记忆/跨会话上下文时；工具调用前先读指导',
      content,                                     // SKILL.md 全文（从文件动态读）
      source: 'custom',
      provider: 'dsh-memory',                      // 来源插件标识
      resourceBase: { kind: 'directory', path: skillRoot }, // references/ 可解析
      invocation: { modelInvocable: true, userInvocable: true },
    })
  } catch {
    // 技能注册失败静默降级：不拖垮插件主体
  }
}
```

要点（实测）：
- **动态读文件**：`content` 从 skillRoot 读 SKILL.md，插件可配置指向任意技能目录——比内联占位更生产。
- **完整字段**：`name/description/whenToUse/content/source/provider/resourceBase/invocation` 八个——`whenToUse` 给触发时机，`invocation` 控制模型/用户双开关。
- **降级策略**：`ctx.get('skills')` + try-catch——技能服务缺失或注册失败都不影响插件主体。
- **打包副本**：可选 `bundledSkillRoot()` 指向包内 `resources/agent-memory` 副本，离线可用（见 packaging.md 多语言内核的"资产随包分发"）。

## 4. Client 侧（浏览器 UI，静态插件）

Client 半区是另一段 JS 代码（`code.client`），与 Host 通过 JSON RPC 通信：

```ts
// Client：注册 UI 到 Slot（先 cordis_inspect_query Slots.listSubTree 查协议）
export function apply(ctx: Context) {
  const slots = ctx.get('slots')
  if (slots === undefined) return
  slots.inject('target.slot', () => slots.register(
    { name: 'target.slot', id: 'my-view' },
    (props) => React.createElement('div', null, String(props.someValue)),
  ))
}
```

- Client 侧**无 JSX/TS/import**：纯 JS + `React.createElement`；可用 Builtin：`ctx` / `React` / `host` / `styles` / `console`。
- Host↔Client 私有通信：Host `harness.handle('method', fn)` ↔ Client `host.call('method', args)`，仅 lossless JSON。
- `styles.insert(css)` 插入插件自有样式，随运行清理。
- **先查 Slot 协议再写注册**：`Slots.listSubTree` 无 root 看树，有 root 看完整契约（single/list/keyed/chain）。

## 5. 权限边界（构建者须知）

- 插件执行受当前会话 sandbox / approval 策略约束——工具注册不豁免权限。
- 声明式装配的插件，其权限 = 装配它的 profile/会话的权限；预设不能放松自身约束（否则破坏沙箱边界）。
- 凭据/密钥走环境变量或 `ctx.credentials`，不硬编码；外部输入先校验再使用。

## 6. 源码加载插件 + 动态插件桥接模式（Client UI 能力）

> 来源：DSH-Context-Pro 项目实测

源码加载插件（`file://` 路径）不能使用 `harness.handle()`（`harness` 是 `node:vm` 沙箱全局变量，只存在于动态 Cordis 插件沙箱中）。需要 Client UI 时，必须通过动态 Cordis 插件桥接。

### 标准桥接步骤

```
源码加载插件侧：ctx.provide('serviceName', serviceInstance)  → 暴露服务
         ↓
动态插件侧 Host 半区：ctx.get('serviceName') 消费 + harness.handle() 注册 RPC
         ↓
动态插件侧 Client 半区：host.call('methodName', args) 调取数据 + slots.inject() 注册 UI
```

### 完整示例

```ts
// ① 源码加载插件（持久）：暴露服务
export function apply(ctx: Context) {
  const engine = new InsightEngine()
  ctx.effect(() => ctx.provide('insightEngine', engine))  // ctx.provide 返回 disposer
}

// ② 动态插件 Host 半区：消费服务 + 注册 RPC
// ctx.get('insightEngine') 消费源码插件暴露的服务
// harness.handle('insight.get-topics', handler) 注册 RPC 供 Client 调用
harness.handle('insight.get-topics', async ({ sessionId }) => {
  const engine = ctx.get('insightEngine')
  return engine.getLatestTopics(sessionId)
})

// ③ 动态插件 Client 半区：调取数据 + 注册 UI
const topics = await host.call('insight.get-topics', { sessionId })
slots.inject('conversation.input.dock', () => slots.register(
  { name: 'conversation.input.dock', id: 'insight-topics' },
  (props) => React.createElement(TopicWidget, { topics, sessionId: props.sessionId }),
))
```

### 替代方案：`webServer.register()` HTTP 端点

桥接模式依赖动态插件（重启丢失）。需要**持久化 Client-Host 通信**时，改用 `webServer.register()` 注册 HTTP 端点（详见 [client-ui.md](client-ui.md) §3.5）：

```ts
// 源码加载插件直接注册 HTTP 端点，无需动态插件桥接
const webServer = ctx.get('webServer')
if (webServer) {
  ctx.effect(() => webServer.register({
    kind: 'exact',
    path: '/api/my-plugin/topics',
    handler(_req, res) {
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify(engine.getLatestTopics(sessionId)))
    },
  }))
}
```

### 选择依据

| 场景 | 推荐方案 |
|------|---------|
| 动态插件内部临时通信 | `harness.handle` + `host.call`（灵活，重启不保留） |
| 生产功能持久通信 | `webServer.register` HTTP 端点（重启不丢，代码在仓库） |
| 实验/热替换 | 动态插件（适合验证想法） |

## 7. 源码开发模式接入 harness（web-app bundle）

> 来源：DSH-Context-Pro 项目实测

本地方源码开发时，在 harness 的 web-app bundle 集成文件 `packages/bundle/web-app/cordis.patch.yml` 的 `insert:` 区块首位添加本地源码条目，即可让主 DSH 进程加载本地插件。

```yaml
- insert:
    - id: context-pro
      name: 'file:///E:/Deepseek/DSH-Context-Pro/src/index.ts'   # 源码入口
      config:
        chains:
          enabled: true
          injectProtocol: true
```

启动：`pnpm dsh --profile web` → 浏览器访问 http://127.0.0.1:3080 自动加载。

**关键约束（避坑复用）**：

| 约束 | 说明 | 来源 |
|------|------|------|
| Windows 路径必须三斜杠 | `file:///E:/...`，裸路径报 `ERR_UNSUPPORTED_ESM_URL_SCHEME` | traps.md |
| 新条目必须用 `insert:` 包裹 | 裸 `- id:` 是覆盖语义，非插入 | traps.md |
| 条目带稳定 `id` | 无 `id` 导致 HMR 全量重挂 | traps.md |
| 发布后 patch 的 `name` 用 npm 包名 | 非 `file:///`，见 packaging.md | packaging.md |

> 开发模式用 `file:///` 加载源码；发布模式改为 npm 包名（见 packaging.md 发布包机制）。两者是同一插件在不同生命周期的两种加载形态。

## 检查清单（能力挂载）

- [ ] 工具：`defineTool` 参数/输出 JSON Schema 齐全；`register` 返回挂 `ctx.effect()`；execute 返回 lossless JSON
- [ ] 提示词：section/variable 挂 effect；名字合法；无同层重复
- [ ] 技能：`ctx.get('skills')` 探测；content 为 SKILL.md 全文；resourceBase 指对
- [ ] Client：Slot 协议已查；React.createElement（无 JSX）；RPC 只传 JSON
- [ ] 权限：工具行为符合会话沙箱；无硬编码凭据
