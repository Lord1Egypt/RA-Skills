# Memo Capture

## Trigger

User explicitly requests to record a note, idea, or memo.
Keywords: "memo", "note", "capture", "jot down", "记录", "笔记", "想法".

## Workflow

1. Parse user input into memo content (markdown supported).
2. Auto-extract tags from content (pattern: `#TagName`).
3. Determine visibility:
   - Default: PRIVATE
   - User can override to PROTECTED or PUBLIC.
4. Show user a preview of the memo content. Get confirmation.
5. Call `memos_create_memo(content=..., visibility=...)`.
6. Return the memo name (`memos/{uid}`) for reference.

## Content Routing (Daily Log Integration)

When memo capture is invoked during a daily-log flow:

1. Create the memo first via `memos_create_memo`.
2. Receive `memos/{uid}` from the response.
3. Append a reference line to the daily log:
   `* <one-line summary>, see memos/{uid}`

This keeps daily logs concise while preserving detailed context in memos.

## Attachments

MCP does not support file upload (protocol limitation).

When the user wants to attach images or files:

1. Create the text memo via MCP first. Note the returned `memos/{uid}`.
2. Provide the Memos web UI URL: `{site_url}/m/{uid}`
   (read `site_url` from `~/.config/fragments.json`).
3. Instruct the user to open that URL in a browser and upload
   attachments there using the Memos web interface.

## Dedup Before Create

Before creating a new memo, run a quick search to avoid duplicates:

1. Call `memos_search_memos(query=<key_phrases_from_content>)`.
2. If a highly similar memo exists, show it to the user and ask:
   - Update the existing memo?
   - Create a new one anyway?
3. If no match, proceed with creation.

---

# Memo Lifecycle {#lifecycle}

## Update Workflow

Update an existing memo's content, visibility, or pin state.

### Trigger

User requests to modify, edit, or update a memo.
Keywords: "update memo", "edit memo", "修改 memo", "更新".

### Steps

1. **Locate the memo:**
   - If user provides memo ID/name: `memos_get_memo(name=...)`
   - If user describes content: `memos_search_memos(query=...)`
   - Show the matching memo(s) for confirmation.

2. **Display current content:**
   - Show the full memo content to the user.
   - Highlight what will change.

3. **Gather changes:**
   - `content`: Updated markdown text (optional)
   - `visibility`: PRIVATE | PROTECTED | PUBLIC (optional)
   - `pinned`: true | false (optional)
   - `state`: NORMAL | ARCHIVED (optional)

4. **User confirmation:**
   - Show a diff or summary of changes.
   - Wait for explicit approval (e.g., "yes", "确认", "update it").

5. **Execute:**
   ```python
   memos_update_memo(
       name="memos/{uid}",
       content=...,      # optional
       visibility=...,   # optional
       pinned=...,       # optional
       state=...         # optional
   )
   ```

6. **Report result:**
   - Return the updated memo name.
   - Confirm which fields were modified.

### Example

```
User: "Update my memo about API design to add authentication section"

1. Search: memos_search_memos(query="API design")
2. Found: memos/abc123 "API Design Guidelines"
3. Show current content
4. User confirms the addition
5. Call memos_update_memo(name="memos/abc123", content="...")
6. Confirm: "Updated memos/abc123 with authentication section"
```

## Delete Workflow

Permanently remove a memo. This operation is irreversible.

### Trigger

User requests to delete or remove a memo.
Keywords: "delete memo", "remove memo", "删除 memo".

### Steps

1. **Locate the memo:**
   - Same as update workflow — search or direct lookup.

2. **Display full content:**
   - Show the complete memo content.
   - Warn: "This action cannot be undone."

3. **Explicit confirmation:**
   - Ask user to confirm with memo ID: "Type 'delete memos/{uid}' to confirm"
   - Do NOT proceed without exact confirmation.

4. **Execute:**
   ```python
   memos_delete_memo(name="memos/{uid}")
   ```

5. **Report result:**
   - Confirm deletion with the memo's former title/ID.

### Safety Checks

- Always show full content before deletion.
- Require explicit confirmation with memo ID.
- If memo has comments, warn: "This memo has N comments which will also be deleted."

## Archive Alternative

For memos that might be needed later, suggest archiving instead of deleting:

```python
memos_update_memo(name="memos/{uid}", state="ARCHIVED")
```

Archived memos are hidden from default searches but remain accessible.
