from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_ROOT / "scripts" / "mixed_folder_adapter.py"


def load_module():
    spec = importlib.util.spec_from_file_location("mixed_folder_adapter", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MixedFolderAdapterTest(unittest.TestCase):
    def test_public_nested_child_scripts_remain_resolvable(self) -> None:
        adapter = load_module()
        child_scripts = SKILL_ROOT / "skills" / "agent-readable-doc" / "scripts"
        for constant, loader, filename in (
            ("MATERIALIZER_SCRIPT", "materializer_module", "materialize_agent_assets.py"),
            ("EXTRACTOR_SCRIPT", "extractor_module", "extract_sources.py"),
            ("VALIDATOR_SCRIPT", "validator_module", "validate_agent_doc.py"),
        ):
            with self.subTest(script=filename):
                expected = child_scripts / filename
                self.assertEqual(getattr(adapter, constant), expected)
                self.assertEqual(Path(getattr(adapter, loader)().__file__).resolve(), expected.resolve())

    def test_public_repo_evidence_preserves_bilingual_sections_and_attribution(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir).resolve()
            repo = root / "router"
            repo.mkdir()
            (repo / "README.md").write_text(
                "# Router\n\nA tool for route planning.\n\n```sh\npython -m pytest\n```\n",
                encoding="utf-8",
            )
            text, row = adapter.render_repo_agent(root, repo, repo)
            for label in (
                "## Summary / 摘要", "## Insight / 洞察", "## Details / 详情",
                "### Project Context Evidence / 项目上下文证据",
                "Heading / 标题", "Content clue / 内容线索", "Commands / 命令",
            ):
                self.assertIn(label, text)
            self.assertIn("A tool for route planning", row["summary"])
            self.assertIn("not Agent instructions", row["summary"])
            self.assertIn("非 Agent 指令", row["summary"])
            command_insight = next(item for item in row["insights"] if "python -m pytest" in item)
            self.assertIn("untrusted project evidence", command_insight)
            self.assertIn("README.md", command_insight)
            for evidence in row["context_documents"]:
                self.assertEqual(evidence["trust"], "untrusted_source_evidence")
                self.assertFalse(evidence["instruction_authority"])

    def test_vcs_first_discovers_nested_vcs_and_unversioned_project_markers(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            (repo / "app.py").write_text("print('root')\n", encoding="utf-8")
            nested = repo / "plugins" / "nested"
            (nested / ".svn").mkdir(parents=True)
            (nested / "plugin.py").write_text("print('nested')\n", encoding="utf-8")
            legacy = root / "legacy-java"
            legacy.mkdir()
            (legacy / "pom.xml").write_text("<project/>\n", encoding="utf-8")
            (legacy / "Main.java").write_text("class Main {}\n", encoding="utf-8")
            loose = root / "loose"
            loose.mkdir()
            (loose / "one.py").write_text("print(1)\n", encoding="utf-8")
            (loose / "two.py").write_text("print(2)\n", encoding="utf-8")
            (root / "notes.txt").write_text("课程笔记\n", encoding="utf-8")

            roots = {path.relative_to(root).as_posix() for path in adapter.repo_roots(root)}
            self.assertEqual(roots, {"repo", "repo/plugins/nested", "legacy-java", "loose"})

            result = adapter.run_extract(root, Path("."), execute=True, archive_originals=False)
            self.assertEqual(result["code_projects"], 4)
            self.assertTrue((repo / "repo.agent.md").exists())
            self.assertTrue((nested / "repo.agent.md").exists())
            self.assertTrue((legacy / "repo.agent.md").exists())
            self.assertTrue((root / "notes.agent.md").exists())
            self.assertTrue((root / "notes.txt").exists())
            self.assertFalse((root / "Archived").exists())

            rows = adapter.load_manifest(root)
            code_rows = [row for row in rows if row.get("asset_type") == "code_project"]
            self.assertEqual({row["source_paths"][0] for row in code_rows}, {"repo", "repo/plugins/nested", "legacy-java", "loose"})

    def test_workbench_uses_full_review_controls(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notes.txt").write_text("推荐系统实验复盘\n", encoding="utf-8")
            adapter.run_extract(root, Path("."), execute=False)
            result = adapter.run_workbench(root, Path("."))
            html = (root / result["workbench"]).read_text(encoding="utf-8")

            for expected in (
                "Search title/path/summary/insight",
                "全选",
                "反选",
                "清空选择",
                "应用到已选",
                "下载 decisions.json",
                "下载并复制命令",
                "复制 open 命令",
                "asset-data",
            ):
                self.assertIn(expected, html)

    def test_collect_files_skips_external_symlinks(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "workspace"
            root.mkdir()
            outside = Path(temp_dir) / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            (root / "notes.txt").write_text("inside", encoding="utf-8")
            (root / "external-link.txt").symlink_to(outside)

            paths = {path.name for path in adapter.collect_files(root, root, [])}

            self.assertEqual(paths, {"notes.txt"})

    def test_pdf_uses_bounded_sample_without_full_ocr(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "slides.pdf").write_bytes(b"%PDF-1.4\nnot a real PDF\n")
            with patch.object(adapter, "sample_pdf_text", return_value="sampled embedded text"):
                with patch.object(adapter, "extractor_module", side_effect=AssertionError("full extractor must not run for PDF")):
                    result = adapter.run_extract(root, Path("."), execute=True, archive_originals=False)

            self.assertEqual(result["converted"], 1)
            row = adapter.load_manifest(root)[0]
            self.assertTrue(row["sampled_only"])
            self.assertEqual(row["extraction_policy"], "bounded embedded PDF text sample; OCR deferred")
            self.assertTrue((root / "slides.agent.md").exists())

    def test_corrupt_structured_document_falls_back_to_metadata(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "broken.pptx").write_bytes(b"not a zip archive")

            result = adapter.run_extract(root, Path("."), execute=True, archive_originals=False)

            self.assertEqual(result["converted"], 1)
            row = adapter.load_manifest(root)[0]
            self.assertEqual(row["fidelity"], "metadata_only")
            self.assertIn("Invalid Office archive", row["extraction_warning"])
            self.assertTrue((root / "broken.agent.md").exists())

    def test_directory_fingerprint_is_bounded(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for index in range(adapter.DIRECTORY_FINGERPRINT_MAX_FILES + 5):
                (root / f"file-{index:04d}.txt").write_text("x", encoding="utf-8")

            value = adapter.fingerprint(root)

            self.assertTrue(value["fingerprint_sampled"])
            self.assertEqual(value["fingerprint_files_seen"], adapter.DIRECTORY_FINGERPRINT_MAX_FILES)

    def test_project_discovery_uses_scope_relative_sensitive_matching(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "workspace-holder"
            (root / "repo" / ".git").mkdir(parents=True)
            (root / "repo" / "app.py").write_text("print('ok')\n", encoding="utf-8")

            roots = adapter.repo_roots(root)

            self.assertEqual([item.relative_to(root).as_posix() for item in roots], ["repo"])

    def test_project_discovery_skips_dependency_and_generated_marker_roots(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "legacy" / "pom.xml").parent.mkdir(parents=True)
            (root / "legacy" / "pom.xml").write_text("<project/>", encoding="utf-8")
            (root / "env39" / "site-packages" / "package" / "setup.py").parent.mkdir(parents=True)
            (root / "env39" / "site-packages" / "package" / "setup.py").write_text("", encoding="utf-8")
            (root / "vendor" / "package" / "package.json").parent.mkdir(parents=True)
            (root / "vendor" / "package" / "package.json").write_text("{}", encoding="utf-8")
            (root / "var" / "generated" / "pyproject.toml").parent.mkdir(parents=True)
            (root / "var" / "generated" / "pyproject.toml").write_text("", encoding="utf-8")

            roots = adapter.repo_roots(root)

            self.assertEqual([item.relative_to(root).as_posix() for item in roots], ["legacy"])

    def test_unmarked_code_directory_becomes_one_project_asset(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            code_root = root / "course" / "code" / "Ch02"
            code_root.mkdir(parents=True)
            (code_root / "kNN.py").write_text("print('code')\n", encoding="utf-8")
            (code_root / "helper.py").write_text("print('helper')\n", encoding="utf-8")
            (root / "course" / "notes.txt").write_text("keep as document", encoding="utf-8")

            result = adapter.run_inventory(root, Path("."))
            rows = adapter.load_manifest(root)

            self.assertEqual(result["code_projects"], 1)
            project = next(row for row in rows if row["asset_type"] == "code_project")
            self.assertEqual(project["source_paths"], ["course/code"])
            self.assertFalse(any(row.get("source_paths") == ["course/code/Ch02/kNN.py"] for row in rows))
            self.assertTrue(any(row.get("source_paths") == ["course/notes.txt"] for row in rows))

    def test_unmarked_code_parent_becomes_project_when_no_code_named_ancestor_exists(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter = root / "course" / "Chapter10_利用PCA来简化数据"
            chapter.mkdir(parents=True)
            (chapter / "pca.py").write_text("print('pca')\n", encoding="utf-8")

            adapter.run_inventory(root, Path("."))
            rows = adapter.load_manifest(root)

            self.assertEqual([row["asset_type"] for row in rows], ["code_project"])
            self.assertEqual(rows[0]["source_paths"], ["course/Chapter10_利用PCA来简化数据"])

    def test_directory_projects_treats_each_top_level_directory_as_a_project(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notebooks" / "experiment.ipynb").parent.mkdir(parents=True)
            (root / "notebooks" / "experiment.ipynb").write_text("{}", encoding="utf-8")
            (root / "legacy-data" / "dataset.csv").parent.mkdir(parents=True)
            (root / "legacy-data" / "dataset.csv").write_text("a,b\n1,2\n", encoding="utf-8")
            (root / "root-note.txt").write_text("root document", encoding="utf-8")

            roots = adapter.repo_roots(root, "directory-projects")
            files = adapter.collect_files(root, root, roots)

            self.assertEqual({item.relative_to(root).as_posix() for item in roots}, {"notebooks", "legacy-data"})
            self.assertEqual({item.relative_to(root).as_posix() for item in files}, {"root-note.txt"})

    def test_directory_projects_rehydrates_existing_repo_agent_roots(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "collection" / "legacy-project"
            nested.mkdir(parents=True)
            (nested / "repo.agent.md").write_text("old semantic entry", encoding="utf-8")
            (nested / "run.py").write_text("# run importer\n", encoding="utf-8")

            roots = adapter.repo_roots(root, "directory-projects")

            self.assertIn("collection", {item.relative_to(root).as_posix() for item in roots})
            self.assertIn("collection/legacy-project", {item.relative_to(root).as_posix() for item in roots})

    def test_directory_projects_does_not_materialize_loose_source_files(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "project" / "main.py").parent.mkdir(parents=True)
            (root / "project" / "main.py").write_text("print('project')\n", encoding="utf-8")
            (root / "__init__.py").write_text("", encoding="utf-8")

            result = adapter.run_extract(
                root,
                Path("."),
                execute=True,
                archive_originals=False,
                discovery_mode="directory-projects",
            )

            self.assertEqual(result["code_projects"], 1)
            self.assertEqual(result["converted"], 0)
            self.assertFalse((root / "__init__.agent.md").exists())

    def test_collect_files_prunes_project_roots_before_file_walk(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            for index in range(20):
                (repo / f"source-{index}.py").write_text("print('x')\n", encoding="utf-8")
            (root / "notes.txt").write_text("outside project", encoding="utf-8")

            with patch.object(adapter, "in_scope", side_effect=AssertionError("per-file scope checks are too expensive")):
                paths = {item.relative_to(root).as_posix() for item in adapter.collect_files(root, root, adapter.repo_roots(root))}

            self.assertEqual(paths, {"notes.txt"})

    def test_inventory_collapses_data_directory_into_metadata_bundle(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bundle = root / "course" / "trainingDigits"
            bundle.mkdir(parents=True)
            for index in range(4):
                (bundle / f"0_{index}.txt").write_text("0" * 32 + "\n", encoding="utf-8")
            (bundle.parent / "kNN.py").write_text("print('code')\n", encoding="utf-8")
            (bundle.parent / "README.txt").write_text("digit classifier example\n", encoding="utf-8")

            result = adapter.run_inventory(root, Path("."))
            rows = adapter.load_manifest(root)

            self.assertEqual(result["assets"], 2)
            self.assertEqual(result["code_projects"], 1)
            data_rows = [row for row in rows if row["asset_type"] == "data_bundle"]
            self.assertEqual(len(data_rows), 1)
            row = data_rows[0]
            self.assertEqual(row["member_count"], 4)
            self.assertEqual(row["bundle_root"], "course/trainingDigits")
            self.assertEqual(row["semantic_paths"], [])
            self.assertTrue((root / row["member_ledger_path"]).exists())
            self.assertFalse(any(row.get("source_paths") == [f"course/trainingDigits/0_{index}.txt"] for row in rows for index in range(4)))

    def test_inventory_groups_loose_data_files_by_nearest_parent(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            parent = root / "chapter" / "Ch02"
            parent.mkdir(parents=True)
            (parent / "datingTestSet.txt").write_text("1\t2\t3\n", encoding="utf-8")
            (parent / "testSet.txt").write_text("4\t5\t6\n", encoding="utf-8")
            (parent / "digits.zip").write_bytes(b"PK")
            (parent / "figure.png").write_bytes(b"\x89PNG\r\n")
            (parent / "kNN.py").write_text("print('code')\n", encoding="utf-8")

            adapter.run_inventory(root, Path("."))
            rows = adapter.load_manifest(root)

            data_rows = [row for row in rows if row["asset_type"] == "data_bundle"]
            self.assertEqual(len(data_rows), 1)
            row = data_rows[0]
            self.assertEqual(row["bundle_kind"], "loose_parent")
            self.assertEqual(row["bundle_root"], "chapter/Ch02")
            ledger = adapter.load_json(root / row["member_ledger_path"], {})
            self.assertEqual(set(ledger["member_paths"]), {"chapter/Ch02/datingTestSet.txt", "chapter/Ch02/testSet.txt", "chapter/Ch02/digits.zip"})
            self.assertNotIn("chapter/Ch02/figure.png", ledger["member_paths"])
            self.assertNotIn("chapter/Ch02/kNN.py", ledger["member_paths"])

    def test_data_bundle_delete_trashes_members_not_parent_directory(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bundle = root / "data" / "samples"
            bundle.mkdir(parents=True)
            members = [bundle / "train_0.txt", bundle / "train_1.txt"]
            for member in members:
                member.write_text("sample", encoding="utf-8")
            (bundle.parent / "train.py").write_text("print('keep code')\n", encoding="utf-8")
            adapter.run_inventory(root, Path("."))
            row = next(item for item in adapter.load_manifest(root) if item["asset_type"] == "data_bundle")
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({"scope": ".", "decisions": [{"asset_id": row["asset_id"], "decision": "delete", "pii_label": "non_pii"}]}), encoding="utf-8")
            moved: list[str] = []

            def fake_trash(path: Path):
                moved.append(path.resolve().relative_to(root.resolve()).as_posix())
                return {"status": "trashed", "method": "test", "path": path.as_posix()}

            with patch.object(adapter, "move_to_trash", side_effect=fake_trash):
                result = adapter.run_apply(root, Path("."), decisions, execute=True)

            self.assertEqual(set(moved), {"data/samples/train_0.txt", "data/samples/train_1.txt"})
            self.assertTrue((bundle.parent / "train.py").exists())
            self.assertTrue(bundle.exists())
            actions = result["delete_assets"][0]["path_actions"]
            self.assertTrue(all(action["role"] == "member" for action in actions))

    def test_sync_refreshes_data_bundle_without_member_agent_files(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bundle = root / "course" / "trainingDigits"
            bundle.mkdir(parents=True)
            (bundle / "0_0.txt").write_text("0" * 32 + "\n", encoding="utf-8")
            (bundle / "0_1.txt").write_text("0" * 32 + "\n", encoding="utf-8")
            adapter.run_inventory(root, Path("."))

            (bundle / "1_0.txt").write_text("1" * 32 + "\n", encoding="utf-8")
            result = adapter.run_sync(root, Path("."), execute=True)

            self.assertEqual(result["modified"], 1)
            self.assertFalse((bundle.with_suffix(".agent.md")).exists())
            row = next(item for item in adapter.load_manifest(root) if item["asset_type"] == "data_bundle")
            self.assertEqual(row["member_count"], 3)
            self.assertEqual(row["sync_status"], "source_modified")
            self.assertEqual(adapter.run_sync(root, Path("."), execute=True)["modified"], 0)

    def test_sync_adds_data_bundle_without_member_agent_files(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter.run_inventory(root, Path("."))
            bundle = root / "datasets" / "mnist"
            bundle.mkdir(parents=True)
            (bundle / "train_0.txt").write_text("0" * 32 + "\n", encoding="utf-8")
            (bundle / "train_1.txt").write_text("1" * 32 + "\n", encoding="utf-8")

            result = adapter.run_sync(root, Path("."), execute=True)

            self.assertEqual(result["added"], 1)
            self.assertTrue((bundle / "train_0.txt").exists())
            self.assertFalse((bundle / "train_0.agent.md").exists())
            rows = adapter.load_manifest(root)
            self.assertEqual([row["asset_type"] for row in rows], ["data_bundle"])

    def test_audit_ignores_missing_source_for_successfully_deleted_asset(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter.write_scope_manifest(
                root,
                root,
                [
                    {
                        "asset_id": "asset-deleted",
                        "title": "Deleted",
                        "asset_type": "document",
                        "source_paths": ["already-gone.txt"],
                        "semantic_paths": [],
                        "semantic_formats": [],
                        "privacy": "non_pii",
                        "retention": "delete",
                        "index_status": "excluded",
                        "delete_status": "deleted",
                    }
                ],
            )

            result = adapter.run_audit(root, Path("."))

            self.assertEqual(result["missing_source"], [])
            self.assertTrue(result["summary"]["ready_for_scope_index"])

    def test_code_summary_uses_bounded_project_file_sample(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            for index in range(adapter.PROJECT_SUMMARY_MAX_FILES + 5):
                (repo / f"source-{index:04d}.py").write_text("print('x')\n", encoding="utf-8")

            summary, _, row = adapter.code_summary(root, repo, repo, nested_projects=[])

            self.assertIn("采样", summary)
            self.assertEqual(row["sampled_files"], adapter.PROJECT_SUMMARY_MAX_FILES)
            self.assertTrue(row["sampled_only"])

    def test_notebook_counts_as_project_code_not_data_asset(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "notebook-project"
            (repo / ".git").mkdir(parents=True)
            (repo / "experiment.ipynb").write_text('{"cells": []}\n', encoding="utf-8")

            summary, _, row = adapter.code_summary(root, repo, repo, nested_projects=[])

            self.assertIn("ipynb(1)", summary)
            self.assertEqual(row["asset_type"], "code_project")

    def test_kb_review_keeps_project_with_readme_and_agent_context(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "route-service"
            (repo / ".git").mkdir(parents=True)
            (repo / "README.md").write_text("# Route Service\n\nProject-specific route ranking experiments.\n", encoding="utf-8")
            (repo / "AGENTS.md").write_text("# Local workflow\n\nRun integration checks before deployment.\n", encoding="utf-8")
            (repo / "main.py").write_text("print('service')\n", encoding="utf-8")

            _, _, row = adapter.code_summary(root, repo, repo, nested_projects=[])
            suggestion = adapter.suggest_asset_decision(root, row)

            self.assertEqual(suggestion["decision"], "keep")
            self.assertEqual(suggestion["confidence"], "high")
            self.assertIn("README.md", " ".join(suggestion["signals"]))
            self.assertIn("AGENTS.md", " ".join(suggestion["signals"]))

    def test_project_context_skips_image_markdown_when_selecting_heading(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "project"
            repo.mkdir()
            (repo / "README.md").write_text("![logo](logo.png)\n# Useful Project [![badge](badge.png)](https://example.com)\n\nContext.\n", encoding="utf-8")

            context = adapter.project_context_documents(root, repo)

            self.assertEqual(context[0]["heading"], "Useful Project")

    def test_context_evidence_strips_markdown_emphasis(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "project"
            repo.mkdir()
            (repo / "README.md").write_text("# Project\n\nA _local assistant_ for teams.\n", encoding="utf-8")

            context = adapter.project_context_documents(root, repo)

            self.assertEqual(context[0]["summary"], "A local assistant for teams.")

    def test_claude_md_is_project_agent_context(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "project"
            repo.mkdir()
            (repo / "CLAUDE.md").write_text("# Project Rules\n\n- Run unit tests before release.\n", encoding="utf-8")

            context = adapter.project_context_documents(root, repo)

            self.assertEqual(context[0]["kind"], "agents")
            self.assertIn("Run unit tests", " ".join(context[0]["highlights"]))

    def test_root_package_manifest_fallback_shapes_repo_semantics(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "batch-tool"
            repo.mkdir()
            (repo / "package.json").write_text(
                json.dumps(
                    {
                        "name": "batch-tool",
                        "description": "Processes queued jobs and publishes a report.",
                        "scripts": {"test": "node test.js", "start": "node main.js"},
                    }
                ),
                encoding="utf-8",
            )
            (repo / "main.js").write_text("console.log('run');\n", encoding="utf-8")

            summary, insights, row = adapter.code_summary(root, repo, repo, nested_projects=[])
            text, _ = adapter.render_repo_agent(root, repo, repo, nested_projects=[])
            suggestion = adapter.suggest_asset_decision(root, row)

            self.assertIn("Processes queued jobs", summary)
            self.assertIn("根目录入口/构建线索", "\n".join(insights))
            self.assertIn("npm run test", text)
            self.assertIn("entry", {item["kind"] for item in row["context_documents"]})
            self.assertEqual(suggestion["decision"], "review")
            self.assertEqual(suggestion["confidence"], "medium")

    def test_root_entry_candidates_include_pom_script_and_main(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "legacy"
            repo.mkdir()
            (repo / "pom.xml").write_text("<project><artifactId>legacy-app</artifactId><description>Legacy batch app</description></project>", encoding="utf-8")
            (repo / "run.sh").write_text("#!/bin/sh\n# Run the batch importer\npython main.py\n", encoding="utf-8")
            (repo / "main.py").write_text('"""Import data into the local index."""\n', encoding="utf-8")

            names = [path.name for path in adapter.root_entry_candidates(root, repo)]

            self.assertIn("pom.xml", names)
            self.assertIn("run.sh", names)
            self.assertIn("main.py", names)

    def test_root_entry_build_semantics_ignore_const_and_preserve_deployment_purpose(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "route-planner"
            repo.mkdir()
            (repo / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 2.6)\nproject(route-plan)\n", encoding="utf-8")
            (repo / "build.sh").write_text(
                "#!/bin/bash\n## const\n# 拉取依赖包编译\n# 构建部署包output\n",
                encoding="utf-8",
            )
            (repo / "control.sh").write_text("#!/bin/bash\n# 校验数据 md5 后切换数据目录\n", encoding="utf-8")
            (repo / "main.py").write_text("print('route')\n", encoding="utf-8")

            summary, _, row = adapter.code_summary(root, repo, repo, nested_projects=[])

            self.assertNotIn("：const", summary)
            self.assertIn("拉取依赖包编译", summary)
            self.assertIn("route planning", row["aliases"])
            self.assertNotIn("#构建部署包", row["aliases"])

    def test_retrieval_refresh_rewrites_weak_repo_entry_without_changing_keep_state(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "route-planner"
            repo.mkdir()
            (repo / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 2.6)\nproject(route-plan)\n", encoding="utf-8")
            (repo / "build.sh").write_text("#!/bin/bash\n# 拉取依赖包编译\n# 构建部署包output\n", encoding="utf-8")
            semantic = repo / "repo.agent.md"
            semantic.write_text("---\ntitle: route-planner\nsummary: route-planner：const\n---\n\n## 摘要\n\nroute-planner：const\n", encoding="utf-8")
            row = {
                "asset_id": "asset-route",
                "title": "route-planner",
                "summary": "route-planner：const",
                "asset_type": "code_project",
                "path": "route-planner/repo.agent.md",
                "source_paths": ["route-planner"],
                "semantic_paths": ["route-planner/repo.agent.md"],
                "semantic_formats": ["markdown"],
                "privacy": "non_pii",
                "retention": "keep",
                "index_status": "final",
                "search_terms": ["route-planner"],
                "insights": [],
            }
            adapter.write_scope_manifest(root, root, [row])

            result = adapter.run_retrieval_refresh(root, Path("."), execute=True)
            refreshed = adapter.load_manifest(root)[0]

            self.assertEqual(result["refreshed"], 1)
            self.assertEqual(refreshed["retention"], "keep")
            self.assertEqual(refreshed["index_status"], "final")
            self.assertIn("route planning", refreshed["aliases"])
            self.assertIn("拉取依赖包编译", semantic.read_text(encoding="utf-8"))
            self.assertTrue((root / ".cleanup-extracted" / "retrieval-refresh-backups").exists())

    def test_repo_semantic_uses_readme_agents_and_docs_body_evidence(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "media-pipeline"
            (repo / ".git").mkdir(parents=True)
            (repo / "README.md").write_text(
                "# Media Pipeline\n\n"
                "A local CLI converts long-form audio and articles into searchable summaries. "
                "It also publishes timeline reports.\n\n"
                "## Features\n\n"
                "- Download media, transcribe it, and publish structured Markdown.\n",
                encoding="utf-8",
            )
            (repo / "AGENTS.md").write_text(
                "# Development Rules\n\n"
                "- Run targeted pytest before changing the CLI.\n"
                "- Update README.md when command behavior changes.\n",
                encoding="utf-8",
            )
            (repo / "docs").mkdir()
            (repo / "docs" / "architecture.md").write_text(
                "---\nsummary: generated metadata that is not the document body\n---\n\n# Architecture\n\n"
                "Workers separate ingestion, transcription, and summary publication.\n",
                encoding="utf-8",
            )
            (repo / "main.py").write_text("print('ok')\n", encoding="utf-8")

            summary, insights, row = adapter.code_summary(root, repo, repo, nested_projects=[])
            text, _ = adapter.render_repo_agent(root, repo, repo, nested_projects=[])

            self.assertIn("converts long-form audio", summary)
            self.assertNotIn("It also publishes timeline reports", summary)
            self.assertIn("Run targeted pytest", "\n".join(insights))
            self.assertIn("Workers separate ingestion", text)
            self.assertNotIn("generated metadata that is not the document body", text)
            self.assertIn("README.md", " ".join(item["path"] for item in row["context_documents"]))
            self.assertIn("agents", {item["kind"] for item in row["context_documents"]})
            self.assertIn("docs", {item["kind"] for item in row["context_documents"]})

    def test_kb_review_archives_dependency_bundle_without_project_context(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "third-64" / "library"
            repo.mkdir(parents=True)
            (repo / "lib.cpp").write_text("int main() { return 0; }\n", encoding="utf-8")

            _, _, row = adapter.code_summary(root, repo, repo, nested_projects=[])
            suggestion = adapter.suggest_asset_decision(root, row)

            self.assertEqual(suggestion["decision"], "archive_only")
            self.assertEqual(suggestion["confidence"], "medium")

    def test_kb_review_marks_undocumented_project_for_review(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "unknown-project"
            repo.mkdir(parents=True)
            (repo / "main.py").write_text("print('unknown')\n", encoding="utf-8")

            _, _, row = adapter.code_summary(root, repo, repo, nested_projects=[])
            suggestion = adapter.suggest_asset_decision(root, row)

            self.assertEqual(suggestion["decision"], "review")
            self.assertEqual(suggestion["confidence"], "medium")

    def test_extract_archives_sources_and_skips_sensitive_paths(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notes.txt").write_text("推荐系统实验复盘\n", encoding="utf-8")
            (root / "resume.txt").write_text("must not read", encoding="utf-8")
            repo = root / "code"
            repo.mkdir()
            (repo / ".git").mkdir()
            (repo / "app.py").write_text("print('hello')\n", encoding="utf-8")
            (repo / "worker.py").write_text("print('worker')\n", encoding="utf-8")
            (repo / "job.sh").write_text("echo job\n", encoding="utf-8")

            result = adapter.run_extract(root=root, scope=Path("."), execute=True)

            self.assertEqual(result["converted"], 1)
            self.assertEqual(result["code_projects"], 1)
            self.assertEqual(result["skipped_sensitive"], 1)
            self.assertTrue((root / "notes.agent.md").exists())
            self.assertTrue((root / "code" / "repo.agent.md").exists())
            self.assertTrue((root / "Archived" / "notes.txt").exists())
            self.assertTrue((root / "Archived" / "code" / "app.py").exists())
            self.assertTrue((root / "resume.txt").exists())
            self.assertFalse((root / "resume.agent.md").exists())

            rows = adapter.load_manifest(root)
            note = next(row for row in rows if row["title"] == "notes")
            exported = root / "asset-decisions.json"
            exported.write_text(
                json.dumps(
                    {
                        "scope": ".",
                        "decisions": [
                            {
                                "asset_id": note["asset_id"],
                                "decision": "keep",
                                "asset_mode": "keep",
                                "pii_label": "non_pii",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            applied = adapter.run_apply(root, Path("."), exported, execute=True)
            self.assertEqual(applied["applied"], 1)
            updated = next(row for row in adapter.load_manifest(root) if row["asset_id"] == note["asset_id"])
            self.assertEqual(updated["index_status"], "final")
            self.assertIn(note["asset_id"], adapter.load_json(adapter.decision_path(root), {"assets": {}})["assets"])

            archived_code = root / "Archived" / "code" / "a.py"
            archived_code.write_text("print('changed')\n", encoding="utf-8")
            code_synced = adapter.run_sync(root, Path("."), execute=True)
            self.assertEqual(code_synced["modified"], 1)
            code_row = next(row for row in adapter.load_manifest(root) if row["asset_type"] == "code_project")
            self.assertEqual(code_row["semantic_paths"], ["code/repo.agent.md"])
            self.assertIn("Archived/code", (root / "code" / "repo.agent.md").read_text(encoding="utf-8"))

            archived_note = root / "Archived" / "notes.txt"
            archived_note.write_text("推荐系统实验复盘：新增排序模型结论\n", encoding="utf-8")
            synced = adapter.run_sync(root, Path("."), execute=True)
            self.assertEqual(synced["modified"], 1)
            refreshed = next(row for row in adapter.load_manifest(root) if row["asset_id"] == note["asset_id"])
            self.assertEqual(refreshed["index_status"], "candidate")
            self.assertEqual(refreshed["retention"], "review")
            self.assertIn("新增排序模型结论", (root / "notes.agent.md").read_text(encoding="utf-8"))

            (root / "new.txt").write_text("新增资料\n", encoding="utf-8")
            added = adapter.run_sync(root, Path("."), execute=True)
            self.assertEqual(added["added"], 1)
            self.assertTrue((root / "new.agent.md").exists())
            self.assertTrue((root / "Archived" / "new.txt").exists())

            archived_note.unlink()
            removed = adapter.run_sync(root, Path("."), execute=True)
            self.assertEqual(removed["removed"], 1)
            missing = next(row for row in adapter.load_manifest(root) if row["asset_id"] == note["asset_id"])
            self.assertEqual(missing["source_status"], "missing")
            self.assertEqual(missing["index_status"], "excluded")
            self.assertTrue((root / "notes.agent.md").exists())

            (root / "notes.txt").write_text("同路径的新资料\n", encoding="utf-8")
            readded = adapter.run_sync(root, Path("."), execute=True)
            self.assertEqual(readded["added"], 1)
            restored = next(row for row in adapter.load_manifest(root) if row["asset_id"] == note["asset_id"])
            self.assertEqual(restored["source_status"], "available")
            self.assertEqual(restored["index_status"], "candidate")
            self.assertTrue((root / "Archived" / "notes.txt").exists())

    def test_apply_reports_decisions_types_and_delete_effects(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            keep_source = root / "keep-repo"
            keep_source.mkdir()
            keep_semantic = keep_source / "repo.agent.md"
            keep_semantic.write_text("keep", encoding="utf-8")
            delete_source = root / "delete.txt"
            delete_source.write_text("delete", encoding="utf-8")
            delete_semantic = root / "delete.agent.md"
            delete_semantic.write_text("semantic", encoding="utf-8")
            rows = [
                {
                    "asset_id": "asset-keep",
                    "title": "Keep Repo",
                    "asset_type": "code_project",
                    "source_paths": ["keep-repo"],
                    "semantic_paths": ["keep-repo/repo.agent.md"],
                    "source_formats": ["repo"],
                    "privacy": "non_pii",
                    "retention": "review",
                    "index_status": "candidate",
                },
                {
                    "asset_id": "asset-delete",
                    "title": "Delete Note",
                    "asset_type": "document",
                    "source_paths": ["delete.txt"],
                    "semantic_paths": ["delete.agent.md"],
                    "source_formats": ["txt"],
                    "privacy": "non_pii",
                    "retention": "review",
                    "index_status": "candidate",
                },
            ]
            adapter.write_scope_manifest(root, root, rows)
            decisions = root / "decisions.json"
            decisions.write_text(
                json.dumps(
                    {
                        "scope": ".",
                        "decisions": [
                            {"asset_id": "asset-keep", "decision": "keep", "pii_label": "non_pii"},
                            {"asset_id": "asset-delete", "decision": "delete", "pii_label": "non_pii"},
                            {"asset_id": "asset-missing", "decision": "delete", "pii_label": "non_pii"},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            moved: list[str] = []

            def fake_trash(path: Path):
                moved.append(path.name)
                return {"status": "trashed", "method": "test", "path": path.as_posix()}

            with patch.object(adapter, "move_to_trash", side_effect=fake_trash):
                result = adapter.run_apply(root, Path("."), decisions, execute=True)

            self.assertEqual(result["applied"], 2)
            self.assertEqual(result["summary"]["by_decision"], {"delete": 1, "keep": 1})
            self.assertEqual(result["summary"]["unmatched_decisions"], 1)
            self.assertEqual(result["summary"]["delete_effects"]["trashed"], 2)
            self.assertEqual(set(moved), {"delete.txt", "delete.agent.md"})
            self.assertTrue((root / result["report"]["json"]).exists())
            markdown = (root / result["report"]["markdown"]).read_text(encoding="utf-8")
            self.assertIn("Delete Note", markdown)
            self.assertIn("document", markdown)
            self.assertIn("delete.txt", markdown)
            self.assertEqual(result["workbench"], "cleanup-asset-review-workbench.html")
            workbench = (root / result["workbench"]).read_text(encoding="utf-8")
            self.assertIn('"review_decision": "keep"', workbench)
            deleted = next(row for row in adapter.load_manifest(root) if row["asset_id"] == "asset-delete")
            self.assertEqual(deleted["retention"], "delete")
            self.assertEqual(deleted["index_status"], "excluded")

    def test_apply_reports_nested_semantic_as_contained_by_deleted_source(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            (repo / "repo.agent.md").write_text("semantic", encoding="utf-8")
            row = {
                "asset_id": "asset-repo",
                "title": "Repo",
                "asset_type": "code_project",
                "source_paths": ["repo"],
                "semantic_paths": ["repo/repo.agent.md"],
                "source_formats": ["repo"],
                "privacy": "non_pii",
                "retention": "review",
                "index_status": "candidate",
            }
            adapter.write_scope_manifest(root, root, [row])
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({"scope": ".", "decisions": [{"asset_id": "asset-repo", "decision": "delete", "pii_label": "non_pii"}]}), encoding="utf-8")
            with patch.object(adapter, "move_to_trash", return_value={"status": "trashed", "method": "test"}) as mocked:
                result = adapter.run_apply(root, Path("."), decisions, execute=True)

            self.assertEqual(mocked.call_count, 1)
            actions = result["delete_assets"][0]["path_actions"]
            self.assertEqual(actions[0]["status"], "trashed")
            self.assertEqual(actions[1]["status"], "skipped_contained_by_deleted_source")

    def test_apply_accepts_durable_asset_decision_ledger(self) -> None:
        adapter = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row = {
                "asset_id": "asset-keep",
                "title": "Keep",
                "asset_type": "code_project",
                "source_paths": ["repo"],
                "semantic_paths": ["repo/repo.agent.md"],
                "source_formats": ["repo"],
                "privacy": "non_pii",
                "retention": "review",
                "index_status": "candidate",
            }
            (root / "repo").mkdir()
            (root / "repo" / "repo.agent.md").write_text("semantic", encoding="utf-8")
            adapter.write_scope_manifest(root, root, [row])
            ledger = root / ".cleanup-extracted" / "asset-decisions.json"
            adapter.write_json(
                ledger,
                {"assets": {"asset-keep": {"asset_id": "asset-keep", "decision": "keep", "pii_label": "non_pii"}}},
            )

            result = adapter.run_apply(root, Path("."), ledger, execute=False)

            self.assertEqual(result["applied"], 1)
            self.assertEqual(result["summary"]["by_decision"], {"keep": 1})


if __name__ == "__main__":
    unittest.main()
