# Daily Log

## Overview

One structured log per user per day. The Memos server enforces this constraint.
`memos_save_daily_log` performs a full replacement — always send the complete
content (existing + new lines).

## .plan Format Rules

Every non-empty line must start with one of these prefixes followed by a space:

| Prefix | Meaning |
|--------|---------|
| `* ` | Done / completed |
| `+ ` | To-do / planned |
| `- ` | Note / observation |
| `? ` | Open question |

Constraints:
- No leading whitespace or tabs (no indentation).
- No `====` day separators.
- Empty lines are allowed.

These rules are validated server-side. Malformed content will be rejected.

## Editability

Only today's log is editable (36-hour window from creation). Past logs are immutable.
Visibility is always PROTECTED (workspace-visible).

## Hook Trigger Workflow

When the passive hook fires (Claude Code `Stop` / OpenCode `session.idle`):

### 1. Assess Relevance

Skip if the session was trivial (greetings, simple questions, no tool use).
Indicators of meaningful work: file edits, bash commands, git operations,
code generation, debugging sessions.

### 2. Fetch Today's Log

Call `memos_get_daily_log(date=YYYY-MM-DD)` where date is today in local time.

- If a log exists → parse existing lines.
- If no log exists → start with empty content.

### 3. Format New Entries

Summarize this session's work as `.plan` lines:
- Completed tasks → `* ` prefix
- Identified next steps → `+ ` prefix
- Observations or context → `- ` prefix
- Unresolved issues → `? ` prefix

### 4. Diff Against Existing

Compare new entries against existing lines (semantic comparison, not exact string match).
If all new entries are already covered by existing content → skip, do not prompt user.

### 5. Content Routing

For each new entry, assess length and structure:
- Short, structured (fits one `.plan` line) → include directly.
- Long-form or detailed (multiple paragraphs, code blocks) →
  suggest creating a memo via `memos_create_memo` first.
  Then reference in daily log as: `* <one-line summary>, see memos/{uid}`

### 6. User Confirmation

Show the user the full merged log (all existing lines + new lines).
Clearly mark which lines are new. Wait for explicit confirmation.

### 7. Save

Call `memos_save_daily_log(date=today, content=full_content)`.
Remember: this is a full replacement. Include every line.

## Active Trigger

When user explicitly asks to record daily log, follow steps 2-7 above.
Skip step 1 (relevance assessment) since the user's intent is explicit.
