#!/usr/bin/env python3
"""Live integration test for the AGY -> Kiro ACP V3 bridge.

This test talks to the real `kiro-cli` using the Kiro Pro session that is
already logged in on this machine. It is therefore **opt-in** and is skipped
unless it is run deliberately:

    AGY_PPT_LIVE_KIRO=1 python3 -m unittest discover \
        -s skills/agy-ppt/tests/integration -t skills/agy-ppt/tests/integration -v

    # or directly
    python3 skills/agy-ppt/tests/integration/test_kiro_v3_acp.py

It is not part of the normal unit-test run and must never be required by CI:
`skills/agy-ppt/tests/test_kiro_acp_bridge.py` covers the same contract with an
in-process fake agent.

Minimum success criteria:

    engine           = v3
    auth             = cli
    agent_requested  = ppt-engineer
    agent_resolved   = true
    agent_scoped     = true
    stop_reason      = end_turn

No API key is used and no OAuth token is read, copied or stored. The task is
read-only and every tool permission request is rejected, so the live run cannot
modify the repository.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
REPO_ROOT = TESTS_DIR.parents[2]
for candidate in (str(SCRIPTS_DIR),):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

import kiro_acp_bridge as bridge_mod  # noqa: E402
from kiro_acp_bridge import (  # noqa: E402
    DEFAULT_AGENT,
    ENGINE_V3,
    PERMISSION_REJECT,
    STATUS_COMPLETED,
    BridgeRequest,
    KiroAcpBridge,
)

LIVE_ENV_FLAG = "AGY_PPT_LIVE_KIRO"
MARKER = "AGY_BRIDGE_LIVE_OK"
DEFAULT_TIMEOUT = float(os.environ.get("AGY_PPT_LIVE_TIMEOUT", "300"))


def live_enabled() -> bool:
    """True when the operator explicitly asked for a live Kiro run."""
    if os.environ.get(LIVE_ENV_FLAG) == "1":
        return True
    # Running the file directly counts as an explicit request.
    return Path(sys.argv[0]).name == Path(__file__).name


def kiro_cli_present() -> bool:
    return shutil.which("kiro-cli") is not None


SKIP_REASON = (
    f"live Kiro integration test: set {LIVE_ENV_FLAG}=1 (or run this file directly) "
    "with a logged-in Kiro Pro session"
)


@unittest.skipUnless(live_enabled(), SKIP_REASON)
@unittest.skipUnless(kiro_cli_present(), "kiro-cli is not on PATH")
class KiroV3AcpLiveTests(unittest.TestCase):
    """One real V3 ACP turn, executed as ppt-engineer."""

    result: bridge_mod.BridgeResult

    @classmethod
    def setUpClass(cls) -> None:
        request = BridgeRequest.from_dict(
            {
                "repository_root": str(REPO_ROOT),
                "task": (
                    "Read-only bridge integration check. Do not create, modify or delete "
                    "any file, and do not run any command. Reply with exactly one line: "
                    f"{MARKER}"
                ),
                "allowed_scope": ["none - read only check"],
                "acceptance_criteria": [f"reply {MARKER}", "no file changes"],
                "verification": ["none"],
                # Reject every tool permission request: the live run must not be
                # able to touch the working tree.
                "permission_mode": PERMISSION_REJECT,
                "timeout_seconds": DEFAULT_TIMEOUT,
                "startup_timeout_seconds": 60,
                "agent_select_timeout_seconds": 60,
            }
        )
        cls.request = request
        cls.result = KiroAcpBridge(request).run()
        cls.payload = cls.result.to_dict()
        if os.environ.get("AGY_PPT_LIVE_DUMP"):
            print(json.dumps(cls.payload, ensure_ascii=False, indent=2))

    # -- launch contract ---------------------------------------------------
    def test_launches_v3_acp_with_cli_auth(self):
        command = self.result.diagnostics["command"]
        self.assertEqual(command[0], "kiro-cli")
        self.assertIn("--v3", command)
        self.assertIn("acp", command)
        self.assertEqual(command[command.index("--auth-method") + 1], "cli")
        # v3 rejects --agent on the acp subcommand.
        self.assertNotIn("--agent", command)
        self.assertEqual(self.result.diagnostics["engine"], ENGINE_V3)
        self.assertEqual(self.result.diagnostics["auth"], "cli")

    def test_no_api_key_is_used(self):
        self.assertFalse(self.result.diagnostics["api_key_used"])
        self.assertTrue(self.result.diagnostics["oauth_only"])
        wire = json.dumps(self.payload, ensure_ascii=False)
        self.assertNotIn("KIRO_API_KEY=", wire)
        self.assertNotIn("Bearer ", wire)

    # -- protocol ----------------------------------------------------------
    def test_initialize_and_session_new_succeeded(self):
        self.assertEqual(self.result.diagnostics["protocol_version"], 1)
        self.assertTrue(self.result.session_id)
        events = [entry["event"] for entry in self.result.timeline]
        self.assertIn("initialized", events)
        self.assertIn("session_created", events)

    def test_agent_swap_and_scope(self):
        diagnostics = self.result.diagnostics
        self.assertEqual(diagnostics["agent_requested"], DEFAULT_AGENT)
        self.assertTrue(diagnostics["agent_resolved"], diagnostics["agent_selection"])
        self.assertTrue(diagnostics["agent_scoped"], diagnostics["agent_selection"])

        selection = diagnostics["agent_selection"]
        self.assertEqual(selection["method"], "session/set_mode")
        self.assertEqual(selection["current_agent"], DEFAULT_AGENT)
        self.assertIn(DEFAULT_AGENT, selection["available_agents"])
        self.assertIsNotNone(selection["confirmed_via"])

    def test_agent_scoped_before_prompt(self):
        events = [entry["event"] for entry in self.result.timeline]
        self.assertIn("agent_scoped", events)
        self.assertIn("prompt_sent", events)
        self.assertLess(events.index("agent_scoped"), events.index("prompt_sent"))

    def test_turn_completed(self):
        self.assertEqual(self.result.status, STATUS_COMPLETED, self.result.error_message)
        self.assertEqual(self.result.stop_reason, "end_turn")
        self.assertTrue(self.result.diagnostics["turn_end_observed"])
        self.assertTrue(self.result.diagnostics["prompt_dispatched"])

    def test_agent_answered_the_marker(self):
        self.assertIn(MARKER, self.result.agent_text)

    # -- boundaries --------------------------------------------------------
    def test_no_engine_fallback_and_no_warnings(self):
        self.assertFalse(self.result.diagnostics["engine_fallback_used"])
        self.assertEqual(self.result.warnings, [])

    def test_no_codex_invocation_was_attempted(self):
        codex = [
            violation
            for violation in self.result.policy_violations
            if violation.get("rule") == "kiro_must_not_call_codex"
        ]
        self.assertEqual(codex, [])

    def test_control_returns_to_agy(self):
        self.assertEqual(self.payload["control"], "returned_to_agy")
        self.assertEqual(self.payload["next_step_owner"], "AGY")

    def test_working_tree_was_not_modified(self):
        # permission_mode=reject means any write attempt was refused.
        allowed_writes = [
            decision
            for decision in self.result.permission_decisions
            if decision.get("decision") == "allowed"
        ]
        self.assertEqual(allowed_writes, [])


def main() -> int:
    if not live_enabled():
        print(SKIP_REASON)
        return 0
    if not kiro_cli_present():
        print("kiro-cli is not on PATH")
        return 1
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(KiroV3AcpLiveTests)
    return 0 if runner.run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
