#!/usr/bin/env python3
"""Live fs_write integration test for the AGY -> Kiro ACP V3 bridge.

This test lets the real `ppt-engineer` agent write one throwaway probe file, so
it exercises the full permission path end to end:

    session/request_permission (fs_write) -> policy -> allow_once -> file on disk

It is **opt-in** and skipped unless explicitly requested:

    AGY_PPT_LIVE_KIRO_WRITE=1 python3 -m unittest discover \
        -s skills/agy-ppt/tests/integration -t skills/agy-ppt/tests/integration -v

    # or directly
    python3 skills/agy-ppt/tests/integration/test_kiro_v3_acp_write.py

It never touches production files. The only writable target is:

    <repo>/.agy-ppt-integration/bridge-write-test.txt

which must contain exactly ``KIRO_WRITE_OK`` and is removed again in teardown,
together with the probe directory when it ends up empty. No API key is used and
no OAuth token is read, copied or stored.
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
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import kiro_acp_bridge as bridge_mod  # noqa: E402
from kiro_acp_bridge import (  # noqa: E402
    DEFAULT_AGENT,
    ENGINE_V3,
    PERMISSION_ALLOW_ONCE,
    STATUS_COMPLETED,
    BridgeRequest,
    KiroAcpBridge,
)

LIVE_ENV_FLAG = "AGY_PPT_LIVE_KIRO_WRITE"
PROBE_DIR_NAME = ".agy-ppt-integration"
PROBE_FILE_NAME = "bridge-write-test.txt"
PROBE_CONTENT = "KIRO_WRITE_OK"
PROBE_DIR = REPO_ROOT / PROBE_DIR_NAME
PROBE_FILE = PROBE_DIR / PROBE_FILE_NAME
PROBE_REL = f"{PROBE_DIR_NAME}/{PROBE_FILE_NAME}"
DEFAULT_TIMEOUT = float(os.environ.get("AGY_PPT_LIVE_TIMEOUT", "300"))

# Files that must never be used as a write probe.
FORBIDDEN_PROBE_PARTS = ("SKILL.md", "docs", "scripts", "tests", "assets", "references")


def live_enabled() -> bool:
    """True when the operator explicitly asked for a live Kiro write run."""
    if os.environ.get(LIVE_ENV_FLAG) == "1":
        return True
    return Path(sys.argv[0]).name == Path(__file__).name


def kiro_cli_present() -> bool:
    return shutil.which("kiro-cli") is not None


SKIP_REASON = (
    f"live Kiro write integration test: set {LIVE_ENV_FLAG}=1 (or run this file "
    "directly) with a logged-in Kiro Pro session"
)


@unittest.skipUnless(live_enabled(), SKIP_REASON)
@unittest.skipUnless(kiro_cli_present(), "kiro-cli is not on PATH")
class KiroV3AcpWriteLiveTests(unittest.TestCase):
    """One real V3 ACP turn that performs an approved fs_write."""

    result: bridge_mod.BridgeResult
    file_existed_after_turn: bool
    file_content_after_turn: str | None

    @classmethod
    def setUpClass(cls) -> None:
        # Guard: the probe path must be a throwaway location.
        assert PROBE_DIR_NAME.startswith("."), "probe dir must be a dot directory"
        for part in FORBIDDEN_PROBE_PARTS:
            assert part not in PROBE_REL.split("/"), f"probe path must not touch {part}"

        cls._dir_existed_before = PROBE_DIR.exists()
        PROBE_DIR.mkdir(parents=True, exist_ok=True)
        if PROBE_FILE.exists():
            PROBE_FILE.unlink()

        request = BridgeRequest.from_dict(
            {
                "repository_root": str(REPO_ROOT),
                "task": (
                    f"Create the file `{PROBE_REL}` containing exactly the single line "
                    f"`{PROBE_CONTENT}` (no extra text, no trailing commentary in the "
                    "file). Do not modify any other file and do not run any shell "
                    "command. Then reply with one line: WRITE_DONE."
                ),
                "allowed_scope": [PROBE_REL],
                "acceptance_criteria": [
                    f"{PROBE_REL} exists",
                    f"its content is {PROBE_CONTENT}",
                    "no other file is modified",
                ],
                "verification": ["none - the harness verifies the file"],
                "permission_mode": PERMISSION_ALLOW_ONCE,
                "allow_dependency_changes": False,
                "timeout_seconds": DEFAULT_TIMEOUT,
                "startup_timeout_seconds": 60,
                "agent_select_timeout_seconds": 60,
            }
        )
        cls.request = request
        cls.result = KiroAcpBridge(request).run()
        cls.payload = cls.result.to_dict()

        # Capture disk state before cleanup so assertions stay independent.
        cls.file_existed_after_turn = PROBE_FILE.exists()
        cls.file_content_after_turn = (
            PROBE_FILE.read_text(encoding="utf-8") if cls.file_existed_after_turn else None
        )
        if os.environ.get("AGY_PPT_LIVE_DUMP"):
            print(json.dumps(cls.payload, ensure_ascii=False, indent=2))

    @classmethod
    def tearDownClass(cls) -> None:
        if PROBE_FILE.exists():
            PROBE_FILE.unlink()
        if PROBE_DIR.exists() and not any(PROBE_DIR.iterdir()):
            PROBE_DIR.rmdir()

    # -- runtime contract --------------------------------------------------
    def test_runs_on_v3_with_cli_auth(self):
        self.assertEqual(self.result.diagnostics["engine"], ENGINE_V3)
        self.assertEqual(self.result.diagnostics["auth"], "cli")
        self.assertNotIn("--agent", self.result.diagnostics["command"])
        self.assertFalse(self.result.diagnostics["engine_fallback_used"])

    def test_agent_scope_confirmed(self):
        diagnostics = self.result.diagnostics
        self.assertEqual(diagnostics["agent_requested"], DEFAULT_AGENT)
        self.assertTrue(diagnostics["agent_resolved"], diagnostics["agent_selection"])
        self.assertTrue(diagnostics["agent_scoped"], diagnostics["agent_selection"])
        self.assertFalse(diagnostics["agent_scope_lost"])
        self.assertEqual(diagnostics["agent_selection"]["method"], "session/set_mode")
        self.assertEqual(diagnostics["agent_selection"]["current_agent"], DEFAULT_AGENT)

    def test_turn_completed(self):
        self.assertEqual(self.result.status, STATUS_COMPLETED, self.result.error_message)
        self.assertEqual(self.result.stop_reason, "end_turn")
        self.assertTrue(self.result.diagnostics["prompt_dispatched"])
        self.assertTrue(self.result.diagnostics["turn_end_observed"])

    # -- the actual write --------------------------------------------------
    def test_bridge_received_and_allowed_an_fs_write_permission(self):
        writes = [
            decision
            for decision in self.result.permission_decisions
            if decision.get("capability") in {"fs_write", "edit", "write"}
        ]
        self.assertTrue(writes, self.result.permission_decisions)
        approved = [decision for decision in writes if decision["decision"] == "allowed"]
        self.assertTrue(approved, writes)
        self.assertEqual(approved[0]["rule"], "write_within_repository")
        self.assertIn(PROBE_FILE_NAME, str(approved[0]["target"]))

    def test_probe_file_was_created_with_the_exact_content(self):
        self.assertTrue(self.file_existed_after_turn, "the agent did not create the probe file")
        self.assertEqual((self.file_content_after_turn or "").strip(), PROBE_CONTENT)

    def test_no_policy_violations(self):
        self.assertEqual(self.result.policy_violations, [])

    def test_no_write_outside_the_repository_was_approved(self):
        for decision in self.result.permission_decisions:
            if decision["decision"] != "allowed":
                continue
            self.assertNotEqual(decision["rule"], "write_outside_repository")

    def test_control_returns_to_agy(self):
        self.assertEqual(self.payload["control"], "returned_to_agy")
        self.assertEqual(self.payload["next_step_owner"], "AGY")

    def test_no_credential_leaked_into_the_result(self):
        self.assertTrue(self.result.diagnostics["oauth_only"])
        self.assertFalse(self.result.diagnostics["api_key_used"])
        wire = json.dumps(self.payload, ensure_ascii=False)
        self.assertNotIn("Bearer ", wire)


def main() -> int:
    if not live_enabled():
        print(SKIP_REASON)
        return 0
    if not kiro_cli_present():
        print("kiro-cli is not on PATH")
        return 1
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(KiroV3AcpWriteLiveTests)
    return 0 if runner.run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
