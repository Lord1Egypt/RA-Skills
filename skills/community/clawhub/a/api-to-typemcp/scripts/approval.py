"""Isolated-state manifest approval receipts for the bundled engine."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import tempfile
import time
from pathlib import Path
from typing import Any, Optional

# Receipts expire after one hour to limit replay windows.
RECEIPT_TTL_SECONDS = 3600

# Receipt filenames embed a digest prefix for lookup.
_DIGEST_PREFIX_LEN = 16


class ApprovalError(Exception):
    """Safe, user-facing approval-state error."""


# ---------------------------------------------------------------------------
# State directory
# ---------------------------------------------------------------------------

def approval_state_dir() -> Path:
    """Return the process-owned isolated approval-state directory.

    Override with ``TYPE_MCP_APPROVAL_STATE_DIR`` for testing.  The default
    lives under the system temp directory and is namespaced by UID so that
    different local users do not share state.
    """
    env = os.environ.get("TYPE_MCP_APPROVAL_STATE_DIR")
    if env:
        p = Path(env)
        p.mkdir(parents=True, exist_ok=True)
        return p

    p = Path(tempfile.gettempdir()) / f"api-to-typemcp-approvals-{os.getuid()}"
    p.mkdir(parents=True, exist_ok=True)
    os.chmod(p, 0o700)
    return p


def _secret_path(state_dir: Path) -> Path:
    return state_dir / "secret"


def _receipt_path(state_dir: Path, manifest_digest: str) -> Path:
    # Strip the "sha256:" prefix for the filename.
    raw = manifest_digest.split(":", 1)[-1]
    return state_dir / f"receipt-{raw[:_DIGEST_PREFIX_LEN]}.json"


# ---------------------------------------------------------------------------
# Secret management
# ---------------------------------------------------------------------------

def _read_or_create_secret(state_dir: Path) -> bytes:
    """Read the per-state HMAC secret, creating it on first use."""
    path = _secret_path(state_dir)
    if path.exists():
        data = path.read_bytes()
        if len(data) >= 32:
            return data[:32]
        raise ApprovalError("approval state secret is corrupted or truncated")
    secret = secrets.token_bytes(32)
    path.write_bytes(secret)
    os.chmod(path, 0o600)
    return secret


# ---------------------------------------------------------------------------
# Receipt creation
# ---------------------------------------------------------------------------

def issue_receipt(manifest_digest: str, *, ttl: int = RECEIPT_TTL_SECONDS) -> Path:
    """Create a single-use, HMAC-authenticated receipt for *manifest_digest*.

    Returns the path to the written receipt file.
    """
    state_dir = approval_state_dir()
    secret = _read_or_create_secret(state_dir)

    now = int(time.time())
    nonce = secrets.token_hex(16)
    expires_at = now + ttl

    payload = f"{manifest_digest}|{now}|{expires_at}|{nonce}"
    mac = hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()

    receipt: dict[str, Any] = {
        "manifest_digest": manifest_digest,
        "issued_at": now,
        "expires_at": expires_at,
        "nonce": nonce,
        "hmac": mac,
    }

    path = _receipt_path(state_dir, manifest_digest)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)
    return path


# ---------------------------------------------------------------------------
# Receipt validation / consumption
# ---------------------------------------------------------------------------

def _compute_hmac(secret: bytes, receipt: dict[str, Any]) -> str:
    payload = (
        f"{receipt['manifest_digest']}|"
        f"{receipt['issued_at']}|"
        f"{receipt['expires_at']}|"
        f"{receipt['nonce']}"
    )
    return hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()


def validate_and_consume_receipt(
    manifest_digest: str,
    *,
    now: Optional[int] = None,
) -> None:
    """Validate the receipt for *manifest_digest* and consume it.

    Raises ``ApprovalError`` when no valid, unexpired, unconsumed receipt
    exists.  On success the receipt file is deleted (single-use).
    """
    if now is None:
        now = int(time.time())

    state_dir = approval_state_dir()
    secret = _read_or_create_secret(state_dir)
    path = _receipt_path(state_dir, manifest_digest)

    if not path.exists():
        raise ApprovalError(
            f"no approval receipt found for digest {manifest_digest}; "
            "run `approve --manifest-digest <digest>` first"
        )

    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ApprovalError(f"approval receipt is unreadable: {exc}") from exc

    # --- structural checks -------------------------------------------------
    required_keys = {"manifest_digest", "issued_at", "expires_at", "nonce", "hmac"}
    missing = required_keys - set(receipt)
    if missing:
        raise ApprovalError(f"approval receipt is missing fields: {sorted(missing)}")

    # --- HMAC integrity ----------------------------------------------------
    expected = _compute_hmac(secret, receipt)
    if not hmac.compare_digest(expected, receipt["hmac"]):
        raise ApprovalError(
            "approval receipt failed integrity check; it may have been tampered with"
        )

    # --- digest binding ----------------------------------------------------
    if receipt["manifest_digest"] != manifest_digest:
        raise ApprovalError(
            "approval receipt is bound to a different manifest digest"
        )

    # --- expiration --------------------------------------------------------
    if now >= receipt["expires_at"]:
        raise ApprovalError("approval receipt has expired")

    # --- consume (single-use) ----------------------------------------------
    path.unlink()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def has_receipt(manifest_digest: str) -> bool:
    """Return True if an unconsumed receipt file exists (no validation)."""
    state_dir = approval_state_dir()
    return _receipt_path(state_dir, manifest_digest).exists()
