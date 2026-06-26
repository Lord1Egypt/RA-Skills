---
name: dingtalk-setup
description: 钉钉机器人连接配置指南。用于安装、配置和排查 OpenClaw 钉钉连接器 (dingtalk-connector) 的问题。当用户需要连接钉钉机器人、配置 AppKey/AppSecret、或排查钉钉消息收发问题时使用。
---

# 钉钉机器人配置

配置 OpenClaw 与钉钉机器人连接，支持 AI Card 流式响应和会话管理。

## 前置要求

- OpenClaw >= 2026.3.22（dingtalk-connector v0.8.6+ 必需）
- 钉钉企业账号
- OpenRouter API Key

## 快速配置

### 1. 安装插件

```bash
openclaw plugins install @dingtalk-real-ai/dingtalk-connector
```

### 2. 创建钉钉应用

1. 访问 https://open-dev.dingtalk.com/
2. 应用开发 → 创建企业内部应用
3. 添加应用能力 → 选择"机器人"
4. 获取 **AppKey** 和 **AppSecret**（凭证与基础信息页面）
5. 发布应用（版本管理与发布）

> ⚠️ 应用必须发布才能正常接收消息

### 3. 配置凭证

使用命令行配置：

```bash
openclaw channels add
```

选择 DingTalk，输入 AppKey 和 AppSecret。

或手动编辑 `~/.openclaw/openclaw.json`：

```json5
{
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "你的AppKey",
      "clientSecret": "你的AppSecret"
    }
  }
}
```

### 4. 重启并验证

```bash
openclaw gateway restart
openclaw status
```

确认 DingTalk 状态为 `ON / OK`。

## 常见问题排查

### 机器人不回复

```bash
openclaw logs --follow
```

检查日志确认：
- 应用已发布
- 机器人模式为 Stream（非 Webhook）
- AppKey/AppSecret 正确

### 版本不兼容错误

错误信息：`Cannot find module '.../plugin-sdk/root-alias.cjs/channel-runtime'`

原因：OpenClaw 版本过低

解决：
```bash
npm install -g openclaw@latest
openclaw gateway restart
```

### HTTP 401 错误

- 检查 AppKey/AppSecret 是否正确（注意多余空格）
- 确认应用已发布

### Stream 连接 400 错误

| 原因 | 解决方案 |
|------|----------|
| 应用未发布 | 发布应用 |
| 凭证错误 | 检查 AppKey/AppSecret |
| 非 Stream 模式 | 确认机器人配置为 Stream 模式 |
| IP 白名单限制 | 检查应用是否设置了 IP 白名单 |

### 端口冲突

```bash
openclaw gateway stop
openclaw gateway start
```

## 进阶配置

### 异步模式（长时间任务）

```json5
{
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "AppKey",
      "clientSecret": "AppSecret",
      "asyncMode": true,
      "ackText": "收到，处理中..."
    }
  }
}
```

### 会话配置

```json5
{
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "AppKey",
      "clientSecret": "AppSecret",
      "separateSessionByConversation": true,
      "groupSessionScope": "group"
    }
  }
}
```

## 参考链接

- 插件文档：https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector
- 钉钉开放平台：https://open-dev.dingtalk.com/
