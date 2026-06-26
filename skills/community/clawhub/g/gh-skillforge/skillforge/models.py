"""
Pydantic request/response models for SkillForge API.
"""

from pydantic import BaseModel, ConfigDict, Field


class ForgeSkillRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100, description="Skill name.")
    description: str = Field(..., min_length=1, max_length=500, description="Short description.")
    instructions: str = Field(..., min_length=1, max_length=50_000, description="Skill instructions (Markdown).")
    version: str = Field(default="1.0.0", description="Semver version string.")
    env_vars: list[str] | None = Field(default=None, description="Required environment variables.")
    bins: list[str] | None = Field(default=None, description="Required CLI binaries.")


class ForgeSkillResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_md: str = Field(..., description="Generated SKILL.md content.")
    slug: str = Field(..., description="ClawHub-compatible slug name.")
