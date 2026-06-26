---
name: agent-creator
description: 创建具有独立工作区和配置的独立 OpenClaw Agent。适用于用户需要完全隔离的 Agent（独立工作区、配置、身份），而不是临时子 Agent 会话的情况。支持飞书机器人绑定，用于多机器人部署。
---

# Agent Creator (Agent 创建器)

此技能帮助你创建具有独立工作区、配置和可选飞书机器人绑定的 **独立 OpenClaw Agent**。

## 何时使用

当用户希望执行以下操作时使用此技能：
- 创建一个拥有自己工作区的完全隔离的 Agent
- 为特定项目/客户设置专用 Agent
- 部署多个飞书机器人，每个机器人具有独立的身份
- 创建长期运行的专用 Agent（而不是临时子 Agent）

**触发请求示例：**
- "帮我创建一个客服 agent，用独立的 workspace"
- "我需要一个专门处理设计师工作的 agent"
- "创建一个新的飞书机器人，用于内部 IT 支持"
- "Create a standalone agent for customer support"
- "Set up a new Feishu bot for the HR team"

## 两种模式

### 模式 1: Standalone Agent (独立 Agent - 推荐)

创建一个完全隔离的 Agent，包含：
- 独立的工作区目录
- `openclaw.json` 中单独的 Agent 配置
- 可选的飞书机器人绑定
- 独立的身份和记忆

### 模式 2: Subagent Session (子 Agent 会话 - 临时)

创建一个临时子 Agent 会话（用于快速任务）。仅用于短期的辅助工作。

---

## 独立 Agent 创建流程

### 第 1 步：收集需求

询问用户（如果尚未提供）：

| 问题 | 目的 |
|----------|---------|
| **Agent ID** | 唯一标识符（例如：`support`, `hr-bot`, `designer`） |
| **Agent Name** | 易读的名称 |
| **Workspace Path** | 存储 Agent 文件的位置（默认：`~/.openclaw/workspace-{id}`） |
| **Feishu Bot?** | 此 Agent 是否需要绑定飞书机器人？ |
| **Feishu Account ID** | 如果绑定到飞书，使用哪个账户 ID？（例如：`support`, `hr`） |
| **Model** | 此 Agent 应该使用哪个模型？ |

### 第 2 步：创建 Agent 目录结构

创建 Agent 目录：

```
~/.openclaw/agents/{agent-id}/
├── agent/
│   ├── auth-profiles.json
│   └── models.json
└── sessions/
```

### 第 3 步：更新 openclaw.json

将 Agent 添加到 `agents.list`：

```json
{
  "agents": {
    "list": [
      {
        "id": "{agent-id}",
        "name": "{agent-name}",
        "workspace": "{workspace-path}",
        "agentDir": "{agent-dir-path}"
      }
    ]
  }
}
```

### 第 4 步：创建飞书绑定（可选）

如果 Agent 需要飞书机器人，添加绑定：

```json
{
  "bindings": [
    {
      "type": "route",
      "agentId": "{agent-id}",
      "match": {
        "channel": "feishu",
        "accountId": "{account-id}"
      }
    }
  ]
}
```

### 第 5 步：配置飞书账户（可选）

如果使用单独的飞书应用，添加到 `channels.feishu.accounts`：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "{account-id}": {
          "enabled": true,
          "appId": "{feishu-app-id}",
          "appSecret": "{feishu-app-secret}",
          "domain": "feishu",
          "groupPolicy": "open"
        }
      }
    }
  }
}
```

### 第 6 步：初始化 Agent 工作区

创建包含必要文件的工作区目录：

```
{workspace-path}/
├── AGENTS.md
├── SOUL.md
├── USER.md
├── IDENTITY.md
├── MEMORY.md
├── TOOLS.md
├── HEARTBEAT.md
└── memory/
```

### 第 7 步：重启 Gateway

修改 `openclaw.json` 后，Gateway 需要重新加载：

```bash
openclaw gateway restart
```

或者通知用户手动重启。

---

## 脚本使用

使用提供的脚本自动创建 Agent：

```bash
python scripts/create_standalone_agent.py \
  --agent-id support \
  --agent-name "Customer Support Bot" \
  --workspace "C:\Users\Administrator\.openclaw\workspace-support" \
  --feishu-account support \
  --feishu-app-id cli_xxx \
  --feishu-app-secret xxx
```

---

## 快速参考

### 所需信息

| 字段 | 必填 | 示例 |
|-------|----------|---------|
| `agent-id` | ✅ | `support`, `hr-bot`, `designer` |
| `agent-name` | ✅ | "Customer Support", "HR Assistant" |
| `workspace-path` | ✅ | `~/.openclaw/workspace-support` |
| `feishu-binding` | ❌ | `true` 或 `false` |
| `feishu-account-id` | ❌ | `support`, `hr` |
| `feishu-app-id` | ❌ | `cli_a9249b9ee9785cee` |
| `feishu-app-secret` | ❌ | `PAY8vhyLkiLpfmun09sXSboJyoSQXK3g` |

### 配置示例

**简单 Agent（无飞书）**
```json
{
  "agent-id": "research-assistant",
  "agent-name": "Research Assistant",
  "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace-research"
}
```

**带飞书绑定的 Agent（共享应用）**
```json
{
  "agent-id": "support",
  "agent-name": "Customer Support",
  "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace-support",
  "feishu-binding": true,
  "feishu-account-id": "support"
}
```

**带专用飞书应用的 Agent**
```json
{
  "agent-id": "hr-bot",
  "agent-name": "HR Assistant",
  "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace-hr",
  "feishu-binding": true,
  "feishu-account-id": "hr",
  "feishu-app-id": "cli_xxx",
  "feishu-app-secret": "xxx"
}
```

---

## 注意事项

- **Agent ID** 在所有 Agent 中必须唯一
- **Workspace** 应该是一个新的空目录
- **Feishu Account ID** 用于绑定匹配，而不是实际的 App ID
- **Gateway Restart** 修改 `openclaw.json` 后必须重启
- **Auth Profiles** 和 **Models** 默认从主 Agent 复制
- **Security**: 小心处理飞书应用密钥；存储在 `openclaw.json` 中应具有适当的权限

---

## 子 Agent 模式（旧版）

对于临时助手，你仍然可以使用 `sessions_spawn`：

```
sessions_spawn({
  task: "<任务描述>",
  runtime: "subagent" | "acp",
  mode: "session" | "run",
  label: "<Agent 名称>",
  model: "<模型别名>",
  thread: true | false
})
```

但对于生产环境 Agent，请首选独立模式。

---

## 参考文件

- **详细指南**: 见 `references/standalone-agent-guide.md` 以获取完整文档
- **脚本帮助**: 运行 `python scripts/create_standalone_agent.py --help`

---

## 快速开始

```bash
# 简单 Agent（无飞书）
python scripts/create_standalone_agent.py \
  --agent-id my-agent \
  --agent-name "My Agent"

# 带飞书绑定的 Agent
python scripts/create_standalone_agent.py \
  --agent-id support \
  --agent-name "Support Bot" \
  --feishu-account support

# 然后重启 Gateway
openclaw gateway restart
```
