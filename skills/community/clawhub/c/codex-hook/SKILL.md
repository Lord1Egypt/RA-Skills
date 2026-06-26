---
name: Codex Hook
description: OpenClaw 智能任务执行系统 - 支持任务派发、执行、监控（精简版）
license: MIT-0
version: 1.1.1
---


### 核心脚本
| 脚本 | 功能 | 状态 |
|------|------|------|
| task-execute.sh | 单任务派发（推荐） | ✅ |
| codex-tasks.sh | 任务管理入口 | ✅ |
| task-registry.sh | 任务注册表 | ✅ |
| task-monitor.sh | 任务监控 | ✅ |
| notify.sh | 通知系统 | ✅ |
| auto-merge.sh | 自动合并 | ✅ |
| codex-progress-reporter.sh | 进度汇报 | ✅ |
| task-dispatcher.sh | 任务调度器（高级） | ⚠️ 可选 |

### Worktree 管理策略

**复用逻辑**：
- 关联任务（同一项目）→ 复用现有 worktree
- 独立任务 → 新建 worktree

**合并命令**：
```bash
# 1. 在 worktree 中提交
git add .
git commit -m "feat: 描述"

# 2. 推送分支
git push -u origin <branch>

# 3. 创建 PR（需要手动或用 gh）

## 架构

```
OpenClaw (编排层) → codex-hook (执行层)
       ↓                    ↓
    拆解任务              并行执行
       ↓                    ↓
    子任务列表            tmux 隔离
       ↓                    ↓
    调用 codex-hook       监控+干预
                           ↓
                        自动合并
```

## 依赖

- `bash` - 执行脚本
- `jq` - JSON 处理
- `tmux` - 任务隔离（可选）
- `gh` - GitHub CLI（自动合并需要）
- `codex` - Codex CLI
- `curl` - 发送通知

## 安装

脚本已位于：`~/.openclaw/skills/codex-hook/scripts/`

建议添加 alias 到 shell 配置：
```bash
# ~/.zshrc 或 ~/.bashrc
alias codex-tasks='bash ~/.openclaw/skills/codex-hook/scripts/codex-tasks.sh'
```

## 快速开始

```bash
# 1. 初始化
codex-tasks init

# 2. 执行任务（OpenClaw 拆解后调用）
codex-tasks execute parent-login '[{"name":"后端API","description":"实现登录API"},{"name":"前端","description":"实现登录页"}]'

# 3. 查看状态
codex-tasks status
```

## 核心文件

```
~/.openclaw/skills/codex-hook/scripts/
├── codex-tasks.sh       # 统一入口
├── task-registry.sh     # 任务注册表
├── task-dispatcher.sh   # 任务调度器
├── auto-merge.sh       # 自动 PR 创建、CI、检查、合并
├── task-monitor.sh      # 任务监控
└── task-splitter.sh    # 任务拆解（预留）
```

## 命令说明

| 命令 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `init` | `i` | 初始化任务系统 | `codex-tasks init` |
| `execute` | `run` | 接收子任务并执行 | `execute p1 '[{"name":"API"}]'` |
| `add-subtask` | `add` | 添加单个子任务 | `add p1 "API" "实现登录"` |
| `start` | - | 开始执行所有子任务 | `start p1` |
| `status` | `list` | 查看状态 | `status` / `status task-xxx` |
| `monitor` | `watch` | 实时监控面板 | `monitor` |
| `check` | - | 单次检查任务状态 | `check` |
| `intervene` | `send` | 干预任务 | `intervene t-xxx "消息"` |
| `stop` | `kill` | 停止任务 | `stop t-xxx` |
| `logs` | `log` | 查看日志 | `logs t-xxx` |
| `auto-merge` | `merge` | 自动合并 PR | `auto-merge t-xxx` |
| `report` | - | 汇报完成 | `report t-xxx` |
| `cleanup` | `clean` | 清理已完成任务 | `cleanup 10` |

## 工作流

### 1. OpenClaw 拆解任务

OpenClaw 负责分析需求，拆分为子任务列表：

```json
[
  {"name": "后端API开发", "description": "实现用户登录API"},
  {"name": "前端页面", "description": "实现登录页面"},
  {"name": "单元测试", "description": "编写登录相关测试"}
]
```

### 2. 调用 codex-hook 执行

```bash
# 方式一：一次性接收所有子任务
codex-tasks execute <parent_id> '<子任务JSON>' [workspace]

# 方式二：逐个添加子任务
codex-tasks add-subtask <parent_id> "任务名" "描述"
codex-tasks add-subtask <parent_id> "任务名2" "描述2"
codex-tasks start <parent_id> [workspace]
```

### 3. 监控与干预

```bash
# 查看所有任务
codex-tasks status

# 实时监控
codex-tasks monitor

# 干预任务（发送消息到 tmux）
codex-tasks intervene <task_id> "停下，先做X"

# 停止任务
codex-tasks stop <task_id>

# 查看日志
codex-tasks logs <task_id>
```

### 4. 自动合并与汇报

```bash
# 自动合并 PR (CI检查 → 代码审查 → 合并)
codex-tasks auto-merge <task_id> [repo]

# 汇报完成
codex-tasks report <task_id> [telegram]

# 清理已完成任务
codex-tasks cleanup [保留数量]
```

## 任务注册表

- 位置: `/tmp/codex-tasks/active-tasks.json`
- 包含: 所有任务状态、子任务关系、日志

```bash
# 直接查看 JSON
codex-tasks json

# 清理已完成任务
codex-tasks cleanup 10
```

## 查看任务输出

```bash
# 任务目录
ls /tmp/codex-results/tasks/<task_id>/

# 执行日志
cat /tmp/codex-results/tasks/<task_id>/output.log

# 任务提示词
cat /tmp/codex-results/tasks/<task_id>/prompt.txt
```

## 监控设置 (可选)

```bash
# 方式一：加载环境变量后启动监控
export $(cat ~/.openclaw/.env | xargs) && codex-tasks monitor-start 60 &

# 方式二：直接指定间隔
codex-tasks monitor-start 60 &
```

**注意**：需要先配置通知环境变量才能收到进度/完成通知。

## OpenClaw 集成示例

在 OpenClaw 中使用：

```
你: 实现用户登录功能

OpenClaw (拆解):
→ 分析需求，拆分为子任务
→ 调用 codex-hook 执行
→ 监控任务状态
→ 自动合并 PR
→ 汇报完成
```

## 通知配置

### 方式一：环境变量文件

推荐将配置写入 `~/.openclaw/.env`：

```bash
# ~/.openclaw/.env
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHAT_ID="your-chat-id"
TELEGRAM_TOPIC_ID="123456"  # 可选，Forum 话题 ID
DISCORD_WEBHOOK="https://discord.com/api/webhooks/xxx"
WEBHOOK_URL="https://your-webhook.com/hook"
DEFAULT_CHANNEL="telegram"
```

启动监控时加载：
```bash
export $(cat ~/.openclaw/.env | xargs) && codex-tasks monitor-start
```

### 方式二：环境变量

```bash
# Telegram (用户/群组/话题)
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
export TELEGRAM_TOPIC_ID="123456"  # 可选，Forum 话题 ID

# Discord
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/xxx"

# 通用 Webhook
export WEBHOOK_URL="https://your-webhook.com/hook"

# 默认渠道
export DEFAULT_CHANNEL="telegram"
```

### 通知类型

| 事件 | 通知内容 |
|------|----------|
| 任务开始 | 任务ID、名称、时间 |
| 进度更新 | 进度条 (0-100%)、当前状态 |
| 任务完成 | 任务ID、名称、PR链接、时间 |
| 任务失败 | 任务ID、名称、错误信息 |
| 人工干预 | 干预消息 |

### 快速测试

```bash
# 测试发送
bash notify.sh send telegram "Hello"

# 测试进度条
bash notify.sh bar 50 "处理中..."
```

### tmux 不可用
```
⚠️ tmux 不可用，使用后台执行
```
- 解决：安装 tmux `brew install tmux`

### codex 命令找不到
- 解决：确保 codex 已安装并在 PATH 中

### gh 命令找不到 (自动合并)
- 解决：安装 GitHub CLI `brew install gh`

### Telegram 通知不工作
- 配置环境变量：
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

