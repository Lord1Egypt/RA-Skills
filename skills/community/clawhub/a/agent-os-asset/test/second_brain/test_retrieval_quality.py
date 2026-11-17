from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "second-brain"
    / "scripts"
    / "retrieval_quality.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("retrieval_quality", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def test_quality_report_requires_strict_top_one_and_recommends_embedding(tmp_path: Path) -> None:
    quality = load_module()
    index = tmp_path / "documents.jsonl"
    write_jsonl(
        index,
        [
            {
                "record_id": "asset:planner",
                "record_type": "document",
                "path": "route-planner/repo.agent.md",
                "source_paths": ["route-planner"],
                "title": "route-planner",
                "aliases": ["route planner", "route planning"],
                "tags": ["code"],
                "search_terms": ["route planning build control"],
                "use_when": ["路线规划服务构建部署"],
                "summary": "Route planning service.",
                "insights": ["build and control"],
                "key_points": [],
                "search_text": "route planner route planning build control",
            },
            {
                "record_id": "asset:feature",
                "record_type": "document",
                "path": "route-feature/repo.agent.md",
                "source_paths": ["route-feature"],
                "title": "route-feature",
                "aliases": ["route feature"],
                "tags": ["code"],
                "search_terms": ["route feature"],
                "use_when": ["路线特征"],
                "summary": "Route feature service.",
                "insights": [],
                "key_points": [],
                "search_text": "route feature",
            },
        ],
    )
    benchmark = {
        "schema_version": 1,
        "queries": [
            {"id": "planner", "query": "route planning build control", "expected_title": "route-planner", "strict": True},
            {"id": "wrong", "query": "route feature", "expected_title": "route-planner", "strict": True},
        ],
    }

    report = quality.evaluate(index, benchmark)

    assert report["summary"]["strict_total"] == 2
    assert report["summary"]["strict_top1"] == 1
    assert report["summary"]["strict_top1_passed"] is False
    assert report["summary"]["embedding_recommended"] is True


def test_quality_report_records_semantic_rerank_status(monkeypatch, tmp_path: Path) -> None:
    quality = load_module()
    index = tmp_path / "documents.jsonl"
    write_jsonl(
        index,
        [
            {
                "record_id": "asset:planner",
                "record_type": "document",
                "path": "route-planner/repo.agent.md",
                "source_paths": ["route-planner"],
                "title": "route-planner",
                "aliases": ["route planner"],
                "tags": ["code"],
                "search_terms": ["route planning"],
                "use_when": [],
                "summary": "Route planning service.",
                "insights": [],
                "key_points": [],
                "search_text": "route planning service",
            }
        ],
    )
    monkeypatch.setattr(
        quality.query_index,
        "search_with_semantic_rerank",
        lambda *args, **kwargs: ([{"record_id": "asset:planner", "title": "route-planner", "path": "route-planner/repo.agent.md", "score": 1}], {"status": "applied"}),
    )

    report = quality.evaluate(
        index,
        {"queries": [{"query": "route planning", "expected_title": "route-planner", "strict": True}]},
        semantic_rerank="always",
    )

    assert report["summary"]["strict_top1_passed"] is True
    assert report["summary"]["semantic_rerank_statuses"] == ["applied"]
