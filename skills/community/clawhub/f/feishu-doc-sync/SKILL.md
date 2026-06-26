---
name: feishu-doc-sync
description: |
  飞书文档增量同步与表格操作指南。覆盖：表格更新策略（delete+insert）、header_row 设置、insert action、列宽算法、三阶段 diff 同步。当需要同步本地文档到飞书、操作飞书表格、或做增量编辑时激活。
---

# Feishu Document Tool

Single tool `feishu_doc` with action parameter for all document operations, including table creation for Docx.

## Token Extraction

From URL `https://xxx.feishu.cn/docx/ABC123def` → `doc_token` = `ABC123def`

## Actions

### Read Document

```json
{ "action": "read", "doc_token": "ABC123def" }
```

Returns: title, plain text content, block statistics. Check `hint` field — if present, structured content (tables, images) exists that requires `list_blocks`.

### Write Document (Replace All)

```json
{ "action": "write", "doc_token": "ABC123def", "content": "# Title\n\nMarkdown content..." }
```

Replaces entire document with markdown content. Supports: headings, lists, code blocks, quotes, links, images (`![](url)` auto-uploaded), bold/italic/strikethrough, **and Markdown tables**.

### Append Content

```json
{ "action": "append", "doc_token": "ABC123def", "content": "Additional content" }
```

Appends markdown to end of document. Supports the same content types as `write`, including Markdown tables.

### Insert Content (Positioned)

```json
{
  "action": "insert",
  "doc_token": "ABC123def",
  "after_block_id": "doxcnXXX",
  "content": "Markdown content including tables..."
}
```

Inserts content after a specific block. Uses Descendant API internally, supports all block types including tables.

**Key usage:** This is the primary way to insert content at a precise position. Use `list_blocks` first to find the `after_block_id`.

### Create Document

```json
{ "action": "create", "title": "New Document", "owner_open_id": "ou_xxx" }
```

With folder:

```json
{
  "action": "create",
  "title": "New Document",
  "folder_token": "fldcnXXX",
  "owner_open_id": "ou_xxx"
}
```

**Important:** Always pass `owner_open_id` with the requesting user's `open_id` (from inbound metadata `sender_id`) so the user automatically gets `full_access` permission on the created document. Without this, only the bot app has access.

### List Blocks

```json
{ "action": "list_blocks", "doc_token": "ABC123def" }
```

Returns full block data including tables, images. Use this to read structured content and find block IDs for positioning.

### Get Single Block

```json
{ "action": "get_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

### Update Block Text

```json
{
  "action": "update_block",
  "doc_token": "ABC123def",
  "block_id": "doxcnXXX",
  "content": "New text with **bold** and `code`"
}
```

Supports Markdown inline styles: `**bold**`, `` `code` ``, `[link](url)`, `~~strike~~`.

**Supported block types:** Text, Heading, Bullet, Ordered, Code, Quote, Todo.

**⚠️ NOT for tables:** Using `update_block` on a table cell replaces content as plain text, destroying all inline formatting (inline_code, bold, etc.).

### Delete Block

```json
{ "action": "delete_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

### Create Table

```json
{
  "action": "create_table",
  "doc_token": "ABC123def",
  "row_size": 2,
  "column_size": 2,
  "column_width": [200, 200]
}
```

**⚠️ Positioning unreliable:** `parent_block_id` and `index` parameters do not work correctly for tables — tables always end up at the document end. Use `insert` action with `after_block_id` instead for positioned tables.

### Write Table Cells

```json
{
  "action": "write_table_cells",
  "doc_token": "ABC123def",
  "table_block_id": "doxcnTABLE",
  "values": [
    ["A1", "B1"],
    ["A2", "B2"]
  ]
}
```

Writes plain text into table cells. Supports Markdown inline styles in cell values.

**Note:** This clears and rebuilds cell children. Suitable for initial table filling or full-cell replacement, but not for partial cell edits.

### Create Table With Values (One-step)

```json
{
  "action": "create_table_with_values",
  "doc_token": "ABC123def",
  "row_size": 2,
  "column_size": 2,
  "column_width": [200, 200],
  "values": [["A1", "B1"], ["A2", "B2"]]
}
```

**⚠️ Same positioning caveat as `create_table`** — use `insert` action for positioned tables.

### Table Row/Column Operations

```json
{ "action": "insert_table_row", "doc_token": "...", "table_block_id": "...", "row_index": -1 }
{ "action": "insert_table_column", "doc_token": "...", "table_block_id": "...", "column_index": -1 }
{ "action": "delete_table_rows", "doc_token": "...", "block_id": "...", "row_start": 1, "row_count": 1 }
{ "action": "delete_table_columns", "doc_token": "...", "block_id": "...", "column_start": 0, "column_count": 1 }
{ "action": "merge_table_cells", "doc_token": "...", "table_block_id": "...", "row_start": 0, "row_end": 2, "column_start": 0, "column_end": 2 }
```

**Note for `delete_table_rows`:** Uses `block_id` (not `table_block_id`), `row_start` (not `row_index`).

### Upload Image

```json
{ "action": "upload_image", "doc_token": "ABC123def", "url": "https://example.com/image.png" }
```

Or local path with position control:

```json
{
  "action": "upload_image",
  "doc_token": "ABC123def",
  "file_path": "/tmp/image.png",
  "parent_block_id": "doxcnParent",
  "index": 5
}
```

Or base64 data URI:

```json
{
  "action": "upload_image",
  "doc_token": "ABC123def",
  "image": "data:image/png;base64,iVBOR..."
}
```

**Note:** Image display size is determined by the uploaded image's pixel dimensions. For small images (e.g. 480x270), scale to 800px+ width before uploading.

### Upload File Attachment

```json
{ "action": "upload_file", "doc_token": "ABC123def", "url": "https://example.com/report.pdf" }
```

Or local path:

```json
{ "action": "upload_file", "doc_token": "ABC123def", "file_path": "/tmp/report.pdf", "filename": "Q1-report.pdf" }
```

### Color Text

```json
{
  "action": "color_text",
  "doc_token": "ABC123def",
  "block_id": "doxcnXXX",
  "content": "colored text",
  "color": "red"
}
```

## Reading Workflow

1. Start with `action: "read"` — get plain text + statistics
2. Check `block_types` in response for Table, Image, Code, etc.
3. If structured content exists, use `action: "list_blocks"` for full data

---

## Incremental Sync Best Practices

### When to Use Incremental vs Full Sync

- **< 5 blocks changed** → incremental (delete + insert individual blocks)
- **> 80% blocks changed** → full sync (`write` action to replace all)
- **Single table changed** → delete old table + insert new table

### Table Update Strategy: Delete + Insert

Tables should NEVER be edited in-place. Always:

```
1. list_blocks → find the block before the table (anchor_block_id)
2. delete_block(block_id = old_table_id)
3. insert(after_block_id = anchor_block_id, content = "| new | table |...")
```

**Why not edit in-place?**
- `update_block` on table cell → strips inline formatting (inline_code, bold, links all become plain text)
- `write_table_cells` → clears and rebuilds cell children, similar formatting loss
- `create_table` / `create_table_with_values` → positioning unreliable

### Multi-Block Batch Replacement

When changes span multiple consecutive blocks:

1. Find anchor (last unchanged block before the changed region)
2. Delete changed blocks in **reverse order** (to avoid index drift)
3. Single `insert` call with all new content (supports mixed block types)

### Diff Strategy (from feishu-doc-sync)

1. Block signature matching — (type, content) hash for alignment, style hash for change detection
2. LCS alignment of local ↔ remote blocks
3. Three-phase execution: **UPDATE** (text blocks) → **DELETE** (reverse order) → **INSERT** (forward order)
4. Tables: if structure is identical, cell-level diff is possible; if structure differs, full table replacement
5. When change rate > 80%, fall back to full sync

---

## Table Header Row (Dark Background)

The `header_row: true` property gives tables a dark header background. This is a common requirement.

### ⚠️ Critical: `header_row` can ONLY be set at creation time

**The PATCH API (`update_table_property`) does NOT work for `header_row`** — it returns `code: 0` (success) but silently fails to apply the property. This applies to both single-block PATCH and `batch_update`.

### How to Create Tables with Header Row

Since `insert` action (Descendant API) and `create_table` action do not support `header_row`, you must use the raw Feishu API:

```bash
# Step 1: Get tenant_access_token
TOKEN=$(curl -s https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"'$APP_ID'","app_secret":"'$APP_SECRET'"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# Step 2: Create empty table with header_row via document_block_children.create
curl -s -X POST \
  "https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children?document_revision_id=-1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [{
      "block_type": 31,
      "table": {
        "property": {
          "row_size": 3,
          "column_size": 2,
          "header_row": true,
          "column_width": [300, 400]
        }
      }
    }],
    "index": 5
  }'

# Step 3: Fill cells via feishu_doc write_table_cells
# (use the new table's block_id from step 2 response)
```

**Credentials:** Read from `/root/.openclaw/openclaw.json` → `channels.feishu.appId` / `channels.feishu.appSecret`.

### Workflow for Positioned Table with Header Row

1. `list_blocks` → find the anchor block and target index
2. (If replacing) `delete_block` → remove old table
3. Raw API `document_block_children.create` → create empty table with `header_row: true` at correct index
4. `feishu_doc write_table_cells` → fill content
5. Verify: `get_block` → check `table.property.header_row`

### Column Width Algorithm

Auto-calculated when using `insert` action (Descendant API):
- Total width: ~730px
- CJK characters count as 2x width
- Per-column: proportional distribution, clamped to 50–400px
- When using raw API, specify `column_width` manually

---

## Sync Prerequisites

- **Always `git pull` before reading local repo files** — ensures latest content
- **Compare before writing** — use `read` or `list_blocks` to check current state
- **Preserve formatting** — inline_code, bold, links in table cells require careful handling

## Configuration

```yaml
channels:
  feishu:
    tools:
      doc: true  # default: true
```

**Note:** `feishu_wiki` depends on this tool — wiki page content is read/written via `feishu_doc`.

## Permissions

Required: `docx:document`, `docx:document:readonly`, `docx:document.block:convert`, `drive:drive`
