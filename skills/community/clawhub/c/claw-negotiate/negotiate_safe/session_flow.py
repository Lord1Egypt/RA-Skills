"""sshsign session create/join helpers for two-party SAFE negotiations."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from sshsign_session import SshsignSession, SshsignSessionError


_PLACEHOLDER_BOT_HANDLES = {"", "yourbot", "@yourbot"}


def configured_bot_handle() -> str:
    """Return the configured Telegram bot handle, ignoring install examples."""
    handle = (os.environ.get("TELEGRAM_BOT_USERNAME") or "").strip()
    return "" if handle.lower() in _PLACEHOLDER_BOT_HANDLES else handle


def sshsign_session_id(negotiation_id: str) -> str:
    """Return the sshsign session_id used by upstream signing calls."""
    if not negotiation_id:
        return ""
    return negotiation_id if negotiation_id.startswith("session_") else f"session_{negotiation_id}"


def role_pubkey_path(neg_dir: Path, role: str) -> Path:
    return neg_dir / "keys" / f"{role}_public.pem"


def register_signing_session(
    mint_output: dict,
    constraints: dict,
    user_role: str,
    neg_dir: Path,
    session_client=None,
    telegram_user_id: int | None = None,
) -> dict | None:
    """Create an sshsign session and publish the creator's APOA pubkey."""
    pubkey_path = role_pubkey_path(neg_dir, user_role)
    if user_role not in ("founder", "investor") or not pubkey_path.exists():
        sys.stderr.write(
            f"APOA pubkey for role={user_role} not found at {pubkey_path}\n"
        )
        return None

    try:
        apoa_pubkey_pem = pubkey_path.read_text()
    except OSError as e:
        sys.stderr.write(f"reading {pubkey_path}: {e}\n")
        return None

    metadata_public = {"use_case": "safe", "version": 1}
    for field in ("company_name", "founder_name", "founder_title", "investor_name", "investor_firm"):
        if constraints.get(field):
            metadata_public[field] = constraints[field]
    if user_role == "founder":
        bot_handle = configured_bot_handle()
        if bot_handle:
            metadata_public["founder_bot_handle"] = bot_handle

    metadata_member: dict = {}
    for field in (
        "founder_name", "founder_title",
        "investor_name", "investor_firm",
        "investment_amount",
    ):
        val = constraints.get(field)
        if val not in (None, ""):
            metadata_member[field] = val
    if telegram_user_id and user_role == "founder":
        metadata_member["telegram"] = {"founder_user_id": int(telegram_user_id)}

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )
    try:
        sess = client.create_session(
            session_id=sshsign_session_id(mint_output["negotiation_id"]),
            role=user_role,
            apoa_pubkey_pem=apoa_pubkey_pem,
            party_did=os.environ.get("USER_DID") or None,
            metadata_public=metadata_public,
            metadata_member=metadata_member,
        )
    except SshsignSessionError as e:
        sys.stderr.write(f"create-session failed: {e}\n")
        return None

    session_id = sess.get("session_id") or sshsign_session_id(mint_output["negotiation_id"])
    if session_id:
        bot_handle = configured_bot_handle()
        if bot_handle:
            try:
                client.update_session_member_text(
                    session_id, field="bot_handle", text_value=bot_handle,
                )
            except SshsignSessionError as e:
                sys.stderr.write(f"create: bot_handle write: {e}\n")
        if telegram_user_id:
            try:
                client.update_session_member_text(
                    session_id,
                    field="telegram_user_id",
                    text_value=str(int(telegram_user_id)),
                )
            except (ValueError, SshsignSessionError) as e:
                sys.stderr.write(f"create: telegram_user_id write: {e}\n")

    return {
        "session_code": sess.get("session_code"),
        "session_created_at": sess.get("created_at"),
        "session_expires_at": sess.get("expires_at"),
        "session_status": sess.get("status"),
    }


def join_signing_session(
    mint_output: dict,
    shared_session: dict,
    user_role: str,
    neg_dir: Path,
    repo: Path | None = None,
    session_client=None,
    telegram_user_id: int | None = None,
) -> dict | None:
    """Join an sshsign session and cache the counterparty APOA pubkey."""
    del mint_output, repo
    pubkey_path = role_pubkey_path(neg_dir, user_role)
    if user_role not in ("founder", "investor") or not pubkey_path.exists():
        sys.stderr.write(
            f"Cannot join: APOA pubkey for role={user_role} not found at {pubkey_path}\n"
        )
        return None

    try:
        our_pubkey_pem = pubkey_path.read_text()
    except OSError as e:
        sys.stderr.write(f"reading {pubkey_path}: {e}\n")
        return None

    session_code = shared_session.get("session_code")
    if not session_code:
        sys.stderr.write("Cannot join: shared_session has no session_code\n")
        return None

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )

    try:
        join_result = client.join_session(
            session_code=session_code,
            role=user_role,
            apoa_pubkey_pem=our_pubkey_pem,
            party_did=os.environ.get("USER_DID") or None,
        )
    except SshsignSessionError as e:
        sys.stderr.write(f"join-session failed: {e}\n")
        return None

    bot_handle = configured_bot_handle()
    joined_session_id = (join_result or {}).get("session_id")
    if joined_session_id:
        if bot_handle:
            try:
                client.update_session_member_text(
                    joined_session_id, field="bot_handle", text_value=bot_handle,
                )
            except SshsignSessionError as e:
                sys.stderr.write(f"join: bot_handle write: {e}\n")
        if telegram_user_id:
            try:
                client.update_session_member_text(
                    joined_session_id,
                    field="telegram_user_id",
                    text_value=str(int(telegram_user_id)),
                )
            except (ValueError, SshsignSessionError) as e:
                sys.stderr.write(f"join: telegram_user_id write: {e}\n")

    try:
        member_view = client.get_session(session_code=session_code)
    except SshsignSessionError as e:
        sys.stderr.write(f"post-join get-session failed: {e}\n")
        member_view = join_result

    counterparty_role = "investor" if user_role == "founder" else "founder"
    counterparty_pubkey_pem = ""
    for member in (member_view.get("members") or []):
        if member.get("role") == counterparty_role:
            counterparty_pubkey_pem = member.get("apoa_pubkey_pem") or ""
            break

    counterparty_pubkey_path = role_pubkey_path(neg_dir, counterparty_role)
    if counterparty_pubkey_pem:
        try:
            counterparty_pubkey_path.write_text(counterparty_pubkey_pem)
        except OSError as e:
            sys.stderr.write(f"writing counterparty pubkey: {e}\n")

    return {
        "session_code": session_code,
        "session_created_at": member_view.get("created_at"),
        "session_expires_at": member_view.get("expires_at"),
        "session_status": member_view.get("status"),
        "counterparty_pubkey_path": (
            str(counterparty_pubkey_path) if counterparty_pubkey_pem else ""
        ),
    }
