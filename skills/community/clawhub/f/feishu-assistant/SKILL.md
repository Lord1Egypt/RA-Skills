---
name: feishu-assistant
description: 飞书助手，用于发送图片到飞书平台。当用户需要将生成的图片发送到飞书（私聊或群聊）时使用此技能。支持通过 user_id、open_id 或 chat_id 发送图片。
---

# Feishu Assistant

发送图片到飞书平台（私聊或群聊）。

## 凭证配置（0配置，开箱即用）

### ✅ 推荐：OpenClaw 主配置（无需任何操作）
如果你的 OpenClaw 已经配置了飞书机器人，**自动读取，无需任何操作**。

技能会级联读取飞书凭证，优先级：
1. 环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
2. OpenClaw 主配置 `~/.openclaw/openclaw.json` 中的飞书配置
3. 以上都没有 → 脚本会报"未配置飞书凭证"错误

### 获取飞书配置
1. 访问 https://open.feishu.cn/ 创建企业自建应用
2. 获取 App ID 和 App Secret
3. 开启权限：`im:message:send_as_bot`
4. 将应用添加到群聊（获取 chat_id）

---

## 使用方法

### 发送图片到群聊
```bash
python3 scripts/send_image.py /path/to/image.png --chat-id chat_xxxxx
```

### 发送图片到用户（私聊）
```bash
# 通过 user_id
python3 scripts/send_image.py /path/to/image.png --user-id u_xxxxx

# 通过 open_id
python3 scripts/send_image.py /path/to/image.png --open-id o_xxxxx
```

### 回复某条消息（发送到同一对话）
```bash
python3 scripts/send_image.py /path/to/image.png --message-id oxxxxxx
```

---

## 获取 ID 的方法

| ID 类型 | 格式 | 获取方式 |
|---------|------|----------|
| 群聊 ID | `chat_xxxxx` | 飞书群设置 → 群机器人 → 复制 Chat ID |
| 用户 ID | `u_xxxxx` | 企业内部用户 ID，通过 API 或管理后台获取 |
| Open ID | `o_xxxxx` | 开放平台用户 ID，可通过机器人获取 |
| 消息 ID | `o_xxxxx` | 消息事件中携带的 message_id |

---

## 集成其他技能

当用户说"发送到飞书"或"发到群里"时，调用此技能发送图片。

脚本路径：
```
skills/feishu-assistant/scripts/send_image.py
```
