# Agent Creator 技能

快速创建、删除、管理 OpenClaw agent 实例。

## 触发条件

用户要求创建新机器人、新 agent、新助手、删除 agent、查看 agent 列表时激活此技能。

## 可用脚本

| 脚本 | 功能 |
|------|------|
| `list-agents.sh` | 查看当前所有 agent |
| `create-agent.sh` | 创建新 agent |
| `delete-agent.sh` | 删除 agent |

## 创建 Agent

### 参数

```
./create-agent.sh <agent-id> <agent-name> <app-id> <app-secret> [model] [description]
```

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| agent-id | ✅ | 唯一标识符（英文小写） | `xiaoming` |
| agent-name | ✅ | 显示名称 | `小明` |
| app-id | ✅ | 飞书 App ID | `cli_xxx` |
| app-secret | ✅ | 飞书 App Secret | `xxx` |
| model | ❌ | 使用的模型（默认 glm-5） | `qwen3.5-plus` |
| description | ❌ | 人设描述 | `客服助手` |

### 示例

```bash
# 创建一个客服机器人
./create-agent.sh xiaokefu 小客服 cli_a94xxx mysecret123 glm-5 "客服助手，帮助用户解答问题"

# 使用默认模型创建
./create-agent.sh xiaowang 小王 cli_a94xxx mysecret123
```

### 创建后步骤

1. 执行 `openclaw gateway restart` 重载配置
2. 在飞书开放平台配置事件订阅地址
3. 在群里 @ 新机器人测试

## 删除 Agent

```bash
./delete-agent.sh <agent-id>
```

⚠️ 注意：main agent 不能被删除

## 查看列表

```bash
./list-agents.sh
```

## 配置文件位置

- 主配置: `/home/admin/.openclaw/openclaw.json`
- Agent 目录: `/home/admin/.openclaw/agents/{agent-id}/`
- Workspace: `/home/admin/.openclaw/workspace-{agent-id}/`

## 创建时自动完成

1. ✅ 创建 agent 目录结构 (`agents/{id}/agent/`, `agents/{id}/sessions/`)
2. ✅ 创建 workspace 目录和默认文件 (AGENTS.md, SOUL.md, USER.md 等)
3. ✅ 更新 openclaw.json:
   - 添加到 `agents.list`
   - 添加飞书账号到 `channels.feishu.accounts`
   - 添加绑定到 `bindings`
   - 添加到 `tools.agentToAgent.allow`
4. ✅ 复制 models.json 配置

## 注意事项

- 飞书机器人需要先在飞书开放平台创建应用
- 需要配置飞书事件订阅地址（通常为 Gateway 地址）
- 创建/删除后需要重启 Gateway 才能生效