# Feishu Tool Matrix

Complete mapping of feishu_* tools to capability areas, with configuration guidance.

## Tool Categories

### IM (消息与通讯)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_im_bot_image` | Download images/files sent to bot (bot identity) | alsoAllow | ✅ Recommended |
| `feishu_im_user_fetch_resource` | Download images/files (user identity, needs OAuth) | alsoAllow | ✅ Recommended |
| `feishu_im_user_get_messages` | Get chat history (user identity) | alsoAllow | ✅ Recommended |
| `feishu_im_user_get_thread_messages` | Get thread replies | alsoAllow | ✅ Recommended |
| `feishu_im_user_message` | Send message as user identity | alsoAllow | ⚠️ Sensitive |
| `feishu_im_user_search_messages` | Search messages across chats | alsoAllow | ✅ Recommended |

### Calendar (日历)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_calendar_calendar` | Calendar CRUD | alsoAllow | ✅ Recommended |
| `feishu_calendar_event` | Event CRUD + search + RSVP | alsoAllow | ✅ Recommended |
| `feishu_calendar_event_attendee` | Attendee management | alsoAllow | ✅ Recommended |
| `feishu_calendar_freebusy` | Free/busy query | alsoAllow | ✅ Recommended |

### Docs (云文档)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_create_doc` | Create doc from Markdown | alsoAllow | ✅ Recommended |
| `feishu_fetch_doc` | Read doc content | alsoAllow | ✅ Recommended |
| `feishu_update_doc` | Update doc (7 modes) | alsoAllow | ✅ Recommended |
| `feishu_doc_comments` | Document comments | alsoAllow | ❌ Disabled by default |
| `feishu_doc_media` | Document media assets | alsoAllow | ❌ Disabled by default |

### Bitable (多维表格)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_bitable_app` | App-level CRUD | alsoAllow | ✅ Recommended |
| `feishu_bitable_app_table` | Table CRUD | alsoAllow | ✅ Recommended |
| `feishu_bitable_app_table_field` | Field (column) management | alsoAllow | ✅ Recommended |
| `feishu_bitable_app_table_record` | Record (row) CRUD + search | alsoAllow | ✅ Recommended |
| `feishu_bitable_app_table_view` | View management | alsoAllow | ❌ Disabled by default |

### Drive & Sheets

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_drive_file` | Drive file management | alsoAllow | ❌ Disabled by default |
| `feishu_sheet` | Spreadsheet operations | alsoAllow | ❌ Disabled by default |

### Wiki (知识库)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_wiki_space` | Wiki space management | alsoAllow | ❌ Disabled by default |
| `feishu_wiki_space_node` | Wiki node management | alsoAllow | ❌ Disabled by default |

### Contacts (通讯录)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_get_user` | Get user info | alsoAllow | ✅ Recommended |
| `feishu_search_user` | Search users by keyword | alsoAllow | ✅ Recommended |

### Chat (群聊)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_chat` | Search/get group info | alsoAllow | ✅ Recommended |
| `feishu_chat_members` | Get group member list | alsoAllow | ✅ Recommended |

### Search (搜索)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_search_doc_wiki` | Unified doc & wiki search | alsoAllow | ✅ Recommended |

### OAuth (授权)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_oauth` | Revoke user authorization | alsoAllow | ✅ Recommended |
| `feishu_oauth_batch_auth` | Batch authorize all scopes | alsoAllow | ✅ Recommended |

### Task (任务)

| Tool | Description | Config Key | Default |
|------|-------------|------------|---------|
| `feishu_task_task` | Task CRUD | alsoAllow | ❌ Disabled by default |
| `feishu_task_tasklist` | Task list management | alsoAllow | ❌ Disabled by default |
| `feishu_task_comment` | Task comments | alsoAllow | ❌ Disabled by default |
| `feishu_task_subtask` | Subtask management | alsoAllow | ❌ Disabled by default |

## Enable/Disable Logic

Tools work through two config arrays:

1. **`tools.alsoAllow`**: Tools available in the `full` profile that need explicit enabling. Feishu tools must be listed here.
2. **`tools.deny`**: Tools to explicitly disable. Takes precedence over alsoAllow.

**To enable a disabled tool**: Remove from `tools.deny` array.
**To disable a tool**: Add to `tools.deny` array.

```bash
# Example: Enable feishu_task_task
openclaw config get tools.deny --json
# Edit the array to remove feishu_task_task, then:
openclaw config set tools.deny '[...]' --strict-json
```

## Bundled Skills

openclaw-lark ships with these skills (auto-available when plugin is enabled):

| Skill | Description |
|-------|-------------|
| `feishu-bitable` | Bitable creation, query, editing. 27 field types, advanced filtering, batch ops. |
| `feishu-calendar` | Calendar & event management, attendee management, free/busy query. |
| `feishu-channel-rules` | Lark/Feishu channel output rules. Always active. |
| `feishu-create-doc` | Create cloud docs from Markdown. |
| `feishu-fetch-doc` | Read cloud doc content as Markdown. |
| `feishu-im-read` | IM message reading: history, thread, search, resource download. |
| `feishu-task` | Task management (requires skill enabled + tools un-denied). |
| `feishu-troubleshoot` | Feishu plugin diagnostics and FAQ. |
| `feishu-update-doc` | Update cloud docs (7 modes: append, overwrite, replace, insert, delete). |
