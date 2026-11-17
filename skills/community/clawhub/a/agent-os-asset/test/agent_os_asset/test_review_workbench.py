from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_ROOT / "scripts" / "review_workbench.py"
SERVER = SKILL_ROOT / "scripts" / "review_workbench_server.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReviewWorkbenchTest(unittest.TestCase):
    def test_static_workbench_keeps_main_review_capabilities(self) -> None:
        renderer = load_module(SCRIPT, "review_workbench")
        html = renderer.render_workbench(
            root=Path("/tmp/workspace"),
            scope=".",
            rows=[
                {
                    "asset_id": "asset-a",
                    "asset_type": "code_project",
                    "source_paths": ["nested/repo"],
                    "semantic_paths": ["repo/repo.agent.md"],
                    "source_formats": ["repo"],
                    "title": "Repo </script>",
                    "summary": "summary",
                    "insights": ["insight"],
                    "index_status": "candidate",
                    "privacy": "non_pii",
                    "suggested_decision": "keep",
                    "suggestion_reason": "useful project",
                }
            ],
            adapter_path=Path("/tmp/adapter.py"),
            pipeline_path=Path("/tmp/pipeline.py"),
            shortcut_available=False,
        )

        for expected in (
            "全选",
            "反选",
            "清空选择",
            "应用到已选",
            "Search title/path/summary/insight",
            "复制 open 命令",
            "下载 decisions.json",
            "下载并复制命令",
            "filterSuggestion",
            "filterDecision",
            "filterPii",
            "filterFileType",
            "type=\"checkbox\"",
            "aria-label=\"Select asset / 选择资产",
            "appearance:auto",
            "accent-color:var(--blue)",
            "file://",
            "asset-data",
            "<\\/script>",
            "frozen-index",
            "frozen-decision",
            "frozen-pii",
            "workspace/nested/repo",
            "max-height:calc(100vh",
            "已执行并回写 workbench",
            "window.location.reload",
        ):
            self.assertIn(expected, html)
        self.assertNotIn("Shortcut 打开", html)

    def test_server_path_resolution_rejects_workspace_escape(self) -> None:
        server = load_module(SERVER, "review_workbench_server")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            inside = root / "scope" / "notes.txt"
            inside.parent.mkdir()
            inside.write_text("ok", encoding="utf-8")
            self.assertEqual(server.resolve_review_path(root, "scope/notes.txt"), inside.resolve())
            with self.assertRaises(ValueError):
                server.resolve_review_path(root, "../outside.txt")

    def test_server_handler_is_configured_with_pipeline_path(self) -> None:
        server = load_module(SERVER, "review_workbench_server")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = root / "adapter.py"
            pipeline = root / "pipeline.py"
            adapter.write_text("# adapter", encoding="utf-8")
            pipeline.write_text("# pipeline", encoding="utf-8")
            handler = server.configured_handler(
                root,
                adapter,
                pipeline,
                allow_write=False,
                allow_apply=False,
                allow_file_open=False,
                session_token="test-token",
            )
            self.assertEqual(handler.adapter_path, adapter.resolve())
            self.assertEqual(handler.pipeline_path, pipeline.resolve())
            self.assertFalse(handler.allow_write)
            self.assertFalse(handler.allow_apply)
            self.assertFalse(handler.allow_file_open)
            self.assertEqual(handler.session_token, "test-token")

    def test_server_security_helpers_reject_unsafe_defaults(self) -> None:
        server = load_module(SERVER, "review_workbench_server_security")

        self.assertTrue(server.is_loopback_host("127.0.0.1"))
        self.assertTrue(server.is_loopback_host("localhost"))
        self.assertFalse(server.is_loopback_host("0.0.0.0"))
        self.assertTrue(
            server.valid_session_token(
                {"X-Agent-Asset-Token": "expected"}, "expected"
            )
        )
        self.assertFalse(
            server.valid_session_token(
                {"X-Agent-Asset-Token": "wrong"}, "expected"
            )
        )

    def test_server_extracts_refreshed_workbench_from_pipeline_result(self) -> None:
        server = load_module(SERVER, "review_workbench_server")
        pipeline_stdout = json.dumps(
            {
                "results": [
                    {
                        "stage": "apply",
                        "status": "ok",
                        "stdout": json.dumps(
                            {
                                "workbench": "cleanup-asset-review-workbench.html",
                                "report": {"json": ".cleanup-extracted/report.json"},
                            }
                        ),
                    },
                    {"stage": "post-apply-index", "status": "skipped", "blocked_reason": "scope is not index-ready"},
                ]
            }
        )

        result = server.pipeline_apply_result(pipeline_stdout)

        self.assertEqual(result["workbench"], "cleanup-asset-review-workbench.html")
        self.assertEqual(result["post_apply_index"]["status"], "skipped")


if __name__ == "__main__":
    unittest.main()
