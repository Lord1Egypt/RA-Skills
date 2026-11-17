from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_ROOT / "scripts" / "asset_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location("asset_pipeline", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AssetPipelineTest(unittest.TestCase):
    def test_post_apply_index_ready_requires_clean_scope(self) -> None:
        pipeline = load_module()
        ready, reason = pipeline.post_apply_index_ready(
            {"success": True, "summary": {"unmatched_decisions": 0}},
            {"summary": {"ready_for_scope_index": True}},
        )
        self.assertTrue(ready)
        self.assertIn("ready", reason)
        ready, reason = pipeline.post_apply_index_ready(
            {"success": True, "summary": {"unmatched_decisions": 0}},
            {"summary": {"ready_for_scope_index": False, "candidate": 2, "review": 2}},
        )
        self.assertFalse(ready)
        self.assertIn("candidate", reason)

    def test_execute_apply_auto_indexes_only_when_audit_is_ready(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = root / "adapter.py"
            adapter.write_text("# adapter", encoding="utf-8")
            routine = root / "routine.py"
            routine.write_text("# routine", encoding="utf-8")
            decisions = root / "decisions.json"
            decisions.write_text("{}", encoding="utf-8")
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--cleanup-tool", str(adapter), "--stage", "apply",
                    "--decisions", str(decisions), "--execute-decisions", "--after-apply-index", "auto",
                    "--second-brain-routine", str(routine),
                ]
            )
            plan = pipeline.build_plan(args)
            apply_payload = json.dumps({"success": True, "summary": {"unmatched_decisions": 0}})
            audit_payload = json.dumps({"summary": {"ready_for_scope_index": True}})
            calls: list[list[str]] = []

            def fake_run(command, **kwargs):
                calls.append(command)
                if "--audit-agent-assets" in command:
                    return subprocess.CompletedProcess(command, 0, audit_payload, "")
                if "--source-mode" in command:
                    return subprocess.CompletedProcess(command, 0, json.dumps({"status": "ok"}), "")
                return subprocess.CompletedProcess(command, 0, apply_payload, "")

            with patch.object(pipeline.subprocess, "run", side_effect=fake_run):
                results = pipeline.run_plan(args, plan)

            self.assertEqual([result.stage for result in results], ["apply", "post-apply-audit", "post-apply-index"])
            self.assertEqual(results[-1].status, "ok")
            self.assertTrue(any("--source-mode" in call for call in calls))

    def test_execute_apply_skips_index_when_scope_has_candidates(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = root / "adapter.py"
            adapter.write_text("# adapter", encoding="utf-8")
            routine = root / "routine.py"
            routine.write_text("# routine", encoding="utf-8")
            decisions = root / "decisions.json"
            decisions.write_text("{}", encoding="utf-8")
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--cleanup-tool", str(adapter), "--stage", "apply",
                    "--decisions", str(decisions), "--execute-decisions", "--after-apply-index", "auto",
                    "--second-brain-routine", str(routine),
                ]
            )
            plan = pipeline.build_plan(args)
            apply_payload = json.dumps({"success": True, "summary": {"unmatched_decisions": 0}})
            audit_payload = json.dumps({"summary": {"ready_for_scope_index": False, "candidate": 1}})

            def fake_run(command, **kwargs):
                if "--audit-agent-assets" in command:
                    return subprocess.CompletedProcess(command, 2, audit_payload, "")
                return subprocess.CompletedProcess(command, 0, apply_payload, "")

            with patch.object(pipeline.subprocess, "run", side_effect=fake_run):
                results = pipeline.run_plan(args, plan)

            self.assertEqual(results[-1].stage, "post-apply-index")
            self.assertEqual(results[-1].status, "skipped")
            self.assertIn("candidate", results[-1].blocked_reason)

    def test_automatic_index_inherits_force_flag(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            routine = root / "routine.py"
            routine.write_text("# routine", encoding="utf-8")
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--second-brain-routine", str(routine),
                    "--force-index",
                ]
            )

            command = pipeline.automatic_index_command(args)

            self.assertIn("--force", command)

    def test_execute_apply_rewrites_workbench_then_runs_ready_scope_index(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            (repo / "repo.agent.md").write_text("semantic", encoding="utf-8")
            state = root / ".cleanup-extracted"
            state.mkdir()
            manifest_row = {
                "asset_id": "asset-repo",
                "title": "Repo",
                "asset_type": "code_project",
                "path": "repo/repo.agent.md",
                "source_paths": ["repo"],
                "semantic_paths": ["repo/repo.agent.md"],
                "semantic_formats": ["markdown"],
                "source_formats": ["repo"],
                "privacy": "non_pii",
                "retention": "review",
                "index_status": "candidate",
            }
            (state / "asset-manifest.jsonl").write_text(json.dumps(manifest_row) + "\n", encoding="utf-8")
            decisions = root / "decisions.json"
            decisions.write_text(
                json.dumps({"scope": ".", "decisions": [{"asset_id": "asset-repo", "decision": "keep", "pii_label": "non_pii"}]}),
                encoding="utf-8",
            )
            routine = root / "routine.py"
            routine.write_text(
                "from pathlib import Path\n"
                "import json, sys\n"
                "vault = Path(sys.argv[sys.argv.index('--vault') + 1])\n"
                "(vault / 'index-call.json').write_text(json.dumps(sys.argv), encoding='utf-8')\n"
                "print(json.dumps({'status': 'ok'}))\n",
                encoding="utf-8",
            )
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--cleanup-tool", str(pipeline.DEFAULT_MIXED_FOLDER_ADAPTER),
                    "--stage", "apply", "--decisions", str(decisions), "--execute-decisions",
                    "--second-brain-routine", str(routine),
                ]
            )

            results = pipeline.run_plan(args, pipeline.build_plan(args))

            self.assertEqual([result.stage for result in results], ["apply", "post-apply-audit", "post-apply-index"])
            self.assertEqual(results[-1].status, "ok")
            self.assertTrue((root / "cleanup-asset-review-workbench.html").exists())
            call = json.loads((root / "index-call.json").read_text(encoding="utf-8"))
            self.assertIn("asset-manifest", call)

    def test_optimize_retrieval_requires_explicit_refresh_and_index_gates(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = root / "adapter.py"
            adapter.write_text("# adapter", encoding="utf-8")
            routine = root / "routine.py"
            routine.write_text("# routine", encoding="utf-8")
            benchmark = root / "benchmark.json"
            benchmark.write_text('{"queries": []}\n', encoding="utf-8")
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--cleanup-tool", str(adapter),
                    "--pipeline", "optimize-retrieval", "--retrieval-benchmark", str(benchmark),
                    "--second-brain-routine", str(routine),
                ]
            )

            plan = pipeline.build_plan(args)

            self.assertEqual([item.stage for item in plan], ["retrieval-audit", "retrieval-refresh", "index", "retrieval-verify"])
            self.assertIn("execute-retrieval-refresh", plan[1].blocked_reason)
            self.assertIn("execute-index", plan[2].blocked_reason)

    def test_retrieval_verify_marks_strict_gate_failure_as_attention(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = root / "adapter.py"
            adapter.write_text("# adapter", encoding="utf-8")
            benchmark = root / "benchmark.json"
            benchmark.write_text('{"queries": []}\n', encoding="utf-8")
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--cleanup-tool", str(adapter), "--stage", "retrieval-verify",
                    "--retrieval-benchmark", str(benchmark),
                ]
            )
            plan = pipeline.build_plan(args)

            with patch.object(
                pipeline.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(plan[0].command, 3, json.dumps({"summary": {"strict_top1_passed": False}}), ""),
            ):
                results = pipeline.run_plan(args, plan)

            self.assertEqual(results[0].status, "attention")

    def test_retrieval_verify_runs_semantic_fallback_after_lexical_gate_failure(self) -> None:
        pipeline = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = root / "adapter.py"
            adapter.write_text("# adapter", encoding="utf-8")
            benchmark = root / "benchmark.json"
            benchmark.write_text('{"queries": []}\n', encoding="utf-8")
            args = pipeline.parse_args(
                [
                    "--root", str(root), "--cleanup-tool", str(adapter), "--stage", "retrieval-verify",
                    "--retrieval-benchmark", str(benchmark), "--allow-semantic-rerank",
                ]
            )
            plan = pipeline.build_plan(args)
            calls: list[list[str]] = []

            def fake_run(command, **kwargs):
                calls.append(command)
                if "--semantic-rerank" in command:
                    return subprocess.CompletedProcess(command, 0, json.dumps({"summary": {"strict_top1_passed": True}}), "")
                return subprocess.CompletedProcess(command, 3, json.dumps({"summary": {"strict_top1_passed": False}}), "")

            with patch.object(pipeline.subprocess, "run", side_effect=fake_run):
                results = pipeline.run_plan(args, plan)

            self.assertEqual([result.stage for result in results], ["retrieval-verify", "retrieval-semantic-verify"])
            self.assertEqual(results[-1].status, "ok")
            self.assertTrue(any("--semantic-rerank" in command for command in calls))


if __name__ == "__main__":
    unittest.main()
