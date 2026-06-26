"""
Pydantic models for RateLimiter API.
"""

from pydantic import BaseModel, ConfigDict, Field


class CreateLimitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1, max_length=200, description="Unique identifier for this rate limit.")
    max_requests: int = Field(..., gt=0, le=100_000, description="Max requests per window.")
    window_seconds: int = Field(..., gt=0, le=86400, description="Sliding window duration in seconds.")


class LimitStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    allowed: bool
    remaining: int = Field(..., ge=0)
    limit: int = Field(..., gt=0)
    window_seconds: int = Field(..., gt=0)
    retry_after_seconds: int = Field(default=0, ge=0)


class LimitInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    max_requests: int
    remaining: int
    window_seconds: int


class LimitListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    limits: list[LimitInfo]
    total: int = Field(..., ge=0)


class DeleteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    deleted: bool
