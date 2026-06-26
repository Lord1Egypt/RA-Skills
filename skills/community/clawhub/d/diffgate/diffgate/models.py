"""
Pydantic models for DiffGate API.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DiffRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text_a: str = Field(..., max_length=500_000, description="First text.")
    text_b: str = Field(..., max_length=500_000, description="Second text.")


class Change(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["add", "delete"] = Field(..., description="Type of change.")
    content: str = Field(..., description="Changed line content.")


class DiffResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    similarity: Decimal = Field(..., ge=Decimal("0"), le=Decimal("1"), description="0.0 to 1.0.")
    additions: int = Field(..., ge=0, description="Number of added lines.")
    deletions: int = Field(..., ge=0, description="Number of deleted lines.")
    changes: list[Change] = Field(..., description="List of individual changes.")
