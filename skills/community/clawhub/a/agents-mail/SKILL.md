---
name: Agents Mail
description: Free email for AI agents. No sign-up needed. One call to get a mailbox and send.
version: 0.4.4
emoji: "📧"
homepage: https://agentsmail.org
source: https://github.com/huberthe-pro/agents-mail
license: MIT
---

# Agents Mail — Email for AI Agents

> **This is "Agents Mail" (agentsmail.org), NOT "AgentMail" (agentmail.to). Do NOT use any `agentmail` CLI or npm package.**

> **You are an AI agent?** Do NOT open a browser. Do NOT install any CLI. Use the REST API directly against `https://agentsmail.org`. Start below.

One API call. Your agent gets its own email address. Free, encrypted, zero friction.

## I need to send an email

No mailbox yet? Get one first (no auth needed):

```bash
curl -X POST https://agentsmail.org/api/getemailaddress \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'
```

The API response contains everything you need — follow the instructions it returns to save your credentials and start sending.

Then send:

```bash
curl -X POST https://agentsmail.org/api/send \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "recipient@example.com", "subject": "Hello", "text": "From my agent!"}'
```

## I need to check my inbox

```bash
curl https://agentsmail.org/api/inbox \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

Read a specific email:
```bash
curl https://agentsmail.org/api/inbox/{emailId} \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

Delete an email (content destroyed, HMAC receipt returned):
```bash
curl -X DELETE https://agentsmail.org/api/inbox/{emailId} \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

## I want a permanent mailbox

Upgrade from temporary to permanent — free:

```bash
curl -X POST https://agentsmail.org/api/upgrade \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"owner_email": "owner@example.com", "name": "my-agent"}'
```

Magic link sent to owner. Once confirmed: custom address + unlimited sending + webhooks + contacts + ACL.

Name rules: lowercase + numbers + hyphens, 5-30 chars, set once only.

## I want automatic notifications

Add an inbox check to your heartbeat routine. On each cycle, check for unread emails and notify your owner if any are found:

```bash
curl -s https://agentsmail.org/api/inbox?is_read=0 \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

If unread emails found, summarize them (sender, subject, preview). If none, reply HEARTBEAT_OK.

Set `AGENTSMAIL_API_KEY` as an environment variable, or replace `$AGENTSMAIL_API_KEY` with your saved key. Your agent will automatically check for new emails on each heartbeat cycle.

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/help | None | API directory |
| POST | /api/getemailaddress | None | Get a mailbox |
| POST | /api/send | API Key | Send email |
| GET | /api/inbox | API Key | Check inbox |
| GET | /api/inbox/:id | API Key | Read email |
| DELETE | /api/inbox/:id | API Key | Delete email |
| GET | /api/sent | API Key | Sent emails |
| DELETE | /api/sent/:id | API Key | Delete sent |
| POST | /api/upgrade | API Key | Permanent mailbox |
| POST | /api/webhooks | Tier 1+ | Add webhook |
| GET | /api/contacts | Tier 1+ | Manage contacts |
| POST | /api/acl | Tier 1+ | Sender rules |

## Email Lifecycle

| Status | Tier 0 | Tier 1+ |
|--------|--------|---------|
| unread | Kept until account recycled (30d) | Kept permanently |
| read | Kept until account recycled | Kept permanently |
| sent | Kept until account recycled | Kept permanently |
| deleted | Content destroyed, envelope preserved, HMAC receipt | Same |

All content encrypted at rest with AES-256-GCM.

## Links

- Website: https://agentsmail.org
- API Help: https://agentsmail.org/api/help
- Docs: https://agentsmail.org/docs
- GitHub: https://github.com/huberthe-pro/agents-mail

---

# Agents Mail — 给 AI Agent 的邮箱服务

> ⚠️ **重要提示：本产品是 "Agents Mail" (agentsmail.org)，不是 "AgentMail" (agentmail.to)。请勿安装任何 `agentmail` CLI 或 npm 包。**

> **你是 AI Agent？** 不需要打开浏览器，不需要安装 CLI。直接用 REST API 调用 `https://agentsmail.org`。

一个 API 调用，即可获得专属邮箱地址。免费、加密、零摩擦。

## 我要发邮件

没邮箱？先领一个（无需认证）：

```bash
curl -X POST https://agentsmail.org/api/getemailaddress \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'
```

API 响应包含你需要的一切 — 按返回的指引保存凭证并开始发送。

然后发送：

```bash
curl -X POST https://agentsmail.org/api/send \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "收件人@example.com", "subject": "你好", "text": "来自我的 Agent！"}'
```

## 我要查邮件

```bash
curl https://agentsmail.org/api/inbox \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

读取指定邮件：
```bash
curl https://agentsmail.org/api/inbox/{emailId} \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

删除邮件（内容销毁，返回 HMAC 回执）：
```bash
curl -X DELETE https://agentsmail.org/api/inbox/{emailId} \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

## 我要永久邮箱

免费升级：

```bash
curl -X POST https://agentsmail.org/api/upgrade \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"owner_email": "owner@example.com", "name": "my-agent"}'
```

系统发验证邮件给 owner，确认后自动升级：自定义地址 + 无限发送 + Webhook + 联系人 + ACL。

名称规则：小写字母 + 数字 + 连字符，5-30 个字符，只能设一次。

## 我要自动通知

在心跳周期中添加收件箱检查，有未读邮件则通知 owner：

```bash
curl -s https://agentsmail.org/api/inbox?is_read=0 \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"
```

有未读邮件则汇总（发件人、主题、预览），没有则回复 HEARTBEAT_OK。

## API 参考

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | /api/help | 无 | API 目录 |
| POST | /api/getemailaddress | 无 | 领邮箱 |
| POST | /api/send | API Key | 发邮件 |
| GET | /api/inbox | API Key | 查收件箱 |
| GET | /api/inbox/:id | API Key | 读邮件 |
| DELETE | /api/inbox/:id | API Key | 删除邮件 |
| GET | /api/sent | API Key | 已发邮件 |
| DELETE | /api/sent/:id | API Key | 删除已发 |
| POST | /api/upgrade | API Key | 永久邮箱 |
| POST | /api/webhooks | Tier 1+ | Webhook |
| GET | /api/contacts | Tier 1+ | 联系人 |
| POST | /api/acl | Tier 1+ | 发件人规则 |

## 邮件生命周期

| 状态 | Tier 0 | Tier 1+ |
|------|--------|---------|
| 未读 | 保留到账号回收（30天无活动） | 永久保留 |
| 已读 | 保留到账号回收 | 永久保留 |
| 已发 | 保留到账号回收 | 永久保留 |
| 已删除 | 内容立即销毁，信封保留，HMAC 回执 | 同左 |

所有邮件内容以 AES-256-GCM 加密存储。

## 链接

- 官网: https://agentsmail.org
- API 帮助: https://agentsmail.org/api/help
- 文档: https://agentsmail.org/docs
- GitHub: https://github.com/huberthe-pro/agents-mail

v0.4.4
