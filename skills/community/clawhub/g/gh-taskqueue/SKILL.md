---
name: gh-taskqueue
description: "In-memory priority task queue for AI agents. Create tasks with priorities and tags, claim the next highest-priority task, mark tasks complete or failed, filter by status or tag, and get queue statistics. Like a lightweight Celery for agent workflows."
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# TaskQueue

Priority task queue for agent workflows.

## Start the server

```bash
uvicorn taskqueue.app:app --port 8014
```

## Create a task

```bash
curl -s -X POST http://localhost:8014/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Scan skill", "payload": {"skill": "my-skill"}, "priority": 5, "tags": ["security"]}' | jq
```

## Claim the next task (highest priority first)

```bash
curl -s -X POST http://localhost:8014/v1/claim | jq
```

Returns the task with status changed to `running`.

## Complete or fail a task

```bash
curl -s -X POST http://localhost:8014/v1/tasks/TASK_ID/complete \
  -H "Content-Type: application/json" \
  -d '{"result": {"output": "all clear"}}' | jq

curl -s -X POST http://localhost:8014/v1/tasks/TASK_ID/fail \
  -H "Content-Type: application/json" \
  -d '{"error": "scan timed out"}' | jq
```

## List and filter tasks

```bash
curl -s "http://localhost:8014/v1/tasks?status=pending" | jq
curl -s "http://localhost:8014/v1/tasks?tag=security" | jq
```

## Queue stats

```bash
curl -s http://localhost:8014/v1/stats | jq
```

Returns `total`, `pending`, `running`, `completed`, `failed`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/tasks | Create a task |
| GET | /v1/tasks | List tasks (filter: ?status=, ?tag=) |
| GET | /v1/tasks/{id} | Get task by ID |
| POST | /v1/claim | Claim next pending task |
| POST | /v1/tasks/{id}/complete | Mark done with result |
| POST | /v1/tasks/{id}/fail | Mark failed with error |
| GET | /v1/stats | Queue statistics |
