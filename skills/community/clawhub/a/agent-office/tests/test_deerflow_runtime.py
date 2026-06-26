import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "deerflow_runtime.py"
SPEC = importlib.util.spec_from_file_location("deerflow_runtime_module", MODULE_PATH)
deerflow_runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(deerflow_runtime)


class DeerflowRuntimeTests(unittest.TestCase):
    def test_missing_prerequisites_reports_absent_commands(self):
        with mock.patch.object(deerflow_runtime.shutil, "which", side_effect=lambda name: None):
            self.assertEqual(
                deerflow_runtime.missing_prerequisites(),
                ["git", "uv"],
            )

    def test_ensure_worker_home_creates_agent_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            office_dir = Path(tmpdir) / "office"
            with mock.patch.dict(os.environ, {"HERMES_OFFICE_DIR": str(office_dir)}, clear=False):
                home_dir = deerflow_runtime.ensure_worker_home(
                    "xiaod2",
                    "小D2",
                    "complex",
                    model="gpt-5.4",
                )

            self.assertTrue((home_dir / "agents" / "xiaod2" / "config.yaml").exists())
            soul = (home_dir / "agents" / "xiaod2" / "SOUL.md").read_text(encoding="utf-8")
            self.assertIn("小D2", soul)
            self.assertIn("complex", soul)

    def test_write_worker_runtime_config_includes_workspace_mount(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            office_dir = Path(tmpdir) / "office"
            worker_dir = office_dir / "workers" / "xiaod2"
            workspace_dir = Path(tmpdir) / "workspace"
            worker_dir.mkdir(parents=True, exist_ok=True)
            workspace_dir.mkdir(parents=True, exist_ok=True)
            with mock.patch.dict(os.environ, {"HERMES_OFFICE_DIR": str(office_dir)}, clear=False):
                config_path = deerflow_runtime.write_worker_runtime_config(
                    worker_dir,
                    str(workspace_dir),
                    "xiaod2",
                    "小D2",
                    "complex",
                    model="gpt-5.4",
                    reasoning_effort="medium",
                )

            content = config_path.read_text(encoding="utf-8")
            self.assertIn(str(workspace_dir), content)
            self.assertIn(str(worker_dir), content)
            self.assertIn('container_path: "/mnt/workspace"', content)
            self.assertIn('container_path: "/mnt/worker"', content)
            self.assertNotIn(f'host_path: "{office_dir}"', content)
            self.assertIn('name: "gpt-5.4"', content)
            self.assertIn("deerflow.models.openai_codex_provider:CodexChatModel", content)

    def test_write_worker_runtime_config_keeps_worker_alias_when_workspace_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            office_dir = Path(tmpdir) / "office"
            worker_dir = office_dir / "workers" / "xiaod2"
            worker_dir.mkdir(parents=True, exist_ok=True)
            with mock.patch.dict(os.environ, {"HERMES_OFFICE_DIR": str(office_dir)}, clear=False):
                config_path = deerflow_runtime.write_worker_runtime_config(
                    worker_dir,
                    str(worker_dir),
                    "xiaod2",
                    "小D2",
                    "complex",
                    model="gpt-5.4",
                    reasoning_effort="medium",
                )

            content = config_path.read_text(encoding="utf-8")
            self.assertEqual(content.count(str(worker_dir)), 2)
            self.assertIn('container_path: "/mnt/workspace"', content)
            self.assertIn('container_path: "/mnt/worker"', content)


if __name__ == "__main__":
    unittest.main()
