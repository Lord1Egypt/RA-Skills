from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "second-brain"
BUILD_SCRIPT = SKILL_ROOT / "scripts" / "build_index.py"
QUERY_SCRIPT = SKILL_ROOT / "scripts" / "query_index.py"

BUILD_SPEC = importlib.util.spec_from_file_location("build_index", BUILD_SCRIPT)
assert BUILD_SPEC is not None
build_index = importlib.util.module_from_spec(BUILD_SPEC)
assert BUILD_SPEC.loader is not None
BUILD_SPEC.loader.exec_module(build_index)

QUERY_SPEC = importlib.util.spec_from_file_location("query_index", QUERY_SCRIPT)
assert QUERY_SPEC is not None
query_index = importlib.util.module_from_spec(QUERY_SPEC)
assert QUERY_SPEC.loader is not None
QUERY_SPEC.loader.exec_module(query_index)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def agent_doc(title: str = "CC Practice") -> str:
    return f"""---
id: cc-practice
doc_type: reference
title: {title}
summary: Codex 和 Claude Code 的高频工作流经验。
tags:
  - Tech
aliases:
  - CC实践
  - AI Coding
search_terms:
  - Codex context engineering
  - Claude Code workflow
use_when:
  - 需要查询 AI coding agent 的操作偏好和上下文工程经验。
skip_when:
  - 查询旅游攻略时不要使用。
version: 0.6.6
last_reviewed: 2026-05-11
---

## 摘要

- 优先用小步验证降低 agent 修改风险。
- 复杂改动应先明确验收口径。

## Details

### 工作流

正文细节。
"""


def test_agent_readable_records_use_frontmatter_and_conclusion(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "CC实践.agent.md", agent_doc())

    summary = build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )
    assert summary.total_documents == 1

    records = query_index.load_documents(out_dir / "documents.jsonl")
    assert len(records) == 1
    record = records[0]
    assert record["path"] == "CC实践.agent.md"
    assert record["title"] == "CC Practice"
    assert record["doc_type"] == "reference"
    assert record["summary"] == "Codex 和 Claude Code 的高频工作流经验。"
    assert record["aliases"] == ["CC实践", "AI Coding"]
    assert record["search_terms"] == ["Codex context engineering", "Claude Code workflow"]
    assert record["use_when"] == ["需要查询 AI coding agent 的操作偏好和上下文工程经验。"]
    assert record["skip_when"] == ["查询旅游攻略时不要使用。"]
    assert record["key_points"][:2] == [
        "优先用小步验证降低 agent 修改风险。",
        "复杂改动应先明确验收口径。",
    ]
    assert "Codex context engineering" in record["search_text"]
    assert "需要查询 AI coding agent" in record["search_text"]
    assert "旅游攻略" not in record["search_text"]


def test_legacy_conclusion_heading_still_indexes_key_points(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "legacy.agent.md", agent_doc().replace("## 摘要", "## 先给结论"))

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    records = query_index.load_documents(out_dir / "documents.jsonl")
    assert records[0]["key_points"][:2] == [
        "优先用小步验证降低 agent 修改风险。",
        "复杂改动应先明确验收口径。",
    ]


def test_summary_heading_takes_priority_over_legacy_conclusion_heading(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    doc = agent_doc().replace(
        "## 摘要\n\n- 优先用小步验证降低 agent 修改风险。\n- 复杂改动应先明确验收口径。",
        "## 先给结论\n\n- Legacy point should not win.\n\n## 摘要\n\n- New summary point wins.",
    )
    write(vault / "mixed.agent.md", doc)

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    records = query_index.load_documents(out_dir / "documents.jsonl")
    assert records[0]["key_points"][0] == "New summary point wins."


def test_agent_readable_mode_excludes_raw_archived_extracted_and_profile_docs(
    tmp_path: Path,
) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "CC实践.agent.md", agent_doc())
    write(vault / "CC实践.md", "# Raw duplicate\n\nShould not be indexed.")
    write(vault / "Archived" / "old.agent.md", agent_doc("Archived"))
    write(vault / "extracted" / "normalized" / "middle.agent.md", agent_doc("Extracted"))
    write(vault / "README.md", "# Operational doc")
    write(vault / "050 Template" / "template.agent.md", agent_doc("Template"))
    write(vault / "关于我.agent.md", agent_doc("Profile"))

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    records = query_index.load_documents(out_dir / "documents.jsonl")
    assert [record["path"] for record in records] == ["CC实践.agent.md"]


def test_privacy_and_archived_tags_are_not_indexed(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "ok.agent.md", agent_doc("Allowed"))
    write(
        vault / "secret.agent.md",
        agent_doc("Secret").replace("tags:\n  - Tech", "tags:\n  - PII"),
    )
    write(
        vault / "archived-tag.agent.md",
        agent_doc("Archived Tag").replace("tags:\n  - Tech", "tags:\n  - archived"),
    )

    summary = build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    records = query_index.load_documents(out_dir / "documents.jsonl")
    assert [record["path"] for record in records] == ["ok.agent.md"]
    assert summary.excluded_pii_documents == 1


def test_query_ranks_aliases_search_terms_and_use_when(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "CC实践.agent.md", agent_doc())
    write(vault / "产品.agent.md", agent_doc("Product").replace("Codex", "PMF"))

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    results = query_index.search(
        out_dir / "documents.jsonl",
        "AI Coding Codex workflow",
        top_k=1,
    )
    assert results[0]["path"] == "CC实践.agent.md"


def test_asset_manifest_record_merges_repo_semantic_metadata_and_aliases(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    repo = vault / "code" / "route-planner"
    repo.mkdir(parents=True)
    write(
        repo / "repo.agent.md",
        """---
title: route-planner
summary: Route planning service builds deployment packages and controls data rollout.
aliases:
  - route planner
  - route planning
search_terms:
  - route planning build control
use_when:
  - 需要定位路线规划服务的构建、部署或数据切换逻辑时。
tags:
  - code
  - route
---

## 摘要

Route planning service builds deployment packages and controls data rollout.

## Insight

- Build downloads dependencies, produces an output package, and control validates data checksums before switching data directories.
""",
    )
    manifest = vault / ".cleanup-extracted" / "asset-manifest.jsonl"
    write(
        manifest,
        json.dumps(
            {
                "asset_id": "asset-route",
                "title": "route-planner",
                "summary": "route-planner: const",
                "asset_type": "code_project",
                "source_paths": ["code/route-planner"],
                "semantic_paths": ["code/route-planner/repo.agent.md"],
                "semantic_formats": ["markdown"],
                "privacy": "non_pii",
                "retention": "keep",
                "index_status": "final",
                "search_terms": ["route-planner"],
                "insights": ["build.sh"],
            }
        )
        + "\n",
    )

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_ASSET_MANIFEST,
    )

    records = query_index.load_documents(out_dir / "documents.jsonl")
    record = records[0]
    assert "deployment packages" in record["summary"]
    assert "route planning" in record["aliases"]
    assert "route plan" in record["aliases"]
    assert "data checksums" in " ".join(record["insights"])
    results = query_index.search(out_dir / "documents.jsonl", "route planning build control", top_k=1)
    assert results[0]["title"] == "route-planner"


def test_query_prefers_specific_project_phrase_over_generic_field_name() -> None:
    documents = [
        {
            "record_id": "asset:feature",
            "record_type": "document",
            "path": "feature/repo.agent.md",
            "source_paths": ["feature"],
            "title": "feature",
            "tags": ["code"],
            "aliases": [],
            "search_terms": ["feature"],
            "use_when": ["feature service"],
            "summary": "Generic feature service.",
            "insights": [],
            "key_points": [],
            "display_snippet": "Generic feature service.",
            "excerpt": "Generic feature service.",
        },
        {
            "record_id": "asset:fepipeline",
            "record_type": "document",
            "path": "FEpipeline/repo.agent.md",
            "source_paths": ["FEpipeline"],
            "title": "FEpipeline",
            "tags": ["code"],
            "aliases": ["feature engineering pipeline"],
            "search_terms": ["Spark feature engineering", "distributed feature engineering framework"],
            "use_when": ["distributed Spark feature engineering"],
            "summary": "Scalable distributed feature engineering framework based on Spark.",
            "insights": ["Spark job framework for feature engineering."],
            "key_points": [],
            "display_snippet": "Scalable distributed feature engineering framework based on Spark.",
            "excerpt": "Scalable distributed feature engineering framework based on Spark.",
        },
    ]

    results = query_index.search_documents(documents, "scalable distributed Spark feature engineering framework", top_k=1)

    assert results[0]["title"] == "FEpipeline"


def test_manifest_is_compact_incremental_state(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "CC实践.agent.md", agent_doc())

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == build_index.MANIFEST_SCHEMA_VERSION
    assert "index_version" not in manifest
    assert manifest["source_mode"] == build_index.SOURCE_MODE_AGENT_READABLE
    source = manifest["sources"]["CC实践.agent.md"]
    assert source == {
        "size": source["size"],
        "mtime_ns": source["mtime_ns"],
        "sha256": source["sha256"],
    }
    for removed_key in [
        "path",
        "tags",
        "pii_status",
        "record_ids",
        "group_id",
        "source_mode",
        "summary_mode",
        "extractor_version",
        "summary_version",
    ]:
        assert removed_key not in source


def test_old_manifest_schema_is_reused_and_migrated(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "CC实践.agent.md", agent_doc())

    first = build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )
    assert first.indexed_documents == 1

    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source = manifest["sources"]["CC实践.agent.md"]
    old_manifest = {
        "schema_version": build_index.DOCUMENT_SCHEMA_VERSION,
        "index_version": build_index.DOCUMENT_SCHEMA_VERSION,
        "extractor_version": build_index.EXTRACTOR_VERSION,
        "summary_version": build_index.SUMMARY_VERSION,
        "source_mode": build_index.SOURCE_MODE_AGENT_READABLE,
        "sources": {
            "CC实践.agent.md": {
                **source,
                "path": "CC实践.agent.md",
                "tags": ["Tech"],
                "pii_status": "allowed",
                "record_ids": ["doc:CC实践.agent.md"],
                "group_id": None,
                "source_mode": build_index.SOURCE_MODE_AGENT_READABLE,
                "summary_mode": build_index.current_summary_mode(),
                "extractor_version": build_index.EXTRACTOR_VERSION,
                "summary_version": build_index.SUMMARY_VERSION,
            }
        },
        "groups": {},
        "excluded_pii_paths": [],
        "summary": first.as_dict(),
    }
    manifest_path.write_text(json.dumps(old_manifest, ensure_ascii=False), encoding="utf-8")

    second = build_index.build_index(
        vault,
        out_dir,
        force=False,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )

    assert second.indexed_documents == 0
    assert second.reused_documents == 1
    migrated = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert migrated["schema_version"] == build_index.MANIFEST_SCHEMA_VERSION
    assert set(migrated["sources"]["CC实践.agent.md"]) == {"size", "mtime_ns", "sha256"}


def test_source_mode_change_invalidates_reuse(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    out_dir = tmp_path / "generated"
    write(vault / "CC实践.agent.md", agent_doc())

    build_index.build_index(
        vault,
        out_dir,
        force=True,
        source_mode=build_index.SOURCE_MODE_AGENT_READABLE,
    )
    second = build_index.build_index(
        vault,
        out_dir,
        force=False,
        source_mode=build_index.SOURCE_MODE_ALL_MARKDOWN,
    )

    assert second.indexed_documents == 1
    assert second.reused_documents == 0


def test_local_fallback_summary_requires_explicit_remote_opt_in(monkeypatch) -> None:
    record = {"source_fingerprints": {"summary_provider": "local-fallback"}}

    monkeypatch.delenv("SECOND_BRAIN_SUMMARY_ENABLED", raising=False)
    monkeypatch.delenv("SECOND_BRAIN_SUMMARY_API_KEY", raising=False)
    monkeypatch.delenv("SECOND_BRAIN_SUMMARY_BASE_URL", raising=False)
    monkeypatch.delenv("SECOND_BRAIN_SUMMARY_MODEL", raising=False)
    assert build_index.summary_reusable(record)

    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "general-key-must-not-be-consumed")
    assert build_index.summary_reusable(record)

    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_ENABLED", "1")
    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_API_KEY", "test-key")
    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_MODEL", "test-model")
    assert not build_index.summary_reusable(record)
