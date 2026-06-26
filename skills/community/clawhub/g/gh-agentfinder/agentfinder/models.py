"""
Pydantic models for AgentFinder API.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., min_length=1, max_length=500, description="What you're looking for.")
    registries: list[str] | None = Field(default=None, description="Registries to search. None = all.")
    max_results: int = Field(default=10, gt=0, le=100)
    min_score: Decimal = Field(default=Decimal("0"), ge=Decimal("0"), le=Decimal("1"))


class SkillResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    registry: str
    author: str = ""
    version: str = ""
    score: Decimal = Field(default=Decimal("0"), ge=Decimal("0"), le=Decimal("1"), description="Relevance score.")
    url: str = ""
    tags: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    results: list[SkillResult]
    total: int = Field(..., ge=0)
    registries_searched: list[str]


class RecommendRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    problem: str = Field(..., min_length=1, max_length=2000, description="Describe what you need.")
    max_results: int = Field(default=5, gt=0, le=20)


class RecommendResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    problem: str
    recommendations: list[SkillResult]
    total: int = Field(..., ge=0)


class RegistryInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    url: str
    status: Literal["active", "coming_soon"]
    skill_count: int = Field(default=0, ge=0)
    description: str


class RegistriesResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    registries: list[RegistryInfo]
    total: int = Field(..., ge=0)


class CompareResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    by_registry: dict[str, list[SkillResult]]
    total: int = Field(..., ge=0)
