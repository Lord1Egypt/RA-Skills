"""Tests for secret-free MCP installation plans and portable export."""
from __future__ import annotations
import json
import os
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/api-to-typemcp/scripts"))
from agent_clients import McpServerSpec  # noqa: E402
from install_plan import (  # noqa: E402
    InstallPlanError,
    build_plan,
    issue_install_receipt,
    validate_install_receipt,
    write_portable_export,
)


class InstallPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.state = self.root / "state"; self.state.mkdir()
        self._previous_state = os.environ.get("TYPE_MCP_APPROVAL_STATE_DIR")
        os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = str(self.state)
        self.project = self.root / "project"; self.project.mkdir()
        self.spec = McpServerSpec("petstore-mcp", "node", ("/safe/project/dist/index.js",), self.project, ("TYPE_MCP_API_KEY",))
        self.home = self.root / "home"; (self.home / ".codex").mkdir(parents=True)
        (self.home / ".codex/config.toml").write_text("model='x'\n")
    def tearDown(self) -> None:
        if self._previous_state is None:
            os.environ.pop("TYPE_MCP_APPROVAL_STATE_DIR", None)
        else:
            os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = self._previous_state
        self.tmp.cleanup()
    def test_plan_is_secret_free_and_fingerprint_bound(self) -> None:
        plan = build_plan(self.spec, selected=("codex",), home=self.home)
        public = plan.to_public_dict()
        self.assertEqual(public["targets"][0]["action"], "add")
        self.assertRegex(public["targets"][0]["config_fingerprint"], r"^sha256:[0-9a-f]{64}$")
        self.assertIn("TYPE_MCP_API_KEY", json.dumps(public))
        self.assertNotIn("real-secret", json.dumps(public))
    def test_plan_rejects_missing_native_configuration(self) -> None:
        with self.assertRaises(InstallPlanError):
            build_plan(self.spec, selected=("gemini-cli",), home=self.home)

    def test_duplicate_name_requires_explicit_replace(self) -> None:
        (self.home / ".cursor").mkdir(); (self.home / ".cursor/mcp.json").write_text('{"mcpServers":{"petstore-mcp":{}}}')
        with self.assertRaises(InstallPlanError):
            build_plan(self.spec, selected=("cursor",), home=self.home)

    def test_codex_duplicate_uses_toml_structure_not_exact_text(self) -> None:
        (self.home / ".codex/config.toml").write_text('[mcp_servers."petstore_mcp"]\ncommand = "old"\n')
        with self.assertRaises(InstallPlanError):
            build_plan(self.spec, selected=("codex",), home=self.home)
    def test_portable_export_contains_descriptor_not_values(self) -> None:
        output = write_portable_export(self.project, self.spec)
        data = json.loads(output.read_text())
        self.assertEqual(data["mcpServers"]["petstore-mcp"]["command"], "node")
        self.assertNotIn("TYPE_MCP_API_KEY", output.read_text())
        self.assertFalse((self.project / ".cursor/mcp.json").exists())

    def test_plan_rejects_symlinked_config_parent(self) -> None:
        external = self.root / "external-codex"
        external.mkdir()
        (external / "config.toml").write_text("model='outside'\n", encoding="utf-8")
        (self.home / ".codex" / "config.toml").unlink()
        (self.home / ".codex").rmdir()
        (self.home / ".codex").symlink_to(external, target_is_directory=True)

        with self.assertRaises(InstallPlanError):
            build_plan(self.spec, selected=("codex",), home=self.home)

    def test_plan_rejects_home_with_symlinked_ancestor(self) -> None:
        outside = self.root / "outside-home"
        outside.mkdir()
        (outside / "home" / ".codex").mkdir(parents=True)
        (outside / "home" / ".codex" / "config.toml").write_text("model='outside'\n", encoding="utf-8")
        linked_parent = self.root / "home-parent-link"
        linked_parent.symlink_to(outside, target_is_directory=True)
        linked_home = linked_parent / "home"

        with self.assertRaises(InstallPlanError):
            build_plan(self.spec, selected=("codex",), home=linked_home)

    def test_portable_export_rejects_literal_secret_like_argument(self) -> None:
        unsafe = McpServerSpec("petstore-mcp", "node", ("/safe/dist/index.js", "--token=real-secret"), self.project)
        with self.assertRaises(InstallPlanError):
            write_portable_export(self.project, unsafe)

    def test_portable_export_rejects_existing_symlinked_directory(self) -> None:
        external = self.root / "external-export"
        external.mkdir()
        (self.project / "agent-install").symlink_to(external, target_is_directory=True)

        with self.assertRaises(InstallPlanError):
            write_portable_export(self.project, self.spec)

    def test_portable_export_rejects_project_with_symlinked_ancestor(self) -> None:
        outside = self.root / "outside-project"
        (outside / "project").mkdir(parents=True)
        linked_parent = self.root / "project-parent-link"
        linked_parent.symlink_to(outside, target_is_directory=True)

        with self.assertRaises(InstallPlanError):
            write_portable_export(linked_parent / "project", self.spec)

    def test_install_receipt_is_bound_to_exact_plan_and_single_use(self) -> None:
        plan = build_plan(self.spec, selected=("codex",), home=self.home)
        receipt = issue_install_receipt(plan)

        validate_install_receipt(plan)
        with self.assertRaises(InstallPlanError):
            validate_install_receipt(plan)

    def test_install_receipt_rejects_changed_target_plan(self) -> None:
        plan = build_plan(self.spec, selected=("codex",), home=self.home)
        issue_install_receipt(plan)
        changed_spec = McpServerSpec("other-mcp", "node", self.spec.args, self.project, self.spec.env_names)
        changed_plan = build_plan(changed_spec, selected=("codex",), home=self.home)

        with self.assertRaises(InstallPlanError):
            validate_install_receipt(changed_plan)

    def test_install_receipt_binds_full_target_list(self) -> None:
        plan = build_plan(self.spec, selected=("codex",), home=self.home)
        issue_install_receipt(plan)
        (self.home / ".cursor").mkdir()
        (self.home / ".cursor" / "mcp.json").write_text('{"mcpServers":{}}\n')
        changed_plan = build_plan(self.spec, selected=("codex", "cursor"), home=self.home)

        with self.assertRaises(InstallPlanError):
            validate_install_receipt(changed_plan)
if __name__ == "__main__": unittest.main()
