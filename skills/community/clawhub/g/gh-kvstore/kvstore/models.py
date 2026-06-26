"""
Pydantic models for KVStore API.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1, max_length=500)
    value: Any = Field(...)
    ttl_seconds: int | None = Field(default=None, gt=0, le=86400, description="Time to live in seconds.")


class GetResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    value: Any
    ttl_remaining: int | None = Field(default=None, description="Seconds until expiry, or null if permanent.")


class SetResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    stored: bool


class DeleteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    deleted: bool


class KeyListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    keys: list[str]
    total: int = Field(..., ge=0)


class FlushResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deleted: int = Field(..., ge=0)


class StatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_keys: int = Field(..., ge=0)
    hits: int = Field(..., ge=0)
    misses: int = Field(..., ge=0)
