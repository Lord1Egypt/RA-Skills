---
name: feishu-send-message
description: |
  Proactively send messages to Feishu (Lark) users or group chats from your OpenClaw agent.
  Supports name-based lookup from DM contacts config, open_id, and chat_id.
  Zero dependencies — uses only Python 3 stdlib. Reads credentials from openclaw.json automatically.
  Use when: agent needs to notify someone, send task results, or communicate with team members on Feishu.
metadata:
  clawdbot:
    emoji: "✉️"
    requires:
      plugins: ["feishu"]
      files: ["scripts/*"]
---

# 飞书发送消息 Skill / Feishu Send Message

让 OpenClaw Agent 主动给飞书（Lark）用户或群聊发送文本消息。

## 为什么需要这个 Skill？

OpenClaw 内置的 `feishu_chat` 工具只支持查询群信息和成员列表，**不能主动发消息给其他用户**。
这个 Skill 补充了这个能力 — Agent 可以通过命令行脚本向任何已授权的飞书用户或群聊发送消息。

典型场景：
- 定时任务完成后通知指定同事
- 竞品分析/舆情报告生成后推送给相关人
- Agent 之间通过飞书协作通知

## 安装

```bash
clawhub install feishu-send-message
```

或手动复制到 `~/.openclaw/workspace/skills/feishu-send-message/`。

## 配置（首次使用前必读）

### 1. 确保飞书插件已启用

你的 `openclaw.json` 中需要有飞书 channel 配置：

```json
"channels": {
  "feishu": {
    "accounts": {
      "default": {
        "appId": "your_app_id",
        "appSecret": "your_app_secret"
      }
    }
  }
}
```

### 2. 添加联系人映射

在飞书 account 配置中添加 `dms` 字段，这样 Agent 就能用姓名发消息：

```json
"dms": {
  "ou_xxxxxx": { "label": "张三" },
  "ou_yyyyyy": { "label": "李四" }
}
```

### 3. 如何获取正确的 open_id

**重要**：飞书的 `open_id` 是按应用隔离的，每个飞书应用看到的同一用户 open_id 不同。

获取方法：
1. 让目标用户在飞书中找到你的 OpenClaw 机器人，发送任意一条消息
2. 查看日志 `~/.openclaw/logs/gateway.log`，找到：
   ```
   Feishu[default] DM from ou_xxxxxx: 你好
   ```
3. 这个 `ou_xxxxxx` 就是该用户在你的应用下的正确 open_id

## 使用方法

### 按姓名发送（推荐）

```bash
python3 {baseDir}/scripts/send.py --to "张三" --text "报告已生成，请查收"
```

### 按 open_id 发送

```bash
python3 {baseDir}/scripts/send.py --to "ou_xxxxxx" --text "你好"
```

### 发送到群聊

```bash
python3 {baseDir}/scripts/send.py --to "oc_xxxxxx" --text "大家好，以下是今日简报"
```

### 查看已配置的联系人

```bash
python3 {baseDir}/scripts/send.py --list-contacts
```

### 指定 ID 类型（高级）

```bash
python3 {baseDir}/scripts/send.py --to "on_xxxxxx" --id-type union_id --text "消息内容"
```

支持的 ID 类型：`open_id`（默认）、`chat_id`、`user_id`、`union_id`

## 输出格式

脚本输出 JSON，方便 Agent 解析。

成功：
```json
{
  "success": true,
  "to": "ou_xxxxxx",
  "to_label": "张三",
  "message_id": "om_xxxxxx",
  "chat_id": "oc_xxxxxx"
}
```

失败：
```json
{
  "success": false,
  "to": "ou_xxxxxx",
  "to_label": null,
  "error_code": 99992361,
  "error_msg": "open_id cross app"
}
```

## 前提条件

1. **飞书插件已配置** — `openclaw.json` 中有飞书 appId 和 appSecret
2. **收件人已授权** — 目标用户必须先给机器人发过至少一条消息（飞书平台要求）
3. **Python 3** — 脚本使用纯标准库，无需 pip install

## 常见错误

- **99992361 open_id cross app** — 使用了其他飞书应用的 open_id，必须用当前应用下的（参考上方「如何获取正确的 open_id」）
- **230001 bot not in chat** — 机器人无权给该用户发消息，让用户先给机器人发一条消息即可
- **230002 invalid content** — 消息内容为空或格式错误

## 安全说明

- 脚本从 `~/.openclaw/openclaw.json` 读取飞书应用凭证，不需要额外配置环境变量
- 不会存储或转发消息内容
- 仅调用飞书开放平台官方 API (`open.feishu.cn`)
