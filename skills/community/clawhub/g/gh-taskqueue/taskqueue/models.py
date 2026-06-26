"""
Pydantic models for TaskQueue API.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class CreateTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=500)
    payload: Any = Field(...)
    priority: int = Field(default=0, ge=0, le=100)
    tags: list[str] = Field(default_factory=list, max_length=20)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    status: Literal["pending", "running", "completed", "failed"]
    priority: int
    tags: list[str]
    payload: Any
    result: Any = None
    error: str = ""
    created_at: str


class TaskListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tasks: list[TaskResponse]
    total: int = Field(..., ge=0)


class CompleteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result: Any = Field(...)


class FailRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str = Field(..., min_length=1)


class QueueStatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int = Field(..., ge=0)
    pending: int = Field(..., ge=0)
    running: int = Field(..., ge=0)
    completed: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)
