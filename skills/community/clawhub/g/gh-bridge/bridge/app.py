"""
Bridge API — Agent-to-Human verification & escrow platform.

Endpoints:
  POST   /v1/tasks              — Request human actuation
  GET    /v1/tasks               — List tasks (filter by status)
  GET    /v1/tasks/{id}          — Get task by ID
  POST   /v1/tasks/{id}/verify   — Submit proof and verify
  POST   /v1/tasks/{id}/dispute  — Dispute a task
  GET    /v1/platforms           — List available platforms
  GET    /v1/stats               — Platform statistics
"""

from fastapi import FastAPI, HTTPException, Query

from .models import (
    BridgeStatsResponse,
    CreateTaskRequest,
    DisputeRequest,
    DisputeResponse,
    PlatformInfo,
    PlatformsResponse,
    TaskListResponse,
    TaskResponse,
    VerifyRequest,
    VerifyResponse,
)
from .state import bridge_stats, create_task, dispute_task, get_task, list_tasks, update_task_status
from .verifier import verify_all

app = FastAPI(
    title="Bridge API",
    description="Agent-to-Human verification & escrow platform.",
    version="0.1.0",
)


def _task_to_response(task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        description=task.description,
        status=task.status,
        budget_usdc=task.budget_usdc,
        fee_usdc=task.fee_usdc,
        escrow_status=task.escrow_status,
        location=task.location,
        verification_criteria=task.verification_criteria,
        priority=task.priority,
        deadline_hours=task.deadline_hours,
        created_at=task.created_at,
        worker_id=task.worker_id,
    )


@app.post("/v1/tasks", response_model=TaskResponse)
async def create(request: CreateTaskRequest) -> TaskResponse:
    """Request human actuation — create a task with escrow."""
    task = create_task(
        description=request.description,
        budget_usdc=request.budget_usdc,
        location=request.location,
        verification_criteria=request.verification_criteria,
        priority=request.priority,
        deadline_hours=request.deadline_hours,
    )
    return _task_to_response(task)


@app.get("/v1/tasks", response_model=TaskListResponse)
async def list_all(status: str | None = Query(default=None)) -> TaskListResponse:
    """List all tasks, optionally filtered by status."""
    tasks = list_tasks(status)
    return TaskListResponse(
        tasks=[_task_to_response(t) for t in tasks],
        total=len(tasks),
    )


@app.get("/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_by_id(task_id: str) -> TaskResponse:
    """Get a task by ID."""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return _task_to_response(task)


@app.post("/v1/tasks/{task_id}/verify", response_model=VerifyResponse)
async def verify(task_id: str, request: VerifyRequest) -> VerifyResponse:
    """Submit proof and verify against criteria."""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    if task.status == "disputed":
        raise HTTPException(status_code=409, detail="Task is disputed — cannot verify")

    update_task_status(task_id, "proof_submitted", worker_id=request.worker_id)

    all_passed, results = verify_all(task.verification_criteria, request.proofs)

    if all_passed:
        update_task_status(task_id, "completed", escrow_status="released")
        escrow_action = "release"
    else:
        update_task_status(task_id, "failed", escrow_status="locked")
        escrow_action = "hold"

    return VerifyResponse(
        task_id=task_id,
        verification_status="PASSED" if all_passed else "FAILED",
        criteria_results=results,
        escrow_action=escrow_action,
    )


@app.post("/v1/tasks/{task_id}/dispute", response_model=DisputeResponse)
async def file_dispute(task_id: str, request: DisputeRequest) -> DisputeResponse:
    """Dispute a task — freezes escrow."""
    task = dispute_task(task_id, request.reason)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return DisputeResponse(
        task_id=task_id,
        status=task.status,
        escrow_status=task.escrow_status,
        dispute_reason=task.dispute_reason,
    )


@app.get("/v1/platforms", response_model=PlatformsResponse)
async def get_platforms() -> PlatformsResponse:
    """List available human-work platforms."""
    return PlatformsResponse(platforms=[
        PlatformInfo(name="rentahuman", status="active", description="RentAHuman.ai — crypto-native A2H marketplace"),
        PlatformInfo(name="meatlayer", status="coming_soon", description="MeatLayer — physical world API layer"),
        PlatformInfo(name="manual", status="active", description="Manual fulfillment via Telegram notification"),
    ])


@app.get("/v1/stats", response_model=BridgeStatsResponse)
async def stats() -> BridgeStatsResponse:
    """Get platform statistics."""
    s = bridge_stats()
    return BridgeStatsResponse(**s)
