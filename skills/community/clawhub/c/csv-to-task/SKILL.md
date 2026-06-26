---
name: csv-to-task
description: >
  Use when (1) user pastes CSV data and wants to convert each row into an actionable task, ticket, or to-do item. 
  (2) user says "convert these to tasks", "create tasks from this list", or "turn this spreadsheet into a todo list". 
  (3) user provides a project roster, backlog, or table and asks to "make it a task list". 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# CSV to Task

Use when (1) user pastes CSV data and wants to convert each row into an actionable task, ticket, or to-do item. (2) user says "convert these to tasks", "create tasks from this list", or "turn this spreadsheet into a todo list". (3) user provides a project roster, backlog, or table and asks to "make it a task list".

## Core Position

This skill solves the specific problem of: *rows of tabular data need to become individual, trackable task units.*

This skill IS NOT:
- A data analysis tool — it produces tasks, not insights
- A reminder/calendar tool — tasks can be for any system (Jira, Linear, Notion, plain text)
- Activated by general "make a list" requests without structured data

This skill IS activated ONLY when: structured tabular/CSV data + task creation intent are both present.

## Modes

### `/csv-to-task`

**Default mode.** Converts CSV rows to structured task objects with status, assignee, priority, and due date.

When to use: User provides CSV and wants task objects (Jira format, Markdown checklist, etc.)

### `/csv-to-task/estimate`

Adds time or complexity estimates to each task based on column data.

When to use: User wants to go beyond raw conversion and add sprint planning data.

## Execution Steps

### Step 1 — Parse the CSV

1. Receive CSV input (pasted text, file, or path)
2. Detect header row — columns become task field names
3. Identify key task fields:
   - **Title/Name** (required): usually first string column or explicitly labeled
   - **Assignee** (optional): person responsible
   - **Priority** (optional): high/medium/low, P0-P3, or numeric
   - **Due date** (optional): ISO date, MM/DD, or relative ("next Friday")
   - **Status** (optional): todo/done/in-progress or explicit column
   - **Description** (optional): longer text fields
4. If no clear title column exists, ask the user which column to use as task name

### Step 2 — Map to Task Structure

Map each row to a task object. Default fields:

| CSV Column | Task Field |
|---|---|
| Any text column (title-like) | `title` |
| Person name/email column | `assignee` |
| H/M/L or P0-P3 | `priority` |
| Date column | `dueDate` |
| Category/tag column | `labels` |
| Long text column | `description` |

Unmapped columns → attach as key-value metadata.

### Step 3 — Format Output

Choose format based on user intent or explicit request:

- **Markdown checklist**: `- [ ] Task title @assignee #priority`
- **Jira-style**: `PROJECT-123: Task title [labels] — assignee`
- **JSON array**: `[{"title": "...", "assignee": "...", ...}]`
- **CSV with new columns**: original CSV + added `status` and `taskId` columns

### Step 4 — Validate

- No rows silently dropped — count input rows vs. output tasks
- Title field is populated for every task
- Date formats are consistent and valid

## Mandatory Rules

### Do not

- Do not invent assignee names not in the data
- Do not set due dates arbitrarily — use column data or ask
- Do not merge or split rows without explicit instruction
- Do not use task status "done" unless user confirms completion

### Do

- Respect column-to-field mappings from the data
- Preserve all original CSV data as task metadata
- Handle empty cells explicitly (mark as "unassigned", "none")
- Output a consistent format for all rows

## Quality Bar

**A good output:**
- Every row becomes exactly one task with a title
- Field mapping is explicit and traceable to source columns
- All original data is preserved (no silent drop)
- Output format is valid and runnable/parseable

**A bad output:**
- Merges multiple rows into one task
- Drops rows with missing fields
- Produces plain text without structure (not parseable)
- Invents data not present in the CSV

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| 10 rows, no status column | All marked "done" by default | All marked "todo" with note "no status column found" |
| Missing assignee | "Assignee: John" (random) | "Assignee: unassigned" |
| Priority in P0-P3 format | Ignored | Mapped correctly to P0/P1/P2/P3 |
| Title column has 200 chars | Truncated to 50 | Kept full, summarized in description |

## References

- `references/` — Field mapping templates, output format examples for Jira/Label/Notion/Linear