---
name: feishu-md2blocks
description: Insert rich Markdown content (including tables) into Feishu documents. Use when feishu_doc write/append fails with tables, or when inserting complex formatted content (tables, code blocks, nested lists) into an existing document at a specific position.
---

# Feishu Markdown to Blocks

Insert Markdown content—including tables—into Feishu documents via the block convert + descendant API.

## When to Use

- `feishu_doc` `write` replaces the entire document; use this to **insert** content at a position
- `feishu_doc` `create_table_with_values` has limitations for larger tables
- You need to insert tables, code blocks, or complex nested content into an existing doc

## Usage

```bash
# Insert from file (appends to document end)
python3 <skill_dir>/scripts/md2blocks.py <doc_token> content.md

# Insert from stdin
echo "| A | B |\n|---|---|\n| 1 | 2 |" | python3 <skill_dir>/scripts/md2blocks.py <doc_token> -

# Insert after a specific block
python3 <skill_dir>/scripts/md2blocks.py <doc_token> content.md --after <block_id>

# Replace all content
python3 <skill_dir>/scripts/md2blocks.py <doc_token> content.md --replace
```

## How It Works

1. Calls `POST /docx/v1/documents/blocks/convert` to convert Markdown → block structures
2. Removes `merge_info` from table blocks (read-only field that causes insertion errors)
3. Calls `POST /docx/v1/documents/{doc}/blocks/{parent}/descendant` to insert blocks

The descendant API handles nested structures (tables with cells containing text) that the simpler `/children` API cannot.

## Position Control

The `--after <block_id>` option inserts content right after the specified block. The script finds the block's index automatically.

**Key detail:** The `/descendant` API's `index` parameter **must be in the request body**, not as a URL query parameter. Passing `?index=N` in the URL is silently ignored (content appends to end). The script handles this correctly.

## Supported Markdown

Text, headings (h1-h9), bullet lists, ordered lists, code blocks, quotes, tables, todo items, dividers.

## Limitations

- Images in Markdown are not automatically uploaded; they require separate upload + patch steps
- Max 1000 blocks per insert call; split large documents if needed
- Requires `docx:document.block:convert` permission on the Feishu app
- Document edit rate limit: 3 ops/sec per document

## Reference

For complete block-level API reference, see the **feishu-block-ops** skill which covers:
- All block APIs (create/read/update/delete/batch)
- Block type reference, text element types
- Table operation patterns (batch edit, merge cells)
- Common patterns and gotchas
