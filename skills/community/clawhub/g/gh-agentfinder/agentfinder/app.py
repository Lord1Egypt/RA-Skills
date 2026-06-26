"""
AgentFinder API — "Kayak for agents" skill discovery aggregator.

Endpoints:
  POST   /v1/search              — Search across all registries
  GET    /v1/search/{query}/compare — Compare results by registry
  POST   /v1/recommend            — Get skill recommendations for a problem
  GET    /v1/registries           — List available registries
"""

from fastapi import FastAPI

from .models import (
    CompareResponse,
    RecommendRequest,
    RecommendResponse,
    RegistriesResponse,
    RegistryInfo,
    SearchRequest,
    SearchResponse,
)
from .registries import REGISTRIES, search_by_registry, search_skills

app = FastAPI(
    title="AgentFinder API",
    description="Skill discovery aggregator — search across ClawHub, SkillsMP, LobeHub, and more.",
    version="0.1.0",
)


@app.post("/v1/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Search for skills across registries."""
    results = search_skills(
        query=request.query,
        registries=request.registries,
        max_results=request.max_results,
        min_score=request.min_score,
    )
    searched = request.registries or [r for r, info in REGISTRIES.items() if info["status"] == "active"]
    return SearchResponse(
        query=request.query,
        results=results,
        total=len(results),
        registries_searched=searched,
    )


@app.get("/v1/search/{query}/compare", response_model=CompareResponse)
async def compare(query: str) -> CompareResponse:
    """Compare search results across registries."""
    by_reg = search_by_registry(query)
    total = sum(len(v) for v in by_reg.values())
    return CompareResponse(query=query, by_registry=by_reg, total=total)


@app.post("/v1/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest) -> RecommendResponse:
    """Recommend skills for a problem description."""
    # Extract key terms from the problem and search
    results = search_skills(
        query=request.problem,
        max_results=request.max_results,
    )
    return RecommendResponse(
        problem=request.problem,
        recommendations=results,
        total=len(results),
    )


@app.get("/v1/registries", response_model=RegistriesResponse)
async def list_registries() -> RegistriesResponse:
    """List available skill registries."""
    regs = [
        RegistryInfo(
            name=name,
            url=info["url"],
            status=info["status"],
            skill_count=info["skill_count"],
            description=info["description"],
        )
        for name, info in REGISTRIES.items()
    ]
    return RegistriesResponse(registries=regs, total=len(regs))
