---
name: feishu-agent-bind
description: 绑定飞书机器人到Agent。用户发送App ID和App Secret即可自动配置飞书账号并绑定到指定Agent。用于：(1) 用户提供App ID和App Secret (2) 创建或选择要绑定的Agent (3) 自动配置openclaw.json并重启Gateway。
---

# 飞书 Agent 绑定

用户发送 App ID 和 App Secret 时，使用此 skill 自动完成飞书机器人绑定。

## 触发条件

- 用户发送 `cli_` 开头的 App ID
- 用户发送飞书机器人凭证

## 绑定流程

### 1. 收集信息

需要用户提供：
- **App ID**: 飞书应用 ID (cli_xxx)
- **App Secret**: 飞书应用密钥
- **Agent名称**: 要绑定的 Agent ID (如 `news`, `assistant` 等)

如果用户只提供 App ID 和 App Secret，询问要绑定到哪个 Agent，或自动创建一个新 Agent。

### 2. 创建 Agent (如需要)

```bash
# 创建新 Agent
openclaw agents add <agentName>

# 示例：创建 news agent
openclaw agents add news
```

### 3. 执行绑定

```bash
# 查看现有 Agent 列表
openclaw agents list

# 添加飞书账号到配置
openclaw config set "channels.feishu.accounts.<agentName>.appId" "<App ID>"
openclaw config set "channels.feishu.accounts.<agentName>.appSecret" "<App Secret>"

# 绑定 Agent 到飞书账号
openclaw agents bind --agent <agentName> --bind feishu:<agentName>
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

### 4. 验证

```bash
openclaw channels status
```

## 注意事项

- 如果是首次配置，需要确保飞书应用已在开放平台发布并具备必要权限：
  - `im:message:send_as_bot`
  - `im:message:receive`
  - `contact:contact.base:readonly`
- 配置完成后告知用户如何获取 user open_id 以配置白名单
