---
name: cron-manager-master
description: 定时任务创建通用技能。自动提取当前对话上下文，标准化创建和检查OpenClaw定时任务。
---

# Skill: 定时任务创建通用技能 (Cron-Manager-Master)

## 📋 技能概述

本技能用于在 OpenClaw 系统中标准化、自动化地创建和检查定时任务。技能会智能提取当前对话的上下文信息（通道和用户 ID），实现零配置、无缝创建，确保所有任务符合系统规范。

## 🎯 触发条件

当识别到以下意图时触发本技能：

- "创建定时任务"
- "设置cron任务"
- "openclaw cron"
- "定时任务创建"

## ⚙️ 自动上下文提取（核心特性）

为极大地简化使用流程，本技能**无需用户手动配置或记忆参数**。
在每次触发创建定时任务时，技能会自动从当前会话中提取以下信息：

1. **通道 (channel)** - 从当前会话自动获取（如 `feishu`、`wecom` 等）
2. **用户ID (to)** - 从当前会话自动获取（如 `ou_xxxxxx`）

**实现方式**：
- 从 `session_status` 命令输出中提取 `channel` 和 `user_id`
- 当前会话示例：`feishu:direct:ou_xxxxxx`

## 📝 核心工作流

### 步骤 1：识别任务需求与目标

- 明确任务名称、执行时间（一次性或周期性）、消息内容
- 自动读取当前会话的 `channel` 和 `user_id`

### 步骤 2：执行创建命令

请严格使用以下命令格式，技能会自动填充当前会话的上下文：

**一次性任务（指定具体时间）**

```bash
openclaw cron add \
  --name "<任务名称>" \
  --at "<YYYY-MM-DDTHH:mm:ss+08:00>" \
  --session isolated \
  --message "<消息内容>" \
  --announce \
  --channel feishu \
  --to "ou_xxxxxx"
```

**周期性任务**

```bash
openclaw cron add \
  --name "<任务名称>" \
  --cron "<cron表达式>" \
  --session isolated \
  --message "<消息内容>" \
  --announce \
  --channel feishu \
  --to "ou_xxxxxx"
```

### 步骤 3：参数规范检查（创建前自检）

| **参数**               | **状态** | **规范要求**             |
| -------------------- | ------ | -------------------- |
| `--name`             | ✅ 必需   | 任务名称，必须清晰明确          |
| `--at`/`--cron`      | ✅ 必需   | ISO 时间格式或标准 cron 表达式 |
| `--session isolated` | ✅ 必需   | 必须使用独立会话隔离执行环境       |
| `--message`          | ✅ 必需   | 要发送的提醒或消息内容          |
| `--announce`         | ✅ 必需   | 启用消息发送功能             |
| `--channel`          | ✅ 自动   | 从当前会话自动获取通道值         |
| `--to`               | ✅ 自动   | 从当前会话自动获取用户 ID 值     |

### 步骤 4：创建后系统验证

任务创建完成后，必须执行验证命令检查任务状态：

```bash
# 使用jq精确匹配任务名称
openclaw cron list --json | jq '.[] | select(.name == "<任务名称>")'
```

**验证要点**：
1. 检查 `"sessionTarget": "isolated"`
2. 检查 `"delivery": {"mode": "announce"}`
3. 检查 `"channel": "feishu"`（或其他正确通道）
4. 检查 `"to": "user:ou_xxxxxx"`（格式正确）
5. 检查时间格式正确（ISO 8601 UTC时间格式）

## ✅ 自动化规范检查清单

创建任务后，必须立即执行以下检查：

- [ ] `--session isolated`参数 → 检查 `"sessionTarget": "isolated"`
- [ ] `--announce`参数 → 检查 `"delivery": {"mode": "announce"}`
- [ ] 指定了正确的`--channel` → 检查 `"channel": "feishu"`（或其他正确通道）
- [ ] 包含用户ID → 检查 `"to": "user:ou_xxxxxx"`（格式正确）
- [ ] 时间格式正确 → 检查 ISO 8601 UTC时间格式
- [ ] 任务名称清晰明确 → 检查 `"name"` 和 `"description"`

## 🚨 错误处理与操作红线

### 核心红线

- **严禁私自操作系统服务**：如遇到 Gateway 连接失败或服务异常，必须先请求人工授权，禁止私自重启服务或变更底层配置
- **承诺必须兑现**：收到任务指令后必须实际创建自动化机制，不得仅作口头回复
- **Gateway重启必须确认**：Gateway 重启是重要操作，必须让用户确认后再执行

### 监控与告警

1. **执行前检查**：重要任务需在执行前提前 30 分钟检查系统运行状态（包括脚本、目录和权限）
2. **失败主动报告**：如创建任务失败或定时任务执行超时（超过 5 分钟），需立即主动报告问题并提供备选方案（如询问是否立即手动执行）
3. **日志记录**：将所有的检查结果、操作记录或异常情况记入系统的 `memory` 或日志文件中以便复盘

### 错误处理示例

```bash
# 创建任务失败时的处理
if ! openclaw cron add ...; then
    echo "❌ 创建定时任务失败"
    echo "请检查："
    echo "1. Gateway服务是否运行 (openclaw gateway status)"
    echo "2. 参数格式是否正确"
    echo "3. 是否有创建权限"
    exit 1
fi
```

## 📁 文件结构

```
cron-manager-master/
├── SKILL.md                    # 本文件
├── references/
│   └── cron-examples.md        # cron表达式示例参考
└── scripts/                    # （可选）辅助脚本
```

## 🔧 使用方法

1. **直接调用技能**：当检测到相关触发词时，技能会自动激活
2. **手动创建任务**：使用上述命令模板，替换 `<任务名称>`、`<时间>`、`<消息内容>`
3. **参数说明**：
   - `--name`：任务名称（必需）
   - `--at`：一次性执行时间（ISO格式：`YYYY-MM-DDTHH:mm:ss+08:00`）
   - `--cron`：周期性执行cron表达式
   - `--message`：要发送的消息内容（必需）
   - `--session isolated`：使用独立会话（必需）
   - `--announce`：启用消息发送（必需）
   - `--channel`：自动从当前会话获取
   - `--to`：自动从当前会话获取

## 📝 示例

### 示例1：创建明天上午9点的提醒
```bash
openclaw cron add \
  --name "明天会议提醒" \
  --at "2026-03-26T09:00:00+08:00" \
  --session isolated \
  --message "上午9点有团队会议，请准时参加" \
  --announce \
  --channel feishu \
  --to "ou_xxxxxx"
```

### 示例2：创建每天上午10点的日报
```bash
openclaw cron add \
  --name "每日AI新闻日报" \
  --cron "0 10 * * *" \
  --session isolated \
  --message "正在生成今日AI新闻日报..." \
  --announce \
  --channel feishu \
  --to "ou_xxxxxx"
```
