"""
Bridge API — Agent-to-Human verification & escrow platform.

Endpoints:
  POST   /v1/tasks              — Request human actuation
  GET    /v1/tasks               — List tasks (filter by status)
  GET    /v1/tasks/{id}          — Get task by ID
  POST   /v1/tasks/{id}/accept   — Worker accepts a task
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
    VerifyMilestoneRequest,
    VerifyRequest,
    VerifyResponse,
    WorkerListResponse,
    WorkerResponse,
)
from .state import (
    bridge_stats,
    complete_milestone,
    create_task,
    dispute_task,
    get_task,
    get_worker,
    list_tasks,
    list_workers,
    record_worker_outcome,
    update_task_status,
)
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
        milestones=task.milestones,
        milestones_completed=task.milestones_completed,
        milestones_total=task.milestones_total,
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
        milestones=request.milestones,
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


@app.post("/v1/tasks/{task_id}/accept", response_model=TaskResponse)
async def accept_task(task_id: str, worker_id: str = Query(...)) -> TaskResponse:
    """Worker accepts a task — status moves to 'accepted'."""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    if task.status != "posted":
        raise HTTPException(status_code=409, detail=f"Task cannot be accepted in state '{task.status}'")
    update_task_status(task_id, "accepted", worker_id=worker_id)
    return _task_to_response(get_task(task_id))


@app.post("/v1/tasks/{task_id}/verify", response_model=VerifyResponse)
async def verify(task_id: str, request: VerifyRequest) -> VerifyResponse:
    """Submit proof and verify against criteria."""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    if task.status not in ("posted", "accepted"):
        raise HTTPException(
            status_code=409,
            detail=f"Task cannot be verified in state '{task.status}' — must be 'posted' or 'accepted'",
        )

    update_task_status(task_id, "proof_submitted", worker_id=request.worker_id)

    all_passed, results = verify_all(task.verification_criteria, request.proofs)

    if all_passed:
        update_task_status(task_id, "completed", escrow_status="released")
        escrow_action = "release"
        record_worker_outcome(request.worker_id, "completed", earned=task.budget_usdc - task.fee_usdc)
    else:
        update_task_status(task_id, "failed", escrow_status="locked")
        escrow_action = "hold"
        record_worker_outcome(request.worker_id, "failed")

    return VerifyResponse(
        task_id=task_id,
        verification_status="PASSED" if all_passed else "FAILED",
        criteria_results=results,
        escrow_action=escrow_action,
    )


@app.post("/v1/tasks/{task_id}/verify-milestone", response_model=VerifyResponse)
async def verify_milestone(task_id: str, request: VerifyMilestoneRequest) -> VerifyResponse:
    """Verify a specific milestone within a task."""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    if not task.milestones:
        raise HTTPException(status_code=400, detail="Task has no milestones")
    if task.status in ("completed", "refunded", "disputed"):
        raise HTTPException(status_code=409, detail=f"Task cannot be verified in state '{task.status}'")
    if request.milestone_index >= len(task.milestones):
        raise HTTPException(status_code=400, detail=f"Milestone index {request.milestone_index} out of range (0-{len(task.milestones)-1})")

    ms = task.milestones[request.milestone_index]
    ms_criteria = ms.criteria if hasattr(ms, 'criteria') else ms.get("criteria", [])

    all_passed, results = verify_all(ms_criteria, request.proofs)

    if all_passed:
        updated_task, released = complete_milestone(task_id, request.milestone_index)
        record_worker_outcome(request.worker_id, "completed", earned=released)
        escrow_action = "release"
    else:
        record_worker_outcome(request.worker_id, "failed")
        escrow_action = "hold"

    return VerifyResponse(
        task_id=task_id,
        verification_status="PASSED" if all_passed else "FAILED",
        criteria_results=results,
        escrow_action=escrow_action,
        milestone_index=request.milestone_index,
        budget_released_usdc=released if all_passed else None,
    )


@app.post("/v1/tasks/{task_id}/dispute", response_model=DisputeResponse)
async def file_dispute(task_id: str, request: DisputeRequest) -> DisputeResponse:
    """Dispute a task — freezes escrow."""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    if task.status in ("completed", "refunded"):
        raise HTTPException(
            status_code=409,
            detail=f"Task cannot be disputed in state '{task.status}' — escrow already settled",
        )
    if task.worker_id:
        record_worker_outcome(task.worker_id, "disputed")
    task = dispute_task(task_id, request.reason)
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


# ── Worker reputation ──────────────────────────────────────────────────────

def _worker_to_response(w) -> WorkerResponse:
    return WorkerResponse(
        worker_id=w.worker_id,
        score=w.score,
        tasks_completed=w.tasks_completed,
        tasks_failed=w.tasks_failed,
        tasks_disputed=w.tasks_disputed,
        total_earned_usdc=w.total_earned_usdc,
    )


@app.get("/v1/workers", response_model=WorkerListResponse)
async def get_workers() -> WorkerListResponse:
    """List all workers sorted by reputation score."""
    workers = list_workers()
    return WorkerListResponse(
        workers=[_worker_to_response(w) for w in workers],
        total=len(workers),
    )


@app.get("/v1/workers/{worker_id}", response_model=WorkerResponse)
async def get_worker_profile(worker_id: str) -> WorkerResponse:
    """Get a worker's reputation profile."""
    w = get_worker(worker_id)
    if w is None:
        raise HTTPException(status_code=404, detail=f"Worker not found: {worker_id}")
    return _worker_to_response(w)
