---
name: aight-utils
version: 1.0.0
description: Native Aight app integration for creating reminders, tasks, triggers, and items. Use when user mentions deadlines, reminders, tasks, or tracking.
author: alex
---

# Aight Utils

**Native integration with the Aight iOS app.**

Creates reminders, tasks, and tracked items that appear in the user's Aight Today view.

## When to Use

| User Says | Create Type | Example |
|-----------|-------------|---------|
| "Remind me to..." | `trigger` | `scheduledFor: ISO 8601` |
| "Don't forget..." | `trigger` | `scheduledFor: ISO 8601` |
| "Add this to my tasks" | `item` | `labels: ["category"]` |
| "Deadline is..." | `trigger` | `type: "deadline"` |
| "Track this PR/issue" | `item` | `url: "<link>"` |
| "Done" / "Cancel" | Update status | `status: "done"/"cancelled"` |

## Item Types

| Type | Use For | Key Fields |
|------|---------|------------|
| `trigger` | Time-based, fire-once | `scheduledFor` (ISO 8601) |
| `item` | Stateful, lifecycle | `labels`, `status` |
| `process` | Background work | `sessionTarget`, `label` |

## Usage Examples

### Create a Reminder

```json
{
  "id": "remind-dentist-1711123200",
  "type": "trigger",
  "text": "Call dentist to schedule appointment",
  "scheduledFor": "2026-03-23T14:00:00+08:00",
  "labels": ["health", "personal"]
}
```

### Create a Task

```json
{
  "id": "task-bp-draft-1711123200",
  "type": "item",
  "text": "Draft Q2 funding BP",
  "labels": ["work", "fundraising"],
  "status": "active"
}
```

### Create a Deadline

```json
{
  "id": "deadline-tax-1711123200",
  "type": "trigger",
  "text": "File tax return",
  "scheduledFor": "2026-04-15T23:59:59+08:00",
  "type": "deadline",
  "labels": ["finance", "urgent"]
}
```

### Track a PR

```json
{
  "id": "pr-openclaw-123-1711123200",
  "type": "item",
  "text": "Review OpenClaw PR #123",
  "url": "https://github.com/openclaw/openclaw/pull/123",
  "labels": ["code-review"],
  "status": "active"
}
```

### Mark Complete

```json
{
  "id": "task-bp-draft-1711123200",
  "status": "done"
}
```

## ID Generation Rules

- Format: `<type>-<slug>-<timestamp>`
- Slug: kebab-case, 2-4 words describing the item
- Timestamp: Unix epoch or short hash for uniqueness

**Examples:**
- `remind-groceries-1711123200`
- `task-bp-draft-1711123200`
- `deadline-tax-2026q1`
- `pr-openclaw-123`

## Labels Convention

Use consistent labels for categorization:

| Category | Labels |
|----------|--------|
| Work | `work`, `meeting`, `code-review`, `fundraising` |
| Personal | `personal`, `health`, `family` |
| Finance | `finance`, `tax`, `billing` |
| Urgency | `urgent`, `high-priority` |

## Date Parsing

Parse natural language dates to ISO 8601:

| User Input | ISO 8601 |
|------------|----------|
| "tomorrow at 2pm" | `2026-03-23T14:00:00+08:00` |
| "next Friday" | `2026-03-27T09:00:00+08:00` |
| "end of day" | `2026-03-22T23:59:59+08:00` |
| "in 2 hours" | `2026-03-22T17:30:00+08:00` |

**Current time:** 2026-03-22 23:45 GMT+8 (Asia/Shanghai)

## Rules

1. **Always generate unique IDs** — use slug + timestamp
2. **Parse dates before calling** — convert natural language to ISO 8601
3. **Set labels for categorization** — helps user filter in Today view
4. **Default status is "active"** — don't set unless changing
5. **For reminders:** always use `type: "trigger"` with `scheduledFor`
6. **For tasks:** use `type: "item"` with `labels`
7. **For completions:** update existing item with `status: "done"`

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `proactive-agent` | Outcome tracking → create deadline triggers |
| `memory-manager` | Important events → create reminder triggers |
| `watchdog` | Task completion → update item status |

## Error Handling

If item creation fails:
1. Log to `.learnings/ERRORS.md`
2. Inform user: "Couldn't create reminder — adding to memory instead"
3. Create fallback in `memory/YYYY-MM-DD.md`

---

**Version:** 1.0.0  
**Author:** alex  
**Last Updated:** 2026-03-22
