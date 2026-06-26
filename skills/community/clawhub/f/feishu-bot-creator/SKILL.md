---
name: feishu-bot-creator
description: 飞书机器人创建器 — 自动化创建和配置飞书机器人，包括应用创建、权限配置、 webhook 设置等。| Feishu Bot Creator — Automate creation and configuration of Feishu bots, including app creation, permission setup, webhook configuration.
license: MIT
compatibility: openclaw
metadata:
  version: "1.0.0"
  tags: [feishu, bot, robot, automation, openapi]
  author: 老牛
  openclaw:
    emoji: "🤖"
    requires:
      bins: [python3, curl]
      config:
        - ~/.openclaw/openclaw.json
---

# Feishu Bot Creator | 飞书机器人创建器

自动化创建和配置飞书机器人，省去手动在飞书开放平台操作的麻烦。

Automate creation and configuration of Feishu bots, eliminating the need for manual operations on Feishu Open Platform.

## 快速开始 | Quick Start

```bash
python3 scripts/feishu_bot_creator.py \
  --name "我的机器人" \
  --webhook-url "http://your-server/webhook"
```

## 使用方法 | Usage

### 创建新机器人
```bash
python3 scripts/feishu_bot_creator.py \
  --name "机器人名称" \
  --description "机器人描述" \
  --webhook-url "http://your-server/webhook" \
  --permissions "im:message,im:chat"
```

### 参数说明 | Arguments

- `--name`（必填）：机器人名称
- `--description`（可选）：机器人描述
- `--webhook-url`（可选）：接收消息的 webhook 地址
- `--permissions`（可选）：需要的权限，逗号分隔
- `--icon`（可选）：机器人图标 URL
- `--output`（可选）：输出配置文件路径，默认 `~/.feishu/bots/<name>.json`

### 可用权限 | Available Permissions

```
im:message          - 发送消息
im:chat             - 访问聊天信息
im:chat:read        - 读取聊天记录
im:message:send_as_bot - 以机器人身份发送消息
contact:contact:readonly - 读取通讯录
calendar:calendar:readonly - 读取日历
drive:drive:readonly - 读取云文档
```

## 工作原理 | How It Works

1. 调用飞书开放平台 API 创建应用
2. 配置应用权限
3. 设置机器人头像和名称
4. 配置 webhook（如提供）
5. 生成配置文件

## 输出示例 | Output Example

```json
{
  "app_id": "cli_a1b2c3d4e5f6",
  "app_secret": "xxxxx",
  "name": "我的机器人",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx",
  "permissions": ["im:message", "im:chat"]
}
```

## 前置要求 | Prerequisites

1. 需要飞书开放平台账号
2. 需要有创建应用的权限
3. 需要配置 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量

## 环境变量 | Environment Variables

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
export FEISHU_API_BASE="https://open.feishu.cn"  # 可选，默认
```

## 错误处理 | Error Handling

- **权限不足** → 检查账号是否有创建应用权限
- **名称重复** → 换一个机器人名称
- **API 限制** → 等待后重试

## 安全说明 | Security

- 生成的 `app_secret` 请妥善保管
- 建议将配置文件添加到 `.gitignore`
- 不要将凭证提交到版本控制

## 随附脚本 | Bundled Script

- `scripts/feishu_bot_creator.py`

## 示例 | Examples

### 创建简单的通知机器人
```bash
python3 scripts/feishu_bot_creator.py \
  --name "项目通知" \
  --description "发送项目更新通知" \
  --permissions "im:message"
```

### 创建完整的聊天机器人
```bash
python3 scripts/feishu_bot_creator.py \
  --name "AI 助手" \
  --description "智能聊天助手" \
  --webhook-url "http://localhost:8080/webhook" \
  --permissions "im:message,im:chat,im:chat:read" \
  --icon "https://example.com/icon.png"
```
