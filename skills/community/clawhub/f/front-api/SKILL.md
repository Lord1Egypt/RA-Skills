---
name: front
description: |
  Front API integration with managed OAuth. Manage conversations, messages, contacts, tags, inboxes, teammates, and teams.
  Use this skill when users want to interact with Front - managing customer communications, conversations, contacts, or team collaboration.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: "📬"
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Front

Access the Front API with managed OAuth authentication. Manage conversations, messages, contacts, tags, inboxes, teammates, and teams.

## Quick Start

```bash
# List inboxes
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/front/inboxes')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/front/
```

Only the endpoints listed in the API Reference section below are supported. Maton proxies requests to `api2.frontapp.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Front OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=front&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'front'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-04-02T22:15:03.462342Z",
    "last_updated_time": "2026-04-02T22:15:37.297108Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "front",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Front connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/front/inboxes')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to conversations, messages, contacts, tags, inboxes, teammates, and teams within the connected Front workspace.
- **All write operations require explicit user approval.** Before executing any send, create, update, or delete call, confirm the target resource and intended effect with the user.
- **Shared workspace scope**: Front resources (inboxes, conversations, contacts, tags, teams) are shared across the workspace. Modifications are visible to all teammates.

## API Reference

### Company / Me

#### Get Current Company

```bash
GET /front/me
```

**Response:**
```json
{
  "_links": {"self": "https://company.api.frontapp.com/me"},
  "name": "Company Name",
  "id": "cmp_12345"
}
```

### Teammates

#### List Teammates

```bash
GET /front/teammates
```

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "tea_pa3u0",
      "email": "user@example.com",
      "username": "username",
      "first_name": "John",
      "last_name": "Doe",
      "is_admin": true,
      "is_available": true,
      "is_blocked": false,
      "type": "user"
    }
  ]
}
```

#### Get Teammate

```bash
GET /front/teammates/{teammate_id}
```

### Teams

#### List Teams

```bash
GET /front/teams
```

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "tim_9p8dk",
      "name": "Customer Support"
    },
    {
      "id": "tim_9p8fc",
      "name": "Sales"
    }
  ]
}
```

### Inboxes

#### List Inboxes

```bash
GET /front/inboxes
```

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "inb_lzrag",
      "name": "Support",
      "is_private": false,
      "is_public": true,
      "address": "support@company.com",
      "send_as": "support@company.com",
      "type": "smtp"
    }
  ]
}
```

#### Get Inbox

```bash
GET /front/inboxes/{inbox_id}
```

#### Create Inbox

```bash
POST /front/inboxes
Content-Type: application/json

{
  "name": "New Inbox",
  "teammate_ids": ["tea_abc123"]
}
```

### Channels

#### List Channels

```bash
GET /front/channels
```

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "cha_ogobs",
      "name": "support@company.com",
      "address": "support@company.com",
      "send_as": "support@company.com",
      "type": "smtp",
      "is_private": false,
      "is_valid": true
    }
  ]
}
```

#### Get Channel

```bash
GET /front/channels/{channel_id}
```

### Conversations

#### List Conversations

```bash
GET /front/conversations
```

**Query Parameters:**
- `q` - Search query
- `page_token` - Pagination token

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "cnv_abc123",
      "subject": "Help with order",
      "status": "open",
      "assignee": {
        "id": "tea_pa3u0",
        "email": "agent@company.com"
      },
      "recipient": {
        "handle": "customer@example.com"
      },
      "last_message": {
        "body": "Message content..."
      },
      "created_at": 1774828390.948
    }
  ]
}
```

#### Get Conversation

```bash
GET /front/conversations/{conversation_id}
```

#### Update Conversation

```bash
PATCH /front/conversations/{conversation_id}
Content-Type: application/json

{
  "assignee_id": "tea_abc123",
  "inbox_id": "inb_xyz789",
  "status": "archived",
  "tag_ids": ["tag_123"]
}
```

#### Update Conversation Assignee

```bash
PUT /front/conversations/{conversation_id}/assignee
Content-Type: application/json

{
  "assignee_id": "tea_abc123"
}
```

### Messages

#### Get Message

```bash
GET /front/messages/{message_id}
```

**Response:**
```json
{
  "id": "msg_abc123",
  "type": "email",
  "is_inbound": true,
  "created_at": 1774828390.948,
  "blurb": "Message preview...",
  "body": "Full message content...",
  "author": {
    "id": "tea_pa3u0",
    "email": "agent@company.com"
  },
  "recipients": [
    {
      "handle": "customer@example.com",
      "role": "to"
    }
  ]
}
```

#### Send Reply

```bash
POST /front/conversations/{conversation_id}/messages
Content-Type: application/json

{
  "author_id": "tea_abc123",
  "body": "Thank you for reaching out!",
  "type": "reply"
}
```

#### Send New Message

```bash
POST /front/channels/{channel_id}/messages
Content-Type: application/json

{
  "author_id": "tea_abc123",
  "to": ["customer@example.com"],
  "subject": "Following up",
  "body": "Hi, just following up on your inquiry..."
}
```

### Contacts

#### List Contacts

```bash
GET /front/contacts
```

**Query Parameters:**
- `q` - Search query (email, name, phone)
- `page_token` - Pagination token

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "crd_54wgwiw",
      "name": "John Doe",
      "description": "",
      "handles": [
        {"source": "email", "handle": "john@example.com"}
      ],
      "groups": [],
      "updated_at": 1774828390.948,
      "is_private": false
    }
  ]
}
```

#### Get Contact

```bash
GET /front/contacts/{contact_id}
```

#### Create Contact

```bash
POST /front/contacts
Content-Type: application/json

{
  "name": "Jane Smith",
  "handles": [
    {"source": "email", "handle": "jane@example.com"}
  ],
  "description": "VIP customer"
}
```

#### Update Contact

```bash
PATCH /front/contacts/{contact_id}
Content-Type: application/json

{
  "name": "Jane Smith-Jones",
  "description": "Updated description"
}
```

#### Delete Contact

```bash
DELETE /front/contacts/{contact_id}
```

### Tags

#### List Tags

```bash
GET /front/tags
```

**Response:**
```json
{
  "_pagination": {"next": null},
  "_results": [
    {
      "id": "tag_6v3mzs",
      "name": "Urgent",
      "highlight": "red",
      "description": "High priority items",
      "is_private": false,
      "is_visible_in_conversation_lists": true
    }
  ]
}
```

#### Get Tag

```bash
GET /front/tags/{tag_id}
```

#### Create Tag

```bash
POST /front/tags
Content-Type: application/json

{
  "name": "Follow-up",
  "highlight": "blue",
  "description": "Needs follow-up"
}
```

#### Update Tag

```bash
PATCH /front/tags/{tag_id}
Content-Type: application/json

{
  "name": "Updated Tag Name",
  "highlight": "green"
}
```

#### Delete Tag

```bash
DELETE /front/tags/{tag_id}
```

### Accounts

#### List Accounts

```bash
GET /front/accounts
```

#### Get Account

```bash
GET /front/accounts/{account_id}
```

#### Create Account

```bash
POST /front/accounts
Content-Type: application/json

{
  "name": "Acme Corp",
  "description": "Enterprise customer",
  "domains": ["acme.com"]
}
```

#### Update Account

```bash
PATCH /front/accounts/{account_id}
Content-Type: application/json

{
  "name": "Acme Corporation",
  "description": "Updated description"
}
```

### Comments

#### List Conversation Comments

```bash
GET /front/conversations/{conversation_id}/comments
```

#### Create Comment

```bash
POST /front/conversations/{conversation_id}/comments
Content-Type: application/json

{
  "author_id": "tea_abc123",
  "body": "Internal note: Customer is a VIP"
}
```

## Pagination

Front uses cursor-based pagination with `_pagination` in responses:

```json
{
  "_pagination": {
    "next": "https://api2.frontapp.com/contacts?page_token=abc123"
  },
  "_results": [...]
}
```

To get the next page, use the `page_token` parameter:

```bash
GET /front/contacts?page_token=abc123
```

When `_pagination.next` is `null`, there are no more results.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/front/inboxes',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data._results);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/front/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
contacts = response.json()['_results']
```

### Create Contact and Tag Conversation

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create a contact
contact_resp = requests.post(
    'https://api.maton.ai/front/contacts',
    headers=headers,
    json={
        'name': 'New Customer',
        'handles': [{'source': 'email', 'handle': 'new@example.com'}]
    }
)
contact = contact_resp.json()

# Tag a conversation
conversation_id = 'cnv_abc123'
requests.patch(
    f'https://api.maton.ai/front/conversations/{conversation_id}',
    headers=headers,
    json={'tag_ids': ['tag_urgent']}
)
```

## Notes

- Resource IDs use prefixes: `tea_` (teammate), `tim_` (team), `inb_` (inbox), `cha_` (channel), `cnv_` (conversation), `msg_` (message), `crd_` (contact), `tag_` (tag), `cmp_` (company)
- Timestamps are Unix timestamps (seconds since epoch)
- The API returns `_links` with related resource URLs
- Responses include `_pagination` for list endpoints
- Maton proxies to your company's Front API subdomain (e.g., `company.api.frontapp.com`)
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Front connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Front API |

## Resources

- [Front API Reference](https://dev.frontapp.com/reference/introduction)
- [Front API Authentication](https://dev.frontapp.com/docs/authentication)
- [Front API Rate Limits](https://dev.frontapp.com/docs/rate-limiting)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
