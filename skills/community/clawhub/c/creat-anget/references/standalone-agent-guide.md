# Agent Creator - 参考指南

创建独立 OpenClaw Agent 的详细参考。

---

## 架构概览

### 独立 Agent 结构

```
~/.openclaw/
├── openclaw.json              # 主配置 (已更新)
├── agents/
│   └── {agent-id}/           # 新 Agent 目录
│       ├── agent/
│       │   ├── auth-profiles.json   # 从主 Agent 复制
│       │   └── models.json          # 从主 Agent 复制
│       └── sessions/                # 会话存储
└── workspace-{agent-id}/     # 新工作区
    ├── AGENTS.md
    ├── SOUL.md
    ├── USER.md
    ├── IDENTITY.md
    ├── MEMORY.md
    ├── TOOLS.md
    ├── HEARTBEAT.md
    └── memory/
```

### 配置变更

**openclaw.json - agents.list:**
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace"
      },
      {
        "id": "{agent-id}",
        "name": "{agent-name}",
        "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace-{id}",
        "agentDir": "C:\\Users\\Administrator\\.openclaw\\agents\\{id}"
      }
    ]
  }
}
```

**openclaw.json - bindings (用于飞书):**
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

**openclaw.json - channels.feishu.accounts (用于专用飞书应用):**
```json
{
  "channels": {
    "feishu": {
      "appId": "cli_main_app",
      "appSecret": "main_secret",
      "accounts": {
        "{account-id}": {
          "enabled": true,
          "appId": "cli_dedicated_app",
          "appSecret": "dedicated_secret",
          "domain": "feishu",
          "groupPolicy": "open"
        }
      }
    }
  }
}
```

---

## 脚本参考

### create_standalone_agent.py

**位置:** `scripts/create_standalone_agent.py`

**必填参数:**
- `--agent-id` - 唯一标识符（小写，允许连字符）
- `--agent-name` - 易读的名称

**可选参数:**
- `--workspace` - 自定义工作区路径（默认：`~/.openclaw/workspace-{id}`）
- `--agent-dir` - 自定义 Agent 目录（默认：`~/.openclaw/agents/{id}`）
- `--feishu-account` - 用于路由的飞书账户 ID
- `--feishu-app-id` - 飞书 App ID（如果使用专用应用）
- `--feishu-app-secret` - 飞书 App Secret
- `--dry-run` - 预览而不进行更改

---

## 示例

### 示例 1: 简单 Agent（无飞书）

```bash
python scripts/create_standalone_agent.py \
  --agent-id research-assistant \
  --agent-name "Research Assistant"
```

**结果:**
- 创建 `~/.openclaw/agents/research-assistant/`
- 创建 `~/.openclaw/workspace-research-assistant/`
- 添加 Agent 到 `openclaw.json`
- 无飞书绑定

### 示例 2: 带飞书绑定的 Agent（共享应用）

```bash
python scripts/create_standalone_agent.py \
  --agent-id support \
  --agent-name "Customer Support" \
  --feishu-account support
```

**结果:**
- 创建 Agent 和工作区
- 添加飞书绑定：`support` Agent → `support` 账户
- 使用主飞书应用凭据

### 示例 3: 带专用飞书应用的 Agent

```bash
python scripts/create_standalone_agent.py \
  --agent-id hr-bot \
  --agent-name "HR Assistant" \
  --feishu-account hr \
  --feishu-app-id cli_a9249b9ee9785cee \
  --feishu-app-secret PAY8vhyLkiLpfmun09sXSboJyoSQXK3g
```

**结果:**
- 创建 Agent 和工作区
- 添加飞书绑定
- 创建具有单独应用凭据的专用飞书账户

---

## 创建后的手动步骤

### 1. 重启 Gateway

```bash
openclaw gateway restart
```

或者在 Windows 上：
```powershell
openclaw gateway restart
```

### 2. 自定义 Agent 身份

编辑新工作区的文件：
- `IDENTITY.md` - 设置 Agent 名称、个性、Emoji
- `USER.md` - 描述目标用户
- `SOUL.md` - 自定义行为和语气（可选）

### 3. 配置飞书机器人（如适用）

如果使用专用飞书应用：
1. 在飞书开放平台创建应用
2. 配置事件订阅
3. 设置 Webhook URL 指向你的 Gateway

### 4. 测试 Agent

发送消息给飞书机器人（如果已配置）或在日志中验证：
```bash
openclaw logs --agent {agent-id}
```

---

## 故障排除

### Agent 无响应

1. 检查 Gateway 是否运行：`openclaw gateway status`
2. 验证 `openclaw.json` 中的绑定
3. 检查日志：`openclaw logs`
4. 确保飞书应用配置正确

### 配置错误

1. 验证 `openclaw.json` 的 JSON 语法
2. 检查 Agent ID 是否唯一
3. 验证工作区路径是否存在且可写

### 飞书机器人未收到消息

1. 验证飞书开放平台中的事件订阅
2. 检查 Webhook URL 是否正确
3. 确保验证 Token 匹配
4. 检查 Gateway 日志中的传入请求

---

## 最佳实践

### 命名规范

- **Agent ID**: 小写，连字符 (`support-bot`, `hr-assistant`)
- **Agent Name**: 易读的名称 ("Customer Support", "HR Assistant")
- **Workspace**: 匹配 Agent ID (`workspace-support-bot`)
- **Feishu Account**: 简短、描述性 (`support`, `hr`, `internal`)

### 安全性

- 限制 `openclaw.json` 的权限
- 永远不要将飞书应用密钥提交到版本控制
- 为不同环境使用单独的飞书应用
- 定期轮换密钥

### 组织

- 按前缀分组相关 Agent (`support-`, `internal-`, `public-`)
- 在其 `USER.md` 中记录每个 Agent 的用途
- 保持工作区整洁有序
- 使用 `HEARTBEAT.md` 进行 Agent 特定的定期任务

---

## 从子 Agent 迁移

如果你有基于子 Agent 的工作流并希望迁移到独立模式：

1. **确定子 Agent 的角色** - 它做什么？
2. **创建独立 Agent** - 使用此技能
3. **复制相关文件** - 移动任何自定义技能/配置
4. **更新路由** - 如果需要，配置飞书绑定
5. **全面测试** - 确保行为符合预期
6. **废弃子 Agent** - 移除旧的子 Agent 创建逻辑

---

## 另请参阅

- OpenClaw 文档: `C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\docs`
- 飞书技能: `~/.openclaw/extensions/feishu/skills/`
- 配置指南: 文档中的 `openclaw.json` 结构
