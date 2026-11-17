# 能力接缝（Capability Seams）：可替换提供者模式（实测 2026-08，555 文档蒸馏）

> DSH 插件架构最核心的模式。理解它 = 理解"为什么一个提供者替换能改变整个产品"。
> 文档来源：`docs/architecture.md`、`docs/capability-seams.md`（自动生成）、`docs/glossary.md`。

## 1. 定义：seam 是三角色完整能力

> **seam** = 一个可替换的能力，含三个角色：**Service Definition**（声明接口）、
> **Service Provider**（实现接口）、**Consumer**（使用接口，通常是模型可见工具）。
> 单一角色不是 seam；新增能力 = 设计全部三角色。

```
┌────────────────────────────────────────────────┐
│           能力接缝（Seam）= 完整能力             │
│                                                │
│  Service Definition ──声明 ctx.<key>──┐         │
│  （抽象类/注册表，owner 包）            │         │
│                                      ▼         │
│  Service Provider ──────实现─────► ctx.<key>   │
│  （可替换：local/sandbox/e2b...）               │
│                                      │         │
│  Consumer ─────────────inject───────┘         │
│  （模型工具，按名引用不 import 提供方）           │
└────────────────────────────────────────────────┘
```

**为什么重要**：文件系统与子进程提供者共享同一执行世界——把 `ctx.fs` 指向远程沙箱，
Bash/PTY/LSP 全部跟着走，无提供者分叉。这就是"换一个提供者 = 换整个产品"。

## 2. 三角色示例（canonical）

| Seam | Definition（owner） | Providers | Consumers |
|---|---|---|---|
| `ctx.llm` | llm（LLM 适配器注册表）| llm-deepseek, llm-replay | agent-loop, compaction-basic, token-meter |
| `ctx.shell` | shell | bash-local, bash-sandbox | tool-bash, hooks-* |
| `ctx.fs` | fs | fs-local, fs-sandbox, fs-e2b | tool-fs, tool-grep, tool-glob |
| `ctx.subprocess` | subprocess | subprocess-local, subprocess-e2b | bash-local, bash-sandbox |
| `ctx.sessionPersistence` | session-persistence | jsonl, sqlite | tool-bash, hooks-* |
| `ctx.settings` | settings | settings-file | apiproxy, credentials |
| `ctx.web` | web | web-search-exa/perplexity/deepseek, web-fetch-http | tool-web |

**bash 是规范例**：`dsh-shell`（Definition）→ `dsh-bash-local`/`dsh-bash-sandbox`（Providers）→ `dsh-tool-bash`（Consumer）。

## 3. 两种接缝形状：单提供者 vs 命名注册表

```
单提供者（bash 形）          命名注册表（subagent/llm 形）
  ctx 上注册一个执行器          多个提供者各自注册名字
  第二个加载直接 throw          调用方按名挑选
  适合"一台机器一种方式"        适合"多种实现共存"
  (ShellExecutor)              (LlmRuntime.registerAdapter)
```

- **bash seam**：每 ctx 一个 executor，加载第二个抛错——正确（一台机器一种跑法）。
- **subagent seam**（`ctx.subagents`）：**命名提供者注册表**——in-process / ACP / Codex / Claude Code 多种共存，父进程按名选。形状镜像 LLM 注册表，非 bash 形。

### 底层实现：Symbol 隔离

Cordis 在底层用 `Symbol(name)` 作为 store key 来隔离同名服务。同一 scope 下若试图注册同名服务（如重复 `ctx.plugin(BashLocal)`），会抛 `"service has been registered"` 错误。需要让多个同名服务共存时，必须显式调用 `ctx.isolate(name)` 创建新的隔离 scope，此时框架为该 scope 生成新的 Symbol，store 中互不冲突。

## 4. 角色分包惯例

- 角色**通常分属独立包**（各自独立演进）：Definition 一包、Provider 一包、Consumer 一包。
- 一个包可持有多个角色（`dsh-llm` 同时是 Definition + Consumer），当它们是一个关注点时。
- 提供者**注册能力不注册工具**：`dsh-tool-web` 是唯一持有模型可见名/描述/schema/presentation 的包。

## 5. 对插件开发者的意义（如何接入/新造 seam）

**接入现有 seam**（选型，见 [deployment-overview.md](../50-ship/deployment-overview.md) 六形态）：
```ts
// 作为 Provider：实现接口，注册到 ctx.<key>
export const inject = ['llm']
export function apply(ctx: Context) {
  ctx.llm.registerAdapter(['my-provider'], { ... })  // 具体以 Inspect 契约为准
}

// 作为 Consumer：inject 服务，按名引用
export const inject = ['llm']
export function apply(ctx: Context) {
  ctx.llm.stream({ provider: 'my-provider', model: 'x', ... })
}
```

**新造一个 seam**（三角色齐全才算完成）：
1. **Definition**：抽象类/注册表，拥有 `ctx.<key>` 与词汇类型（`declare module` 声明合并）。
2. **Provider**：实现并注册（一个或多个）。
3. **Consumer**：模型工具或服务，`inject` 消费。
> 只有 Definition 而无 Provider/Consumer = 未完成的 seam——除非主干服务（session/tools 等不可替换）。

## 6. 与能力挂载的关系

- **能力接缝** = 服务层可替换性（`ctx.llm` 换适配器）。
- **事件** = 进程内拦截（`agent/pre-step` 拦轮次）——"capability events" 在不产生 import 环的前提下给 seam 挂策略。
- **工具注册**（harness-integration.md）= 模型可见面，消费 seam 的一种形态。
