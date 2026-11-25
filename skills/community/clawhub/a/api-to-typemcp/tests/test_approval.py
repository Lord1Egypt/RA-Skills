"""Approval receipt lifecycle, integrity, and single-use tests."""

from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

import sys

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import approval  # noqa: E402


class ApprovalReceiptTest(unittest.TestCase):
    """Isolated-state receipt lifecycle."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = self._tmp.name
        self.state_dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        del os.environ["TYPE_MCP_APPROVAL_STATE_DIR"]
        self._tmp.cleanup()

    # ------------------------------------------------------------------
    # issue → validate → consume round-trip
    # ------------------------------------------------------------------

    def test_issue_creates_receipt_file(self) -> None:
        path = approval.issue_receipt("sha256:abc123")
        self.assertTrue(path.exists())
        data = json.loads(path.read_text())
        self.assertEqual(data["manifest_digest"], "sha256:abc123")
        self.assertIn("hmac", data)
        self.assertIn("nonce", data)

    def test_validate_consumes_receipt(self) -> None:
        path = approval.issue_receipt("sha256:abc123")
        approval.validate_and_consume_receipt("sha256:abc123")
        self.assertFalse(path.exists(), "receipt must be deleted after consumption")

    def test_second_validation_fails_after_consumption(self) -> None:
        approval.issue_receipt("sha256:abc123")
        approval.validate_and_consume_receipt("sha256:abc123")
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:abc123")
        self.assertIn("no approval receipt found", str(ctx.exception))

    # ------------------------------------------------------------------
    # digest binding
    # ------------------------------------------------------------------

    def test_receipt_bound_to_exact_digest(self) -> None:
        approval.issue_receipt("sha256:original")
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:tampered")
        self.assertIn("no approval receipt found", str(ctx.exception))

    # ------------------------------------------------------------------
    # expiration
    # ------------------------------------------------------------------

    def test_expired_receipt_is_rejected(self) -> None:
        approval.issue_receipt("sha256:abc123", ttl=1)
        future = int(time.time()) + 3600
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:abc123", now=future)
        self.assertIn("expired", str(ctx.exception))

    # ------------------------------------------------------------------
    # HMAC integrity / forgery resistance
    # ------------------------------------------------------------------

    def test_tampered_digest_is_rejected(self) -> None:
        path = approval.issue_receipt("sha256:abc123")
        data = json.loads(path.read_text())
        data["manifest_digest"] = "sha256:evil"
        path.write_text(json.dumps(data))
        # Validate with the ORIGINAL digest so the file is found by prefix,
        # but the HMAC over the tampered payload must fail.
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:abc123")
        self.assertIn("integrity check", str(ctx.exception))

    def test_tampered_hmac_is_rejected(self) -> None:
        path = approval.issue_receipt("sha256:abc123")
        data = json.loads(path.read_text())
        data["hmac"] = "0" * 64
        path.write_text(json.dumps(data))
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:abc123")
        self.assertIn("integrity check", str(ctx.exception))

    def test_tampered_expiry_is_rejected(self) -> None:
        path = approval.issue_receipt("sha256:abc123", ttl=1)
        data = json.loads(path.read_text())
        data["expires_at"] = int(time.time()) + 999999
        path.write_text(json.dumps(data))
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:abc123")
        self.assertIn("integrity check", str(ctx.exception))

    def test_missing_field_is_rejected(self) -> None:
        path = approval.issue_receipt("sha256:abc123")
        data = json.loads(path.read_text())
        del data["nonce"]
        path.write_text(json.dumps(data))
        with self.assertRaises(approval.ApprovalError) as ctx:
            approval.validate_and_consume_receipt("sha256:abc123")
        self.assertIn("missing fields", str(ctx.exception))

    # ------------------------------------------------------------------
    # state isolation
    # ------------------------------------------------------------------

    def test_different_state_dirs_are_isolated(self) -> None:
        """A receipt issued in one state dir cannot be consumed in another."""
        approval.issue_receipt("sha256:abc123")

        with tempfile.TemporaryDirectory() as other:
            os.environ["TYPE_MCP_APPROVAL_STATE_DIR"] = other
            with self.assertRaises(approval.ApprovalError) as ctx:
                approval.validate_and_consume_receipt("sha256:abc123")
            self.assertIn("no approval receipt found", str(ctx.exception))

    # ------------------------------------------------------------------
    # helper
    # ------------------------------------------------------------------

    def test_has_receipt(self) -> None:
        self.assertFalse(approval.has_receipt("sha256:xyz"))
        approval.issue_receipt("sha256:xyz")
        self.assertTrue(approval.has_receipt("sha256:xyz"))
        approval.validate_and_consume_receipt("sha256:xyz")
        self.assertFalse(approval.has_receipt("sha256:xyz"))


if __name__ == "__main__":
    unittest.main()
