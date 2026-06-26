"""
Pydantic request/response models for DataGate API.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ValidateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    json_schema: dict[str, Any] = Field(
        ..., description="JSON Schema to validate against."
    )
    payload: Any = Field(..., description="The data payload to validate.")


class ValidationError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(..., description="JSON path to the error location.")
    message: str = Field(..., description="Human-readable error description.")


class ValidateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valid: bool = Field(..., description="Whether the payload is valid.")
    error_count: int = Field(..., ge=0, description="Number of validation errors.")
    errors: list[ValidationError] = Field(..., description="List of validation errors.")
