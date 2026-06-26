"""
Pydantic models for EnvCheck API.
"""

from pydantic import BaseModel, ConfigDict, Field


class CheckEnvRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required_env: list[str] = Field(default_factory=list, description="Env vars that must be set.")
    required_bins: list[str] = Field(default_factory=list, description="CLI tools that must be on PATH.")


class CheckEnvResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ready: bool = Field(..., description="True if all requirements are met.")
    present_env: list[str] = Field(..., description="Env vars that are set.")
    missing_env: list[str] = Field(..., description="Env vars that are NOT set.")
    present_bins: list[str] = Field(..., description="Bins found on PATH.")
    missing_bins: list[str] = Field(..., description="Bins NOT found on PATH.")
