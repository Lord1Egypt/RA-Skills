from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[2] / "skills" / "second-brain" / "scripts"
REGISTRY_SCRIPT = SCRIPTS / "asset_index_registry.py"
QUERY_SCRIPT = SCRIPTS / "query_index.py"
ROUTINE_SCRIPT = SCRIPTS / "routine_update.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


class AssetIndexRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_module(REGISTRY_SCRIPT, "asset_index_registry")
        self.query = load_module(QUERY_SCRIPT, "query_index_registry_test")

    def make_workspace(self, base: Path, name: str, title: str, aliases: list[str]) -> tuple[Path, Path]:
        root = base / name
        repo = root / "repo"
        repo.mkdir(parents=True)
        (repo / "repo.agent.md").write_text("semantic", encoding="utf-8")
        manifest = root / ".cleanup-extracted" / "asset-manifest.jsonl"
        write_jsonl(
            manifest,
            [
                {
                    "asset_id": f"asset-{name}",
                    "title": title,
                    "asset_type": "code_project",
                    "path": "repo/repo.agent.md",
                    "source_paths": ["repo"],
                    "semantic_paths": ["repo/repo.agent.md"],
                    "semantic_formats": ["markdown"],
                    "privacy": "non_pii",
                    "retention": "keep",
                    "index_status": "final",
                }
            ],
        )
        index = root / ".cleanup-extracted" / "second-brain-asset-index" / "documents.jsonl"
        write_jsonl(
            index,
            [
                {
                    "record_id": f"asset:asset-{name}",
                    "record_type": "document",
                    "path": "repo/repo.agent.md",
                    "source_paths": ["repo"],
                    "title": title,
                    "aliases": aliases,
                    "tags": ["code", "repo"],
                    "search_terms": aliases,
                    "use_when": [f"需要定位 {title} 项目时。"],
                    "summary": f"{title} project",
                    "insights": ["build and control workflow"],
                    "key_points": ["build and control workflow"],
                    "search_text": " ".join([title, *aliases, "build control workflow"]),
                }
            ],
        )
        return root, index

    def test_upsert_and_validation_skip_stale_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root, index = self.make_workspace(base, "route-workspace", "route-planner", ["route planner", "route planning"])
            registry_path = base / "registry.json"

            entry = self.registry.upsert_asset_index(root, index, registry_path)
            valid, skipped = self.registry.valid_asset_indexes(registry_path)

            self.assertEqual(entry["workspace_label"], "route-workspace")
            self.assertEqual(len(valid), 1)
            self.assertEqual(skipped, [])

            manifest = root / ".cleanup-extracted" / "asset-manifest.jsonl"
            manifest.write_text(manifest.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            valid, skipped = self.registry.valid_asset_indexes(registry_path)

            self.assertEqual(valid, [])
            self.assertEqual(skipped[0]["reason"], "manifest_changed")

    def test_federated_auto_routes_code_query_and_keeps_generic_query_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root, index = self.make_workspace(base, "route-workspace", "route-planner", ["route planner", "route planning"])
            registry_path = base / "registry.json"
            self.registry.upsert_asset_index(root, index, registry_path)
            primary = base / "primary.jsonl"
            write_jsonl(
                primary,
                [
                    {
                        "record_id": "doc:travel",
                        "record_type": "document",
                        "path": "travel.agent.md",
                        "source_paths": ["travel.agent.md"],
                        "title": "Travel Guide",
                        "aliases": [],
                        "tags": ["life"],
                        "search_terms": ["travel guide"],
                        "use_when": ["查询旅行时使用。"],
                        "summary": "Travel planning notes.",
                        "insights": [],
                        "key_points": [],
                        "search_text": "travel guide planning",
                    }
                ],
            )

            results, routing = self.query.federated_search(
                primary,
                "route planning build control",
                asset_indexes="auto",
                registry_path=registry_path,
            )

            self.assertEqual(results[0]["title"], "route-planner")
            self.assertEqual(results[0]["origin"], "asset")
            self.assertEqual(routing["asset_reason"], "code_intent")

            generic, routing = self.query.federated_search(
                primary,
                "travel guide",
                asset_indexes="auto",
                registry_path=registry_path,
            )

            self.assertEqual(generic[0]["title"], "Travel Guide")
            self.assertEqual(routing["asset_indexes"], [])

    def test_asset_manifest_routine_registers_ready_index(self) -> None:
        routine = load_module(ROUTINE_SCRIPT, "routine_update_registry_test")
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root, index = self.make_workspace(base, "ready-workspace", "ready-project", ["ready project"])
            registry_path = base / "registry.json"

            result = routine.run_update(
                vault=root,
                out_dir=index.parent,
                log_path=base / "routine.log",
                lock_path=base / "routine.lock",
                source_mode="asset-manifest",
                use_lock=False,
                registry_path=registry_path,
            )

            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["asset_index_registry"]["workspace_label"], "ready-workspace")
            valid, skipped = self.registry.valid_asset_indexes(registry_path)
            self.assertEqual(len(valid), 1)
            self.assertEqual(skipped, [])

    def test_federated_auto_uses_semantic_rerank_when_quality_gate_requests_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root, index = self.make_workspace(base, "route-workspace", "route-planner", ["route planner", "route planning"])
            registry_path = base / "registry.json"
            self.registry.upsert_asset_index(root, index, registry_path)
            (root / ".cleanup-extracted" / "retrieval-quality-strict-top1.json").write_text(
                json.dumps({"summary": {"embedding_recommended": True}}),
                encoding="utf-8",
            )
            primary = base / "primary.jsonl"
            write_jsonl(primary, [])

            def fake_rerank(query, results, documents, **kwargs):
                output = [dict(item) for item in results]
                output[0]["semantic_score"] = 0.99
                output[0]["rerank_score"] = 1.0
                return output

            with (
                patch.object(self.query.embedding_rerank, "provider_status", return_value={"available": True, "provider": "test"}),
                patch.object(self.query.embedding_rerank, "rerank_results", side_effect=fake_rerank),
            ):
                results, routing = self.query.federated_search(
                    primary,
                    "route planning build control",
                    asset_indexes="auto",
                    registry_path=registry_path,
                    semantic_rerank="auto",
                )

            self.assertEqual(results[0]["title"], "route-planner")
            self.assertEqual(routing["semantic_rerank"]["status"], "applied")

    def test_local_semantic_search_can_rerank_quality_benchmark_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            _, index = self.make_workspace(base, "route-workspace", "route-planner", ["route planner", "route planning"])

            def fake_rerank(query, results, documents, **kwargs):
                output = [dict(item) for item in results]
                output[0]["semantic_score"] = 0.99
                output[0]["rerank_score"] = 1.0
                return output

            with (
                patch.object(self.query.embedding_rerank, "provider_status", return_value={"available": True, "provider": "test"}),
                patch.object(self.query.embedding_rerank, "rerank_results", side_effect=fake_rerank),
            ):
                results, status = self.query.search_with_semantic_rerank(index, "route planning build control", semantic_rerank="always")

            self.assertEqual(results[0]["title"], "route-planner")
            self.assertEqual(status["status"], "applied")

    def test_federated_probe_routes_capability_query_without_code_keyword(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root, index = self.make_workspace(base, "global-workspace", "global_ebr", ["global ebr"])
            write_jsonl(
                index,
                [
                    {
                        "record_id": "asset:asset-global-workspace",
                        "record_type": "document",
                        "path": "repo/repo.agent.md",
                        "source_paths": ["repo"],
                        "title": "global_ebr",
                        "aliases": ["global ebr"],
                        "tags": ["code"],
                        "search_terms": ["international semantic vector retrieval model"],
                        "use_when": ["国际化向量语义检索模型。"],
                        "summary": "International semantic vector retrieval model.",
                        "insights": [],
                        "key_points": [],
                        "search_text": "international semantic vector retrieval model",
                    }
                ],
            )
            registry_path = base / "registry.json"
            self.registry.upsert_asset_index(root, index, registry_path)
            primary = base / "primary.jsonl"
            write_jsonl(primary, [])

            results, routing = self.query.federated_search(
                primary,
                "international semantic vector retrieval",
                asset_indexes="auto",
                registry_path=registry_path,
            )

            self.assertEqual(results[0]["title"], "global_ebr")
            self.assertEqual(routing["asset_reason"], "asset_probe")


if __name__ == "__main__":
    unittest.main()
