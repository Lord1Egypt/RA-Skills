---
name: feishu-api-lookup
description: |
  Look up Feishu Open API documentation. Activate when: needing to find a specific Feishu API endpoint,
  understanding API parameters/response, writing scripts that call Feishu APIs, or troubleshooting
  Feishu API errors. Uses web_search + web_fetch to find and extract API docs in real-time.
---

# Feishu API Lookup

Query Feishu Open Platform API documentation on demand. Since the Feishu docs site is a SPA that can't be statically scraped, this skill uses web search + page fetch to find API docs in real-time.

## When to Use

- Need to find a Feishu API endpoint (e.g., "how to forward a thread")
- Need to understand API parameters, request/response format
- Writing a Python/Node script that calls Feishu APIs
- Troubleshooting Feishu API error codes
- The built-in OpenClaw feishu plugin doesn't support the needed operation

## How to Look Up

### Step 1: Search for the API

Use `web_search` with targeted queries:

```
web_search("飞书 open API {你要找的功能} site:open.feishu.cn")
```

**Search tips:**
- Use Chinese keywords for better results: "发送消息", "转发话题", "合并转发", "创建文档", "多维表格"
- Add `site:open.feishu.cn` to limit to official docs
- Add `POST /im/v1/` or similar path patterns if you know the API domain
- Alternative: search `site:feishu.apifox.cn` for the Apifox mirror (sometimes more accessible)

**Common API domains:**
| Domain | Path prefix | Description |
|--------|------------|-------------|
| 消息 (IM) | `/im/v1/` | Messages, threads, reactions, pins |
| 通讯录 | `/contact/v3/` | Users, departments, groups |
| 云文档 | `/drive/v1/`, `/docx/v1/` | Docs, sheets, files |
| 多维表格 | `/bitable/v1/` | Bitable (multidimensional tables) |
| 知识库 | `/wiki/v2/` | Wiki spaces, nodes |
| 日历 | `/calendar/v4/` | Calendars, events |
| 审批 | `/approval/v4/` | Approvals |
| 任务 | `/task/v2/` | Tasks |
| 群组 | `/im/v1/chats/` | Chat groups |
| 权限 | `/drive/v1/permissions/` | File permissions |
| 应用 | `/application/v6/` | App management |

### Step 2: Fetch the API doc page

Use `web_fetch` to get the doc content:

```
web_fetch("https://open.feishu.cn/document/server-docs/im-v1/message/create", maxChars=15000)
```

**⚠️ The official docs site is SPA-rendered — `web_fetch` may return empty content.**

**Fallbacks when web_fetch fails:**
1. Try the Apifox mirror: `https://feishu.apifox.cn` (search for the API there)
2. Search for the Chinese doc URL pattern: `https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/...`
3. Use `web_search` with more specific queries to find the exact parameters

### Step 3: Extract key information

From the doc, extract:
- **HTTP Method + URL**: e.g., `POST /open-apis/im/v1/messages/{message_id}/forward`
- **Headers**: Usually `Authorization: Bearer {tenant_access_token}` + `Content-Type: application/json`
- **Path params**: Variables in the URL
- **Query params**: Required/optional query parameters
- **Request body**: JSON structure with field types and descriptions
- **Response body**: Expected response format
- **Error codes**: Common errors and fixes
- **Required permissions**: Which scopes are needed

## Authentication

Almost all Feishu APIs need a `tenant_access_token`. Get it from:

```python
import json, urllib.request

with open('/root/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
app_id = cfg['channels']['feishu']['appId']
app_secret = cfg['channels']['feishu']['appSecret']

req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
    headers={"Content-Type": "application/json"}
)
token = json.loads(urllib.request.urlopen(req).read())['tenant_access_token']
```

## Common Patterns

### Send a request to Feishu API

```python
req = urllib.request.Request(
    f'https://open.feishu.cn/open-apis/{api_path}',
    data=json.dumps(body).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
)
try:
    resp = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    resp = json.loads(e.read().decode())
```

### Pagination pattern

Many list APIs use cursor-based pagination:
```python
page_token = None
all_items = []
while True:
    url = f'https://open.feishu.cn/open-apis/{path}?page_size=50'
    if page_token:
        url += f'&page_token={page_token}'
    resp = fetch(url)
    all_items.extend(resp['data']['items'])
    if not resp['data'].get('has_more'):
        break
    page_token = resp['data']['page_token']
```

## Frequently Used APIs (Quick Reference)

### Messages (IM)
| Action | Method | Path |
|--------|--------|------|
| Send message | POST | `/im/v1/messages?receive_id_type={type}` |
| Reply to message | POST | `/im/v1/messages/{message_id}/reply` |
| Forward message | POST | `/im/v1/messages/{message_id}/forward?receive_id_type={type}` |
| Merge forward | POST | `/im/v1/messages/merge_forward?receive_id_type={type}` |
| Forward thread | POST | `/im/v1/threads/{thread_id}/forward?receive_id_type={type}` |
| Get message | GET | `/im/v1/messages/{message_id}` |
| List messages | GET | `/im/v1/messages?container_id_type=chat&container_id={id}` |
| Delete message | DELETE | `/im/v1/messages/{message_id}` |
| Update message | PATCH | `/im/v1/messages/{message_id}` |
| Add reaction | POST | `/im/v1/messages/{message_id}/reactions` |
| Get message file | GET | `/im/v1/messages/{message_id}/resources/{file_key}?type={type}` |

### Groups (Chat)
| Action | Method | Path |
|--------|--------|------|
| Create group | POST | `/im/v1/chats` |
| Get group info | GET | `/im/v1/chats/{chat_id}` |
| List members | GET | `/im/v1/chats/{chat_id}/members` |
| Add members | POST | `/im/v1/chats/{chat_id}/members` |

### Docs
| Action | Method | Path |
|--------|--------|------|
| Create document | POST | `/docx/v1/documents` |
| Get document content | GET | `/docx/v1/documents/{document_id}/raw_content` |
| List blocks | GET | `/docx/v1/documents/{document_id}/blocks` |
| Create block | POST | `/docx/v1/documents/{document_id}/blocks/{block_id}/children` |
| Update block | PATCH | `/docx/v1/documents/{document_id}/blocks/{block_id}` |
| Delete block | DELETE | `/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete` |

### Drive
| Action | Method | Path |
|--------|--------|------|
| Upload file | POST | `/drive/v1/medias/upload_all` |
| List folder | GET | `/drive/v1/files?folder_token={token}` |
| Get file info | GET | `/drive/v1/metas/batch_query` |
| Move file | POST | `/drive/v1/files/{file_token}/move` |

### Bitable
| Action | Method | Path |
|--------|--------|------|
| List records | GET | `/bitable/v1/apps/{app_token}/tables/{table_id}/records` |
| Create record | POST | `/bitable/v1/apps/{app_token}/tables/{table_id}/records` |
| Update record | PUT | `/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}` |
| List fields | GET | `/bitable/v1/apps/{app_token}/tables/{table_id}/fields` |
| Search records | POST | `/bitable/v1/apps/{app_token}/tables/{table_id}/records/search` |

### Wiki
| Action | Method | Path |
|--------|--------|------|
| List spaces | GET | `/wiki/v2/spaces` |
| Get node | GET | `/wiki/v2/spaces/get_node?token={token}` |
| List nodes | GET | `/wiki/v2/spaces/{space_id}/nodes` |
| Create node | POST | `/wiki/v2/spaces/{space_id}/nodes` |

### Permissions
| Action | Method | Path |
|--------|--------|------|
| List permissions | GET | `/drive/v1/permissions/{token}/members?type={type}` |
| Add permission | POST | `/drive/v1/permissions/{token}/members?type={type}` |
| Remove permission | DELETE | `/drive/v1/permissions/{token}/members/{member_id}?type={type}` |

## Error Handling

Common error codes:
- `99991663` — Invalid tenant_access_token (expired or wrong)
- `99991668` — Invalid user_access_token
- `230001` — Invalid request parameter
- `230002` — Bot not in group
- `230013` — User not in bot's availability scope
- `230020` — Rate limit exceeded
- `230027` — Insufficient permissions

## Tips

1. **Always use the `/open-apis/` prefix** in the full URL: `https://open.feishu.cn/open-apis/im/v1/messages`
2. **Token expires in 2 hours** — cache it but refresh before expiry
3. **receive_id_type matters** — `open_id` for users, `chat_id` for groups, `union_id` for cross-app
4. **File uploads use multipart/form-data**, not JSON
5. **Feishu vs Lark** — same API, different domain (`open.feishu.cn` vs `open.larksuite.com`)
