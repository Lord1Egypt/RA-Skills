---
name: auwomo-task
version: 1.5.0
description: >
  任务管理：查看任务上下文、记录进展、创建主线/子线、生成汇报。
  Triggers: 任务, 进展, 记录, 汇报, 主线, 子线, 待办, 日报, 周报, context, record, report, progress,
  做了, 完成了, 修了, 搞定了, 推进了, 今天做的, 帮我记, 写进任务, 工作内容, 今日进展.
  NOT for: 消息发送(use auwomo-message), 提醒配置(暂不支持).
metadata:
  openclaw:
    requires:
      bins:
        - auwomo
        - lark-cli
---

# auwomo-task

围绕飞书任务的长期任务结构、进展记录、汇报能力。所有操作通过 `auwomo` CLI 执行。

## 触发条件

当用户提到以下内容时激活本技能：

- 查看任务、任务进展、任务上下文
- 记录工作、写进展、"帮我记一下"
- 生成日报、周报、汇报
- 创建主线、子线任务
- "看看我的任务"、"check 一下"
- **用户描述做了什么工作**："今天修了 xxx"、"完成了 xxx"、"搞定了 xxx"、"做了 xxx"
  → 这是工作记录请求，走 task-record 流程，**不要写到本地 memory**

## 排除场景

- 只是闲聊、不涉及飞书任务系统 → 不激活
- 发消息给某人 → 转到 `auwomo-message`
- agent→agent 通信 → 暂不支持

## 前置依赖

执行任何操作前，确认身份可用：

```bash
auwomo identity whoami
```

如果返回错误，先解决身份问题再继续。

## 标题前缀契约

| 前缀 | 含义 | 创建方式 |
|------|------|---------|
| `[主线]` | 顶层长期工作主线 | `task create` |
| `[子线]` | 主线下的结构子任务（支持多级） | `task create --parent` |
| `[记录]` | 已完成工作的记录 | `task record` |

## CLI 命令速查表

| 场景 | 命令 | 说明 |
|------|------|------|
| 查看任务上下文 | `auwomo task context --duration 7d` | 轻量模式 |
| 查看详细上下文 | `auwomo task context --duration 7d -d` | 含 description |
| 查看团队上下文 | `auwomo task context --duration 7d --team` | 含下属 |
| 检查是否已初始化 | `auwomo task check init` | 有无可挂载主线 |
| 检查可挂载候选 | `auwomo task check attachable` | 找记录挂点 |
| 检查昨日记录 | `auwomo task check yesterday-record` | 昨天有无进展 |
| 列出任务 | `auwomo task list` | 扁平列表 |
| 查看任务树 | `auwomo task tree` | 完整树状结构 |
| 查看单个任务 | `auwomo task show <guid>` | 详细信息 |
| 记录进展 | `auwomo task record --work <guid> --summary "..."` | 创建记录 |
| 创建任务 | `auwomo task create --title "[主线] ..."` | 创建主线/子线 |

所有命令支持 `--format json` 切换为机器可读输出。

## 参考文档路由

| 场景 | 文档 |
|------|------|
| 需要了解当前任务状态 | [task-context.md](references/task-context.md) |
| 需要记录一段工作 | [task-record.md](references/task-record.md) |
| 需要创建主线/子线 | [task-create.md](references/task-create.md) |
| 需要生成汇报 | [task-report.md](references/task-report.md) |
| 需要做前置检查 | [task-check.md](references/task-check.md) |
| 定时任务模板 | [cron-templates.md](references/cron-templates.md) |

## **数据源：Cotrace**

当用户说"帮我记录"但未提供具体内容时，**优先使用 Cotrace 获取工作数据**。
详见 `skills/cotrace/SKILL.md`。
