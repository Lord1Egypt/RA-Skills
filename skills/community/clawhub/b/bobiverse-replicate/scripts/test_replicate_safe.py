import argparse
import io
import json
import shutil
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock
import importlib.util
import uuid


sys.dont_write_bytecode = True

SPEC = importlib.util.spec_from_file_location(
    "replicate_safe", Path(__file__).with_name("replicate_safe.py")
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


REPO_ROOT = Path(__file__).resolve().parents[3]
TEST_TMP_ROOT = REPO_ROOT / ".tmp-tests" / "replicate-safe"


class ReplicateSafeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if TEST_TMP_ROOT.exists():
            for candidate in TEST_TMP_ROOT.glob("case-*"):
                shutil.rmtree(candidate, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        try:
            TEST_TMP_ROOT.rmdir()
        except OSError:
            pass
        try:
            TEST_TMP_ROOT.parent.rmdir()
        except OSError:
            pass

    def setUp(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.test_dir = TEST_TMP_ROOT / f"case-{uuid.uuid4().hex}"
        self.test_dir.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)
        self.home = self.test_dir / "home"
        self.openclaw_root = self.home / ".openclaw"
        self.openclaw_root.mkdir(parents=True)
        self.home_patcher = mock.patch.object(MODULE.Path, "home", return_value=self.home)
        self.home_patcher.start()
        self.addCleanup(self.home_patcher.stop)

    def create_workspace(
        self,
        name: str = "workspace-parent",
        *,
        with_required_files: bool = True,
    ) -> Path:
        workspace = self.openclaw_root / name
        workspace.mkdir(parents=True, exist_ok=True)
        if with_required_files:
            for filename in MODULE.WORKSPACE_ROOT_FILES:
                (workspace / filename).write_text(f"{filename}\n", encoding="utf-8")
        return workspace

    def make_args(self, parent_workspace: Path, clone_id: str = "Bob-2-TestSystem-2026-04-03"):
        return argparse.Namespace(clone_id=clone_id, parent_workspace=str(parent_workspace))

    def run_command(self, argv, *, now=None):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = MODULE.run(argv, current_time=now)
        return result, buffer.getvalue()

    def read_audit(self):
        audit_path = self.openclaw_root / "replication-audit.log"
        if not audit_path.exists():
            return []
        return [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines() if line]

    def test_ensure_within_openclaw_rejects_escape(self):
        outside = self.test_dir / "outside"
        outside.mkdir()
        with self.assertRaises(ValueError):
            MODULE.ensure_within_openclaw(outside, self.openclaw_root)

    def test_build_plan_happy_path(self):
        parent = self.create_workspace()
        plan = MODULE.build_plan(self.make_args(parent), self.openclaw_root)
        self.assertEqual(plan.agent_id, "bob-2-testsystem-2026-04-03")
        self.assertEqual(plan.parent_workspace, parent.resolve())
        self.assertTrue(str(plan.clone_workspace).endswith("workspace-bob-2-testsystem-2026-04-03"))
        self.assertTrue(str(plan.staging_workspace).endswith(".replication-staging-bob-2-testsystem-2026-04-03"))

    def test_build_plan_rejects_openclaw_root_parent(self):
        with self.assertRaises(ValueError):
            MODULE.build_plan(self.make_args(self.openclaw_root), self.openclaw_root)

    def test_build_plan_rejects_non_workspace_directory_name(self):
        parent = self.create_workspace(name="agents-parent")
        with self.assertRaises(ValueError):
            MODULE.build_plan(self.make_args(parent), self.openclaw_root)

    def test_build_plan_rejects_nested_workspace_descendant(self):
        parent = self.openclaw_root / "archives" / "workspace-parent"
        parent.mkdir(parents=True, exist_ok=True)
        for filename in MODULE.WORKSPACE_ROOT_FILES:
            (parent / filename).write_text(f"{filename}\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            MODULE.build_plan(self.make_args(parent), self.openclaw_root)

    def test_build_plan_rejects_missing_required_root_files(self):
        parent = self.create_workspace(with_required_files=False)
        (parent / "SOUL.md").write_text("SOUL.md\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            MODULE.build_plan(self.make_args(parent), self.openclaw_root)

    def test_build_plan_rejects_symlink_entries(self):
        parent = self.create_workspace()
        fake_link = mock.Mock()
        fake_link.is_symlink.return_value = True
        fake_link.__str__ = mock.Mock(return_value="workspace-parent/outside-link")
        with mock.patch.object(MODULE.Path, "rglob", return_value=[fake_link]):
            with self.assertRaises(ValueError):
                MODULE.build_plan(self.make_args(parent), self.openclaw_root)

    def test_dry_run_creates_pending_approval_and_nonce_token(self):
        parent = self.create_workspace()
        now = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            result, stdout = self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=now,
            )

        self.assertEqual(result, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["event"], "dry-run-created")
        self.assertEqual(payload["confirm_token"], "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123")

        approval_path = self.openclaw_root / "replication-pending" / "Bob-2-TestSystem-2026-04-03.json"
        self.assertTrue(approval_path.exists())
        approval = json.loads(approval_path.read_text(encoding="utf-8"))
        self.assertEqual(approval["nonce"], "nonce123")
        self.assertEqual(approval["purpose"], "specialized code review clone")

        audit = self.read_audit()
        self.assertEqual([entry["event"] for entry in audit], ["dry-run-created"])

    def test_execute_requires_pending_approval(self):
        parent = self.create_workspace()
        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                ]
            )

    def test_execute_rejects_mismatched_nonce(self):
        parent = self.create_workspace()
        now = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=now,
            )

        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 wrongnonce",
                ],
                now=now + timedelta(minutes=1),
            )

    def test_execute_rejects_mismatched_purpose(self):
        parent = self.create_workspace()
        now = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=now,
            )

        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized design clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                ],
                now=now + timedelta(minutes=1),
            )

    def test_execute_rejects_mismatched_parent_workspace(self):
        parent = self.create_workspace()
        other_parent = self.create_workspace(name="workspace-other")
        now = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=now,
            )

        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(other_parent),
                    "--purpose",
                    "specialized code review clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                ],
                now=now + timedelta(minutes=1),
            )

    def test_execute_rejects_expired_pending_approval(self):
        parent = self.create_workspace()
        now = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=now,
            )

        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                ],
                now=now + MODULE.PENDING_APPROVAL_TTL + timedelta(seconds=1),
            )

        approval_path = self.openclaw_root / "replication-pending" / "Bob-2-TestSystem-2026-04-03.json"
        self.assertFalse(approval_path.exists())

    def test_high_workspace_count_requires_explicit_acknowledgement(self):
        parent = self.create_workspace()
        for index in range(1, 10):
            self.create_workspace(name=f"workspace-{index}")

        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ]
            )

        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            result, _ = self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                    "--allow-high-workspace-count",
                ]
            )
        self.assertEqual(result, 0)

    def test_cooldown_blocks_execute_without_override_but_preserves_pending_approval(self):
        parent = self.create_workspace()
        base_time = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=base_time,
            )

        MODULE.write_audit(
            self.openclaw_root,
            {
                "timestamp_utc": (base_time - timedelta(hours=2)).isoformat(),
                "event": "execute-started",
            },
        )

        with self.assertRaises(ValueError):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                ],
                now=base_time,
            )

        approval_path = self.openclaw_root / "replication-pending" / "Bob-2-TestSystem-2026-04-03.json"
        self.assertTrue(approval_path.exists())

    def test_failed_execute_rolls_back_clone_and_audits_failure(self):
        parent = self.create_workspace()
        (parent / "notes.txt").write_text("parent data\n", encoding="utf-8")
        base_time = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=base_time,
            )

        with mock.patch.object(
            MODULE.subprocess,
            "run",
            side_effect=subprocess.CalledProcessError(1, ["openclaw"]),
        ):
            with self.assertRaises(subprocess.CalledProcessError):
                self.run_command(
                    [
                        "--clone-id",
                        "Bob-2-TestSystem-2026-04-03",
                        "--parent-workspace",
                        str(parent),
                        "--purpose",
                        "specialized code review clone",
                        "--execute",
                        "--confirm",
                        "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                    ],
                    now=base_time + timedelta(minutes=1),
                )

        clone_workspace = self.openclaw_root / "workspace-bob-2-testsystem-2026-04-03"
        staging_workspace = self.openclaw_root / ".replication-staging-bob-2-testsystem-2026-04-03"
        approval_path = self.openclaw_root / "replication-pending" / "Bob-2-TestSystem-2026-04-03.json"
        self.assertFalse(clone_workspace.exists())
        self.assertFalse(staging_workspace.exists())
        self.assertFalse(approval_path.exists())

        events = [entry["event"] for entry in self.read_audit()]
        self.assertEqual(events, ["dry-run-created", "execute-started", "execute-failed"])

    def test_successful_execute_consumes_pending_and_uses_shell_false(self):
        parent = self.create_workspace()
        (parent / "notes.txt").write_text("parent data\n", encoding="utf-8")
        base_time = datetime(2026, 4, 3, 21, 0, tzinfo=timezone.utc)
        with mock.patch.object(MODULE.secrets, "token_urlsafe", return_value="nonce123"):
            self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                ],
                now=base_time,
            )

        with mock.patch.object(MODULE.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as mocked_run:
            result, stdout = self.run_command(
                [
                    "--clone-id",
                    "Bob-2-TestSystem-2026-04-03",
                    "--parent-workspace",
                    str(parent),
                    "--purpose",
                    "specialized code review clone",
                    "--execute",
                    "--confirm",
                    "REPLICATE Bob-2-TestSystem-2026-04-03 nonce123",
                    "--override-cooldown-reason",
                    "mission requires immediate execution",
                ],
                now=base_time + timedelta(minutes=1),
            )

        self.assertEqual(result, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["event"], "execute-succeeded")
        clone_workspace = self.openclaw_root / "workspace-bob-2-testsystem-2026-04-03"
        approval_path = self.openclaw_root / "replication-pending" / "Bob-2-TestSystem-2026-04-03.json"
        self.assertTrue(clone_workspace.exists())
        self.assertTrue((clone_workspace / "notes.txt").exists())
        self.assertFalse(approval_path.exists())

        mocked_run.assert_called_once()
        command = mocked_run.call_args.args[0]
        self.assertEqual(
            command,
            [
                "openclaw",
                "agents",
                "add",
                "bob-2-testsystem-2026-04-03",
                "--workspace",
                str(clone_workspace),
            ],
        )
        self.assertFalse(mocked_run.call_args.kwargs["shell"])
        self.assertTrue(mocked_run.call_args.kwargs["check"])

        events = [entry["event"] for entry in self.read_audit()]
        self.assertEqual(events, ["dry-run-created", "execute-started", "execute-succeeded"])

    def test_last_execute_time_reads_latest_execute_attempt(self):
        older = datetime.now(timezone.utc) - timedelta(days=2)
        newer = datetime.now(timezone.utc) - timedelta(hours=2)
        MODULE.write_audit(
            self.openclaw_root,
            {"timestamp_utc": older.isoformat(), "event": "execute-started"},
        )
        MODULE.write_audit(
            self.openclaw_root,
            {"timestamp_utc": newer.isoformat(), "event": "execute-failed"},
        )
        MODULE.write_audit(
            self.openclaw_root,
            {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "event": "dry-run-created"},
        )

        last = MODULE.last_execute_time(self.openclaw_root)
        self.assertIsNotNone(last)
        assert last is not None
        self.assertEqual(last.replace(microsecond=0), newer.replace(microsecond=0))


if __name__ == "__main__":
    unittest.main()
