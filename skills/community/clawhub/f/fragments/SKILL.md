---
name: fragments
version: 1.0.0
description: >
  Fragmented work logging and idea capture powered by Memos.
  Full memo lifecycle: create, search, update, delete, and comment.
  Daily-log: structured work journal in .plan format.
  Passive trigger: after agent completes a task, prompt user to record.
  Active trigger: user says "memo", "note", "capture", "daily log",
  "fragments", "记录", "笔记", "日志", "想法", "评论", "comment",
  "更新 memo", "删除 memo".
---

# Fragments

## Setup Check

1. Read `~/.config/fragments.json` (Windows: `%USERPROFILE%\.config\fragments.json`).
2. If file missing → first install. Detect current platform, read the matching setup guide:
   - Claude Code → `references/setup-claude-code.md`
   - OpenCode → `references/setup-opencode.md`
   - OpenClaw → `references/setup-openclaw.md`
3. If file exists → verify MCP is configured. If incomplete → read the matching setup guide.
4. All good → proceed to normal usage.

## Platform Detection

Detect the current platform by checking for platform-specific markers:

| Platform | Detection Marker |
|----------|------------------|
| Claude Code | `~/.claude/` directory exists |
| OpenCode | `~/.config/opencode/` directory exists |
| OpenClaw | `~/.openclaw/` directory exists |

## Modes

### memo — Full Lifecycle Management

Create, search, update, delete, and comment on memos via MCP tools.

**Workflows:**
- Create & dedup → `references/memo-capture.md`
- Update & delete → `references/memo-capture.md#lifecycle`
- Comments → `references/memo-comments.md`

Write operations require user confirmation before calling.

### daily-log — Daily Work Journal

One structured log per user per day. Content follows `.plan` format
enforced by the Memos server.

Format rules, diff-merge logic, and hook trigger workflow:
→ `references/daily-log.md`

### search — Semantic Search

Server-side full-text retrieval via MCP, optional client-side
TF-IDF + LSA rerank for semantic/fuzzy queries.

Pipeline details and tuning parameters:
→ `references/search-strategy.md`

## Retrieval Strategy

Data volume can be large. Always prefer targeted retrieval over bulk listing.

### Memos

1. **Search first**: `memos_search_memos(query=...)` — use when the user has
   any intent, keyword, or topic. Returns bounded results.
2. **Get by ID**: `memos_get_memo(name=...)` — use when you already know the
   memo name. Expand full content only for shortlisted results.
3. **List as fallback**: `memos_list_memos(page_size=10)` — use only for
   explicit "show recent" requests. Always set a small `page_size`.
4. **Client-side rerank**: pipe search results through `scripts/fragments_search.py`
   for semantic ranking when server-side results need refinement.

### Comments

- **List comments**: `memos_list_memo_comments(name=...)` — retrieve all comments
  on a memo. Comments inherit the parent memo's visibility.

### Daily Logs

1. **Get by date**: `memos_get_daily_log(date=YYYY-MM-DD)` — single log lookup.
   Pass `creator="users/{id}"` to view another user's log (PROTECTED visibility).
2. **List with date range**: `memos_list_daily_logs(start_date, end_date, page_size=10)`
   — use only for explicit "show this week/month" requests. Always bound the range.

### Tags

- `memos_list_tags` — lightweight, use to discover available tags for filtering.

No read operations require user confirmation.

## Write Operations

All write operations require explicit user confirmation before calling.
Read operations need no confirmation. Never echo PAT tokens to the conversation.

### Memo Writes

| Operation | MCP Tool | When to Use |
|-----------|----------|-------------|
| Create | `memos_create_memo` | New idea, note, snippet |
| Update | `memos_update_memo` | Modify content, visibility, pin |
| Delete | `memos_delete_memo` | Remove memo (irreversible) |
| Add comment | `memos_create_memo_comment` | Append discussion to memo |

### Daily Log Writes

- `memos_save_daily_log(date=..., content=...)` — full replacement save.
  Always include complete content (existing + new lines).

## Hook Workflow (Passive Trigger)

When triggered by agent task completion:

1. Assess whether this session performed meaningful work. Skip if trivial.
2. Call `memos_get_daily_log` for today's date.
3. Format new entries in `.plan` style.
4. Diff against existing content. Skip if no new information.
5. Long-form content → suggest creating a memo first, reference in daily log.
6. Show user the full merged log (existing + new). Wait for confirmation.
7. Call `memos_save_daily_log` with complete content (full replacement).
