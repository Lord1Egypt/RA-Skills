"""Trust and opt-in regressions; all execution is mocked or in temp folders."""

import importlib.util
import io
from contextlib import redirect_stderr, redirect_stdout
import json
import os
from pathlib import Path
import subprocess
import shlex
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PipelineSecurityTest(unittest.TestCase):
    def test_index_preflight_rejects_sibling_final_assets_and_unknown_privacy(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / ".cleanup-extracted"
            state.mkdir()
            manifest = state / "asset-manifest.jsonl"
            safe = {"asset_id": "docs", "path": "docs/entry.agent.md", "source_paths": ["docs/source.md"],
                    "semantic_paths": ["docs/entry.agent.md"], "privacy": "non_pii", "index_status": "final"}
            other = dict(safe, asset_id="other", path="other/entry.agent.md", source_paths=["other/source.md"], semantic_paths=["other/entry.agent.md"])
            manifest.write_text(json.dumps(safe) + "\n" + json.dumps(other) + "\n")
            self.assertIn("outside", pipeline.index_scope_error(root, "docs"))
            self.assertEqual(pipeline.index_scope_error(root, "."), "")
            manifest.write_text(json.dumps(dict(safe, privacy="unknown")) + "\n")
            self.assertIn("privacy", pipeline.index_scope_error(root, "."))
            manifest.write_text(json.dumps(safe) + "\n")
            self.assertEqual(pipeline.index_scope_error(root, "docs"), "")

    def test_apply_plan_discloses_conditional_index_effects(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            args = pipeline.parse_args(["--root", directory, "--stage", "apply", "--decisions", "review.json", "--execute-decisions"])
            description = pipeline.build_plan(args)[0].description
            self.assertIn("conditional", description)
            self.assertIn("registry", description)
            self.assertIn("log", description)

    def test_all_index_routes_stop_before_reading_other_scope(self):
        pipeline = load_script("asset_pipeline")
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            state = root / ".cleanup-extracted"
            state.mkdir()
            (state / "asset-manifest.jsonl").write_text(json.dumps({
                "asset_id": "other", "path": "other/source.md", "source_paths": ["other/source.md"],
                "privacy": "non_pii", "index_status": "final",
            }) + "\n")
            routine = root / "routine.py"
            routine.touch()

            def fake_run(command, **kwargs):
                if "--audit-agent-assets" in command:
                    data = {"summary": {"ready_for_scope_index": True}}
                else:
                    data = {"success": True, "index_ready": True, "failed": 0, "added": 1}
                return subprocess.CompletedProcess(command, 0, json.dumps(data), "")

            benchmark = state / "retrieval-benchmark.json"
            benchmark.write_text('{"queries": []}\n')
            routes = (
                ["--stage", "apply"],
                ["--stage", "index"],
                ["--pipeline", "index"],
                ["--pipeline", "maintain", "--execute-sync", "--auto-keep"],
                ["--pipeline", "full", "--execute-extraction"],
                ["--pipeline", "optimize-retrieval", "--execute-retrieval-refresh"],
            )
            for route in routes:
                args = pipeline.parse_args([
                    "--root", str(root), "--scope", "docs", *route,
                    "--execute-index", "--skip-decision-ledger-check", "--second-brain-routine", str(routine),
                    "--decisions", "review.json", "--execute-decisions",
                ])
                with self.subTest(route=route), patch.object(pipeline.subprocess, "run", side_effect=fake_run) as run:
                    results = pipeline.run_plan(args, pipeline.build_plan(args))
                    self.assertFalse(any("--source-mode" in call.args[0] for call in run.call_args_list))
                    self.assertIn("outside", results[-1].blocked_reason)
            with patch.object(sync.subprocess, "run", side_effect=fake_run) as run, patch.object(sync, "notify"):
                result = sync.run_automatic_sync(root, "docs", routine, debounce_seconds=0, auto_keep=True)
            self.assertFalse(any("--source-mode" in call.args[0] for call in run.call_args_list))
            self.assertIn("outside", result["reason"])

    def test_copyable_plan_keeps_shell_metacharacters_literal(self):
        pipeline = load_script("asset_pipeline")
        command = ["python3", "/tmp/a'$(touch NOT_EXECUTED)`id`.py"]
        output = io.StringIO()
        with redirect_stdout(output):
            pipeline.print_plan([pipeline.StagePlan("inventory", command, "preview")], False)
        copied = output.getvalue().split("  command / 命令: ", 1)[1].strip()
        self.assertEqual(shlex.split(copied), command)
        self.assertEqual(copied, shlex.join(command))

    def test_default_maintain_is_candidate_sync_without_index(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            args = pipeline.parse_args(["--root", directory, "--pipeline", "maintain", "--execute-sync"])
            self.assertEqual([stage.stage for stage in pipeline.build_plan(args)], ["sync"])

    def test_optimize_cannot_refresh_before_index_gate_is_approved(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            args = pipeline.parse_args([
                "--root", directory, "--pipeline", "optimize-retrieval", "--execute-retrieval-refresh",
            ])
            refresh = next(stage for stage in pipeline.build_plan(args) if stage.stage == "retrieval-refresh")
            self.assertIn("execute-index", refresh.blocked_reason)

    def test_workspace_code_is_never_discovered_as_an_executable(self):
        pipeline = load_script("asset_pipeline")
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "tools" / "cleanup_convert.py"
            tool.parent.mkdir()
            tool.write_text("raise RuntimeError('untrusted source')\n")
            for module in (pipeline, sync):
                with self.subTest(module=module.__name__):
                    args = module.parse_args(["--root", str(root)])
                    self.assertEqual(args.cleanup_tool, pipeline.DEFAULT_MIXED_FOLDER_ADAPTER)
                    explicit = module.parse_args(["--root", str(root), "--cleanup-tool", str(tool)])
                    self.assertEqual(explicit.cleanup_tool, tool.resolve())

    def test_scope_and_state_symlink_cannot_escape_root(self):
        for name in ("asset_pipeline", "auto_sync"):
            module = load_script(name)
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "workspace"
                root.mkdir()
                outside = Path(directory) / "outside"
                outside.mkdir()
                for scope in ("../outside", str(outside)):
                    with self.subTest(module=name, scope=scope), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                        module.parse_args(["--root", str(root), "--scope", scope])
                (root / "linked").symlink_to(outside, target_is_directory=True)
                with self.subTest(module=name, scope="linked"), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    module.parse_args(["--root", str(root), "--scope", "linked"])
                (root / ".cleanup-extracted").symlink_to(outside, target_is_directory=True)
                with self.subTest(module=name, state=True), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    module.parse_args(["--root", str(root)])

    def test_state_links_cannot_redirect_writes_to_sources_inside_root(self):
        for name in ("asset_pipeline", "auto_sync"):
            module = load_script(name)
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "source"
                source.mkdir()
                (root / ".cleanup-extracted").symlink_to(source, target_is_directory=True)
                with self.subTest(module=name), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    module.parse_args(["--root", str(root)])

    def test_sync_lock_does_not_truncate_a_hardlinked_source(self):
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_text("SOURCE_SENTINEL")
            state = root / ".cleanup-extracted"
            state.mkdir()
            os.link(source, state / sync.LOCK_NAME)
            with self.assertRaises(ValueError):
                with sync.sync_lock(root):
                    self.fail("lock unexpectedly acquired")
            self.assertEqual(source.read_text(), "SOURCE_SENTINEL")

    def test_direct_index_and_ledger_override_still_require_audit(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            routine = root / "routine.py"
            routine.touch()
            args = pipeline.parse_args([
                "--root", str(root), "--stage", "index", "--execute-index",
                "--skip-decision-ledger-check", "--second-brain-routine", str(routine),
            ])
            for payload in ({}, {"summary": {"ready_for_scope_index": "false"}},
                            {"summary": {"ready_for_scope_index": True, "candidate": 1}}):
                with self.subTest(payload=payload):
                    with patch.object(pipeline.subprocess, "run", return_value=subprocess.CompletedProcess(
                        [], 0, json.dumps(payload), ""
                    )) as run:
                        results = pipeline.run_plan(args, pipeline.build_plan(args))
                    self.assertFalse(any("--source-mode" in call.args[0] for call in run.call_args_list))
                    self.assertEqual(results[-1].status, "blocked")

    def test_direct_index_accepts_fresh_clean_audit(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            routine = root / "routine.py"
            routine.touch()
            args = pipeline.parse_args([
                "--root", str(root), "--stage", "index", "--execute-index",
                "--skip-decision-ledger-check", "--second-brain-routine", str(routine),
            ])
            with patch.object(pipeline.subprocess, "run", side_effect=[
                subprocess.CompletedProcess([], 0, '{"summary":{"ready_for_scope_index":true}}', ""),
                subprocess.CompletedProcess([], 0, '{}', ""),
            ]) as run:
                results = pipeline.run_plan(args, pipeline.build_plan(args))
            self.assertIn("--audit-agent-assets", run.call_args_list[0].args[0])
            self.assertIn("--source-mode", run.call_args_list[1].args[0])
            self.assertEqual(results[-1].status, "ok")

    def test_lexical_failure_does_not_silently_enable_provider(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            args = pipeline.parse_args(["--root", directory])
            plan = [pipeline.StagePlan("retrieval-verify", ["mock-check"], "verify", allow_returncodes=(0, 3))]
            with patch.object(pipeline.subprocess, "run", return_value=subprocess.CompletedProcess(
                [], 3, '{"summary":{"strict_top1_passed":false}}', ""
            )) as run:
                results = pipeline.run_plan(args, plan)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(results[0].status, "attention")

    def test_automatic_sync_requires_separate_auto_keep_opt_in(self):
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "adapter.py"
            tool.touch()
            with patch.object(sync.subprocess, "run", return_value=subprocess.CompletedProcess(
                [], 0, '{"added":1,"failed":0,"index_ready":true}', ""
            )) as run, patch.object(sync, "notify"):
                result = sync.run_automatic_sync(root, ".", tool, debounce_seconds=0)
            self.assertEqual(run.call_count, 1)
            self.assertNotIn("--auto-keep", run.call_args.args[0])
            self.assertIsNone(result["index"])
            self.assertNotIn("--auto-keep", sync.launch_agent_payload(root, ".", tool, 0)["ProgramArguments"])

    def test_auto_keep_alone_cannot_bypass_fresh_audit(self):
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "adapter.py"
            tool.touch()
            with patch.object(sync.subprocess, "run", side_effect=[
                subprocess.CompletedProcess([], 0, '{"added":1,"failed":0,"index_ready":true}', ""),
                subprocess.CompletedProcess([], 0, '{"summary":{"ready_for_scope_index":"false"}}', ""),
            ]) as run, patch.object(sync, "notify"):
                result = sync.run_automatic_sync(root, ".", tool, debounce_seconds=0, auto_keep=True)
            self.assertEqual(run.call_count, 2)
            self.assertIn("--auto-keep", run.call_args_list[0].args[0])
            self.assertIn("--audit-agent-assets", run.call_args_list[1].args[0])
            self.assertIsNone(result["index"])
            self.assertEqual(result["status"], "attention")

    def test_auto_sync_api_rejects_scope_before_lock_or_execute(self):
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "workspace"
            root.mkdir()
            tool = root / "adapter.py"
            tool.touch()
            with patch.object(sync.subprocess, "run") as run, self.assertRaises(ValueError):
                sync.run_automatic_sync(root, "..", tool, debounce_seconds=0)
            run.assert_not_called()
            self.assertFalse((root / ".cleanup-extracted").exists())

    def test_index_commands_use_public_runtime_registry_and_workspace_effect_paths(self):
        self.addCleanup(lambda: (load_script("asset_pipeline"), load_script("auto_sync")))
        pipeline = load_script("asset_pipeline")
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / "runtime" / "asset-index-registry.json"
            # Public releases honor portable runtime configuration, not a private runtime's home.
            with patch.dict(os.environ, {"SECOND_BRAIN_ASSET_REGISTRY": str(registry)}):
                pipeline = load_script("asset_pipeline")
                sync = load_script("auto_sync")
            args = pipeline.parse_args(["--root", str(root)])
            for command in (pipeline.automatic_index_command(args), sync.index_command(root)):
                with self.subTest(command=command):
                    for flag, path in (
                        ("--out", root / ".cleanup-extracted/second-brain-asset-index"),
                        ("--log", root / ".cleanup-extracted/second-brain-routine.log"),
                        ("--lock", root / ".cleanup-extracted/second-brain-routine.lock"),
                        ("--asset-index-registry", registry),
                    ):
                        self.assertIn(flag, command)
                        self.assertEqual(Path(command[command.index(flag) + 1]), path.resolve())
                    self.assertIn("skills/second-brain/scripts/routine_update.py", command[1])

    def test_readiness_rejects_false_success_malformed_summary_and_conflicting_blockers(self):
        pipeline = load_script("asset_pipeline")
        clean = {"summary": {"ready_for_scope_index": True}}
        for apply in ({"success": "true"}, {"success": 1},
                      {"success": True, "summary": []},
                      {"success": True, "summary": {"unmatched_decisions": "0"}}):
            with self.subTest(apply=apply):
                self.assertFalse(pipeline.post_apply_index_ready(apply, clean)[0])
        for value in ("false", 1, None):
            with self.subTest(ready=value):
                self.assertFalse(pipeline.post_apply_index_ready(
                    {"success": True}, {"summary": {"ready_for_scope_index": value}}
                )[0])
        for blocker in ("candidate", "review", "missing_source", "missing_semantic", "final_pii", "delete_failed"):
            with self.subTest(blocker=blocker):
                self.assertFalse(pipeline.post_apply_index_ready(
                    {"success": True}, {"summary": {"ready_for_scope_index": True, blocker: 1}}
                )[0])

    def test_each_index_entrypoint_requires_successful_same_scope_audit(self):
        pipeline = load_script("asset_pipeline")
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "adapter.py"
            tool.touch()
            routine = root / "routine.py"
            routine.touch()
            routes = (["--stage", "apply"], ["--stage", "index"],
                      ["--pipeline", "maintain", "--execute-sync", "--auto-keep"])
            for audit_code in (0, 2):
                def fake_run(command, **kwargs):
                    if "--audit-agent-assets" in command:
                        self.assertEqual(command[command.index("--scope") + 1], "docs")
                        return subprocess.CompletedProcess(command, audit_code,
                            '{"summary":{"ready_for_scope_index":true}}', "")
                    return subprocess.CompletedProcess(command, 0,
                        '{"success":true,"index_ready":true,"failed":0,"added":1}', "")

                for route in routes:
                    args = pipeline.parse_args([
                        "--root", str(root), "--scope", "docs", "--cleanup-tool", str(tool),
                        *route, "--execute-index", "--skip-decision-ledger-check",
                        "--second-brain-routine", str(routine), "--execute-decisions", "--decisions", "review.json",
                    ])
                    with self.subTest(route=route, audit_code=audit_code), patch.object(
                        pipeline.subprocess, "run", side_effect=fake_run
                    ) as run:
                        pipeline.run_plan(args, pipeline.build_plan(args))
                        commands = [call.args[0] for call in run.call_args_list]
                        self.assertTrue(any("--audit-agent-assets" in command for command in commands))
                        self.assertEqual(any("--source-mode" in command for command in commands), audit_code == 0)
                with self.subTest(route="automatic-sync", audit_code=audit_code), patch.object(
                    sync.subprocess, "run", side_effect=fake_run
                ) as run, patch.object(sync, "notify"):
                    sync.run_automatic_sync(root, "docs", tool, debounce_seconds=0, auto_keep=True)
                    commands = [call.args[0] for call in run.call_args_list]
                    self.assertTrue(any("--audit-agent-assets" in command for command in commands))
                    self.assertEqual(any("--source-mode" in command for command in commands), audit_code == 0)

    def test_manifest_scope_validation_rejects_malformed_paths_and_accepts_scoped_archive(self):
        pipeline = load_script("asset_pipeline")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / ".cleanup-extracted"
            state.mkdir()
            manifest = state / "asset-manifest.jsonl"
            base = {"index_status": "final", "privacy": "non_pii", "source_paths": ["docs/source.md"]}
            for row in (dict(base, source_paths="docs/source.md"), dict(base, source_paths=[None]),
                        dict(base, source_paths=[]), dict(base, source_paths=["../outside.md"]),
                        dict(base, semantic_paths=["sibling/entry.agent.md"]),
                        dict(base, privacy=None), [], "not-json"):
                with self.subTest(row=row):
                    manifest.write_text(row if isinstance(row, str) else json.dumps(row))
                    self.assertTrue(pipeline.index_scope_error(root, "docs"))
            manifest.write_text(json.dumps(dict(base, source_paths=["Archived/docs/source.md"],
                                                semantic_paths=["docs/entry.agent.md"])))
            self.assertEqual(pipeline.index_scope_error(root, "docs"), "")

    def test_sync_payload_and_launcher_require_boolean_explicit_opt_in(self):
        pipeline = load_script("asset_pipeline")
        sync = load_script("auto_sync")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "adapter.py"
            tool.touch()
            payload = sync.launch_agent_payload(root, "docs", tool, 0, auto_keep=True)
            self.assertIn("--auto-keep", payload["ProgramArguments"])
            self.assertEqual(payload["WatchPaths"], [str(root / "docs"), str(root / "Archived/docs")])
            args = pipeline.parse_args([
                "--root", str(root), "--cleanup-tool", str(tool), "--pipeline", "maintain",
                "--execute-sync", "--auto-keep", "--second-brain-routine", str(tool),
            ])
            for ready in ("true", "false", 1):
                with self.subTest(ready=ready), patch.object(pipeline.subprocess, "run", return_value=
                    subprocess.CompletedProcess([], 0, json.dumps({"index_ready": ready}), "")
                ) as run:
                    results = pipeline.run_plan(args, pipeline.build_plan(args))
                    self.assertEqual(run.call_count, 1)
                    self.assertEqual(results[-1].status, "skipped")


if __name__ == "__main__":
    unittest.main()
