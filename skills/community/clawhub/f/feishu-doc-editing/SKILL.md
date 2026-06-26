---
name: feishu-doc-editing
description: |
  Performance-optimized strategies for editing Feishu (Lark) documents via OpenClaw's feishu_doc tool.
  Use when: (1) modifying existing Feishu documents, (2) inserting images at specific positions,
  (3) writing tables or structured content, (4) any multi-block document editing task,
  (5) writing long documents that may hit API size limits.
  Provides concrete patterns to minimize API calls and maximize editing speed while preserving
  existing formatting. Covers: parallel operations, positioned image insertion, large document
  chunking, rate-limit handling, rich-text preservation, and conflict avoidance.
  Complements the built-in feishu-doc skill (API reference) with operational best practices.
---

# Feishu Document Editing — Performance Best Practices

## Core Principle: Minimum Change

Never use `write` (full document replace) for partial edits — it destroys existing rich-text formatting (colors, highlights, inline styles). Always use targeted block-level operations.

> Full decision tree (when to use update_block vs delete+insert vs append, with protection mechanisms) is in `~/self-improving/domains/feishu.md` under "最小改动原则".

## Strategy 1: Scan Once, Act in Parallel

**Pattern:** One `list_blocks` → plan all changes → fire independent operations together.

```
1. feishu_doc(action: "list_blocks", doc_token: "xxx")
   → Full block tree with IDs, types, content

2. Identify which blocks need update/delete/insert

3. Issue all independent operations in one tool-call batch:
   - update_block(block_id: "A", content: "new text")
   - update_block(block_id: "B", content: "new text")
   - delete_block(block_id: "C")
   - insert(after_block_id: "D", content: "...")
```

**Why:** `update_block` on different blocks has zero dependency. OpenClaw executes independent tool calls within a single response concurrently (other AI frameworks may vary — verify before assuming).

**Result:** 10 serial updates (3–5 s) → 10 concurrent updates (~0.3–1 s).

**Cache the block tree:** Reuse `list_blocks` throughout the session. Re-fetch only after inserts/deletes that shift the structure.

## Strategy 2: Back-to-Front for Insert/Delete

When mixing `insert` and `delete`, operate from the document's end toward the beginning.

**Why:** Inserting or deleting a block shifts indices of all subsequent siblings. Back-to-front keeps earlier indices stable — no need to re-query after each op.

**Example:** Delete blocks at indices 5, 12, 20 → delete 20 first, then 12, then 5.

## Strategy 3: Merge Adjacent Inserts

Combine consecutive inserts into one call:

```json
{
  "action": "insert",
  "doc_token": "xxx",
  "after_block_id": "target_block",
  "content": "## New Section\n\nParagraph one.\n\nParagraph two.\n\n![caption](https://image-url.png)"
}
```

Images as `![alt](url)` inside `insert`/`append` are auto-positioned inline — no separate `upload_image` needed when the URL is public.

## Strategy 4: Positioned Image Insertion

| Method | When to use |
|--------|------------|
| `insert` with `![](url)` markdown | Public URL, image goes with surrounding text |
| `upload_image` + `parent_block_id` + `index` | Local file / base64, precise position needed |

**upload_image with position:**

```json
{
  "action": "upload_image",
  "doc_token": "xxx",
  "file_path": "/tmp/chart.png",
  "parent_block_id": "doc_root_or_parent_id",
  "index": 5
}
```

**Finding the index:** From `list_blocks`, locate the target in its parent's `children` array. Use that index to insert before, or index+1 to insert after.

## Strategy 5: Table Performance

Docx tables are the slowest — each cell needs separate clear + convert + insert API calls.

- **Prefer Bitable** for data-heavy tables. Bitable has native batch record APIs.
- **Minimize cell count.**
- **New tables:** use `create_table_with_values` (one-step).
- **Existing tables:** update only changed cells, not the entire table.

## Strategy 6: Large Document Chunking

The Feishu `document.convert` API and `documentBlockChildren.create` have per-request size limits. For long content:

- **Chunk appends at 300–600 lines** (or ~3K chars) per call to avoid 400 errors.
- **Split at heading boundaries** (`#` or `##`) — keeps each chunk semantically coherent.
- Avoid splitting inside fenced code blocks.
- OpenClaw's `append`/`insert` auto-chunk internally, but feeding smaller pieces reduces conversion failures.

## Strategy 7: Rate-Limit & Retry

Feishu API returns `429` when request frequency is too high. Handle it:

- **Space concurrent calls** — if firing 10+ parallel operations, use a concurrency limit of ~5.
- **Exponential backoff on 429** — wait 1s, 2s, 4s before retrying. Max 3 retries.
- **Batch block creation** where possible — one request with multiple `children` beats N separate requests.

OpenClaw's built-in tool handles basic retries, but be aware when orchestrating many operations in rapid succession.

## Strategy 8: Rich-Text Preservation

`update_block` replaces the entire text element array — **all inline styles (bold, italic, color, links) are lost**. To preserve formatting:

- **Read the block first** via `get_block` to inspect existing `text_element_style` fields.
- **Only update blocks where the text actually changed** — skip unchanged blocks even if you're rewriting a section.
- **For style-only changes** (color, highlight), use `color_text` action instead of `update_block`.
- **When rich text must be preserved exactly**, consider `delete_block` + `insert` with markdown that re-expresses the formatting, rather than `update_block` which strips styles.

## Strategy 9: Conflict Avoidance

When multiple agents or users may edit the same document simultaneously:

- **Check `revision_id`** from `read` action before making changes. If the revision has advanced since your `list_blocks`, re-fetch before editing.
- **Minimize the edit window** — scan, plan, and execute in quick succession. Don't hold a stale block tree for minutes.
- **Prefer append for additive content** — appending to the end rarely conflicts with other editors working in the middle.
- **Avoid deleting blocks you didn't create** unless explicitly instructed.

## Anti-Patterns

| Don't | Do instead |
|-------|-----------|
| `write` to change a few paragraphs | `update_block` on specific blocks |
| Serial update_block one-by-one | Batch independent ops in one tool-call |
| `upload_image` without position params | Pass `parent_block_id` + `index`, or use `insert` with `![](url)` |
| Parallel `upload_image` with `after_block_id` to different positions | Serial: append text → upload_image → append text → upload_image (API ignores after_block_id in parallel) |
| Re-fetch `list_blocks` after every edit | Cache and reuse; re-fetch only after structural changes |
| Insert top-to-bottom when mixing insert/delete | Back-to-front to avoid index drift |
| Append 2000-line markdown in one call | Chunk at ~300–600 lines per append |
| Ignore 429 rate limits | Exponential backoff, limit concurrency to ~5 |
| `update_block` on formatted text blindly | Check existing styles; use `color_text` for style-only edits |

## Compatibility

- Works with OpenClaw's built-in `feishu_doc` tool — no code changes needed
- Complements `feishu-doc` skill (API reference) and `feishu-readability` skill (formatting rules)
- Applies to all Feishu accounts (球球星球 / 小米 / any tenant)
