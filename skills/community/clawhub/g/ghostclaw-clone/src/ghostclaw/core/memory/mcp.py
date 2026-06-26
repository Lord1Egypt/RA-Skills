"""
Advanced memory functionality for Ghostclaw (Search, Diff, Knowledge Graph).
These are primarily used by the MCP server tools.
"""

import json
import sqlite3
import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional

try:
    import aiosqlite
except ImportError:
    pass

logger = logging.getLogger("ghostclaw.memory.mcp")


async def search_memory(
    store: Any,
    query: str,
    repo_path: Optional[str] = None,
    stack: Optional[str] = None,
    min_score: Optional[int] = None,
    max_score: Optional[int] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Search across past analysis reports by keyword and optional filters."""
    if not store._db_exists():
        return []

    conditions = []
    params: list = []

    if query:
        conditions.append("report_json LIKE ? ESCAPE '\\'")
        escaped_query = query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        params.append(f"%{escaped_query}%")

    if repo_path:
        conditions.append("repo_path = ?")
        params.append(repo_path)

    if stack:
        conditions.append("stack = ?")
        params.append(stack)

    if min_score is not None:
        conditions.append("vibe_score >= ?")
        params.append(min_score)

    if max_score is not None:
        conditions.append("vibe_score <= ?")
        params.append(max_score)

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    sql = (
        f"SELECT id, timestamp, vibe_score, stack, files_analyzed, "
        f"total_lines, repo_path, report_json FROM reports "
        f"WHERE {where_clause} ORDER BY timestamp DESC LIMIT ?"
    )
    params.append(limit)

    async with aiosqlite.connect(store.db_path) as db:
        db.row_factory = sqlite3.Row
        async with db.execute(sql, params) as cursor:
            rows = await cursor.fetchall()

    results = []
    for row in rows:
        row_dict = dict(row)
        report_json_str = row_dict.pop("report_json", "{}")
        snippets = _extract_snippets(report_json_str, query)
        row_dict["matched_snippets"] = snippets
        results.append(row_dict)

    return results


def _extract_snippets(
    report_json_str: str, query: str, max_snippets: int = 5, context_chars: int = 120
) -> List[str]:
    """Extract text snippets around query matches in the report JSON."""
    if not query:
        return []

    snippets = []
    lower_text = report_json_str.lower()
    lower_query = query.lower()
    search_start = 0

    while len(snippets) < max_snippets:
        idx = lower_text.find(lower_query, search_start)
        if idx == -1:
            break
        start = max(0, idx - context_chars)
        end = min(len(report_json_str), idx + len(query) + context_chars)
        snippet = report_json_str[start:end].strip()
        snippet = snippet.replace("\\n", " ").replace('\\"', '"')
        snippets.append(f"...{snippet}...")
        search_start = idx + len(query)

    return snippets


async def diff_analysis_runs(
    store: Any, run_id_a: int, run_id_b: int
) -> Optional[Dict[str, Any]]:
    """Compare two analysis runs and highlight differences."""
    run_a = await store.get_run(run_id_a)
    run_b = await store.get_run(run_id_b)

    if not run_a or not run_b:
        return None

    report_a = run_a.get("report", {})
    report_b = run_b.get("report", {})

    def _make_mapping(items):
        mapping = {}
        for item in items:
            if isinstance(item, dict):
                key = json.dumps(item, sort_keys=True)
            else:
                key = str(item)
            mapping[key] = item
        return mapping

    issues_a_map = _make_mapping(report_a.get("issues", []))
    issues_b_map = _make_mapping(report_b.get("issues", []))
    ghosts_a_map = _make_mapping(report_a.get("architectural_ghosts", []))
    ghosts_b_map = _make_mapping(report_b.get("architectural_ghosts", []))
    flags_a_map = _make_mapping(report_a.get("red_flags", []))
    flags_b_map = _make_mapping(report_b.get("red_flags", []))

    new_issue_keys = set(issues_b_map.keys()) - set(issues_a_map.keys())
    resolved_issue_keys = set(issues_a_map.keys()) - set(issues_b_map.keys())
    new_ghost_keys = set(ghosts_b_map.keys()) - set(ghosts_a_map.keys())
    resolved_ghost_keys = set(ghosts_a_map.keys()) - set(ghosts_b_map.keys())
    new_flag_keys = set(flags_b_map.keys()) - set(flags_a_map.keys())
    resolved_flag_keys = set(flags_a_map.keys()) - set(flags_b_map.keys())

    new_issues = sorted([issues_b_map[k] for k in new_issue_keys], key=lambda x: str(x))
    resolved_issues = sorted([issues_a_map[k] for k in resolved_issue_keys], key=lambda x: str(x))
    new_ghosts = sorted([ghosts_b_map[k] for k in new_ghost_keys], key=lambda x: str(x))
    resolved_ghosts = sorted([ghosts_a_map[k] for k in resolved_ghost_keys], key=lambda x: str(x))
    new_flags = sorted([flags_b_map[k] for k in new_flag_keys], key=lambda x: str(x))
    resolved_flags = sorted([flags_a_map[k] for k in resolved_flag_keys], key=lambda x: str(x))

    return {
        "run_a": {"id": run_id_a, "timestamp": run_a.get("timestamp")},
        "run_b": {"id": run_id_b, "timestamp": run_b.get("timestamp")},
        "vibe_score_delta": (
            report_b.get("vibe_score", 0) - report_a.get("vibe_score", 0)
        ),
        "new_issues": new_issues,
        "resolved_issues": resolved_issues,
        "new_ghosts": new_ghosts,
        "resolved_ghosts": resolved_ghosts,
        "new_flags": new_flags,
        "resolved_flags": resolved_flags,
        "metrics_comparison": {
            "files_analyzed": {
                "before": report_a.get("files_analyzed", 0),
                "after": report_b.get("files_analyzed", 0),
            },
            "total_lines": {
                "before": report_a.get("total_lines", 0),
                "after": report_b.get("total_lines", 0),
            },
            "vibe_score": {
                "before": report_a.get("vibe_score", 0),
                "after": report_b.get("vibe_score", 0),
            },
        },
    }


async def generate_knowledge_graph(
    store: Any,
    repo_path: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    """Build a knowledge graph from accumulated analysis history."""
    if not store._db_exists():
        return _empty_knowledge_graph()

    async with aiosqlite.connect(store.db_path) as db:
        db.row_factory = sqlite3.Row
        if repo_path:
            query = (
                "SELECT report_json, timestamp, vibe_score, stack "
                "FROM reports WHERE repo_path = ? "
                "ORDER BY timestamp ASC LIMIT ?"
            )
            params = (repo_path, limit)
        else:
            query = (
                "SELECT report_json, timestamp, vibe_score, stack "
                "FROM reports ORDER BY timestamp ASC LIMIT ?"
            )
            params = (limit,)

        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()

    if not rows:
        return _empty_knowledge_graph()

    issue_counts: Dict[str, int] = defaultdict(int)
    ghost_counts: Dict[str, int] = defaultdict(int)
    flag_counts: Dict[str, int] = defaultdict(int)
    coupling_instability: Dict[str, List[float]] = defaultdict(list)
    score_trend: List[Dict[str, Any]] = []
    stacks_seen: set = set()

    for row in rows:
        row_dict = dict(row)
        score_trend.append({
            "timestamp": row_dict["timestamp"],
            "vibe_score": row_dict["vibe_score"],
        })
        if row_dict.get("stack"):
            stacks_seen.add(row_dict["stack"])

        try:
            report = json.loads(row_dict.get("report_json", "{}"))
        except (json.JSONDecodeError, TypeError):
            continue

        for issue in report.get("issues", []):
            if isinstance(issue, dict):
                key = issue.get("message", json.dumps(issue, sort_keys=True))
            else:
                key = str(issue)
            issue_counts[key] += 1
        for ghost in report.get("architectural_ghosts", []):
            if isinstance(ghost, dict):
                key = ghost.get("message", json.dumps(ghost, sort_keys=True))
            else:
                key = str(ghost)
            ghost_counts[key] += 1
        for flag in report.get("red_flags", []):
            if isinstance(flag, dict):
                key = flag.get("message", json.dumps(flag, sort_keys=True))
            else:
                key = str(flag)
            flag_counts[key] += 1

        coupling = report.get("coupling_metrics", {})
        for module, metrics in coupling.items():
            if isinstance(metrics, dict):
                instability = metrics.get("instability")
                if instability is not None:
                    coupling_instability[module].append(instability)

    coupling_hotspots = []
    for module, instabilities in coupling_instability.items():
        avg = sum(instabilities) / len(instabilities)
        if avg > 0.7:
            coupling_hotspots.append({
                "module": module,
                "avg_instability": round(avg, 3),
                "occurrences": len(instabilities),
            })
    coupling_hotspots.sort(key=lambda x: x["avg_instability"], reverse=True)

    return {
        "total_runs": len(rows),
        "stacks_seen": sorted(stacks_seen),
        "score_trend": score_trend,
        "recurring_issues": _top_items(issue_counts),
        "recurring_ghosts": _top_items(ghost_counts),
        "recurring_flags": _top_items(flag_counts),
        "coupling_hotspots": coupling_hotspots[:20],
    }


def _top_items(counts: Dict[str, int], top_n: int = 20) -> List[Dict[str, Any]]:
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [
        {"item": item, "count": count}
        for item, count in sorted_items[:top_n]
    ]


def _empty_knowledge_graph() -> Dict[str, Any]:
    return {
        "total_runs": 0,
        "stacks_seen": [],
        "score_trend": [],
        "recurring_issues": [],
        "recurring_ghosts": [],
        "recurring_flags": [],
        "coupling_hotspots": [],
    }
