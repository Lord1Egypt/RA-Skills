import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PATHS_MODULE_PATH = PROJECT_ROOT / "core" / "paths.py"

spec = importlib.util.spec_from_file_location("chronos_paths", PATHS_MODULE_PATH)
paths = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(paths)


class PathsTests(unittest.TestCase):
    def _load_paths_module(self):
        spec = importlib.util.spec_from_file_location("chronos_paths_reloaded", PATHS_MODULE_PATH)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module

    def test_workspace_env_overrides_default_lookup(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "todo.db").write_text("", encoding="utf-8")

            with patch.dict(os.environ, {"CHRONOS_WORKSPACE": str(workspace)}, clear=False):
                reloaded = self._load_paths_module()
                self.assertEqual(reloaded.WORKSPACE, workspace)
                self.assertEqual(reloaded.TODO_DB, workspace / "todo.db")

    def test_db_path_env_has_highest_priority(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            custom_db = workspace / "custom.db"

            with patch.dict(
                os.environ,
                {
                    "CHRONOS_WORKSPACE": str(workspace),
                    "CHRONOS_DB_PATH": str(custom_db),
                },
                clear=False,
            ):
                reloaded = self._load_paths_module()
                self.assertEqual(reloaded.WORKSPACE, workspace)
                self.assertEqual(reloaded.TODO_DB, custom_db)

    def test_workspace_env_is_respected_even_without_todo_db(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir) / "workspace"
            workspace.mkdir()

            with patch.dict(os.environ, {"CHRONOS_WORKSPACE": str(workspace)}, clear=False):
                reloaded = self._load_paths_module()
                self.assertEqual(reloaded.WORKSPACE, workspace)
                self.assertEqual(reloaded.TODO_DB, workspace / "todo.db")


if __name__ == "__main__":
    unittest.main()
