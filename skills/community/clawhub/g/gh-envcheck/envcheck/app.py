"""
EnvCheck API — FastAPI application.

Single endpoint: POST /v1/check-env
Verifies environment readiness: checks if required env vars and binaries exist.
"""

import os
import shutil

from fastapi import FastAPI

from .models import CheckEnvRequest, CheckEnvResponse

app = FastAPI(
    title="EnvCheck API",
    description="Environment readiness checker for AI agents.",
    version="0.1.0",
)


@app.post("/v1/check-env", response_model=CheckEnvResponse)
async def check_env(request: CheckEnvRequest) -> CheckEnvResponse:
    """Check if required env vars and binaries are available."""
    present_env = []
    missing_env = []
    for var in request.required_env:
        if os.environ.get(var) is not None:
            present_env.append(var)
        else:
            missing_env.append(var)

    present_bins = []
    missing_bins = []
    for bin_name in request.required_bins:
        if shutil.which(bin_name) is not None:
            present_bins.append(bin_name)
        else:
            missing_bins.append(bin_name)

    ready = len(missing_env) == 0 and len(missing_bins) == 0

    return CheckEnvResponse(
        ready=ready,
        present_env=present_env,
        missing_env=missing_env,
        present_bins=present_bins,
        missing_bins=missing_bins,
    )
