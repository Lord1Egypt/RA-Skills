> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：工具插件（defineTool 与裸 register 两条路径）、可配置插件（Config 与 Schema DSL）、斜杠命令、事件五种分发模式与 waterfall 拦截、服务插件、终端家族。写具体功能时按需查。
> **合成来源**：DSH插件开发指导手册.md（第 4~8 章）
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

> **本文件导航 —— 共 1,101 行，不要整读。** 先 `grep` 定位小节，再只读需要的那一节。
> - **本文件全是整理稿**（无上游素材混杂），但它仍是基线快照——写代码前先过版本闸门。
> - 常用检索：`grep -n '^## '`（API 面分类）、`grep -n 'ctx\.'`（按 API 名查）

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 580-1653 -->

# 第 4 章 第二课｜工具插件：让 AI 模型会调用你的能力

> **本课目标**：注册一个「工具」，让模型能主动调用它。
> **这是 DSH 插件开发里最常用、最有价值的一类。** 90% 的实用插件都是工具插件。

## 4.1 先分清：谁在调用你的东西

| | 工具（Tool） | 命令（Command，第 6 章讲） |
|---|---|---|
| **调用方** | **模型** | **人**（敲 `/xxx`） |
| 进不进模型上下文 | 进（schema 自动流入系统提示词） | 不进 |
| 注册 API | `ctx.tools.register(defineTool({...}))` | `ctx.commands.register({...})` |
| 用途 | 读文件、跑命令、搜索、查数据库 | 切模式、压缩历史、退出 |

来源：`packages/interaction/commands/README.zh.md:12`、`docs/cookbook/extension-cookbook.zh.md:119`

## 4.2 最小工具（逐字照抄）

来源：`docs/user/develop/basic/tool.zh.md:11-33`

```ts
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',
    parameters: {
      name: { type: 'string', required: true, description: 'The name to greet' },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      return `Hello, ${args.name}!`
    },
  }))
}
```

官方对此段的解释（`tool.zh.md:36`，逐字）：

> `inject` 让 Cordis 等待工具注册表就绪。`defineTool` 根据 `parameters` 推导并校验 `args`；`execute` 返回 `output.schema` 声明的规范值，`output.render` 再将该值转换为面向模型的内容。

**三个必知要点**：

1. `export const inject = ['tools']` —— 没写这行，`ctx.tools` 就是 undefined，插件直接报错。
2. 工具名 `name: 'greet'` **必须唯一**；`run_code` 是保留名，不能用（`docs/subsystems/tools.zh.md:645`；⚠️ 原引 `:633` 在**旧树里就已偏 15 行**，属历史笔误，非本区间漂移）。
3. `ctx.tools.register(...)` 是**副作用**：插件卸载时工具自动注销，你不需要手动清。

## 4.3 `defineTool` 的完整字段

`defineTool` 的选项结构（源码权威定义：`packages/core/tools/src/schema.ts:483-537`）：

```ts
export interface DefineToolOptions<S extends ParameterSchemaSpec, O extends ValueSchemaSpec> {
  /** Tool name (must be unique). */
  readonly name: string
  /** Human-readable description sent to the model. */
  readonly description: string
  /** Per-property parameter schema compiled to an implicit open object root. */
  readonly parameters: S
  /** Canonical output schema plus pure Native and presentation projections. */
  readonly output: {
    /** Schema enforced against every successful body or policy-replaced value. */
    readonly schema: O
    /** Pure Native/model rendering of one validated canonical value. */
    render(args: InferArgs<S>, value: InferValue<NoInfer<O>>): ContentBlock[]
    /** Pure replayable presentation metadata for native and nested calls. */
    presentationMeta?(args: InferArgs<S>, value: InferValue<NoInfer<O>>): JsonValue
  }
  /** Optional positive cooperative timeout budget in milliseconds. */
  readonly timeoutMs?: number
  isConcurrencySafe?(args: InferArgs<S>): boolean
  execute(args: InferArgs<S>, exec: ToolRunContext): Promise<InferValue<NoInfer<O>>>
  finalizeContent?(exec: Readonly<ToolExecution>, result: Readonly<ToolExecutionResult>): ContentBlock[] | undefined
  presentCall?(args: InferArgs<S>): ToolCallView | undefined
  presentResult?(args: InferArgs<S>, result: ToolResult): ToolResultView | undefined
}
```

> ⚠️ **`0.2.1-alpha.2` 变更（`c7e62c1062`）**：`output.presentationMeta` 的注释由「direct top-level calls」改为「**native and nested calls**」，运行时守卫也去掉了 `exec.parent === undefined` 前缀 —— **嵌套 PTC 派发现在同样会投影**（`ToolResult.meta` 随之落到 `tool/result` **或** `tool/ptc-dispatch`）。上方摘录已同步为新签名。**纯加法**（改前嵌套调用根本不产生 `meta`），但**声明了该钩子的插件在嵌套派发时也会被调用** —— 若实现里假定「只在顶层被调」，需复核（`packages/core/tools/src/schema.ts:497-498`、`packages/core/tools/src/index.ts:219-220`、`:310`、`:1851`）。

**按重要性分三档**：

| 档位 | 字段 | 你必须知道的 |
|---|---|---|
| **必填** | `name` | 唯一；`run_code` 保留 |
| **必填** | `description` | **写给模型看的**。写得越清楚，模型越会用对。这是提示词工程。 |
| **必填** | `parameters` | 参数 schema，见 4.4 |
| **必填** | `output.schema` | 输出规范值 schema，见 4.5 |
| **必填** | `output.render` | 把规范值渲染成模型可见内容 |
| **必填** | `execute(args, exec)` | 干活的地方 |
| 可选 | `timeoutMs` | 协作式超时（毫秒）。⚠️ **绝不下发给模型**，是本地策略 |
| 可选 | `isConcurrencySafe(args)` | 返回 `true` 才允许与其他工具**并行**跑 |
| 可选 | `presentCall` / `presentResult` | UI 卡片呈现（见第 8 章） |
| 可选 | `finalizeContent` | 模型可见内容的最后一道变换 |
| 可选 | `presentationMeta` | 供 UI 回放的元数据（**`0.2.1-alpha.2` 起嵌套调用也投影**） |

## 4.4 参数怎么写（Schema DSL）

DSH **没有**用 JSON Schema 直接写参数，而是自己的一套 DSL（源码 `packages/core/tools/src/schema.ts:86-107`）。支持的类型：

```ts
type ValueSchemaSpec =
  | { type: 'string' }
  | { type: 'number' }
  | { type: 'integer' }
  | { type: 'boolean' }
  | { type: 'null' }
  | { type: 'array', items? }
  | { type: 'object', properties?, additionalProperties: boolean }
  | { type: 'json' }            // 仅作者侧，不加约束
  | { oneOf: [分支A, 分支B, ...] }  // 至少两分支，恰好命中一个
```

**四条硬规则**（`docs/subsystems/tools.zh.md:110-159` + 源码；旧引 `:100-149`）：

1. **`parameters` 是一个「隐式开放对象」的属性映射** —— 你直接写属性名即可，**不要**自己包一层 `{ type: 'object', properties: {...} }`。
2. **必填靠逐属性 `required: true`**；**不写就是可选**：

```ts
parameters: {
  path:  { type: 'string', required: true, description: 'Absolute path' },  // 必填
  limit: { type: 'number' },                                                 // 可选
}
```

3. **显式对象节点必须声明 `additionalProperties`**（`true` 或 `false`，必填）：

```ts
parameters: {
  options: {
    type: 'object',
    additionalProperties: false,
    properties: { verbose: { type: 'boolean' } },
  },
}
```

4. 标量可以加 `enum` / `const`（必须与节点类型匹配）。

**类型自动推导**：`execute(args)` 里的 `args` 是**有精确类型的**，不是 `any`。上面的例子里 `args` 就是 `{ path: string; limit?: number }`。

**报错对照**：
- 参数不匹配 → `ToolArgsError`（`INVALID_ARGS`）
- 函数体/后置策略产出无效值 → `ToolOutputError`（`INVALID_TOOL_OUTPUT`）

## 4.5 输出怎么写

两个东西：`schema` 定义**规范值**，`render` 把规范值转成**模型看得懂的内容块**。

### 输出是标量

```ts
output: {
  schema: { type: 'string' },
  render: (_args, value) => [{ type: 'text', text: value }],
},
```

### 输出是对象（真实生产级写法）

来源：`packages/interaction/tool-ask-user/src/index.ts:58-80`

```ts
output: {
  schema: {
    type: 'object',
    additionalProperties: false,
    properties: {
      answers: {
        type: 'array',
        required: true,
        items: {
          type: 'object',
          additionalProperties: false,
          properties: {
            id: { type: 'string', required: true },
            selected: { type: 'array', required: true, items: { type: 'string' } },
            custom: { type: 'string' },
          },
        },
      },
    },
  },
  render: (_args, value) => [{ type: 'text', text: JSON.stringify(value) }],
},
```

💡 **关键洞察**：`render` 拿到的 `value` 是**已按 `output.schema` 校验过的对象**，所以可以直接 `JSON.stringify(value)`，不用担心它缺字段。

**为什么要把"规范值"和"渲染"分开？** 因为 `execute` 返回的是**数据**，`render` 负责**表达**。同一份数据可以有不同的表达方式（给模型看的文本、给界面看的卡片），互不干扰。

## 4.6 一个有实用价值的完整例子：读文件

来源：`docs/cookbook/adding-a-tool.zh.md:9-36`（逐字）

```ts
import { readFile } from 'node:fs/promises'
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'my-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'read_file',
    description: 'Read a file from disk.',          // what the model sees
    parameters: {
      path: { type: 'string', required: true, description: 'Absolute path' },
      limit: { type: 'number' },                     // optional by default
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args, exec) {
      // args is TYPED from the schema: { path: string; limit?: number }
      // exec carries immutable identity + token; signal is the operational field
      return readFile(args.path, { encoding: 'utf8', signal: exec.signal })
    },
  }))
}
```

**注意 `exec.signal`**：这是取消信号。长耗时的操作应该把它传给底层 API，这样用户中断时你的操作能跟着停。**这是官方示例刻意演示的最佳实践**。

## 4.7 权限与审批：**不在工具里声明**（重要）

新手最容易犯的错，是在 `defineTool` 里找一个 `permission: 'admin'` 之类的字段。**没有这个字段。**

官方立场（`docs/cookbook/adding-a-tool.zh.md:61`）：**尽量不要把部署策略内建到工具中。**

权限走**注册表流水线**——`tools/pre-execute` 事件（详细写法见第 7 章）。决策类型（`docs/subsystems/tools.zh.md:543-548`；旧引 `:388-412`）：

```ts
type PreToolDecision =
  | { kind: 'allow' }
  | { kind: 'deny'; reason: string; info?: ToolErrorInfo }
  | { kind: 'cancel' }
  | { kind: 'ask'; reason?: string; displayReason?: { readonly en: string; readonly [locale: string]: string } }
```

还有一条**不可撤销**的最终拒绝：`ctx.tools.guard(guard)`（`tools.zh.md:726-731`）：

```ts
type ToolGuard = (execution: Readonly<ToolExecution>) => string | undefined
```

## 4.8 工具的注册表 API 速查

来源：`docs/subsystems/tools.zh.md:639-746`（由源码生成的 cordis-surface；旧引 `:488-580`）

```ts
register(definition: ToolDefinition, options: ToolRegistrationOptions = {}): () => void
restrict(filter: ToolRestriction): () => void
guard(guard: ToolGuard): () => void
get(name: string, scope?: ScopeKey): ToolDefinition | undefined
schemas(scope?: ScopeKey): ToolSchema[]
executionMode(exec: ToolExecutionInput): ToolExecutionMode
async execute(exec: ToolExecutionInput): Promise<ToolExecutionResult>
```

## 4.9 🤖 让 AI Agent 帮你做这一课

> 我要给 DSH 写一个工具插件，功能是：**（用一句话描述你的需求，例如"查深圳天气"）**。
> 请：
> 1. 先读 `docs/user/develop/basic/tool.zh.md` 和 `docs/subsystems/tools.zh.md`，然后告诉我 `defineTool` 的 `parameters` 支持哪些类型；
> 2. 再写插件文件，必须包含 `export const name` / `export const inject = ['tools']` / `apply`；
> 3. `execute` 里所有外部调用都要接 `exec.signal`；
> 4. 输出用 `output.schema` + `output.render` 分离，不要图省事直接返回字符串。
> 约束：**每个 API 都要标注它在仓库中的出处（文件路径 + 行号）**；如果某个字段你没在仓库里找到，就说"未找到"，不允许猜。不要引入任何第三方依赖，除非你能证明仓库里已有同款。

## 4.10 ✅ 第 4 章验收清单

- [ ] 插件里有 `export const inject = ['tools']`
- [ ] `parameters` 是属性映射，**没有**多包一层 `type: 'object'`
- [ ] 必填参数写了 `required: true`，可选参数**没有**写
- [ ] 有 `output.schema` 与 `output.render`
- [ ] `execute` 里用到了 `args`（而且是有类型的，不是 `any`）
- [ ] 长耗时操作接了 `exec.signal`
- [ ] 在 DSH 里实际让模型调用了一次你的工具，看到了结果

---

# 第 5 章 第三课｜可配置插件：让用户不改代码就能调参

> **本课目标**：把你的插件变成「可配置」的——用户在 `cordis.yml` 里填几个值，行为就变了。
> **为什么重要**：官方有一条硬规矩——**不允许硬编码可调参数**。

## 5.1 官方硬规矩（先记住这句话）

`docs/user/develop/basic/config.zh.md:80`（逐字）：

> Harness 的约定：**凡是不同部署可能需要采用不同值的参数，都必须定义为配置字段**。

检验标准（`config.zh.md:92`）：

> 能否在 `cordis.yml` 中改变这个值，而不需要修改代码？

反面例子（官方给的）：

```ts
// Wrong: hardcoded timeout.
const TIMEOUT = 30000
```

## 5.2 定义 Config（完整写法，逐字照抄）

来源：`docs/user/develop/basic/config.zh.md:11-32`

```ts
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'

export const name = 'my-plugin'

export interface Config {
  greeting: string
  maxRetries: number
  verbose?: boolean
}

export const Config: Schema<Config> = Schema.object({
  greeting: Schema.string().default('Hello'),
  maxRetries: Schema.number().default(3),
  verbose: Schema.boolean().default(false),
})

export function apply(ctx: Context, config: Config) {
  console.log(config.greeting)  // User value or schema default.
}
```

**这段代码有三个「反直觉」的地方，必须讲清楚**：

1. **`Config` 是双重身份**：`export interface Config` 是**类型**（给 TypeScript 编译器看），`export const Config` 是**运行时校验器**（给 Cordis 看）。它们**同名共存**。
2. **`apply` 多了第二个参数**：`apply(ctx, config)`。配置从框架传进来。
3. **⚠️ 不要导出普通对象当 `Config`** —— 官方原文（`config.zh.md:45`）：「不要导出普通对象作为 `Config`，因为它不满足 Cordis 要求的 Standard Schema 接口。」必须用 Schemastery（或任意 Standard Schema 验证器）。

## 5.3 用户在 `cordis.yml` 里怎么填

来源：`docs/user/develop/basic/config.zh.md:36-43`

```yaml
- insert:
    - id: hello
      name: './src/my-plugin.ts'
      config:
        greeting: 'Hi there'
        maxRetries: 5
```

**行为**：插件加载时，Cordis 用你的 schema 校验配置，**未提供的字段自动填默认值**。所以 `apply` 里拿到的 `config` **永远是完整且经过验证的**（`docs/cordis-tutorial/05-config.zh.md`）。

## 5.4 严格校验：必填与枚举

来源：`docs/user/develop/basic/config.zh.md:51-71`

```ts
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'

export const name = 'validated-plugin'

export interface Config {
  apiKey: string
  timeout: number
  mode: 'fast' | 'accurate'
}

export const Config = Schema.object({
  apiKey: Schema.string().required(),
  timeout: Schema.number().default(30000),
  mode: Schema.union(['fast', 'accurate']).default('fast'),
})

export function apply(ctx: Context, config: Config) {
  // config is validated and type-safe.
}
```

**常用 Schemastery 方法**（本文档范围内证实可用的）：
`Schema.string()` / `Schema.number()` / `Schema.boolean()` / `Schema.array(...)` / `Schema.object({...})` / `Schema.union([...])`
修饰：`.default(v)` / `.required()` / `.step(1)` / `.min(n)` / `.max(n)`

来源：`docs/cordis-tutorial/05-config.zh.md`、`packages/client/ui-theme/src/theme-settings.ts`

## 5.5 配置写错了会怎样？（重要）

配置校验失败**不会**静默跳过，而是**响亮地失败**。

来源：`docs/cordis-tutorial/05-config.zh.md`（逐字）

```yaml
- name: './config-demo.ts'
  config:
    targets: 'not-an-array'
```

```
ValidationError: invalid config:
  - $.targets expected array but got not-an-array (at targets)
```

> 插件的 fiber 进入 FAILED 状态，本教程的启动器打印错误后以状态码 1 退出。

**这正是官方提倡的**（`config.zh.md:94`）：「配置错误要响亮」——在 schema 里表达自身完备的约束，使无效配置在**插件加载时**就失败，而不是等到运行时出诡异问题。

## 5.6 一个特殊能力：`!!js` 表达式

来源：`docs/cordis-tutorial/05-config.zh.md`

```yaml
- name: './config-demo.ts'
  config:
    greeting: !!js process.env.DEMO_GREETING ?? 'Hello'
```

⚠️ **只在两个地方有效**：插件的 `config` 字段、以及条目级的 `disabled` 字段。其余元数据（`name`、`id`、`inject`）保持静态。

⚠️ **官方事故复盘**（`docs/postmortem/0002-js-expression-disabled-filesystem-tools.zh.md`）：有人把 `!!js` 用在 entry 级 `disabled` 上期待条件求值，结果 Cordis **只在插件 `config` 内部求值 `!!js`**，entry 级 `disabled` 是直接读取的，表达式对象恒为真 → 文件系统栈被**永久禁用**。教训原文：

> 语法上被接受的配置值不一定在该位置被求值；应记录并验证具体对哪些字段进行插值。

**所以：不要拿 `!!js` 玩花样。** 需要条件启用/禁用，就把判断写进代码。

## 5.7 配置改了会怎样

`config.zh.md:100`：

> 配置变更会触发插件热替换：修改 `cordis.yml` 中某个插件的 `config` 后，框架会卸载旧实例并加载新实例。由于注册都属于 effect 并会自动清理，替换后不会保留旧实例的注册。

**这是「注册即 effect」设计带来的直接好处**：重新加载 = 旧的全部撤销 + 新的重新注册，干净无残留。

## 5.8 🤖 让 AI Agent 帮你做这一课

> 请把我第 4 章写的工具插件改成「可配置」的：
> 1. 找出插件里所有写死的参数（路径、超时、阈值、开关），列给我看；
> 2. 按 `docs/user/develop/basic/config.zh.md` 的写法加 `Config`：`interface` + 同名 `const Config = Schema.object(...)`，每个字段都要有 `.default(...)`；
> 3. 告诉我 `cordis.yml` 里怎么填；
> 4. 举一个"用户填错配置"的例子，并说明会报什么错。
> 约束：字段名用英文，必须有 JSDoc 注释说明用途；**不允许**保留任何硬编码的可调参数。

## 5.9 ✅ 第 5 章验收清单

- [ ] 有 `export interface Config`（类型）
- [ ] 有 `export const Config = Schema.object(...)`（运行时校验器），**不是**普通对象
- [ ] 每个字段都有 `.default(...)` 或 `.required()`
- [ ] `apply` 签名是 `apply(ctx: Context, config: Config)`
- [ ] 插件里**没有**残留的硬编码可调参数
- [ ] 故意填错一次配置，确认看到了 `ValidationError`

---

# 第 6 章 第四课｜命令插件：给人用的 `/斜杠命令`

> **本课目标**：注册一个用户能直接敲的命令（如 `/compact`）。
> **和工具的区别**：工具是**模型**决定什么时候用；命令是**人**决定什么时候用。

## 6.1 完整示例（最小可抄）

来源：`packages/interaction/commands/README.zh.md:34-44`

```ts
ctx.commands.register({
  name: 'plan',
  description: 'Enter plan mode',
  input: { hint: '<message>' },
  handler: ({ agent, rawInput }) => {
    // Runs directly against the agent; no model message is created.
    return { kind: 'success', text: 'plan mode selected' }
  },
})
```

## 6.2 `CommandDefinition` 完整字段

来源：`docs/subsystems/commands.zh.md:33-53`（逐字）

```ts
interface CommandDefinition {
  /** Stable plugin-owned identity; absent for definitions without identity-based client behavior. */
  readonly definitionId?: CommandDefinitionId
  /** Lowercase command name without the leading slash. */
  readonly name: string
  /** Human-readable summary used in discovery UI. */
  readonly description: string
  /** Optional free-form input hint advertised to capable clients. */
  readonly input?: CommandInputDescriptor
  /**
   * Whether `command/run` records `rawInput`. Defaults to true. A command
   * whose domain event owns the payload sets this false to avoid duplicating
   * that payload in the session log.
   */
  readonly recordInput?: boolean
  /** Execute against the receiving agent without sending the command to the model. */
  readonly handler: (invocation: CommandInvocation) => CommandResult | Promise<CommandResult>
}
```

配套类型（`commands.zh.md:13-91`）：

```ts
interface CommandInputDescriptor {
  readonly hint: string
  readonly attachments?: boolean
}

interface CommandInvocation {
  readonly commandId: CommandId
  readonly agent: Agent
  readonly rawInput: string
  readonly attachments: readonly (ImageBlock | FileBlock)[]
  readonly signal: AbortSignal
}

type CommandResult =
  | {
    readonly kind: 'success'
    readonly text?: string
    readonly sourceEventSeq?: SessionSeq
  }
  | { readonly kind: 'error'; readonly text: string }
```

**字段精讲**：

| 字段 | 说明 |
|---|---|
| `name` | **小写、不带斜杠**。写 `'plan'`，用户敲 `/plan` |
| `definitionId` | 插件的稳定身份。**建议写**，用包名，例如 `CommandDefinitionId('@your/your-plugin')` |
| `input.hint` | 给界面用的输入提示，如 `'<message>'` |
| `recordInput` | 是否把用户输入记进会话日志，默认 `true` |
| `handler` | 真正的逻辑。**注意它能拿到 `agent`**，即直接操作智能体，不经过模型 |

## 6.3 命令的语法规则

来源：`packages/interaction/commands/README.zh.md:48-50`

- 命令行**第 0 个字节必须是 `/`**
- 随后是**小写名称**（可含字母、数字、`_`、`-`）
- 之后的**所有字节**（含分隔空白）都算 `rawInput`
- 不符合语法或名称未知的行会被适配器**拒绝**，**而不是**变成模型提示词

⚠️ **重要限制**（`docs/subsystems/commands.zh.md:11`）：**无 UI 的演示与 ACP 自动化不提供命令面** —— 命令只在交互式 UI（CLI / Web）里存在。

## 6.4 真实范本：`/compact`

仓库里最清晰的命令插件是 `packages/compaction/command-compact/`（主文件 108 行）。它的骨架（`src/index.ts:6-14`，逐字）：

```ts
import type { Context } from '@deepseek-ai/cordis'
import { CommandDefinitionId } from '@deepseek-ai/dsh-commands/brand'
import { ManualCompactionError } from '@deepseek-ai/dsh-compaction'
import type { CommandInvocation, CommandResult } from '@deepseek-ai/dsh-commands'

export const name = 'command-compact'
export const inject = ['commands', 'compaction']
```

它的 `apply` 里展示了一个**进阶但很值得借鉴**的写法——用 `ctx.effect` 管理"正在执行的命令"的生命周期（`src/index.ts:85-108`）：

```ts
export function apply(ctx: Context): void {
  const active = new Set<Promise<CommandResult>>()
  const handler = (invocation: CommandInvocation): Promise<CommandResult> => {
    const operation = executeCompact(ctx, invocation)
    active.add(operation)
    const retire = (): void => { active.delete(operation) }
    void operation.then(retire, retire)
    return operation
  }

  ctx.effect(function* () {
    // Yield drain before registration: composite teardown is LIFO, so no new
    // invocation can enter while already-started handler promises quiesce.
    yield async () => { await Promise.allSettled(active) }
    yield ctx.commands.register({
      definitionId: CommandDefinitionId('@deepseek-ai/dsh-command-compact'),
      name: 'compact',
      description: 'Compact older conversation history',
      handler,
    })
  }, 'command-compact lifecycle')
}
```

💡 这一段的**设计意图**：卸载时先"排空"正在执行的命令，再注销注册。因为复合拆卸是 **LIFO（后进先出）** 的，把 `yield` 顺序写对，才能保证"没有新的调用进入"之后才真正注销。**这是给进阶者的范例，你第一版不用写到这个程度。**

## 6.5 什么时候用命令、什么时候用工具

官方给的最佳范例是 Plan mode（`docs/cookbook/extension-cookbook.zh.md:126`）：

> `/plan [message]` 入口是**命令**（人主动进入计划模式），`exit_plan_mode` 出口是**工具**（模型判断该退出了）。

**判断口诀**：
- 「用户想主动做的事」→ 命令
- 「模型需要用来完成任务的能力」→ 工具
- 「两者都要」→ 各写一个（就像 Plan mode）

## 6.6 🤖 让 AI Agent 帮你做这一课

> 我要给 DSH 加一个斜杠命令 `/（你的命令名）`，作用是**（描述）**。
> 请：
> 1. 先读 `docs/subsystems/commands.zh.md`，把 `CommandDefinition` 的字段列表和 `CommandResult` 的两种形态说给我听；
> 2. 参考 `packages/compaction/command-compact/src/index.ts` 的写法，写一个命令插件；
> 3. 明确告诉我 `inject` 该写哪些服务名，以及为什么；
> 4. 告诉我用户敲什么能看到我的命令。
> 约束：命令名必须小写、不带斜杠；`handler` 不要创建模型消息；每个 API 标注仓库出处。

## 6.7 ✅ 第 6 章验收清单

- [ ] 插件有 `export const inject = ['commands']`（以及你真正需要的其他服务）
- [ ] `name` 是小写、无斜杠
- [ ] `handler` 返回的是 `{ kind: 'success' | 'error', text }` 形态
- [ ] 在 Web UI 里敲 `/你的命令` 能真的触发
- [ ] 你能说清：为什么这个功能做成了命令而不是工具

---

# 第 7 章 第五课｜进阶：事件、拦截与权限门禁

> **本课目标**：不新增功能，而是**改变已有行为**——审计别人的工具调用、拦截危险操作、给工具加权限。
> **难度说明**：这一章涉及「事件分发模式」，是全书概念密度最高的一章。慢慢看。

## 7.1 事件：五种分发模式（必须分清）

来源：`docs/cordis-tutorial/04-events.zh.md`、`docs/cordis-primer.zh.md`

| 模式 | 调用 | 是否 await | 语义 |
|---|---|---|---|
| **emit** | `ctx.emit(name, ...args)` | 否 | 同步广播；不等待、不收集返回值 |
| **parallel** | `await ctx.parallel(name, ...args)` | 是 | 所有监听器**并发**运行，一起等 |
| **serial** | `await ctx.serial(name, ...args)` | 是 | 监听器**按顺序**运行并等待；第一个非 `null`/`false`/`undefined` 的返回值**胜出**并停止后续 |
| **bail** | `ctx.bail(name, ...args)` | 否 | serial 的**同步**版本 |
| **waterfall** | `ctx.waterfall(name, ...args, next)` | 否 | **环绕中间件**：每个监听器决定"继续传给下一个"还是"就在这里截断" |

**新手只需记住两种**：
- 我要**看**（审计、记录、统计）→ `ctx.on(...)` + emit
- 我要**改/拦**（改写、否决、门禁）→ waterfall

## 7.2 最基础：监听一个事件

来源：`docs/user/develop/framework/events.zh.md`

```ts ignore-check
ctx.on('event-name', (payload) => {
  // Handle the event.
})
```

```ts ignore-check
ctx.emit('event-name', payload)
```

**真实可运行范例：记录每一次工具调用**（`docs/cordis-tutorial/07-into-the-harness.zh.md`，逐字）

```ts
import type { Context } from '@deepseek-ai/cordis'
import type {} from '@deepseek-ai/dsh-tools'

export const name = 'tool-logger'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.on('tools/result', (exec, result) => {
    const text = result.content
      .map(block => (block.type === 'text' ? block.text : ''))
      .join('')
    console.log(`[tool-logger] ${exec.name} -> ${text}`)
  })
}
```

💡 **`import type {} from '@deepseek-ai/dsh-tools'` 这一行的作用**：它不导入任何运行时值，只是**引入该包的声明合并**，让 `'tools/result'` 这个事件名和它的参数具有类型。少了它，TypeScript 会报"未知事件名"。

⚠️ **监听器也是 effect**：`ctx.on()` 注册的监听器会随插件卸载自动移除，**永远不需要手动 removeListener**（`docs/user/develop/framework/events.zh.md`）。

## 7.3 waterfall：唯一的"改动别人行为"机制

这是本仓库的**常设规则**，违反了会造成极隐蔽的 bug。

`docs/cordis-tutorial/04-events.zh.md` 原文（逐字）：

> **只负责观察或标注的 waterfall 监听器必须调用 `next()`**；不调用就直接返回代表有意短路。如果日志监听器忘记调用 `next()`，会悄无声息地吞掉所有下游的默认行为。这是本仓库的常设规则。

**完整示例**（`04-events.zh.md`，逐字）：

```ts
import type { Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Events {
    'demo/transform'(input: string, next: () => Promise<string>): Promise<string>
  }
}

export const name = 'waterfall-demo'

export function apply(ctx: Context) {
  // Listener 1: wrap the downstream result.
  ctx.on('demo/transform', async (input, next) => {
    const downstream = await next()
    return downstream.toUpperCase()
  })

  // Listener 2: short-circuit when it owns the decision.
  ctx.on('demo/transform', async (input, next) => {
    if (input.includes('blocked')) return '** blocked **'
    return next()
  })

  void (async () => {
    console.log(await ctx.waterfall('demo/transform', 'hello', async () => 'hello'))
    console.log(await ctx.waterfall('demo/transform', 'blocked words', async () => 'blocked words'))
  })()
}
```

输出：

```
HELLO
** BLOCKED **
```

**看懂这段的两个关键**：
1. **监听器 1** 先 `await next()` 拿到下游结果，再 `toUpperCase()` —— 这是「观察后加工」。
2. **监听器 2** 遇到 `blocked` 就直接 `return` —— 这是「短路 / 否决」，下游再也不会执行。

## 7.4 真实威力：给所有工具加权限门禁

来源：`docs/cookbook/extension-cookbook.zh.md:17-33`（逐字；该文件自述此片段**省略了 import 与 `isAllowed` 实现，无法直接复制运行**）

```ts
import type { Context } from '@deepseek-ai/cordis'
import type { PreToolDecision, ToolExecution } from '@deepseek-ai/dsh-tools'

declare function isAllowed(exec: ToolExecution): Promise<boolean>

export const name = 'permission-gate'

export function apply(ctx: Context) {
  ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
    if (!(await isAllowed(exec))) {
      return { kind: 'deny', reason: 'Denied by policy.' }
    }
    return next()
  })
}
```

**这一个插件就能管住所有工具**（包括官方工具）——这就是「一切皆插件」架构的威力：你没有改官方一行代码，却改变了它的行为。

`ask` 决策需要审批服务配合才生效；**没有审批通道时，`ask` 会变成拒绝**（`docs/subsystems/tools.zh.md:545`；旧引 `:402`）。

## 7.5 自定义事件（声明类型）

来源：`docs/user/develop/framework/events.zh.md`（逐字）

```ts
import '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Events {
    'my-plugin/ready': (payload: { id: string }) => void
    'my-plugin/check': (input: string) => boolean | undefined
    'my-plugin/transform': (input: string, next: () => Promise<string>): Promise<string>
  }
}
```

**命名规范**：`namespace/action`。harness 自己的事件都遵循这个规范（`agent/pre-step`、`tools/result`、`session/event`）。

## 7.6 ⚠️ 一个极容易踩的坑：会话事件 vs Cordis 事件

`docs/user/develop/framework/events.zh.md` 原文（逐字）：

> `turn/*`、`step/*`、`tool/call`、`tool/result` 和 `compaction/*` 是**持久化的会话事件类型，不是同名 Cordis 事件**。需要观察它们时，监听 `session/event` 并检查 `event.type`。
>
> Harness 的 Cordis 事件遵循 `namespace/action` 命名，例如 `agent/pre-step`、`agent/request`、`agent/request-error`、`tools/result` 和 `session/event`。

**这段话的重要性**：`tools/result` 是 Cordis 事件 ✅，但 `tool/result` 是会话事件类型 ❌。**一字之差（单复数），排查起来能要你半条命。**

**已证实存在的 harness 事件**（本手册核实过的）：

| 事件名 | 类型 | 用途 |
|---|---|---|
| `tools/result` | Cordis 事件 | 工具结果物化时触发 |
| `tools/pre-execute` | Cordis 事件（waterfall） | 工具执行前的门禁/改写 |
| `agent/pre-step` | Cordis 事件 | 步骤开始前 |
| `agent/request` | Cordis 事件（waterfall） | 请求发出前，可改写 |
| `agent/request-error` | Cordis 事件 | 请求出错 |
| `session/event` | Cordis 事件 | 会话事件流总入口 |
| `internal/status` | Cordis 事件 | fiber 状态转换 |

⚠️ **不存在「完整的内置事件清单」文档**。官方反复指向各子系统页面里**自动生成**的 `cordis-surface` 区块。官方明确要求：**不要维护另一份静态清单**，要用时去查生成的区块和 TypeScript 接口。

**实用建议**：想知道某个服务有哪些事件和方法，直接让你的 Agent 去读对应的 `docs/subsystems/<服务名>.zh.md`。

## 7.7 服务：从「用别人的」到「给别人用」

### 用别人的服务（第 4 章用过）

```ts
export const name = 'consumer'
export const inject = ['greeter']

export function apply(ctx: Context) {
  console.log(ctx.greeter.greet('world'))
}
```

`inject` 的**精确语义**（`docs/cordis-tutorial/03-services.zh.md`，逐字）：

> `inject` 列出该插件需要的服务。Cordis 会让插件保持 PENDING，直到列出的每项服务都存在，因此在 `apply` 内可以保证 `ctx.greeter` 已经就绪。

⚠️ **`inject` 不是一次性的启动检查**（同一文档，逐字）：

> 如果应用运行期间所需服务消失，例如提供方被卸载或热替换，每个依赖插件也会随之卸载，并在服务恢复后再次加载。

### ⚠️ 可选依赖必须用 `ctx.get()`，不要用 `ctx.<name>`

这是官方事故复盘里的根因之一（`docs/postmortem/0001-acp-default-export-drops-inject.zh.md`），也是 `packages/AGENTS.md:6` 的硬规则（逐字）：

> **Optional services use `ctx.get(name)`.** Reserve `ctx.<name>` for declared injections; the property proxy is topology-sensitive, while strict `ctx.get` reads the global service store.

正确写法：

```ts ignore-check
export function apply(ctx: Context) {
  // undefined when no provider is loaded; the plugin still runs.
  const greeter = ctx.get('greeter')
  console.log(greeter?.greet('maybe') ?? 'no greeter available')
}
```

**为什么**？属性代理 `ctx.<name>` 的解析**只向祖先方向遍历 fiber**，经过外部 shadow 时会失败；`ctx.get(name)` 是**拓扑无关**的查找。**这条踩坑成本极高，请务必记住。**

### 定义自己的服务（要让别人用时才需要）

来源：`docs/cordis-tutorial/03-services.zh.md`（逐字）

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context {
    greeter: GreeterService
  }
}

export class GreeterService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'greeter')
  }

  greet(who: string) {
    return `Hello, ${who}!`
  }
}

export const name = 'greeter'

export function apply(ctx: Context) {
  ctx.plugin(GreeterService)
}
```

官方对两部分的解释（逐字）：
- **运行时**：`super(ctx, 'greeter')` 以名称 `greeter` 注册该实例。此后任何插件都可以通过 `ctx.greeter` 访问。
- **编译时**：`declare module '@deepseek-ai/cordis'` 块使用 TypeScript 声明合并，把 `greeter` 加入 `Context` 接口。**它不生成代码**；没有该声明时服务运行时仍能工作，但消费方会失去类型安全。

⚠️ **服务名是全局扁平命名空间**。官方提醒（`03-services.zh.md`）：

> 请为自有服务添加有辨识度的前缀或命名空间（harness 已占用 `tools` 和 `llm` 等普通名称）。

**建议**：服务名写成 `你的插件名-api` 这种形式，别叫 `cache`、`data` 这类烂大街的名字。冲突时 `ctx.provide` 会**抛异常**（`docs/cordis-api/context.zh.md`）。

## 7.8 诊断：为什么我的插件没反应？（PENDING）

最让新手抓狂的场景：插件明明写了，就是不执行，**还不报错**。答案是 **PENDING**。

`docs/cordis-tutorial/03-services.zh.md` 原文（逐字）：

> 尝试彻底移除 `./greeter.ts`：消费方会保持 PENDING，不输出任何内容，既不崩溃，也不会只运行一部分。处于 PENDING 的 fiber 也不会让 Node 的事件循环保持活跃，因此如果组合中没有其他运行项，进程会静默地以状态码 0 退出。

**好消息：DSH 启动时会审计这件事。** 源码实证（`packages/boot/app-boot/src/index.ts:1112` 单条格式串、`:1132` 分组汇总表）：树 settle 后，对仍处于 PENDING 的条目会打印

```
<name>: pending (waiting for service: <缺失服务>)
```

然后抛出 `dsh: N entries did not activate` 并以**非零**状态退出。

**所以：如果你的插件毫无反应，先看启动日志里有没有 `pending (waiting for service: ...)`。** 这行字直接告诉了你缺哪个服务。

## 7.9 🤖 让 AI Agent 帮你做这一课

> 我要给 DSH 加一个「（你的策略，例如：禁止删除操作 / 记录所有工具调用到文件）」。
> 请：
> 1. 先读 `docs/user/develop/framework/events.zh.md` 与 `docs/subsystems/tools.zh.md`，告诉我应该监听哪个事件、用哪种分发模式（emit/serial/waterfall）；
> 2. 写插件，注意：**只观察**的监听器必须调用 `next()`；
> 3. 如果我要拦截，请明确说明返回什么值代表"允许"、什么代表"拒绝"；
> 4. 告诉我怎么验证它生效了。
> 约束：如果用可选服务，必须用 `ctx.get(name)`；不要用 `ctx.<name>` 读未声明的服务。所有事件名必须能在仓库里找到出处——**特别注意 `tools/result`（Cordis 事件）和 `tool/result`（会话事件类型）的区别**。

## 7.10 ✅ 第 7 章验收清单

- [ ] 我能说出 emit / serial / bail / waterfall 的区别
- [ ] 我写的 waterfall 监听器在"只观察"时调用了 `next()`
- [ ] 我用的可选服务是 `ctx.get(name)` 而不是 `ctx.<name>`
- [ ] 我知道 `tools/result` ≠ `tool/result`（一个是事件、一个是会话事件类型）
- [ ] 我知道插件没反应要去日志里找 `pending (waiting for service: ...)`

---

# 第 8 章 第六课｜终端类插件（PTY 家族 + 终端卡片）

> **本课目标**：让 AI 能在终端里跑**交互式**命令并保持状态（跨多次工具调用）。
> ⚠️ **先纠正一个流行误解**，见下。

## 8.1 ⚠️ 重要澄清：这里的"终端"指什么

| 你可能以为 | 实际 |
|---|---|
| 「写一个终端界面（TUI）插件」 | ❌ TUI 前端**已归档**（2026-08-04），当前仓库无 `packages/ui/` |
| 「给 AI 一个能持续交互的终端」 | ✅ **这才是「终端」在 DSH 里的含义** |

`docs/subsystems/terminal.zh.md` 讲的**不是界面渲染**，而是**持久 PTY 会话能力**：让 agent 的交互式 shell/REPL **跨工具调用**保持（工作目录、环境变量、运行中的子进程）。

归档笔记（`.agents/notes/archived/feature/2026-07-17-dedicated-full-screen-tui-front-door.zh.md`）明确：

> 可复用的 TUI 包（package）仍然保留实现，但 [`dsh` 不再将其作为应用入口交付]。Status: implemented / Archived: 2026-08-04

**本手册如实告知：当前快照下，「自己写 TUI 插件」没有可照抄的路径。** 如果你就是想做，只能参考归档笔记（渲染基于 `pi-tui`，要求 stdin/stdout 均为 TTY），风险自担。

## 8.2 终端能力由三个包组成

来源：`packages/terminal/README.zh.md:27-30`（⚠️ `0.2.1-alpha.2` 起该家族只剩 `terminal/` 与 `terminal-bash/` 两行 —— `tool-terminal/` 已搬到 `packages/experimental/tool-terminal/`，**包名 `@deepseek-ai/dsh-tool-terminal` 不变**）

| 包 | 角色 | ctx 键 |
|---|---|---|
| `terminal/`（`@deepseek-ai/dsh-terminal`） | **会话服务**：限定所有者范围的会话、不透明 id、精确到所有者的限制与等待完成的清理 | `ctx.terminals` |
| `terminal-bash/`（`@deepseek-ai/dsh-terminal-bash`） | **shell 后端**：在共享沙箱策略下启动交互式 bash 或 pwsh | 注册后端到 `ctx.terminals` |
| `tool-terminal/`（`@deepseek-ai/dsh-tool-terminal`） | **6 个面向模型的工具** | 注册到 `ctx.tools` |

> ⚠️ **`0.2.1-alpha.2` 起 `tool-terminal/` 不在 `packages/terminal/` 下了** —— 它搬到 `packages/experimental/tool-terminal/`（**包名不变**），故下方两处引用均指向新路径；`packages/terminal/` 只剩 `terminal/`（会话服务）与 `terminal-bash/`（shell 后端）。

**这三个包正好演示了第 1 章讲的 capability seam 三角色**：Service Definition + Service Provider + Consumer。这是仓库里最标准的三角色范本。

组合方式（`packages/experimental/tool-terminal/README.zh.md:46-48`，逐字）：

```yaml
- name: '@deepseek-ai/dsh-terminal'
- name: '@deepseek-ai/dsh-terminal-bash'
- name: '@deepseek-ai/dsh-tool-terminal'
```

## 8.3 六个终端工具

| 工具名 | 作用 |
|---|---|
| `terminal_open` | 开一个会话 |
| `terminal_send` | 往里发输入 |
| `terminal_read` | 读输出 |
| `terminal_signal` | 发信号（如 Ctrl-C） |
| `terminal_close` | 关闭会话 |
| `terminal_list` | 列出会话 |

来源：`packages/experimental/tool-terminal/README.zh.md:34-41`（新位置含「作用 / 结果」两列）

**这六个工具就是普通的 `defineTool`**，和第 4 章你学的完全同构。它们本身不渲染任何东西——**呈现交给各 UI 的适配器**。

## 8.4 带 Config 的终端工具（示范"数值范围校验"）

来源：`packages/experimental/tool-terminal/src/index.ts:37-49`（逐字）

```ts
/** Model-facing terminal tool configuration. */
export interface Config {
  /** Expose `run_in_background` and accept background sends (default true). */
  enableRunInBackground?: boolean
  /** Maximum UTF-8 bytes in one complete terminal or task-output result. */
  maxResultBytes?: number
}

/** Schemastery configuration for the terminal tool consumer. */
export const Config: z<Config> = z.object({
  enableRunInBackground: z.boolean().default(true),
  maxResultBytes: z.number().step(1).min(MIN_MAX_RESULT_BYTES).max(Number.MAX_SAFE_INTEGER).default(DEFAULT_MAX_RESULT_BYTES),
})
```

💡 **这段是「第 5 章 Config」的最佳实战范本**：注意它用了 `.min()` / `.max()` / `.step()` 做范围约束——这就是官方说的"配置错误要响亮"。

> ⚠️ **`0.2.1-alpha.2` 变更**：上面这段 Config 本身**逐字未变**，但同文件的 `inject` 多了 **`workingDirectory`**（`['terminals','tools','systemPrompt','workingDirectory']`，`:30`），且 `terminal_open` 的 **`cwd` 语义改了** —— 由「缺省用部署工作区根」改为**「相对 Session 当前目录解析，非绝对路径即按 Session 目录展开」**（`:171` 的描述串 + `:187-192` 用 `ctx.workingDirectory.ensure(owner, exec.signal)` 取值再 `resolve(cwd, args.cwd)`）。**写这类工具的插件若要「跟着会话换目录」，需照抄这个 `inject` + `ensure()` 模式。**

## 8.5 工具卡片：让工具在界面上好看

工具执行时，界面要显示什么？靠两个**纯函数**：

| 函数 | 何时调用 | 返回 |
|---|---|---|
| `presentCall(args)` | 调用**进行中** | `ToolCallView` |
| `presentResult(args, result)` | 调用**完成** | `ToolResultView` |

可用的卡片类型（`docs/subsystems/tools.zh.md:622-623`；旧引 `:459-468`）：

- `presentCall` → `generic` / `terminal` / `diff`
- `presentResult` → `generic` / `terminal` / `diff` / `read` / `search` / `web`

**真实范例**（`packages/shell/tool-bash/src/index.ts:101-135`，逐字节选）：

```ts
function presentBashCall(args: BashCallArgs): GenericCallView | TerminalCallView {
  if (args.run_in_background === true) {
    return {
      card: 'generic',
      title: args.command,
      kind: 'execute',
      rawInput: args.command,
      content: [{ type: 'text', text: args.description }],
    }
  }
  return {
    card: 'terminal',
    title: args.command,
    description: args.description,
    ...args.workdir !== undefined ? { cwd: args.workdir } : {},
  }
}
```

### ⚠️ 三条硬约束（写错了会出现诡异的运行期问题）

1. **必须是纯函数**：实时流与回放都会跑它。
2. **不得做 I/O、不得读会话状态/时钟/随机数。**
3. **参数格式错误要返回 `undefined`（回退到通用卡片），不要抛异常** —— `defineTool` 对展示路径做的是**软校验**（`docs/cookbook/adding-a-tool.zh.md:87-91`）。

### ⚠️ 一个反直觉事实

`docs/cookbook/adding-a-tool.zh.md:97` + 源码 `packages/core/tools/README.zh.md:98`：

> 内置 Web Client **不消费** `presentCall` / `presentResult`，而是通过 keyed slot `tool.call.toolview` 从原始事件派生。

**翻译**：你写的卡片函数，默认 Web UI **不看**。要让界面真的按你的想法渲染，得往 `tool.call.toolview` 插槽里注册组件（第 9 章）。

## 8.6 关于 `ctx.terminals` 服务

`docs/subsystems/terminal.zh.md:101-184` 给出了完整签名：`registerBackend` / `spawn` / `startSend` / `read` / `signal` / `kill` / `list`。

**新手建议**：除非你要**换一个终端后端**（比如接到远程机器），否则**不要去实现这个服务**——直接用官方那三个包提供的工具就够了。要写 Provider，请先读 `packages/terminal/terminal-bash/`（1244 行）作为范本。

## 8.7 🤖 让 AI Agent 帮你做这一课

> 我想让 DSH 具备「（终端相关需求）」能力。
> 请先回答三个问题，**再**写代码：
> 1. 我的需求是「让模型能操作持久终端」（→ 用 `@deepseek-ai/dsh-tool-terminal` 那三个包）还是「换一个终端后端」（→ 实现 Provider）？
> 2. 对应的事件名、服务名、工具名，在 `docs/subsystems/terminal.zh.md` 与 `packages/terminal/` 里的出处分别是什么？
> 3. 如果要自定义工具卡片，`presentCall` / `presentResult` 必须遵守哪些约束？
> 约束：**明确告诉我 TUI 前端在当前版本是否可用**，如果你在仓库里找不到 `packages/ui/tui`，就直接说不存在，不要按记忆补全。

## 8.8 ✅ 第 8 章验收清单

- [ ] 我能说清「终端插件」在 DSH 里指 PTY 能力，不是 TUI 界面
- [ ] 我知道终端能力由哪三个包组成、各自是什么角色
- [ ] 我能列出至少 4 个终端工具名
- [ ] 我知道 `presentCall` / `presentResult` 必须是纯函数
- [ ] 我知道内置 Web Client 默认不消费这两个函数

---


---

