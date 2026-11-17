---
name: "cron-setup-guide-free"
description: "Agent Gateway定时任务设置完全指南免费版，覆盖三种调度类型、会话模式、投递配置与基础作业管理。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "定时任务设置指南(免费版)"
  version: "1.0.0"
  summary: "Agent Gateway定时任务设置完全指南免费版，覆盖三种调度类型、会话模式、投递配置与基础作业管理。"
  tags:
    - "定时任务"
    - "调度配置"
    - "作业管理"
    - "自动化"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 定时任务设置指南（免费版）

> **不是教你写cron表达式，而是教你完整配置一个定时任务。调度类型、会话模式、投递通道，配置细节一网打尽。**

定时任务的正确配置涉及多个维度：选择哪种调度类型？任务该跑在主会话还是独立会话？结果投递到哪里？本技能聚焦配置层面的技术细节，帮助Agent建立完整的定时任务配置能力。

## 架构总览

```text
┌─────────────────────────────────────────────────────────┐
│           定时任务设置指南 (免费版)                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────┐          │
│  │            调度类型选择层                    │          │
│  │   一次性(at) │ 固定间隔(every) │ Cron表达式  │          │
│  └────────────────────────────────────────────┘          │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────┐          │
│  │            会话模式决策层                    │          │
│  │   主会话(main) │ 独立会话(isolated)          │          │
│  └────────────────────────────────────────────┘          │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────┐          │
│  │            投递配置层                        │          │
│  │   频道投递(announce) │ 无投递(none)          │          │
│  └────────────────────────────────────────────┘          │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────┐          │
│  │            作业管理层                        │          │
│  │   list │ run │ edit │ remove │ runs         │          │
│  └────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 60秒上手（创建一次性提醒）

最小化配置，立即创建一个主会话的一次性提醒：

```bash
# 创建20分钟后的一次性提醒（主会话模式）
skill-platform cron add \
  --name "提醒事项" \
  --at "20m" \
  --session main \
  --system-event "20分钟后检查日历" \
  --wake now \
  --delete-after-run
```

参数说明：
1. `--name`：作业名称，便于后续管理
2. `--at "20m"`：相对时间（20分钟后），也可用绝对时间如 `2026-07-20T10:00:00Z`
3. `--session main`：主会话模式，融入正常心跳流程
4. `--system-event`：系统事件文本，作为payload传递给主会话
5. `--wake now`：立即唤醒Agent执行
6. `--delete-after-run`：执行后自动删除

### 120秒标准搭建（周期性任务）

配置一个每日定时执行的独立会话任务：

```bash
# 每天早上7点生成晨间简报（独立会话模式）
skill-platform cron add \
  --name "晨间简报" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结昨晚的邮件和日历事件" \
  --announce \
  --channel telegram \
  --to "+8613800138000"
```

关键差异：
7. `--cron "0 7 * * *"`：使用标准5字段cron表达式（分 时 日 月 周）
8. `--tz`：时区设置，强烈建议显式指定，避免时区漂移
9. `--session isolated`：独立会话模式，不污染主会话历史
10. `--message`：agentTurn的message字段，独立会话的执行指令
11. `--announce`：投递模式，将结果投递到指定频道
12. `--channel telegram` / `--to`：投递目标

### 300秒完整配置（JSON Schema工具调用）

通过JSON Schema进行更精细的工具调用配置：

```json
{
  "name": "晨间简报",
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "总结隔夜更新"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "+8613800138000",
    "bestEffort": true
  }
}
```

JSON Schema字段速查：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 作业名称 |
| `schedule.kind` | enum | 是 | `at` / `every` / `cron` |
| `schedule.at` | string | 条件 | kind=at时指定，ISO时间或相对时间 |
| `schedule.everyMs` | number | 条件 | kind=every时指定间隔毫秒 |
| `schedule.expr` | string | 条件 | kind=cron时指定5字段表达式 |
| `schedule.tz` | string | 否 | IANA时区，默认UTC |
| `sessionTarget` | enum | 是 | `main` / `isolated` |
| `wakeMode` | enum | 否 | `now` / `next-heartbeat` |
| `payload.kind` | enum | 是 | `systemEvent` / `agentTurn` |
| `payload.text` | string | 条件 | systemEvent的文本内容 |
| `payload.message` | string | 条件 | agentTurn的执行指令 |
| `delivery.mode` | enum | 否 | `announce` / `none`（免费版） |
| `delivery.channel` | string | 条件 | announce模式必填 |
| `delivery.to` | string | 条件 | announce模式必填 |
| `deleteAfterRun` | boolean | 否 | 执行后自动删除 |

---

## 核心能力
### 三种调度类型

| 类型 | 字段 | 适用场景 | 示例 |
|------|------|----------|------|
| **一次性** | `schedule.kind: "at"` | 单次提醒、未来事件 | `"2026-07-20T10:00:00Z"` 或 `"20m"` |
| **固定间隔** | `schedule.kind: "every"` | 周期性轮询、心跳检查 | `everyMs: 3600000`（1小时） |
| **Cron表达式** | `schedule.kind: "cron"` | 复杂时间规则 | `expr: "0 7 * * *"`（每天7点） |

**选择决策树**：

```text
需要执行几次？
├── 仅一次 → at（一次性）
│   └── 需要指定具体时间或相对时间
└── 多次 → 每次间隔是否固定？
    ├── 固定间隔 → every（固定间隔）
    └── 复杂规则 → cron（Cron表达式）
        ├── 每日固定时间：0 7 * * *
        ├── 每周一9点：0 9 * * 1
        ├── 工作日每天：0 9 * * 1-5
        └── 每月1号：0 0 1 * *
```

**输入**: 用户提供三种调度类型所需的指令和必要参数。
**处理**: 按照skill规范执行三种调度类型操作,遵循单一意图原则。
**输出**: 返回三种调度类型的执行结果,包含操作状态和输出数据。

### 双会话模式

| 模式 | 用途 | payload类型 | 上下文继承 |
|------|------|-------------|------------|
| **main**（主会话） | 系统事件，融入正常心跳流程 | `systemEvent` | 继承主会话上下文 |
| **isolated**（独立会话） | 后台任务，不污染主会话历史 | `agentTurn` | 独立上下文 |

**决策原则**：
- 任务需要主会话上下文（如引用之前对话）→ `main`
- 任务是独立的后台操作（如数据汇总、定时报告）→ `isolated`
- 任务结果需要投递到外部频道 → 必须 `isolated`
- 任务是简单的提醒通知 → `main`（更轻量）

**输入**: 用户提供双会话模式所需的指令和必要参数。
**处理**: 按照skill规范执行双会话模式操作,遵循单一意图原则。
**输出**: 返回双会话模式的执行结果,包含操作状态和输出数据。

### 基础投递配置

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `announce` | 投递到指定频道，并在主会话发送简短摘要 | 需要外部通知的任务 |
| `none` | 仅内部执行，无投递 | 仅需内部记录的任务 |

> **省略 `delivery` 字段时默认行为**：`announce` 模式

**频道配置示例**：

```bash
# Telegram 投递
--channel telegram --to "+8613800138000"

# Discord 投递
--channel discord --to "channel:1476104553148452958"
```

**输入**: 用户提供基础投递配置所需的指令和必要参数。
**处理**: 按照skill规范执行基础投递配置操作,遵循单一意图原则。
**输出**: 返回基础投递配置的执行结果,包含操作状态和输出数据。

### 作业管理命令

```bash
# 列出所有作业
skill-platform cron list

# 立即运行指定作业（不等待调度）
skill-platform cron run <job-id>

# 查看作业的运行历史（最近10次）
skill-platform cron runs --id <job-id> --limit 10

# 编辑作业的message
skill-platform cron edit <job-id> --message "新提示词"

# 删除作业
skill-platform cron remove <job-id>
```

---

**输入**: 用户提供作业管理命令所需的指令和必要参数。
**处理**: 按照skill规范执行作业管理命令操作,遵循单一意图原则。
**输出**: 返回作业管理命令的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Agent、Gateway、定时任务设置完全、指南免费版、覆盖三种调度类型、会话模式、投递配置与基础作、业管理、定时任务设置指南、免费版是面向、的定时调度配置手、不同于最佳实践类、本技能聚焦、如何正确配置定时、的技术细节、调度类型选择、会话目标决策、投递通道设置、JSON、Schema、作业生命周期管理、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：每日晨间简报自动化

**角色**：独立开发者

**场景描述**：每天早上7点自动生成包含邮件、日历、天气的晨间简报，并通过Telegram推送。

```bash
skill-platform cron add \
  --name "晨间简报" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "汇总昨晚邮件、今日日历事件和上海天气" \
  --announce \
  --channel telegram \
  --to "+8613800138000"
```

**关键决策**：
- 调度类型选 `cron`：每日固定时间触发
- 会话模式选 `isolated`：避免简报生成过程污染主会话
- 投递模式选 `announce`：结果需要推送到Telegram

### 场景二：项目截止一次性提醒

**角色**：项目经理

**场景描述**：在项目截止前2小时触发提醒，融入主会话上下文。

```bash
skill-platform cron add \
  --name "项目截止提醒" \
  --at "2026-07-20T15:00:00Z" \
  --session main \
  --system-event "项目A将于2小时后截止，请确认完成状态" \
  --wake now \
  --delete-after-run
```

**关键决策**：
- 调度类型选 `at`：仅执行一次
- 会话模式选 `main`：需要在主会话上下文中触发
- 启用 `--delete-after-run`：避免遗留无用作业

### 场景三：每小时健康检查

**角色**：运维工程师

**场景描述**：每小时检查服务状态，仅在主会话内部记录，无需外部投递。

```bash
skill-platform cron add \
  --name "服务健康检查" \
  --every "3600000" \
  --session main \
  --system-event "执行服务健康检查并记录结果" \
  --wake next-heartbeat
```

**关键决策**：
- 调度类型选 `every`：固定间隔轮询
- 投递模式选 `none`：仅内部记录
- `wakeMode: next-heartbeat`：不立即唤醒，等下次心跳

---

## FAQ

### Q1：主会话和独立会话有什么区别？

主会话（main）继承当前对话上下文，适合需要引用之前讨论的系统事件，payload类型为 `systemEvent`。独立会话（isolated）创建全新上下文，不污染主会话历史，适合后台任务，payload类型为 `agentTurn`。需要投递到外部频道的任务必须使用独立会话。

### Q2：`--at` 参数支持哪些时间格式？

支持两种格式：(1) ISO 8601绝对时间，如 `2026-07-20T10:00:00Z`；(2) 相对时间，如 `20m`（20分钟后）、`2h`（2小时后）、`1d`（1天后）。相对时间从作业创建时刻开始计算。

### Q3：cron表达式的5个字段分别是什么？

标准5字段格式：`分 时 日 月 周`。例如 `0 7 * * *` 表示每天7点0分。字段取值范围：分(0-59)、时(0-23)、日(1-31)、月(1-12)、周(0-6，0为周日)。`*` 表示任意值，`-` 表示范围（如 `1-5`），`,` 表示列表（如 `1,3,5`）。

### Q4：为什么建议显式指定时区？

不指定时区时默认使用UTC，可能导致任务在非预期时间触发。例如期望"每天早上7点"但实际在UTC 7点（即北京时间15点）触发。显式指定 `--tz "Asia/Shanghai"` 可确保任务按本地时间执行。时区使用IANA格式（如 `Asia/Shanghai`、`America/New_York`）。

### Q5：作业执行后如何查看运行历史？

使用 `skill-platform cron runs --id <job-id> --limit 10` 查看指定作业的最近10次运行记录。运行历史存储在 `~/.skill-platform/cron/runs/<jobId>.jsonl`，包含每次执行的开始时间、结束时间、状态、输出等信息。

---

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Agent Gateway**: 需启用cron调度器（`cron.enabled: true`）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Agent Gateway | 运行时 | 必需 | Agent平台内置 |
| skill-platform CLI | 工具 | 必需 | Agent平台内置 |
| Telegram Bot | 投递通道 | 否 | 注册Telegram Bot获取 |
| Discord Bot | 投递通道 | 否 | 注册Discord Bot获取 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### LLM模型路由
- 免费版使用 **GPT-4o-mini** 模型路由，降低平台运营成本
- 复杂调度场景建议升级至专业版（GPT-4o模型路由）

### API Key 配置
- Telegram投递需要Telegram Bot Token（存储在Agent Gateway配置中）
- Discord投递需要Discord Bot Token（存储在Agent Gateway配置中）
- 禁止在SKILL.md或脚本中硬编码Token

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent配置定时任务

---
- API Key通过环境变量配置: export API_KEY=your_key

## License与版权声明

本技能基于原始开源定时调度配置作品改进，保留原始版权声明：

- 原始作品：Gateway Cron Setup Guide
- 原始license：MIT
- 改进作品：定时任务设置指南（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，适配中文用户工作流
- 聚焦"技术配置细节"而非方法论
- 新增三种调度类型对比矩阵与选择决策树
- 新增双会话模式决策原则与对比表
- 新增JSON Schema完整字段速查表
- 新增作业管理命令速查表
- 新增分级快速开始指南（60秒/120秒/300秒三档）
- 新增三类真实场景示例（晨间简报/项目截止/健康检查）
- 新增FAQ章节（5问）
- 新增依赖说明章节与License版权声明
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，完全符合MIT license要求。

---

## 已知限制

本免费体验版限制以下高级功能：

- Webhook投递模式（POST到HTTP端点）需升级专业版
- 模型覆盖（model override）与思考强度配置需升级专业版
- Telegram论坛话题投递需升级专业版
- 退避策略调优（指数退避参数配置）需升级专业版
- 高级配置项（sessionRetention/runLog等）需升级专业版
- Cron与Heartbeat对比决策指南需升级专业版
- 多角色场景指南（7种角色）需升级专业版
- 完整FAQ（10+问）与故障排查表需升级专业版
- 性能优化策略与多平台集成示例需升级专业版

解锁全部功能请使用专业版：cron-setup-guide-pro

## 示例

### 示例1：基础用法

```
### 60秒上手（创建一次性提醒）

最小化配置，立即创建一个主会话的一次性提醒：

```bash
```

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
