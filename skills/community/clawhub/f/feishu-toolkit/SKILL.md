---
name: feishu-toolkit
version: 1.0.0
description: >
  Complete Feishu (Lark) integration toolkit for AI agents. Read/write documents, 
  fetch chat history, send files & screenshots, manage permissions, and create 
  scheduled reminders. Supports Wiki, Docs, Sheets, Bitable, and IM operations.
  Triggers: "飞书", "feishu", "lark", "读文档", "群聊记录", "发文件", 
  "截屏发飞书", "文档权限", "定时提醒".
tags: [feishu, lark, document, chat, file, screenshot, permission, reminder, chinese, productivity]
env:
  FEISHU_APP_ID: "Your Feishu app ID (from open.feishu.cn)"
  FEISHU_APP_SECRET: "Your Feishu app secret"
---

# Feishu Toolkit (飞书工具箱)

A comprehensive Feishu (Lark) integration skill for AI agents. Covers 6 major capabilities:

1. **📄 Document Operations** — Read, create, write, and append Feishu Docs, Sheets, Bitable, Wiki
2. **💬 Chat History** — Fetch and summarize group chat messages
3. **📎 File Sending** — Upload and send files to Feishu chats via REST API
4. **📸 Screenshot** — Capture macOS screenshots and send to Feishu
5. **🔐 Permission Management** — List, add, remove document collaborators
6. **⏰ Cron Reminders** — Create scheduled recurring reminders to Feishu chats

---

## Prerequisites

### Feishu App Setup
1. Go to [Feishu Open Platform](https://open.feishu.cn/app) and create an app
2. Enable required permissions:
   - `im:message:send_as_bot` — Send messages
   - `im:resource` — Upload files/images
   - `docx:document` — Read/write documents
   - `drive:permission` — Manage permissions (optional)
3. Set `FEISHU_APP_ID` and `FEISHU_APP_SECRET` environment variables

### Authentication
All API calls use Feishu's tenant access token:
```python
import requests

def get_tenant_token(app_id, app_secret):
    r = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': app_id, 'app_secret': app_secret}
    )
    return r.json()['tenant_access_token']
```

---

## 1. Document Operations (Read/Write/Create/Append)

### Read a Document
```bash
# Fetch document content as Markdown
# Supports: doc, docx, sheet, bitable, wiki
GET /open-apis/docx/v1/documents/{document_id}/raw_content
```

### Create a Document
```bash
POST /open-apis/docx/v1/documents
Body: {"title": "My Document"}
```

### Write (Overwrite) a Document
```bash
# Overwrite entire document content with Markdown
POST /open-apis/docx/v1/documents/{document_id}/blocks/batch_update
```

### Append Content (Long Documents)
For documents exceeding LLM output limits:
1. **Create** the document first to get a `doc_token`
2. **Chunk** content into logical sections
3. **Append** each chunk sequentially
4. Do NOT try to write the entire document in one call if it is very long

### Wiki URL Resolution
Wiki URLs need to be resolved to actual document tokens first:
```bash
POST /open-apis/wiki/v2/spaces/get_node
Body: {"token": "wiki_token"}
# Returns the actual doc_token and doc_type
```

---

## 2. Chat History

Fetch and summarize messages from a Feishu group chat.

### Fetch Messages
```python
# GET /open-apis/im/v1/messages
params = {
    'container_id_type': 'chat',
    'container_id': chat_id,
    'page_size': 50
}
```

### Message Types
| Type | Handling |
|------|----------|
| `text` | Extract `.body.content` JSON → `text` field |
| `interactive` | Extract text nodes from `elements` array |
| `image` | Note as `[图片]` |
| `system` | Filter out unless relevant |

### Pagination
If `has_more=true`, fetch more pages using `page_token`. Default: 50 messages per page.

---

## 3. File Sending

Send files to Feishu chats via REST API.

### Upload File
```python
# POST /open-apis/im/v1/files
headers = {'Authorization': f'Bearer {token}'}
data = {'file_type': 'stream', 'file_name': 'filename.ext'}
files = {'file': ('filename.ext', open(path, 'rb'), 'application/octet-stream')}
```

Supported `file_type`: `opus`, `mp4`, `pdf`, `doc`, `xls`, `ppt`, `stream` (generic)

### Send File Message
```python
# POST /open-apis/im/v1/messages
json = {
    'receive_id': chat_id,
    'msg_type': 'file',
    'content': json.dumps({'file_key': file_key})
}
```

---

## 4. Screenshot & Send

Capture macOS screenshots and send to Feishu.

```bash
# 1. Capture screenshot
SCREENSHOT_PATH="$TMPDIR/screenshot_$(date +%s).png"
screencapture -x "$SCREENSHOT_PATH"

# 2. Upload image
# POST /open-apis/im/v1/images
# data: image_type=message, file=screenshot

# 3. Send image message
# POST /open-apis/im/v1/messages
# msg_type: image, content: {"image_key": "..."}
```

> **Note**: Use `$TMPDIR` not `/tmp` on macOS.

---

## 5. Permission Management

Manage document/file permissions.

### Actions
| Action | Description |
|--------|-------------|
| `list` | List all collaborators |
| `add` | Add collaborator with permission level |
| `remove` | Remove a collaborator |

### Token Types
`doc`, `docx`, `sheet`, `bitable`, `folder`, `file`, `wiki`, `mindnote`

### Member Types
`email`, `openid`, `userid`, `unionid`, `openchat`, `opendepartmentid`

### Permission Levels
| Level | Description |
|-------|-------------|
| `view` | View only |
| `edit` | Can edit |
| `full_access` | Full access (can manage permissions) |

### Example: Share document
```python
# POST /open-apis/drive/v1/permissions/{token}/members
params = {'type': 'docx'}
json = {
    'member_type': 'email',
    'member_id': 'user@company.com',
    'perm': 'edit'
}
```

> **Note**: Permission management is sensitive. Use with caution.

---

## 6. Cron Reminders

Create recurring scheduled reminders to Feishu chats.

### Before Creating
**Always confirm with the user**:
1. **Frequency**: How often? (e.g., every 10 min, every hour, daily at 9am)
2. **Target**: Where to send? (default: current IM conversation)

### Template
```bash
cron add \
  --name "<task_name>" \
  --every "<interval>" \
  --session main \
  --system-event "[CRON] <task_name>. Send message to Feishu: '<reminder_content>'"
```

### Interval Examples
| Interval | Description |
|----------|-------------|
| `1m` | Every minute |
| `5m` | Every 5 minutes |
| `30m` | Every 30 minutes |
| `1h` | Every hour |
| `*/30 * * * *` | Cron expression (with `--tz`) |

### Management
```bash
cron list          # List all tasks
cron edit <id>     # Edit task
cron rm <id>       # Delete (ask user first!)
cron runs --id <id> # View execution history
cron run <id>      # Manual trigger
```

---

## API Reference

| API | Method | Path |
|-----|--------|------|
| Tenant Token | POST | `/auth/v3/tenant_access_token/internal` |
| Read Document | GET | `/docx/v1/documents/{id}/raw_content` |
| Create Document | POST | `/docx/v1/documents` |
| Send Message | POST | `/im/v1/messages` |
| Upload File | POST | `/im/v1/files` |
| Upload Image | POST | `/im/v1/images` |
| List Messages | GET | `/im/v1/messages` |
| Manage Permissions | POST | `/drive/v1/permissions/{token}/members` |
| Resolve Wiki | POST | `/wiki/v2/spaces/get_node` |

Base URL: `https://open.feishu.cn/open-apis`

---

## Notes

- All APIs require `tenant_access_token` in the `Authorization` header
- File upload uses `multipart/form-data`
- Message sending uses `application/json`
- Bot can only download files it uploaded itself
- For detailed API docs, visit: https://open.feishu.cn/document
