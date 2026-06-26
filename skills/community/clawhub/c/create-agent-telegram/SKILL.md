---
name: create-agent-telegram
description: 创建新 OpenAgent Agent 并绑定 Telegram Bot
---

# 创建 Agent + Telegram Bot

## 用途
自动化创建新的 OpenClaw agent 并绑定到 Telegram 机器人。

## 步骤

### 1. 获取 Bot Token
- 找 @BotFather 创建新机器人，获取 token

### 2. 添加 Bot 到配置
```bash
openclaw config set "channels.telegram.accounts.<bot名>.botToken" "<token>"
openclaw config set "channels.telegram.accounts.<bot名>.dmPolicy" "pairing"
```

### 3. 创建新 Agent
```bash
openclaw agents add <agentID> --non-interactive --workspace /root/.openclaw/workspace-<agentID>
```

### 4. 绑定 Bot 到 Agent
```bash
openclaw agents bind --agent <agentID> --bind telegram:<bot名>
```

### 5. 重启 Gateway
```bash
openclaw gateway restart
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| bot名 | Telegram bot 账户 ID | judge |
| token | BotFather 给的 token | 8764559332:xxx |
| agentID | 新 agent 的 ID | judge |

## 验证
```bash
openclaw agents bindings
openclaw gateway status
```

## 完整示例
```bash
# 添加 bot
openclaw config set "channels.telegram.accounts.judge.botToken" "8764559332:AAGxxx"
openclaw config set "channels.telegram.accounts.judge.dmPolicy" "pairing"

# 创建 agent
openclaw agents add judge --non-interactive --workspace /root/.openclaw/workspace-judge

# 绑定
openclaw agents bind --agent judge --bind telegram:judge

# 重启
openclaw gateway restart
```
