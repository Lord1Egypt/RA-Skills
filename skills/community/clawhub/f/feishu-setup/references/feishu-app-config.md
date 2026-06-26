# Feishu Open Platform App Configuration

Step-by-step guide to configure a Feishu App on the Open Platform for use with OpenClaw.

## 1. Create App

1. Visit [Feishu Open Platform](https://open.feishu.cn/app)
2. Click "Create Custom App"
3. Fill in:
   - **App Name**: Your bot's display name
   - **Description**: Brief description
   - **Icon**: Upload an icon
4. After creation, note:
   - **App ID** (`cli_xxx`) — needed in OpenClaw config
   - **App Secret** — needed in OpenClaw config (keep secret!)

## 2. Enable Capabilities

Under "Capabilities & Features" (能力与权益), enable:

### 2.1 Bot (机器人)

Enable the Bot capability so users can chat with the app.

### 2.2 Webhooks

Under "Event Subscriptions" (事件订阅):
- Set **Request URL**: `<YOUR_OPENCLAW_URL>/feishu/webhook`
- The platform will send a verification challenge; openclaw-lark handles this automatically
- After verification, subscribe to events (see below)

### 2.3 Card Interaction (可选)

If using interactive message cards, enable card callback.

## 3. Permission Scopes (权限管理)

Under "Permissions & Scopes" (权限管理), search and enable these scopes:

### IM (消息与群组) — Required

| Scope | Description |
|-------|-------------|
| `im:message` | Send and receive messages |
| `im:message:send_as_bot` | Send messages as bot |
| `im:resource` | Access message resources (images, files) |
| `im:chat` | Access chat/group info |
| `im:chat:readonly` | Read chat info |

### Contact (通讯录)

| Scope | Description |
|-------|-------------|
| `contact:user.id:readonly` | Read user IDs |
| `contact:user.base:readonly` | Read basic user info (name, avatar) |
| `contact:user.phone:readonly` | Read phone numbers |
| `contact:user.email:readonly` | Read email addresses |
| `contact:user.department_id:readonly` | Read department IDs |

### Calendar (日历)

| Scope | Description |
|-------|-------------|
| `calendar:calendar` | Manage calendars |
| `calendar:calendar:readonly` | Read calendar info |
| `calendar:event` | Manage events |
| `calendar:event:readonly` | Read events |
| `calendar:freebusy:readonly` | Read free/busy status |

### Docs & Drive (云文档)

| Scope | Description |
|-------|-------------|
| `docx:document` | Read and write documents |
| `docx:document:readonly` | Read documents |
| `drive:drive` | Access drive files |
| `drive:drive:readonly` | Read drive files |
| `sheets:spreadsheet` | Access spreadsheets |
| `bitable:app` | Access Bitable (multidimensional tables) |
| `bitable:app:readonly` | Read Bitable data |
| `wiki:wiki` | Access Wiki |
| `wiki:wiki:readonly` | Read Wiki |

### Search (搜索)

| Scope | Description |
|-------|-------------|
| `search:app` | Search across Feishu |

### Approval (审批) — Optional

| Scope | Description |
|-------|-------------|
| `approval:approval` | Access approval workflows |
| `approval:approval:readonly` | Read approvals |

## 4. Event Subscriptions (事件订阅)

Subscribe to these events under "Event Subscriptions":

### Required for IM

| Event | Event Key |
|-------|-----------|
| Receive message | `im.message.receive_v1` |
| Message reaction created | `im.message.reaction_created_v1` |
| Bot joined group | `im.chat.member.bot.added_v1` |
| Bot removed from group | `im.chat.member.bot.deleted_v1` |

### Optional for Calendar

| Event | Event Key |
|-------|-----------|
| Calendar event created | `calendar.calendar.event.created_v6` |
| Calendar event updated | `calendar.calendar.event.updated_v6` |
| Calendar event deleted | `calendar.calendar.event.deleted_v6` |

### Optional for Docs

| Event | Event Key |
|-------|-----------|
| Document permission changed | `drive.drive.permission.member_role.changed_v1` |

## 5. Version & Release

After configuring:
1. Create a version under "Version Management & Release" (版本管理与发布)
2. Submit for review (internal apps may auto-approve)
3. Set availability scope:
   - **All employees** (全员可见)
   - **Specific departments/users** (指定范围)
   - For testing: add yourself first

## 6. Important Notes

- **domain**: Use `"feishu"` for feishu.cn (mainland China), `"lark"` for larksuite.com (international)
- **Encrypt Key & Verification Token**: Found under "Security Settings"; needed if openclaw-lark requires them
- **Self-built app vs Store app**: This guide is for self-built apps (企业自建应用)
- After changing permissions or events, you need to create a new version and publish
