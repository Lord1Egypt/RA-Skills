"""Integration tests for Ghostclaw MCP memory tools.

These tests exercise the agent-facing memory tools end-to-end, ensuring
correct JSON payloads and interaction with the MemoryStore.
"""

import json
import pytest
import tempfile
from pathlib import Path
import aiosqlite

from ghostclaw.core.memory import MemoryStore

# Skip if aiosqlite is not installed (but it is a requirement)
pytest.importorskip("aiosqlite")


@pytest.fixture
def temp_db():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "ghostclaw.db"
        yield db_path


def _make_report(vibe_score=70, issues=None, architectural_ghosts=None, coupling_metrics=None):
    """Helper to construct a minimal Ghostclaw report."""
    return {
        "vibe_score": vibe_score,
        "issues": issues or [],
        "architectural_ghosts": architectural_ghosts or [],
        "red_flags": [],
        "coupling_metrics": coupling_metrics or {},
        "ai_synthesis": "",
        "files_analyzed": 10,
        "total_lines": 1000,
        "stack": "python",
    }


async def _seed_run(db_path: Path, vibe_score=70, report=None, repo_path="/test/repo", stack="python", timestamp=None):
    """Insert a run directly into the database."""
    if timestamp is None:
        # Increment by second to get distinct ordering
        import itertools
        _seed_run.counter = getattr(_seed_run, "counter", itertools.count())
        base = "2025-01-01T00:00:00"
        ts = f"2025-01-01T00:00:{next(_seed_run.counter):02d}"
    else:
        ts = timestamp
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
            INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, report_json, repo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ts,
                vibe_score,
                stack,
                report.get("files_analyzed", 10),
                report.get("total_lines", 1000),
                json.dumps(report),
                repo_path,
            ),
        )
        await db.commit()
    return True


@pytest.mark.asyncio
async def test_memory_search_integration(temp_db):
    """Test memory search with seeded data."""
    # Initialize DB
    store = MemoryStore(db_path=temp_db)
    await store._ensure_db()

    # Seed two runs
    await _seed_run(temp_db, vibe_score=60, report=_make_report(issues=["Large file", "Missing tests"]))
    await _seed_run(temp_db, vibe_score=80, report=_make_report(issues=["Large file", "Naming convention"]))

    results = await store.search(query="Large file", limit=10)
    response = {"results": results, "count": len(results)}
    parsed = json.loads(json.dumps(response, indent=2))

    assert parsed["count"] == 2
    # At least one snippet contains "Large file" per result
    assert all(any("Large file" in s for s in r["matched_snippets"]) for r in parsed["results"])


@pytest.mark.asyncio
async def test_memory_list_runs_integration(temp_db):
    """Test list_runs returns summaries in descending order."""
    store = MemoryStore(db_path=temp_db)
    await store._ensure_db()

    await _seed_run(temp_db, vibe_score=65, report=_make_report(issues=["issue A"]))
    await _seed_run(temp_db, vibe_score=75, report=_make_report(issues=["issue B"]))

    runs = await store.list_runs(limit=10)
    response = {"runs": runs, "count": len(runs)}
    parsed = json.loads(json.dumps(response, indent=2))

    assert parsed["count"] == 2
    # Latest (higher timestamp) first => vibe_score 75 should be first
    assert runs[0]["vibe_score"] == 75
    assert runs[1]["vibe_score"] == 65


@pytest.mark.asyncio
async def test_memory_get_run_integration(temp_db):
    """Test get_run retrieves full report."""
    store = MemoryStore(db_path=temp_db)
    await store._ensure_db()

    report = _make_report(
        vibe_score=85,
        issues=["God Module: utils.py", "Missing tests"],
        architectural_ghosts=["God Module"],
    )
    await _seed_run(temp_db, vibe_score=85, report=report)

    run = await store.get_run(1)
    response = json.dumps(run, indent=2)
    parsed = json.loads(response)

    assert parsed["vibe_score"] == 85
    # Issues are inside the 'report' key
    assert "God Module: utils.py" in parsed["report"]["issues"]
    assert "God Module" in parsed["report"]["architectural_ghosts"]


@pytest.mark.asyncio
async def test_memory_diff_runs_integration(temp_db):
    """Test diff_runs compares two runs correctly."""
    store = MemoryStore(db_path=temp_db)
    await store._ensure_db()

    report_a = _make_report(vibe_score=60, issues=["issue A", "issue B"], architectural_ghosts=["ghost X"])
    report_b = _make_report(vibe_score=80, issues=["issue B", "issue C"], architectural_ghosts=["ghost X", "ghost Y"])

    await _seed_run(temp_db, vibe_score=60, report=report_a)
    await _seed_run(temp_db, vibe_score=80, report=report_b)

    diff = await store.diff_runs(1, 2)
    response = json.dumps(diff, indent=2)
    parsed = json.loads(response)

    assert parsed["vibe_score_delta"] == 20
    assert "issue C" in parsed["new_issues"]
    assert "issue A" in parsed["resolved_issues"]
    assert "ghost Y" in parsed["new_ghosts"]


@pytest.mark.asyncio
async def test_knowledge_graph_integration(temp_db):
    """Test knowledge_graph aggregates recurring items."""
    store = MemoryStore(db_path=temp_db)
    await store._ensure_db()

    # Seed multiple runs with overlapping issues
    for i in range(3):
        await _seed_run(
            temp_db,
            vibe_score=70,
            report=_make_report(issues=["Large file", "Missing tests"], architectural_ghosts=["God Module"]),
        )
    await _seed_run(
        temp_db,
        vibe_score=90,
        report=_make_report(issues=["Large file"], architectural_ghosts=["Circular Import"]),
    )

    graph = await store.get_knowledge_graph()
    response = json.dumps(graph, indent=2)
    parsed = json.loads(response)

    assert parsed["total_runs"] == 4
    # recurring_issues entries have keys: 'item' and 'count'
    assert any(rec["item"] == "Large file" and rec["count"] >= 4 for rec in parsed["recurring_issues"])
    assert any(rec["item"] == "God Module" and rec["count"] == 3 for rec in parsed["recurring_ghosts"])
