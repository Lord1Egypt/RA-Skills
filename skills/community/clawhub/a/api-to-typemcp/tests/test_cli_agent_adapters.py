"""Test-first contracts for official CLI-based MCP registration."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/api-to-typemcp/scripts"))

from agent_clients import McpServerSpec  # noqa: E402
from install_plan import build_plan, issue_install_receipt  # noqa: E402
from install_mcp import InstallError, apply_native_plan  # noqa: E402


class CliAgentAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.state = self.root / "state"
        self.state.mkdir()
        self.previous_state = os.environ.get("TYPE_MCP_APPROVAL_STATE_DIR")
        os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = str(self.state)
        self.spec = McpServerSpec(
            "petstore-mcp",
            "node",
            ("/safe/project/dist/index.js",),
            Path("/safe/project"),
            ("TYPE_MCP_BASE_URL",),
        )

    def tearDown(self) -> None:
        if self.previous_state is None:
            os.environ.pop("TYPE_MCP_APPROVAL_STATE_DIR", None)
        else:
            os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = self.previous_state
        self.tmp.cleanup()

    def test_hermes_cli_add_then_test_is_receipt_gated_and_secret_free(self) -> None:
        plan = build_plan(self.spec, selected=("hermes",), home=self.home)
        self.assertEqual(plan.targets[0].action, "cli-add")
        self.assertEqual(plan.targets[0].verification, "hermes-mcp-test")
        self.assertNotIn("TYPE_MCP_BASE_URL=", str(plan.to_public_dict()))

        calls: list[list[str]] = []

        def runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

        with self.assertRaises(InstallError):
            apply_native_plan(plan, self.spec, runner=runner)
        self.assertEqual(calls, [])

        issue_install_receipt(plan)
        result = apply_native_plan(plan, self.spec, runner=runner)

        self.assertEqual(result[0].client_id, "hermes")
        self.assertEqual(calls, [
            ["hermes", "mcp", "add", "petstore-mcp", "--command", "node", "--args", "/safe/project/dist/index.js"],
            ["hermes", "mcp", "test", "petstore-mcp"],
        ])

    def test_claude_code_uses_official_stdio_separator_and_connected_list_verification(self) -> None:
        plan = build_plan(self.spec, selected=("claude-code",), home=self.home)
        calls: list[list[str]] = []

        def runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            stdout = "petstore-mcp: ✔ Connected" if command[-1] == "list" else "Added petstore-mcp"
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

        issue_install_receipt(plan)
        result = apply_native_plan(plan, self.spec, runner=runner)

        self.assertEqual(result[0].client_id, "claude-code")
        self.assertEqual(calls, [
            ["claude", "mcp", "add", "--transport", "stdio", "petstore-mcp", "--", "node", "/safe/project/dist/index.js"],
            ["claude", "mcp", "list"],
        ])

    def test_claude_code_named_but_unhealthy_server_is_removed(self) -> None:
        plan = build_plan(self.spec, selected=("claude-code",), home=self.home)
        calls: list[list[str]] = []

        def runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            stdout = "petstore-mcp: ! Needs authentication" if command[-1] == "list" else "Added petstore-mcp"
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

        issue_install_receipt(plan)
        with self.assertRaisesRegex(InstallError, "Claude Code MCP verification failed"):
            apply_native_plan(plan, self.spec, runner=runner)
        self.assertEqual(calls[-1], ["claude", "mcp", "remove", "petstore-mcp"])

    def test_claude_code_does_not_accept_a_different_server_name_as_connected(self) -> None:
        plan = build_plan(self.spec, selected=("claude-code",), home=self.home)
        calls: list[list[str]] = []

        def runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            stdout = "petstore-mcp-old: ✔ Connected" if command[-1] == "list" else "Added petstore-mcp"
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

        issue_install_receipt(plan)
        with self.assertRaisesRegex(InstallError, "Claude Code MCP verification failed"):
            apply_native_plan(plan, self.spec, runner=runner)
        self.assertEqual(calls[-1], ["claude", "mcp", "remove", "petstore-mcp"])

    def test_hermes_add_failure_attempts_compensating_remove(self) -> None:
        plan = build_plan(self.spec, selected=("hermes",), home=self.home)
        calls: list[list[str]] = []

        def runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            return subprocess.CompletedProcess(
                command,
                1 if command[2] == "add" else 0,
                stdout="",
                stderr="write may have occurred",
            )

        issue_install_receipt(plan)
        with self.assertRaisesRegex(InstallError, "Hermes MCP registration failed"):
            apply_native_plan(plan, self.spec, runner=runner)
        self.assertEqual(calls, [
            ["hermes", "mcp", "add", "petstore-mcp", "--command", "node", "--args", "/safe/project/dist/index.js"],
            ["hermes", "mcp", "remove", "petstore-mcp"],
        ])

    def test_official_cli_registration_preserves_all_server_arguments(self) -> None:
        spec = McpServerSpec(
            "petstore-mcp",
            "node",
            ("/safe/project/dist/index.js", "--enable-source-maps"),
            Path("/safe/project"),
        )
        plan = build_plan(spec, selected=("hermes", "claude-code"), home=self.home)
        calls: list[list[str]] = []

        def runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            stdout = "petstore-mcp: ✔ Connected" if command[-1] == "list" else "ok"
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

        issue_install_receipt(plan)
        apply_native_plan(plan, spec, runner=runner)
        self.assertEqual(calls, [
            ["hermes", "mcp", "add", "petstore-mcp", "--command", "node", "--args", "/safe/project/dist/index.js", "--enable-source-maps"],
            ["hermes", "mcp", "test", "petstore-mcp"],
            ["claude", "mcp", "add", "--transport", "stdio", "petstore-mcp", "--", "node", "/safe/project/dist/index.js", "--enable-source-maps"],
            ["claude", "mcp", "list"],
        ])

    def test_failed_cli_verification_reports_failure_without_direct_config_mutation(self) -> None:
        plan = build_plan(self.spec, selected=("hermes",), home=self.home)

        calls: list[list[str]] = []

        def failing_runner(command: list[str]) -> subprocess.CompletedProcess[str]:
            calls.append(command)
            return subprocess.CompletedProcess(
                command,
                1 if command == ["hermes", "mcp", "test", "petstore-mcp"] else 0,
                stdout="",
                stderr="connection failed",
            )

        issue_install_receipt(plan)
        with self.assertRaisesRegex(InstallError, "Hermes MCP verification failed"):
            apply_native_plan(plan, self.spec, runner=failing_runner)
        self.assertEqual(calls, [
            ["hermes", "mcp", "add", "petstore-mcp", "--command", "node", "--args", "/safe/project/dist/index.js"],
            ["hermes", "mcp", "test", "petstore-mcp"],
            ["hermes", "mcp", "remove", "petstore-mcp"],
        ])


if __name__ == "__main__":
    unittest.main()
