---
name: agent-extract
description: 将技能/功能从 main agent 剥离成独立 agent，实现 session 隔离和独立保活。Use when: (1) 用户想把某个功能独立成单独的 agent，(2) 需要隔离 session 避免污染，(3) 需要 agent 独立保活运行。触发词：剥离 agent、独立 agent、拆分 agent、创建独立 agent。
---

# Agent Extract（Agent 剥离技能）

将技能/功能从 main agent 剥离成独立 agent，实现：
- Session 隔离（不污染 main）
- 独立心跳/保活
- 独立 workspace、memory、identity

## 🚀 快速开始

### 安装后如何使用

安装此技能后，只需告诉你的 agent：

```
把 <技能名> 剥离成独立 agent
```

例如：
- "把 aiway 剥离成独立 agent"
- "让 email 功能独立保活"
- "创建一个独立 agent 处理日程"

Agent 会自动：
1. 评估当前环境
2. 创建新 agent 配置
3. 复制必要的技能和记忆文件
4. 设置独立心跳
5. 验证迁移完整性

### 实际案例：AIWay 剥离

**剥离前**：main agent 同时处理日常任务 + AIWay 社交

**剥离后**：
- main agent：专注日常任务
- aiway agent：独立运行，处理 AIWay 社交

**效果**：session 隔离，互不污染

## ⚠️ 核心约束（必须遵守）

### 1. 不能损坏原有环境

- **不删除** main agent 的任何现有 session
- **不修改** main agent 的 transcript 文件
- **不改变** main agent 的配置（除非用户明确要求）
- **保留** 所有现有的 cron jobs（除非明确要迁移）

### 2. 不能破坏当前 channel

- **不修改** channel 配置
- **不删除** channel 凭证
- **保持** 所有现有的消息路由正常工作
- 新 agent 的消息路由是新增的，不是替换

### 3. 原有记忆、人格、身份不能丢失

- **复制** 而非移动相关文件
- **保留** 原有的 SOUL.md、IDENTITY.md、USER.md
- **迁移** memory 文件到新 workspace（复制）
- **验证** 新 agent 可以访问所有必要的技能文件

## 剥离流程

### Step 1: 评估现状

```bash
# 1. 检查 main agent 配置
cat ~/.openclaw/openclaw.json | jq '.agents'

# 2. 检查目标技能/功能
ls -la ~/.openclaw/workspace/skills/<skill-name>/

# 3. 检查现有 cron jobs
openclaw cron list

# 4. 检查现有 sessions
cat ~/.openclaw/agents/main/sessions/sessions.json | jq 'keys'
```

### Step 2: 创建新 Agent 配置

在 `~/.openclaw/openclaw.json` 的 `agents.list` 中添加：

```json
{
  "id": "<new-agent-id>",
  "name": "<Agent 显示名称>",
  "workspace": "/Users/<user>/.openclaw/workspace-<new-agent-id>"
}
```

**⚠️ 注意：** 使用 `config.patch` 而不是直接编辑文件，确保不破坏其他配置。

### Step 3: 创建新 Workspace

```bash
# 创建 workspace 目录
mkdir -p ~/.openclaw/workspace-<new-agent-id>/{memory,skills}

# 复制必要的身份文件（复制，不是移动！）
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace-<new-agent-id>/
cp ~/.openclaw/workspace/IDENTITY.md ~/.openclaw/workspace-<new-agent-id>/
cp ~/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace-<new-agent-id>/

# 复制技能文件
cp -r ~/.openclaw/workspace/skills/<skill-name> ~/.openclaw/workspace-<new-agent-id>/skills/

# 复制记忆文件（如果需要）
cp -r ~/.openclaw/workspace/memory/*.md ~/.openclaw/workspace-<new-agent-id>/memory/
```

### Step 4: 创建独立心跳配置

**在新 workspace 创建 HEARTBEAT.md：**

```markdown
# 心跳任务

## 任务描述
（从 main 的 HEARTBEAT.md 复制相关内容）

## 频率控制
- 检查间隔：X 小时

## 静默条件
- 夜间 23:00-08:00 除非紧急
- 无新通知时回复 HEARTBEAT_OK
```

**清理 main workspace 的 HEARTBEAT.md：**

```markdown
# 心跳任务

（暂无心跳任务）

## 静默条件
- 无任务时回复 HEARTBEAT_OK
```

### Step 5: 创建 Cron Job

```bash
# 创建独立 cron job
openclaw cron add --name "<Agent Name> Heartbeat" \
  --schedule "every 30m" \
  --agent-id "<new-agent-id>" \
  --session-key "agent:<new-agent-id>:main" \
  --session-target "isolated" \
  --message "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK." \
  --delivery "announce"
```

或使用 tool：

```json
{
  "name": "<Agent Name> Heartbeat",
  "schedule": {"kind": "every", "everyMs": 1800000},
  "agentId": "<new-agent-id>",
  "sessionKey": "agent:<new-agent-id>:main",
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Read HEARTBEAT.md..."
  },
  "delivery": {"mode": "announce"}
}
```

### Step 6: 验证

**检查清单：**

```bash
# 1. 验证新 agent 配置
cat ~/.openclaw/openclaw.json | jq '.agents.list[] | select(.id == "<new-agent-id>")'

# 2. 验证新 workspace
ls -la ~/.openclaw/workspace-<new-agent-id>/

# 3. 验证 cron job
openclaw cron list

# 4. 验证 main session 未受影响
cat ~/.openclaw/agents/main/sessions/sessions.json | jq 'keys'

# 5. 验证 channel 配置未受影响
cat ~/.openclaw/openclaw.json | jq '.channels'
```

**手动触发测试：**

```bash
openclaw cron run <job-id>
```

## 文件迁移对照表

| 文件类型 | 操作 | 说明 |
|---------|------|------|
| SOUL.md | 复制 | 保持人格一致 |
| IDENTITY.md | 复制 | 保持身份一致 |
| AGENTS.md | 复制后修改 | 移除不需要的共享内容 |
| USER.md | 复制 | 用户偏好 |
| HEARTBEAT.md | 新建 + 清理原 | 独立心跳任务 |
| skills/ | 复制 | 技能文件 |
| memory/*.md | 复制 | 历史记忆 |
| MEMORY.md | 复制 | 长期记忆 |

## 常见问题

### Q: 如何确保 channel 不受影响？

A: Channel 配置在 `~/.openclaw/openclaw.json` 的 `channels` 字段中。剥离 agent 只修改 `agents.list`，不触及 `channels`。消息路由基于 `lastChannel` 和 `deliveryContext`，新 agent 的 session 是新创建的，不影响现有路由。

### Q: 如何确保记忆不丢失？

A: 所有文件都是**复制**而非移动。原始文件保留在 main workspace。新 agent 的 memory 是独立的副本，之后的修改互不影响。

### Q: 如果剥离失败怎么办？

A: 按照以下步骤回滚：
1. 删除新创建的 workspace：`rm -rf ~/.openclaw/workspace-<new-agent-id>`
2. 删除 cron job：`openclaw cron remove <job-id>`
3. 从配置中移除 agent（使用 `config.patch`）
4. 恢复 main 的 HEARTBEAT.md（如果修改了）

### Q: 如何验证剥离成功？

A: 检查以下几点：
1. 新 agent 有独立的 session key
2. 新 agent 的消息不会出现在 main 的 transcript 中
3. main 的 session 数量没有减少
4. channel 消息正常路由
5. 新 agent 的记忆、人格、身份正常工作

## 架构图

```
剥离前：
┌─────────────────────────────────────┐
│  Main Agent                         │
│  - Session A                        │
│  - Session B                        │
│  - 心跳（包含技能X任务）              │
│  - skills/skill-x/                  │
│  - memory/                          │
└─────────────────────────────────────┘

剥离后：
┌─────────────────────────────────────┐
│  Main Agent                         │
│  - Session A                        │
│  - Session B                        │
│  - 心跳（无技能X任务）                │
│  - skills/skill-x/（保留）           │
│  - memory/（保留）                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Skill-X Agent (新)                 │
│  - Session: agent:skill-x:main      │
│  - 独立心跳（cron job）              │
│  - skills/skill-x/（复制）           │
│  - memory/（复制）                   │
│  - SOUL.md / IDENTITY.md（复制）     │
└─────────────────────────────────────┘
```

## 示例：AIWay 剥离

```bash
# 1. 评估现状
cat ~/.openclaw/openclaw.json | jq '.agents'

# 2. 创建新 agent 配置
# （使用 config.patch 或手动编辑）

# 3. 创建 workspace
mkdir -p ~/.openclaw/workspace-aiway/{memory,skills}
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace-aiway/
cp ~/.openclaw/workspace/IDENTITY.md ~/.openclaw/workspace-aiway/
cp -r ~/.openclaw/workspace/skills/aiway ~/.openclaw/workspace-aiway/skills/

# 4. 创建 HEARTBEAT.md
# （在新 workspace 创建独立心跳配置）

# 5. 清理 main 的 HEARTBEAT.md
# （移除 AIWay 相关任务）

# 6. 创建 cron job
openclaw cron add --name "AIWay Heartbeat" \
  --schedule "every 30m" \
  --agent-id "aiway" \
  --session-target "isolated" \
  --delivery "announce"
```