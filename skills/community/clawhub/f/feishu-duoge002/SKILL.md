# Feishu Multi-Bot Setup

批量创建多个飞书机器人（多Agent），每个机器人拥有：
- ✅ **独立记忆系统** - 独立的 MEMORY.md 和每日日志
- ✅ **独立存储空间** - 每个机器人独立工作目录
- ✅ **独立大模型配置** - 每个机器人可配置不同的模型
- ✅ **独立角色设定** - 独立的 SOUL.md、IDENTITY.md
- ✅ **独立飞书连接** - 每个机器人对应独立的飞书应用凭证

## 功能特点

- 一键批量创建多个飞书机器人
- 自动转换配置格式（从单账号到多账号）
- 自动创建所有配置文件
- 自动绑定路由规则
- 自动处理白名单权限问题
- 每个机器人完全隔离

## 使用方法

### 1. 准备配置文件

创建一个 JSON 配置文件 `bots_config.json`，格式如下：

```json
{
  "bots": [
    {
      "name": "coding-assistant-bot",
      "agentId": "feishu-coding-assistant",
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "xxx",
      "verificationToken": "xxx",
      "model": "volcengine-plan/ark-code-latest",
      "connectionMode": "websocket",
      "personality": {
        "role": "编程助手",
        "tagline": "全栈开发工程师",
        "style": "严谨高效、直给代码",
        "styleDescription": "代码风格严谨高效，直接给出可运行代码",
        "responsibilities": [
          "代码编写",
          "Bug修复",
          "框架开发",
          "接口与部署"
        ],
        "description": "我是全栈开发工程师...",
        "motto": "代码即艺术，效率即生命",
        "emoji": "💻"
      }
    }
  ]
}
```

### 配置字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | Bot 内部名称 (飞书账号 ID) |
| agentId | ✅ | Agent 唯一标识 |
| appId | ✅ | 飞书应用 ID |
| appSecret | ✅ | 飞书应用密钥 |
| encryptKey | ❌ | 加密密钥 |
| verificationToken | ❌ | 验证令牌 |
| model | ❌ | 独立大模型配置，默认使用全局默认 |
| connectionMode | ❌ | websocket 或 webhook，默认 websocket |
| personality | ✅ | 机器人角色信息（见下面） |

### Personality 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| role | ✅ | 机器人角色名称 |
| tagline | ✅ | 简短描述 |
| style | ✅ | 工作风格描述 |
| styleDescription | ❌ | 详细风格说明 |
| responsibilities | ✅ | 职责列表 |
| description | ✅ | 自我介绍 |
| motto | ❌ | 签名格言 |
| emoji | ✅ | 机器人表情 |

### 2. 运行批量创建脚本

```bash
python3 /root/.openclaw/workspace/skills/feishu-multi-bot-setup/scripts/setup_bots.py /path/to/bots_config.json
```

### 3. 重启网关

```bash
openclaw gateway restart
```

## 权限说明

- 每个飞书机器人应用中，用户的 Open ID 是**完全不同的**
- 首次运行后，可以从网关日志中提取每个机器人对应的用户 ID
- 然后将用户 ID 添加到对应机器人配置的 `allowFrom` 列表中
- `dmPolicy: "open"` 配合空的 `allowFrom` 表示允许所有人访问
- `dmPolicy: "allowlist"` 需要配置具体的允许用户列表

## 常见问题

### Q: 为什么机器人收到消息但不回复？
A: 检查网关日志，看是否显示 `blocked unauthorized sender`，如果有，说明需要将对应的用户 ID 添加到该机器人的 `allowFrom` 白名单中。

### Q: 每个机器人真的完全独立吗？
A: 是的！每个机器人：
- 独立工作目录 `~/.openclaw/agents/{agent_id}/workspace/`
- 独立的记忆文件 `MEMORY.md` 和 `memory/` 目录
- 独立的角色配置 `SOUL.md` 和 `IDENTITY.md`
- 可以配置独立的大模型
- 独立的飞书连接

### Q: websocket 和 webhook 选哪个？
A: 推荐使用 `websocket`，不需要公网 IP，OpenClaw 主动连接飞书服务器。如果使用 `webhook` 需要公网可访问地址。

## 总结

这个技能解决了批量创建多个独立飞书机器人的问题，让你可以：
- 根据不同职能创建不同的机器人
- 每个机器人有自己独立的记忆和模型
- 机器人之间完全隔离互不干扰
- 一键配置，自动完成所有设置

**作者**: OpenClaw 批量飞书机器人配置
**版本**: 1.0.0
