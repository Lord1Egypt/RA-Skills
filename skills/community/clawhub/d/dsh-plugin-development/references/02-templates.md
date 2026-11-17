> **文件来源**：本文件由 DSH 插件开发手册套件整合生成；**2026-09-14 已把两段上游素材拆出为独立分册**（`02b`/`02c`），本文件只保留面向任务的整理稿。

> **本文件用途**：由易到难的 12 个可直接复制的插件模板（T1~T12），覆盖零代码组合包、补丁语法、工具、命令、配置、服务、UI、设置卡片、流程拦截、外部集成、工程骨架。**官方七类模板的逐字源码**已拆到 `02b-official-templates.md`，**社区零代码组合包全文**已拆到 `02c-community-bundle.md`。T3/T5/T6 与 `02b` 的模板 3/4/5 是同一件事的两种粒度：本文件给讲解与坑，`02b` 给可逐字照抄的完整源码——**冲突时以 `02b` 的官方源码为准**。
> **合成来源**：DSH插件开发实战补充-模板与踩坑.md（第二篇）
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。

> **本文件导航 —— 共 1,260 行，纯整理稿（已无上游素材混杂）。**
> - 内容：T1~T12 十二个模板，按**难度从易到难**排列；每节自带「何时选它 / 完整代码 / 常见坑」。
> - **不要整读**：先 `grep -n '^## T[0-9]'` 拿模板清单（12 条），再只读你要的那一个模板。
> - 相关的上游原文分册：`02b-official-templates.md`（官方 7 类逐字源码）、`02c-community-bundle.md`（社区组合包范本）。

---

<!-- ↓ 源：DSH插件开发实战补充-模板与踩坑.md 区间 64-1256 -->

# 第二篇 · 模板库（12 个，由易到难）

> 每个模板的结构：**它是干什么的 → 完整代码（逐字可抄）→ 逐行讲解 → 易错点 → 🤖 AI Agent 提示词**。
> 全部代码来自真实仓库，标注来源路径。

---

## T1 · 零代码组合包 ★（最小可用插件）

**它是什么**：整个插件只有 **3 个文件**，**不写一行 JavaScript**。靠一个 `cordis.patch.yml` 把现成能力挂进 DSH。
**来源**：`Q00/ouroboros → integrations/dsh-plugin/`（官方精选清单里**唯一**的纯配置零代码插件，约 5,805★）。它靠这一个补丁，给模型新增了 **35 个工具**。

### 1.1 目录结构（就这么多）

```
my-plugin/
├── package.json
├── cordis.patch.yml
└── README.md
```

### 1.2 `package.json`（逐字）

```json
{
  "name": "dsh-ouroboros",
  "version": "0.1.0",
  "description": "Mount Ouroboros (spec-first AI dev workflow engine) into DeepSeek Harness as native tools — type \"ooo interview\" or \"ooo auto\" in chat.",
  "type": "module",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/Q00/ouroboros.git",
    "directory": "integrations/dsh-plugin"
  },
  "keywords": [
    "dsh-plugin",
    "deepseek-harness",
    "ouroboros",
    "mcp"
  ],
  "files": [
    "cordis.patch.yml",
    "README.md"
  ],
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

### 1.3 `cordis.patch.yml`（骨架；原文很长，此处保留结构最关键部分）

```yaml
# 注释可以写得很长 —— 对这个插件来说，注释就是它的"文档"
- insert:
    - id: mcp-ouroboros
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: ouroboros
        transport: stdio
        command: uvx
        args:
          # ⚠️ 主包必须写精确版本。uvx 会在启动时去索引取包并执行，写浮动规格
          #    （省略版本 / latest）等于「每次启动跑的都是当时的线上最新版」——
          #    这份配置被审阅之后，实际执行的代码仍然会变。
          #    另外注意：**上游原文只固定了辅助依赖（mcp==2.0.0），没有固定主包**。
          #    照抄上游写法时，「把版本固定住」是必须自行补上的那一步。
          #    下面的 1.4.0 是占位，请换成你核对过的精确版本。
          - --from
          - 'ouroboros-ai[mcp]==1.4.0'
          - --with
          - 'mcp==2.0.0'
          - ouroboros
          - mcp
          - serve
        # ⚠️ 下面列出的每个凭据，都会被上面那个「运行时下载下来的子进程」读到，
        #    且它以 DSH 同等权限运行（可读写文件、可发网络请求）。
        #    优先用低配额、可随时撤销的专用 key，不要用通用主 key。
        env:
          OUROBOROS_LLM_BACKEND: !!js process.env.OUROBOROS_LLM_BACKEND ?? ''
          OUROBOROS_AGENT_RUNTIME: !!js process.env.OUROBOROS_AGENT_RUNTIME || 'host'
          DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY ?? ''
        toolCallTimeoutMs: 1800000
        failOnStartupError: false
```

### 1.4 逐行讲解（4 个必抄点）

| 位置 | 为什么必须这样写 |
|---|---|
| `"type": "module"` | 必须 |
| `files` 里有 `cordis.patch.yml` | 🔥 **漏了它，发布后补丁文件不会进 npm 包，插件装上有警告、功能全无** |
| `dsh.bundle.patch` | 🔥 **少了它，`dsh plugin add` 会打那条 `declares no dsh.bundle` 警告，然后什么都不做** |
| 没有 `main`/`exports`/`dependencies` | 零代码包本来就没有 JS 入口 —— 这是它和普通包的显著差异 |

### 1.5 附带学到的 4 条硬知识（都来自原文注释）

1. **`!!js` 可以写在 `config:` 内部**（`env:` 里就用了）。
2. 🔥 **子进程环境会被"清洗"**：`@deepseek-ai/dsh-subprocess` 会把**凭据形状的名字**（正则 `/KEY|PASSWORD|SECRET|TOKEN/i`）**和所有 `DSH_*`** 从父环境里删掉。**你要传的凭据必须显式列在 `env:` 里**。
   原文：`hands mcp-client a scrubbed parent env with every credential-shaped name (/KEY|PASSWORD|SECRET|TOKEN/i) and every DSH_* name removed`
3. 🔥 **后面的层"替换"整段 `config`，不做深合并** —— 覆盖时必须**把整个 config 重述一遍**。
   原文：`restating the whole config, since a later layer replaces a row's config rather than deep-merging it`
4. **`failOnStartupError: false` = 软失败**：没装依赖的机器也能正常启动 DSH，其它插件照常工作。但**软失败不等于自动恢复**。
   原文：`Recovery is not guaranteed to be automatic — whether mcp-client retries at all depends on the dsh build`

### 1.6 安装

```bash
dsh plugin --profile web add ./my-plugin     # 本地目录
dsh plugin --profile web add dsh-my-plugin   # 已发布到 npm
```

### 1.7 ⚠️ 边界（诚实说清）

T1 **只能挂载别人已有的能力**（如 MCP server）。要给模型加**你自己写的新工具**，去 T3。

### 🤖 让 AI Agent 帮你做 T1

```
我要做一个 DSH 插件，它不做别的，只把 <外部工具/MCP server> 挂进 DSH。
请帮我写这个插件的三个文件：package.json、cordis.patch.yml、README.md。

要求：
1. package.json 必须有 "type":"module"、"files" 包含 cordis.patch.yml、
   "dsh":{"bundle":{"patch":"./cordis.patch.yml"}}。
2. cordis.patch.yml 用 "- insert:" 列表，具体怎么配 <外部工具> 请先查
   <外部工具的官方文档/GitHub>，不要猜参数名。
3. 所有需要传给子进程的凭据，必须在 config.env 里显式列出（用 !!js process.env.X ?? ''）。
4. 加 failOnStartupError: false，让依赖缺失时也能启动 DSH。

铁律：每个配置字段都要说出出处（文档链接或仓库文件路径）。查不到的字段不要编。
```

---

## T2 · 组合包与 `cordis.patch.yml` 语法详解 ★★

**它是什么**：把 T1 的补丁文件语法彻底讲清。官方自己最核心的包 `@deepseek-ai/dsh-base` 就是一个纯配置组合包。
**来源**：官方 `packages/bundle/base/`。

### 2.1 官方纯配置包的 `src/index.ts`（全文，就 9 行）

```ts
/**
 * @deepseek-ai/dsh-base — the shared dsh core as a profile bundle. The
 * package's substance is `cordis.patch.yml`, declared by the `dsh.bundle.patch`
 * manifest field and resolved by the profile composer through that field;
 * this module carries no runtime API.
 * @module @deepseek-ai/dsh-base
 */

export {}
```

> 官方注释说得很直白：**这个包的实质是 `cordis.patch.yml`，这个模块不承载任何运行时 API。**

### 2.2 补丁行的完整字段表

| 字段 | 必填 | 含义 |
|---|---|---|
| `id` | ✅ | 行标识。**后续层靠它覆盖该行**（逐行 last-write-wins）。**全局唯一** —— ⚠️ 0.1.6-alpha.1 起重复不再报错，而是**后者静默覆盖前者** |
| `name` | ✅ | 包名。可以指向子路径，如 `@deepseek-ai/dsh-tool-subagent-control/list-agents`。**也可以写相对路径**（见 2.5） |
| `disabled` | ❌ | `true` 关闭该行；支持 `!!js` 表达式 |
| `config` | ❌ | 传给插件的配置对象。**覆盖时整段替换，不合并** |

### 2.3 `!!js` 内联表达式（官方原文用法）

```yaml
    - id: session-persistence-jsonl
      name: '@deepseek-ai/dsh-session-persistence-jsonl'
      config:
        root: !!js dshHomePath('sessions')

    - id: sandbox-policy
      name: '@deepseek-ai/dsh-sandbox-policy'
      config:
        mode: !!js process.env.DSH_PERMISSION_MODE ?? 'workspace-write'
        workspaceRoot: !!js process.cwd()

    # 🔥 跨平台标准写法：官方就这么处理 bash/pwsh 的平台差异
    - id: bash-sandbox
      name: '@deepseek-ai/dsh-bash-sandbox'
      disabled: !!js process.platform === 'win32'
      config:
        timeoutMs: 60000

    - id: pwsh-sandbox
      name: '@deepseek-ai/dsh-pwsh-sandbox'
      disabled: !!js process.platform !== 'win32'
```

**`!!js` 的求值范围（官方复盘 0002 的教训，必须记牢）**：

| 位置 | `!!js` 是否被求值 |
|---|---|
| `config:` 内部的任何值 | ✅ 会 |
| entry 的 `disabled:` | ✅ 会（当前版本） |
| **其它任何 entry 元数据**（如 `id`、`name`） | ❌ **不会**，必须写字面量 |

> ⚠️ 写在不会求值的位置**不报错**，只是**静默失效** —— 这是复盘 0002 整整一个事故的根因。

### 2.4 五条铁律（都有官方原文或复盘背书）

| # | 铁律 | 依据 |
|---|---|---|
| 1 | **行的书写顺序不影响加载顺序** —— 激活由「服务可用性」驱动，不是顺序 | 官方 base 补丁注释：`Row order carries no load semantics (activation is service-availability driven)` |
| 2 | `config` 是**整段替换**，不是深合并 | 同上：`A patch replaces the targeted row's whole config rather than merging into it` |
| 3 | `!!js` 的**可见范围**是「同一补丁内、它之前的行」 | `omdsh-dev/DSH-better-sidebar` 补丁注释：`only rows before this one are visible` |
| 4 | 同一个 `id` 重复 → **0.1.6-alpha.1 起静默覆盖**（后者胜），不再崩溃 | 见 `05-pitfalls.md` 坑 P3 |
| 5 | 补丁文件**顶层是单个数组**（一个 `- insert:`），不要写成两个顶层值 | 见 `第三篇 · 坑 P3` |

### 2.5 相对路径 `name` 的真相（官方文档自相矛盾，以源码为准）

官方文档 `user/develop/basic/index.zh.md:56` 说插件路径「必须是绝对路径」。
但源码 `packages/boot/app-boot/src/index.ts` 的 `anchorInsertedPluginNames()` 明确把相对路径**锚定到补丁文件旁边**：

```ts
const base = dirname(resolve(file))
entry.name = pathToFileURL(resolve(base, entry.name)).href
```

**结论**：**写相对路径是可行的**（且有单元测试固定该行为）。但为了可移植，第三方插件建议用**包名**（`@scope/name`），而不是相对路径。

---

## T3 · 工具插件 · `defineTool`（让模型调用你的能力）★★

**它是什么**：给模型加一个可调用的工具。**这是"外部调用方向"的主力形态。**
**来源**：官方 `packages/interaction/tool-ask-user`（官方**最小**的工具插件，全包 101 行）。完整全文见本文件**附录 E 的官方模板 3**。

> 🔴 **前提（`0.2.2-alpha.2` 起）**：**注册工具 ≠ 工具可执行。** 执行由**独立的执行器插件**承担 —— 官方 base 补丁挂的是 `@deepseek-ai/dsh-tool-executor-native`（PTC 是另一个插件，默认 `disabled: true`）。
> **自建组合若一个执行器都没挂**，`ctx.tools` 在选择执行器时直接抛 `ToolExecutorUnavailableError`（`packages/core/tools/src/index.ts:365`、`packages/core/tools/src/executor.ts:97`）；同理，`dsh-tools` 的 `Config` 里 `mode` 与 `maxParallelSubCalls` 已是 `z.never()` 占位（`:101-104`），**在 patch 里写这两个键会被拒**。
> 内置 profile（default / web / headless / sdk）都已挂执行器，所以下面这段代码在任何官方 profile 里可直接跑。判据：`docs/upgrade-guide/v0.2.1-rc.2/tool-executor-plugins/guide.zh.md`。

### 3.1 完整骨架（逐字，可直接抄）

```ts
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'
import '@deepseek-ai/dsh-user-questions'

export const name = 'tool-ask-user'
export const inject = ['tools', 'userQuestions']

const description = 'Ask the user a concise question when you need confirmation, a choice, or missing information before proceeding. '
  + 'Send one or more questions, each with a stable id that will be echoed in the answer.'

export function apply(ctx: Context): void {
  ctx.tools.register(defineTool({
    name: 'ask_user_question',
    description,
    parameters: {
      questions: {
        type: 'array',
        required: true,
        description: 'Questions to ask the user before continuing.',
        items: {
          type: 'object',
          additionalProperties: true,
          properties: {
            id: { type: 'string', required: true, description: 'Stable id for this question; echoed in the answer.' },
            question: { type: 'string', required: true, description: 'The specific question to ask the user.' },
          },
        },
      },
    },
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
    async execute(args, exec) {
      // 业务逻辑；exec.signal 是取消信号，exec.agent 是当前 agent
      const result = await ctx.userQuestions.ask({ /* ... */ signal: exec.signal })
      return { /* 返回值必须匹配 output.schema */ }
    },
  }))
}
```

### 3.1b 🆕 条件工具：`register(definition, { when })`（`0.2.2-alpha.2` 起）

**什么时候用**：工具只在某些步骤才有意义（例如只在计划模式下、只在某个模型下、只在某个 provider 可用时）。**不要再用 `system-prompt/assemble` 去筛工具 —— 那条路已经断了**（`0.2.2-alpha.2` 起该 waterfall 不再携带工具数组，返回的 `tools` 被忽略、`assembly.tools` 为 `undefined`，见 `05-pitfalls.md` 坑 P24）。

```ts
ctx.tools.register(defineTool({ /* … */ }), {
  // 每个拟议步骤计算一次；可同步可异步
  when: ({ agent, modelSelection, signal }) => modelSelection.model.includes('pro'),
})
```

- 判据来源：`packages/core/tools/src/contracts.ts:105-126`（`ToolActivationContext` = `{ agent, modelSelection, signal }`，`ToolRegistrationOptions.when`）。
- 返回 `false` → 工具从**声明 / 原生分发 / PTC 绑定 / 嵌套调用**四处一并移除；条件抛错 → 轮次以 `TOOL_ACTIVATION_FAILED` 结束；不属于已准入集合的调用返回 `UNKNOWN_TOOL` 且**不执行**。
- ⚠️ **步骤中途重新注册工具**（热重载 / MCP 重连 / skill 重载）会让该步骤内**尚未开始**的调用失败 —— 不要在一步之内反复注册同一个工具名。

### 3.2 🔥🔴 最重要的一课：`required` 有**两套写法**，混用必报错

DSH 有**两条**注册工具的路径，`required` 的位置**正好相反**：

| 注册方式 | `parameters` 是什么 | 必填怎么写 | 写错的后果 |
|---|---|---|---|
| **`defineTool({...})`**（官方自研插件全走这条，**新手推荐**） | **DSH 作者 DSL** | **属性级** `required: true` | 写对象级 `required: ['a']` → 报 `parameters.a.required must be true when present` |
| **裸 `ctx.tools.register({...})`**（社区插件常走） | **原始 JSON Schema** | **对象级** `required: ['a']` | 写属性级 `required: true` → 报 `required must be an array of strings` |

**证据（官方源码 `packages/core/tools/src/schema.ts`）**：

```ts
// 第 96-106 行
/** One implicit parameter-root property, optionally required. */
export type ParameterPropertySpec = ValueSchemaSpec & { required?: true }

/**
 * Tool parameter schema. The map itself is an implicit open object root;
 * requiredness remains a per-property `required: true` annotation.
 */
export type ParameterSchemaSpec = {
  [key: string]: ParameterPropertySpec
  [key: symbol]: never
}
```

```ts
// 第 570-571 行（defineTool 实现体内）
const parameters = parameterSchemaSpecToJsonSchema(options.parameters)
const outputSchema = valueSchemaSpecToJsonSchema(options.output.schema)
```

```ts
// 第 292-295 行（属性级 required 被收集成对象级数组）
if (Object.hasOwn(task.property, 'required') && task.property.required !== true) {
  authorError(`${task.path}.required must be true when present`)
}
if (Object.hasOwn(task.property, 'required') && task.property.required === true) task.required.push(task.key)
```

**三句话记住**：
1. 走 `defineTool` → `parameters` 的根是**隐式对象**，直接铺字段名，**不写** `type:'object'`/`properties` 包装。
2. 走 `defineTool` → 必填一律**属性级** `required: true`。
3. **`output.schema` 走 `defineTool` 时也是同一套 DSL**，同样用属性级 `required: true`；且它的**根节点不允许 `required`**。

> ⚠️ 这条之所以要单独强调：社区里有真实仓库（如 `yjh051108/dsh-routing-suite`）在注释里留下"血泪坑：属性级一律不允许 required 键"——那个结论**只对裸 `register` 路径成立**。照抄到 `defineTool` 上会直接报错。

### 3.3 `parameters` DSL 支持的类型

```
'string' | 'number' | 'integer' | 'boolean' | 'null' | 'array' | 'object' | 'json'
或者用 oneOf（需 ≥2 个分支，且不能与 type 同时声明）
```

官方报错原文（`schema.ts:411`）：
```
${path}.type must be string/number/integer/boolean/null/array/object/json, or use oneOf
```

### 3.4 字段速查

| 字段 | 说明 |
|---|---|
| `name` | 模型看到的工具名，下划线风格（`ask_user_question`） |
| `description` | **极重要**：模型靠它决定是否调用，要写"**什么时候用**" |
| `parameters.<x>.type` | 见 3.3 |
| `parameters.<x>.required` | `true`（属性级） |
| `parameters.<x>.description` | 逐字段描述，模型靠它填参 |
| `parameters.<x>.items` | 数组元素 schema |
| `parameters.<x>.properties` + `additionalProperties` | 对象字段 schema |
| `output.schema` | 返回值结构约束 |
| `output.render` | `(args, value) => [{type:'text', text}]`，渲染成模型可读内容 |
| `execute` | `async (args, exec) => result`；`exec.signal` 取消信号、`exec.agent` 当前 agent |
| `timeoutMs` | 可选，正有限数（写 0 或负数会抛 `timeoutMs must be a positive finite number`） |
| `isConcurrencySafe` | 可选，`() => true` 表示只读可并发 |

### 3.5 ⚠️ 三条易错点

1. **`output.schema` 必须描述返回值结构** —— 模型看到的是它。忘了写或写错，模型会困惑。
2. **`execute` 返回纯数据**（可序列化 JSON）。要逐字段把 `unknown` 收窄（`typeof x === 'string' ? x : ''`），别把 `undefined`/函数/类实例丢回去。
3. **权限与审批不在工具里声明**（主手册 4.7 已讲）。工具只管"能做什么"，"允不允许"由 sandbox/approval 服务管。

### 🤖 让 AI Agent 帮你做 T3

```
帮我写一个 DSH 工具插件，工具名 <tool_name>，它要做 <一句话功能>。

铁律（必须遵守，否则代码跑不起来）：
1. 用 defineTool()，从 '@deepseek-ai/dsh-tools' 导入。
2. 具名导出 name / inject / apply，绝对不要写 export default。
3. parameters 用 DSH 的 Schema DSL：
   - 根是隐式对象，直接写字段名，不要写 type:'object'/properties 包装
   - 必填写在属性级：{ type:'string', required: true, description:'...' }
4. output.schema 描述返回值结构，output.render 返回 [{type:'text', text}]。
5. execute 只返回纯数据，逐字段把 unknown 收窄。
6. inject 里写上你依赖的服务名。

请先告诉我：这个工具应该 inject 哪些服务？依据是什么（哪个官方包的 inject 里有类似服务）？
```

---

## T4 · 工具插件 · 手写 `ToolDefinition`（进阶备选）★★

**它是什么**：绕过 `defineTool`，直接手写 `ToolDefinition` 对象注册。社区插件常用这条路。
**来源**：`Tencent/WeKnora → packages/dsh-weknora/src/tools.ts`（腾讯开源，4 个只读工具，**最干净的社区范本**）。

### 4.1 写法对比（关键差异就一处）

```ts
// 路径 B：先构造 ToolDefinition 数组，再统一注册
const definitions: ToolDefinition[] = []

definitions.push({
  name: name('list_knowledge_bases'),
  description: '...',
  // ⚠️ 这里是【原始 JSON Schema】，不是 DSH DSL
  parameters: { type: 'object', properties: {}, additionalProperties: false },
  timeoutMs: config.requestTimeoutMs,
  isConcurrencySafe: () => true,
  output: {
    schema: {
      type: 'object',
      properties: {
        count: { type: 'integer' },
        knowledge_bases: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              id: { type: 'string' },
              name: { type: 'string' },
              description: { type: 'string' },
            },
            // ⚠️ 对象级 required 数组
            required: ['id', 'name', 'description'],
            additionalProperties: false,
          },
        },
      },
      required: ['count', 'knowledge_bases'],
      additionalProperties: false,
    },
    render: (_args, value) => { /* 返回文本块 */ },
  },
  async execute(_args, exec) {
    const bases = await client.listKnowledgeBases(exec.signal)
    return {
      count: bases.length,
      knowledge_bases: bases.map(kb => ({
        id: typeof kb.id === 'string' ? kb.id : '',
        // ...
      })),
    }
  },
})
```

带参数的例子（对象级 `required`）：

```ts
  parameters: {
    type: 'object',
    properties: {
      query: { type: 'string', description: 'Natural-language query; a full question retrieves better than keywords.' },
      knowledge_base_ids: { ...STRING_ARRAY, description: 'Restrict the search to these knowledge base ids.' },
      max_results: { type: 'integer', description: 'Maximum passages to return.' },
    },
    required: ['query'],
    additionalProperties: false,
  },
```

### 4.2 两条路怎么选

| | 路径 A `defineTool` | 路径 B 手写 `ToolDefinition` |
|---|---|---|
| 参数校验 | **自动**（`validateJsonSchemaValue`） | 自己保证 |
| 类型推导 | 有（`InferArgs<S>`） | 无 |
| 报错友好度 | 高 | 低 |
| 写法 | DSH DSL | 标准 JSON Schema |
| **推荐** | ✅ **新手一律走这条** | 想要零运行时依赖时才用（见 4.3） |

### 4.3 路径 B 唯一的真实优势：**零依赖**

WeKnora 的做法有一个值得学的技巧：它**不 import 任何 DSH 内部包**，而是手写一份"自己用到的接口"的类型镜像（`src/harness.ts`）。好处是：
- 不会撞上「官方装配不装 peers」的 `Cannot find package '@deepseek-ai/dsh-tools'` 报错（见坑 P18）；
- 不随 DSH 升级被迫重新发布；
- **代价**：DSH 大改字段时编译不报错，要靠 e2e 测试兜底。

---

## T5 · 命令插件（给人用的 `/斜杠命令`）★★

**来源**：官方 `packages/feedback/command-feedback`（提供 `/feedback` 命令）。

### 5.1 核心注册代码（逐字）

```ts
import { CommandDefinitionId } from '@deepseek-ai/dsh-commands/brand'
import type { CommandInvocation, CommandResult } from '@deepseek-ai/dsh-commands'

export const name = 'command-feedback'
export const inject = ['commands']

const USAGE = 'Usage: /feedback <text>'

function executeFeedbackCommand(invocation: CommandInvocation): CommandResult {
  if (invocation.rawInput.trim().length === 0) {
    return { kind: 'error', text: `Feedback text is required. ${USAGE}` }
  }
  recordFeedback(invocation.agent.session, { text: invocation.rawInput })
  return {
    kind: 'success',
    text: `Feedback recorded for session ${invocation.agent.session.id}`,
  }
}

export function apply(ctx: Context): void {
  ctx.commands.register({
    definitionId: CommandDefinitionId('@deepseek-ai/dsh-command-feedback'),
    name: 'feedback',
    description: 'Record feedback about this session',
    input: { hint: '<text>' },
    recordInput: false,
    handler: executeFeedbackCommand,
  })
}
```

### 5.2 参数速查

| 字段 | 值 | 说明 |
|---|---|---|
| `definitionId` | `CommandDefinitionId('@scope/pkg')` | 品牌化 id，**必须用 `CommandDefinitionId()` 包装** |
| `name` | `'feedback'` | 用户敲的 `/feedback` |
| `description` | `string` | 斜杠菜单里显示 |
| `input` | `{ hint: '<text>' }` | 输入提示 |
| `recordInput` | `false` | 是否把输入记进会话日志 |
| `handler` | `(inv) => CommandResult` | 返回值二选一 |

**`CommandResult` 两种形态**：`{ kind: 'success', text }` / `{ kind: 'error', text }`
**`CommandInvocation` 关键字段**：`invocation.rawInput`（用户原始输入）、`invocation.agent`（当前 agent，`agent.session` 是会话）。

### 5.3 命令 vs 工具

| | 命令 Command | 工具 Tool |
|---|---|---|
| 触发者 | **人**（敲 `/xxx`） | **模型**（自动决定调用） |
| 注册 API | `ctx.commands.register({...})` | `ctx.tools.register(defineTool({...}))` |
| 依赖服务 | `inject = ['commands']` | `inject = ['tools', ...]` |
| 典型用途 | 开关模式、导出、清空、反馈 | 读写文件、搜索、调外部 API |

### 5.4 官方内置的 6 个命令（可作范本）

`/compact`、`/feedback`、`/goal`、`/permission`、`/plan`、`/export`

---

## T6 · 可配置插件（让用户不改代码就能调参）★★

**来源**：官方 `packages/context/time-context`（schemastery 路线）+ `packages/plan/plan-mode`（手写校验路线）。

### 6.1 路线一：`export const Config = z.object({...})`（推荐给新手）

```ts
import z from '@deepseek-ai/schemastery'

/** The agent registry that owns pre-step processing. */
export const inject = ['agents', 'sessionProjections']

/** Request-preparation clock formatting and append scheduling. Invalid values fail plugin load. */
export interface Config {
  /** Fallback display zone when the open turn has no unique browser zone. Omit to use the process zone. */
  timeZone?: string
  /** Minimum milliseconds between durable injections in one session. Omit or set to 0 to inject at every eligible step. */
  refreshIntervalMs?: number
}

/** Schemastery validation for {@link Config}. */
export const Config: z<Config> = z.object({
  timeZone: z.string(),
  refreshIntervalMs: z.number(),
})
```

**机制（新手必须懂）**：
- 同一个名字 `Config` 既导出 **TypeScript 接口**，又导出**运行时校验器**（接口与值同名共存）。
- DSH 的加载器看到插件导出的 `Config`，就把它当作 schema，对 `cordis.patch.yml` 里该行的 `config:` 做校验。
- 校验失败 → **插件加载失败**（官方注释原文：`Invalid values fail plugin load.`）。

### 6.2 路线二：手写 `resolveConfig()`（想要"人话报错"时）

```ts
export interface PlanModeConfig {
  /** Guidance rendered as the `plan:policy` prompt section while plan mode is active. */
  section: string
}

export function resolveConfig(config: PlanModeConfig): PlanModeConfig {
  const section = (config as Partial<PlanModeConfig>).section
  // 校验：必须是字符串、非空、且不能有未知键
  throw new Error(`PlanModeConfig has unknown key(s) ${unknown.join(', ')} — config is { section }`)
}
```

> 🔥 这行报错是**教科书级范本**：说清"错在哪"+"期望是什么"。写自己的配置校验时照这个格式抄。

### 6.3 两路线取舍

| | `export const Config = z.object({...})` | 手写 `resolveConfig()` |
|---|---|---|
| 代码量 | 少 | 多 |
| 报错信息 | 库自动生成 | **可以写得非常人话** |
| 适用 | 新手首选 | 想"教会用户怎么配"的场景 |

---

## T7 · 服务插件（给别的插件提供能力）★★★

**来源**：官方 `packages/storage/storage/src/index.ts`（98 行，官方最小服务包）。

### 7.1 🔴 先记最重要的一条：服务插件与函数式插件**导出形式相反**

```ts
// ✅ 服务包：default export 服务类
export default MyService

// ✅ 函数式插件：具名导出 name/inject/apply，绝对没有 default export
export const name = '...'
export const inject = [...]
export function apply(ctx) { ... }
```

**混用会怎样**（官方复盘 0001，真实事故）：
- 官方原文：`service packages default-export their service class; function plugins named-export name / inject / Config / apply and have no default export. Mixing the forms makes the Loader discard the function plugin's namespace.`
- 事故现场：一个多余的 `export default apply` 让 Loader **丢弃了整个命名空间**（`inject`/`name`/`Config` 全丢），插件加载时崩在 `Internal error: cannot get property "agents" without inject`。**178 个绿灯单元测试、100% 行覆盖率，一个都没抓到。**

### 7.2 官方服务插件完整模板（逐字）

```ts
import { Context, Service } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context {
    storage: Storage        // ← 声明合并：让 ctx.storage 有类型
  }
}

export class Storage extends Service {
  readonly backend: BackendRegistry = new BackendRegistry()
  private readonly forms = new Map<keyof StorageForms, unknown>()

  constructor(ctx: Context) {
    super(ctx, 'storage')   // ← 服务名（ctx.storage）
  }

  mount<K extends keyof StorageForms>(form: K, facility: StorageForms[K]): () => void {
    if (this.forms.has(form)) {
      throw new StorageError('duplicate-mount', `storage form '${String(form)}' is already mounted`)
    }
    this.forms.set(form, facility)
    // 🔥 返回 disposer：卸载时清干净
    return () => {
      if (this.forms.get(form) === facility) {
        this.forms.delete(form)
      }
    }
  }
}

// Service packages default-export their service class and nothing else
// plugin-shaped (packages/AGENTS.md): mixing a default export with a
// function-plugin `apply` makes the Loader drop the plugin namespace.
export default Storage
```

**挂了之后在 `apply` 里启动它**：

```ts
export function apply(ctx: Context): void {
  ctx.plugin(SessionFeedbackService)   // ← 官方 command-feedback 的写法
}
```

### 7.3 社区的另一条路：函数式插件 + `ctx.provide`

**重要事实**：本次调研的社区插件（MemOS / loopx / archify / better-sidebar 等）**没有一个用 `extends Service`**。它们统一是：

```ts
export const name = 'my-plugin'
export const inject = ['...']
export function apply(ctx: Context, config: Config): void {
  // ① 发布一个服务
  ctx.provide('myServiceName', someValue)      // 官方 ThemeRuntime 的写法
  // 或 ctx.reflect.provide('myServiceName', someValue)   // loopx 的写法
  // ② 类只是普通 class，不继承任何基类
  // ③ 生命周期靠 ctx.effect 返回 disposer 接管
}
```

**两条路都真实存在**，选择建议：

| | `export default class extends Service`（官方） | 函数式 + `ctx.provide`（社区） |
|---|---|---|
| 适合 | 在官方 monorepo 里贡献、要做完整能力 seam | 第三方插件、单个服务 |
| 优点 | Loader 原生生命周期管理、`static inject` 声明 | 与函数式插件同构，好写 |
| 证据 | 官方 `packages/storage`、`packages/skill` | MemOS、loopx、archify |

### 🤖 让 AI Agent 帮你做 T7

```
我要写一个 DSH 服务插件，服务名 <xxx>，能力是 <一句话>。

请严格按官方 packages/storage/storage/src/index.ts 的形态写：
1. export class Xxx extends Service，constructor 里 super(ctx, '<服务名>')
2. declare module '@deepseek-ai/cordis' { interface Context { xxx: Xxx } }
3. 所有"注册型"方法必须返回 disposer，并且要有"陈旧 disposer 守卫"
4. 文件末尾 export default Xxx（服务包必须 default export）
5. 绝对不要在同一个文件里再写 export function apply

另外告诉我：装了这个服务之后，别人应该在 inject 数组里写什么字符串？
```

---

## T8 · 最小 UI 插件 + 插槽机制 ★★★

**来源**：官方 `packages/client/ui-brand-official`（全包 49 行，官方最小的 UI 插件）。
**完整原文见**本文件**附录 E 的官方模板 2**。

### 8.1 一个 UI 插件 = 两个半侧

```
my-ui-plugin/
├── package.json
├── tsconfig.json          # extends tsconfig.base.client.json（注意是 client 版）
├── tsdown.config.ts
└── src/
    ├── index.ts           # 宿主半侧（node 侧）—— 可以是空的
    └── client/
        ├── index.ts       # 客户端半侧（浏览器侧）—— 真正的 UI 逻辑
        └── MyWidget.tsx   # React 组件
```

### 8.2 `package.json` 的四个关键点（逐字）

```json
{
  "exports": {
    ".": { "types": "./lib/types/index.d.ts", "default": "./lib/index.js" },
    "./client": { "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" },
    "./src/*": "./src/*",
    "./package.json": "./package.json"
  },
  "dsh": {
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-ui-renderer",
        "@deepseek-ai/dsh-client-ui-sidebar"
      ],
      "platform": "web"
    }
  },
  "files": ["lib/index.js", "lib/client.js", "lib/types/**/*.d.ts"]
}
```

| # | 关键点 | 漏了会怎样 |
|---|---|---|
| 1 | `exports["./client"]` 指向 `lib/client.js` | 🔥 **客户端半侧根本不会被加载** |
| 2 | `dsh.client.inject` 声明依赖的**包名**数组 | 组装失败 |
| 3 | `dsh.client.platform: "web"` | — |
| 4 | `files` 含 `lib/client.js` | 发布后 UI 半侧丢失 |

### 8.3 宿主半侧可以完全是空的（逐字）

```ts
/**
 * Official browser-brand plugin, node half. The empty apply gives Loader a
 * host-side row while the browser half ships through `exports["./client"]`.
 */

/** Host plugin body — this package contributes browser presentation only. */
export function apply(): void {}
```

> 🔑 **纯 UI 插件的宿主半侧空实现就够了** —— 这是标准形态，不是偷懒。

### 8.4 客户端半侧 + 插槽（逐字）

```ts
import type { Context as ClientContext } from '@deepseek-ai/cordis'
import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'
import type {} from '@deepseek-ai/dsh-client-ui-sidebar/client'
import { OfficialBrandMark, OfficialBrandName } from './Brand.tsx'

/** Required service: the UI slot registry. */
export const inject = ['slots']

export function apply(ctx: ClientContext): void {
  ctx.slots.inject('sidebar.brand.mark', () =>
    ctx.slots.inject('sidebar.brand.name', function* () {
      yield ctx.slots.register({ name: 'sidebar.brand.mark' }, OfficialBrandMark)
      yield ctx.slots.register({ name: 'sidebar.brand.name' }, OfficialBrandName)
    }))
}
```

**三个必记点**：
1. `export const inject = ['slots']` —— 声明依赖 **slots 服务**。
2. `ctx.slots.inject('<插槽名>', () => ...)` —— 往插槽注入；**返回 disposer**。
3. `ctx.slots.register({ name: '<插槽名>' }, 组件)` —— 注册组件；**返回 disposer**。

> 🔥 **`inject` 的两层含义**（新手最容易混）：
> - `package.json` 的 `dsh.client.inject` 是**包级依赖**（字符串包名），决定加载顺序。
> - 代码里的 `export const inject = [...]` 是**服务级依赖**（服务名），决定 `apply` 何时被调用。

### 8.5 最常用的三个插槽名（**先记住这三个**）

| 插槽名 | 用途 |
|---|---|
| `settings.section` | 加一整段设置页 |
| `settings.general.item` | 通用设置里加一行/一项 |
| `conversation.view` | 替换对话主视图（最激进） |

> ⚠️ 基线时本手册说这里有「40 个官方插槽名」——**那是低估**。对基线 `dsh-v0.2.2-alpha.2` 重新抽取：声明侧 **148 个键**、并集 **150** 个，剔除 **44** 个测试专用键后**约 106 个公开可用**（**2026-09-23 修好抽取器两处漏抽后重抽**；**2026-09-25 随 rc.2 推进 +3 / −0**；**2026-09-29 随 0.2.0-rc.1 推进 +0 / −0**；**2026-09-30 随 0.2.0-rc.2 推进 +1 / −0**；**2026-10-04 随 0.2.1-alpha.1 推进 +2 / −0**；**2026-10-09 随 0.2.1-alpha.2 推进 +2 / −0**；**2026-10-15 随 0.2.1-alpha.3 推进 +5 / −1**（新增 `conversation.chat.message.images` / `conversation.chat.user.images` / `conversation.hero.options` / `conversation.user.text.node` / `workspace.toast`，**旧键 `conversation.message.images` 改名走掉**）；**2026-10-16 随 0.2.1-alpha.4 推进 +1 / −0**（`slot-catalog.ts` **98 → 99**；新增键 = `plugins.tab`）；**2026-10-17 随 0.2.1-rc.2 推进 +1 / −0**（`slot-catalog.ts` **99 → 100**；新增键 = `conversation.input.model.label`）；**2026-10-24 随 0.2.1-rc.3 推进 +3 / −0**（`slot-catalog.ts` **100 → 103**；新增键 = `conversation.session.header.views.actions` / `sidebar.panellist.actions` / `sidebar.right.tab.guide.actions`）；**2026-10-29 随 0.2.2-alpha.2 推进 +3 / −0**（`slot-catalog.ts` **103 → 106**；新增键 = `conversation.chat.text-interaction` / `conversation.chat.user.before` / `sidebar.session.row.trailing`）；此前公布的 96/99/约81 系低估）。
> 完整清单与可复现命令：`<skill>/scripts/extract_slots.py <DSH仓库路径> <skill目录>`；签名与报错见 `14-inbound-http-and-timers.md` §17.4，那份是权威。

### 8.6 🔴 UI 插件的三条硬约束

1. **`dsh.client` 与 `exports["./client"]` 必须成对存在**。缺任一个，宿主报 `client package failed to compose`。
2. **浏览器半侧里 `@deepseek-ai/*` 只能写 `import type`**。要用值只允许**平台种子表**里的 9 个 specifier（全名，`packages/client/web/src/platform.ts:8-14`）：
   `react`、`react/jsx-runtime`、`react-dom`、`react-dom/client`、`@deepseek-ai/cordis`、`@deepseek-ai/dsh-client-store`、`@deepseek-ai/dsh-client-ui-slots`、`@deepseek-ai/dsh-client-ui-primitives`、`@deepseek-ai/dsh-client-ui-dockkit`；
   个别包另有需要的，在 `dsh.client.external` 里**精确**追加。越界报：
   ```
   client bundle purity: "..." is not in the default client externals or <id>'s
   dsh.client.external, an inline-safe wire layer, or a generated /remote contribution
   ```
   （运行时层面的旧报错文案是 `client-modules: require("...") missed the module table …`——两道门禁，构建期与运行期各一道。）
3. **不要 `import` 别人的实现**。跨插件协作走 **cordis 服务**（`ctx.slots`/`ctx.sessions`/`ctx.workspaces`）或**插槽**。

### 8.7 样式方案（事实，不猜测）

- **CSS Modules**：`import css from './X.module.css'`
- 全局语义 token 用 `--dsw-alias-*`（**明暗两套都要给**）
- **不要**假设能用 Tailwind

**官方为"只给了一个值"写的教学式报错（逐字，值得学）**：

```ts
throw new TypeError(
  `theme override "${name}" from "${source}" is a bare string — pass { light: ${JSON.stringify(value)}, dark: ${JSON.stringify(value)} } `
  + '(repeat the value when it is the same in both palettes); a single value goes illegible when the user switches color scheme',
)
```

### 🤖 让 AI Agent 帮你做 T8

```
我要给 DSH 的网页界面加一个 <位置描述> 上的 <控件描述>。

请按官方 packages/client/ui-brand-official 的形态写（这是官方最小的 UI 插件）：
1. package.json 必须有 exports["./client"] 和 dsh.client（inject 写包名数组、platform:"web"），
   files 必须含 lib/client.js。
2. 宿主半侧 src/index.ts 可以是 export function apply(): void {} 空实现。
3. 客户端半侧 src/client/index.ts：export const inject = ['slots']，
   用 ctx.slots.inject('<插槽名>', () => ctx.slots.register({ name: '<插槽名>' }, 组件))。
4. 组件用 React + CSS Modules；浏览器半侧里 @deepseek-ai/* 只能 import type。

请先回答：我应该用哪个插槽名？请从源码里的 SlotMap 声明中找（别猜），并说明依据。
```

---

## T9 · 设置卡片（在设置界面里加一张卡）★★★

**来源**：官方 `packages/client/ui-theme`（它自己就是一个"主题设置"插件）。

### 9.1 `dsh.client` 要加 `immediately`

```json
  "dsh": {
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-connection",
        "@deepseek-ai/dsh-client-locale",
        "@deepseek-ai/dsh-client-ui-renderer",
        "@deepseek-ai/dsh-client-ui-settings",
        "@deepseek-ai/dsh-api-remotes"
      ],
      "platform": "web",
      "immediately": true
    }
  }
```

> `immediately: true` = **立刻加载**（不等别人按需触发）。设置类插件通常需要。

### 9.2 宿主半侧：用 `Config` 声明你的设置（🔴 已按 `0.2.0-rc.2` 重写）

> 🔴 **本小节在 `0.2.0-rc.2` 轮被重写**：旧版教的是 `ctx.get('settings')` + `settings.register(ns, Schema)`，
> 这两个入口**在 `0.1.7-rc.1` 的设置机制重做里已被移除** —— 新的 `SettingsForms` 服务面只剩
> `configure` / `prepareDocument` / `describe` / `update` / `replace` / `mutate`（逐条映射见 `04-ui-and-slots.md` §10.9）。
> 新写法在下面：**设置项就是插件的 `Config` 字段**，用 `.volatile()` 标出「允许运行时热改」。
> （来源：`packages/client/ui-theme/src/index.ts:20-46`，`dsh-v0.2.1-alpha.3` 实测；下方为**节选**，真实 `Config` 界面另有 5 个字体族字段）

```ts
export interface Config {
  preference: Volatile<ThemePreference>
  fontSize: Volatile<number>
}

export const Config = z.object({
  preference: z.union([...THEME_PREFERENCES]).default(DEFAULT_PREFERENCE).volatile(),
  fontSize: z.number().step(1).min(FONT_SIZE_MIN).max(FONT_SIZE_MAX).default(DEFAULT_FONT_SIZE).volatile(),
})

export function apply(ctx: Context, config: Config): void {
  // 只声明「本条目由我自己的表单承载」；**不再**手动 register 命名空间
  ctx.inject(['settings'], (child) => {
    child.effect(() => child.settings.configure({ auto: false }, ctx.fiber))
  })
  // 往页面 HTML 注入首屏数据，避免闪烁
  ctx.on('webserver/index-inject', (table) => {
    table.push(...bootThemeInjections(config.preference.get(), config.fontSize.get()))
  }, { prepend: true })
}
```

| API | 用法 |
|---|---|
| `Config` 里的 `.volatile()` 字段 | **热改**：运行时写入后立刻生效，不必重启插件 |
| `ctx.inject(['settings'], cb)` | 等服务就绪后再执行 `cb`（**这条仍然需要**，别写成硬依赖） |
| `ctx.settings.configure({ auto }, fiber)` | 声明本条目由**自己的**表单承载（`auto: false`） |
| `ctx.on('webserver/index-inject', ...)` | 往页面 HTML 注入行（首屏生效） |

（`SettingsForms` 的公共方法面：`packages/settings/settings/src/index.ts:266`（`configure`）/ `:296`（`prepareDocument`）/ `:302`（`describe`）/ `:348`（`update`）/ `:358`（`replace`）/ `:368`（`mutate`））

### 9.3 客户端半侧：注册到设置插槽（关键部分，已按 `0.2.0-rc.2` 更新）

> 🔴 **两处改动**（旧写法照抄会直接报「服务不存在」）：`inject` 里的客户端服务名
> **`settingsScope` → `configForms`**；取表单的那一句 **`ctx.settingsScope.bind<T>({ namespace: ns })` → `ctx.configForms.get<T>(ns)`**。
> 返回的 `ConfigForm<T>` 提供 `getSnapshot()` / `subscribe()` / `set(field, value)` / `unset(field)` / `mutate(ops, expectedRevision?)`
> （`packages/client/ui-settings/src/client/config-form-types.ts:36-74`）。
> 下面是当前上游的原文（`packages/client/ui-theme/src/client/index.ts:587,599`，`dsh-v0.2.2-alpha.2` 实测）：

```ts
export const inject = ['slots', 'locale', 'remote', 'configForms']

export function apply(ctx: ClientContext): void {
  const host = ctx.configForms.get<ThemeSettings>(THEME_SETTINGS_NAMESPACE)
  const theme = new ThemeRuntime(ctx, host)
  ctx.provide('theme', theme)

  ctx.effect(() => ctx.locale.register(SETTINGS_NS, { zh, en }), 'ui-theme: settings row dictionaries')

  const store = createAppearanceRowStore()
  let bound: BoundActions<typeof store> | undefined
  const sync = (snapshot: ThemeSnapshot): void => { bound?.sync(snapshot.preference, snapshot.revision) }
  ctx.on('theme/change', sync)

  const injected = (actions: BoundActions<typeof store>): AppearanceRowInjected => {
    bound = actions
    // 从 getter 重新同步，确保注册与首次渲染之间的改动不丢
    sync(theme.getTheme())
    return { setTheme: (id) => { theme.setTheme(id) } }
  }

  ctx.slots.inject('settings.general.item', () => ctx.slots.register({
    name: 'settings.general.item',
    id: 'appearance',
    order: 10,
    store,
    locale: SETTINGS_NS,
    inject: injected,
  }, AppearanceRow))
}
```

**`ctx.slots.register` 的完整参数**：

| 字段 | 说明 |
|---|---|
| `name` | 插槽名（`'settings.general.item'`） |
| `id` | 本注册项在该插槽内的唯一 id |
| `order` | 排序（数字小的在前） |
| `store` | 绑给组件的响应式 store（组件用 `useStore` 消费） |
| `locale` | 文案命名空间 |
| `inject` | 给组件注入"业务动作"的回调工厂 |

### 9.4 组件写法与 props 四件套（逐字）

```tsx
import type { PropsLocale, PropsRuntime, PropsStore } from '@deepseek-ai/dsh-client-ui-slots'
import css from './AppearanceRow.module.css'

/** Full component props: runtime share + store share + locale seat + injected face. */
export type AppearanceRowComponentProps =
  PropsRuntime<'settings.general.item'> & PropsStore<ReturnType<typeof createAppearanceRowStore>>
  & PropsLocale<'settings.theme'> & AppearanceRowInjected

export function AppearanceRow({ t, setTheme, useStore }: AppearanceRowComponentProps) {
  const preference = useStore(s => s.preference)
  return (
    <div className={css.group}>
      <div className={css.title}>{t('appearance.title')}</div>
      <button type="button" onClick={() => { setTheme('dark') }}>{t('appearance.dark')}</button>
    </div>
  )
}
```

**四件套**：`PropsRuntime<'插槽名'>` + `PropsStore<store 类型>` + `PropsLocale<'命名空间'>` + 自己的 `Injected` 面。

### 9.5 ⚠️ 两个真实事故（社区侧证据）

1. **把类实例的方法交给 React 当回调 → 必须 `.bind()`**
   （⚠️ **时效**：下面这个 `SettingsScope` 已在 `dsh-v0.1.7-rc.1` 被移除，本例按**通用规则**保留。）
   官方 `SettingsScope` 的 `subscribe`/`getSnapshot` 是读 `this.store` 的原型方法，React 的 `useSyncExternalStore` 会当裸函数调用，`this` 变 `undefined`，第一次 `getSnapshot()` 就抛：
   ```
   TypeError: Cannot read properties of undefined (reading 'store')
       at getSnapshot (client.js:998)
   slot entry crashed in 'settings.section'
   ```
   **修复**：`settings.subscribe.bind(settings)`（官方用 `useMemo` 保持稳定身份）。
   **通用规则**：凡是把**类实例的方法**交给 React 当回调，一律 `.bind(instance)`。闭包 store（`createSnapshotStore` 之类）不用 bind。

2. **卡片整个不渲染** → 先看崩溃日志里带的**插槽名**（`slot entry crashed in 'settings.section'`），那是第一手线索。

---

## T10 · Agent 流程拦截（改 Agent 的行为）★★★★

**它是什么**：这是用户特别关心的"**Agent 会话流程设计**"能力。DSH 把 Agent 的每一步都做成了**可拦截的 waterfall 事件**。

### 10.1 核心概念：waterfall（瀑布式事件）

```ts
ctx.on('事件名', async (payload, next) => {
  // ① await next() → 保持原样（继续走后面的监听器）
  const original = await next()
  // ② 返回替换值 → 改变流程
  return modified
  // ③ 不调 next() 就 return → 短路（官方用词：reject）
})
```

> 🔴 **铁律**：waterfall 监听器**必须** `await next()` 或 `return next()`，否则会**静默吃掉**后续所有处理 —— 而且不报错。

### 10.2 两个最关键的拦截点

#### `agent/pre-step` —— **改消息 / 拦步骤**

官方逐字文档（`docs/subsystems/core.zh.md:1046-1061`，**整节**；引文在 `:1048-1059`。旧引 `:925-950`；该文档本轮由 1125 行涨到 1200 行）：

> ```
> Reject a proposed step or replace the messages that enter it. Calling `next()` preserves the current messages.
> @param payload.agent - the agent proposing the step.
> @param payload.messages - messages removed from the inbox for this step.
> @param payload.turn - the turn that will own the step.
> @param payload.step - the step proposed by the loop.
> @param payload.signal - the current turn's cancellation signal.
> @mode waterfall
> ```

官方定位（`core.zh.md:345` 逐字）：
> `agent/pre-step` 是请求推导前**唯一**的 waterfall 监听器链。

#### `agent/request` —— **改调用配置**

官方逐字文档（`core.zh.md:1090` 附近）：
> Replace the frozen call configuration. `await next()` yields the config the machine would use (agent options on the first request, the logged header afterwards); return a replacement to switch. On step admission, this runs after assembly and `step/start`, before the system prompt and accepted user batch are committed. Cancellation here or during subsequent `prepareCall()` resolution commits neither. The prepared call capability governs prompt admission. **Model-visible content must use logged channels; this waterfall cannot mutate messages.**

### 10.3 其它可用的流程钩子

| 事件名 | 时机 / 能力 |
|---|---|
| `agent/turn-stopping` | 轮次即将结束（在最后一次 steering 排空之前） |
| `agent/request-error` | 失败请求的恢复（如触发重试） |
| `agent/assistant-stream` | 助手流式输出 |
| `llm/stream` | LLM 输出流拦截 |
| `system-prompt/assemble` | 组装 system prompt |
| `approval/request` | 审批决策（第一个应答者占唯一决策槽） |
| `compaction/*` | 上下文压缩的各阶段 |
| `tools/change` | 工具注册表变化 |

### 10.4 ⚠️ 社区真实事故：**用 system prompt 注入内容会被 persona 整段丢弃**

来自 DSH **自身机制**的坑（**官方一手源，MIT**；详见 `05-pitfalls.md` 坑 P17 与素材 B 坑 O1）：
**`agent preset` 的 persona 若声明了 `complete: true`，会丢弃其它插件贡献的 system prompt 段。**
→ 想往 system prompt 里加内容时，**先确认当前 persona 有没有 `complete: true`**。

### 🤖 让 AI Agent 帮你做 T10

```
我要拦截 DSH Agent 的 <某个环节>，做 <某件事>。

请先查阅官方仓库 docs/subsystems/core.zh.md 里这个事件的 waterfall 文档原文，
告诉我：
1. 这个事件的 payload 字段有哪些？每个字段什么含义？
2. 它是 waterfall 还是普通事件？我该不该 await next()？
3. 我的监听器返回什么类型？

然后再写代码。要求：
- 具名导出 name/inject/apply，不要 export default
- 所有注册都包 ctx.effect 并返回 disposer
- 铁律：waterfall 监听器必须 await next() 或 return next()，否则会静默吃掉后续处理
- 请在代码注释里写出你引用的官方文档路径
```

---

## T11 · 外部集成（HTTP / CLI / 协议）★★★

**两条路**：

| 路 | 做法 | 范本 | 什么时候用 |
|---|---|---|---|
| **零代码** | 对方已有 MCP server → 用 `@deepseek-ai/dsh-mcp-client` 挂 | **T1**（ouroboros） | **首选**，不写代码 |
| **写代码** | 自己写 `defineTool` 封装 HTTP/CLI | **T3/T4** | 对方没有 MCP，或需要特殊处理 |

### 11.1 从 ouroboros 学到的 3 条集成硬知识

1. 🔥 **子进程环境会被清洗**：凭据形状的名字（`/KEY|PASSWORD|SECRET|TOKEN/i`）和所有 `DSH_*` 会被移除。**要传的凭据必须显式列在 `config.env` 里**。
2. **长任务必须显式加大超时**：MCP 客户端默认 60s，长流程要写 `toolCallTimeoutMs: 1800000`。
3. **`failOnStartupError: false` 做软失败**：外部依赖没装好时，DSH 仍能正常启动。

### 11.2 社区踩过的外部调用坑（详见 `05-pitfalls.md` 与 `10b-casebook-tools.md`）

| 坑 | 教训 |
|---|---|
| 无 scope 的检索调用 → 模型收到不透明的 HTTP 400 | 错误信息要**给人/模型看得懂**，别只回状态码 |
| SSE 流被截断时把半截答案当完整答案 | 流式响应必须校验完整性 |
| dsh 会 scrub 掉继承环境里的"凭据形状"变量 | 同 11.1 第 1 条 |
| 工具结果用 camelCase 的 `isError`，插件只认 `is_error` | **字段名大小写**是跨系统集成的头号坑；以宿主的实际字段为准 |
| MCP 代理**自身超时**被当成"服务器不可达"上报 | 区分"我方超时"和"对方不可达" |
| Node 的 `fetch` 默认无视代理环境变量 | 需要代理时要显式配置 |
| 外部 provider 返回的 JSON 不符合声明的 schema | 收到外部数据必须**逐字段校验**，别直接透传 |

---

## T12 · 工程化骨架（完整规范的插件工程）★★★

### 12.1 官方标准目录（逐字，`docs/cookbook/adding-a-package.zh.md §1`）

```
packages/<group>/<pkg>/
  package.json     # copy from packages/core/tools, adjust name/description/deps
  tsconfig.json    # extends ../../../tsconfig.base.json, rootDir src,
                   # outDir lib/types, references: ../../../vendor/cosmokit,
                   # ../../../vendor/cordis (+ ../../../vendor/schemastery if
                   # you use Config, + ../../<group>/<dep> for each dsh dep)
  src/index.ts     # service default export or plugin (name/inject/apply/Config)
  README.md        # service API, events, extension points, design notes,
                   # + gated Model Experience context blocks or short form
                   # + the gated "Known Limitations and Deferred Work" section
```

> 🔑 那一行 `src/index.ts  # service default export or plugin (name/inject/apply/Config)` —— 官方一句话说清两种形态的选择。

### 12.2 第三方插件推荐目录（把官方约定搬到独立仓库）

```
my-dsh-plugin/
├── package.json
├── tsconfig.json
├── tsdown.config.ts          # 仅 UI 插件需要
├── cordis.patch.yml          # 仅组合包需要
├── README.md                 # 必须写：功能/前置要求/配置项/已知限制
├── src/
│   ├── index.ts              # 宿主半侧：apply()
│   ├── types.ts              # 只放类型，不放运行时代码
│   └── client/               # 仅 UI 插件
│       ├── index.ts
│       ├── Widget.tsx
│       └── Widget.module.css
└── tests/                    # 测试放这里，不是 src/__tests__/
    └── my-plugin.spec.ts
```

### 12.3 `package.json` 不变式（逐字）

> `private: true`，`version` 与根 `package.json` 一致，`type: module`，`main: "lib/index.js"`，`types: "lib/types/index.d.ts"`，`exports["."].types: "./lib/types/index.d.ts"`，`exports["."].default: "./lib/index.js"`，`@deepseek-ai/cordis` 同时出现在 peerDependencies 和 devDependencies 中（相同范围）。每个 dsh 对等依赖（peer dependency）都要在 devDependencies 中镜像。`@deepseek-ai/schemastery` 放在 `dependencies` 中（它是运行时校验器），与 agent-loop 保持一致。`files` 列表精确包含 `lib/index.js`、`lib/types/**/*.d.ts` …

### 12.4 相对导入必须写 `.ts` 后缀（逐字）

> 包内的相对导入在源码中使用显式 `.ts` 后缀（例如 `export * from './types.ts'`）。编译器在输出的 JS 中将其重写为 `.js`，在声明文件中保留显式 `.ts` 后缀。

> 💡 所以官方代码里全是 `from './types.ts'`、`from './Brand.tsx'` —— **这是官方要求，不是笔误**。

### 12.5 发布前自查

```bash
npx publint          # 检查 exports / files 是否配错（最有用的一条）
```

官方完整门禁清单见 `07-conventions.md` 第 J 篇。

### 12.6 命名别纠结：官方角色命名表（节选）

| 词 | 什么时候用 | **不该**用的时候 |
|---|---|---|
| `Registry` | 拥有一组动态具名注册 + 查询/重复项/优先级/生命周期 | 主要约定是分派、执行、取消 |
| `Store` | 拥有一组数据，提供 CRUD/snapshot/subscription | 校验状态机、裁决权限。**类里有 map ≠ store** |
| `Runtime` | 跑实时工作，跨调用拥有分派/取消/生命周期 | 只存记录、只返回目录 |
| `Policy` | 决定允许/选择/限制什么 | 执行该决定所允许的机制 |
| `Gateway` | 适配进程、网络、RPC 或 API 边界 | 只注册同进程服务 |
| `Provider` | 提供某项能力的一个实现（多实现加厂商限定词） | 表示能力定义或 provider registry |
| `Controller` | 接受命令/用户意图并改变领域状态 | 执行任意工作、拥有一组 provider |
| `Service` | 无法用以上更精确角色诚实描述的内聚领域服务 | **只因为继承了 Cordis `Service`** |

> 🔑 官方还规定：**单数 key 用于 engine/runtime/policy/controller/resolver/store/当前配置；复数 key 用于 registry/多具名成员的服务**。类的角色与 key 的单复数必须一致。

### 12.7 README 必须包含的两节（官方强制）

```
## Model Experience        # 这个插件对模型的请求上下文有什么影响（token / KV cache）
## Known Limitations and Deferred Work   # 诚实清单：已知限制与没做的事
```

> 💡 即使你不在官方仓库，**照抄这两节**会让你的插件 README 质量立刻上一个档次 —— 尤其"已知限制"这节，能极大减少用户的困惑。

---


---

