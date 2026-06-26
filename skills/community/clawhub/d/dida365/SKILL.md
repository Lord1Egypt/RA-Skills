---
name: dida365
description: Use when the user wants to interact with TickTick/Dida365 (滴答清单) — managing tasks, projects, and to-dos, checking productivity stats, completing tasks, searching or filtering tasks, or asking about their task completion rate and achievement progress. Invoke this skill whenever the user mentions TickTick, Dida365, 滴答清单, their tasks, to-do lists, projects in TickTick, or anything about their task management workflow, even if they don't say "TickTick" explicitly.
---

# TickTick / Dida365 (滴答清单)

Task management via the `mcp__dida__*` MCP tools. Query, create, and update tasks across all projects — no app required.

**可用工具:** 查询任务、清单查询、任务管理

## 清单查询

| 工具 | 介绍 | 说明 |
|------|------|------|
| `list_projects` | 获取当前账号中的所有清单 | |
| `get_project_by_id` | 根据清单 ID 获取指定清单的详细信息 | |
| `get_project_with_undone_tasks` | 获取指定清单详情，同时返回该清单下所有未完成的任务 | |
| `get_task_in_project` | 获取指定清单中的某个特定任务 | |

## 查询任务

| 工具 | 介绍 | 说明 |
|------|------|------|
| `search_task` | 使用关键词搜索任务，返回任务 ID、标题和链接等 | |
| `get_task_by_id` | 根据任务 ID 获取任务的完整内容 | |
| `list_undone_tasks_by_time_query` | 查询一段时间的未完成任务，默认查询今天的未完成任务 | 支持选项：`today`, `last24hour`, `last7day`, `tomorrow`, `next24hour`, `next7day` |
| `list_undone_tasks_by_date` | 查询指定日期范围内的未完成任务 | 日期跨度最大 14 天 |
| `list_completed_tasks_by_date` | 查询指定清单中，在日期范围内的已完成的任务 | |
| `filter_tasks` | 按日期、清单、优先级、标签、类型、状态等多条件组合查询任务 | |

## 任务管理

| 工具 | 介绍 | 说明 |
|------|------|------|
| `create_task` | 创建任务，支持设置标题、描述、日期、优先级、清单、标签等属性 | |
| `batch_add_tasks` | 批量创建任务，并设置每个任务的各字段 | |
| `complete_task` | 完成指定任务 | |
| `complete_tasks_in_project` | 批量完成指定清单中的多个任务 | 每次最多 20 个 |
| `update_task` | 修改任务的标题、描述、日期、优先级等属性 | |
| `move_task` | 将任务移动到其他清单 | |
| `batch_update_tasks` | 批量修改多个任务的属性值 | |

## Common Workflows

### See what's on today's plate
```
mcp__dida__list_undone_tasks_by_time_query { queryCommand: "today" }
```

### Find a task by keyword
```
mcp__dida__search_task { query: "关键词" }
```

### Check productivity / completion rate

Dida365's achievement system tracks your completion rate as:
**completion rate = completed tasks ÷ originally scheduled tasks**

Achievement points increase when you finish tasks on time and decrease with procrastination. Points update daily at midnight. There are 12 achievement levels.

To compute your completion rate for a period:

1. Get completed tasks:
   ```
   mcp__dida__list_completed_tasks_by_date {
     completedTaskSearch: { projectIds: [], startDate: "2024-01-01", endDate: "2024-01-07" }
   }
   ```

2. Get undone tasks for the same range:
   ```
   mcp__dida__list_undone_tasks_by_date {
     undoneTaskSearch: { projectIds: [], startDate: "2024-01-01", endDate: "2024-01-07" }
   }
   ```

3. Compute: `completed / (completed + undone)` — this mirrors what Dida365 shows in the achievement panel.

### Create a task with a due date
```
mcp__dida__create_task {
  task: {
    title: "买咖啡",
    projectId: "<project-id>",
    dueDate: "2024-01-15T09:00:00+08:00",
    priority: 1,   // 0=none, 1=low, 3=medium, 5=high
    timeZone: "Asia/Shanghai",
    isAllDay: false,
    status: 0,
    ...
  }
}
```

> For required fields with no meaningful value, use: `assignor: ""`, `childIds: []`, `columnId: ""`, `columnName: ""`, `completedTime: ""`, `content: ""`, `desc: ""`, `etag: ""`, `id: ""`, `items: []`, `kind: ""`, `parentId: ""`, `reminders: []`, `repeatFlag: ""`, `sortOrder: 0`, `startDate: ""`, `tags: []`.

### Complete a task
```
mcp__dida__complete_task { projectId: "<id>", taskId: "<id>" }
```

### Filter high-priority tasks due this week
```
mcp__dida__filter_tasks {
  taskFilterDto: {
    startDate: "2024-01-15",
    endDate: "2024-01-21",
    priority: [5],
    status: [0],
    projectIds: [],
    kind: [],
    tag: []
  }
}
```

## Priority Levels

| Value | Meaning |
|-------|---------|
| 0 | No priority |
| 1 | Low |
| 3 | Medium |
| 5 | High |

## Task Status

| Value | Meaning |
|-------|---------|
| 0 | Undone |
| 2 | Completed |

## Tips

- **projectIds: []** means "all projects" in filter/date queries
- Tasks in shared lists have a per-user view — tasks assigned to others don't affect your achievement score
- `dueDate` and `startDate` use ISO 8601 with timezone, e.g. `"2024-03-15T10:00:00+08:00"`
- Date range for `list_undone_tasks_by_date` is capped at **14 days** per call
