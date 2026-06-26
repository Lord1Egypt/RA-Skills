# Feishu Permission Scopes Reference

OAuth scopes required for each feature area. Configure in Feishu Open Platform → App → Permissions.

## Scope Categories

### IM Scopes (消息)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `im:message` | Send & receive messages | All IM functionality |
| `im:message:send_as_bot` | Bot sends messages | Bot replies |
| `im:resource` | Access message attachments | Download images, files |
| `im:chat` | Manage chats | Group operations |
| `im:chat:readonly` | Read chat info | List groups, get group info |

### Contact Scopes (通讯录)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `contact:user.id:readonly` | Read user IDs | User lookup |
| `contact:user.base:readonly` | Read name, avatar | Display user info |
| `contact:user.phone:readonly` | Read phone | Phone-based lookup |
| `contact:user.email:readonly` | Read email | Email-based lookup |
| `contact:user.department_id:readonly` | Read department | Org chart |
| `contact:user.employee_id:readonly` | Read employee ID | HR integration |

### Calendar Scopes (日历)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `calendar:calendar:readonly` | Read calendars | List calendars, get primary |
| `calendar:calendar` | Manage calendars | Create/modify calendars |
| `calendar:event:readonly` | Read events | View schedule |
| `calendar:event` | Manage events | Create/edit/delete events |
| `calendar:freebusy:readonly` | Read free/busy | Schedule conflict checking |

### Document Scopes (云文档)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `docx:document:readonly` | Read documents | Fetch doc content |
| `docx:document` | Read & write documents | Create/update docs |
| `drive:drive:readonly` | Read drive files | Browse files |
| `drive:drive` | Manage drive files | Upload/download files |

### Bitable Scopes (多维表格)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `bitable:app:readonly` | Read tables | Query data |
| `bitable:app` | Read & write tables | Create/modify tables, records |

### Sheet Scopes (电子表格)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `sheets:spreadsheet` | Access spreadsheets | Read/write sheet data |

### Wiki Scopes (知识库)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `wiki:wiki:readonly` | Read wiki | Browse wiki content |
| `wiki:wiki` | Manage wiki | Create/edit wiki pages |

### Search Scopes (搜索)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `search:app` | Search across Feishu | Unified doc & wiki search |

### Task Scopes (任务)

| Scope | Purpose | Required For |
|-------|---------|-------------|
| `task:task:readonly` | Read tasks | View tasks |
| `task:task` | Manage tasks | Create/edit tasks |
| `task:tasklist` | Manage task lists | Organize tasks |

## Feature-to-Scope Mapping

### Minimal Setup (IM Only)

```
im:message, im:message:send_as_bot, im:resource, im:chat:readonly
contact:user.id:readonly, contact:user.base:readonly
```

### Standard Setup (IM + Calendar + Docs)

```
IM scopes above +
calendar:calendar:readonly, calendar:event, calendar:freebusy:readonly +
docx:document, drive:drive:readonly +
search:app
```

### Full Setup (All Features)

```
All scopes above +
bitable:app +
sheets:spreadsheet +
wiki:wiki +
task:task, task:tasklist
```

## User Authorization Flow

Some scopes require **user authorization** (OAuth). The flow:

1. User sends a message to the bot
2. Bot detects operation needs user-scoped permission
3. Bot sends an authorization card with a link
4. User clicks to authorize
5. Token is stored for subsequent use

The `feishu_oauth` tool handles revocation; `feishu_oauth_batch_auth` handles bulk authorization.

## Scope Status Check

After enabling scopes in the Open Platform:
1. Create a new app version
2. Publish the version
3. Scopes take effect after publication
4. Users may need to re-authorize if new scopes were added
