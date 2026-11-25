"""Read-only detection safety tests."""
from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/api-to-typemcp/scripts"))
from agent_clients import AgentClientError, detect_clients, server_spec_from_project  # noqa: E402


class DetectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.home = self.root / "home"; self.home.mkdir()
        self.project = self.root / "server"; (self.project / "dist").mkdir(parents=True)
        (self.project / "dist/index.js").write_text("// built\n")
        (self.project / ".env").write_text("TOKEN=real-secret\n")
        (self.home / ".codex").mkdir(); (self.home / ".codex/config.toml").write_text("model='x'\n")
    def tearDown(self) -> None: self.tmp.cleanup()
    def test_spec_is_built_contained_and_secret_free(self) -> None:
        spec = server_spec_from_project(self.project, server_name="petstore-mcp")
        self.assertEqual(spec.command, "node"); self.assertNotIn("real-secret", json.dumps(spec.to_public_dict()))
        with self.assertRaises(AgentClientError): server_spec_from_project(self.project, server_name="../bad")
    def test_rejects_symlinked_build_parent(self) -> None:
        ext = self.root / "external"; ext.mkdir(); (ext / "index.js").write_text("// outside")
        (self.project / "dist/index.js").unlink(); (self.project / "dist").rmdir(); (self.project / "dist").symlink_to(ext, target_is_directory=True)
        with self.assertRaises(AgentClientError): server_spec_from_project(self.project, server_name="petstore-mcp")
    def test_detection_is_read_only_and_secret_free(self) -> None:
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        clients = detect_clients(home=self.home, project=self.project, which=lambda n: "/bin/codex" if n == "codex" else None)
        self.assertEqual([x.id for x in clients], ["codex"]); self.assertNotIn("real-secret", json.dumps([x.to_public_dict() for x in clients]))
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}; self.assertEqual(before, after)
    def test_rejects_symlinked_config_parent(self) -> None:
        ext = self.root / "external"; ext.mkdir(); (ext / "config.toml").write_text("model='x'")
        (self.home / ".codex/config.toml").unlink(); (self.home / ".codex").rmdir(); (self.home / ".codex").symlink_to(ext, target_is_directory=True)
        self.assertNotIn("codex", [x.id for x in detect_clients(home=self.home, project=self.project, which=lambda _: None)])

    def test_rejects_project_with_symlinked_ancestor(self) -> None:
        outside = self.root / "outside"; outside.mkdir()
        linked_root = self.root / "project-link"; linked_root.symlink_to(outside, target_is_directory=True)
        project = linked_root / "project"; (outside / "project/dist").mkdir(parents=True)
        (outside / "project/dist/index.js").write_text("// built")
        with self.assertRaises(AgentClientError):
            server_spec_from_project(project, server_name="petstore-mcp")

    def test_rejects_home_with_symlinked_ancestor(self) -> None:
        outside = self.root / "outside-home"; outside.mkdir()
        (outside / ".codex").mkdir(); (outside / ".codex/config.toml").write_text("model='x'")
        linked_home = self.root / "home-link"; linked_home.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(AgentClientError):
            detect_clients(home=linked_home, project=self.project, which=lambda _: None)
if __name__ == "__main__": unittest.main()
