"""
SkillForge API — FastAPI application.

Single endpoint: POST /v1/forge-skill
Accepts product metadata, returns a valid ClawHub-ready SKILL.md.
"""

from fastapi import FastAPI

from .generator import generate_skill_md, to_slug
from .models import ForgeSkillRequest, ForgeSkillResponse

app = FastAPI(
    title="SkillForge API",
    description="Generate valid ClawHub-compatible SKILL.md files.",
    version="0.1.0",
)


@app.post("/v1/forge-skill", response_model=ForgeSkillResponse)
async def forge_skill(request: ForgeSkillRequest) -> ForgeSkillResponse:
    """Generate a SKILL.md from product metadata."""
    skill_md = generate_skill_md(
        name=request.name,
        description=request.description,
        instructions=request.instructions,
        version=request.version,
        env_vars=request.env_vars,
        bins=request.bins,
    )

    return ForgeSkillResponse(
        skill_md=skill_md,
        slug=to_slug(request.name),
    )
