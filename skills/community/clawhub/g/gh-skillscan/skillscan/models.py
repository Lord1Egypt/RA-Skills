"""
Pydantic request/response models for SkillScan API.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ScanSkillRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_content: str = Field(
        ...,
        min_length=1,
        max_length=500_000,
        description="Raw content of the SKILL.md file to scan.",
    )


class ScanSkillResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    safety_score: Decimal = Field(
        ...,
        ge=Decimal("0"),
        le=Decimal("1"),
        description="Safety score in [0.0, 1.0]. Higher = safer.",
    )
    findings: list[str] = Field(
        ...,
        description="List of detected threat pattern names.",
    )
    verdict: Literal["SAFE", "CAUTION", "DANGEROUS"] = Field(
        ...,
        description="Overall safety verdict.",
    )
    skill_name: str = Field(
        ...,
        description="Extracted skill name from frontmatter, or 'unknown'.",
    )
