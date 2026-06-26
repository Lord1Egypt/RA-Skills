"""
Registry adapters for AgentFinder.

Each adapter implements search against a specific skill registry.
For now, uses a local index that can be populated from real registries.
"""

from decimal import ROUND_HALF_UP, Decimal
from difflib import SequenceMatcher

from .models import SkillResult


# ── Local skill index (populated from registries or manually) ──────────────

_SKILL_INDEX: list[dict] = [
    # ClawHub skills (Green Helix products)
    {"name": "promptguard", "description": "Detect prompt injection attacks in text", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/promptguard", "tags": ["security", "injection", "scanning"]},
    {"name": "gh-skillscan", "description": "Scan SKILL.md files for security threats", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-skillscan", "tags": ["security", "scanning", "openclaw"]},
    {"name": "scopecheck", "description": "Analyze SKILL.md permission scopes", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/scopecheck", "tags": ["security", "permissions", "openclaw"]},
    {"name": "datagate", "description": "Validate JSON against JSON Schema", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/datagate", "tags": ["data", "validation", "schema"]},
    {"name": "gh-skillforge", "description": "Generate ClawHub-ready SKILL.md files", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-skillforge", "tags": ["devtools", "generator", "openclaw"]},
    {"name": "diffgate", "description": "Compare two texts with similarity scoring", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/diffgate", "tags": ["text", "diff", "comparison"]},
    {"name": "formatgate", "description": "Convert between JSON YAML and TOML", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/formatgate", "tags": ["data", "format", "conversion"]},
    {"name": "healthprobe", "description": "Check URL health status and latency", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/healthprobe", "tags": ["infrastructure", "monitoring", "health"]},
    {"name": "gh-securitysuite", "description": "Comprehensive security platform with 7 endpoints", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-securitysuite", "tags": ["security", "audit", "batch"]},
    {"name": "gh-pipelinegate", "description": "Multi-step pipeline engine for tool workflows", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-pipelinegate", "tags": ["pipeline", "workflow", "orchestration"]},
    {"name": "gh-ratelimiter", "description": "In-memory sliding window rate limiter", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-ratelimiter", "tags": ["infrastructure", "rate-limit", "throttling"]},
    {"name": "gh-kvstore", "description": "Key-value store with TTL for agent state", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-kvstore", "tags": ["storage", "cache", "state"]},
    {"name": "gh-taskqueue", "description": "Priority task queue for agent workflows", "registry": "clawhub", "author": "mirni", "version": "1.0.0", "url": "https://clawhub.ai/mirni/gh-taskqueue", "tags": ["queue", "tasks", "workflow"]},
    {"name": "a2h-bridge", "description": "Agent-to-Human verification and escrow platform", "registry": "clawhub", "author": "mirni", "version": "2.0.0", "url": "https://clawhub.ai/mirni/a2h-bridge", "tags": ["a2h", "escrow", "verification", "physical"]},
    # Well-known third-party skills
    {"name": "github", "description": "Interact with GitHub using the gh CLI", "registry": "clawhub", "author": "steipete", "version": "1.0.0", "url": "https://clawhub.ai/steipete/github", "tags": ["github", "git", "pr", "issues"]},
    {"name": "coding-agent", "description": "Run coding agents in background processes", "registry": "clawhub", "author": "steipete", "version": "1.0.0", "url": "https://clawhub.ai/steipete/coding-agent", "tags": ["coding", "agent", "background"]},
    # SkillsMP examples
    {"name": "web-search", "description": "Search the web and return structured results", "registry": "skillsmp", "author": "community", "version": "1.0.0", "url": "https://skillsmp.com/skills/web-search", "tags": ["search", "web", "research"]},
    {"name": "code-review", "description": "Automated code review with suggestions", "registry": "skillsmp", "author": "community", "version": "1.0.0", "url": "https://skillsmp.com/skills/code-review", "tags": ["code", "review", "quality"]},
    # LobeHub examples
    {"name": "pdf-reader", "description": "Extract text and data from PDF documents", "registry": "lobehub", "author": "lobehub", "version": "1.0.0", "url": "https://lobehub.com/skills/pdf-reader", "tags": ["pdf", "document", "extraction"]},
    {"name": "image-gen", "description": "Generate images from text descriptions", "registry": "lobehub", "author": "lobehub", "version": "1.0.0", "url": "https://lobehub.com/skills/image-gen", "tags": ["image", "generation", "creative"]},
]

REGISTRIES = {
    "clawhub": {"url": "https://clawhub.ai", "status": "active", "skill_count": 18000, "description": "OpenClaw skill registry with vector search"},
    "skillsmp": {"url": "https://skillsmp.com", "status": "active", "skill_count": 66000, "description": "Aggregator for Claude Code, Codex, ChatGPT skills"},
    "lobehub": {"url": "https://lobehub.com/skills", "status": "active", "skill_count": 5000, "description": "LobeHub skill marketplace"},
    "moltbook": {"url": "https://moltbook.com", "status": "coming_soon", "skill_count": 0, "description": "Social network for AI agents — service discovery"},
}


def _relevance_score(query: str, skill: dict) -> Decimal:
    """Compute relevance score using fuzzy matching on name, description, and tags."""
    q = query.lower()
    name_score = SequenceMatcher(None, q, skill["name"].lower()).ratio()
    desc_score = SequenceMatcher(None, q, skill["description"].lower()).ratio()

    # Boost for exact substring match
    name_bonus = 0.3 if q in skill["name"].lower() else 0
    desc_bonus = 0.2 if q in skill["description"].lower() else 0

    # Tag match boost
    tag_bonus = 0
    for tag in skill.get("tags", []):
        if q in tag.lower() or tag.lower() in q:
            tag_bonus = 0.25
            break

    raw_score = max(name_score, desc_score) + name_bonus + desc_bonus + tag_bonus
    return Decimal(str(min(1.0, raw_score))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def search_skills(
    query: str,
    registries: list[str] | None = None,
    max_results: int = 10,
    min_score: Decimal = Decimal("0"),
) -> list[SkillResult]:
    """Search the skill index."""
    results = []
    for skill in _SKILL_INDEX:
        if registries and skill["registry"] not in registries:
            continue
        score = _relevance_score(query, skill)
        if score >= min_score:
            results.append(SkillResult(
                name=skill["name"],
                description=skill["description"],
                registry=skill["registry"],
                author=skill.get("author", ""),
                version=skill.get("version", ""),
                score=score,
                url=skill.get("url", ""),
                tags=skill.get("tags", []),
            ))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:max_results]


def search_by_registry(query: str, max_per_registry: int = 5) -> dict[str, list[SkillResult]]:
    """Search and group results by registry."""
    by_reg: dict[str, list[SkillResult]] = {}
    for reg_name in REGISTRIES:
        if REGISTRIES[reg_name]["status"] != "active":
            continue
        results = search_skills(query, registries=[reg_name], max_results=max_per_registry)
        if results:
            by_reg[reg_name] = results
    return by_reg
