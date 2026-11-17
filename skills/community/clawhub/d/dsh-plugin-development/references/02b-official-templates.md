# 官方七类模板 · 逐字源码分册

> **文件来源**：本文件由 `02-templates.md` 拆分而来，正文为原文的**逐行搬迁**，未做改写。
> **本册性质**：**全部是上游一手素材原文** —— 性质不一：既有官方文档的**逐字摘录（属权威原文）**，也有调研期写下的**粗笔记（仅备查）**。**读某一段前，务必连带读该段开头的取材说明**，那是判断这段能信多少的依据。
> **不要整读**：先 `grep -n '^#{1,2} '` 拿小节清单，再只读需要的那一节。本技能面向任务的整理稿见 `02-templates.md`。
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。

---

<!-- ↓ 源：E-official-templates.md （全文） -->

# E. 官方自带插件 —— 七类可复用模板（原始素材）

> 来源：**DSH 上游检出**（完整克隆，commit `86a402200d`，`0.2.1-alpha.4`；本 skill 不附带该检出，核验方式见 `00-version-gate.md`）。
> 所有代码**逐字照抄**仓库原文，未改写。每个模板标注来源文件路径。
> 面向《DSH 插件开发实战手册》补充篇，读者为零软件工程经验新手。

---

## 0. 官方插件全景（实证数字）

| 事实 | 数值 | 取证命令 |
|---|---|---|
| 声明 `dsh` 清单的官方包 | **70** | `grep -rl '"dsh"\s*:' packages/*/*/package.json \| wc -l` |
| 其中 `packages/client/*`（UI 插件） | **46** | 同上，按目录分组统计 |
| `packages/bundle/*`（组合包） | 6 | |
| `packages/api/*`（宿主 RPC） | 5 | |
| `packages/experimental/*` | 4 | |
| `packages/session/*` | 3 | |
| `packages/subagent/*` | 2 | |
| `packages/extensions/*` | 2 | |

**`dsh` 字段只有两种形态**（去重后）：
- `{"bundle": {"patch": "./cordis.patch.yml"}}` ×10 —— 组合包（配置型插件）
- `{"client": {"inject": [...], "platform": "web", "immediately"?: true, "external"?: [...]}}` ×其余 —— 客户端（UI）插件

**官方包命名**：宿主侧 `@deepseek-ai/dsh-<域>-<名>`；客户端侧 `@deepseek-ai/dsh-client-<域>-<名>`。

**官方顶层分组（51 个域）**：
`acp api attachment boot browser-use bundle client compaction computer-use context core credentials experimental extensions feedback fs goal guard hooks host identity interaction jobs llm lsp mcp plan preset ptc-runtime runtime-diagnostics sandbox schedule sdk session session-query settings shell skill spill ssh storage subagent subprocess terminal test-support todo typert util web webhook workflow workspace`

> ⚠️ 上述目录名随官方增删而变；本行已于基线 `dsh-v0.1.7-rc.1` 复核（`code-runtime` → `ptc-runtime`、`e2b` 整体移除、新增 `browser-use` / `computer-use` / `ssh`）。**要用请现场 `ls` 一遍，不要照抄本行。**

---

## 模板 1 · 纯配置组合包（零代码插件）

**学习点**：插件可以**不写任何运行时代码**，只靠一个 YAML 补丁文件描述"要挂载哪些行"。

**来源**：`packages/bundle/base`（`src/index.ts` 仅 9 行）

### 1.1 `package.json`（关键字段）

```json
{
  "name": "@deepseek-ai/dsh-base",
  "version": "0.1.7-rc.1",
  "type": "module",
  "main": "lib/index.js",
  "types": "lib/types/index.d.ts",
  "exports": {
    ".": {
      "types": "./lib/types/index.d.ts",
      "default": "./lib/index.js"
    },
    "./cordis.patch.yml": "./cordis.patch.yml",
    "./src/*": "./src/*",
    "./package.json": "./package.json"
  },
  "files": [
    "lib/index.js",
    "cordis.patch.yml",
    "lib/types/**/*.d.ts"
  ],
  "license": "MIT",
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

> ⚠️ 注意 `files` 必须包含 `cordis.patch.yml`，否则发布到 npm 后补丁文件丢失，插件装上等于没装。同时 `exports` 里要有 `"./cordis.patch.yml": "./cordis.patch.yml"`。

### 1.2 `src/index.ts`（全文）

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

### 1.3 `cordis.patch.yml` 语法（从 `packages/bundle/base/cordis.patch.yml` 提炼）

补丁文件用 **`insert:` 列表**，每行一个插件节点：

```yaml
- insert:
    - id: timer
      name: '@deepseek-ai/cordis-plugin-timer'

    - id: hmr
      name: '@deepseek-ai/dsh-hmr'
      disabled: !!js "!ctx.get('profileContext')"
      config:
        root: []

    - id: agent-default-model
      name: '@deepseek-ai/dsh-agent-default-model'
      config:
        provider: deepseek-official
        model: deepseek-flash

    - id: session-title
      name: '@deepseek-ai/dsh-session-title'
      config:
        fallbackMaxWords: 5
        fallbackMaxBytes: 40
        maxTitleBytes: 80
```

**字段语义（原文注释 + 结构实证）**：

| 字段 | 含义 |
|---|---|
| `id` | 行标识。后续补丁层与用户的 `cordis.patch.yml` 靠它**覆盖**该行，**逐行 last-write-wins** |
| `name` | 包名（npm 包名，可指向子路径如 `@deepseek-ai/dsh-tool-subagent-control/list-agents`） |
| `disabled` | `true` 关闭该行；可用 `!!js` 表达式（见下） |
| `config` | 传给该插件的配置对象。**补丁替换整段 config，不做合并**（原文注释明确） |

**`!!js` 内联表达式**（原文出现，可直接抄）：

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

    - id: bash-sandbox
      name: '@deepseek-ai/dsh-bash-sandbox'
      disabled: !!js process.platform === 'win32'
      config:
        timeoutMs: 60000
```

> 🔥 **跨平台写法必抄**：官方用 `disabled: !!js process.platform === 'win32'` 让 bash 工具只在非 Windows 启用、pwsh 工具只在 Windows 启用。这是处理平台差异的**官方姿势**。

**原文关键约束（逐字摘录，对写补丁极重要）**：

> A patch replaces the targeted row's whole `config` rather than merging into it, so a row whose value differs by mode does NOT live here: it belongs to each mode bundle, keeping any single row down to one bundle layer plus the user's.

> Row order carries no load semantics (activation is service-availability driven); the grouping is for readers.

**第二条极其关键**：**行的书写顺序不影响加载顺序**，激活由「服务可用性」驱动。这是新手最常见的误解（以为要按依赖顺序写）。

---

## 模板 2 · 最小 UI 插件（客户端半侧 + 插槽）

**学习点**：UI 插件 = 一个空的宿主半侧 + 一个客户端半侧。UI 通过**命名插槽（slot）**注入，不直接改别人的界面。

**来源**：`packages/client/ui-brand-official`（全包 49 行）

### 2.1 `package.json`（关键字段）

```json
{
  "name": "@deepseek-ai/dsh-client-ui-brand-official",
  "version": "0.1.7-rc.1",
  "type": "module",
  "main": "lib/index.js",
  "types": "lib/types/index.d.ts",
  "exports": {
    ".": {
      "types": "./lib/types/index.d.ts",
      "default": "./lib/index.js"
    },
    "./client": {
      "types": "./lib/types/client/index.d.ts",
      "default": "./lib/client.js"
    },
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
  "scripts": {
    "bundle": "tsdown",
    "watch": "tsdown --watch"
  },
  "license": "MIT",
  "peerDependencies": {
    "@deepseek-ai/cordis": "workspace:^"
  },
  "devDependencies": {
    "@deepseek-ai/dsh-client-ui-primitives": "workspace:^",
    "@deepseek-ai/dsh-client-ui-renderer": "workspace:^",
    "@deepseek-ai/dsh-client-ui-sidebar": "workspace:^",
    "@deepseek-ai/cordis": "workspace:^",
    "@testing-library/react": "^16.1.0",
    "@types/react": "~18.3.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "files": [
    "lib/index.js",
    "lib/client.js",
    "lib/types/**/*.d.ts"
  ]
}
```

**四个必记点**：
1. `exports["./client"]` 指向客户端 bundle（`lib/client.js`）——**缺了它 UI 半侧不会被加载**。
2. `dsh.client.inject` 声明"我依赖哪些客户端插件"，值为**包名数组**。
3. `dsh.client.platform: "web"`。
4. `files` 必须含 `lib/client.js`。

### 2.2 宿主半侧 `src/index.ts`（全文）

```ts
/**
 * Official browser-brand plugin, node half. The empty apply gives Loader a
 * host-side row while the browser half ships through `exports["./client"]`.
 */

/** Host plugin body — this package contributes browser presentation only. */
export function apply(): void {}
```

> 宿主半侧**空实现**就够了 —— 这是纯 UI 插件的标准形态。

### 2.3 客户端半侧 `src/client/index.ts`（全文）

```ts
/** Official DeepSeek Harness occupants for the generic browser-brand slots. */
import type { Context as ClientContext } from '@deepseek-ai/cordis'
import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'
import type {} from '@deepseek-ai/dsh-client-ui-sidebar/client'
import { OfficialBrandMark, OfficialBrandName } from './Brand.tsx'

/** Required service: the UI slot registry. */
export const inject = ['slots']

/**
 * Fill the sidebar brand slots as one declaration-aware registration set. The
 * conversation hero stays on its declaring package's animated fish fallback,
 * so the official build registers nothing there.
 * @param ctx - Client root context.
 */
export function apply(ctx: ClientContext): void {
  if (process.env.DSH_CLIENT_BUILD_PROFILE !== 'official') return
  ctx.slots.inject('sidebar.brand.mark', () =>
    ctx.slots.inject('sidebar.brand.name', function* () {
      yield ctx.slots.register({ name: 'sidebar.brand.mark' }, OfficialBrandMark)
      yield ctx.slots.register({ name: 'sidebar.brand.name' }, OfficialBrandName)
    }))
}
```

**三个必记点**：
1. `export const inject = ['slots']` —— 声明依赖 **slots 服务**（UI 插槽注册表）。
2. `ctx.slots.inject('<slot名>', () => ...)` —— 往某插槽注入；**返回 disposer**，用于卸载。
3. `ctx.slots.register({ name: '<slot名>' }, 组件)` —— 注册组件；**返回 disposer**。

> 🔥 **`inject` 的两层含义**（新手最容易混）：
> - `package.json` 的 `dsh.client.inject` 是**包级依赖**（字符串包名），决定加载顺序。
> - 代码里的 `export const inject = [...]` 是**服务级依赖**（服务名），决定 `apply` 何时被调用。
> 两者名字像、层级完全不同。

### 2.4 组件 `src/client/Brand.tsx`（全文）

```tsx
import { BrandWordmark, FishLogo } from '@deepseek-ai/dsh-client-ui-primitives'
import type { SidebarBrandMarkOwnerProps } from '@deepseek-ai/dsh-client-ui-sidebar/client'

/**
 * Render the official mark with the presentation requested by its host surface.
 * @param props - Host-supplied mark presentation.
 * @returns the official whale mark.
 */
export function OfficialBrandMark({ size }: SidebarBrandMarkOwnerProps) {
  return <FishLogo size={size} />
}

/**
 * Render the official name artwork without its independently slotted mark.
 * @returns the official name wordmark.
 */
export function OfficialBrandName() {
  return <BrandWordmark includeMark={false} />
}
```

> 前端框架 = **React 18 + TSX**（`react`/`react-dom` 为 `devDependencies`，由宿主提供）。

### 2.5 构建配置 `tsdown.config.ts`（全文）

```ts
import { clientBundle } from '../tsdown.client.ts'

export default clientBundle('@deepseek-ai/dsh-client-ui-brand-official', ['lib/types/index.js'])
```

### 2.6 `tsconfig.json`（全文）

```json
{
  "extends": "../../../tsconfig.base.client.json",
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "lib/types"
  },
  "include": [
    "src"
  ],
  "references": [
    {
      "path": "../../../vendor/cordis"
    },
    {
      "path": "../ui-renderer"
    },
    {
      "path": "../ui-primitives"
    },
    {
      "path": "../ui-sidebar"
    },
    {
      "path": "../ui-slots"
    }
  ]
}
```

> ⚠️ `extends` 的是 **客户端专用** 基座 `tsconfig.base.client.json`（不是服务端的）。

---

## 模板 3 · 工具插件（`defineTool`）

**学习点**：给模型加一个可调用的工具。这是"外部调用/集成方向"的骨架。

**来源**：`packages/interaction/tool-ask-user`（全包 101 行，官方最小的工具插件）

### 3.1 `package.json` 关键字段

```json
{
  "name": "@deepseek-ai/dsh-tool-ask-user",
  "version": "0.1.7-rc.1",
  "type": "module",
  "main": "lib/index.js",
  "types": "lib/types/index.d.ts",
  "exports": {
    ".": {
      "types": "./lib/types/index.d.ts",
      "default": "./lib/index.js"
    },
    "./src/*": "./src/*",
    "./package.json": "./package.json"
  },
  "files": ["lib/index.js", "lib/types/**/*.d.ts"],
  "license": "MIT",
  "peerDependencies": {
    "@deepseek-ai/dsh-agent": "workspace:^",
    "@deepseek-ai/dsh-tools": "workspace:^",
    "@deepseek-ai/dsh-user-questions": "workspace:^",
    "@deepseek-ai/cordis": "workspace:^"
  }
}
```

> 💡 **工具插件没有 `dsh` 字段**！它靠"依赖被谁挂载"进入组合，不需要 `dsh.bundle` 或 `dsh.client`。这是和 UI 插件/组合包的**关键差异**。

> ⚠️ **本技能补充（不是上面模板的原文，改模板时别混进去）**：上面这些官方模板里 `"@deepseek-ai/dsh-*": "workspace:^"` 用的是 `workspace:` 协议 —— **只在 `peerDependencies` 里有效**。自 `dsh-v0.2.1-alpha.4` 起，如果你另外声明 **`engines.dsh`**，则**它单独决定兼容性**，这些 peer 范围**不再**放宽或收窄它，而且 **`engines.dsh` 里写 `workspace:` 会被判不兼容**（`engines` 非对象或 `engines.dsh` 非字符串还会让该包**被直接拒绝装载**）。→ 要么给 `engines.dsh` 一个覆盖全部目标版本的完整语义化范围，要么**不写**它、退回 peer 检查。判据：`docs/upgrade-guide/v0.2.1-alpha.3/plugin-engines-dsh/guide.zh.md`、`packages/boot/app-boot/src/plugin-compatibility.ts:55-73`。

### 3.2 `src/index.ts`（全文，逐字）

```ts
/**
 * Model-facing Consumer of the `ctx.userQuestions` capability seam.
 * The tool pauses until a UI provider returns a human answer, then feeds that
 * answer back into the agent loop as an ordinary tool result.
 *
 * @module @deepseek-ai/dsh-tool-ask-user
 */

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
            header: {
              type: 'string',
              description: 'Optional short heading for the question, such as "Confirm" or "Choose Mode".',
            },
            options: {
              type: 'array',
              description: 'Optional choices to show the user. If you recommend one, put it first and append "(Recommended)" to that label.',
              items: {
                type: 'object',
                additionalProperties: true,
                properties: {
                  label: { type: 'string', required: true, description: 'Short user-facing option label.' },
                  description: { type: 'string', description: 'One sentence explaining the tradeoff or impact.' },
                },
              },
            },
            multi_select: {
              type: 'boolean',
              description: 'Whether the user may select more than one option. Defaults to false.',
            },
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
      const result = await ctx.userQuestions.ask({
        questions: args.questions.map(question => ({
          id: question.id,
          question: question.question,
          ...question.header !== undefined ? { header: question.header } : {},
          ...question.options !== undefined ? { options: question.options } : {},
          ...question.multi_select !== undefined ? { multiSelect: question.multi_select } : {},
        })),
        ...exec.agent !== undefined ? { agent: exec.agent } : {},
        signal: exec.signal,
      })
      return {
        answers: result.answers.map(answer => ({
          id: answer.id,
          selected: [...answer.selected],
          ...answer.custom !== undefined ? { custom: answer.custom } : {},
        })),
      }
    },
  }))
}
```

### 3.3 `defineTool` 参数结构（速查表）

| 字段 | 类型/写法 | 说明 |
|---|---|---|
| `name` | `string` | 模型看到的工具名，下划线风格（`ask_user_question`） |
| `description` | `string` | **极重要**：模型靠它决定是否调用，要写"什么时候用" |
| `parameters` | 对象字面量（**不是** JSON Schema 顶层 `type/properties` 包装） | 直接写字段名 → `{type, required, description, items/properties}` |
| `parameters.<x>.type` | `'string' \| 'number' \| 'boolean' \| 'array' \| 'object'` | |
| `parameters.<x>.required` | `true` / 省略 | **`required` 写在字段里**，不是单独的 required 数组 |
| `parameters.<x>.description` | `string` | 逐字段描述，模型靠它填参 |
| `parameters.<x>.items` | 数组元素 schema | 数组用 `items` |
| `parameters.<x>.properties` | 对象字段 schema | 对象用 `properties` + `additionalProperties` |
| `output.schema` | JSON Schema | 返回值的结构约束 |
| `output.render` | `(args, value) => [{type:'text', text}]` | 渲染成模型可读内容 |
| `execute` | `async (args, exec) => result` | 业务逻辑；`exec.signal` 是取消信号，`exec.agent` 是当前 agent |

> 🔥 **与网上旧教程的关键差异**：`parameters` **不是**原始 JSON Schema（旧写法是 `parameters: {type:'object', properties:{...}, required:[...]}`）。新版是"字段名直接铺平 + `required` 内联"的 DSL。抄错会完全不工作。

---

## 模板 4 · 命令插件（`/斜杠命令`）

**来源**：`packages/feedback/command-feedback`

### 4.1 核心注册代码（逐字摘录）

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
    text: `Feedback recorded for session ${invocation.agent.session.id}\nAnonymous user: ${getOrCreateAnonymousUserId()}.`,
  }
}

export function apply(ctx: Context): void {
  ctx.plugin(SessionFeedbackService)
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

### 4.2 命令注册参数速查

| 字段 | 值 | 说明 |
|---|---|---|
| `definitionId` | `CommandDefinitionId('@scope/pkg')` | 品牌化 id，**必须用 `CommandDefinitionId()` 包装** |
| `name` | `'feedback'` | 用户在输入框敲的 `/feedback` |
| `description` | `string` | 斜杠菜单里显示 |
| `input` | `{ hint: '<text>' }` | 输入提示 |
| `recordInput` | `false` | 是否把输入记进会话日志 |
| `handler` | `(inv: CommandInvocation) => CommandResult` | 返回值二选一 |

**`CommandResult` 两种形态**：
- 成功：`{ kind: 'success', text: string }`
- 失败：`{ kind: 'error', text: string }`

**`CommandInvocation` 关键字段**：`invocation.rawInput`（用户原始输入）、`invocation.agent`（当前 agent，`agent.session` 是会话）。

### 4.3 「命令 vs 工具」怎么选

| | 命令 Command | 工具 Tool |
|---|---|---|
| 触发者 | **人**（敲 `/xxx`） | **模型**（自动决定调用） |
| 注册 API | `ctx.commands.register({...})` | `ctx.tools.register(defineTool({...}))` |
| 依赖服务 | `inject = ['commands']` | `inject = ['tools', ...]` |
| 典型用途 | 开关模式、导出、清空、反馈 | 读写文件、搜索、调外部 API |

---

## 模板 5 · 可配置插件（Config Schema）

**学习点**：让用户在 `cordis.patch.yml` 的 `config:` 里配置你的插件，并在加载时校验。

**来源**：`packages/context/time-context`

### 5.1 极简写法（推荐给新手）

```ts
import zd from '@deepseek-ai/schemastery'   // 注意：官方此文件里 import 名是 z（见下）

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

> 原文 import 行逐字为：`import z from '@deepseek-ai/schemastery'`

**机制（关键，新手必须懂）**：
- 同一个名字 `Config` 既导出 **TypeScript 接口**，又导出**运行时校验器**（接口与值同名共存）。
- DSH 的加载器看到插件模块导出的 `Config`，就把它当作 schema，对 `cordis.patch.yml` 里该行的 `config:` 做校验。
- 校验失败 → **插件加载失败**（官方注释原文：`Invalid values fail plugin load.`）。

### 5.2 手写校验（另一条路，无 schema 依赖）

**来源**：`packages/plan/plan-mode`

```ts
/** Deployment-owned plan guidance. */
export interface PlanModeConfig {
  /** Guidance rendered as the `plan:policy` prompt section while plan mode is active. */
  section: string
}

export function resolveConfig(config: PlanModeConfig): PlanModeConfig {
  const section = (config as Partial<PlanModeConfig>).section
  // (原文随后校验：必须是字符串、非空、且不能有未知键)
  ...
  throw new Error(`PlanModeConfig has unknown key(s) ${unknown.join(', ')} — config is { section }`)
}
```

**两条路的取舍**：

| | `export const Config = z.object({...})` | 手写 `resolveConfig()` |
|---|---|---|
| 代码量 | 少 | 多 |
| 报错信息 | 库自动生成 | **可以写得非常人话** |
| 适用 | 新手首选 | 想要"教会用户怎么配"的场景 |

> 🔥 `resolveConfig` 抛出的 `PlanModeConfig has unknown key(s) ... — config is { section }` 是**教科书级错误信息**：说清错在哪、期望是什么。写自己的配置校验时照这个格式抄。

### 5.3 在 `cordis.patch.yml` 里消费配置

```yaml
    - id: plan-mode
      name: '@deepseek-ai/dsh-plan-mode'
      config:
        section: |
              You are in plan mode. Stay in plan mode until exit_plan_mode succeeds...
```

---

## 模板 6 · 设置卡片插件（在设置界面加一张卡）

> 🔴 **本节的代码是 `0.1.7-rc.1` 之前的上游形态，别照抄**（本册是**逐行搬迁的素材原文**，为保留历史原样**不做改写**）。
> 具体失效点：客户端服务 **`ctx.settingsScope` 已移除**（新树全树 0 命中）→ 改为 **`ctx.configForms.get<T>(ns)`**；
> 宿主侧 **`settings.register(ns, Schema)` / `settings.get(ns)` 已移除** → 改为**由插件自己的 `Config` schema 派生表单** + `ctx.settings.configure(...)`。
> **当前可用写法见 `02-templates.md` 的 T9（§9.2 / §9.3，已按 `0.2.0-rc.2` 重写）与 `04-ui-and-slots.md` §10.9 的逐条映射表。**
> 下面 6.2 / 6.3 两段保留原文，仅作「旧机制长什么样」的对照。

**学习点**：UI 插件往 `settings.general.item` 这类插槽塞一个 React 组件，并通过宿主 settings 服务持久化。

**来源**：`packages/client/ui-theme`

### 6.1 `package.json` 的 `dsh.client`

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

### 6.2 宿主半侧注册"设置命名空间"（`src/index.ts` 摘录）

```ts
/** Read the registered theme section or the schema defaults without a settings provider. */
function readSection(ctx: Context): { preference: ThemePreference; fontSize: number } {
  const fallback = { preference: DEFAULT_PREFERENCE, fontSize: DEFAULT_FONT_SIZE }
  const settings = ctx.get('settings')
  if (settings === undefined) return fallback
  const section = settings.get(THEME_NAMESPACE) as ThemeSettings | undefined
  if (section === undefined) return fallback
  return section
}

export function apply(ctx: Context): void {
  ctx.inject(['settings'], (settingsCtx) => {
    settingsCtx.settings.register(THEME_NAMESPACE, ThemeSettingsSchema)
  })
  ctx.on('webserver/index-inject', (table) => {
    const section = readSection(ctx)
    table.push(bootThemeInjection(section.preference, section.fontSize))
  })
}
```

**必记点**：
- `ctx.get('settings')` —— **探测**可选服务是否存在（不阻塞加载）。
- `ctx.inject(['settings'], cb)` —— **等服务就绪后再执行** `cb`（不要写成硬依赖）。
- `settingsCtx.settings.register(命名空间, Schema)` —— 注册一个持久化的设置段。
- `ctx.on('webserver/index-inject', ...)` —— 往页面 HTML 注入行（首屏生效，避免闪烁）。

### 6.3 客户端半侧注册到设置插槽（`src/client/index.ts` 摘录）

```ts
/**
 * Required services: settings transport plus slots/locale for the Appearance
 * row. `remote` carries the forwarded settings invalidation that
 * `ctx.settingsScope.bind(spec)` subscribes to on this context.
 */
export const inject = ['slots', 'locale', 'remote', 'settingsScope']

export function apply(ctx: ClientContext): void {
  installThemeStyles(ctx)
  const host = ctx.settingsScope.bind<ThemeSettings>({ namespace: THEME_SETTINGS_NAMESPACE })
  const theme = new ThemeRuntime(ctx, host)
  ctx.provide('theme', theme)

  ctx.effect(() => ctx.locale.register(SETTINGS_NS, { zh, en }), 'ui-theme: settings row dictionaries')

  const store = createAppearanceRowStore()
  let bound: BoundActions<typeof store> | undefined
  const sync = (snapshot: ThemeSnapshot): void => {
    bound?.sync(snapshot.preference, snapshot.revision)
  }
  ctx.on('theme/change', sync)
  const injected = (actions: BoundActions<typeof store>): AppearanceRowInjected => {
    bound = actions
    // Re-sync from the getter so no event is lost between registration and
    // first render (the store's revision guard drops stale duplicates).
    sync(theme.getTheme())
    return {
      setTheme: (id) => { theme.setTheme(id) },
    }
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

**`ctx.slots.register` 的完整参数（UI 高级用法）**：

| 字段 | 说明 |
|---|---|
| `name` | 插槽名（`'settings.general.item'`） |
| `id` | 本注册项在该插槽内的唯一 id |
| `order` | 排序（数字小的在前；此处 10、11） |
| `store` | 绑给组件的响应式 store（`useStore` 消费） |
| `locale` | 文案命名空间 |
| `inject` | 给组件注入"业务动作"的回调工厂 |

### 6.4 组件写法（`src/client/AppearanceRow.tsx` 摘录）

```tsx
import type { PropsLocale, PropsRuntime, PropsStore } from '@deepseek-ai/dsh-client-ui-slots'
import type { createAppearanceRowStore } from './settings-store.ts'
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
      <div className={css.cubeRow}>
        {CUBES.map(({ id, labelKey, Icon }) => (
          <button
            key={id}
            type="button"
            className={clsx(css.themeCube, preference === id && css.selected)}
            aria-pressed={preference === id}
            onClick={() => { setTheme(id) }}
          >
            <Icon />
            {t(labelKey)}
          </button>
        ))}
      </div>
    </div>
  )
}
```

**四件套 props（插槽组件的标准契约）**：
- `PropsRuntime<'插槽名'>` —— 运行时共享
- `PropsStore<store 类型>` —— 提供 `useStore` 选择器
- `PropsLocale<'命名空间'>` —— 提供 `t()` 翻译函数
- 自己的 `Injected` 面 —— 业务动作（如 `setTheme`）

**样式方案**：**CSS Modules**（`import css from './X.module.css'`）+ 全局语义 token（`--dsw-alias-*`）。官方不要求 Tailwind。

### 6.5 官方主题 token（可以直接用的语义变量）

**来源**：`packages/client/ui-theme/src/client/index.ts`

| Token | 用途 |
|---|---|
| `--dsw-alias-bg-base` | 应用基础背景 |
| `--dsw-alias-bg-layer-1` / `-layer-2` | 一/二级浮起表面 |
| `--dsw-alias-bg-overlay` | 浮层/气泡背景 |
| `--dsw-alias-border-l1` / `-l2` | 一/二级边框 |
| `--dsw-alias-brand-primary` | 品牌主色 |
| `--dsw-alias-label-primary` / `-secondary` | 主/次文字 |
| `--dsw-alias-state-error-primary` | 错误态 |
| `--dsw-alias-state-success-primary` | 成功态 |
| `--dsw-alias-state-warn-primary` | 警告态 |
| `--dsw-specific-sidebar-fill` | 侧栏底色 |

> 🔥 每个 token **都要求 light/dark 两个值**（原文：`requiresLightAndDark: true`）。只给一个值在切换配色时会变瞎——官方为此专门写了一段会抛错的校验（见下）。

**官方为"只给一个值"写的教学式报错（逐字，极好的错误信息范本）**：

```ts
      throw new TypeError(
        `theme override "${name}" from "${source}" is a bare string — pass { light: ${JSON.stringify(value)}, dark: ${JSON.stringify(value)} } `
        + '(repeat the value when it is the same in both palettes); a single value goes illegible when the user switches color scheme',
      )
```

---

## 模板 7 · 生命周期与副作用回收（`ctx.effect`）

**来源**：`packages/client/ui-theme/src/client/index.ts`

```ts
    if (this.media !== undefined) {
      const media = this.media
      const onChange = (): void => {
        if (this.preference !== 'system') return
        this.publish()
      }
      ctx.effect(() => {
        media.addEventListener('change', onChange)
        return () => { media.removeEventListener('change', onChange) }
      }, 'ui-theme: prefers-color-scheme listener')
    }
    ctx.effect(() => host.subscribe(() => { this.adopt() }), 'ui-theme: settings scope adoption')
```

**`ctx.effect(setup, label)` 规则**：
- `setup` 是函数，**返回一个清理函数**（disposer）。
- 第二个参数是**人类可读的标签**（官方每次都写，如 `'ui-theme: prefers-color-scheme listener'`）。
- 插件卸载 / HMR 重载时，DSH 自动调用清理函数 → **监听器、订阅、定时器不会泄漏**。

> 🔥 **新手第一号事故源**：加了事件监听/订阅却忘了返回清理函数 → 热更新后监听器叠加、界面越改越慢、事件触发多次。**凡是在插件里注册了外部资源，一律包进 `ctx.effect`。**

**注册类 API 一般自带 disposer**，不必再包 `ctx.effect`：

```ts
  register(definition: ThemeDefinition): () => void {
    ...
    return () => {
      if (!this.themes.some(t => t.id === definition.id)) return
      this.themes = this.themes.filter(t => t.id !== definition.id)
      ...
    }
  }
```

**官方注释原文（讲清了"为什么"）**：
> Disposing the theme backing the active preference resets the preference to the default so the UI never keeps tokens of an unregistered theme.

---

## 附：官方服务名速查（从各插件 `inject` 实证）

| 服务名（`inject` 里的字符串） | 用途 | 来源 |
|---|---|---|
| `tools` | 工具注册表 | `tool-ask-user` |
| `commands` | 斜杠命令注册表 | `command-feedback` |
| `userQuestions` | 向用户提问的能力 | `tool-ask-user` |
| `agents` | agent 注册表 | `time-context` |
| `sessionProjections` | 会话投影 | `time-context` |
| `settings` | 用户设置存储 | `ui-theme`（宿主） |
| `sessions` | 会话存储 | `command-feedback` |
| `slots` | UI 插槽注册表 | `ui-brand-official`、`ui-theme` |
| `locale` | 文案 | `ui-theme` |
| `remote` | 宿主↔客户端转发 | `ui-theme` |
| `configForms` | 客户端设置表单的读 / 写面（`get<T>(entryId)` → `getSnapshot` / `subscribe` / `set` / `unset` / `mutate`） | `ui-theme` |

> 🔴 **本表最后一行 2026-09-30 更正**：原先记的是 **`settingsScope`** —— 该客户端服务随 `0.1.7-rc.1` 的「设置机制重做」**已被移除**（新树全树 **0 命中**），继任者是 **`configForms`**。
> 实测依据：`packages/client/ui-theme/src/client/index.ts:587` 的 `inject = ['slots', 'locale', 'remote', 'configForms']`、`:599` 的 `ctx.configForms.get<ThemeSettings>(ns)`。
> 其余各行经同轮复核**仍然有效**。

**宿主事件名（`ctx.on` 实证）**：`webserver/index-inject`（注入页面 HTML）、`theme/change`（自定义事件示例）。

**插槽名（实证）**：`sidebar.brand.mark`、`sidebar.brand.name`、`settings.general.item`。

---

## 附：官方 UI 插槽名（**节选 40 余个**，实测提取）

> ⚠️ **这不是全清单。** 本表由 `grep -rhoE "slots\.(inject|register)\(\s*'[^']+'" packages/*/*/src` 提取，因此**天然抓不到内建键**（如 `root` 是用 `renderSlot('root')` 渲染的）。
> 对基线 `dsh-v0.2.2-alpha.2` 的声明侧复核结果：**148 个键**（并集 **150** 个；剔除 **44** 个测试专用键后**约 106 个公开可用**）—— 2026-09-23 修好抽取器两处漏抽后重抽、2026-09-25 随 rc.2 推进 **+3 / −0**、2026-09-29 随 0.2.0-rc.1 推进 **+0 / −0**、2026-09-30 随 0.2.0-rc.2 推进 **+1 / −0**、2026-10-04 随 0.2.1-alpha.1 推进 **+2 / −0**、2026-10-09 随 0.2.1-alpha.2 推进 **+2 / −0**、**2026-10-15 随 0.2.1-alpha.3 推进 +5 / −1**（新增 `conversation.chat.message.images` / `conversation.chat.user.images` / `conversation.hero.options` / `conversation.user.text.node` / `workspace.toast`，**旧键 `conversation.message.images` 改名走掉**）、**2026-10-16 随 0.2.1-alpha.4 推进 +1 / −0**（新增键 `plugins.tab`）、**2026-10-17 随 0.2.1-rc.2 推进 +1 / −0**（新增键 `conversation.input.model.label`）；**2026-10-24 随 0.2.1-rc.3 推进 +3 / −0**（`slot-catalog.ts` **100 → 103**；新增键 = `conversation.session.header.views.actions` / `sidebar.panellist.actions` / `sidebar.right.tab.guide.actions`）；**2026-10-29 随 0.2.2-alpha.2 推进 +3 / −0**（`slot-catalog.ts` **103 → 106**；新增键 = `conversation.chat.text-interaction` / `conversation.chat.user.before` / `sidebar.session.row.trailing`）（旧值 96/99/约81 系低估）。另有**客户端半侧的权威口径**：上游生成产物 `packages/extensions/cordis-client-runner/src/client/slot-catalog.ts` 现有 **106 个**，抽取器 A2 段与它自动交叉核对，**漏抽量须为 0**。完整清单与可复现的抽取命令见 `14-inbound-http-and-timers.md` 与 `scripts/extract_slots.py`；注册签名（组件是第二个参数）与「未声明 slot 报什么错」也记在那里。
> 用法：`ctx.slots.inject('<插槽名>', () => ctx.slots.register({ name: '<插槽名>' }, 组件))`

### 会话 / 对话区（conversation.*）

| 插槽名 | 位置 |
|---|---|
| `conversation.view` | 对话主视图（**最常用的整块替换点**） |
| `conversation.chat.node` | 聊天消息节点 |
| `conversation.chat.assistant-actions` | 助手消息的操作按钮区 |
| `conversation.composer` | 输入框整体 |
| `conversation.composer.dock` | 输入框停靠区 |
| `conversation.input.dock` | 输入区停靠 |
| `conversation.input.overlay` | 输入区浮层 |
| `conversation.input.attachments` | 输入区附件 |
| `conversation.input.model` | 输入区模型选择 |
| `conversation.input.plan` | 输入区计划 |
| `conversation.hero.workspace` | 空态主视觉 / 工作区 |
| `conversation.hero.workspace.directoryFlow` | 空态目录选择流 |
| `conversation.chat.message.images` | `0.2.1-alpha.3` 起：助手消息里**一组连续持久化图片**的渲染器（`single` / `session`；`packages/client/ui-chat/src/client/contract/slots.ts:456`）。⚠️ **旧键 `conversation.message.images` 已在 `0.2.1-alpha.3` 改名走掉** |
| `conversation.chat.user.images` | `0.2.1-alpha.3` 新增：**用户消息**里的图片（含待发送与本地回显预览），可与输出侧图片**分别替换**（`single` / `session`；`…/ui-chat/src/client/contract/slots.ts:417`） |
| `conversation.user.text.node` | `0.2.1-alpha.3` 新增：业务方自有的**纯 JSON 文本节点**内联渲染器（`keyed` / `session`；`packages/client/ui-conversation/src/client/contract/slots.ts:214`） |
| `conversation.hero.options` | `0.2.1-alpha.3` 新增：新建会话行里**右对齐的紧凑选项位**（排在工作区与预设控件之后，仅在有会话时渲染；`list` / `session`；`…/ui-conversation/src/client/contract/slots.ts:268`） |
| `conversation.trajectory.images` | 轨迹里的图片 |
| `conversation.session.header.corner` | 会话头部角落 |
| `conversation.session.header.utilities` | 会话头部工具区 |
| `conversation.approval.detail` | 审批详情 |
| `workspace.toast` | `0.2.1-alpha.3` 新增：工作区级**通知位**，按既有的业务判别键选择（`keyed` / `root`；`packages/extensions/cordis-client-runner/src/client/slot-catalog.ts` 的 `key: 'workspace.toast'` 条目） |

### 侧栏（sidebar.*）

| 插槽名 | 位置 |
|---|---|
| `sidebar` | 侧栏整体 |
| `sidebar.brand.mark` | 品牌图标（官方 `ui-brand-official` 用它） |
| `sidebar.brand.name` | 品牌文字（同上） |
| `sidebar.settings` | 侧栏设置入口 |
| `sidebar.workspaces` | 侧栏工作区列表 |
| `sidebar.workspaces.directoryFlow` | 侧栏目录选择流 |
| `sidebar.footer.action` | 侧栏底部动作 |
| `sidebar.right.pane.tab` | 右侧面板标签页 |
| `sidebar.right.pane.tab.title` | 右侧面板标签页标题 |
| `sidebar.right.tab.document` | 右侧文档标签 |

### 设置页（settings.*）

| 插槽名 | 位置 |
|---|---|
| `settings.section` | **设置页整段**（社区插件加设置页常注册这里） |
| `settings.general.item` | **通用设置里的一行/一项**（官方 `ui-theme` 用它） |
| `settings.header` | 设置页头部 |
| `settings.action` | 设置页动作区 |
| `settings.close` | 设置页关闭按钮位 |
| `settings.trigger` | 设置页触发入口 |
| `settings.onboarding` | 首次引导 |
| `settings.plugins.tab` | 插件标签页 |
| `plugins.item` | 单个插件的配置条目（**插件页**用，list 语义：`id` + `order` + `label`） |
| `plugins.bundle.config` | 某个 bundle 的配置（keyed：key = bundle 包名） |
| `plugins.row.config` | bundle 里某一行的配置（keyed：key = `<包名>#<行 id>`） |

### 其他

| 插槽名 | 位置 |
|---|---|
| `root` | **内建根插槽**（唯一由 Cordis service 自身渲染的键）。`ui-layout` 被禁用后，整页由它接管 —— 见 T8/根布局玩法 |
| `main` | 主区域 |
| `rightbar` | 右侧栏 |
| `tool.call.toolview` | **工具调用的自定义视图**（工具插件想画专属卡片就用它） |
| `tool.call.images` | 工具调用里的图片 |

> 💡 **对新手最重要的三个**：`settings.section`（加设置页）、`settings.general.item`（加设置项）、`conversation.view`（整块替换对话视图，最激进）。

---

## 附：UI 插件的三条硬约束（实测 + 官方文档）

1. **`dsh.client` 与 `exports["./client"]` 必须成对存在**。缺任一个，客户端半侧不会被组装（宿主报 `client package failed to compose`）。
2. **浏览器半侧里 `@deepseek-ai/*` 只能写 `import type`**。要用值只允许**平台种子表**里的 9 个 specifier（全名）：`react`、`react/jsx-runtime`、`react-dom`、`react-dom/client`、`@deepseek-ai/cordis`、`@deepseek-ai/dsh-client-store`、`@deepseek-ai/dsh-client-ui-slots`、`@deepseek-ai/dsh-client-ui-primitives`、`@deepseek-ai/dsh-client-ui-dockkit`；个别包另有需要的在 `dsh.client.external` 精确追加。越界会报：
   `client bundle purity: "..." is not in the default client externals or <id>'s dsh.client.external, an inline-safe wire layer, or a generated /remote contribution`
   （权威来源与两道门禁的区别见 `14-inbound-http-and-timers.md` §17.3）
3. **跨插件协作走服务或插槽，不要 `import` 别人的实现**（客户端 bundle 纯度门）。

---

## 附：官方 `packages/AGENTS.md` 对写插件的硬约束（原文摘录）

**来源**：`deepseek-harness/packages/AGENTS.md`（27 行，官方对"包/插件"的强制约定）。

> 🔴 **`0.2.1-alpha.1` 变更（blob `f0c49d55` → `8c071dac`，28 → 27 行）**：① 原「**Publish `./invariant` only for diverging observations.** …」**整条已删除**；② 「**Package tsconfig**」规则里 `references runtime-diagnostics/invariants only when the package publishes ./invariant` 子句也已去掉。→ **新写插件不必再考虑 `./invariant` 这套发布约定**（历史素材里出现的 `exports["./invariant"]` 只适用于仓库内既有包，别照抄）。

### 前 3 条是新手必读（逐字）

> - **Plugin exports:** service packages default-export their service class; function plugins named-export `name` / `inject` / `Config` / `apply` and have no default export. Mixing the forms makes the Loader discard the function plugin's namespace ([postmortem](../docs/postmortem/0001-acp-default-export-drops-inject.md)).

> - **Optional services use `ctx.get(name)`.** Reserve `ctx.<name>` for declared injections; the property proxy is topology-sensitive, while strict `ctx.get` reads the global service store ([postmortem](../docs/postmortem/0001-acp-default-export-drops-inject.md)).

> - **Product-visible plugins require a non-unit REAL-composition test.** Hand-built `ctx.plugin(...)` suites are insufficient. Boot test-only `cordis.yml` through the Loader and app/process; mock only external services or nondeterministic inputs and assert model-visible, durable, or user-visible output. Keep opt-ins out of shipped defaults. [Policy](../docs/testing.md).

**翻译成人话**：

| 规则 | 一句话 |
|---|---|
| R-1 导出形态不能混 | **函数式插件** = 具名导出 `name`/`inject`/`Config`/`apply`，**绝不能有 default export**；**服务式插件** = default export 服务类。混用 → Loader **静默丢弃**你的命名空间（插件看起来装上了但不工作）。 |
| R-2 可选服务用 `ctx.get('x')` | 只有**声明过的**依赖才能写 `ctx.x`；探测"有没有"一律用 `ctx.get('x')`。 |
| R-3 面向用户可见的插件必须有真组合测试 | 只手搓 `ctx.plugin()` 不算；要真跑一遍 Loader + 应用，断言"模型可见 / 持久化 / 用户可见"的输出。 |

### 其余规则（对插件作者有约束力的）

> - **Initiator-owned private chains derive, then capture.** ... Keep `Agent` and `Session` explicit at lifecycle, session-log, service, authority, worker/process, persistence, and wire interfaces ...
> - **Represent one asynchronous operation with one lifecycle controller or transaction.** ... otherwise fold it while preserving rollback, callback containment, and quiescence.
> - **Design Service Definitions for all current Consumers.** Keep tool-schema, Loader, UI, transport, and provider-specific behavior in the Consumer or provider; do not let one Consumer dictate the service contract. Inverse smell: a public service method with one internal caller — pass a private capability closure instead.
> - **Require a current owner and need.** Tie each abstraction, state machine, option, defensive copy, and compatibility path to a current contract or production consumer ...
> - **Require evidence for public choices.** Configurability does not justify an unsupported default, public operation set, format, or imported external concept ...
> - **Write model-facing contracts from the model's perspective.** Prompts, tool schemas, results, and diagnostics contain only task-relevant concepts, not UI, transport, or implementation vocabulary.
> - **Enforce a decision in the operation that makes it.** Schema omission, prompt filtering, facades, wrappers, and listener order are not enforcement when direct or alternate callers can bypass them; test denial through the executor.
> - **Publish state only at its commit point.** Emit each notification and update derived state only after the operation succeeds ...
> - **Apply bounds to the complete result.** Enforce byte, token, item, and time limits where the complete emitted or retained value, including wrappers and metadata, is known ...
> - **Registry contributions prove disposal** through the HMR-safety test required by testing policy: **dispose the fiber and observe removal.**
> - **Specs run concurrently** in forked workers beside other gate processes. Own each acquired port, path, and child process through teardown; **a spec that passes only when run alone is a defect in the spec**.

### 命名与目录约定（逐字）

> - **Package tsconfig:** extends `tsconfig.base.json` (Client: `tsconfig.base.client.json`), sets `rootDir: src` and `outDir: lib/types`, references workspace dependencies ...
> - `src/types.ts` contains only types — no runtime code.
> - Tests live at package level under `tests/`, not `src/__tests__/`.
> - Update package README and JSDoc contracts in the same commit as behavior ...

**目录约定速查（可以直接照抄的结构）**：

```
my-plugin/
├── package.json
├── tsconfig.json          # extends tsconfig.base.json（客户端插件用 tsconfig.base.client.json）
├── tsdown.config.ts       # 只有客户端插件需要
├── cordis.patch.yml       # 只有组合包需要
├── README.md / README.zh.md
├── src/
│   ├── index.ts           # 宿主半侧：apply()
│   ├── types.ts           # 只放类型，不放运行时代码
│   └── client/            # 客户端半侧（UI 插件才有）
│       ├── index.ts       # apply(ctx) + inject
│       ├── Xxx.tsx
│       └── Xxx.module.css
└── tests/                 # 测试放这里，不是 src/__tests__/
    └── my-plugin.spec.ts
```

> ⚠️ `README.zh.md` / `README.i18n.yaml`：官方每个包都有中英双份 README + 一份 i18n 索引。第三方插件不强制，但**若想被官方精选清单收录，README 是硬门槛**。

---

## 附：🔴 上游**随产品自带**的开发 skill 与官方模板（`0.1.7-rc.1` 新增，`0.2.0-rc.1` / `0.2.1-alpha.1` 两次扩员 —— 别错过）

> 本节由 **2026-09-23 复核补入**：本轮首轮六维度差异**整块漏掉了它**。重要性与本册同级 —— **上游现在自己发布了一套插件开发技能与模板**，随 `dsh-agent-preset` 包装到用户机器上。

**位置**：`packages/preset/agent-preset/skills/`（旧基线**完全没有**该目录；`0.1.7-rc.1` 由 `d1e22a7e24 feat(preset): declare Agent compositions in profile YAML (#4569)` 一次引入 15 个文件，`0.2.0-rc.1` 再增至 17 个文件，`0.2.1-alpha.1` 再增至 **21 个文件 / 4 个 skill**）

| 官方 skill | 覆盖什么 | 规模 |
|---|---|---|
| **`cordis-plugin-development`** | **持久化插件 / MCP 连接的编写、安装、配置、调试** —— 本册的官方对应物。流程：先写进工作区 → 用 `plugin_manager` 装 → **拿插件本身当第一版预览**（首装前不得造预览 HTML / mock 外壳 / 截图脚本）→ 验证 → 同插件内修缺陷 | `SKILL.md` + `references/{host-plugin,mcp-bundle,practices,ui-plugin,verification,user-actions}.md` + **`templates/{mcp,decoration}/`**（`user-actions.md` 为 **`0.2.0-rc.1` 新增**；**`0.2.1-alpha.1` 起两个模板各补 `icon.svg` + `locale/en.json`**） |
| `agent-experience` | **怎么写「模型可见」的工具定义**：参数说明放参数上、每条事实只说一次、删掉模型能从调用结果学到的约束、优先有界输出（给 id / 路径让模型再取）、把可能的邻近上下文随结果一起给并**显式标注截断**；也讲技能与上下文加载、以及「省上下文只有不导致更多搜索/重复读才算赚」。**`0.2.0-rc.1` 新增** | `SKILL.md`(30 行) |
| `cordis-composition-reference` | **Loader YAML 方言**（`insert` / 按 id `override` / `group` / `disabled` / `isolate` / `!!js`）+ **可安装包清单** | `SKILL.md`(29 行) + `packages/preset/agent-preset/skills/cordis-composition-reference/references/packages.md`(**501 行**) |
| `editing-cordis-compositions` | agent preset 的改动流程 | `SKILL.md`(84 行) |

### 🔴 `0.2.0-rc.1` 新增的官方约定：**一个操作，两个调用者**（`packages/preset/agent-preset/skills/cordis-plugin-development/references/user-actions.md`）

上游第一次把「**插件 UI 的操作也该暴露给 agent**」写成正式约定。三条要点（原文要点，非逐字翻译）：

1. **一次实现，两处调用**：把操作实现成**宿主服务方法**（返回结果或显式状态，失败带原因）→ UI 动作经客户端可调的宿主入口（如 session command，用 `ctx.remote.commands.execute()` 执行）调用它并显示失败 → **agent 工具用相同的参数与语义**调**同一个方法**，把结果原样作为工具结果返回。相关操作可共用一个工具，用 `action` 参数区分。
2. **授权类动作只能给用户**：批准一次工具调用、回答 agent 提出的问题、放松某项策略 —— 这类「授予或确认权限」的动作**必须 user-only**，**agent 不得自行执行或授权**。
3. **不要在 UI 路径和工具路径里各写一份逻辑**；两侧必须共用同一个服务方法。

**怎么验**（原文的 Verification 段）：对两者都可用的操作，**只经工具**执行一遍，把状态变化、返回值、失败与 UI 动作**逐项对照**；对 user-only 的动作，**反过来验证 agent 确实无法执行或授权**。

### 🔴 `0.2.1-alpha.1` 新增的官方约定：**显示元数据与图标**（上游 `packages/preset/agent-preset/skills/cordis-plugin-development/references/host-plugin.md` 的 §*Display metadata and icon*）

上游第一次把「**插件该长什么样**」写成安装前必须完成的检查清单 —— 依据是 **Plugin Manager 与 Settings 会在不激活插件的前提下**直接读 `locale/*.json` 里的 `meta.title` / `meta.description` 与 `./icon`。四条要点（原文要点，非逐字翻译）：

1. **i18n 标题与描述必须真实**：在 `locale/en.json` 的 `meta.title` / `meta.description` 写**可辨识的标题 + 能说明能力的描述**；给用户语言及其他支持语言补同样的字段（如 `locale/zh.json`）。**不得留下与最终插件无关的模板文案。**
2. **图标必须原创或可再分发**：自己画，或用许可允许再分发的美术资源，**保留要求的署名**。
3. **导出 + `files` 白名单同步扩**：导出 `./locale/*.json` 与 `./icon`（**保留既有运行时导出**），并把 patch、locales、icon、每个运行时文件都列进 `files`；**新增模块或资源时必须更新它**。打包/发布的包要核对**实际打包清单**；本地目录安装是链接 checkout、`files` **不过滤**链接目录，要看真实文件。
4. **图标必须真能渲染**：校验格式合法、路径与**大小 ≤ 256 KiB**、留在包内（绝对路径、URL、指向包外的符号链接一律拒绝）。**文件名合法 ≠ 字节可渲染。** 支持 SVG / PNG / JPEG / WebP。

> **包根插件 vs 子路径插件**：包根插件可在 `package.json` 顶层声明 `icon`（**优先于 `./icon`**，路径相对 manifest 目录）；子路径插件（如 `my-plugins/search`）**不是包**、从不读 `package.json`，要导出 `./search/locale/*.json` 与 `./search/icon`。包根插件缺字段回落到 `package.json` 的 `name` / `description`，缺图用面板默认美术；元数据畸形会产出诊断并保留合法文本。

**怎么验**（原文的 Verification 段）：装完后在**包详情与插件行**核对标题/描述与**渲染出的图标**（含用户语言）；查元数据诊断与非预期回落。**没有浏览器控制时，只能检查已安装资源并如实报告「渲染未核验」—— 不得仅凭安装成功就宣称视觉通过。**

**官方模板** = 本册 `assets/minimal-*` 的官方对应物，`0.2.1-alpha.1` 起两个模板都带显示资源：`templates/mcp/`（`cordis.patch.yml` 8 行 + `package.json` **9** 行 + `icon.svg` 5 + `locale/en.json` 6）、`templates/decoration/`（`client.js` 22 + `cordis.patch.yml` 3 + `index.js` 2 + `package.json` **21** + `icon.svg` 3 + `locale/en.json` 6）。

> 🔴 **用法的硬约束**（官方 `SKILL.md` 原文）：这些文件在 **Desktop 里位于 `app.asar` 内**，只有 Host 自身的文件读取能打开 —— `ls` / `cat` / `cp` / `cmp`、glob、原生 ripgrep、`node`、pnpm **全部失败**。必须先**用文件读写工具把模板复制进工作区**再装，**绝不就地安装或就地做语法检查**。

### 两条 agent 侧能力面（本册此前完全没写）

**1. `plugin_manager` 工具 —— agent 自己就能装插件，不必走 CLI**（`packages/boot/plugin-manager/src/tools.ts:20`）

- `action`（必填）**共 8 个**：`list_plugins` / `list_bundles` / `set_plugin` / `set_bundle` / `install_bundle` / `remove_bundle` / `list_version_exemptions` / `set_version_exemption`；
- `target` 含义随 action 变（插件条目 id / bundle 包名 / 安装 spec）；`enabled` 用于 set；`approvedBuilds` **只在用户显式同意**跑安装脚本时传；`registry` 指定 npm 源；`offset`/`limit` 分页（1–100，默认 25）；
- 🔴 **每个 action 都需要 `danger-full-access` 权限或本次调用的批准**，且**批准不改变会话权限模式**；改动影响该 profile 的**每个会话**；live profile 立即生效、startup profile 需重启；**DSH peer 依赖不兼容会阻止**安装与激活；
- 🔴 `set_version_exemption` 是**风险操作**：官方文案要求「先警告用户可能的**崩溃与数据丢失**、并取得对该**确切插件与运行时版本**的显式许可」—— 通用安装许可**不算**。
- → 与 `09-agent-pairing.md` 直接相关：结对时 agent 装插件走这条**或** CLI（`dsh plugin --profile <n> add <包>`），而不是让用户手动拷文件。

**2. `cordis_inspect_*` 三件套**（`packages/extensions/tool-cordis/src/index.ts:23,42`）：`cordis_inspect_list`（列 Provider/method）→ `cordis_inspect_query`（按 method 查）。可查 Service 方法、Event 模式、**已挂载插件的 Config JSON Schema**（`Config.listConfigs`：按 `name` 过滤分页目录，再查该 `entry` id → 返回 `packageDir`）、本 agent 可调用的 Tool、实时 Client Slots 与 Theme token。

- ⚠️ **没有裸 `cordis_inspect`**：`docs/subsystems/slots.zh.md:202` 与历史 Agent Notes 里的 `cordis_inspect what:"client"` / `what:"api"` 是**旧简写**，照抄会找不到工具（`04` / `05` 已改为 `cordis_inspect_query`）。
- `Config.listConfigs` 返回的 `packageDir` 是**权威包目录**：官方强调**不要**从 `$DSH_PROFILE_DIR` 猜路径（内置包解析自 dsh 安装目录，profile 装的 bundle 解析自 profile）。
- 顺带：`DSH_PROFILE`（profile 名）/ `DSH_PROFILE_DIR`（其目录，`node_modules` 只含 profile 装的 bundle）在 **profile 启动的 harness 里每次 shell 调用都有**，不带 profile 启动时**不存在**；Bash 读 `$DSH_PROFILE`、PowerShell 读 `$env:DSH_PROFILE`。

### 为什么首轮会漏掉它（判据缺陷，已登记进 SOP §9 与 `13` §2）

六个维度分别看「**包**增删 / `docs/` / 插槽 / 事件 / API / 补丁行」，**没有任何一维覆盖「包内新发布的*非代码资源*」** —— 而 `skills/` 是**既有包 `dsh-agent-preset` 里的目录**：包级 diff 看不见、`docs/` diff 也看不见 → **最大的一处结构性新增静默逃逸**。本节收录它，正是为了把这个盲区堵上。

