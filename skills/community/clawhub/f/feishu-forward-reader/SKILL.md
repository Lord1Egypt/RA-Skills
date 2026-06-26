---
name: feishu-forward-reader
description: 读取和解析飞书合并转发消息(merge_forward)的详细内容。当收到飞书转发消息显示为"Merged and Forwarded Message"时使用此 skill 获取原始消息内容。
---

# 飞书转发消息读取器

读取飞书合并转发消息的详细内容。

## 问题背景

飞书的合并转发消息 (`merge_forward`) 在 OpenClaw 中默认只显示 "Merged and Forwarded Message"，无法看到实际转发的内容。此 skill 通过飞书 API 获取转发消息的完整子消息列表。

## 凭证配置

脚本会自动从以下位置获取飞书凭证（按优先级）：

1. **命令行参数**: `--app-id` / `--app-secret`
2. **环境变量**: `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
3. **OpenClaw 配置**: `~/.openclaw/openclaw.json` 中的 `channels.feishu.appId/appSecret`

如果已配置 OpenClaw 飞书插件，无需额外配置即可使用。

## 快速使用

### 方法 1：Python 脚本（推荐）

```bash
# 自动从 OpenClaw 配置读取凭证
python3 scripts/parse_forward.py <message_id>

# 或手动指定凭证
python3 scripts/parse_forward.py <message_id> --app-id <id> --app-secret <secret>

# JSON 格式输出
python3 scripts/parse_forward.py <message_id> --format json

# 不查询用户名（更快）
python3 scripts/parse_forward.py <message_id> --no-names
```

### 方法 2：Shell 脚本（原始 JSON）

```bash
# 自动从配置读取凭证
./scripts/read_forward.sh <message_id>

# 或手动指定
./scripts/read_forward.sh <message_id> <app_id> <app_secret>
```

### 方法 3：直接调用 API

```bash
# 获取 token
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"YOUR_APP_ID","app_secret":"YOUR_APP_SECRET"}' | jq -r '.tenant_access_token')

# 获取消息详情
curl -s "https://open.feishu.cn/open-apis/im/v1/messages/<message_id>" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

## API 响应结构

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "message_id": "om_xxx",
        "msg_type": "merge_forward",
        "body": {"content": "Merged and Forwarded Message"}
      },
      {
        "message_id": "om_yyy",
        "msg_type": "text",
        "body": {"content": "{\"text\":\"实际消息内容\"}"},
        "upper_message_id": "om_xxx",
        "sender": {"id": "ou_xxx", "sender_type": "user"},
        "create_time": "1234567890000"
      }
    ]
  }
}
```

- 第一条是转发消息本身 (`msg_type: merge_forward`)
- 后续是被转发的原始消息，带有 `upper_message_id` 指向父消息

## 支持的消息类型

| 类型 | 说明 | 解析方式 |
|------|------|----------|
| `text` | 文本消息 | `body.content` → JSON → `text` |
| `post` | 富文本消息 | `body.content` → JSON → `title` + `content` |
| `interactive` | 卡片消息 | `body.content` → JSON → `title` + `elements` |
| `image` | 图片 | 显示 `[图片]` |
| `file` | 文件 | 显示 `[文件]` |
| `audio` | 语音 | 显示 `[语音]` |
| `video` | 视频 | 显示 `[视频]` |

## 权限要求

飞书应用需要以下权限：
- `im:message:readonly` - 获取群组中所有消息（敏感权限）
- `contact:contact.base:readonly` - 获取用户基本信息（可选，用于显示用户名）

## 示例输出

```
📨 合并转发消息 (3 条)
来源群: oc_xxxxxxxxxxxxxxxxxxxx
----------------------------------------
[02-25 14:02] 张三
  大家好，这是一条测试消息

[02-25 14:03] ou_yyyyyyyyyyy...
  收到，我看看

[02-25 14:05] 李四
  已处理完成
```

注：可见范围内的用户显示真实姓名，范围外的显示 ID 前缀。
