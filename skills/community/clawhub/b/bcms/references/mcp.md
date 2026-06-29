# BCMS Model Context Protocol (MCP)

Official documentation: [BCMS docs](https://thebcms.com/docs) · [MCP guide](https://thebcms.com/docs/mcp)

BCMS exposes an **MCP server** so coding assistants (Cursor, Claude Code, VS Code, Windsurf, Codex, etc.) can read and mutate BCMS content and schema using a dedicated API key. MCP complements the **`@thebcms/client` SDK**: use MCP when the agent has MCP tools configured; use the SDK inside applications, CI, and server code.

The server registers a fixed set of **kebab-case** tools (their names do **not** contain template IDs) plus a few read-only **resources**. The same tool set is available to every key that has MCP enabled.

## Enabling MCP and keys

1. In the BCMS dashboard, create or edit an **API key** and turn on **MCP access**.
2. The key string is the same three-part API key used by the REST client: **`keyId.secret.instanceId`**.
3. Keep the key in **environment variables** or secure local config — never commit it.

The MCP endpoint authenticates the key on every connection:

- The key must split into exactly **three** dot-separated parts (`keyId.secret.instanceId`).
- The `keyId` + `instanceId` must resolve to a real key, the `secret` must match, and the key must have the **MCP flag** enabled.
- A key **without** the MCP flag is rejected (`403` — key does not have MCP access).

> The MCP layer exposes the **full tool set** to any key that has MCP enabled; it does not hide individual tools based on per-template GET/POST/PUT/DELETE toggles. Operations execute as the key's user, so treat an MCP key as a write-capable credential and scope/rotate it accordingly.

## Client configuration (Cursor, Claude, etc.)

Point your MCP client at the BCMS MCP URL with the key passed as the **`mcpKey`** query parameter:

```json
{
  "mcpServers": {
    "bcms": {
      "url": "https://app.thebcms.com/api/v3/mcp?mcpKey=YOUR_MCP_KEY_HERE"
    }
  }
}
```

- The endpoint path is **`/api/v3/mcp`** and the key query parameter is **`mcpKey`** (not `apiKey`).
- `YOUR_MCP_KEY_HERE` is the full three-part `keyId.secret.instanceId` string.
- Replace the host if your organization uses a custom BCMS app URL.

### Environment-based URL (recommended)

Avoid pasting the key into JSON checked into git:

- **Shell**: `export BCMS_MCP_KEY='keyId.secret.instanceId'`, then build the URL `https://<app-host>/api/v3/mcp?mcpKey=$BCMS_MCP_KEY` where your client supports variable expansion.
- **Cursor / VS Code**: keep the URL in **user** MCP config (not the repo) or a secret manager.

If your MCP client does not expand env vars, generate the full URL at runtime or use a small wrapper script — never commit the literal key.

## Transport and sessions

- The server uses **Streamable HTTP** (MCP over HTTP).
- The first request must be an **`initialize`** request; the server creates a session and returns an **`mcp-session-id`**.
- Every subsequent HTTP request in that session must include the **`mcp-session-id`** header. Requests without a session id (that are not `initialize`) are rejected, and an unknown/expired session id returns a "session not found" error.
- Most MCP clients manage the session header automatically. On session errors, re-run the `initialize` flow.

### Session lifecycle (mental model)

1. Client opens a connection to the MCP URL (with the `mcpKey` query param).
2. Client sends **`initialize`**; the server creates a session and returns the **`mcp-session-id`**.
3. Every subsequent request includes that **`mcp-session-id`** header (your client usually handles this).
4. On "session invalid" / "session not found", discard the session id and repeat from step 1.

## HTTP errors and what they usually mean

| Situation | Typical cause | What to do |
|-----------|----------------|------------|
| **400** at connect | Key is not three dot-separated parts | Use the full `keyId.secret.instanceId` string |
| **401** at connect | Key not found, or wrong `secret` | Verify the key in the dashboard; rotate if needed |
| **403** at connect | Key exists but **MCP flag** is off | Enable MCP access on the key in the dashboard |
| **404** at connect | Instance segment does not resolve | Check the `instanceId` part of the key |
| Missing `mcpKey` | URL is missing the query parameter | Add `?mcpKey=<three-part-key>` to the URL |
| Session / stream errors | Missing `mcp-session-id`, expired session, or a proxy stripping headers | Re-initialize; ensure the client sends the session header on follow-ups |
| Tool returns an `error` object | Operation failed downstream (validation, not-found, etc.) | Read `structuredContent.error.status` / `.message` and adjust the call |

Tool results are always wrapped: success returns `{ data }` and failures return `{ error: { status, message } }` (both in `structuredContent` and as JSON text). A tool call that fails server-side still returns HTTP 200 with the `error` object — inspect the payload, not just the status code.

## What MCP can do

The MCP server exposes full CRUD over content **and** schema, plus media and supporting resources. This includes operations the docs previously described as dashboard-only:

- **Entries**: list, read, **create**, **update**, **delete**.
- **Templates, groups, widgets**: list, read, **create**, **update**, **delete** (schema design is available over MCP, not dashboard-only).
- **Entry statuses**: list, read, create, update, delete.
- **Entry history**: list and read history items and their file data.
- **Languages**: list available/added, read, add, update, delete.
- **Media**: list items and directories, read, create directories, and request a pre-signed upload URL for files.
- **Pointer links**: resolve internal **entry** and **media** pointer strings for rich-text links.
- **Trash**: list and read trashed items and their file data.

There is no media-file *delete* tool and no base64 media-upload tool; media files are uploaded via the pre-signed URL returned by `request-upload-media-url`.

## Tools (as registered by the server)

All tool names are **kebab-case** and fixed — they take IDs (e.g. `templateId`, `entryId`) as **input arguments** rather than encoding the ID in the tool name.

### Instance

| Tool | Purpose |
|------|--------|
| `instance-get` | Get the current instance details |

### Templates

| Tool | Purpose |
|------|--------|
| `get-all-templates` | List all templates |
| `get-template-by-id` | Get one template by ID |
| `create-template` | Create a template |
| `update-template` | Update a template (add/update/remove props via `propChanges`) |
| `delete-template-by-id` | Delete a template |

### Entries

| Tool | Purpose |
|------|--------|
| `get-all-entries-by-template-id` | List entries for a template (`templateId` argument) |
| `get-entry-by-id` | Get one entry by ID |
| `create-entries` | Create an entry (`templateId`, `statuses`, `meta`, `content`) |
| `update-entries` | Update an entry |
| `delete-entries` | Delete an entry (`templateId`, `entryId`) |

### Entry statuses

| Tool | Purpose |
|------|--------|
| `list-entry-statuses` | List entry statuses |
| `get-entry-status-by-id` | Get one status by ID |
| `create-entry-status` | Create a status |
| `update-entry-status` | Update a status |
| `delete-entry-status-by-id` | Delete a status |

### Entry history

| Tool | Purpose |
|------|--------|
| `get-all-entry-history-items` | List all history items |
| `get-entry-history-items-for-entry` | List history items for one entry |
| `get-entry-history-by-id` | Get one history item by ID |
| `get-entry-history-file-data` | Get the stored file data for a history item |

### Groups

| Tool | Purpose |
|------|--------|
| `get-all-groups` | List all groups |
| `get-group-by-id` | Get one group by ID |
| `create-group` | Create a group |
| `update-group` | Update a group (props via `propChanges`) |
| `delete-group-by-id` | Delete a group |

### Widgets

| Tool | Purpose |
|------|--------|
| `get-all-widgets` | List all widgets |
| `get-widget-by-id` | Get one widget by ID |
| `create-widget` | Create a widget |
| `update-widget` | Update a widget (props via `propChanges`) |
| `delete-widget-by-id` | Delete a widget |

### Languages

| Tool | Purpose |
|------|--------|
| `get-all-languages` | List languages added to the instance |
| `get-available-languages` | List languages available to add |
| `get-language-by-id` | Get one language by ID |
| `add-language` | Add a language to the instance |
| `update-language` | Update a language |
| `delete-language-by-id` | Delete a language |

### Media

| Tool | Purpose |
|------|--------|
| `get-all-media` | List media library items |
| `get-media-by-id` | Get one media item by ID |
| `list-media-directories` | List the media folder tree |
| `create-media-directory` | Create a media folder |
| `request-upload-media-url` | Get a pre-signed **POST** URL (+ a `curl` example) for uploading a file |

### Pointer links

| Tool | Purpose |
|------|--------|
| `get-entry-pointer-link` | Resolve the internal pointer string for an entry, for rich-text `link` marks |
| `get-media-pointer-link` | Resolve the internal pointer string for a media item, for rich-text `link` marks |

### Trash

| Tool | Purpose |
|------|--------|
| `get-all-trash-items` | List trashed items |
| `get-trash-item-by-id` | Get one trashed item by ID |
| `get-trash-item-file-data` | Get the stored file data for a trashed item |

## Resources

The server also registers read-only MCP **resources** (served from `<app-host>/mcp-resources/*.md`). Load these for authoritative guidance before composing payloads:

| Resource | Purpose |
|----------|---------|
| `Entry` | Explains what a BCMS Entry is (status / meta / content) and embeds the live **Entry JSON schema** |
| `Important` | Operating note: if an MCP operation errors, do not silently fall back to the `@thebcms/client` SDK or CLI |
| `Update Instructions` | How to use `propChanges` when updating templates, groups, and widgets (one example per property type) |

## Entry payloads: meta, content, statuses

An entry has three parts:

- **statuses** — per-locale status assignments (`{ lng, id }`), where `id` is an entry-status ID.
- **meta** — structured, per-locale data whose shape is defined by the template (groups, widgets, pointers, localized fields).
- **content** — unstructured, per-locale rich text expressed as a **node tree**.

Each content (and rich-text prop) entry is an object:

```jsonc
{
  "lng": "en",          // language code; the language must exist in the instance
  "plainText": "",      // system-populated; send an empty string
  "nodes": [ /* content nodes */ ]
}
```

Follow each tool's input schema (and the `Entry` resource's embedded schema) as the source of truth.

### Rich-text node trees

Content `nodes` use a ProseMirror/Tiptap-style tree. The server accepts exactly these **node types**:

`paragraph`, `heading`, `text`, `bulletList`, `orderedList`, `listItem`, `codeBlock`, `hardBreak`, `horizontalRule`, `widget`, `media`.

Text **marks**: `bold`, `italic`, `underline`, `strike`, `inlineCode`, `link`.

Common `attrs` by node type:

- `heading` → `{ "level": 1-6 }`
- `orderedList` → `{ "start": 1 }`
- `listItem` → `{ "list": true }`
- `codeBlock` → `{ "language": "typescript", "code": "..." }`
- `media` → `{ "mediaId": "...", "altText": "...", "caption": "..." }`
- `widget` → `{ "data": { "_id": "<widgetId>", "props": [...] } }` (`propPath` / `readOnly` are system-managed; leave them empty)
- `link` mark → `{ "href": "...", "target": "_blank", "rel": "noopener noreferrer nofollow" }`

> There is **no** `image` or `blockquote` node type — embed media with the **`media`** node, and use `heading`/`paragraph` for callouts.

### Internal links in rich text

For `link` marks, the `href` must use a BCMS pointer string rather than a `/slug` path. Resolve them with the pointer-link tools instead of hand-building them:

- **Entry**: `get-entry-pointer-link` returns `entry:<entryId>@*_<templateId>:entry`.
- **Media**: `get-media-pointer-link` returns the internal media pointer string.
- **External** destinations use normal `https://...` or `mailto:...` targets.

### Minimal node shapes (illustrative)

```json
{
  "type": "paragraph",
  "content": [{ "type": "text", "text": "Hello" }]
}
```

```json
{
  "type": "heading",
  "attrs": { "level": 2 },
  "content": [{ "type": "text", "text": "Section title" }]
}
```

```json
{
  "type": "text",
  "text": "Read the guide",
  "marks": [{ "type": "link", "attrs": { "href": "entry:<entryId>@*_<templateId>:entry", "target": "_self" } }]
}
```

## Updating schema with `propChanges`

`update-template`, `update-group`, and `update-widget` accept a **`propChanges`** array to add, update, or remove properties. Each change names a property `type` (`STRING`, `NUMBER`, `BOOLEAN`, `DATE`, `ENUMERATION`, `ENTRY_POINTER`, `GROUP_POINTER`, `MEDIA`, `RICH_TEXT`) and a matching `data` block. Load the **Update Instructions** resource for one worked example per type. Example (add a string prop):

```json
{
  "propChanges": [
    {
      "label": "Subtitle",
      "type": "STRING",
      "required": false,
      "array": false,
      "data": { "propString": [] }
    }
  ]
}
```

## Recipes (agent workflows)

**Discover the instance**

1. `instance-get`, then `get-all-templates` (and `get-all-groups` / `get-all-widgets` if you need the schema).
2. For a template you want to edit, `get-all-entries-by-template-id` with its `templateId`.

**Create → publish pattern**

1. `list-entry-statuses` to find draft vs published status IDs (they are instance-specific).
2. `create-entries` with minimal valid `meta` (and a draft status per locale) while iterating.
3. `update-entries` with the published status ID for the relevant locale(s) when ready.

**New entry with title + slug**

1. Read the template's required `meta` props (`get-template-by-id`).
2. `create-entries` with minimal valid `meta` and a small or empty `content`, then `update-entries` to flesh out rich text.

**Rich text with an internal link**

1. `get-entry-pointer-link` (or `get-media-pointer-link`) for the target.
2. Add a `link` mark on a `text` node whose `attrs.href` is the returned pointer string.

**Upload media**

1. `request-upload-media-url` to get a pre-signed POST URL (and a `curl` example).
2. `POST` the file as `form-data` to that URL (optionally with `parentId` for a folder); the response contains the new media item.

**Remove content or schema**

- `delete-entries` (with `templateId` + `entryId`) removes an entry.
- `delete-template-by-id` / `delete-group-by-id` / `delete-widget-by-id` remove schema objects — inspect usage first, since deletes are destructive.

## Choosing MCP vs `@thebcms/client`

| Use MCP | Use SDK / REST |
|--------|----------------|
| Agent is editing content or schema from the IDE | Application runtime, SSR, builds |
| Exploratory listing and scripted content/schema updates | Batch jobs you own in TypeScript |
| Assistant has BCMS MCP tools enabled | Custom automation without MCP |

Both MCP and the SDK operate on the same instance; pick the surface that matches where the work runs.
