"""
PipelineGate API — Configurable multi-step pipeline engine.

Chains Green Helix tools into workflows. Agents define steps,
PipelineGate executes them in sequence.
"""

from fastapi import FastAPI

from .executor import TOOLS, execute_step
from .models import (
    PipelineRequest,
    PipelineResponse,
    StepResult,
    ToolInfo,
    ToolsResponse,
)

app = FastAPI(
    title="PipelineGate API",
    description="Multi-step pipeline engine for Green Helix tools.",
    version="0.1.0",
)


@app.post("/v1/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest) -> PipelineResponse:
    """Execute a multi-step pipeline."""
    results: list[StepResult] = []
    completed = 0
    overall_success = True

    for step in request.steps:
        success, output, error = execute_step(step.tool, step.input)
        results.append(StepResult(
            tool=step.tool,
            success=success,
            output=output,
            error=error,
        ))
        if success:
            completed += 1
        else:
            overall_success = False
            if request.stop_on_error:
                break

    return PipelineResponse(
        success=overall_success,
        total_steps=len(request.steps),
        completed_steps=completed,
        results=results,
    )


@app.get("/v1/tools", response_model=ToolsResponse)
async def list_tools() -> ToolsResponse:
    """List available pipeline tools."""
    return ToolsResponse(
        tools=[
            ToolInfo(
                name=name,
                description=info["description"],
                input_fields=info["fields"],
            )
            for name, info in TOOLS.items()
        ]
    )
