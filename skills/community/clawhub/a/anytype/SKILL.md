---
name: anytype
description: Interact with Anytype via anytype-cli and its HTTP API. Use when reading, creating, updating, or searching objects/pages in Anytype spaces; managing spaces; or automating Anytype workflows. Covers first-time setup (account creation, service start, space joining, API key) and ongoing API usage.
metadata:
  openclaw:
    requires:
      env:
        - ANYTYPE_API_KEY
    primaryEnv: ANYTYPE_API_KEY
---

# Anytype Skill

Binary: `anytype` (install via https://github.com/anyproto/anytype-cli)
API base: `http://127.0.0.1:31012`
Auth: `Authorization: Bearer <ANYTYPE_API_KEY>` (key stored in `.env` as `ANYTYPE_API_KEY`)
API docs: https://developers.anytype.io

> **Instance config:** Space IDs, tag IDs, collection IDs, and sharing links are in `SETUP.md` (same directory). Read that alongside this file.

## Check Status First

```bash
anytype auth status     # is an account set up?
anytype space list      # is the service running + spaces joined?
```

If either fails → follow **Setup** below. Otherwise skip to **API Usage**.

## Setup (one-time)

```bash
# 1. Create a dedicated bot account (generates a key, NOT mnemonic-based)
anytype auth create my-bot

# 2. Install and start as a user service
anytype service install
anytype service start

# 3. Have the space owner send an invite link from Anytype desktop, then join
anytype space join <invite-link>

# 4. Create an API key
anytype auth apikey create my-key

# 5. Store the key
echo "ANYTYPE_API_KEY=<key>" >> ~/.openclaw/workspace/.env
```

## API Usage

Load the API key (reads only `ANYTYPE_API_KEY` from env or `.env`):
```python
import os, requests

def load_api_key():
    if "ANYTYPE_API_KEY" in os.environ:
        return os.environ["ANYTYPE_API_KEY"]
    env_path = os.path.expanduser("~/.openclaw/workspace/.env")
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.strip().startswith("ANYTYPE_API_KEY="):
                return line.strip().split("=", 1)[1]
    return ""

API_KEY = load_api_key()
BASE = 'http://127.0.0.1:31012'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
```

See `references/api.md` for all endpoints and request shapes.

### Common Patterns

**List spaces:**
```
GET /v1/spaces
```

**Search objects globally:**
```
POST /v1/search
{"query": "meeting notes", "limit": 10}
```

**List objects in a space:**
```
GET /v1/spaces/{space_id}/objects?limit=50
```

**Create an object:**
```
POST /v1/spaces/{space_id}/objects
{"type_key": "page", "name": "My Page", "body": "Markdown content here"}
```

**Update an object (patch body/properties):**
```
PATCH /v1/spaces/{space_id}/objects/{object_id}
{"markdown": "Updated content"}
```

⚠️ **Create uses `body`, Update uses `markdown`** — different field names for the same content. Easy to mix up.

⚠️ **CRITICAL: PATCH does NOT update the body/content field.** Sending `body` or `markdown` in a PATCH silently succeeds (HTTP 200) but the content is NOT updated in Anytype. Only metadata fields like `name` are updated via PATCH.

**The only reliable way to update an object's content is: DELETE + recreate.**

⚠️ **This is destructive.** Always save the old content before deleting:

```python
# Step 0: fetch and save existing content before deleting
old = requests.get(f"{BASE}/v1/spaces/{space_id}/objects/{old_id}", headers=headers).json()
old_content = old.get("object", {}).get("snippet", "")  # keep a local copy

# Step 1: delete old object (irreversible via API — confirm before running)
requests.delete(f"{BASE}/v1/spaces/{space_id}/objects/{old_id}", headers=headers)

# Step 2: create new object with full updated content
resp = requests.post(f"{BASE}/v1/spaces/{space_id}/objects",
    json={"name": name, "type_key": "page", "body": new_content},
    headers=headers)
new_id = resp.json()["object"]["id"]
```

Store the new object ID — callers must update any references (e.g. `related_pages`) after recreation. Deleted objects may be recoverable from the Anytype bin in the desktop app.

Use `scripts/anytype_api.py` as a ready-made helper for making API calls.

## Key Constraints (learned from testing)

- **`links` property is read-only** — system-managed, populated only by the desktop editor. API returns 400 if you try to set it.
- **Collections cannot have an `icon` set on create** — causes a 500. Create without icon, add it after.
- **`body` vs `markdown`** — create uses `body`, update uses `markdown`.
- **PATCH cannot update content** — `body`/`markdown` fields in PATCH are silently ignored. HTTP 200 is returned but content is unchanged. To update content: DELETE + recreate.
- **`related_pages` custom property** (key: `related_pages`, format: `objects`) — writable via API for linking objects. Must be created in the space first if it doesn't exist.

---

## Object Type Preference

**Default to `page` for all content.** Notes (`note` type) are the exception — use only when content is informal/scratchpad and doesn't need linking into the knowledge graph.

Everything meaningful (call notes, research, hub pages, product docs, meeting summaries) → `type_key: "page"`.

---

## Knowledge Graph Principles — Apply These Always

Anytype is a **linked knowledge base**, not a flat file store. Every time you create or update content, ask: *how does this connect to what already exists?*

### 1. Link Everything
- Use `[[Page Name]]` style inline links in the markdown body to reference related objects.
- When creating a new page, search for related existing pages first and link back to them.
- When updating an existing page, add links to any newly created pages that are related.

### 2. Collections as Cluster Containers
- For any topic cluster, create a **Collection** (`type_key: collection`) — not a plain page hub.
- Collections are Anytype's native container type. They appear in the sidebar, support multiple views (grid, list, kanban), and are queryable.
- Use the **Lists API** to add child objects to a collection.
- Also maintain a **hub page** inside the collection as the written overview (description + links).

**Create + populate a collection:**
```python
# 1. Create (no icon on create — causes 500)
col = api('POST', f'/v1/spaces/{SPACE}/objects', {'type_key': 'collection', 'name': 'My Cluster'})
col_id = col['object']['id']

# 2. Add objects
api('POST', f'/v1/spaces/{SPACE}/lists/{col_id}/objects', {'objects': [id1, id2, id3]})
```

**Sidebar note:** Sidebar pinning is manual only — no API. Ask the user to pin collections in the Anytype desktop app.

### 3. Bidirectional Awareness
- Anytype shows backlinks automatically, but you must **write forward links** in the body.
- After creating content, update the hub page to include a link to the new object.

### 4. Before Creating a Page
```
1. Search: POST /v1/spaces/{space_id}/search {"query": "<topic>", "limit": 10}
2. Check if a page already exists — update it rather than duplicate
3. Identify the parent hub page(s) this belongs to
4. Create the page with inline links to related pages in the body
5. Update the hub page(s) to add a link to the new page
```

### 5. Hub Page Template
When creating a hub page, use this structure:

```markdown
## Overview
<2-3 sentence summary>

## Pages
- [Child Page Name](anytype://object?objectId=<id>&spaceId=<space_id>) — one-line description
- [Another Page](anytype://object?objectId=<id>&spaceId=<space_id>) — one-line description

## Key Facts
- Fact 1
- Fact 2
```

### 6. Native Object Links (Anytype Graph Feature)

Anytype has two link mechanisms. Use **both**:

#### A. System `links` property (read-only via API)
The built-in `links` property is auto-populated by the Anytype desktop app when you use `@mention` or `[[]]` syntax in the rich text editor. **The API cannot set it directly** — attempting to do so returns `400`.

#### B. Custom `related_pages` property (writable via API) ✅
Create a custom `objects`-type property called **`related_pages`** (key: `related_pages`) in your space. This shows up in each object's sidebar and lets the API express object relationships.

```json
// On create:
{
  "type_key": "page",
  "name": "My Page",
  "body": "...",
  "properties": [
    {"key": "related_pages", "objects": ["<hub_id>", "<sibling_id>"]}
  ]
}
```

**Rule:** Hub pages → `related_pages` set to all children. Child pages → `related_pages` set back to their hub. This creates visible edges in the graph view.

### 7. Inline Links Syntax

**Use `anytype://` deep links — NOT `object.any.coop` URLs — for links inside the app.**

`object.any.coop` URLs in body text render as plain text and are NOT clickable inside Anytype. The only format that renders as a clickable internal link is:

```markdown
[Link Text](anytype://object?objectId=<object_id>&spaceId=<space_id>)
```

Helper function:
```python
def anytype_link(name, obj_id, space_id):
    return f"[→ Open: {name}](anytype://object?objectId={obj_id}&spaceId={space_id})"
```

**⚠️ Do NOT put links inside markdown headings** — Anytype strips the link and renders only plain text. Links only work as inline body text.

Use `object.any.coop` links only when sharing with external users (outside the Anytype app).

### 8. Tags

Tags require pre-existing tag option IDs in the space — you cannot pass free-text strings directly.

**Create a new tag:**
```
POST /v1/spaces/{space_id}/properties/{tag_property_id}/tags
{"name": "my-tag", "color": "blue"}
→ returns tag.id — use that ID in multi_select
```

**Set tags on an object:**
```json
PATCH /v1/spaces/{space_id}/objects/{object_id}
{
  "properties": [
    {"key": "tag", "multi_select": ["<tag_id_1>", "<tag_id_2>"]}
  ]
}
```

> See `SETUP.md` for the tag property ID and all defined tag IDs for this instance.

### 9. Proactive Organization Checklist
After any write operation, run through:
- [ ] Does a hub page exist for this topic? If not, create one.
- [ ] Did I link the new/updated page from the hub?
- [ ] Did I link related pages from within the new content?
- [ ] Are there orphan pages (no incoming links) I should connect?
- [ ] Did I set `tag` (project + content type + domain) on the new page?
- [ ] Did I set `related_pages` pointing to the hub?

---

## Sharing Links

**Use the public web link format when sharing externally:**

```
https://object.any.coop/{object_id}?spaceId={space_id}&inviteId={invite_id}#{hash}
```

The `inviteId` and `#hash` are space-level constants. Only `object_id` changes per object.

> See `SETUP.md` for this instance's `spaceId`, `inviteId`, and `hash`.
