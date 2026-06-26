---
name: fast-claude-code
description: >
  Claude Code 任务完成回调 Runtime。支持 Single / Interactive / Team 三种模式，
  ⚠️  任务在后台 tmux 会话中运行，完成后通过 System Event 自动通知，无需轮询。
  Use when: 需要运行 Claude Code 任务并在完成时获得通知。
  NOT for: 简单的文件读写（直接用 read/write 工具）。
metadata:
  {
    "openclaw": {
      "emoji": "⚡",
      "os": ["darwin", "linux"],
      "requires": {
        "bins": ["bash", "claude", "tmux"],
        "anyBins": ["openclaw"],
        "optionalBins": ["jq"]
      }
    }
  }
---

# Fast Claude Code ⚡

Claude Code 任务完成自动通知 Runtime。任务在后台 tmux 会话中运行，完成后通过 System Event 自动回调。

## ⚠️ IMPORTANT: Entry Point

**必须使用 `bin/fast-claude-code.sh` 作为入口！**

- ✅ 正确：`bin/fast-claude-code.sh team --project "/path" --template "xxx" --task "xxx"`
- ❌ 错误：直接调用 `bin/send-task.sh` 或 `modes/team.sh`
- ❌ 错误：直接使用 `tmux` 命令

所有操作都通过 `fast-claude-code.sh` 分发，它会：
1. 启动正确的 tmux 会话
2. 安装完成检测机制
3. 等待回调通知

## Use When

- 需要运行 Claude Code 任务并获得完成通知
- 需要多 Agent 协作完成复杂任务（Team 模式）
- 需要长时间运行的 Claude Code 会话（Interactive 模式）

## NOT For

- 简单的文件读写（直接用 read/write 工具）
- 单次简单命令执行

## Quick Start

```bash
# Single 模式 - 一次性任务
bin/fast-claude-code.sh single --task "任务描述" --project "/path/to/project"

# Interactive 模式 - 多轮对话
# - 开启
bin/fast-claude-code.sh interactive --project "/path" --label "session-name" --task "任务描述"
# - 后续（使用 send-task，不要直接用 tmux）
bin/fast-claude-code.sh send-task --session "session-name" --task "任务描述"

# Team 模式 - 多 Agent 协作
bin/fast-claude-code.sh team --project "/path" --template "模板" --task "任务描述"
```

## Modes

| Mode | Use For | Required Params |
|------|---------|-----------------|
| `single` | 单文件重构、简单代码审查、一次性分析 | `--task`, `--project` |
| `interactive` | 长时运行任务、需要多轮对话、需要人工干预 | `--project`, `--label` |
| `team` | 复杂代码审查、架构决策、性能分析、多 Agent 协作 | `--project`, `--template`, `--task` |

## Mode Decision Guide

```
用户任务需要 Claude Code？
├─ 是 → 任务类型？
│   ├─ 一次性（单文件/简单操作）→ Single
│   ├─ 需要多轮对话/长时间 → Interactive
│   └─ 需要多 Agent 协作/复杂分析 → Team
└─ 否 → 不使用此 skill
```

## Team Templates

| Template | Use For | Keywords |
|----------|---------|----------|
| `parallel-review` | 代码审查、安全检查、性能测试 | 审查、安全、性能、测试 |
| `competing-hypotheses` | 问题诊断、调试、找原因 | 调试、问题、原因、为什么 |
| `fullstack-feature` | 全栈功能开发 | 开发、实现、功能、全栈 |
| `architecture-decision` | 架构决策、技术选型 | 架构、选择、对比、决策 |
| `bottleneck-analysis` | 性能瓶颈分析 | 慢、性能、瓶颈、优化 |
| `inventory-classification` | 批量分类、批量分析 | 分析、分类、评估 |
| `simple-dialog` | 简单对话、单 Agent 问答 | 对话、问答、讨论 |

## Parameters

| Parameter | Mode | Description |
|-----------|------|-------------|
| `--task` | Single/Team | 任务描述 |
| `--project` | All | 项目路径（必须） |
| `--label` | Interactive | 会话标识符 |
| `--template` | Team | 模板名称 |
| `--permission-mode` | All | `auto`（默认）或 `plan` |
| `--session` | send-task | 会话名 |
| `--callback` | All | 回调类型（默认 openclaw） |
| `--session-key` | All | OpenClaw gateway session key（必须），指定回调投递的目标会话 |

> ⚠️ **必须从 `session_status` 获取 session-key！**
> 
> 执行前先运行 `session_status` 获取实际返回的 session key（例如 `agent:main:main`），**不要硬编码** "current" 或其他猜测值，否则回调可能无法正确投递。
> 
> 步骤：
> 1. 调用 `session_status` 工具
> 2. 从返回结果中复制实际的 `Session: xxx` 值
> 3. 使用该值作为 `--session-key` 参数

## Settings

### Timeout（Team 模式）

| 复杂度 | 超时 | 场景 |
|--------|------|------|
| 简单 | 默认 1h | 单文件、单模块 |
| 中等 | 默认 1h | 少量文件、标准任务 |
| 复杂 | 7200（2h） | 多模块、跨功能 |
| 超复杂 | 10800（3h） | 全项目、架构级 |

```bash
TEAM_TIMEOUT=7200 bin/fast-claude-code.sh team --project "/path" --template "xxx" --task "xxx"
```

### 环境变量

- `TEAM_TIMEOUT`：Team 模式超时时间（秒）
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`：Team 模式必须设置

## Examples

```bash
# 重构单个文件
bin/fast-claude-code.sh single --task "重构 auth.js 的 JWT 逻辑" --project "/my/project"

# 安全审查（多视角）
bin/fast-claude-code.sh team --project "/my/project" --template "parallel-review" --task "审查安全性"

# 架构决策
bin/fast-claude-code.sh team --project "/my/project" --template "architecture-decision" --task "选择 PostgreSQL 还是 MongoDB"

# 复杂功能开发（设置超时）
TEAM_TIMEOUT=7200 bin/fast-claude-code.sh team --project "/my/project" --template "fullstack-feature" --task "实现用户认证系统"

# Interactive 发送后续任务
bin/fast-claude-code.sh send-task --session "session-name" --task "后续任务"

# Interactive 结束会话
bin/fast-claude-code.sh send-task --session "session-name" --task "exit session"
```

## How It Works

### Single 模式
1. 在 tmux 中启动 Claude Code
2. 执行单次任务
3. 任务完成后通过 callback 通知

### Interactive 模式
1. 创建持久 tmux 会话
2. 可通过 `send-task` 发送后续任务
3. 每次任务完成都触发 callback

### Team 模式
1. 安装 Stop hook 监听完成事件
2. 在 tmux 中启动 Team 模式
3. 主 agent spawn 子 agents 协作
4. 检测 `CC_CALLBACK_DONE` marker 确认真正完成
5. 回调通知并清理资源

## Notes

- 任务在后台 tmux 会话中运行，完成后自动回调
- Team 模式需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Interactive 模式下可用 `send-task` 发送后续任务
- ⚠️ 建议不要在一个项目下并行执行多个 Team 任务

## Callback

任务完成后自动回调，格式：
```
请总结以下 Claude Code 任务的执行结果，并回复用户：

=== 任务信息 ===
模式: model-name
状态: done
任务标识: session-id

=== 用户请求 ===
<USERINPUT>

=== 执行结果 ===
<OUTPUT>
```
