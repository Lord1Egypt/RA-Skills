# Feishu Task Manager

Manage Feishu (Lark) tasks and to-dos directly from your AI agent.

## Overview

This skill integrates with the Feishu/Lark Task API, allowing you to:
- Create tasks with assignees, due dates, and descriptions
- List and query your tasks
- Mark tasks as complete
- Add comments to tasks
- Manage task checklists

## Installation

This skill is automatically installed when you install the `feishu-task` skill from ClawHub.

## Configuration

Before using this skill, you need:
1. A Feishu (Lark) account
2. A Feishu application with Task permissions

### Setting up Feishu App

1. Go to [Feishu Open Platform](https://open.feishu.cn/app)
2. Create a new app or select existing app
3. Enable the following permissions:
   - `task:task:readonly`
   - `task:task:write`
   - `task:comment:read`
   - `task:comment:write`
4. Get your `App ID` and `App Secret`
5. Configure the credentials in your OpenClaw config

## Usage

### Create a Task

```
Create a task titled "Review PR #42" assigned to @zhangsan, due tomorrow with priority high
```

### List Tasks

```
Show me all my incomplete tasks
List tasks due this week
```

### Complete a Task

```
Mark task #123456 as completed
```

### Add Comment

```
Add comment "LGTM!" to task #123456
```

## Examples

### Example 1: Quick Task Creation

Human: Create a task for me to review the Q4 report, due Friday

Agent: (uses feishu_task_tool to create the task)

### Example 2: Team Task Management

Human: Assign "Prepare presentation" to all team members, due next Monday

Agent: (creates tasks for each team member)

### Example 3: Daily Review

Human: What tasks are due today?

Agent: (queries Feishu API, returns today's tasks)

## Technical Details

### API Endpoints Used

- `POST /open-apis/task/v2/tasks` - Create task
- `GET /open-apis/task/v2/tasks` - List tasks
- `PATCH /open-apis/task/v2/tasks/:task_guid` - Update task
- `POST /open-apis/task/v2/tasks/:task_guid/complete` - Complete task
- `GET /open-apis/task/v2/tasks/:task_guid/comments` - Get comments
- `POST /open-apis/task/v2/tasks/:task_guid/comments` - Add comment

### Rate Limits

- Standard Feishu API rate limits apply
- Recommended: batch operations when possible

## Troubleshooting

### "Unauthorized" Error
- Check your App ID and App Secret are correct
- Ensure your app has the required permissions

### "Task not found"
- Verify the task GUID is correct
- Check the task exists in your Feishu workspace

### "Permission denied"
- Re-check the permission settings in Feishu Open Platform
- Ensure the app version is published

## Changelog

### 1.0.0 (2026-04-22)
- Initial release
- Full task CRUD operations
- Comment management
- Assignee support

## License

MIT-0
