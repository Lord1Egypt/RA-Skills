# Csv To Task

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Converts CSV rows into structured, trackable task objects — Jira tickets, Markdown checklists, or JSON arrays

## What Problem This Solves

User has a spreadsheet or CSV export and needs to turn each row into a task they can actually track — assign, prioritize, set due dates. This skill maps CSV columns to task fields (title, assignee, priority, due date) and outputs in the format they need.

**When triggered:** CSV data + task/todo/ticket creation intent.

## Features

- **Automatic field mapping** — detects column names and maps them to task attributes (title from first text col, assignee from name col, priority from P0-P3 or H/M/L)
- **Multi-format output** — Markdown checklist, Jira-style tickets, JSON array, or CSV with new columns
- **Handles incomplete data** — marks missing assignees as "unassigned", missing priority as "normal"
- **Preserves all original data** — every row becomes exactly one task, no silent drops

## Quick Start

```bash
# Via ClawHub
clawhub install csv-to-task

# Or manually
cp -r csv-to-task ~/.openclaw/skills/
```

### Usage

```
/csv-to-task
```

Paste CSV and ask "convert to tasks" — specify format (Jira, Markdown, JSON).

```
/csv-to-task/estimate
```

Adds time or complexity estimates to each task for sprint planning.

## Modes

| Mode | Description |
|------|-------------|
| `/csv-to-task` | Default — converts CSV rows to task objects in specified format |
| `/csv-to-task/estimate` | Adds time/complexity estimates to each task |

## Examples

| Scenario | Output |
|----------|--------|
| 10 rows, no status column | All tasks marked "todo" with note "no status column found" |
| Priority in P0-P3 format | Correctly mapped to task priority |
| Title column 200 chars | Full title kept, summarized in description field |
| 3 rows with no assignee | "unassigned" for each, no invented names |

## Directory Structure

```
csv-to-task/
├── SKILL.md          # Entry point
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Field mapping templates, format examples
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).