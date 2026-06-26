# Single-Entry Multi-Task Workbench Protocol

## Goal

Let one Feishu/OpenClaw chat window manage multiple independent workstreams without mixing their context.

## Visible concepts

Users should see only:

- task
- task id
- current task
- status
- summary

Users should not need to see:

- sessionKey
- isolated session
- subagent internals
- routing mechanics

## Canonical commands

Keep Feishu aligned with the Weixin workbench protocol:

- `新建任务：<title>`
- `任务列表`
- `切到 #<id>`
- `继续`
- `总结 #<id>`
- `关闭 #<id>`
- `归档 #<id>`
- `任务状态`

Ordinary plain-text follow-up should route to the current task.

## Minimal data model

```json
{
  "currentTaskId": 2,
  "tasks": [
    {
      "id": 1,
      "title": "周报",
      "sessionKey": "sess_a",
      "status": "completed",
      "updatedAt": "2026-03-20T19:00:00-07:00",
      "summary": "已输出周报终稿"
    },
    {
      "id": 2,
      "title": "PPT",
      "sessionKey": "sess_b",
      "status": "in_progress",
      "updatedAt": "2026-03-20T19:12:00-07:00",
      "summary": "已完成结构与前两页"
    }
  ]
}
```

## Output patterns

### Task list

```text
任务列表 / Task List
#1 周报 [已完成]
#2 PPT [进行中] ← 当前
```

### Summary

```text
任务 #2：PPT
- 进展：已完成结构与前两页
- 当前状态：进行中
- 阻塞：缺少最新数据图
- 下一步：补图并统一视觉样式
```

## Recommended statuses

- `todo`
- `in_progress`
- `waiting_input`
- `blocked`
- `completed`
- `archived`

## Routing decision tree

1. If the user asks for list/create/switch/summarize/close/archive/status, treat it as control-plane work.
2. If the user references `#<id>`, route to that task.
3. Otherwise route ordinary plain-text follow-up content to `currentTaskId`.
4. If there is no current task, ask whether to create one with `新建任务：<title>` or choose from `任务列表`.

For the Feishu rollout, keep responses plain text and prepend the task header when routing into a concrete task:

```text
[任务:#2 周报]
```
