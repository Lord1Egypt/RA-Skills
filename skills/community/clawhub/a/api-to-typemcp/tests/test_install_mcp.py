"""Safety tests for atomic MCP configuration installation and rollback."""
from __future__ import annotations
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/api-to-typemcp/scripts"))
from agent_clients import McpServerSpec  # noqa: E402
import install_mcp as installer  # noqa: E402
from install_mcp import InstallError, apply_json_plan, apply_json_target, apply_native_plan  # noqa: E402
from install_plan import build_plan, issue_install_receipt  # noqa: E402


class AtomicInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.state = self.root / "state"; self.state.mkdir()
        self.previous = os.environ.get("TYPE_MCP_APPROVAL_STATE_DIR"); os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = str(self.state)
        self.home = self.root / "home"; (self.home / ".cursor").mkdir(parents=True)
        self.config = self.home / ".cursor/mcp.json"; self.original = b'{"mcpServers":{"other":{"command":"node"}}}\n'; self.config.write_bytes(self.original)
        self.spec = McpServerSpec("petstore-mcp", "node", ("/safe/dist/index.js",), self.root, ("TYPE_MCP_API_KEY",))
        self.plan = build_plan(self.spec, selected=("cursor",), home=self.home)
    def tearDown(self) -> None:
        if self.previous is None: os.environ.pop("TYPE_MCP_APPROVAL_STATE_DIR", None)
        else: os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = self.previous
        self.tmp.cleanup()
    def test_apply_creates_mode_600_backup_and_adds_server(self) -> None:
        issue_install_receipt(self.plan)
        result = apply_json_target(self.plan.targets[0], self.spec, plan=self.plan)
        self.assertTrue(result.backup_path.is_file())
        self.assertEqual(result.backup_path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(json.loads(self.config.read_text())["mcpServers"]["petstore-mcp"]["command"], "node")
    def test_apply_rejects_changed_fingerprint_without_writing(self) -> None:
        self.config.write_text('{"mcpServers":{"changed":{}}}\n')
        issue_install_receipt(self.plan)
        with self.assertRaises(InstallError): apply_json_target(self.plan.targets[0], self.spec, plan=self.plan)
        self.assertEqual(self.config.read_text(), '{"mcpServers":{"changed":{}}}\n')

    def test_apply_refuses_existing_backup_without_mutating_config(self) -> None:
        backup = self.plan.targets[0].backup_path
        backup.write_text("attacker backup", encoding="utf-8")
        issue_install_receipt(self.plan)

        with self.assertRaises(InstallError):
            apply_json_target(self.plan.targets[0], self.spec, plan=self.plan)

        self.assertEqual(self.config.read_bytes(), self.original)
        self.assertEqual(backup.read_text(encoding="utf-8"), "attacker backup")

    def test_apply_rechecks_content_after_backup_before_replace(self) -> None:
        original_backup = installer._exclusive_backup
        def race(parent_fd: int, name: str, content: bytes) -> None:
            original_backup(parent_fd, name, content)
            self.config.write_text('{"mcpServers":{"raced":{}}}\n', encoding="utf-8")
        issue_install_receipt(self.plan)

        with patch.object(installer, "_exclusive_backup", side_effect=race), self.assertRaises(InstallError):
            apply_json_target(self.plan.targets[0], self.spec, plan=self.plan)

        self.assertIn("raced", json.loads(self.config.read_text())["mcpServers"])
    def test_failed_verification_restores_target_backup(self) -> None:
        issue_install_receipt(self.plan)
        with self.assertRaises(InstallError):
            apply_json_target(self.plan.targets[0], self.spec, plan=self.plan, verifier=lambda: False)
        self.assertEqual(self.config.read_bytes(), self.original)

    def test_plan_receipt_is_consumed_once_for_multiple_targets(self) -> None:
        gemini = self.home / ".gemini"; gemini.mkdir()
        (gemini / "settings.json").write_text('{"mcpServers":{}}\n')
        plan = build_plan(self.spec, selected=("cursor", "gemini-cli"), home=self.home)
        issue_install_receipt(plan)

        results = apply_json_plan(plan, self.spec)

        self.assertEqual([result.status for result in results], ["verified", "verified"])
        self.assertIn("petstore-mcp", json.loads(self.config.read_text())["mcpServers"])
        self.assertIn("petstore-mcp", json.loads((gemini / "settings.json").read_text())["mcpServers"])

    def test_batch_failure_restores_prior_target(self) -> None:
        gemini = self.home / ".gemini"; gemini.mkdir()
        gemini_config = gemini / "settings.json"; gemini_original = b'{"mcpServers":{}}\n'; gemini_config.write_bytes(gemini_original)
        plan = build_plan(self.spec, selected=("cursor", "gemini-cli"), home=self.home)
        plan.targets[1].backup_path.write_text("block later backup", encoding="utf-8")
        issue_install_receipt(plan)

        with self.assertRaises(InstallError):
            apply_json_plan(plan, self.spec)

        self.assertEqual(self.config.read_bytes(), self.original)
        self.assertEqual(gemini_config.read_bytes(), gemini_original)

    def test_opencode_uses_its_native_mcp_servers_shape(self) -> None:
        opencode_dir = self.home / ".config/opencode"; opencode_dir.mkdir(parents=True)
        opencode = opencode_dir / "opencode.json"; opencode.write_text('{"mcp":{"servers":{}}}\n')
        plan = build_plan(self.spec, selected=("opencode",), home=self.home)
        issue_install_receipt(plan)

        apply_json_plan(plan, self.spec)

        entry = json.loads(opencode.read_text())["mcp"]["servers"]["petstore-mcp"]
        self.assertEqual(entry["command"], ["node", "/safe/dist/index.js"])
        self.assertNotIn("args", entry)

    def test_codex_appends_native_toml_without_rewriting_profiles(self) -> None:
        codex = self.home / ".codex"; codex.mkdir()
        config = codex / "config.toml"; config.write_text("model = 'x'\n\n[profiles.safe]\nmodel = 'safe'\n")
        plan = build_plan(self.spec, selected=("codex",), home=self.home)
        issue_install_receipt(plan)

        apply_native_plan(plan, self.spec)

        content = config.read_text()
        self.assertIn("[profiles.safe]", content)
        self.assertIn("[mcp_servers.petstore_mcp]", content)
if __name__ == "__main__": unittest.main()
