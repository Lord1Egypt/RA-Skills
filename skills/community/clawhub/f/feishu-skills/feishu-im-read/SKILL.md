---
name: feishu-im-read
description: |
  读取飞书 IM 消息。支持会话历史和跨会话搜索。
overrides: feishu_im_user_get_messages, feishu_im_user_search_messages, feishu_im_user_get_thread_messages, feishu_pre_auth
inline: true
---

# feishu-im-read
> **模块兼容**：所有脚本均提供 `.js` 和 `.mjs` 两个版本。优先使用 `.js`，若报 `require is not defined` 错误则改用同名 `.mjs` 文件。

直接用 `exec` 执行，不要检查文件或环境。

## 获取会话消息（应用级权限，无需用户授权）

使用 tenant_access_token，机器人必须在群组中。

```bash
node ./im-read.js --action "get_messages" --open-id "SENDER_OPEN_ID" --chat-id "oc_xxx"
```

可选：`--thread-id "omt_xxx"` `--relative-time "today"` `--start-time "ISO8601"` `--end-time "ISO8601"` `--sort-rule "create_time_asc"` `--page-size 20` `--page-token "xxx"`

## 搜索消息（需要用户授权）

使用 user_access_token。

```bash
node ./im-read.js --action "search_messages" --open-id "SENDER_OPEN_ID" --query "关键词"
```

可选：`--chat-id "oc_xxx"` `--sender-ids "ou_xxx,ou_yyy"` `--message-type "file"` `--chat-type "group"`

## 必须确认的参数

| 参数 | 何时询问 |
|---|---|
| `--chat-id` / `--target-open-id` | 用户未指明会话（当前会话 chat_id 可从上下文获取） |
| `--query` | search_messages 时未提供关键词 |

## 授权

若返回 `{"error":"auth_required"}` 或 `{"error":"permission_required"}`，**不要询问用户是否授权，直接立即执行以下命令发送授权链接：**

- 若返回 JSON 中包含 `required_scopes` 字段，将其数组值用空格拼接后传入 `--scope` 参数：

```bash
node ../feishu-auth/auth.js --auth-and-poll --open-id "SENDER_OPEN_ID" --chat-id "CHAT_ID" --timeout 60 --scope "<required_scopes 用空格拼接>"
```

- 若返回中不包含 `required_scopes`，则不加 `--scope` 参数（使用默认权限）。

- `{"status":"authorized"}` → 重新执行原始命令
- `{"status":"polling_timeout"}` → **立即重新执行此 auth 命令**（不会重复发卡片）
- `CHAT_ID` 不知道可省略

## 权限不足时（应用级）

若返回中包含 `"auth_type":"tenant"`，说明需要管理员在飞书开放平台开通应用权限，**必须将 `reply` 字段内容原样发送给用户**。
