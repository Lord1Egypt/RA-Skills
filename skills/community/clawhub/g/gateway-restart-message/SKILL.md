---
name: "Gateway Restart Message"
description: "OpenClaw gateway 重启标准流程：五道校验门(Gate0-4)+自杀进程规避+continuationMessage回执，通用"
tags:
  - gateway
  - openclaw
  - operations
---

# OpenClaw Gateway 重启标准流程

> 适用于任何 OpenClaw agent。涉及 gateway 重启操作时加载并遵循此流程。
> 核心：改 openclaw.json 走五道校验门（Gate0-4），全绿才重启；重启用平台工具托管 + 自动回执，
> 绝不在会话内裸跑会自杀进程的复合命令。

---

## 前置条件

- 仅授权用户（operator）明确确认后才能执行重启
- 修改 openclaw.json 前必须先备份

---

## 五道校验门（Gate0-4，改 openclaw.json 必走）

> 教训：`python3 -m json.tool` 和 `openclaw config validate` 都只验"格式合法"，
> **不验"模型真的能调用"**。曾出现 JSON 合法、config validate 通过，
> 但因为模型只写进 `agents.defaults.models` 白名单、没写进
> `models.providers.<provider>.models[]`，运行时静默 fallback 到别的模型。
> 所以校验必须分门逐层，缺一不可。

### Gate 0 · 官方文档 / 实现核对

改动涉及不确定的配置字段前，先查官方文档或本机实现确认字段名、取值、语义，
不要凭印象改。这是"改对方向"的前提，不能跳。

### Gate 1 · JSON 语法

```bash
cp openclaw.json openclaw.json.bak      # 先备份
python3 -m json.tool openclaw.json > /dev/null
```

- ✅ 通过 → 下一门
- ❌ 失败 → 立即回滚 `.bak`，不准重启，汇报授权用户

### Gate 2 · Schema 校验

```bash
openclaw config validate
```

- 只验配置结构合法，**不代表模型可调用**，通过也要继续 Gate 3

### Gate 3 · 模型可调用性（改动涉及模型/provider/cron model 时必做）

改动只要碰到 `agents.defaults.model`、`agents.defaults.models`、
`agents.list[].model`、或任何 cron 的 `payload.model`，必须逐个核对模型引用
都在 provider 层真正注册：

```bash
openclaw models list          # primary/fallback 引用的模型是否都可用
openclaw models aliases list  # 每个 alias 的目标是否真实存在于 catalog
```

核对要点：
- primary + 所有 fallback，都要能在 `models.providers.<provider>.models[]` 找到注册
- 每个 alias 的目标模型必须真实存在于 provider catalog（杜绝"白名单有、catalog 无"的半注册）
- cron 的 payload.model 逐个核对，别只查主 agent 配置

任一模型引用查不到 provider 注册 → 视为失败，先补齐注册再重启。

### Gate 4 · 执行重启

Gate0-3 全绿 + 授权用户已确认 → 才能进入本门。见下节"如何重启"。

---

## 如何重启 —— 优先用平台工具，不要在会话里裸跑 shell

> 教训：**不要在 agent 会话内直接执行 `openclaw gateway stop && openclaw gateway start`。**
> `stop` 一旦生效会立即杀掉当前 agent 自己的进程，`&&` 后面的 `start` 根本没机会执行，
> 也拿不到返回值——结果是只 stop 没 start，要人工补 start。

**做法 A（推荐）：调用 gateway 工具，平台托管重启 + 自动回执**

```
gateway restart:
  note: "简短说明本次改动内容"
  continuationMessage: "重启完毕。[改动简述]，[后续状态]。"
```

gateway 工具由平台在新进程里托管重启，`continuationMessage` 在重启后由**新进程自动投递**，
不依赖被杀掉的旧进程。这是会话内触发重启唯一安全的方式。

**做法 B（会话外 / 确需 shell）：单条 `restart`，绝不用 `stop && start`**

```bash
openclaw gateway restart
```

单条 `restart` 是原子操作，不会在两步之间自杀。但发出后当前进程仍会被终止——
**不能在同一回合声称"重启成功"**，只能说"已发出重启指令"，由新进程或事后检查确认结果。

**会话内自触发重启的授权条件（三者同时满足）：**
1. Gate0-4 全绿
2. 授权用户已明确确认本次改动
3. 走做法 A（gateway 工具 + continuationMessage），而非裸 shell

不满足任一条 → 走会话外 / 外部终端手动重启。

**continuationMessage 铁律：**
- 必填，不能省略
- 内容 = 重启完毕 + 改动摘要 + 后续状态
- 示例：`重启完毕。fallback 链已从 A 模型切到 B 模型，下次定时任务会走新链。`

---

## 重启后

- 需要补充说明 → 用 message 工具再发一条；不需要 → continuationMessage 已足够
- 涉及模型 / provider 改动的，重启后再核对一次运行时实际生效的模型，确认没有静默 fallback

---

## 为什么这样做

| 问题 | 解法 |
|------|------|
| 改错 JSON 导致 gateway 起不来 | Gate1 备份 + JSON 语法校验 |
| 配置结构不合法 | Gate2 schema 校验 |
| JSON 合法但模型没注册，运行时静默 fallback | Gate3 模型可调用性校验 |
| 会话内 `stop && start` 自杀进程，start 没跑 | 用 gateway 工具托管重启，或单条 `restart` |
| 重启后不知道好了没 | continuationMessage 自动回执 |

---

## systemd 警告

**systemd override.conf 绝对不允许自行修改**（改错会失联）。

---

## 变更记录

- **v1.2.0**：校验流程整理为五道门 Gate0-4（新增 Gate0 文档核对、Gate2 schema 校验）；
  全文角色中性化，去除特定部署的私有称呼，适配所有 OpenClaw 用户。
- **v1.1.0**：新增模型可调用性校验、self-restart 自杀进程规避、自触发授权条件、重启后模型生效复核。
- **v1.0.0**：备份 → JSON 校验 → continuationMessage 回执重启 → systemd 禁改。
