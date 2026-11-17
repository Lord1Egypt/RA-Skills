"""All inputs are isolated structural test fixtures, never real transcripts."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("backup", Path(__file__).parents[1] / "scripts/backup.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.src = self.base / "source"
        self.src.mkdir()
        self.file = self.src / ".codex/sessions/test-only.txt"
        self.file.parent.mkdir(parents=True)
        self.file.write_text("structural fixture")
        self.dest = self.base / "backup"
        self.conf = {"hosts": [{"name": "test-host", "source_root": str(self.src)}]}
    def test_dry_run_writes_nothing(self):
        report = mod.backup(self.conf, self.dest, True)
        self.assertEqual(report["hosts"][0]["planned"], 1)
        self.assertFalse(self.dest.exists())
    def test_copy_is_additive_and_source_readonly(self):
        self.assertEqual(mod.backup(self.conf, self.dest)["status"], "ok")
        target = self.dest / "test-host/.codex/sessions/test-only.txt"
        self.file.write_text("changed source")
        mod.backup(self.conf, self.dest)
        self.assertEqual(target.read_text(), "structural fixture")
        self.assertEqual(self.file.read_text(), "changed source")
    def test_excludes_credentials(self):
        (self.file.parent / "auth.json").write_text("test-only")
        mod.backup(self.conf, self.dest)
        self.assertFalse((self.dest / "test-host/.codex/sessions/auth.json").exists())
    def test_host_traversal_rejected_without_writes(self):
        self.conf["hosts"][0]["name"] = "../escape"
        with self.assertRaises(ValueError):
            mod.backup(self.conf, self.dest)
        self.assertFalse(self.dest.exists())
    def test_empty_host_fails(self):
        self.file.unlink()
        self.file.parent.rmdir()
        self.assertEqual(mod.backup(self.conf, self.dest)["status"], "failed")
    def test_partial_status(self):
        (self.file.parent / "link").symlink_to(self.file)
        self.assertEqual(mod.backup(self.conf, self.dest)["status"], "partial")
    def test_destination_symlink_rejected(self):
        self.dest.mkdir()
        (self.dest / "test-host").symlink_to(self.src, target_is_directory=True)
        self.assertEqual(mod.backup(self.conf, self.dest)["status"], "failed")
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            mod.backup(self.conf, self.src / "backup")
    def test_duplicate_host_rejected(self):
        self.conf["hosts"].append(self.conf["hosts"][0])
        with self.assertRaises(ValueError):
            mod.backup(self.conf, self.dest)

    def test_source_ancestor_symlink_rejected(self):
        external = self.base / "external"
        (self.src / ".codex").rename(external)
        (self.src / ".codex").symlink_to(external, target_is_directory=True)
        self.assertEqual(mod.backup(self.conf, self.dest)["status"], "failed")
        self.assertFalse(self.dest.exists())

    def test_destination_directory_is_not_existing_backup(self):
        target = self.dest / "test-host/.codex/sessions/test-only.txt"
        target.mkdir(parents=True)
        result = mod.backup(self.conf, self.dest)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["hosts"][0]["existing"], 0)

    def test_new_files_and_all_directories_are_private(self):
        previous = os.umask(0o022)
        try:
            mod.backup(self.conf, self.dest)
        finally:
            os.umask(previous)
        for path in [self.dest, *self.dest.rglob("*")]:
            self.assertEqual(path.stat().st_mode & 0o777, 0o700 if path.is_dir() else 0o600)

if __name__ == "__main__":
    unittest.main()
