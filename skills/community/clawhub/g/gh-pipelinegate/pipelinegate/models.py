"""
Pydantic models for PipelineGate API.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PipelineStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool: str = Field(..., description="Tool name (scan-text, scan-skill, check-scope, validate, diff, check-env, convert).")
    input: dict[str, Any] = Field(..., description="Input payload for the tool.")


class PipelineRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    steps: list[PipelineStep] = Field(..., min_length=1, max_length=20, description="Pipeline steps to execute.")
    stop_on_error: bool = Field(default=True, description="Stop pipeline on first error.")


class StepResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool: str
    success: bool
    output: dict[str, Any] = Field(default_factory=dict)
    error: str = Field(default="")


class PipelineResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    total_steps: int = Field(..., ge=0)
    completed_steps: int = Field(..., ge=0)
    results: list[StepResult]


class ToolInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    input_fields: list[str]


class ToolsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tools: list[ToolInfo]
