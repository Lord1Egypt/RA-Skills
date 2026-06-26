"""
TaskQueue API — In-memory priority task queue.

Endpoints:
  POST   /v1/tasks              — create a task
  GET    /v1/tasks               — list tasks (filter by status, tag)
  GET    /v1/tasks/{id}          — get task by ID
  POST   /v1/claim               — claim the next highest-priority pending task
  POST   /v1/tasks/{id}/complete — mark task completed with result
  POST   /v1/tasks/{id}/fail     — mark task failed with error
  GET    /v1/stats               — queue statistics
"""

from fastapi import FastAPI, HTTPException, Query

from .models import (
    CompleteRequest,
    CreateTaskRequest,
    FailRequest,
    QueueStatsResponse,
    TaskListResponse,
    TaskResponse,
)
from .state import claim_next, complete_task, create_task, fail_task, get_task, list_tasks, queue_stats

app = FastAPI(
    title="TaskQueue API",
    description="In-memory priority task queue for AI agent workflows.",
    version="0.1.0",
)


def _task_to_response(task) -> TaskResponse:
    return TaskResponse(
        id=task.id, title=task.title, status=task.status,
        priority=task.priority, tags=task.tags, payload=task.payload,
        result=task.result, error=task.error, created_at=task.created_at,
    )


@app.post("/v1/tasks", response_model=TaskResponse)
async def create(request: CreateTaskRequest) -> TaskResponse:
    task = create_task(request.title, request.payload, request.priority, request.tags)
    return _task_to_response(task)


@app.get("/v1/tasks", response_model=TaskListResponse)
async def list_all(
    status: str | None = Query(default=None),
    tag: str | None = Query(default=None),
) -> TaskListResponse:
    tasks = list_tasks(status, tag)
    return TaskListResponse(tasks=[_task_to_response(t) for t in tasks], total=len(tasks))


@app.get("/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_by_id(task_id: str) -> TaskResponse:
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return _task_to_response(task)


@app.post("/v1/claim", response_model=TaskResponse)
async def claim() -> TaskResponse:
    task = claim_next()
    if task is None:
        raise HTTPException(status_code=404, detail="No pending tasks to claim")
    return _task_to_response(task)


@app.post("/v1/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete(task_id: str, request: CompleteRequest) -> TaskResponse:
    task = complete_task(task_id, request.result)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return _task_to_response(task)


@app.post("/v1/tasks/{task_id}/fail", response_model=TaskResponse)
async def fail(task_id: str, request: FailRequest) -> TaskResponse:
    task = fail_task(task_id, request.error)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return _task_to_response(task)


@app.get("/v1/stats", response_model=QueueStatsResponse)
async def stats() -> QueueStatsResponse:
    return QueueStatsResponse(**queue_stats())
