# SKILL.md - 飞书多机器人配置

## 描述

为多个 OpenClaw Agent 配置独立的飞书机器人，支持免配对直接聊天模式。

## 触发条件

用户请求：
- "给多个 agent 配置飞书机器人"
- "配置飞书多账号"
- "让每个 agent 用不同的飞书机器人"
- 提供多个飞书 App ID + App Secret 要求配置

## 执行步骤

### 步骤 1：收集信息

向用户确认以下信息（格式示例）：

```
Agent 名称 | 飞书 App ID | 飞书 App Secret
-----------|------------|----------------
银月       | cli_xxx    | xxx
韩立       | cli_yyy    | yyy
```

### 步骤 2：构建配置

使用 `gateway` 工具的 `config.patch` 动作，更新配置：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "defaultAccount": "<第一个 agent 名称>",
      "dmPolicy": "open",
      "connectionMode": "websocket",
      "domain": "feishu",
      "groupPolicy": "open",
      "accounts": {
        "<agent1>": {
          "appId": "<app_id_1>",
          "appSecret": "<app_secret_1>"
        },
        "<agent2>": {
          "appId": "<app_id_2>",
          "appSecret": "<app_secret_2>"
        }
      }
    }
  }
}
```

### 步骤 3：应用配置

调用 `gateway` 工具：

```
action: config.patch
note: "已配置飞书多机器人：[Agent 列表]，Gateway 将自动重启"
raw: <上述配置 JSON>
```

### 步骤 4：验证状态

配置完成后，执行：

```bash
openclaw gateway status
```

确认 Gateway 运行正常。

### 步骤 5：返回摘要

向用户返回配置摘要：

| Agent | 飞书账号名 | App ID | 状态 |
|-------|-----------|--------|------|
| 银月 | yinyue | cli_xxx | ✅ |
| 韩立 | hanli | cli_yyy | ✅ |

**默认账号**: `<defaultAccount>`

**免配对模式**: 已启用，添加机器人后可直接聊天。

---

## 注意事项

1. **App Secret 保密**：不要在日志或公开场合泄露
2. **账号命名**：建议使用 agent 名称作为账号标识
3. **defaultAccount**：设置为最常用的 Agent
4. **dmPolicy: "open"**：关闭配对，任何人添加机器人即可聊天
5. **重启生效**：config.patch 会自动触发 Gateway 重启

---

## 故障排查

| 问题 | 检查项 |
|------|--------|
| 机器人不响应 | `openclaw gateway status` 确认运行中 |
| 配置未生效 | 检查 `openclaw logs --follow` 查看错误 |
| 账号冲突 | 确保每个 accountId 唯一 |

---

## 相关文档

- OpenClaw 飞书文档：https://docs.openclaw.ai/channels/feishu.md
- 多账号配置示例：`channels.feishu.accounts`
