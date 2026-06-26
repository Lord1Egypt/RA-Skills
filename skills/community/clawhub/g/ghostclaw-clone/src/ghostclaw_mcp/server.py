"""
MCP Server implementation for Ghostclaw.
Provides tools: ghostclaw_analyze, ghostclaw_get_ghosts, ghostclaw_refactor_plan,
ghostclaw_memory_search, ghostclaw_memory_get_run, ghostclaw_memory_list_runs,
ghostclaw_memory_diff_runs, ghostclaw_knowledge_graph.
"""

import sys
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

# Use try-import to handle optional dependencies for Phase 2
try:
    from mcp.server.fastmcp import FastMCP
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.memory import MemoryStore
from ghostclaw.core.qmd_store import QMDMemoryStore
from ghostclaw.core.config import GhostclawConfig
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ghostclaw-mcp")

# Initialize MCP server if available
mcp = FastMCP("Ghostclaw") if HAS_MCP else None


def get_analyzer() -> CodebaseAnalyzer:
    return CodebaseAnalyzer()


def get_memory_store(repo_path: Optional[str] = None) -> MemoryStore:
    if repo_path:
        db_path = Path(repo_path) / ".ghostclaw" / "storage" / "ghostclaw.db"
    else:
        db_path = Path.cwd() / ".ghostclaw" / "storage" / "ghostclaw.db"

    # Determine whether to use QMD backend.
    # Precedence: env var > project config > default (False)
    use_qmd = False

    # 1. Environment variable (explicit override)
    if os.getenv("GHOSTCLAW_USE_QMD", "").lower() in ("1", "true", "yes"):
        use_qmd = True
    else:
        # 2. Project config (if repo_path known)
        try:
            cfg = GhostclawConfig.load(repo_path or ".")
            use_qmd = cfg.use_qmd
        except Exception as e:
            logger.debug(f"Could not load Ghostclaw config: {e}")
            use_qmd = False

    if use_qmd:
        qmd_db_path = db_path.parent / "qmd" / "ghostclaw.db"
        # Determine embedding backend, prefetch, migration, and Phase 6 settings from config
        embedding_backend = "fastembed"
        ai_buff_enabled = False
        prefetch_enabled = True
        prefetch_workers = 2
        prefetch_window = 2
        prefetch_hours = 24
        prefetch_vibe_delta = 10
        prefetch_stack_count = 5
        auto_migrate = True
        migration_batch_size = 50
        migration_throttle_ms = 100
        max_chunks_per_report = None
        vector_index_config = {}
        try:
            cfg = GhostclawConfig.load(repo_path or ".")
            embedding_backend = getattr(cfg, 'embedding_backend', 'fastembed')
            ai_buff_enabled = getattr(cfg, 'ai_buff_enabled', False)
            prefetch_enabled = getattr(cfg, 'prefetch_enabled', True)
            prefetch_workers = getattr(cfg, 'prefetch_workers', 2)
            prefetch_window = getattr(cfg, 'prefetch_window', 2)
            prefetch_hours = getattr(cfg, 'prefetch_hours', 24)
            prefetch_vibe_delta = getattr(cfg, 'prefetch_vibe_delta', 10)
            prefetch_stack_count = getattr(cfg, 'prefetch_stack_count', 5)
            auto_migrate = getattr(cfg, 'auto_migrate', True)
            migration_batch_size = getattr(cfg, 'migration_batch_size', 50)
            migration_throttle_ms = getattr(cfg, 'migration_throttle_ms', 100)
            max_chunks_per_report = getattr(cfg, 'max_chunks_per_report', None)
            if hasattr(cfg, 'vector_index'):
                vector_index_config = getattr(cfg, 'vector_index', {})
        except Exception:
            pass
        return QMDMemoryStore(
            db_path=qmd_db_path,
            embedding_backend=embedding_backend,
            ai_buff_enabled=ai_buff_enabled,
            prefetch_enabled=prefetch_enabled,
            prefetch_workers=prefetch_workers,
            prefetch_window=prefetch_window,
            prefetch_hours=prefetch_hours,
            prefetch_vibe_delta=prefetch_vibe_delta,
            prefetch_stack_count=prefetch_stack_count,
            auto_migrate=auto_migrate,
            migration_batch_size=migration_batch_size,
            migration_throttle_ms=migration_throttle_ms,
            max_chunks_per_report=max_chunks_per_report,
            vector_index_config=vector_index_config,
        )
    else:
        return MemoryStore(db_path=db_path)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_analyze(repo_path: str) -> str:
    """
    Perform a full architectural vibe analysis of a codebase.
    Returns a detailed JSON report including vibe score, issues, and ghosts.
    """
    if not Path(repo_path).is_dir():
        return json.dumps({"error": f"Path not found: {repo_path}"})

    analyzer = get_analyzer()
    report = await analyzer.analyze(repo_path)
    return report.model_dump_json(indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_get_ghosts(repo_path: str) -> str:
    """
    Analyze architectural smells and 'ghosts' only.
    Returns a list of identified architectural issues.
    """
    if not Path(repo_path).is_dir():
        return json.dumps({"error": f"Path not found: {repo_path}"})

    analyzer = get_analyzer()
    report = await analyzer.analyze(repo_path)
    ghosts = report.architectural_ghosts
    return json.dumps({"architectural_ghosts": ghosts}, indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_refactor_plan(repo_path: str) -> str:
    """
    Generate an automated refactor blueprint based on architectural analysis.
    Identifies the most critical areas for improvement.
    """
    if not Path(repo_path).is_dir():
        return json.dumps({"error": f"Path not found: {repo_path}"})

    analyzer = get_analyzer()
    report = await analyzer.analyze(repo_path)

    # Placeholder for advanced refactor planning logic (Phase 2 enhancement)
    issues = report.issues
    ghosts = report.architectural_ghosts

    plan = [
        "### Ghostclaw Refactor Blueprint",
        "",
        "1. **Address Critical Issues**:",
        *[f"   - {issue}" for issue in issues[:3]],
        "",
        "2. **Mitigate Architectural Ghosts**:",
        *[f"   - {ghost}" for ghost in ghosts[:3]],
        "",
        "3. **Next Steps**:",
        "   - Review large files and apply SOLID principles.",
        "   - Implement missing unit tests for identified hotspots."
    ]

    return "\n".join(plan)


# --- Agent-Facing Memory Tools ---


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_memory_search(
    query: str,
    repo_path: Optional[str] = None,
    stack: Optional[str] = None,
    min_score: Optional[int] = None,
    max_score: Optional[int] = None,
    limit: int = 10,
) -> str:
    """
    Search Ghostclaw's memory of past analysis runs.

    Searches across stored reports for matching keywords in issues,
    architectural ghosts, red flags, AI synthesis, and all other report fields.
    Supports filtering by repo path, tech stack, and vibe score range.

    Returns matching runs with context snippets showing where the query matched.
    """
    store = get_memory_store(repo_path)
    results = await store.search(
        query=query,
        repo_path=repo_path,
        stack=stack,
        min_score=min_score,
        max_score=max_score,
        limit=limit,
    )
    return json.dumps({"results": results, "count": len(results)}, indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_memory_get_run(
    run_id: int,
    repo_path: Optional[str] = None,
) -> str:
    """
    Retrieve the full report from a specific past Ghostclaw analysis run.

    Use ghostclaw_memory_list_runs to discover available run IDs first.
    Returns the complete analysis report including vibe score, issues,
    architectural ghosts, coupling metrics, and AI synthesis.
    """
    store = get_memory_store(repo_path)
    run = await store.get_run(run_id)
    if not run:
        return json.dumps({"error": f"Run {run_id} not found"})
    return json.dumps(run, indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_memory_list_runs(
    repo_path: Optional[str] = None,
    limit: int = 20,
) -> str:
    """
    List recent Ghostclaw analysis runs from memory.

    Returns summary metadata for each run: id, timestamp, vibe score,
    detected stack, files analyzed, and total lines. Use the run id
    with ghostclaw_memory_get_run to fetch the full report.
    """
    store = get_memory_store(repo_path)
    runs = await store.list_runs(limit=limit, repo_path=repo_path)
    return json.dumps({"runs": runs, "count": len(runs)}, indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_memory_diff_runs(
    run_id_a: int,
    run_id_b: int,
    repo_path: Optional[str] = None,
) -> str:
    """
    Compare two past Ghostclaw analysis runs and show what changed.

    Highlights vibe score delta, new/resolved issues, new/resolved
    architectural ghosts, and metrics comparison between the two runs.
    Useful for tracking architectural improvements or regressions over time.
    """
    store = get_memory_store(repo_path)
    diff = await store.diff_runs(run_id_a, run_id_b)
    if not diff:
        return json.dumps({"error": "One or both runs not found"})
    return json.dumps(diff, indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_knowledge_graph(
    repo_path: Optional[str] = None,
    limit: int = 50,
) -> str:
    """
    Query Ghostclaw's knowledge graph built from analysis history.

    Aggregates data across past runs to reveal recurring architectural
    patterns: frequently seen issues, persistent ghosts, coupling hotspots
    with high instability, vibe score trends over time, and detected stacks.

    This provides agents with a high-level architectural memory of the
    codebase that goes beyond any single analysis run.
    """
    store = get_memory_store(repo_path)
    graph = await store.get_knowledge_graph(repo_path=repo_path, limit=limit)
    return json.dumps(graph, indent=2)


@mcp.tool() if HAS_MCP else lambda x: x
async def ghostclaw_memory_get_previous_run(
    repo_path: Optional[str] = None,
) -> str:
    """
    Get the most recent Ghostclaw analysis run from memory.

    Returns the full report from the last analysis run, optionally
    filtered by repository path. Useful for agents that need to recall
    what Ghostclaw found during its previous analysis of a codebase.
    """
    store = get_memory_store(repo_path)
    run = await store.get_previous_run(repo_path=repo_path)
    if not run:
        return json.dumps({"error": "No previous runs found"})
    return json.dumps(run, indent=2)


def main():
    """Entry point for the MCP server."""
    if not HAS_MCP:
        print("Error: mcp-sdk not installed. Install with 'pip install ghostclaw[mcp]'.", file=sys.stderr)
        sys.exit(1)

    mcp.run()


if __name__ == "__main__":
    main()
