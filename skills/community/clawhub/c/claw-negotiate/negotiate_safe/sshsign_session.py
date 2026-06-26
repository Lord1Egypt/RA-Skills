"""SSH client for sshsign's signing_sessions API.

Thin wrapper around `ssh sshsign.dev (create|join|get|cancel|complete|audit)-session`.
Handles the subprocess call, JSON response parsing, and defensive error
mapping. Callers get typed dicts or raise specific exceptions.

Kept separate from telegram_push.py and run_safe.py so it stays easy to
unit-test by injecting the `runner` callable.
"""
from __future__ import annotations

import base64
import json
import subprocess
from typing import Any, Callable, Optional


def _encode_metadata_b64(value: dict) -> str:
    """Compact-JSON-encode + URL-safe base64. Matches what sshsign's
    `--metadata-*-b64` flag expects (P8-2). Keeps the value opaque to
    SSH argv parsing — no whitespace, no quotes, no bare-key repair.
    """
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii")


class SshsignSessionError(Exception):
    """Base for all sshsign session errors."""


class SessionNotFoundError(SshsignSessionError):
    """`get-session` returned not_found, or `join-session` saw an unknown code."""


class SessionTerminalError(SshsignSessionError):
    """Session is in a terminal state (completed, canceled, expired)."""


class SessionExpiredError(SshsignSessionError):
    """Session passed its TTL and has been marked expired."""


class SessionRoleConflictError(SshsignSessionError):
    """Another member already has the role you're trying to claim."""


class SessionNotCreatorError(SshsignSessionError):
    """Operation requires the caller to be the session creator."""


class SessionNotMemberError(SshsignSessionError):
    """Operation requires the caller to be a member of the session."""


class GroupAlreadyBoundError(SshsignSessionError):
    """bind-group: this session is already bound to a different group_chat_id.
    Write-once: the caller must cancel and start a new session if they want
    to change the binding."""


class LeaseHeldError(SshsignSessionError):
    """Another live worker owns the requested workflow lease."""

    def __init__(self, message: str, holder: str = "", expires_at: str = ""):
        super().__init__(message)
        self.holder = holder
        self.expires_at = expires_at


class LeaseNotHeldError(SshsignSessionError):
    """No current lease row exists for the requested key."""


class LeaseHolderMismatchError(SshsignSessionError):
    """The caller's holder/generation is stale or does not own the lease."""


class LeaseExpiredError(SshsignSessionError):
    """The caller's lease existed but has expired."""


class InvalidLeaseError(SshsignSessionError):
    """Invalid lease action, TTL, or generation."""


# Map sshsign's error strings back to Python exception classes. sshsign
# returns plain-text error strings via JSON {"error": "..."}, so we match
# on substrings. Brittle-ish but gives callers useful types.
def _error_from_payload(payload: dict[str, Any]) -> SshsignSessionError:
    msg = str(payload.get("error") or "")
    if msg == "lease_held":
        return LeaseHeldError(
            msg,
            holder=str(payload.get("holder") or ""),
            expires_at=str(payload.get("expires_at") or ""),
        )
    if msg == "lease_not_held":
        return LeaseNotHeldError(msg)
    if msg == "lease_holder_mismatch":
        return LeaseHolderMismatchError(msg)
    if msg == "lease_expired":
        return LeaseExpiredError(msg)
    if msg in ("invalid_lease_action", "invalid_lease_ttl", "invalid_lease_generation"):
        return InvalidLeaseError(msg)
    return _error_from_message(msg)


def _error_from_message(msg: str) -> SshsignSessionError:
    m = msg.lower()
    if "lease_held" in m:
        return LeaseHeldError(msg)
    if "lease_not_held" in m:
        return LeaseNotHeldError(msg)
    if "lease_holder_mismatch" in m:
        return LeaseHolderMismatchError(msg)
    if "lease_expired" in m:
        return LeaseExpiredError(msg)
    if "invalid_lease" in m:
        return InvalidLeaseError(msg)
    if "not found" in m or "session not found" in m:
        return SessionNotFoundError(msg)
    if "expired" in m:
        return SessionExpiredError(msg)
    if "already has a member" in m or "role" in m and "already" in m:
        return SessionRoleConflictError(msg)
    if "only the session creator" in m or "not creator" in m:
        return SessionNotCreatorError(msg)
    if "not a member" in m:
        return SessionNotMemberError(msg)
    if "terminal" in m or "already completed" in m or "already canceled" in m:
        return SessionTerminalError(msg)
    if "group_already_bound" in m:
        return GroupAlreadyBoundError(msg)
    return SshsignSessionError(msg)


SshsignRunner = Callable[..., subprocess.CompletedProcess]


class SshsignSession:
    """Client for sshsign's signing_sessions commands.

    Parameters
    ----------
    host : str
        The sshsign host, e.g. "sshsign.dev". Passed straight to ssh.
    runner : Callable, optional
        Injection point for tests. Defaults to `subprocess.run`. The
        runner receives the full argv list + keyword args and must
        return a `subprocess.CompletedProcess`-compatible object
        (attrs: returncode, stdout, stderr).
    ssh_bin : str, optional
        Name/path of the ssh binary. Defaults to "ssh".
    """

    def __init__(
        self,
        host: str = "sshsign.dev",
        runner: SshsignRunner = subprocess.run,
        ssh_bin: str = "ssh",
    ):
        self.host = host
        self.runner = runner
        self.ssh_bin = ssh_bin

    def _run(self, command: str, *flags: str, timeout: int = 20) -> dict[str, Any]:
        argv = [self.ssh_bin, self.host, command, *flags]
        try:
            result = self.runner(
                argv, capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            raise SshsignSessionError(f"ssh timed out: {e}") from e
        except FileNotFoundError as e:
            raise SshsignSessionError(f"ssh not found: {e}") from e

        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            raise SshsignSessionError(
                f"ssh exited {result.returncode}: {stderr or '(no stderr)'}"
            )

        stdout = (result.stdout or "").strip()
        if not stdout:
            raise SshsignSessionError("ssh returned empty response")

        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as e:
            raise SshsignSessionError(
                f"ssh returned non-JSON: {stdout!r}"
            ) from e

        if isinstance(payload, dict) and payload.get("error"):
            raise _error_from_payload(payload)
        return payload

    # ------------------------------------------------------------------
    # Session commands
    # ------------------------------------------------------------------

    def create_session(
        self,
        session_id: str,
        role: str,
        apoa_pubkey_pem: str,
        party_did: Optional[str] = None,
        metadata_public: Optional[dict] = None,
        metadata_member: Optional[dict] = None,
        ttl_seconds: Optional[int] = None,
    ) -> dict[str, Any]:
        """Create a new signing session; return the session dict including session_code."""
        flags = [
            "--session-id", session_id,
            "--role", role,
            "--apoa-pubkey", apoa_pubkey_pem,
        ]
        if party_did:
            flags += ["--party-did", party_did]
        # P8-2: send metadata base64-encoded via --metadata-{public,member}-b64.
        # SSH argv strips inner double quotes from string values, so a field
        # like `"investor_firm":"Blue Fund"` used to arrive server-side as
        # `investor_firm:Blue Fund` (bare value, malformed JSON). Base64 is
        # a whitespace-free, quote-free alphabet; SSH transports it as one
        # opaque token and the server decodes back to canonical JSON.
        if metadata_public is not None:
            flags += ["--metadata-public-b64", _encode_metadata_b64(metadata_public)]
        if metadata_member is not None:
            flags += ["--metadata-member-b64", _encode_metadata_b64(metadata_member)]
        if ttl_seconds is not None:
            flags += ["--ttl", str(ttl_seconds)]
        return self._run("create-session", *flags)

    def join_session(
        self,
        session_code: str,
        role: str,
        apoa_pubkey_pem: str,
        party_did: Optional[str] = None,
    ) -> dict[str, Any]:
        """Join an existing session by session_code."""
        flags = [
            "--session-code", session_code,
            "--role", role,
            "--apoa-pubkey", apoa_pubkey_pem,
        ]
        if party_did:
            flags += ["--party-did", party_did]
        return self._run("join-session", *flags)

    def get_session(
        self,
        session_code: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Fetch session state by code OR id. Caller is member ⇒ full response;
        otherwise metadata_member and members list are omitted."""
        if session_code:
            return self._run("get-session", "--session-code", session_code)
        if session_id:
            return self._run("get-session", "--session-id", session_id)
        raise ValueError("session_code or session_id is required")

    def cancel_session(self, session_id: str, rescind: bool = False) -> dict[str, Any]:
        """Cancel a session. `rescind=True` produces the rescinded_after_sign
        terminal state (distinct from ordinary cancellation)."""
        flags = ["--session-id", session_id]
        if rescind:
            flags.append("--rescind")
        return self._run("cancel-session", *flags)

    def complete_session(
        self,
        session_id: str,
        executed_artifact: str,
        lease_holder: str | None = None,
        lease_generation: int | None = None,
    ) -> dict[str, Any]:
        """Creator-only. Idempotent for the same args."""
        flags = [
            "--session-id", session_id,
            "--executed-artifact", executed_artifact,
        ]
        if lease_holder is not None or lease_generation is not None:
            if not lease_holder or lease_generation is None:
                raise ValueError("lease_holder and lease_generation must be provided together")
            flags += [
                "--lease-holder", lease_holder,
                "--lease-generation", str(int(lease_generation)),
            ]
        return self._run(
            "complete-session",
            *flags,
        )

    def bind_group(self, session_id: str, group_chat_id: int) -> dict[str, Any]:
        """Bind a session to a chat venue (Telegram group chat_id or equivalent).

        Write-once: if the session already has a binding that matches, this
        is an idempotent no-op and returns the current session. If the
        existing binding differs, raises GroupAlreadyBoundError — the caller
        must cancel and start a new session to re-bind.

        Any member may bind; rejected if the session is in a terminal state.
        """
        return self._run(
            "bind-group",
            "--session-id", session_id,
            "--group-chat-id", str(int(group_chat_id)),
        )

    def audit_session(self, session_id: str) -> list[dict[str, Any]]:
        """Member-only. Returns list of transition events."""
        result = self._run("audit-session", "--session-id", session_id)
        if isinstance(result, list):
            return result
        raise SshsignSessionError(
            f"expected audit list, got: {type(result).__name__}"
        )

    def claim_delivery(
        self,
        session_id: str,
        key: str,
        target: str = "",
        message_id: str = "",
    ) -> dict[str, Any]:
        """Member-only. Atomically claim a durable idempotency key.

        The first caller receives ``{"created": true}``; later callers get
        the existing delivery with ``created`` omitted/false and must suppress
        the Telegram side effect.
        """
        flags = ["--session-id", session_id, "--key", key]
        if target:
            flags += ["--target", str(target)]
        if message_id:
            flags += ["--message-id", str(message_id)]
        return self._run("claim-delivery", *flags)

    def get_delivery(self, session_id: str, key: str) -> dict[str, Any]:
        """Member-only. Read one durable delivery claim."""
        return self._run(
            "get-delivery",
            "--session-id", session_id,
            "--key", key,
        )

    def list_deliveries(self, session_id: str) -> list[dict[str, Any]]:
        """Member-only. Return all durable delivery claims for a session."""
        result = self._run("list-deliveries", "--session-id", session_id)
        if isinstance(result, list):
            return result
        raise SshsignSessionError(
            f"expected delivery list, got: {type(result).__name__}"
        )

    # P7-5: creator-only field updates on the caller's own member row.
    # Whitelist enforced client-side AND server-side; the server is the
    # authority, this check is a fast-fail for typos.
    _UPDATABLE_MEMBER_FIELDS = frozenset({
        "founder_resumed_at", "founder_streaming_at",
    })

    def update_session_member(
        self, session_id: str, field: str, value: int,
    ) -> dict[str, Any]:
        """Update a whitelisted field on the caller's own member row.

        Used by P7-5 durable founder-wait:
          * ``founder_resumed_at`` — set when a cron-scanned ``scan``
            turn reattaches to a waiting session.
          * ``founder_streaming_at`` — set once ``_stream_to_telegram``
            is actually running; the investor polls on this, not on
            ``founder_resumed_at``, so a crash between the two is
            recoverable.

        Creator-only (enforced by sshsign). Raises SshsignSessionError
        on server-side rejection (non-creator, non-whitelisted field,
        terminal session).
        """
        if field not in self._UPDATABLE_MEMBER_FIELDS:
            raise SshsignSessionError(
                f"field not writable via update-session-member: {field!r}"
            )
        return self._run(
            "update-session-member",
            "--session-id", session_id,
            "--field", field,
            "--value", str(int(value)),
        )

    # Inverted-invitation: each member's own bot_handle, written by
    # the member's own bot. ACL is member-self-write (any session
    # member can write their own row's whitelisted text fields).
    _UPDATABLE_MEMBER_TEXT_FIELDS = frozenset({"bot_handle", "telegram_user_id"})

    def update_session_member_text(
        self, session_id: str, field: str, text_value: str,
    ) -> dict[str, Any]:
        """Update a whitelisted text field on the caller's own member row.

        Member-self-write: any session member can write their OWN row.
        Distinct from ``update_session_member`` (creator-only int fields).
        Whitelist: {bot_handle}.

        Empty string is allowed (clears the field). Telegram bot handles
        cap at 32 chars; we don't enforce that client-side — let the
        server own length validation when it eventually adds it.

        Raises SshsignSessionError on rejection.
        """
        if field not in self._UPDATABLE_MEMBER_TEXT_FIELDS:
            raise SshsignSessionError(
                f"text field not writable via update-session-member: {field!r}"
            )
        return self._run(
            "update-session-member",
            "--session-id", session_id,
            "--field", field,
            "--text-value", str(text_value),
        )

    def acquire_lease(
        self,
        session_id: str,
        role: str,
        action: str,
        holder: str,
        ttl_seconds: int | None = None,
    ) -> dict[str, Any]:
        flags = [
            "--session-id", session_id,
            "--role", role,
            "--action", action,
            "--holder", holder,
        ]
        if ttl_seconds is not None:
            flags += ["--ttl", str(int(ttl_seconds))]
        return self._run("acquire-lease", *flags)

    def refresh_lease(
        self,
        session_id: str,
        role: str,
        action: str,
        holder: str,
        generation: int,
        ttl_seconds: int | None = None,
    ) -> dict[str, Any]:
        flags = [
            "--session-id", session_id,
            "--role", role,
            "--action", action,
            "--holder", holder,
            "--generation", str(int(generation)),
        ]
        if ttl_seconds is not None:
            flags += ["--ttl", str(int(ttl_seconds))]
        return self._run("refresh-lease", *flags)

    def check_lease(
        self,
        session_id: str,
        role: str,
        action: str,
        holder: str,
        generation: int,
    ) -> dict[str, Any]:
        return self._run(
            "check-lease",
            "--session-id", session_id,
            "--role", role,
            "--action", action,
            "--holder", holder,
            "--generation", str(int(generation)),
        )

    def release_lease(
        self,
        session_id: str,
        role: str,
        action: str,
        holder: str,
        generation: int,
    ) -> dict[str, Any]:
        return self._run(
            "release-lease",
            "--session-id", session_id,
            "--role", role,
            "--action", action,
            "--holder", holder,
            "--generation", str(int(generation)),
        )
