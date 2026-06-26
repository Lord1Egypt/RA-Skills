#!/usr/bin/env python3
"""Single entry point for the negotiate_safe skill.

Two subcommands:
  prepare   — parse NL message into constraints, write config (fast, <10s)
  negotiate — mint tokens + run negotiation + emit results (long, 90-180s)

The output-dir is the shared state between the two calls. The model never
needs to pass files between scripts or construct shell pipes.

Usage:
  python3 run_safe.py prepare --message "Negotiate my SAFE..." --output-dir /tmp/safe_123
  python3 run_safe.py negotiate --output-dir /tmp/safe_123
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from artifacts import (
    build_artifact_uri as _build_artifact_uri,
    parse_artifact_uri as _parse_artifact_uri,
    write_counterparty_pending as _write_counterparty_pending,
)
from cancel_flow import cancel_preflight, cancel_success_event_type
from parse_constraints import extract_constraints
from parse_identity import extract_identity
from identity import (
    build_env_updates as _build_env_updates,
    persist_env_updates as _persist_env_updates,
    profile_from_env,
)
from links import (
    BIND_CODE_RE as _BIND_CODE_RE,
    build_invite_url as _build_invite_url,
    extract_bind_code as _extract_bind_code,
)
from minting import build_service_name, identity_value, write_local_mint_files
from format_event import format_event, group_setup_reply_markup
from session_flow import (
    register_signing_session as _register_signing_session,
    join_signing_session as _join_signing_session,
)
from telegram_push import (
    resolve_chat_id,
    send_telegram,
    send_signing_url_to_dm,
)
from telegram import route_stream_message, stream_target
from typing_loop import TypingLoop, get_bot_token
from sshsign_session import (
    SshsignSession,
    SshsignSessionError,
    SessionTerminalError,
    SessionExpiredError,
    SessionNotFoundError,
    SessionRoleConflictError,
    SessionNotMemberError,
    GroupAlreadyBoundError,
    LeaseHeldError,
    LeaseHolderMismatchError,
    LeaseExpiredError,
)
import state_store
import orchestrator
from operator_ready import (
    build_operator_updates,
    doctor_checks,
    format_doctor,
    load_env_file,
    load_skill_manifest,
    persist_operator_updates,
)
from reconcile import (
    reconcile_active_sessions,
    classify_founder_resume,
    classify_investor_resume,
    FOUNDER_ALREADY_STREAMING,
    FOUNDER_PROMPT_GROUP,
    FOUNDER_START_STREAM,
    FOUNDER_STALE_NO_MEMBER,
    FOUNDER_WAIT_COUNTERPARTY,
    FOUNDER_WAIT_GROUP_ALREADY_PROMPTED,
    has_executed_delivered,
    INVESTOR_ALREADY_STREAMING,
    INVESTOR_START_STREAM,
    INVESTOR_STALE_NO_FOUNDER,
    INVESTOR_WAIT_FOUNDER_STREAM,
    INVESTOR_WAIT_GROUP_BIND,
    is_terminal_status,
    latest_signing_pending_id,
    mark_executed_delivered,
    normalize_status,
    reconcile_state_by_negotiation_id,
    reconcile_session,
)
from trace_log import write_trace
from executed_pdf import finalize_executed_pdf as _finalize_executed_pdf
from upstream import (
    augment_signing_url as _augment_signing_url,
    ssh_history as _ssh_history,
    synthesize_offer_event as _synthesize_offer_event,
)


IDENTITY_SENTINEL_PATH = Path("/tmp/safe_negotiate/pending_negotiation.txt")


def _identity_configured() -> bool:
    """Return True if the installed user's identity is already set up.

    Either FOUNDER_NAME or INVESTOR_NAME counts — the user might only
    negotiate from one side of the deal. A founder-only install sets
    FOUNDER_NAME; an investor-only install sets INVESTOR_NAME (e.g. an
    investor joining a two-party code via their own OC). Either way the
    wizard has already run to completion and we skip the prompt.
    """
    profile = profile_from_env()
    role = _classify_bot_role()
    if role == "founder":
        return bool(
            identity_value(profile.get("founder_name"))
            and identity_value(profile.get("company_name"), field="company")
        )
    if role == "investor":
        return bool(
            identity_value(profile.get("investor_name"))
            and identity_value(profile.get("investor_firm"))
        )
    return bool(
        identity_value(profile.get("founder_name"))
        or identity_value(profile.get("investor_name"))
    )


def _enrich_constraints_from_profile(constraints: dict, env: dict | None = None) -> dict:
    """Fill this user's party identity from saved onboarding profile."""
    out = dict(constraints)
    profile = profile_from_env(env)
    role = (out.get("role") or "").lower()
    if role == "founder":
        mapping = {
            "founder_name": ("founder_name", ""),
            "founder_title": ("founder_title", ""),
            "company_name": ("company_name", "company"),
        }
    elif role == "investor":
        mapping = {
            "investor_name": ("investor_name", ""),
            "investor_firm": ("investor_firm", ""),
        }
    else:
        return out

    for constraint_key, (profile_key, field) in mapping.items():
        if out.get(constraint_key):
            continue
        value = identity_value(profile.get(profile_key), field=field)
        if value:
            out[constraint_key] = value
    return out


def _missing_counterparty_identity(constraints: dict) -> list[str]:
    """Return missing counterparty identity fields for founder two-party starts."""
    if (constraints.get("mode") or "").lower() != "two_party":
        return []
    if (constraints.get("role") or "").lower() != "founder":
        return []
    if constraints.get("session_code"):
        return []
    missing: list[str] = []
    if not identity_value(constraints.get("investor_name"), drop_placeholders=False):
        missing.append("investor name")
    if not identity_value(constraints.get("investor_firm"), drop_placeholders=False):
        missing.append("investor firm")
    return missing


def _identity_setup_prompt() -> str:
    role = _classify_bot_role()
    if role == "investor":
        return (
            "\U0001f44b Welcome! Before we negotiate, tell me who you are.\n\n"
            "Reply with your investor profile, for example:\n"
            "• \"I'm Nora Vassileva, partner at SD Fund\"\n\n"
            "I'll remember it for future negotiations."
        )
    return (
        "\U0001f44b Welcome! Before we negotiate, tell me who you are.\n\n"
        "Reply with your founder profile, for example:\n"
        "• \"I'm Juan Figuera, CEO of APOA Inc\"\n\n"
        "I'll remember it for future negotiations."
    )


def _embedded_investor_identity(message: str) -> dict | None:
    """Extract investor identity from a two-party join request.

    The founder's invite template now says:

        Joining INV-XXXXX ..., I am Nora Vassileva at SD Fund, cap up to ...

    That sentence is already the investor profile. Do a small deterministic
    parse before the first-run identity gate so the investor does not have to
    introduce themselves twice.
    """
    if not re.search(r"\bJoining\s+INV-[A-Z0-9]{5,}\b", message, re.IGNORECASE):
        return None
    m = re.search(
        r"\bI\s*(?:am|'m)\s+(.+?)\s+(?:at|from)\s+(.+?)"
        r"(?=(?:[,.!?]\s*)?"
        r"(?:cap|valuation|discount|pro[- ]?rata|mfn|invest|investment|check)\b|[.!?]?\s*$)",
        message,
        re.IGNORECASE,
    )
    if not m:
        return None
    name_part = m.group(1).strip(" ,")
    firm = m.group(2).strip(" ,.")
    title = None
    if "," in name_part:
        name, maybe_title = [part.strip() for part in name_part.split(",", 1)]
        title = maybe_title or None
    else:
        name = name_part
    if not name or not firm:
        return None
    return {
        "role": "investor",
        "name": name,
        "title": title,
        "company": None,
        "firm": firm,
    }


SKILL_DIR = Path(__file__).resolve().parent
STREAM_HELPER = SKILL_DIR / "_stream_negotiate.py"


def _sshsign_session_id(negotiation_id: str) -> str:
    """Return the session_id we use when talking to sshsign session APIs.

    The skill derives its signing session id as ``f"session_{negotiation_id}"``
    and passes that value as --session-id on sign calls. For sshsign's cross-party
    get-envelope ACL (which matches pending_signatures.signing_session_id
    against the signing_sessions row's session_id) to let members read
    each other's pendings, we have to use the SAME prefixed form when
    create-session / join-session / get-session etc.
    """
    if not negotiation_id:
        return ""
    if negotiation_id.startswith("session_"):
        return negotiation_id
    return f"session_{negotiation_id}"


def _negotiation_id_from_sshsign_session_id(sshsign_session_id: str) -> str:
    """Inverse of _sshsign_session_id. sshsign's get-session returns the
    prefixed form (e.g. 'session_neg_X'); our on-disk layout keys off the raw negotiation_id
    ('neg_X'). Called by the joiner to recover the raw id after fetching
    a session by code. Tolerates an already-unprefixed input so it's
    safe to apply twice.
    """
    if not sshsign_session_id:
        return ""
    if sshsign_session_id.startswith("session_"):
        return sshsign_session_id[len("session_"):]
    return sshsign_session_id


def _lease_holder(output_dir: Path, role: str, action: str) -> str:
    """Stable-ish holder label for sshsign workflow leases.

    It intentionally contains no secrets; it only helps operators see which
    process owns a live claim when a second process gets `lease_held`.
    """
    host = (os.environ.get("HOSTNAME") or "local").split(".")[0]
    return f"claw-negotiate:{host}:{os.getpid()}:{role}:{action}:{output_dir.name}"


def _acquire_workflow_lease(
    client,
    *,
    output_dir: Path,
    session_id: str,
    role: str,
    action: str,
    ttl_seconds: int = 120,
) -> dict | None:
    holder = _lease_holder(output_dir, role, action)
    try:
        payload = client.acquire_lease(
            session_id=session_id,
            role=role,
            action=action,
            holder=holder,
            ttl_seconds=ttl_seconds,
        )
        if isinstance(payload, dict):
            return payload
        # Unit-test mocks often leave acquire_lease as a bare MagicMock.
        # Return a syntactically valid handle so the flow can exercise
        # sequencing without depending on a full fake sshsign server.
        return {
            "session_id": session_id,
            "role": role,
            "action": action,
            "holder": holder,
            "generation": 1,
        }
    except LeaseHeldError as e:
        sys.stderr.write(
            f"{action} lease held for {session_id}/{role} "
            f"by {e.holder or 'another worker'} until {e.expires_at or 'unknown'}\n"
        )
        return None


def _check_workflow_lease(client, lease: dict | None) -> bool:
    if not lease:
        return False
    try:
        client.check_lease(
            session_id=lease["session_id"],
            role=lease["role"],
            action=lease["action"],
            holder=lease["holder"],
            generation=int(lease["generation"]),
        )
        return True
    except (LeaseHolderMismatchError, LeaseExpiredError, SshsignSessionError) as e:
        sys.stderr.write(f"workflow lease check failed: {e}\n")
        return False


def _release_workflow_lease(client, lease: dict | None) -> None:
    if not lease:
        return
    try:
        client.release_lease(
            session_id=lease["session_id"],
            role=lease["role"],
            action=lease["action"],
            holder=lease["holder"],
            generation=int(lease["generation"]),
        )
    except SshsignSessionError as e:
        # Release is cleanup. The server TTL is the final backstop.
        sys.stderr.write(f"workflow lease release failed: {e}\n")


def _has_authoritative_offer_history(
    negotiation_id: str,
    sshsign_host: str = "sshsign.dev",
    history_fn=None,
) -> bool:
    """True when sshsign already has at least one offer row.

    The upstream distributed runner currently rehydrates history only for
    the non-first mover. If the first mover restarts after offers exist,
    it can replay Round 0 and corrupt the public transcript, so recovery
    must fail closed until the runner can resume from history correctly.
    """
    if history_fn is None:
        history_fn = _ssh_history
    rows = history_fn(negotiation_id, sshsign_host=sshsign_host)
    return bool(rows)


def _resolve_group_chat_id(
    session_id: str,
    session_client=None,
) -> str | None:
    """Read the session's bound Telegram group chat_id, or None if unbound.

    Phase 8 uses sshsign's `group_chat_id` column (set via the K0
    `bind-group` RPC) to pin the "live negotiation" venue. If the session
    has been bound to a group, returns the chat_id as a string (negative
    int); otherwise returns None and the caller keeps streaming to the
    user's DM.

    Defensive: any error talking to sshsign (missing session, network
    problem, malformed response) returns None rather than raising, so a
    momentary sshsign hiccup never prevents the user from seeing their
    own DM stream.
    """
    if not session_id:
        return None
    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )
    try:
        sess = client.get_session(session_id=session_id)
    except (SshsignSessionError, Exception):  # noqa: BLE001 — defensive
        return None
    raw = sess.get("group_chat_id")
    if raw in (None, 0, "0", ""):
        return None
    try:
        as_int = int(raw)
    except (TypeError, ValueError):
        return None
    if as_int == 0:
        return None
    return str(as_int)


# Lightweight regex used for fast role pre-classification before the
# slow Claude call. Mirrors _BIND_CODE_RE; deliberately conservative
# (requires the INV- prefix). Used only to reject obvious wrong-bot
# requests early; the parsed `role` field from extract_constraints is
# still the authoritative post-parse signal.
_INVESTOR_HINT_RE = re.compile(
    r"\b(?:INV-[A-Z0-9]+|join(?:ing)?\s+(?:as|the)?\s*invest|as\s+investor)\b",
    re.IGNORECASE,
)

_STARTGROUP_PAYLOAD_RE = re.compile(
    r"^\s*/start(?:@\w+)?\s+(INV-[A-Z0-9]+)\s*$",
    re.IGNORECASE,
)


def _telegram_startgroup_payload(message: str) -> str | None:
    """Return INV code from Telegram's startgroup deep-link payload.

    Tapping an "add bot to group" button can produce a `/start@bot INV-...`
    message in the target group. That is transport plumbing, not a new SAFE
    request, so prepare/bind should stop before role/active negotiation gates.
    """
    m = _STARTGROUP_PAYLOAD_RE.match(message or "")
    return m.group(1).upper() if m else None


def _classify_bot_role() -> str | None:
    """Return the bot's configured role per env, or None if unset.

    NEGOTIATE_SAFE_BOT_ROLE is the explicit operator-set knob:
      "founder"  → only founder-shaped requests accepted on this bot
      "investor" → only investor-shaped requests accepted
      unset / "either" → no enforcement (test default)

    Falls back to inference from FOUNDER_NAME / INVESTOR_NAME for
    droplets that haven't set the explicit knob yet:
      FOUNDER_NAME set, INVESTOR_NAME unset → founder
      INVESTOR_NAME set, FOUNDER_NAME unset → investor
      both set or both unset → None (no enforcement)
    """
    explicit = (os.environ.get("NEGOTIATE_SAFE_BOT_ROLE") or "").strip().lower()
    if explicit in ("founder", "investor"):
        return explicit
    if explicit:
        # Anything else (including the explicit "either") means
        # operator chose to disable enforcement; do NOT fall through
        # to env-name inference. Falling through caused tests to
        # accidentally inherit "founder" from conftest's FOUNDER_NAME
        # default.
        return None

    # No explicit knob — fall back to inferring from identity env.
    has_f = bool((os.environ.get("FOUNDER_NAME") or "").strip())
    has_i = bool((os.environ.get("INVESTOR_NAME") or "").strip())
    if has_f and not has_i:
        return "founder"
    if has_i and not has_f:
        return "investor"
    return None


def _counterparty_bot_handle_from_session(message: str, bot_role: str) -> str:
    """Resolve the counterparty bot's Telegram @username for the
    rejection card by looking up the session referenced in the
    rejected message (if any). Sshsign is the trust anchor — the
    handle is whatever the OTHER side's bot wrote into the session.

    Returns an "@handle" string when sshsign yields one, or a
    generic phrase ("the investor bot") when there's no INV code in
    the message OR sshsign doesn't have a handle on file.

    No environment-variable fallback: we used to have
    NEGOTIATE_SAFE_COUNTERPARTY_BOT, but it required the operator to
    know the counterparty bot at deploy time — wrong assumption for
    the multi-operator world.
    """
    generic = "the investor bot" if bot_role == "founder" else "the founder bot"
    m = _BIND_CODE_RE.search(message or "")
    if not m:
        return generic
    code = m.group(1).upper()
    try:
        client = SshsignSession(host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"))
        sess = client.get_session(session_code=code)
    except SshsignSessionError:
        return generic

    if bot_role == "founder":
        # Rejecting an investor-shaped message on the founder bot —
        # the investor's destination is the OTHER party's bot, but
        # the SESSION's founder_bot_handle in metadata_public is
        # actually OUR own. We want the investor bot's handle, which
        # lives on the investor's member row. Pre-investor-join,
        # this isn't set — fall back to generic.
        for member in (sess.get("members") or []):
            if (member.get("role") or "").lower() == "investor":
                handle = (member.get("bot_handle") or "").strip()
                if handle:
                    if not handle.startswith("@"):
                        handle = "@" + handle
                    return handle
        return generic

    # bot_role == "investor": rejecting a founder-shaped message on
    # the investor bot. The founder's handle is in metadata_public,
    # written at create-session, available pre-join.
    try:
        meta_pub_raw = sess.get("metadata_public") or "{}"
        meta_pub = (
            json.loads(meta_pub_raw) if isinstance(meta_pub_raw, str)
            else (meta_pub_raw or {})
        )
        handle = (meta_pub.get("founder_bot_handle") or "").strip()
        if handle:
            if not handle.startswith("@"):
                handle = "@" + handle
            return handle
    except (json.JSONDecodeError, AttributeError):
        pass
    return generic


def _enforce_bot_role_pre_parse(message: str) -> str | None:
    """Fast regex-only role check that runs BEFORE parse_constraints
    so an obvious mismatch (investor-shaped message to founder bot or
    vice versa) gets rejected instantly without burning a Claude
    round-trip.

    Returns:
      None if no enforcement needed (mode unset, or message matches bot's role)
      A short human-friendly error string explaining the rejection
    """
    bot_role = _classify_bot_role()
    if bot_role is None:
        return None  # no enforcement configured

    looks_investor = bool(_INVESTOR_HINT_RE.search(message))
    handle = _counterparty_bot_handle_from_session(message, bot_role)

    if looks_investor and bot_role == "founder":
        return (
            "⛔ This bot represents the FOUNDER side.\n\n"  # ⛔
            f"Joining a negotiation as the investor goes through {handle}. "
            "DM there with your join message instead."
        )
    if not looks_investor and bot_role == "investor":
        return (
            "⛔ This bot represents the INVESTOR side.\n\n"  # ⛔
            f"To start a new negotiation as the founder, DM {handle}. "
            "To join an existing one as the investor, include the "
            "INV-XXXXX code in your message here."
        )
    return None


def _enforce_bot_role_post_parse(parsed_role: str, message: str = "") -> str | None:
    """After-parse double-check: parse_constraints might infer a role
    that's contradictory to the bot's configured role even when the
    pre-parse regex didn't catch it. Returns error string or None.

    Optionally takes the original message so the rejection card can
    pull a session-derived counterparty handle (when the message
    contains an INV code).
    """
    bot_role = _classify_bot_role()
    if bot_role is None:
        return None
    parsed = (parsed_role or "").strip().lower()
    if parsed and parsed != bot_role:
        handle = _counterparty_bot_handle_from_session(message, bot_role)
        if bot_role == "founder":
            return (
                "⛔ This bot represents the FOUNDER side, but your "  # ⛔
                f"request reads as an INVESTOR action. DM {handle} instead."
            )
        return (
            "⛔ This bot represents the INVESTOR side, but your "  # ⛔
            f"request reads as a FOUNDER action. DM {handle} instead."
        )
    return None


def _has_active_negotiation() -> tuple[bool, str | None]:
    """Detect whether this droplet already has an in-flight negotiation
    that should block a new one. Two signals:

    1. State pointers: any pointer that maps to a non-terminal sshsign
       session (status in {open, joined}) is an active two-party
       negotiation. Stale pointers (terminal session) are quietly
       cleaned by the next scan tick; we tolerate them here.
    2. ``.session.pid`` in /tmp/safe_negotiate: a still-running
       background process from a prior demo or two-party stream that
       hasn't exited yet.

    Returns ``(True, descriptor)`` to block a new mint, or
    ``(False, None)`` to allow it. The descriptor is human-friendly
    and suitable for inclusion in the rejection card.

    Network/sshsign errors fall through as "no block" — we'd rather
    let a fresh mint proceed than wedge the user behind a transient
    transport failure.
    """
    # Check two-party state pointers first.
    try:
        pointers = state_store.list_active()
    except Exception:  # noqa: BLE001
        pointers = []
    if pointers:
        try:
            client = SshsignSession(host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"))
        except Exception:  # noqa: BLE001
            client = None
        for state in pointers:
            try:
                if client is None:
                    raise SshsignSessionError("no client")
                sess = client.get_session(
                    session_id=_sshsign_session_id(state["negotiation_id"]),
                )
                status = (sess.get("status") or "").lower()
                if status in ("open", "joined"):
                    return (True, state.get("session_code") or state["negotiation_id"])
            except SshsignSessionError:
                # Couldn't reach sshsign — don't block on uncertain state;
                # a stale pointer for a terminal session shouldn't trap
                # the user out of new mints.
                continue

    # Check demo-mode PID file. Two failure modes the naive `os.kill(pid, 0)`
    # check misses: (a) the PID is dead — fine, raises OSError, we treat as
    # not-blocked; (b) the PID got REUSED by an unrelated process (sshd, cron,
    # bash, etc.) — kill(0) succeeds and we falsely block all future mints.
    # Verify it's actually ours by reading /proc/<pid>/cmdline and looking for
    # a run_safe.py / negotiate_safe signature. Any failure of that check
    # treats the pidfile as stale and unlinks it.
    pid_path = Path("/tmp/safe_negotiate/.session.pid")
    try:
        pid_text = pid_path.read_text().strip()
        pid = int(pid_text)
        os.kill(pid, 0)  # raises if process is gone
    except (OSError, ValueError, FileNotFoundError):
        # No pid file, unparsable, or process is dead. Either way: not
        # blocked. Best-effort cleanup of the stale file.
        try:
            pid_path.unlink()
        except (OSError, FileNotFoundError):
            pass
        return (False, None)

    # PID exists. Verify it's actually one of ours before treating as a
    # block. Linux-only path; on platforms without /proc we fall back to
    # treating any live PID as ours (preserves existing behavior on macOS
    # tests). A successful match means the process really is a negotiate
    # run; mismatch means PID-reuse — drop the pidfile, allow new mint.
    cmdline_path = Path(f"/proc/{pid}/cmdline")
    try:
        cmdline = cmdline_path.read_bytes().decode("utf-8", "replace")
    except (OSError, FileNotFoundError):
        # Either the proc entry vanished between kill(0) and now, or
        # we're on a non-Linux platform. Treat as live-and-ours to
        # match prior behavior; ops can manually rm the pidfile if
        # this becomes a problem.
        return (True, "a running negotiation")

    if "run_safe.py" in cmdline or "negotiate_safe" in cmdline:
        return (True, "a running negotiation")

    # PID belongs to an unrelated process — pidfile is stale. Drop it
    # so the user isn't blocked from minting forever.
    sys.stderr.write(
        f"_has_active_negotiation: pid {pid} is not ours "
        f"(cmdline={cmdline[:80]!r}); cleaning stale pidfile\n"
    )
    try:
        pid_path.unlink()
    except (OSError, FileNotFoundError):
        pass
    return (False, None)


def _pid_file_has_live_negotiation(output_dir: Path) -> bool:
    """Return true when output_dir/.session.pid points at our live process."""
    pid_path = output_dir / ".session.pid"
    try:
        pid = int(pid_path.read_text().strip())
        os.kill(pid, 0)
    except (OSError, ValueError, FileNotFoundError):
        return False

    cmdline_path = Path(f"/proc/{pid}/cmdline")
    try:
        cmdline = cmdline_path.read_bytes().decode("utf-8", "replace")
    except (OSError, FileNotFoundError):
        return True
    return "run_safe.py" in cmdline or "negotiate_safe" in cmdline


def run_prepare(
    message: str,
    output_dir: str,
    founder_name: str = "",
    founder_title: str = "CEO",
    chat_id_flag: str | None = None,
    sender=send_telegram,
) -> int:
    """Parse NL constraints, write config.json, and push the confirm card to chat.

    The confirm card uses format_event.py so the copy lives in one place and
    the model never generates UI itself.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_trace(out, "prepare.start", phase="prepare")

    # Resolve chat_id first so we can push an interstitial before the slow parse.
    chat_id = resolve_chat_id(chat_id_flag)

    startgroup_code = _telegram_startgroup_payload(message)
    if startgroup_code:
        write_trace(out, "prepare.noop", phase="prepare", reason="startgroup_payload", chat_id=chat_id, session_code=startgroup_code)
        return 0

    # Gate 1: bot-role pre-check. Reject obviously wrong-bot requests
    # (investor-shaped to founder bot or vice versa) BEFORE we burn a
    # Claude round-trip on parse_constraints. The regex is conservative;
    # the post-parse check below is the authoritative backstop.
    role_err = _enforce_bot_role_pre_parse(message)
    if role_err:
        if chat_id:
            sender(chat_id, message=role_err)
        write_trace(out, "prepare.rejected", phase="prepare", reason="role_pre_parse", chat_id=chat_id)
        return 1

    # Gate 2: single-active-negotiation. Each bot+droplet handles one
    # negotiation at a time. If there's already an in-flight session
    # (two-party state pointer + non-terminal sshsign status, OR a live
    # .session.pid from demo mode), refuse the new mint cleanly and
    # tell the user how to free the slot.
    has_active, descriptor = _has_active_negotiation()
    if has_active:
        body = format_event({
            "type": "active_negotiation_block",
            "descriptor": descriptor,
        })
        if chat_id and body:
            sender(chat_id, message=body)
        write_trace(out, "prepare.rejected", phase="prepare", reason="active_negotiation", descriptor=descriptor, chat_id=chat_id)
        return 1

    # First-run guard: if the user hasn't configured their identity yet,
    # stash their negotiation message and ask for identity before parsing.
    # They'll reply with "I'm Name, Title at Company" → run_setup picks up
    # the stashed message and continues the flow automatically.
    if not _identity_configured():
        embedded_identity = _embedded_investor_identity(message)
        if embedded_identity:
            updates = _build_env_updates(embedded_identity)
            failures = _persist_env_updates(updates)
            # Even if OpenClaw config persistence is unavailable in this
            # process, the current negotiation can continue using the
            # identity parsed from the join request.
            for key, value in updates.items():
                os.environ[key] = value
            write_trace(
                out,
                "prepare.identity_from_join",
                phase="prepare",
                failures=failures,
                chat_id=chat_id,
            )
        else:
            try:
                IDENTITY_SENTINEL_PATH.parent.mkdir(parents=True, exist_ok=True)
                IDENTITY_SENTINEL_PATH.write_text(message)
            except OSError as e:
                sys.stderr.write(f"Could not stash pending message: {e}\n")
            if chat_id:
                sender(chat_id, message=_identity_setup_prompt())
            write_trace(out, "prepare.identity_required", phase="prepare", chat_id=chat_id)
            return 2

    if chat_id:
        sender(chat_id, message="\u23f3 Reading your negotiation terms\u2026")  # ⏳

    # Keep the typing indicator alive during parsing and the rest of prepare.
    # Stopped in `finally` so the confirm card isn't competing with a
    # lingering "typing" status.
    typing = TypingLoop(chat_id=chat_id or "", bot_token=get_bot_token())
    typing.start()

    try:
        try:
            constraints = extract_constraints(message)
        except (ValueError, RuntimeError) as e:
            sys.stderr.write(f"Parse error: {e}\n")
            if chat_id:
                sender(chat_id, message=(
                    "\u26a0\ufe0f Couldn't parse your request. "  # ⚠️
                    "Please rephrase your terms and try again."
                ))
            write_trace(out, "prepare.parse_error", phase="prepare", error=str(e), chat_id=chat_id)
            return 1

        if constraints.get("discount_max") is None and constraints.get("discount_min") is not None:
            constraints["discount_max"] = constraints["discount_min"]
        required_fields = ("valuation_cap_min", "valuation_cap_max", "discount_min", "pro_rata", "mfn")
        missing = [f for f in required_fields if constraints.get(f) is None]
        if missing:
            sys.stderr.write(f"Ambiguous constraints (null values): {missing}. Ask the user to clarify.\n")
            write_trace(out, "prepare.ambiguous", phase="prepare", missing=missing, chat_id=chat_id)
            return 1

        # Gate 3: bot-role post-parse backstop. The regex pre-check
        # catches the obvious cases; this catches subtler classifier
        # outputs (e.g., parse_constraints inferring role=investor from
        # phrasing the regex missed). Critical privacy gate — without
        # it, a wrong-role message produces a confirm card revealing
        # the OTHER party's constraints in this party's chat.
        role_err = _enforce_bot_role_post_parse(constraints.get("role") or "", message)
        if role_err:
            if chat_id:
                sender(chat_id, message=role_err)
            write_trace(out, "prepare.rejected", phase="prepare", reason="role_post_parse", role=constraints.get("role"), chat_id=chat_id)
            return 1

        constraints = _enrich_constraints_from_profile(constraints)
        missing_counterparty = _missing_counterparty_identity(constraints)
        if missing_counterparty:
            if chat_id:
                sender(chat_id, message=(
                    "I need the investor's name and firm for the signing view "
                    "and final SAFE.\n\n"
                    "Please resend the request with the investor included, for example:\n"
                    "\"Live negotiation with Nora Vassileva at SD Fund. "
                    "Cap $30M to $40M, 10% discount, pro-rata required.\""
                ))
            write_trace(
                out,
                "prepare.counterparty_identity_required",
                phase="prepare",
                missing=missing_counterparty,
                chat_id=chat_id,
            )
            return 1

        # Two-party join path: the investor pasted a session_code. Validate
        # the session via sshsign, merge founder-side metadata into
        # constraints, and stash the shared session_id in config so mint
        # can reuse it instead of generating a fresh one.
        joined_session: dict | None = None
        if constraints.get("session_code"):
            sess_payload, err = _fetch_session_for_join(constraints["session_code"])
            if err or not sess_payload:
                if chat_id:
                    sender(chat_id, message=(
                        "\u26a0\ufe0f " + (err or "Couldn't find that negotiation.")  # ⚠️
                        + "\n\nDouble-check the code with your counterparty."
                    ))
                write_trace(out, "prepare.join_lookup_failed", phase="prepare", session_code=constraints.get("session_code"), error=err, chat_id=chat_id)
                return 1
            constraints = _enrich_constraints_from_session(constraints, sess_payload)
            joined_session = sess_payload
            # Inverted-invitation: prefer the sshsign-authoritative
            # founder_bot_handle over whatever the investor typed.
            # The human-typed value can be a typo; the session row is
            # the trust anchor (founder bot self-wrote it at create-
            # session). If sshsign has nothing, keep the parsed value
            # as a best-effort fallback.
            try:
                meta_pub = sess_payload.get("metadata_public")
                if isinstance(meta_pub, str):
                    meta_pub = json.loads(meta_pub)
                if isinstance(meta_pub, dict):
                    sshsign_handle = (meta_pub.get("founder_bot_handle") or "").strip()
                    if sshsign_handle:
                        if not sshsign_handle.startswith("@"):
                            sshsign_handle = "@" + sshsign_handle
                        constraints["founder_bot_handle"] = sshsign_handle
            except (json.JSONDecodeError, AttributeError):
                pass

        config = {
            "constraints": constraints,
            # Legacy field; run_mint reads identity from constraints +
            # FOUNDER_*/INVESTOR_*/COMPANY_NAME env per upstream convention.
            "founder_name": founder_name or os.environ.get("FOUNDER_NAME") or "Founder",
            "founder_title": founder_title,
            "message": message,
        }
        if joined_session:
            config["session"] = {
                "session_id": joined_session.get("session_id"),
                "session_code": joined_session.get("session_code"),
                "status": joined_session.get("status"),
                # Save the founder's APOA pubkey (if we got it in members)
                # so mint can write it to disk without a second sshsign call.
                "counterparty_apoa_pubkey_pem": _extract_counterparty_pubkey(joined_session),
            }

        if chat_id:
            body = format_event({"type": "confirm", "constraints": constraints})
            if body:
                sender(chat_id, message=body)
        else:
            sys.stderr.write(
                "Warning: no chat_id resolvable; skipping confirm push. "
                "The model will need to relay constraints manually.\n"
            )
        (out / "config.json").write_text(json.dumps(config, indent=2))

        if not chat_id:
            sys.stdout.write(json.dumps(constraints, indent=2) + "\n")
        write_trace(
            out,
            "prepare.completed",
            phase="prepare",
            role=constraints.get("role"),
            mode=constraints.get("mode"),
            session_code=constraints.get("session_code"),
            chat_id=chat_id,
        )
        return 0
    finally:
        typing.stop()


def _extract_counterparty_pubkey(session_payload: dict) -> str:
    """Return the first member's APOA pubkey PEM that isn't the caller's own.

    get-session returns the members list only when the caller is a member;
    for a prospective joiner (not yet a member) the list is empty and we
    rely on join-session + a follow-up get-session to retrieve it. In that
    case this returns '' and mint writes a placeholder that _stream_negotiate
    can refresh later.
    """
    members = session_payload.get("members") or []
    for m in members:
        pem = m.get("apoa_pubkey_pem") or ""
        if pem:
            return pem
    return ""


def run_mint(output_dir: str, config: dict, telegram_user_id: int | None = None) -> int:
    """Mint APOA tokens using the constraints from config.json.

    telegram_user_id, when provided (founder two-party path), is stashed on
    the sshsign session's metadata_member so the Phase 8 /bind handler can
    verify that the caller of /bind matches the session creator.
    """
    write_trace(output_dir, "mint.start", phase="mint", role=(config.get("constraints") or {}).get("role"), mode=(config.get("constraints") or {}).get("mode"))

    constraints = config["constraints"]
    out = Path(output_dir)

    # Join mode: the investor is entering a session the founder already
    # created. Reuse the shared session_id as the negotiation_id so both
    # sides' APOA tokens, pending_signatures, and offer logs correlate.
    shared_session = config.get("session")
    if shared_session and shared_session.get("session_id"):
        # Sshsign's get-session returns the prefixed form; strip it so
        # local token/config files use the same raw negotiation_id as the founder.
        negotiation_id = _negotiation_id_from_sshsign_session_id(
            shared_session["session_id"]
        )
    else:
        negotiation_id = f"neg_{uuid.uuid4().hex[:12]}"
    neg_dir = out / "negotiations" / negotiation_id
    neg_dir.mkdir(parents=True, exist_ok=True)

    expires_dt = datetime.now(timezone.utc) + timedelta(
        seconds=int(os.environ.get("NEGOTIATION_TTL", "3600"))
    )
    expires_str = expires_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    service = build_service_name(
        str(constraints.get("company_name") or os.environ.get("COMPANY_NAME") or "Company"),
        negotiation_id,
    )
    try:
        mint_output, user_role = write_local_mint_files(
            negotiation_id=negotiation_id,
            constraints=constraints,
            neg_dir=neg_dir,
            expires_at_epoch=int(expires_dt.timestamp()),
            expires_str=expires_str,
            service=service,
            shared_session=bool(shared_session),
            sshsign_host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
        )
    except Exception as exc:  # noqa: BLE001 - surface setup/signing backend errors
        sys.stderr.write(f"Mint failed: {exc}\n")
        write_trace(output_dir, "mint.failed", phase="mint", reason="local_mint", error=str(exc))
        return 3
    mint_output.update({
        "user_role": user_role,
        "mode": (constraints.get("mode") or "demo").lower(),
    })

    # Two-party mode: register (creator) or join (joiner) the signing
    # session with sshsign. Creator flow (no shared_session in config)
    # creates a fresh session and gets a shareable code. Joiner flow
    # publishes the joiner's APOA pubkey to the existing session.
    if mint_output["mode"] == "two_party":
        if shared_session:
            joined = _join_signing_session(
                mint_output=mint_output,
                shared_session=shared_session,
                user_role=user_role,
                neg_dir=neg_dir,
                repo=SKILL_DIR,
                telegram_user_id=telegram_user_id,
            )
            if joined is None:
                write_trace(output_dir, "mint.failed", phase="mint", reason="join_signing_session", negotiation_id=negotiation_id)
                return 3
            mint_output.update(joined)
        else:
            session_registered = _register_signing_session(
                mint_output, constraints, user_role, neg_dir,
                telegram_user_id=telegram_user_id,
            )
            if session_registered is None:
                write_trace(output_dir, "mint.failed", phase="mint", reason="register_signing_session", negotiation_id=negotiation_id)
                return 3
            mint_output.update(session_registered)

    # Clean up any stale .signed marker from a PRIOR negotiation that
    # ran in the same output_dir. Without this, run_cancel reads the
    # leftover marker and thinks the user signed THIS session — auto-
    # routes to `cancel-session --rescind` instead of plain cancel.
    # Caught live (INV-XXFJ2 → rescinded_after_sign despite being open).
    try:
        (out / ".signed").unlink()
    except FileNotFoundError:
        pass
    except OSError as _e:
        sys.stderr.write(f"clean stale .signed: {_e}\n")

    (out / "mint.json").write_text(json.dumps(mint_output, indent=2))

    # P7-5 + symmetric Path 1: leave a state pointer for BOTH founder
    # and investor in two-party mode so a later cron-scanned `scan`
    # turn can resume the negotiation when OC reaps the foreground
    # process. Founder pointers drive Phase A/B (create-group card →
    # post-/bind stream); investor pointers drive the post-mint wait
    # for `founder_streaming_at` (replacing the old in-process 180s
    # poll that timed out before the founder finished /binding).
    # Demo mode runs inline; no state needed.
    if mint_output["mode"] == "two_party":
        session_code = mint_output.get("session_code")
        if session_code:
            try:
                state_payload = {
                    "negotiation_id": negotiation_id,
                    "output_dir": str(out),
                    "session_code": session_code,
                    "role": user_role,
                }
                # Persist the user's DM chat_id so a cron-triggered
                # scan/resume can route role-specific cards (founder:
                # create-group; investor: heartbeat / both-online)
                # back to the right user even after the foreground
                # process is reaped. In a DM, chat_id == user_id
                # (positive int).
                if telegram_user_id:
                    if user_role == "founder":
                        state_payload["founder_dm_chat_id"] = str(telegram_user_id)
                    elif user_role == "investor":
                        state_payload["investor_dm_chat_id"] = str(telegram_user_id)
                state_store.write_state(state_payload)
            except state_store.StateCorruptError as e:
                # Non-fatal: the user can still wait inline this
                # turn; they just won't survive a reap. Surface the
                # reason so ops can fix the state dir.
                sys.stderr.write(f"state_store.write_state failed: {e}\n")
        # Install the global cron scan job (idempotent). Both roles
        # need cron — investor's resume runs from the same loop as
        # the founder's, just dispatched on the pointer's `role`.
        interval = os.environ.get("CLAW_NEGOTIATE_SCAN_INTERVAL", CRON_SCAN_DEFAULT_INTERVAL)
        ok, err = ensure_cron(interval=interval)
        if not ok and err:
            sys.stderr.write(f"ensure_cron: {err}\n")

    sys.stdout.write(json.dumps({
        "type": "authorized",
        "negotiation_id": negotiation_id,
        "service": service,
        "expires_at": expires_str,
        "mode": mint_output["mode"],
        "session_code": mint_output.get("session_code"),
    }) + "\n")
    sys.stdout.flush()
    write_trace(
        output_dir,
        "mint.completed",
        phase="mint",
        negotiation_id=negotiation_id,
        role=user_role,
        mode=mint_output["mode"],
        session_code=mint_output.get("session_code"),
    )

    return 0


def _wait_for_counterparty(
    session_id: str,
    session_code: str,
    chat_id: str,
    counterparty_label: str,
    sender=send_telegram,
    session_client=None,
    poll_interval: int = 10,
    max_wait_seconds: int = 24 * 60 * 60,  # matches session TTL; sshsign expires first
    typing_factory=None,
    sleep_fn=None,
    now_fn=None,
) -> str:
    """Poll sshsign for the counterparty's join. Returns the final status:
      'joined' — success; caller proceeds to run_distributed
      'expired' — invitation TTL hit; session unusable
      'canceled' — founder canceled; exit cleanly
      'error' — persistent ssh errors; caller surfaces to user

    Periodic waiting cards are pushed at elapsed milestones (5, 15, 60, 180,
    600 minutes) so the user knows we're still alive without being spammed.
    Typing loop runs continuously to keep the UI feeling active.
    """
    if sleep_fn is None:
        import time as _time
        sleep_fn = _time.sleep
    if now_fn is None:
        import time as _time
        now_fn = _time.time

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )

    if typing_factory is None:
        typing = TypingLoop(chat_id=chat_id, bot_token=get_bot_token())
    else:
        typing = typing_factory(chat_id)
    typing.start()

    start = now_fn()
    milestones_minutes = [5, 15, 60, 180, 600]
    fired_milestones: set[int] = set()

    try:
        while True:
            elapsed = now_fn() - start
            if elapsed > max_wait_seconds:
                return "expired"

            try:
                sess = client.get_session(session_id=session_id)
            except SshsignSessionError as e:
                # Transient ssh errors happen (network blips); retry.
                sys.stderr.write(f"get-session transient error: {e}\n")
                sleep_fn(poll_interval)
                continue

            status = (sess.get("status") or "").lower()
            if status == "joined":
                body = format_event({
                    "type": "counterparty_joined",
                    "counterparty_label": counterparty_label,
                })
                if body:
                    sender(chat_id, message=body)
                return "joined"
            if status in ("canceled", "rescinded_after_sign"):
                return "canceled"
            if status == "expired":
                return "expired"

            # Still open — push a waiting card at milestones.
            elapsed_min = int(elapsed / 60)
            for milestone in milestones_minutes:
                if elapsed_min >= milestone and milestone not in fired_milestones:
                    fired_milestones.add(milestone)
                    remaining_hours = (max_wait_seconds - elapsed) / 3600
                    body = format_event({
                        "type": "waiting",
                        "elapsed_minutes": elapsed_min,
                        "remaining_hours": remaining_hours,
                    })
                    if body:
                        sender(chat_id, message=body)
                    break

            sleep_fn(poll_interval)
    finally:
        typing.stop()


def _stream_to_telegram(
    output_dir: Path,
    chat_id: str,
    constraints: dict | None,
    bot_username: str,
    stream_helper: Path = STREAM_HELPER,
    sender=send_telegram,
    popen=subprocess.Popen,
    typing_factory=None,
    group_chat_id: str | None = None,
    dm_sender=send_signing_url_to_dm,
    negotiation_id: str | None = None,
    sshsign_host: str = "sshsign.dev",
    history_fn=None,
    history_interval: float = 1.0,
) -> tuple[int, dict | None]:
    """Spawn the streaming helper; push each event to Telegram as it fires.

    Target routing (Phase 8 K2):
      - `chat_id` is the user's DM (always required). When there is no
        bound group, everything goes to chat_id (Phase 7 behavior).
      - `group_chat_id`, when set, is the Telegram group the session is
        bound to (via K0/K1 /bind). All stream-of-consciousness events
        (rounds, outcome, propose_new_terms, signed) go to the GROUP so
        both parties watch live.
      - The SIGNING URL is the exception: it always goes to the DM via
        the `send_signing_url_to_dm` primitive. Structural privacy —
        the primitive's type signature refuses a group target. The group
        receives a placeholder ("⏳ [Party] signing — check your DM")
        so both observers see the state without the URL leaking.

    P8-1: when `negotiation_id` is set, a background thread polls
    sshsign's authoritative offer log via `history --negotiation-id`
    every `history_interval` seconds and synthesizes offer/counter/
    accept events to supplement upstream's stdout stream. Necessary
    because `run_distributed` only emits the final `signing` event —
    without this poll the group never sees per-round cards. Events
    are deduped by (type, round, party) so events that DO come through
    stdout (e.g. in demo mode) aren't doubled. `history_fn` is
    injectable for testing.

    Returns 0 on clean exit, the subprocess returncode otherwise.
    `sender`, `popen`, and `dm_sender` are injectable for testing.
    """
    import threading

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    cmd = [sys.executable, "-u", str(stream_helper), "--output-dir", str(output_dir)]
    try:
        mint_for_stream = json.loads((output_dir / "mint.json").read_text())
    except (OSError, json.JSONDecodeError):
        mint_for_stream = {}
    negotiate_repo_path = mint_for_stream.get("negotiate_repo_path") or ""
    if negotiate_repo_path:
        cmd.extend(["--negotiate-repo", str(negotiate_repo_path)])

    target_chat = stream_target(chat_id, group_chat_id)
    try:
        (output_dir / "events.ndjson").unlink()
    except FileNotFoundError:
        pass
    except OSError as e:
        sys.stderr.write(f"stream: clearing stale events archive failed: {e}\n")

    if typing_factory is None:
        typing = TypingLoop(chat_id=target_chat, bot_token=get_bot_token())
    else:
        typing = typing_factory(target_chat)
    typing.start()

    events: list[dict] = []
    seen: set[tuple[str, int, str]] = set()
    emit_lock = threading.Lock()
    stderr_lines: list[str] = []

    def _emit(event: dict) -> None:
        """Format + route + record. Dedups offer/counter/accept by
        (type, round, party) so the stdout + history poller can run
        concurrently without double-posting."""
        etype = event.get("type")
        if etype in ("offer", "counter", "accept"):
            try:
                key = (etype, int(event.get("round", 0)), event.get("party") or "")
            except (TypeError, ValueError):
                return
            with emit_lock:
                if key in seen:
                    return
                seen.add(key)
                events.append(event)
        else:
            with emit_lock:
                events.append(event)

        if etype == "signing":
            event = _augment_signing_url(event, bot_username)

        message = format_event(event, constraints=constraints)
        route_stream_message(
            event=event,
            message=message,
            chat_id=chat_id,
            group_chat_id=group_chat_id,
            constraints=constraints,
            sender=sender,
            dm_sender=dm_sender,
        )

        if etype == "outcome" and event.get("result") == "max_rounds":
            cp_label = _counterparty_label_from_constraints(constraints or {})
            follow = format_event({
                "type": "propose_new_terms",
                "counterparty_label": cp_label,
            })
            if follow:
                sender(target_chat, message=follow)

    def _drain_history() -> None:
        if history_fn is not None:
            rows = history_fn()
        elif negotiation_id:
            rows = _ssh_history(negotiation_id, sshsign_host=sshsign_host)
        else:
            rows = None
        if not isinstance(rows, list):
            return
        for row in rows:
            synthesized = _synthesize_offer_event(row)
            if synthesized:
                try:
                    _emit(synthesized)
                except Exception as e:  # never let a render error kill the poller
                    sys.stderr.write(f"stream: history emit failed: {e}\n")

    try:
        proc = popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

        stop_event = threading.Event()
        poller: threading.Thread | None = None
        stderr_thread: threading.Thread | None = None

        if proc.stderr is not None:
            def _drain_stderr() -> None:
                for raw_err in proc.stderr:
                    line = raw_err.rstrip()
                    if not line:
                        continue
                    stderr_lines.append(line)
                    sys.stderr.write(f"stream helper: {line}\n")

            stderr_thread = threading.Thread(target=_drain_stderr, daemon=True)
            stderr_thread.start()

        if negotiation_id or history_fn is not None:
            def _poll() -> None:
                while not stop_event.is_set():
                    try:
                        _drain_history()
                    except Exception as e:
                        sys.stderr.write(f"stream: history poll failed: {e}\n")
                    stop_event.wait(history_interval)

            poller = threading.Thread(target=_poll, daemon=True)
            poller.start()

        assert proc.stdout is not None
        for raw in proc.stdout:
            line = raw.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            if event.get("type") == "signing":
                # In distributed mode, upstream can emit the signing event
                # before our periodic history poll has rendered the final
                # accept/deal row. Drain first so the group sees the deal
                # before the private signing prompt.
                try:
                    _drain_history()
                except Exception as e:
                    sys.stderr.write(f"stream: pre-signing history drain failed: {e}\n")
            _emit(event)

        proc.wait()
        if stderr_thread is not None:
            stderr_thread.join(timeout=1.0)

        if poller is not None:
            # One final drain: upstream emits `signing` on stdout before the
            # last offer has necessarily propagated through sshsign's log.
            # Catch anything that arrived in the window between the last
            # poll and subprocess exit.
            try:
                _drain_history()
            except Exception as e:
                sys.stderr.write(f"stream: final history drain failed: {e}\n")
            stop_event.set()
            poller.join(timeout=history_interval + 1.0)
    finally:
        typing.stop()

    try:
        (output_dir / "events.ndjson").write_text(
            "\n".join(json.dumps(e) for e in events) + "\n"
        )
    except OSError:
        pass

    signing_event = next((e for e in events if e.get("type") == "signing"), None)
    if proc.returncode:
        err_tail = " | ".join(stderr_lines[-5:])
        if err_tail:
            sys.stderr.write(f"stream: helper exited {proc.returncode}: {err_tail}\n")
    return proc.returncode or 0, signing_event


def _counterparty_label_from_constraints(constraints: dict) -> str:
    """Human label for the counterparty, used in propose-new-terms follow-up.

    From the user's perspective: if they're the founder, label is the
    investor's name/firm; if investor, it's the founder + company.
    Returns empty string when we can't build a useful label.
    """
    role = (constraints.get("role") or "founder").lower()
    if role == "founder":
        name = constraints.get("investor_name")
        firm = constraints.get("investor_firm")
        if name and firm:
            return f"{name} at {firm}"
        return name or firm or ""
    name = constraints.get("founder_name")
    company = constraints.get("company_name")
    if name and company:
        return f"{name} at {company}"
    return name or company or ""


# ─── Post-stream: envelope polling + finalize + PDF push ────────────────────


def _ssh_envelope_status(
    pending_id: str,
    sshsign_host: str = "sshsign.dev",
    runner=subprocess.run,
) -> str | None:
    """Return the envelope status ('approved' / 'pending' / other) or None on error."""
    try:
        result = runner(
            ["ssh", sshsign_host, "get-envelope", "--id", pending_id],
            capture_output=True, text=True, timeout=15,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        return str(json.loads(result.stdout).get("status", "")) or None
    except json.JSONDecodeError:
        return None


def _poll_envelope_approval(
    pending_id: str,
    sshsign_host: str = "sshsign.dev",
    timeout: int = 900,
    interval: int = 5,
    status_fn=_ssh_envelope_status,
    sleep_fn=None,
) -> bool:
    """Poll until envelope is approved or timeout elapses. True = approved."""
    if sleep_fn is None:
        import time as _time
        sleep_fn = _time.sleep

    elapsed = 0
    while elapsed < timeout:
        status = status_fn(pending_id, sshsign_host)
        if status == "approved":
            return True
        sleep_fn(interval)
        elapsed += interval
    return False


def _ssh_session_status(
    session_id: str,
    sshsign_host: str = "sshsign.dev",
    runner=subprocess.run,
) -> str | None:
    """Return the aggregate session status from `ssh host session --id <id>`.

    sshsign reports 'complete' when every pending in the session is
    `approved`, 'failed' if any is `denied`, 'pending' otherwise. Used by
    the P8-3 both-signed gate so the creator waits until the counterparty
    has also signed before running finalize.
    """
    try:
        result = runner(
            ["ssh", sshsign_host, "session", "--id", session_id],
            capture_output=True, text=True, timeout=15,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0 or not (result.stdout or "").strip():
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    status = payload.get("status") if isinstance(payload, dict) else None
    return str(status) if status else None


def _poll_session_complete(
    session_id: str,
    sshsign_host: str = "sshsign.dev",
    timeout: int = 900,
    interval: int = 5,
    status_fn=_ssh_session_status,
    sleep_fn=None,
) -> bool:
    """Poll until the session aggregates to 'complete' (all pendings approved).

    Returns True on complete, False on timeout or 'failed' (a denial is
    treated as a hard stop — no point waiting longer). The default
    interval of 5s matches _poll_envelope_approval so a creator's wait
    for its own sig + the P8-3 wait for the counterparty have the same
    cadence.
    """
    if sleep_fn is None:
        import time as _time
        sleep_fn = _time.sleep

    elapsed = 0
    while elapsed < timeout:
        status = status_fn(session_id, sshsign_host)
        if status == "complete":
            return True
        if status == "failed":
            return False
        sleep_fn(interval)
        elapsed += interval
    return False


def _is_still_active_session(output_dir: Path) -> bool:
    """Check if this process is still the active negotiation for this output dir.

    When a new `run_safe.py negotiate` starts, it overwrites `.session.pid`
    with its own PID. A previous process whose long poll later times out
    should silently exit rather than push a stale timeout message into the
    chat (that was bug #4 in the PR-A feedback — the 15-min timeout from a
    prior aborted negotiation posted into a new session).
    """
    try:
        pid_file = output_dir / ".session.pid"
        return int(pid_file.read_text().strip()) == os.getpid()
    except (OSError, ValueError):
        # If the file is missing or unreadable, assume we're still active —
        # better to occasionally send a timeout message than suppress a
        # legitimate one.
        return True


def _await_sign_and_push(
    output_dir: Path,
    chat_id: str,
    sshsign_host: str,
    pending_id: str,
    timeout: int = 900,
    poll_interval: int = 5,
    sender=send_telegram,
    poll_fn=_poll_envelope_approval,
    finalize_fn=_finalize_executed_pdf,
    is_active_fn=_is_still_active_session,
    typing_factory=None,
    group_chat_id: str | None = None,
    pre_finalize_wait_fn=None,
) -> int:
    """Wait for signature, finalize PDF, push confirmation + attachment.

    P8-3: when `pre_finalize_wait_fn` is provided, it runs AFTER the
    caller's own sig lands and BEFORE `finalize_fn`. For the creator
    path this gates on "session aggregates to complete (both parties
    signed)", preventing the race where the founder finalized
    immediately after their own sig and produced a partial PDF that
    got posted to the group. The fn must return True when the gate
    passes; returning False causes the flow to post a "counterparty
    not signed yet" note and exit with rc=4.

    Returns 0 if the user received the executed PDF, 1 on timeout, 2 on
    finalize failure, 3 if this process was superseded by a newer session,
    4 if the pre-finalize wait timed out (own sig landed but counterparty
    didn't sign within the window).
    """
    # Typing covers the gap between "Almost done — sign here" and
    # "Signed ✓" or the eventual PDF generation. Follows the visible
    # venue — status cards go there, so the typing indicator belongs there.
    ui_target = group_chat_id or chat_id
    if typing_factory is None:
        typing = TypingLoop(chat_id=ui_target, bot_token=get_bot_token())
    else:
        typing = typing_factory(ui_target)
    typing.start()

    try:
        approved = poll_fn(
            pending_id=pending_id,
            sshsign_host=sshsign_host,
            timeout=timeout,
            interval=poll_interval,
        )
        if not approved:
            if not is_active_fn(output_dir):
                return 3
            sender(chat_id, message=(
                "Signature not received after waiting.\n"
                'When you sign, reply "signed" and I\'ll verify manually.'
            ))
            return 1

        if not is_active_fn(output_dir):
            return 3

        # Confirm signature receipt immediately, then let the user know the
        # PDF is coming. Finalize (upstream pdf generation) takes a few
        # seconds; posting "Generating executed file\u2026" fills that gap.
        sender(ui_target, message="\u2705 Confirmed signature.")  # ✅
        _mark_signed(output_dir)

        # P8-3: both-signed gate. Without it, the founder's OC runs
        # finalize the moment its own sig is approved — producing a
        # partial PDF with only the founder's signature. Later, the
        # investor's own finalize produces a second (both-signed) PDF.
        # Two PDFs land in the group. With this gate, the creator waits
        # for the session to aggregate `complete` (all pendings
        # approved), then produces the executed PDF on the first try.
        if pre_finalize_wait_fn is not None:
            sender(
                ui_target,
                message="\u23f3 Waiting for counterparty to sign\u2026",  # ⏳
            )
            if not pre_finalize_wait_fn():
                if not is_active_fn(output_dir):
                    return 3
                sender(ui_target, message=(
                    "Your signature is on file, but your counterparty "
                    "hasn't signed yet. The executed PDF will land here "
                    "once both signatures are in."
                ))
                return 4
            if not is_active_fn(output_dir):
                return 3

        sender(ui_target, message="\U0001f4c4 Generating executed file\u2026")  # 📄

        pdf_path = finalize_fn(output_dir, pending_id, sshsign_host)
        if not pdf_path:
            if not is_active_fn(output_dir):
                return 3
            sender(ui_target, message=(
                "Signature received but I couldn't generate the executed PDF. "
                "Check the negotiation output directory on the server."
            ))
            return 2

        if not is_active_fn(output_dir):
            return 3

        # PDF is the final artifact; post to the visible venue AND the
        # DM for archival. When no group is bound the two targets collapse
        # to one — guard against double-posting.
        sender(ui_target, media_path=str(pdf_path))
        if group_chat_id and str(group_chat_id) != str(chat_id):
            sender(chat_id, media_path=str(pdf_path))
        mark_executed_delivered(output_dir)
        return 0
    finally:
        typing.stop()


def _creator_await_sign_and_finalize(
    output_dir: Path,
    chat_id: str,
    sshsign_host: str,
    pending_id: str,
    session_id: str,
    timeout: int = 900,
    poll_interval: int = 5,
    sender=send_telegram,
    poll_fn=_poll_envelope_approval,
    finalize_fn=_finalize_executed_pdf,
    is_active_fn=_is_still_active_session,
    session_client=None,
    typing_factory=None,
    group_chat_id: str | None = None,
    session_complete_fn=_poll_session_complete,
) -> int:
    """Creator-finalizes flow. Same as the demo path, plus a trailing
    `complete-session` call that unblocks the non-creator's poll loop.

    group_chat_id, when set, forwards to _await_sign_and_push so status
    cards + PDF double-post into the bound Telegram group.

    P8-3: gates finalize on the session aggregating to 'complete' (all
    pendings approved) rather than firing on just the creator's own sig.
    Without the gate, creator-runs-finalize-first produced a partial PDF
    with only the founder's signature; later the joiner's own finalize
    produced a second (both-signed) PDF; both got posted to the group.
    The gate pushes both PDFs into one.

    Returns 0 on success (PDF pushed + session marked complete), non-zero
    for partial failures. A failed complete-session is NOT treated as
    fatal — the PDF already reached the user; J7 adds retry + manual
    fallback.
    """
    # P8-3: build the both-signed gate. The creator is the one who
    # ships the finalized PDF, so they need to wait for the joiner's
    # sig before generating the executed file. The joiner waits for
    # complete-session (which creator calls below) in its own flow;
    # no gate needed on that side.
    def _wait_for_both_signed() -> bool:
        if not session_id:
            return True
        return session_complete_fn(
            session_id=session_id,
            sshsign_host=sshsign_host,
            timeout=timeout,
            interval=poll_interval,
        )

    client = session_client or SshsignSession(host=sshsign_host)
    finalize_lease: dict | None = None

    def _leased_finalize(path: Path, pid: str, host: str):
        nonlocal finalize_lease
        if session_id and finalize_lease is None:
            finalize_lease = _acquire_workflow_lease(
                client,
                output_dir=path,
                session_id=session_id,
                role="creator",
                action="finalize",
                ttl_seconds=300,
            )
            if finalize_lease is None:
                return None
        return finalize_fn(path, pid, host)

    rc = _await_sign_and_push(
        output_dir=output_dir,
        chat_id=chat_id,
        sshsign_host=sshsign_host,
        pending_id=pending_id,
        timeout=timeout,
        poll_interval=poll_interval,
        sender=sender,
        poll_fn=poll_fn,
        finalize_fn=_leased_finalize,
        is_active_fn=is_active_fn,
        typing_factory=typing_factory,
        group_chat_id=group_chat_id,
        pre_finalize_wait_fn=_wait_for_both_signed,
    )
    if rc != 0 or not session_id:
        _release_workflow_lease(client, finalize_lease)
        return rc

    # Locate the executed PDF so we can cite a stable URI back to the
    # non-creator. We also embed our own pending_id in the URI so the
    # joiner can reconstruct the PDF locally (upstream's finalize needs
    # a pending file for each role, and the joiner has only its own).
    creator_role = ""
    try:
        mint = json.loads((output_dir / "mint.json").read_text())
        creator_role = mint.get("user_role", "")
        neg_id = mint.get("negotiation_id", "")
        neg_dir = Path(mint["founder_config_path"]).parent
        # Upstream writes the executed PDF as "<neg_id>_executed.pdf"
        # (NOT "<session_id>_executed.pdf") — session_id is the prefixed
        # form we use for sshsign session APIs, not for file layout.
        pdf_path = neg_dir / "output" / f"{neg_id}_executed.pdf"
    except (OSError, json.JSONDecodeError, KeyError):
        pdf_path = output_dir / "executed.pdf"

    try:
        if finalize_lease and not _check_workflow_lease(client, finalize_lease):
            return 3
        client.complete_session(
            session_id=session_id,
            executed_artifact=_build_artifact_uri(
                session_id, pdf_path,
                creator_pending_id=pending_id,
                creator_role=creator_role,
            ),
            lease_holder=finalize_lease["holder"] if finalize_lease else None,
            lease_generation=int(finalize_lease["generation"]) if finalize_lease else None,
        )
    except SshsignSessionError as e:
        sys.stderr.write(f"complete-session failed (non-fatal): {e}\n")
    finally:
        _release_workflow_lease(client, finalize_lease)
    return 0


def _creator_reconcile_finalization(
    *,
    output_dir: Path,
    chat_id: str,
    sshsign_host: str,
    session_id: str,
    group_chat_id: str | None = None,
    sender=send_telegram,
    session_status_fn=None,
    finalize_fn=None,
    session_client=None,
) -> int:
    """Retry creator-side finalization once sshsign says both signatures exist.

    This is the cron-safe recovery path for the common timing hole:
    creator signs first, waits for the counterparty, times out, and exits;
    later the counterparty signs. At that point no stream should be spawned
    again, but the creator can still finalize and call complete-session from
    its local mint/config files.

    Returns:
      0 delivered (or already delivered)
      1 not ready to finalize
      2 finalize failed
      3 complete-session failed after delivery (artifact still reached chat)
    """
    if has_executed_delivered(output_dir):
        return 0

    pending_id = latest_signing_pending_id(output_dir)
    if not pending_id:
        return 1

    if session_status_fn is None:
        session_status_fn = _ssh_session_status
    status = session_status_fn(session_id, sshsign_host)
    if status != "complete":
        return 1

    if finalize_fn is None:
        finalize_fn = _finalize_executed_pdf
    client = session_client or SshsignSession(host=sshsign_host)
    lease = _acquire_workflow_lease(
        client,
        output_dir=output_dir,
        session_id=session_id,
        role="creator",
        action="finalize",
        ttl_seconds=300,
    )
    if lease is None:
        return 1

    ui_target = group_chat_id or chat_id
    sender(ui_target, message="\U0001f4c4 Generating executed file\u2026")  # 📄
    try:
        pdf_path = finalize_fn(output_dir, pending_id, sshsign_host)
        if not pdf_path:
            sender(ui_target, message=(
                "Both signatures are on file, but I couldn't generate the "
                "executed PDF. Check the negotiation output directory on the server."
            ))
            return 2

        sender(ui_target, media_path=str(pdf_path))
        if group_chat_id and str(group_chat_id) != str(chat_id):
            sender(chat_id, media_path=str(pdf_path))
        mark_executed_delivered(output_dir)

        creator_role = ""
        try:
            mint = json.loads((output_dir / "mint.json").read_text())
            creator_role = mint.get("user_role", "")
        except (OSError, json.JSONDecodeError):
            pass

        if not _check_workflow_lease(client, lease):
            return 3
        client.complete_session(
            session_id=session_id,
            executed_artifact=_build_artifact_uri(
                session_id,
                Path(pdf_path),
                creator_pending_id=pending_id,
                creator_role=creator_role,
            ),
            lease_holder=lease["holder"],
            lease_generation=int(lease["generation"]),
        )
    except SshsignSessionError as e:
        sys.stderr.write(f"reconcile complete-session failed: {e}\n")
        return 3
    finally:
        _release_workflow_lease(client, lease)
    return 0


def _joiner_await_sign_and_finalize(
    output_dir: Path,
    chat_id: str,
    sshsign_host: str,
    pending_id: str,
    session_id: str,
    timeout: int = 900,
    poll_interval: int = 5,
    completion_poll_interval: int = 10,
    completion_timeout: int = 900,
    sender=send_telegram,
    poll_fn=_poll_envelope_approval,
    finalize_fn=_finalize_executed_pdf,
    is_active_fn=_is_still_active_session,
    session_client=None,
    sleep_fn=None,
    now_fn=None,
    typing_factory=None,
    group_chat_id: str | None = None,
) -> int:
    """Joiner-finalizes flow. The investor signs their own envelope, then
    waits for the creator to finalize (status=completed) before running
    their own finalize — that way both sides' signatures are present.

    Why wait: finalization pulls signatures from sshsign. If the
    investor finalizes before the founder has signed, the output PDF
    only has the investor's signature. Waiting for status=completed
    signals the founder is done and we can safely reproduce the PDF.

    Returns 0 if the investor received the executed PDF, non-zero on
    timeout or finalize failure.
    """
    if sleep_fn is None:
        import time as _time
        sleep_fn = _time.sleep
    if now_fn is None:
        import time as _time
        now_fn = _time.time

    # Typing indicator spans the whole wait — between clicking sign and
    # the PDF landing. Follows the visible venue (group if bound).
    ui_target = group_chat_id or chat_id
    if typing_factory is None:
        typing = TypingLoop(chat_id=ui_target, bot_token=get_bot_token())
    else:
        typing = typing_factory(ui_target)
    typing.start()

    try:
        approved = poll_fn(
            pending_id=pending_id,
            sshsign_host=sshsign_host,
            timeout=timeout,
            interval=poll_interval,
        )
        if not approved:
            if not is_active_fn(output_dir):
                return 3
            sender(chat_id, message=(
                "Signature not received after waiting.\n"
                'When you sign, reply "signed" and I\'ll verify manually.'
            ))
            return 1

        if not is_active_fn(output_dir):
            return 3

        sender(ui_target, message="\u2705 Confirmed signature.")  # ✅
        _mark_signed(output_dir)
        sender(ui_target, message=(
            "\u23f3 Waiting for your counterparty to sign\u2026"  # ⏳
        ))

        # Poll the session until the founder finalizes.
        client = session_client or SshsignSession(host=sshsign_host)
        start = now_fn()
        while True:
            elapsed = now_fn() - start
            if elapsed > completion_timeout:
                if not is_active_fn(output_dir):
                    return 3
                sender(ui_target, message=(
                    "\u26a0\ufe0f Counterparty didn't finalize in time. "  # ⚠
                    "Check sshsign.dev/audit/" + session_id
                    + " for the latest session status. The executed PDF "
                    "will be available there once both sides complete."
                ))
                return 1
            try:
                sess = client.get_session(session_id=session_id)
            except SshsignSessionError as e:
                sys.stderr.write(f"get-session while waiting completion: {e}\n")
                sleep_fn(completion_poll_interval)
                continue
            status = (sess.get("status") or "").lower()
            if status == "completed":
                # Write the creator's pending_id locally so upstream's
                # finalize can find both envelopes (upstream's
                # _collect_all_signatures reads <neg>/output/
                # <neg>_<role>_pending.txt for each role; we only have
                # our own — extract the creator's from the session's
                # executed_artifact URI).
                artifact_uri = sess.get("executed_artifact") or ""
                creator_pid, creator_role = _parse_artifact_uri(artifact_uri)
                if creator_pid and creator_role:
                    _write_counterparty_pending(
                        output_dir, session_id, creator_role, creator_pid,
                    )
                break
            if status == "expired":
                body = format_event({"type": "session_expired"})
                if body:
                    sender(ui_target, message=body)
                return 2
            if status == "rescinded_after_sign":
                body = format_event({
                    "type": "rescinded_after_sign_observer",
                    "by": "Your counterparty",
                })
                if body:
                    sender(ui_target, message=body)
                return 2
            if status == "canceled":
                body = format_event({
                    "type": "canceled_after_deal_observer",
                    "by": "Your counterparty",
                })
                if body:
                    sender(ui_target, message=body)
                return 2
            sleep_fn(completion_poll_interval)

        if not is_active_fn(output_dir):
            return 3

        sender(ui_target, message="\U0001f4c4 Generating executed file\u2026")  # 📄
        pdf_path = finalize_fn(output_dir, pending_id, sshsign_host)
        if not pdf_path:
            if not is_active_fn(output_dir):
                return 3
            sender(ui_target, message=(
                "Signature received but I couldn't generate the executed PDF. "
                "Check the session on sshsign.dev for the shared artifact."
            ))
            return 2

        if not is_active_fn(output_dir):
            return 3

        # Final artifact: post to the visible venue AND the DM for archival.
        sender(ui_target, media_path=str(pdf_path))
        if group_chat_id and str(group_chat_id) != str(chat_id):
            sender(chat_id, media_path=str(pdf_path))
        mark_executed_delivered(output_dir)
        return 0
    finally:
        typing.stop()


def run_negotiate(output_dir: str, chat_id_flag: str | None = None) -> int:
    """Full negotiate flow: mint tokens then stream the negotiation to chat."""
    out = Path(output_dir)
    write_trace(out, "negotiate.start", phase="negotiate")
    config_path = out / "config.json"
    if not config_path.exists():
        sys.stderr.write(f"No config.json in {output_dir}. Run 'prepare' first.\n")
        write_trace(out, "negotiate.failed", phase="negotiate", reason="missing_config")
        return 2

    config = json.loads(config_path.read_text())

    # Claim this output dir for this process. Any prior process still polling
    # an envelope on behalf of a previous negotiation will see a PID mismatch
    # on its next `_is_still_active_session` check and exit silently.
    try:
        (out / ".session.pid").write_text(str(os.getpid()))
    except OSError:
        pass

    # Push an interstitial so the user knows we're alive during the slow
    # mint step. run_mint does: mint founder/investor authorizations,
    # create signing keys, and register the sshsign session. That's several calls totaling
    # 15-30s; without this the chat sits silent between "🚀 Starting
    # negotiation" and the authorization card.
    chat_id = resolve_chat_id(chat_id_flag)
    if chat_id:
        send_telegram(chat_id, message=(
            "\U0001f510 Setting up your secure session\u2026"  # 🔐
        ))

    # In a Telegram DM, chat_id == user_id (positive int). Thread it through
    # run_mint → _register_signing_session so the founder's user_id gets
    # stashed on the sshsign session's metadata_member for Phase 8 /bind ACL.
    # Positive-only: group chat_ids are negative; we don't want a group id
    # here even if the skill were somehow invoked from a group.
    tg_user_id: int | None = None
    if chat_id:
        try:
            cid_raw = str(chat_id)
            if ":" in cid_raw:
                cid_raw = cid_raw.rsplit(":", 1)[-1]
            cid = int(cid_raw)
            if cid > 0:
                tg_user_id = cid
        except ValueError:
            tg_user_id = None

    if chat_id:
        # run_mint emits a JSON event for non-chat CLI callers. In the
        # Telegram skill path we already push the user-visible cards
        # directly, so keep stdout quiet; otherwise OpenClaw may relay the
        # JSON as a duplicate plain-text authorization card.
        with contextlib.redirect_stdout(io.StringIO()):
            rc = run_mint(output_dir, config, telegram_user_id=tg_user_id)
    else:
        rc = run_mint(output_dir, config, telegram_user_id=tg_user_id)
    if rc != 0:
        write_trace(out, "negotiate.failed", phase="negotiate", reason="mint_failed", returncode=rc, chat_id=chat_id)
        return rc

    if not chat_id:
        sys.stderr.write(
            "No chat_id: pass --chat-id or ensure /root/.openclaw/agents/main/sessions/sessions.json has a telegram:direct entry.\n"
        )
        write_trace(out, "negotiate.failed", phase="negotiate", reason="missing_chat_id")
        return 2

    # Authorization card — first surfacing of APOA after mint. Fires once,
    # before the founder-two-party wait or the first round. User sees their
    # bounds spelled out in plain English so the later "agent tried X,
    # rejected" event has context.
    ttl_seconds = int(os.environ.get("NEGOTIATION_TTL", "3600"))
    auth_body = format_event({
        "type": "authorized",
        "constraints": config.get("constraints") or {},
        "ttl_hours": max(1, ttl_seconds // 3600),
    })
    if auth_body:
        send_telegram(chat_id, message=auth_body)

    # Two-party mode: the founder waits for the investor to join; the
    # investor (who just joined) goes straight to streaming. Demo mode
    # skips both paths.
    try:
        mint = json.loads((out / "mint.json").read_text())
    except (OSError, json.JSONDecodeError):
        mint = {}
    if mint.get("mode") == "two_party":
        if mint.get("user_role") == "founder":
            # Path 1 (post-mortem of INV-GD4KZ on 2026-04-27): the founder
            # mint must NOT keep the foreground process alive waiting for
            # the investor to join. The OC reaper kills it after a few
            # minutes anyway, and any `_stream_to_telegram` it spawns will
            # write Round 0 to sshsign — leaving upstream's stateful
            # negotiation half-bootstrapped. When the cron-driven Phase B
            # later spawns a SECOND `_stream_to_telegram` after /bind,
            # that fresh `run_negotiation` can't reconcile with the
            # already-written Round 0 and the negotiation hangs at
            # round 1 (only the investor's response makes it through).
            #
            # Fix: post the invitation card and EXIT. The cron scan
            # (Phase A) handles the create-group card once the investor
            # joins; `/bind` triggers the SOLE `_stream_to_telegram`
            # invocation via `_run_founder_resume` Phase B.
            invite_rc = _founder_post_invitation_card(
                chat_id=chat_id,
                mint=mint,
                constraints=config.get("constraints") or {},
            )
            if invite_rc != 0:
                write_trace(out, "negotiate.failed", phase="negotiate", reason="invitation_failed", returncode=invite_rc, chat_id=chat_id)
                return invite_rc
            _founder_wait_for_join_and_prompt_group(
                output_dir=out,
                mint=mint,
                chat_id=chat_id,
                sender=send_telegram,
            )
            write_trace(out, "negotiate.waiting", phase="waiting_for_counterparty", role="founder", chat_id=chat_id, session_code=mint.get("session_code"))
            return 0
        elif mint.get("user_role") == "investor":
            # Symmetric Path 1 (post-mortem of INV-T6869 on 2026-04-27):
            # the investor's foreground used to call
            # `_investor_wait_for_founder_streaming` with a 180s cap.
            # In Path 1 the founder takes minutes-to-hours to create
            # the group + /bind, so 180s is hopelessly too short - the
            # investor's process exited (rc=4) long before the founder
            # set `founder_streaming_at`. Result: founder later spawned
            # its stream and waited forever for the investor's offer.
            #
            # Fix: post the "joined; waiting" cards and EXIT. Cron's
            # scan iterates the investor pointer the same way it
            # iterates founder pointers; `_run_investor_resume` fires
            # when sshsign reports the founder's streaming_at is set.
            sender = send_telegram
            sender(chat_id, message="\u2705 Joined the negotiation.")
            wait_body = format_event({"type": "investor_waiting_for_founder"})
            if wait_body:
                sender(chat_id, message=wait_body)
            state = state_store.read_state(mint.get("negotiation_id") or "")
            if state:
                orchestrator.reconcile_state(state, sender=sender)
            write_trace(out, "negotiate.waiting", phase="waiting_for_founder", role="investor", chat_id=chat_id, session_code=mint.get("session_code"))
            return 0
    else:
        # Demo (solo) mode: push the "starting" card directly from the
        # script now that SKILL.md tells the model not to emit its own
        # preamble. This ensures the order is always
        #   🔐 setup → 🔒 auth → 🚀 starting → rounds
        # matching the two-party flow's
        #   🔐 setup → 🔒 auth → 🤝 invite | ✅ joined → rounds
        send_telegram(chat_id, message="\U0001f680 Starting negotiation\u2026")  # 🚀

    # Past this point we're on the DEMO mode path. Two-party founder
    # returned at line ~2190 (after posting invitation card); two-party
    # investor returned at line ~2213 (after posting joined+waiting
    # cards). Both two-party stream invocations now live exclusively
    # in `_run_founder_resume` Phase B and `_run_investor_resume`,
    # both driven by cron. Eliminating the in-process foreground
    # stream prevents the OC reaper / double-spawn class of bugs that
    # broke INV-GD4KZ and INV-T6869.
    sshsign_host = os.environ.get("SSHSIGN_HOST", "sshsign.dev")
    group_chat_id: str | None = None
    bot_username = os.environ.get("TELEGRAM_BOT_USERNAME", "AgenticPOA_bot")
    # Demo (single-party) doesn't need the sshsign history poller —
    # upstream's `run_local` emits round events on stdout directly.
    history_neg_id = None
    stream_rc, signing_event = _stream_to_telegram(
        output_dir=out,
        chat_id=chat_id,
        constraints=config.get("constraints"),
        bot_username=bot_username,
        group_chat_id=group_chat_id,
        negotiation_id=history_neg_id,
        sshsign_host=sshsign_host,
    )
    if stream_rc != 0 or not signing_event:
        write_trace(out, "negotiate.stream_finished", phase="negotiate", returncode=stream_rc, signing_event=bool(signing_event), chat_id=chat_id)
        return stream_rc

    pending_id = signing_event.get("pending_id") or ""
    if not pending_id:
        write_trace(out, "negotiate.completed_without_pending", phase="negotiate", chat_id=chat_id)
        return 0

    # Demo mode: single-party finalize.
    rc = _await_sign_and_push(
        output_dir=out,
        chat_id=chat_id,
        sshsign_host=sshsign_host,
        pending_id=pending_id,
    )
    write_trace(out, "negotiate.completed", phase="completed", returncode=rc, pending_id=pending_id, chat_id=chat_id)
    return rc


def _fetch_session_for_join(
    session_code: str,
    session_client=None,
) -> tuple[dict | None, str | None]:
    """Call sshsign get-session to validate a join-code and pull founder's
    APOA pubkey + member metadata.

    Returns (session_payload, error_message). Exactly one is non-None.
    """
    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )
    try:
        sess = client.get_session(session_code=session_code)
    except SessionNotFoundError:
        return None, (
            "That code doesn't match a current negotiation. "
            "Double-check the code with your counterparty — "
            "it should look like INV-XXXXX."
        )
    except SessionExpiredError:
        return None, (
            "That negotiation expired. Ask your counterparty for a new code."
        )
    except SshsignSessionError as e:
        return None, f"Couldn't look up session: {e}"

    status = (sess.get("status") or "").lower()
    if status in ("canceled", "rescinded_after_sign"):
        return None, "That negotiation was canceled. Ask your counterparty for a new code."
    if status == "expired":
        return None, "That negotiation expired. Ask your counterparty for a new code."
    if status == "completed":
        return None, "That negotiation has already completed."
    if status == "joined":
        # Counterparty role already has a member. We'd be a third wheel —
        # sshsign will reject join-session anyway, but this lets us surface
        # a clearer message before minting wasted tokens.
        return None, (
            "That negotiation has already started with someone else. "
            "Ask your counterparty if they meant to share a different code."
        )
    if status != "open":
        return None, f"Can't join a session in state: {status}"

    # status=open — session is joinable. (We used to accept joined here and
    # defer role-conflict detection to join-session; now the joined branch
    # above short-circuits with a clearer error.)
    return sess, None


def _enrich_constraints_from_session(
    constraints: dict,
    session_payload: dict,
) -> dict:
    """Merge founder-side metadata from the session into the investor's
    parsed constraints. Investor-supplied fields always win — the merge
    only fills gaps.

    Reads from metadata_public always (company_name lives there so
    non-members can see it on the confirm card). Reads from metadata_member
    if the caller is a session member (founder-side view, or investor
    after join-session).
    """
    out = dict(constraints)

    def _parse(raw):
        if raw is None:
            return {}
        if isinstance(raw, dict):
            return raw
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    public_md = _parse(session_payload.get("metadata_public"))
    member_md = _parse(session_payload.get("metadata_member"))

    for key in ("company_name", "founder_name", "founder_title",
                "investor_name", "investor_firm"):
        if out.get(key):
            continue
        if public_md.get(key):
            out[key] = public_md[key]
        elif member_md.get(key):
            out[key] = member_md[key]
    return out


def _founder_post_invitation_card(
    chat_id: str,
    mint: dict,
    constraints: dict,
    sender=send_telegram,
) -> int:
    """Post the invitation card to the founder's DM and return immediately.

    Path 1 replacement for `_founder_two_party_gate`'s blocking wait.
    The founder's mint flow used to BLOCK here waiting for the
    investor to join (via `_wait_for_counterparty`). That foreground
    wait is what the OC reaper killed; worse, on detect-join it would
    spawn `_stream_to_telegram` → upstream's `run_negotiation` →
    Round 0 written to sshsign. When the cron-driven Phase B later
    re-spawned the stream after /bind, upstream couldn't reconcile
    with that pre-written Round 0 and the negotiation deadlocked.

    Now: just push the invitation card and exit. Cron's scan / Phase
    A handle the rest of the founder-side state machine, and the
    `_stream_to_telegram` call lives ONLY in `_run_founder_resume`'s
    Phase B (post-/bind), so upstream is spawned exactly once.

    rc=0    → invitation posted (or skipped silently if missing data);
              the caller should return 0 from run_negotiate.
    rc=3    → missing session_code or negotiation_id; the data needed
              to assemble the card is missing.
    """
    session_code = mint.get("session_code")
    session_id = _sshsign_session_id(mint.get("negotiation_id") or "")
    if not session_code or not session_id:
        sender(chat_id, message=(
            "⚠️ Internal error: two-party session was not registered. "  # ⚠️
            "Try again."
        ))
        return 3

    investor_name = constraints.get("investor_name")
    investor_firm = constraints.get("investor_firm")
    if investor_name and investor_firm:
        counterparty_label = f"{investor_name} at {investor_firm}"
    else:
        counterparty_label = investor_name or investor_firm or "your counterparty"

    invitation_body = format_event({
        "type": "invitation",
        "session_code": session_code,
        "founder_bot_handle": (os.environ.get("TELEGRAM_BOT_USERNAME") or "").strip(),
        "expires_at": mint.get("session_expires_at") or "",
        "ttl_hours": 24,
        "counterparty_label": counterparty_label,
        "investor_name": investor_name or "",
        "investor_firm": investor_firm or "",
    })
    if invitation_body:
        sender(chat_id, message=invitation_body)
    return 0


def _founder_wait_for_join_and_prompt_group(
    output_dir: Path,
    mint: dict,
    chat_id: str,
    sender=send_telegram,
    session_client=None,
    sleep_fn=None,
    now_fn=None,
) -> int:
    """Inline Phase A fallback for founder launches.

    Cron remains the durable recovery path, but the demo should not rely
    on a later system-event tick to tell the founder what to do after the
    investor joins. This helper waits briefly after the invite is posted;
    when sshsign reports `joined`, it re-enters the normal founder resume
    path, which posts the group setup/bind card and then exits before any
    negotiation stream is spawned.
    """
    import time

    negotiation_id = mint.get("negotiation_id") or ""
    if not negotiation_id:
        return 0

    state = state_store.read_state(negotiation_id)
    if not state or (state.get("role") or "founder") != "founder":
        return 0

    try:
        max_wait = int(os.environ.get("CLAW_NEGOTIATE_FOUNDER_JOIN_WAIT", "1800"))
    except ValueError:
        max_wait = 1800
    if max_wait <= 0:
        return 0

    if sleep_fn is None:
        sleep_fn = time.sleep
    if now_fn is None:
        now_fn = time.time
    try:
        poll_interval = max(
            1,
            int(os.environ.get("CLAW_NEGOTIATE_FOUNDER_JOIN_POLL", "5")),
        )
    except ValueError:
        poll_interval = 5

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )
    session_id = _sshsign_session_id(negotiation_id)
    deadline = now_fn() + max_wait

    while now_fn() < deadline:
        try:
            sess = client.get_session(session_id=session_id)
        except SshsignSessionError as e:
            sys.stderr.write(f"founder inline wait: get-session failed: {e}\n")
            return 0

        status = normalize_status(sess.get("status"))
        if status == "joined":
            write_trace(
                output_dir,
                "founder.inline_join_detected",
                phase="waiting_for_group_bind",
                negotiation_id=negotiation_id,
                session_id=session_id,
                chat_id=chat_id,
            )
            _run_founder_resume(
                state,
                session_client=client,
                sender=sender,
                now_fn=now_fn,
            )
            return 0
        if is_terminal_status(status):
            state_store.delete_state(negotiation_id)
            return 0

        sleep_fn(poll_interval)

    write_trace(
        output_dir,
        "founder.inline_join_wait_timeout",
        phase="waiting_for_counterparty",
        negotiation_id=negotiation_id,
        session_id=session_id,
        chat_id=chat_id,
    )
    return 0


def _founder_two_party_gate(
    out: Path,
    chat_id: str,
    mint: dict,
    constraints: dict,
    sender=send_telegram,
    wait_fn=_wait_for_counterparty,
) -> int:
    """Push the invitation card, wait for the counterparty to join, and
    return 0 to proceed with streaming or a non-zero rc if the session
    ended before negotiation could begin.

    rc=0    → counterparty joined; caller should run the stream
    rc=1    → invitation expired; user notified
    rc=2    → session was canceled; user notified (or stays silent if we
              canceled ourselves; the parser owns that path in J5)
    rc=3    → missing session_code or persistent sshsign error
    """
    session_code = mint.get("session_code")
    session_id = _sshsign_session_id(mint.get("negotiation_id") or "")
    if not session_code or not session_id:
        sender(chat_id, message=(
            "\u26a0\ufe0f Internal error: two-party session was not registered. "  # ⚠️
            "Try again."
        ))
        return 3

    # Counterparty label for the card — prefer the user's own NL phrasing
    # (investor_name + firm) over a generic word.
    counterparty_label = (
        _counterparty_label_from_constraints(constraints) or "your counterparty"
    )

    invitation_body = format_event({
        "type": "invitation",
        "session_code": session_code,
        "founder_bot_handle": (os.environ.get("TELEGRAM_BOT_USERNAME") or "").strip(),
        "expires_at": mint.get("session_expires_at") or "",
        "ttl_hours": 24,
        "counterparty_label": counterparty_label,
        "investor_name": constraints.get("investor_name") or "",
        "investor_firm": constraints.get("investor_firm") or "",
    })
    if invitation_body:
        sender(chat_id, message=invitation_body)

    # Pre-join "create the live group" card was previously emitted here
    # with hardcoded counterparty bot handle — wrong assumption for
    # multi-operator deploys (we don't know the investor's bot until
    # they join). Removed. The post-join create-group card from
    # _run_founder_resume composes from real sshsign metadata once
    # both bot handles are known.

    status = wait_fn(
        session_id=session_id,
        session_code=session_code,
        chat_id=chat_id,
        counterparty_label=counterparty_label,
    )
    if status == "joined":
        return 0
    if status == "expired":
        body = format_event({"type": "invitation_expired"})
        if body:
            sender(chat_id, message=body)
        return 1
    if status == "canceled":
        # Cancel message content depends on who canceled — J5 owns the
        # user-facing copy. Keep this path silent for now; the stream
        # loop wouldn't run anyway.
        return 2
    # status == "error" or unknown
    sender(chat_id, message=(
        "\u26a0\ufe0f Lost connection to the signing service while waiting. "
        "Your session still exists; try the command again."
    ))
    return 3


CRON_JOB_NAME = "negotiate_safe-scan"
SYSTEM_CRON_MARKER = "# negotiate_safe-scan"
CRON_SCAN_DEFAULT_INTERVAL = "60s"
CRON_SCAN_MIN_EVERY_MS = 60_000


# P7-5 investor-side wait tuning. Exposed as module constants so tests
# can monkeypatch to fast values and ops can env-override for the
# post-Day-4 tuning pass.
INVESTOR_WAIT_POLL_INTERVAL = float(os.environ.get("CLAW_NEGOTIATE_WAIT_POLL", "3"))
INVESTOR_WAIT_HEARTBEAT_AT = float(os.environ.get("CLAW_NEGOTIATE_WAIT_HEARTBEAT", "15"))
INVESTOR_WAIT_TIMEOUT = float(os.environ.get("CLAW_NEGOTIATE_WAIT_TIMEOUT", "180"))


def _investor_wait_for_founder_streaming(
    session_id: str,
    group_chat_id: str | None,
    session_client=None,
    sender=send_telegram,
    typing_factory=None,
    sleep_fn=None,
    now_fn=None,
    investor_dm_chat_id: str | None = None,
    founder_bot_handle: str | None = None,
) -> str:
    """Bounded poll on founder_streaming_at (not founder_resumed_at).

    Invoked immediately after the investor's join completes, before
    ``_stream_to_telegram`` (because upstream's run_distributed will
    hang on the missing opening offer if the founder's agent hasn't
    resumed yet). Posts a waiting card, starts a typing indicator in
    the group, and polls the session row every 3s for up to 180s.

    Return values (all lowercase strings for easy grep):
      "streaming"     — founder_streaming_at set; caller proceeds to stream
      "timeout"       — 180s elapsed; caller returns without streaming
      "terminal"      — session canceled/rescinded/completed/expired mid-wait

    Cards emitted:
      waiting          → right after join (investor_waiting_for_founder)
      heartbeat        → at ~15s if still waiting (investor_waiting_heartbeat)
      both_online      → on streaming_at hit (investor_both_online)
      timeout          → on 180s cap (investor_wake_timeout)
      session_ended    → on terminal status (investor_session_ended)

    The returned value determines what the caller does next:
      streaming → call _stream_to_telegram
      timeout or terminal → return from run_negotiate without streaming
    """
    import time

    if sleep_fn is None:
        sleep_fn = time.sleep
    if now_fn is None:
        now_fn = time.time

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )

    # Path 1: cards land in the bound group when one exists; otherwise
    # the investor's own DM. The bound group may APPEAR mid-poll
    # (founder taps create-group + /bind in response to the create-
    # group card). Re-resolve the target each iteration so subsequent
    # cards (heartbeat, both-online) target whichever chat is current.
    target_chat = group_chat_id or investor_dm_chat_id or ""

    # Waiting card first — sets the expectation even if the poll
    # returns immediately (same tick the founder flipped streaming_at).
    body = format_event({
        "type": "investor_waiting_for_founder",
        "founder_bot_handle": (founder_bot_handle or "").strip(),
    })
    if body and target_chat:
        sender(target_chat, message=body)

    # Typing indicator in the same chat the cards land in. If the
    # group emerges mid-wait the indicator stays on the original
    # chat — minor visual gap, not worth restarting the loop.
    if typing_factory is None:
        typing = TypingLoop(chat_id=target_chat or "", bot_token=get_bot_token())
    else:
        typing = typing_factory(target_chat)
    typing.start()

    try:
        start = now_fn()
        heartbeat_sent = False
        # Add one extra iteration past the cap so we definitively
        # timeout rather than miss the final check by a hair.
        while True:
            elapsed = now_fn() - start
            if elapsed >= INVESTOR_WAIT_TIMEOUT:
                body = format_event({"type": "investor_wake_timeout"})
                if body and target_chat:
                    sender(target_chat, message=body)
                return "timeout"

            try:
                sess = client.get_session(session_id=session_id)
            except SshsignSessionError as e:
                # Transient: log and keep polling. A persistent error
                # will time out eventually and surface via the timeout
                # card. We don't want a network blip to abort the wait
                # given the founder's resume is the actual blocker.
                sys.stderr.write(f"wait-for-founder: get-session: {e}\n")
                sleep_fn(INVESTOR_WAIT_POLL_INTERVAL)
                continue

            # Path 1: detect group binding mid-poll. The founder's
            # /bind writes group_chat_id on the session row. Once it
            # appears, switch the active target chat so subsequent
            # cards (heartbeat, both-online) land in the group where
            # both parties can see them.
            sess_group_id = sess.get("group_chat_id")
            if sess_group_id:
                # Telegram group_chat_ids on the wire are negative
                # int64; sshsign stores as int. Normalize to str for
                # send_telegram which expects a string target.
                sess_group_str = str(sess_group_id)
                if sess_group_str != target_chat:
                    target_chat = sess_group_str

            status = normalize_status(sess.get("status"))
            if is_terminal_status(status):
                body = format_event({
                    "type": "investor_session_ended", "status": status,
                })
                if body and target_chat:
                    sender(target_chat, message=body)
                return "terminal"

            # Check founder's streaming_at. Members list is the
            # authoritative source; scan the founder row.
            streaming_at = None
            for m in (sess.get("members") or []):
                if (m.get("role") or "").lower() == "founder":
                    streaming_at = m.get("founder_streaming_at")
                    break
            if streaming_at:
                body = format_event({"type": "investor_both_online"})
                if body and target_chat:
                    sender(target_chat, message=body)
                return "streaming"

            if not heartbeat_sent and elapsed >= INVESTOR_WAIT_HEARTBEAT_AT:
                body = format_event({"type": "investor_waiting_heartbeat"})
                if body and target_chat:
                    sender(target_chat, message=body)
                heartbeat_sent = True

            sleep_fn(INVESTOR_WAIT_POLL_INTERVAL)
    finally:
        try:
            typing.stop()
        except Exception:
            pass


def _duration_ms(value: str | None) -> int | None:
    """Parse the small duration subset used for OpenClaw cron intervals."""
    if not value:
        return None
    text = str(value).strip().lower()
    m = re.fullmatch(r"(\d+)\s*(ms|s|m|h)?", text)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2) or "ms"
    if unit == "ms":
        return n
    if unit == "s":
        return n * 1000
    if unit == "m":
        return n * 60_000
    if unit == "h":
        return n * 3_600_000
    return None


def _job_every_ms(job: dict) -> int | None:
    schedule = job.get("schedule")
    if isinstance(schedule, dict):
        if schedule.get("kind") == "every":
            every = schedule.get("everyMs")
            return int(every) if isinstance(every, (int, float)) else None
        return None
    if isinstance(schedule, str):
        m = re.search(r"\bevery\s+(.+)$", schedule.strip(), re.IGNORECASE)
        if m:
            return _duration_ms(m.group(1))
    every = job.get("every") or job.get("everyMs")
    if isinstance(every, (int, float)):
        return int(every)
    if isinstance(every, str):
        return _duration_ms(every)
    return None


def ensure_cron(
    interval: str = "30s",
    runner: "callable | None" = None,
    system_runner: "callable | None" = None,
) -> tuple[bool, str | None]:
    """Install the ``negotiate_safe-scan`` cron job if absent.

    Invoked from the founder's mint path (``_register_signing_session``
    tail) so every fresh two-party session guarantees a running cron
    job on this droplet. Idempotent: if the job already exists, do
    nothing. Non-fatal on any failure — cron is a recovery mechanism,
    not a correctness gate, and the founder's current turn still
    works inline. Ops-visible errors go to stderr.

    Parameters
    ----------
    interval
        ``--every`` argument. Default ``30s``; the plan notes that
        OC may floor at ``60s`` and we re-tune during live dry-run.
    runner
        Injectable subprocess runner for tests; defaults to
        ``subprocess.run``.

    Returns
    -------
    (installed, error_message)
        ``installed`` is True if we called ``cron add`` (or True if
        the job already existed — both are "in place"). ``False``
        means an error prevented us from ensuring the job; error
        message is returned for caller-side logging.
    """
    prefer_system_cron = runner is None
    allow_system_fallback = runner is None or system_runner is not None
    if runner is None:
        runner = subprocess.run
    if system_runner is None:
        system_runner = runner

    def _fallback(reason: str) -> tuple[bool, str | None]:
        if not allow_system_fallback:
            return False, reason
        ok, fallback_err = _ensure_system_cron(runner=system_runner)
        if ok:
            return True, None
        return False, f"{reason}; system cron fallback failed: {fallback_err}"

    if prefer_system_cron:
        ok, err = _ensure_system_cron(runner=system_runner)
        if ok:
            return True, None
        # Fall through to OpenClaw cron only if the deterministic
        # code-level heartbeat cannot be installed on this host.

    # list + parse-json to detect the existing job.
    try:
        list_res = runner(
            ["openclaw", "cron", "list", "--json"],
            capture_output=True, text=True, timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return _fallback(f"openclaw cron list failed: {e}")

    if list_res.returncode != 0:
        # Pairing wall, unpaired gateway, etc. Log + continue; scan
        # can be installed manually by ops as a fallback.
        return _fallback(
            f"openclaw cron list rc={list_res.returncode}: "
            f"{(list_res.stderr or list_res.stdout or '').strip()[:200]}"
        )

    try:
        jobs = json.loads(list_res.stdout or "[]")
    except json.JSONDecodeError as e:
        return _fallback(f"openclaw cron list: invalid JSON: {e}")

    if isinstance(jobs, dict):
        # Some OC versions wrap the list under a top-level key.
        jobs = jobs.get("jobs") or jobs.get("items") or []

    for job in jobs or []:
        if isinstance(job, dict) and job.get("name") == CRON_JOB_NAME:
            # Already installed. Preserve operator tuning unless the
            # interval is below the floor we know can starve Telegram
            # turns: OpenClaw main-session system-event cron runs via
            # the main heartbeat/session, so scan jobs must not overlap.
            every_ms = _job_every_ms(job)
            job_id = str(job.get("id") or "").strip()
            target_ms = max(_duration_ms(interval) or CRON_SCAN_MIN_EVERY_MS, CRON_SCAN_MIN_EVERY_MS)
            if every_ms is not None and every_ms < CRON_SCAN_MIN_EVERY_MS and job_id:
                try:
                    edit_res = runner(
                        [
                            "openclaw", "cron", "edit", job_id,
                            "--every", f"{target_ms // 1000}s",
                        ],
                        capture_output=True, text=True, timeout=10,
                    )
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
                    return False, f"openclaw cron edit failed: {e}"
                if edit_res.returncode != 0:
                    return False, (
                        f"openclaw cron edit rc={edit_res.returncode}: "
                        f"{(edit_res.stderr or edit_res.stdout or '').strip()[:200]}"
                    )
            return True, None

    # Not installed — add it. Flag set discovered live (OC 2026.4.x):
    #   * `--exact` is rejected for `--every` schedules (it's a `--cron`
    #     stagger control, not an `--every` knob).
    #   * `--session isolated` requires `--message` (agentTurn). For our
    #     case a system event in main session is the right shape — A.5
    #     in SKILL.md routes "negotiate_safe_scan" to `run_safe.py scan`
    #     and the scan turn is short, so it doesn't disrupt active
    #     conversations meaningfully.
    #   * `--no-deliver` is only valid for non-main sessions; with main
    #     session we just don't pass it (the system event payload
    #     doesn't generate user-visible chatter on its own).
    add_argv = [
        "openclaw", "cron", "add",
        "--name", CRON_JOB_NAME,
        "--every", interval,
        "--system-event", "negotiate_safe_scan",
        "--keep-after-run",
    ]
    try:
        add_res = runner(add_argv, capture_output=True, text=True, timeout=10)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return _fallback(f"openclaw cron add failed: {e}")

    if add_res.returncode != 0:
        return _fallback(
            f"openclaw cron add rc={add_res.returncode}: "
            f"{(add_res.stderr or add_res.stdout or '').strip()[:200]}"
        )
    return True, None


def _ensure_system_cron(runner=subprocess.run) -> tuple[bool, str | None]:
    """Install a portable OS-cron scan heartbeat when OpenClaw cron is unavailable."""
    skill_dir = Path(__file__).resolve().parent
    python_bin = sys.executable or "python3"
    cron_line = (
        f"* * * * * cd {skill_dir} && {python_bin} run_safe.py scan "
        f">> /tmp/negotiate_safe_scan.log 2>&1 {SYSTEM_CRON_MARKER}"
    )
    try:
        list_res = runner(["crontab", "-l"], capture_output=True, text=True, timeout=10)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return False, f"crontab -l failed: {e}"
    current = list_res.stdout if list_res.returncode == 0 else ""
    if SYSTEM_CRON_MARKER in current:
        return True, None
    new_cron = (current.rstrip() + "\n" if current.strip() else "") + cron_line + "\n"
    try:
        add_res = runner(
            ["crontab", "-"],
            input=new_cron,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return False, f"crontab install failed: {e}"
    if add_res.returncode != 0:
        return False, (add_res.stderr or add_res.stdout or f"exit {add_res.returncode}").strip()
    return True, None


def _hydrate_scan_env_from_openclaw_config() -> None:
    """Let OS cron run the skill without hand-maintained env files."""
    cfg_path = Path("/root/.openclaw/openclaw.json")
    try:
        cfg = json.loads(cfg_path.read_text())
    except (OSError, json.JSONDecodeError):
        return
    env = (
        cfg.get("skills", {})
        .get("entries", {})
        .get("negotiate_safe", {})
        .get("env", {})
    )
    if not isinstance(env, dict):
        return
    for key, value in env.items():
        if isinstance(key, str) and isinstance(value, str):
            os.environ.setdefault(key, value)


def _run_founder_resume(
    state: dict,
    sshsign_host: str | None = None,
    session_client=None,
    sender=send_telegram,
    now_fn=None,
) -> int:
    """P7-5 shared resume path.

    Called from two sites:
      * ``run_bind`` when the investor has ALREADY joined before the
        founder pasted ``/bind`` (fast path: founder is live in the
        bind turn; resume inline).
      * ``run_scan`` when an OpenClaw cron tick finds a waiting session
        that has advanced to ``joined`` but hasn't yet started streaming
        (slow path: founder's original process was reaped; wake fresh).

    Idempotency: if ``founder_resumed_at`` is already non-null on the
    sshsign session, exit without re-streaming. A concurrent scan tick
    or a bind racing with a scan can legitimately fire twice; the
    sshsign row is the single coordination point.

    State cleanup: on terminal session status, delete the local state
    pointer so the next scan doesn't keep poking a dead session.

    Return codes:
      0  resume completed (or cleanly no-op'd)
      1  resume not yet ready (status != joined; caller tries again later)
      2  terminal session — cleaned up; do not retry
      3  sshsign transport error
    """
    import time
    if now_fn is None:
        now_fn = time.time

    negotiation_id = state.get("negotiation_id") or ""
    output_dir_raw = state.get("output_dir") or ""
    if not negotiation_id or not output_dir_raw:
        sys.stderr.write(
            "resume: state missing negotiation_id or output_dir; skipping\n"
        )
        return 2

    out = Path(output_dir_raw)
    if not out.exists():
        # Output_dir was wiped (e.g., /tmp cleaned) — nothing to resume.
        # Drop the pointer so future scans don't keep re-reading it.
        sys.stderr.write(
            f"resume: output_dir {out} missing; cleaning state pointer\n"
        )
        state_store.delete_state(negotiation_id)
        return 2
    if not _state_matches_output_dir(negotiation_id, out):
        sys.stderr.write(
            f"resume: state {negotiation_id} no longer owns {out}; "
            "cleaning stale pointer\n"
        )
        state_store.delete_state(negotiation_id)
        return 2
    write_trace(out, "resume.founder.start", phase="resume", role="founder", negotiation_id=negotiation_id, session_code=state.get("session_code"))
    had_pid_file_before_resume = (out / ".session.pid").exists()
    had_live_stream_before_resume = _pid_file_has_live_negotiation(out)
    try:
        (out / ".session.pid").write_text(str(os.getpid()))
    except OSError:
        pass

    sshsign_host = sshsign_host or os.environ.get("SSHSIGN_HOST", "sshsign.dev")
    client = session_client or SshsignSession(host=sshsign_host)
    session_id = _sshsign_session_id(negotiation_id)

    try:
        sess = client.get_session(session_id=session_id)
    except SessionNotFoundError:
        # sshsign no longer knows this session. Local state is stale.
        state_store.delete_state(negotiation_id)
        return 2
    except SshsignSessionError as e:
        sys.stderr.write(f"resume: get-session failed: {e}\n")
        return 3

    status = normalize_status(sess.get("status"))
    if is_terminal_status(status):
        # Terminal. Drop the pointer; don't re-emit status cards (the
        # turn that terminated the session already sent the right one).
        sys.stderr.write(
            f"resume: session {session_id} is terminal ({status}); "
            f"cleaning state pointer\n"
        )
        state_store.delete_state(negotiation_id)
        return 2

    # If a previous founder stream was killed by the host timeout, sshsign
    # can still say founder_streaming_at is set even though no local stream is
    # alive. Clear the marker so this scan can safely restart the stream.
    if had_pid_file_before_resume and not had_live_stream_before_resume:
        for member in sess.get("members") or []:
            if (
                (member.get("role") or "").lower() == "founder"
                and member.get("founder_streaming_at")
            ):
                if _has_authoritative_offer_history(
                    negotiation_id, sshsign_host=sshsign_host,
                ):
                    write_trace(
                        out,
                        "resume.founder.stale_streaming_history_present",
                        phase="resume",
                        negotiation_id=negotiation_id,
                        session_id=session_id,
                    )
                    return 3
                try:
                    client.update_session_member(
                        session_id, field="founder_streaming_at", value=0,
                    )
                    member["founder_streaming_at"] = 0
                    write_trace(
                        out,
                        "resume.founder.cleared_stale_streaming",
                        phase="resume",
                        negotiation_id=negotiation_id,
                        session_id=session_id,
                    )
                except SshsignSessionError as e:
                    sys.stderr.write(
                        f"resume: clearing stale founder_streaming_at: {e}\n"
                    )
                break

    group_chat_id = _resolve_group_chat_id(session_id, session_client=client)
    founder_phase, founder_row = classify_founder_resume(
        sess,
        group_chat_id=group_chat_id,
    )
    if founder_phase == FOUNDER_WAIT_COUNTERPARTY:
        # Investor hasn't joined yet. Scan will try again on next tick.
        write_trace(out, "resume.founder.not_ready", phase="waiting_for_counterparty", negotiation_id=negotiation_id, session_id=session_id, status=status)
        return 1
    if founder_phase == FOUNDER_STALE_NO_MEMBER or founder_row is None:
        sys.stderr.write("resume: session has no founder member row; cleaning\n")
        state_store.delete_state(negotiation_id)
        return 2

    # Path 1 two-phase state machine. The dedup signal is
    # streaming_at (the "we're done with this resume" marker), NOT
    # resumed_at (which now means "phase A acknowledged the join,
    # waiting for the founder to /bind a group").
    #
    # State table for (resumed_at, streaming_at, group_chat_id):
    #   (null, null, null)       Phase A — post create-group card,
    #                            set resumed_at, exit. Wait for bind.
    #   (set,  null, null)       A-done — no-op (still waiting on bind,
    #                            card already posted on the prior tick).
    #   (any,  null, set)        Phase B — set resumed_at if null,
    #                            set streaming_at, run _stream_to_telegram.
    #                            Combined-pass: covers run_bind's
    #                            in-process fast path that hits us
    #                            after the founder pasted /bind directly
    #                            (group already bound, A never ran).
    #   (any,  set,  any)        Done — streaming has begun on a prior
    #                            pass; nothing more to do here.
    resumed_at = founder_row.get("founder_resumed_at")

    if founder_phase == FOUNDER_ALREADY_STREAMING:
        # Done state. Stream already kicked off on a prior tick.
        founder_dm = str(state.get("founder_dm_chat_id") or "")
        reconcile_rc = _creator_reconcile_finalization(
            output_dir=out,
            chat_id=founder_dm,
            sshsign_host=sshsign_host,
            session_id=session_id,
            group_chat_id=group_chat_id,
            sender=sender,
            session_client=client,
        )
        if reconcile_rc in (0, 3):
            state_store.delete_state(negotiation_id)
        write_trace(
            out,
            "resume.founder.noop",
            phase="resume",
            reason="already_streaming",
            negotiation_id=negotiation_id,
            session_id=session_id,
            reconcile_returncode=reconcile_rc,
        )
        return 0

    if founder_phase in (FOUNDER_PROMPT_GROUP, FOUNDER_WAIT_GROUP_ALREADY_PROMPTED):
        # Phase A or A-done. Founder hasn't /bound a group yet.
        if founder_phase == FOUNDER_WAIT_GROUP_ALREADY_PROMPTED:
            # Phase A-done: card already posted on a prior tick;
            # still waiting for the founder to /bind. No-op so we
            # don't spam the create-group card every 10s.
            write_trace(out, "resume.founder.noop", phase="waiting_for_group_bind", reason="already_prompted_for_group", negotiation_id=negotiation_id, session_id=session_id)
            return 0

        # Phase A: post create-group card, set resumed_at, exit.
        # Pull both bot handles + investor label from sshsign so the
        # card is fully formed (founder's handle from metadata_public
        # written at create-session; investor's handle from the
        # member row written at join). investor_handle may still be
        # empty if the investor's bot couldn't write it on join —
        # the card falls back to a placeholder; cron will re-emit
        # only after the founder /binds (we don't loop on phase A).
        founder_handle = ""
        investor_handle = ""
        investor_label = "your investor"
        try:
            meta_pub_raw = sess.get("metadata_public") or "{}"
            meta_member_raw = sess.get("metadata_member") or "{}"
            meta_pub = (
                json.loads(meta_pub_raw) if isinstance(meta_pub_raw, str)
                else (meta_pub_raw or {})
            )
            meta_member = (
                json.loads(meta_member_raw) if isinstance(meta_member_raw, str)
                else (meta_member_raw or {})
            )
            founder_handle = (meta_pub.get("founder_bot_handle") or "").strip()
            inv_name = (meta_member.get("investor_name") or "").strip()
            inv_firm = (meta_member.get("investor_firm") or "").strip()
            if inv_name and inv_firm:
                investor_label = f"{inv_name} at {inv_firm}"
            elif inv_name or inv_firm:
                investor_label = inv_name or inv_firm
            for m in (sess.get("members") or []):
                if (m.get("role") or "").lower() == "investor":
                    investor_handle = (m.get("bot_handle") or "").strip()
                    break
        except (json.JSONDecodeError, AttributeError):
            pass

        cg_body = format_event({
            "type": "create_group_for_founder",
            "session_code": state.get("session_code"),
            "founder_bot_handle": founder_handle,
            "investor_bot_handle": investor_handle,
            "investor_label": investor_label,
        })
        cg_markup = group_setup_reply_markup({
            "session_code": state.get("session_code"),
            "founder_bot_handle": founder_handle,
            "investor_bot_handle": investor_handle,
        })
        should_send_group_prompt = False
        marker = out / f".group_prompted_{negotiation_id}"
        try:
            with marker.open("x") as f:
                f.write("1\n")
            should_send_group_prompt = True
        except FileExistsError:
            pass
        except OSError:
            should_send_group_prompt = not marker.exists()
        # Founder DM chat_id was persisted to the state pointer at
        # mint time. config.json is the constraints/identity blob;
        # it does NOT carry chat_id, so we MUST read from state here.
        founder_dm_for_card = str(state.get("founder_dm_chat_id") or "")
        if cg_body and founder_dm_for_card and should_send_group_prompt:
            sender(founder_dm_for_card, message=cg_body, reply_markup=cg_markup)

        try:
            client.update_session_member(
                session_id, field="founder_resumed_at", value=int(now_fn()),
            )
        except SshsignSessionError as e:
            sys.stderr.write(f"resume phase A: update resumed_at: {e}\n")
            # Non-fatal: the card was sent. Next tick re-attempts the
            # write; idempotent (sshsign overwrites). Worst case: we
            # post the card again (mild spam) but never advance to
            # phase B. Acceptable risk for transient sshsign blips.
        write_trace(out, "resume.founder.group_required", phase="waiting_for_group_bind", negotiation_id=negotiation_id, session_id=session_id, chat_id=founder_dm_for_card)
        return 0

    if founder_phase != FOUNDER_START_STREAM:
        sys.stderr.write(f"resume: unknown founder phase {founder_phase}\n")
        return 3

    lease = _acquire_workflow_lease(
        client,
        output_dir=out,
        session_id=session_id,
        role="founder",
        action="negotiate",
    )
    if lease is None:
        write_trace(out, "resume.founder.lease_held", phase="resume", negotiation_id=negotiation_id, session_id=session_id)
        return 0

    # group_chat_id is set: Phase B (or combined first-pass if
    # resumed_at was null because the founder went straight from
    # mint → /bind without a cron tick in between).
    now_ts = int(now_fn())
    if not resumed_at:
        try:
            client.update_session_member(
                session_id, field="founder_resumed_at", value=now_ts,
            )
        except SshsignSessionError as e:
            sys.stderr.write(f"resume phase B (combined): resumed_at: {e}\n")
            # Continue — streaming_at is the more important signal
            # for the investor's wait gate.

    # Orienting card lands in the bound group.
    orient_body = format_event({
        "type": "founder_resumed",
        "session_code": state.get("session_code"),
    })
    if orient_body and group_chat_id:
        sender(group_chat_id, message=orient_body)

    # Re-hydrate mint + constraints from disk. These were written at
    # mint-time and output_dir is stable across OC reap events.
    try:
        config = json.loads((out / "config.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"resume: loading config.json: {e}\n")
        return 3
    try:
        mint = json.loads((out / "mint.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"resume: loading mint.json: {e}\n")
        return 3

    # Founder's DM chat_id from the state pointer (persisted at
    # mint time). Used for signing-URL routing; the round cards
    # land in the group via _stream_to_telegram.
    founder_dm = str(state.get("founder_dm_chat_id") or "")

    bot_username = os.environ.get("TELEGRAM_BOT_USERNAME", "AgenticPOA_bot")
    history_neg_id = mint.get("negotiation_id")

    try:
        # Set streaming_at BEFORE invoking _stream_to_telegram. The
        # investor's bounded poll gates run_distributed on this signal;
        # setting it post-stream would deadlock both sides (investor
        # only unblocks after founder's stream is DONE, by which time
        # the founder's run_distributed has exited).
        try:
            client.update_session_member(
                session_id, field="founder_streaming_at", value=int(now_fn()),
            )
        except SshsignSessionError as e:
            # Non-fatal: investor will time out at 180s with emergency
            # card. Stream proceeds; audit trail captures the gap.
            sys.stderr.write(f"resume: update-session-member streaming_at: {e}\n")

        try:
            stream_rc, signing_event = _stream_to_telegram(
                output_dir=out,
                chat_id=str(founder_dm),
                constraints=config.get("constraints"),
                bot_username=bot_username,
                group_chat_id=group_chat_id,
                negotiation_id=history_neg_id,
                sshsign_host=sshsign_host,
            )
        except Exception as e:
            write_trace(out, "resume.founder.stream_exception", phase="negotiating", negotiation_id=negotiation_id, session_id=session_id, error=str(e), group_chat_id=group_chat_id)
            raise
    finally:
        _release_workflow_lease(client, lease)

    if stream_rc != 0 or not signing_event:
        # Stream failed or exited before a signing event landed. State
        # stays (not terminal yet); next tick will re-check and dedup
        # if resumed_at is still set. Real failures are rare; let the
        # scan loop + audit log guide recovery.
        write_trace(out, "resume.founder.stream_finished", phase="negotiating", negotiation_id=negotiation_id, session_id=session_id, returncode=stream_rc, signing_event=bool(signing_event), group_chat_id=group_chat_id)
        return stream_rc

    pending_id = signing_event.get("pending_id") or ""
    if not pending_id:
        return 0

    # Creator (founder) finalize path — same as run_negotiate.
    rc = _creator_await_sign_and_finalize(
        output_dir=out,
        chat_id=str(founder_dm),
        sshsign_host=sshsign_host,
        pending_id=pending_id,
        session_id=session_id,
        group_chat_id=group_chat_id,
    )
    # If we timed out while waiting for signatures, keep the pointer so
    # cron can reconcile later once sshsign reports the aggregate session
    # complete. Other return codes are terminal for this local flow.
    if rc not in (1, 4):
        state_store.delete_state(negotiation_id)
    write_trace(out, "resume.founder.completed", phase="completed", negotiation_id=negotiation_id, session_id=session_id, returncode=rc, pending_id=pending_id, group_chat_id=group_chat_id)
    return rc


def _has_other_active_state_for_chat(
    negotiation_id: str,
    chat_id: str,
    role: str,
) -> bool:
    """Return true when the same Telegram DM has another active pointer.

    Cron scans all local state pointers, including leftovers from older
    live-test attempts. When an old sshsign session later becomes
    terminal, we should retire that pointer without sending a terminal
    card into a newer active DM flow for the same user.
    """
    if not chat_id:
        return False
    key = "investor_dm_chat_id" if role == "investor" else "founder_dm_chat_id"
    try:
        pointers = state_store.list_active()
    except Exception as e:  # pragma: no cover - defensive; status card is safer
        sys.stderr.write(f"active-state lookup failed: {e}\n")
        return False
    for pointer in pointers:
        if pointer.get("negotiation_id") == negotiation_id:
            continue
        if str(pointer.get(key) or "") == str(chat_id):
            return True
    return False


def _state_matches_output_dir(negotiation_id: str, out: Path) -> bool:
    """Verify a state pointer still owns its output directory.

    The live skill reuses `/tmp/safe_negotiate` across attempts. A stale
    pointer from an older negotiation can therefore point at a directory
    whose `mint.json` now belongs to a newer negotiation. Treat that
    pointer as stale before it can stream the wrong config/history pair.
    """
    mint_path = out / "mint.json"
    if not mint_path.exists():
        return True
    try:
        mint = json.loads(mint_path.read_text())
    except (OSError, json.JSONDecodeError):
        return True
    minted_id = mint.get("negotiation_id") or ""
    return not minted_id or minted_id == negotiation_id


def _is_shared_reused_output_dir(out: Path) -> bool:
    """True for the singleton demo output dir that gets reused per attempt."""
    configured = Path(os.environ.get("CLAW_NEGOTIATE_OUTPUT_DIR", "/tmp/safe_negotiate"))
    try:
        return out.resolve() == configured.resolve()
    except OSError:
        return str(out) == str(configured)


def _configured_role_from_output_dir(out: Path) -> str:
    try:
        config = json.loads((out / "config.json").read_text())
    except (OSError, json.JSONDecodeError):
        return ""
    constraints = config.get("constraints") if isinstance(config, dict) else {}
    return str((constraints or {}).get("role") or "").lower()


def _member_for_role(sess: dict, role: str) -> dict:
    for member in sess.get("members") or []:
        if isinstance(member, dict) and str(member.get("role") or "").lower() == role:
            return member
    return {}


def _state_from_session_role(
    *,
    sess: dict,
    role: str,
    output_dir: Path,
) -> dict | None:
    session_id = str(sess.get("session_id") or "")
    negotiation_id = _negotiation_id_from_sshsign_session_id(session_id)
    session_code = str(sess.get("session_code") or "")
    if role not in ("founder", "investor") or not negotiation_id or not session_code:
        return None
    if not _state_matches_output_dir(negotiation_id, output_dir):
        return None
    if not (output_dir / "config.json").exists() or not (output_dir / "mint.json").exists():
        return None

    member = _member_for_role(sess, role)
    telegram_user_id = str(member.get("telegram_user_id") or "")
    if not telegram_user_id and role == "founder":
        try:
            meta = json.loads(sess.get("metadata_member") or "{}")
        except (TypeError, json.JSONDecodeError):
            meta = {}
        telegram_user_id = str((meta.get("telegram") or {}).get("founder_user_id") or "")

    state = {
        "negotiation_id": negotiation_id,
        "output_dir": str(output_dir),
        "session_code": session_code,
        "role": role,
    }
    if role == "founder" and telegram_user_id:
        state["founder_dm_chat_id"] = telegram_user_id
    if role == "investor" and telegram_user_id:
        state["investor_dm_chat_id"] = telegram_user_id
    return state


def _write_reconstructed_state(state: dict) -> dict:
    try:
        state_store.write_state(state)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"state reconstruct write failed: {e}\n")
    return state


def _reconstruct_state_from_current_output(
    *,
    client,
    output_dir: Path | None = None,
    role: str | None = None,
) -> dict | None:
    out = output_dir or Path(os.environ.get("CLAW_NEGOTIATE_OUTPUT_DIR", "/tmp/safe_negotiate"))
    mint_path = out / "mint.json"
    try:
        mint = json.loads(mint_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    negotiation_id = mint.get("negotiation_id") or ""
    if not negotiation_id:
        return None
    local_role = (role or mint.get("user_role") or _configured_role_from_output_dir(out)).lower()
    if local_role not in ("founder", "investor"):
        return None
    try:
        sess = client.get_session(session_id=_sshsign_session_id(negotiation_id))
    except SshsignSessionError:
        return None
    state = _state_from_session_role(sess=sess, role=local_role, output_dir=out)
    return _write_reconstructed_state(state) if state else None


def _run_investor_resume(
    state: dict,
    session_client=None,
    sender=send_telegram,
    now_fn=None,
    sshsign_host: str | None = None,
) -> int:
    """Symmetric Path 1: investor-side cron resume.

    Mirrors `_run_founder_resume` for the investor. Triggered by
    `run_scan` whenever the investor's state pointer is found and
    sshsign shows the founder's `founder_streaming_at` is set
    (meaning the founder has /bound and is streaming). Replaces
    the old in-process `_investor_wait_for_founder_streaming` poll
    that timed out at 180s — way too short for Path 1's
    "founder creates group" wait.

    Returns:
      0 on success (stream + finalize completed), or whatever rc
        the joiner-finalize helper produced.
      1 founder hasn't started streaming yet; nothing to do this tick.
      2 session terminal/missing/stale; pointer already cleaned up.
      3 sshsign transport error; safe to retry on the next tick.

    Idempotency: dedup is a `investor_streaming_started` flag we
    persist into the state pointer the moment we begin streaming.
    A subsequent cron tick re-reads the pointer, sees the flag,
    and bails. Avoids double-spawning upstream (the same class of
    bug the founder side hit on INV-GD4KZ).
    """
    import time
    if now_fn is None:
        now_fn = time.time

    negotiation_id = state.get("negotiation_id") or ""
    output_dir_raw = state.get("output_dir") or ""
    if not negotiation_id or not output_dir_raw:
        sys.stderr.write(
            "investor resume: state missing negotiation_id or output_dir; skipping\n"
        )
        return 2

    out = Path(output_dir_raw)
    if not out.exists():
        sys.stderr.write(
            f"investor resume: output_dir {out} missing; cleaning state pointer\n"
        )
        state_store.delete_state(negotiation_id)
        return 2
    if not _state_matches_output_dir(negotiation_id, out):
        sys.stderr.write(
            f"investor resume: state {negotiation_id} no longer owns {out}; "
            "cleaning stale pointer\n"
        )
        state_store.delete_state(negotiation_id)
        return 2
    write_trace(out, "resume.investor.start", phase="resume", role="investor", negotiation_id=negotiation_id, session_code=state.get("session_code"))
    try:
        (out / ".session.pid").write_text(str(os.getpid()))
    except OSError:
        pass

    sshsign_host = sshsign_host or os.environ.get("SSHSIGN_HOST", "sshsign.dev")
    client = session_client or SshsignSession(host=sshsign_host)
    session_id = _sshsign_session_id(negotiation_id)

    try:
        sess = client.get_session(session_id=session_id)
    except SessionNotFoundError:
        state_store.delete_state(negotiation_id)
        return 2
    except SshsignSessionError as e:
        sys.stderr.write(f"investor resume: get-session failed: {e}\n")
        return 3

    status = normalize_status(sess.get("status"))
    if is_terminal_status(status):
        # Surface a status card to the investor so they aren't left
        # staring at a stale "waiting" card. If this is an older
        # terminal pointer for a DM that already has a different active
        # negotiation, clean it silently; otherwise the current demo DM
        # gets confusing canceled/expired cards from prior attempts.
        body = format_event({"type": "investor_session_ended", "status": status})
        target = state.get("investor_dm_chat_id") or ""
        suppress_card = _has_other_active_state_for_chat(
            negotiation_id,
            target,
            "investor",
        )
        if body and target and not suppress_card:
            sender(target, message=body)
        state_store.delete_state(negotiation_id)
        return 2

    group_chat_id = _resolve_group_chat_id(session_id, session_client=client)
    investor_phase, _founder_row = classify_investor_resume(
        state,
        sess,
        group_chat_id=group_chat_id,
    )
    if investor_phase == INVESTOR_ALREADY_STREAMING:
        write_trace(output_dir_raw, "resume.investor.noop", phase="resume", reason="already_streaming", negotiation_id=negotiation_id)
        return 0
    if investor_phase == INVESTOR_STALE_NO_FOUNDER:
        # Race: founder member row not present yet. Skip this tick.
        return 1

    if investor_phase == INVESTOR_WAIT_FOUNDER_STREAM:
        # Founder hasn't /bound + started streaming yet. Investor stays
        # in the wait state. The cron will retry every tick.
        write_trace(out, "resume.investor.not_ready", phase="waiting_for_founder", negotiation_id=negotiation_id, session_id=session_id)
        return 1

    if investor_phase == INVESTOR_WAIT_GROUP_BIND:
        # founder_streaming_at is set but no group_chat_id resolves —
        # shouldn't happen since the founder sets streaming_at AFTER
        # /bind writes group_chat_id. Defensive: treat as not-yet-ready
        # and let the next tick retry.
        write_trace(out, "resume.investor.not_ready", phase="waiting_for_group_bind", negotiation_id=negotiation_id, session_id=session_id)
        return 1

    if investor_phase != INVESTOR_START_STREAM:
        sys.stderr.write(f"investor resume: unknown phase {investor_phase}\n")
        return 3

    lease = _acquire_workflow_lease(
        client,
        output_dir=out,
        session_id=session_id,
        role="investor",
        action="negotiate",
    )
    if lease is None:
        write_trace(out, "resume.investor.lease_held", phase="resume", negotiation_id=negotiation_id, session_id=session_id)
        return 0

    # Mark as started BEFORE we spawn the stream subprocess. This is
    # the dedup gate: even if the stream takes 5 minutes and the cron
    # ticks 30 times during that window, every tick sees the flag and
    # exits without double-spawning.
    new_state = dict(state)
    new_state["investor_streaming_started"] = True
    send_online_card = not bool(new_state.get("investor_both_online_sent"))
    if send_online_card:
        new_state["investor_both_online_sent"] = True
    try:
        state_store.write_state(new_state)
    except state_store.StateCorruptError as e:
        sys.stderr.write(f"investor resume: write_state failed: {e}\n")
        # Continue anyway — worse case we double-spawn on the next
        # tick. Logging this for ops awareness.

    # Both sides online card to the GROUP — mirrors what the old
    # in-process wait helper used to post.
    online_body = format_event({"type": "investor_both_online"})
    if send_online_card and online_body:
        sender(group_chat_id, message=online_body)

    # Re-hydrate mint + constraints from disk.
    try:
        config = json.loads((out / "config.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"investor resume: loading config.json: {e}\n")
        return 3
    try:
        mint = json.loads((out / "mint.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"investor resume: loading mint.json: {e}\n")
        return 3

    investor_dm = str(state.get("investor_dm_chat_id") or "")
    bot_username = os.environ.get("TELEGRAM_BOT_USERNAME", "AgenticPOAInvestor_bot")
    history_neg_id = mint.get("negotiation_id")

    try:
        try:
            stream_rc, signing_event = _stream_to_telegram(
                output_dir=out,
                chat_id=investor_dm,
                constraints=config.get("constraints"),
                bot_username=bot_username,
                group_chat_id=group_chat_id,
                negotiation_id=history_neg_id,
                sshsign_host=sshsign_host,
            )
        except Exception as e:
            write_trace(out, "resume.investor.stream_exception", phase="negotiating", negotiation_id=negotiation_id, session_id=session_id, error=str(e), group_chat_id=group_chat_id)
            raise
    finally:
        _release_workflow_lease(client, lease)

    if stream_rc != 0 or not signing_event:
        # Stream failed before signing. Leave pointer in place so a
        # retry can re-attempt; in practice run_distributed completion
        # should always emit a signing event when it gets that far.
        retry_state = state_store.read_state(negotiation_id) or {}
        if retry_state.get("investor_streaming_started"):
            retry_state.pop("investor_streaming_started", None)
            try:
                state_store.write_state(retry_state)
            except state_store.StateCorruptError as e:
                sys.stderr.write(
                    f"investor resume: clearing started flag failed: {e}\n"
                )
        write_trace(out, "resume.investor.stream_finished", phase="negotiating", negotiation_id=negotiation_id, session_id=session_id, returncode=stream_rc, signing_event=bool(signing_event), group_chat_id=group_chat_id)
        return stream_rc

    pending_id = signing_event.get("pending_id") or ""
    if not pending_id:
        return 0

    # Joiner finalize path — investor waits for founder's complete-
    # session, then runs local finalize + posts the executed PDF.
    rc = _joiner_await_sign_and_finalize(
        output_dir=out,
        chat_id=investor_dm,
        sshsign_host=sshsign_host,
        pending_id=pending_id,
        session_id=session_id,
        group_chat_id=group_chat_id,
    )
    state_store.delete_state(negotiation_id)
    write_trace(out, "resume.investor.completed", phase="completed", negotiation_id=negotiation_id, session_id=session_id, returncode=rc, pending_id=pending_id, group_chat_id=group_chat_id)
    return rc


def run_scan(
    session_client=None,
    sender=send_telegram,
    now_fn=None,
) -> int:
    """Option B cron/recovery entrypoint.

    Each scan runs short shared-orchestrator reconciliation over local state
    pointers: project missing local-role cards, and run at most one due AI turn
    under a sshsign lease. Cron is a wakeup/recovery mechanism, not workflow
    truth.
    """
    now = now_fn() if now_fn else time.time()
    try:
        min_interval = float(os.environ.get("CLAW_NEGOTIATE_SCAN_MIN_INTERVAL", "15"))
    except ValueError:
        min_interval = 15.0
    throttle_path = state_store.state_dir() / ".scan_last"
    try:
        previous = float(throttle_path.read_text().strip())
    except (OSError, ValueError):
        previous = 0.0
    if min_interval > 0 and previous > 0 and now - previous < min_interval:
        return 0
    try:
        throttle_path.parent.mkdir(parents=True, exist_ok=True)
        throttle_path.write_text(str(now))
    except OSError as e:
        sys.stderr.write(f"scan throttle: {e}\n")

    _hydrate_scan_env_from_openclaw_config()
    client = session_client or SshsignSession(host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"))
    _reconstruct_state_from_current_output(client=client)
    states = []
    for state in state_store.list_active():
        negotiation_id = state.get("negotiation_id") or ""
        output_dir = Path(state.get("output_dir") or "")
        if (
            negotiation_id
            and output_dir
            and _is_shared_reused_output_dir(output_dir)
            and not _state_matches_output_dir(negotiation_id, output_dir)
        ):
            try:
                state_store.delete_state(negotiation_id)
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"scan: stale cleanup: {e}\n")
            continue
        states.append(state)
    results = orchestrator.reconcile_active(
        states=states,
        session_client=client,
        sender=sender,
    )
    for state, result in zip(states, results):
        if result.status.startswith("terminal:"):
            try:
                state_store.delete_state(state.get("negotiation_id") or "")
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"scan: terminal cleanup: {e}\n")
    return 0


def _reconstruct_founder_state_for_bind(
    *,
    negotiation_id: str,
    session_code: str,
    founder_dm_chat_id: str,
    output_dir: str | None = None,
) -> dict | None:
    """Build the minimal founder state pointer when the local JSON is missing.

    `/bind` is the founder's explicit wakeup. If the durable session and
    local config/mint files exist, the skill should not get stuck just
    because the tiny state pointer was lost or not written.
    """
    if not negotiation_id:
        return None
    out = Path(output_dir or os.environ.get("CLAW_NEGOTIATE_OUTPUT_DIR", "/tmp/safe_negotiate"))
    state = {
        "negotiation_id": negotiation_id,
        "output_dir": str(out),
        "session_code": session_code,
        "role": "founder",
        "founder_dm_chat_id": str(founder_dm_chat_id or ""),
    }
    if not _state_matches_output_dir(negotiation_id, out):
        return None
    if not (out / "config.json").exists() or not (out / "mint.json").exists():
        return None
    return _write_reconstructed_state(state)


def run_bind(
    session_code: str,
    group_chat_id: int,
    from_user_id: int,
    dm_chat_id_flag: str | None = None,
    sender=send_telegram,
    session_client=None,
) -> int:
    """Phase 8 /bind handler.

    Invoked when the founder types `/bind INV-XXXXX` in a Telegram group.
    Verifies the caller is the session founder (via metadata_member's
    telegram.founder_user_id, captured at create-session time), then
    calls sshsign `bind-group` to associate the group_chat_id with the
    session. Write-once on the server side, so a second /bind to a
    different group returns a typed error.

    Parameters are all plumbed from the OC Telegram envelope by the
    caller (SKILL.md instructs the model to supply them as flags).

    Return codes:
      0  success (bind applied)
      1  already bound to a different group (idempotent same-group ok)
      2  non-founder tried to bind / unknown code / bad chat type
      3  ssh/transport error

    Reply target: errors that need to reach the founder explicitly go
    to their DM (if dm_chat_id_flag resolves); generic group-context
    errors and the success confirmation go to the group. The wrong-chat
    error prefers DM because /bind in a DM means "I haven't created
    a group yet" — the user is still in the DM.
    """
    if group_chat_id >= 0:
        # Positive or zero chat_id means this wasn't a group — either a
        # DM (positive) or an invalid value. Steer the user to a group.
        body = format_event({"type": "bind_wrong_chat_type"})
        if body:
            target = group_chat_id if group_chat_id > 0 else (
                int(dm_chat_id_flag) if dm_chat_id_flag else 0
            )
            if target:
                sender(str(target), message=body)
        return 2

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )

    try:
        sess = client.get_session(session_code=session_code)
    except SessionNotFoundError:
        body = format_event({"type": "bind_unknown_code"})
        if body:
            sender(str(group_chat_id), message=body)
        return 2
    except SshsignSessionError as e:
        sys.stderr.write(f"bind: get-session failed: {e}\n")
        return 3

    # Pull founder_user_id from metadata_member. Best-effort: if it's
    # missing (older session minted before K1), we refuse the bind —
    # safer to fail closed than to let anyone in the group bind it.
    meta_raw = sess.get("metadata_member") or "{}"
    try:
        meta = json.loads(meta_raw) if isinstance(meta_raw, str) else (meta_raw or {})
    except (json.JSONDecodeError, TypeError):
        meta = {}
    expected_user_id = (meta.get("telegram") or {}).get("founder_user_id")
    if not expected_user_id:
        session_id_for_state = sess.get("session_id") or ""
        negotiation_id_for_state = _negotiation_id_from_sshsign_session_id(session_id_for_state)
        local_state = state_store.read_state(negotiation_id_for_state) if negotiation_id_for_state else None
        expected_user_id = (local_state or {}).get("founder_dm_chat_id")
    try:
        caller_matches_founder = bool(expected_user_id) and int(str(expected_user_id)) == int(from_user_id)
    except (TypeError, ValueError):
        caller_matches_founder = False
    if not caller_matches_founder:
        body = format_event({"type": "bind_wrong_user"})
        if body:
            sender(str(group_chat_id), message=body)
        return 2

    session_id = sess.get("session_id") or _sshsign_session_id(
        _negotiation_id_from_sshsign_session_id(sess.get("session_id", ""))
    )
    if not session_id:
        sys.stderr.write("bind: get-session returned no session_id\n")
        return 3

    try:
        client.bind_group(session_id, int(group_chat_id))
    except GroupAlreadyBoundError:
        body = format_event({"type": "bind_already_bound"})
        if body:
            sender(str(group_chat_id), message=body)
        return 1
    except SessionNotMemberError:
        # Creator IS a member, so this shouldn't fire unless the stored
        # user_id doesn't match a sshsign member row. Treat as auth failure.
        body = format_event({"type": "bind_wrong_user"})
        if body:
            sender(str(group_chat_id), message=body)
        return 2
    except SshsignSessionError as e:
        sys.stderr.write(f"bind-group failed: {e}\n")
        return 3

    # Success: post confirmation IN THE GROUP (not the DM).
    inv_name = meta.get("investor_name") or ""
    inv_firm = meta.get("investor_firm") or ""
    if inv_name and inv_firm:
        counterparty_label = f"{inv_name} at {inv_firm}"
    else:
        counterparty_label = inv_name or inv_firm or "your investor"
    body = format_event({
        "type": "group_bound",
        "session_code": sess.get("session_code") or session_code,
        "counterparty_label": counterparty_label,
    })
    if body:
        sender(str(group_chat_id), message=body)

    # P7-5: if the investor joined BEFORE this /bind turn landed, the
    # session is already in `joined` state. Don't wait for cron —
    # resume inline. The founder's process is live for this turn;
    # scan would eventually handle it, but the UX is better if we
    # skip the wait and stream now.
    status = (sess.get("status") or "").lower()
    if status == "joined":
        negotiation_id = _negotiation_id_from_sshsign_session_id(session_id)
        state = state_store.read_state(negotiation_id)
        if not state:
            state = _reconstruct_founder_state_for_bind(
                negotiation_id=negotiation_id,
                session_code=sess.get("session_code") or session_code,
                founder_dm_chat_id=str(expected_user_id or from_user_id),
            )
        if state:
            orchestrator.reconcile_state(
                state,
                session_client=client,
                sender=sender,
            )

    return 0


def run_setup(
    message: str,
    chat_id_flag: str | None = None,
    sender=send_telegram,
    persister=_persist_env_updates,
) -> int:
    """Parse the user's self-intro, persist identity env vars, and — if a
    stashed negotiation message exists from a prior first-run attempt —
    hand off to prepare automatically so the user doesn't have to retype.
    """
    if message.strip().upper() == "GO" and (Path("/tmp/safe_negotiate") / "config.json").exists():
        return run_negotiate("/tmp/safe_negotiate", chat_id_flag=chat_id_flag)

    chat_id = resolve_chat_id(chat_id_flag)
    typing = TypingLoop(chat_id=chat_id or "", bot_token=get_bot_token())
    typing.start()

    try:
        try:
            identity = extract_identity(message)
        except (ValueError, RuntimeError) as e:
            sys.stderr.write(f"Identity parse error: {e}\n")
            if chat_id:
                sender(chat_id, message=(
                    "\u26a0\ufe0f I couldn't read that. Try: "  # ⚠️
                    "\"I'm Name, Title at Company\" or \"Name, Firm\"."
                ))
            return 1

        if not identity.get("name"):
            if chat_id:
                sender(chat_id, message=(
                    "\u26a0\ufe0f I need at least your name. "
                    "Try: \"I'm Juan Figuera, CEO of APOA Inc\"."
                ))
            return 1
        role = (identity.get("role") or "founder").lower()
        if role == "founder" and not identity.get("company"):
            if chat_id:
                sender(chat_id, message=(
                    "\u26a0\ufe0f I also need your company name for the SAFE. "
                    "Try: \"I'm Juan Figuera, CEO of APOA Inc\"."
                ))
            return 1
        if role == "investor" and not identity.get("firm"):
            if chat_id:
                sender(chat_id, message=(
                    "\u26a0\ufe0f I also need your investor firm or fund. "
                    "Try: \"I'm Nora Vassileva, partner at SD Fund\"."
                ))
            return 1

        updates = _build_env_updates(identity)
        failures = persister(updates)
        if failures:
            sys.stderr.write(f"Failed to persist: {failures}\n")
            if chat_id:
                sender(chat_id, message=(
                    "\u26a0\ufe0f Saved partial profile. "
                    f"Couldn't write: {', '.join(failures)}. "
                    "The admin can fix via `openclaw config set`."
                ))

        if chat_id:
            who = identity.get("name", "you")
            where = identity.get("company") or identity.get("firm") or ""
            hello = f"\u2705 Got it, {who}"  # ✅
            if where:
                hello += f" at {where}"
            hello += ". I'll remember for next time."
            sender(chat_id, message=hello)
    finally:
        typing.stop()

    # If the user tried to negotiate BEFORE setup, we stashed their request —
    # pick it up now and hand off to prepare so they don't have to retype.
    if IDENTITY_SENTINEL_PATH.exists():
        try:
            pending = IDENTITY_SENTINEL_PATH.read_text().strip()
            IDENTITY_SENTINEL_PATH.unlink()
        except OSError:
            pending = ""
        if pending:
            # Env updates are hot-reloaded, but this Python process's
            # os.environ is a snapshot from spawn time. Apply the updates
            # in-process so the downstream prepare + mint see them.
            for key, value in updates.items():
                os.environ[key] = value
            if chat_id:
                sender(chat_id, message="Picking up your negotiation request\u2026")
            return run_prepare(
                message=pending,
                output_dir="/tmp/safe_negotiate",
                chat_id_flag=chat_id_flag,
                sender=sender,
            )

    return 0


_SIGNED_MARKER = ".signed"


def _mark_signed(output_dir: Path) -> None:
    """Drop a sentinel file indicating that the user's envelope was approved.

    Used by run_cancel to distinguish cancel-before-sign (→ `canceled`)
    from cancel-after-sign (→ `rescinded_after_sign`). A plain file beats
    re-querying sshsign since the state needs to survive across processes
    (user signs, then later says "cancel" as a fresh invocation).
    """
    try:
        (output_dir / _SIGNED_MARKER).write_text("1")
    except OSError:
        pass


def _has_signed(output_dir: Path) -> bool:
    return (output_dir / _SIGNED_MARKER).exists()


def run_cancel(
    output_dir: str,
    chat_id_flag: str | None = None,
    sender=send_telegram,
    session_client=None,
) -> int:
    """Cancel an in-flight negotiation.

    State model (see PLAN.md PR J5):
      state 1/2: open/joined → cancel-session, push "canceled before sign"
      state 3:   user has signed → cancel-session --rescind, push rescinded
      state 4:   completed → refuse, push "already executed"

    State 1 vs state 2 (before-deal vs after-deal-pre-sign) is not
    distinguished here: both route through cancel-session with the same
    user-facing copy for the cancel initiator. The observer-side copy
    is pushed by each OC's own wait/poll loop when it detects the
    status transition.
    """
    out = Path(output_dir)
    chat_id = resolve_chat_id(chat_id_flag)

    mint_path = out / "mint.json"
    if not mint_path.exists():
        if chat_id:
            sender(chat_id, message=(
                "\u2139\ufe0f No active negotiation to cancel."  # ℹ
            ))
        return 2

    try:
        mint = json.loads(mint_path.read_text())
    except json.JSONDecodeError:
        return 2

    session_id = _sshsign_session_id(mint.get("negotiation_id") or "")
    if not session_id:
        if chat_id:
            sender(chat_id, message=(
                "\u26a0\ufe0f Couldn't find a session to cancel."  # ⚠
            ))
        return 2

    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )
    negotiation_id = mint.get("negotiation_id") or ""

    def _cleanup_local_cancel_state() -> None:
        try:
            state_store.delete_state(negotiation_id)
        except Exception as _e:  # noqa: BLE001
            sys.stderr.write(f"cancel: state cleanup: {_e}\n")
        try:
            (out / ".session.pid").unlink()
        except (OSError, FileNotFoundError):
            pass

    # State 4 check: refuse if already completed.
    try:
        sess = client.get_session(session_id=session_id)
    except SshsignSessionError as e:
        sys.stderr.write(f"get-session on cancel: {e}\n")
        if chat_id:
            sender(chat_id, message=(
                "\u26a0\ufe0f Couldn't reach the signing service. "  # ⚠
                "Try again in a moment."
            ))
        return 3
    status = sess.get("status")
    preflight = cancel_preflight(status)
    if preflight.action == "refuse":
        body = format_event({"type": preflight.event_type})
        if chat_id and body:
            sender(chat_id, message=body)
        return preflight.return_code or 1
    if preflight.action == "noop":
        # Already in a terminal state — nothing to do. Tell the user so
        # they don't think the command silently failed.
        _cleanup_local_cancel_state()
        if chat_id:
            sender(chat_id, message=(
                "\u2139\ufe0f This negotiation is already "  # ℹ
                f"{preflight.status.replace('_', ' ')}."
            ))
        return preflight.return_code or 0

    # State 1/2 vs 3 split based on local .signed marker.
    rescind = _has_signed(out)
    session_code = mint.get("session_code") or sess.get("session_code") or ""

    # Post an optimistic "canceling…" card BEFORE the slow SSH
    # call. OC's exec lifetime can interrupt mid-call (observed
    # SIGTERM at 8s for INV-3YHM7). Without this immediate ack
    # the user sees nothing if SIGTERM fires between
    # cancel-session success and the confirm card emission.
    if chat_id and session_code:
        sender(chat_id, message=(
            f"\u23f3 Canceling **{session_code}**\u2026"  # ⏳
        ))

    try:
        client.cancel_session(session_id=session_id, rescind=rescind)
    except SshsignSessionError as e:
        try:
            latest = client.get_session(session_id=session_id)
            latest_preflight = cancel_preflight(latest.get("status"))
        except SshsignSessionError:
            latest_preflight = None
        if latest_preflight and latest_preflight.action == "noop":
            _cleanup_local_cancel_state()
            if chat_id:
                sender(chat_id, message=(
                    "\u2139\ufe0f This negotiation is already "  # ℹ
                    f"{latest_preflight.status.replace('_', ' ')}."
                ))
            return latest_preflight.return_code or 0
        sys.stderr.write(f"cancel-session failed: {e}\n")
        if chat_id:
            sender(chat_id, message=(
                "\u26a0\ufe0f Couldn't cancel — signing service error. "  # ⚠
                "Try again, or contact support if it persists."
            ))
        return 3

    body = format_event({
        "type": cancel_success_event_type(rescind=rescind),
        "session_code": session_code,
    })
    if chat_id and body:
        sender(chat_id, message=body)

    # Clean up local state so a future mint isn't blocked by
    # the active-negotiation gate. State pointer might already
    # be gone if scan beat us to it; ignore not-found.
    _cleanup_local_cancel_state()
    return 0


def run_profile(chat_id_flag: str | None = None, sender=send_telegram) -> int:
    """Show the user's saved identity (read from env vars) as a chat card."""
    chat_id = resolve_chat_id(chat_id_flag)
    profile = profile_from_env()
    body = format_event({"type": "profile", "profile": profile})
    if not body:
        return 2
    if chat_id:
        sender(chat_id, message=body)
    else:
        sys.stdout.write(body + "\n")
    return 0


def run_doctor() -> int:
    """Validate operator install/configuration for this skill."""
    checks = doctor_checks()
    sys.stdout.write(format_doctor(checks))
    return 0 if all(c.ok for c in checks) else 1


def _session_status_report(
    *,
    session_code: str = "",
    output_dir: str = "/tmp/safe_negotiate",
    session_client=None,
) -> dict:
    _hydrate_scan_env_from_openclaw_config()
    client = session_client or SshsignSession(
        host=os.environ.get("SSHSIGN_HOST", "sshsign.dev"),
    )
    out = Path(output_dir)
    sess: dict = {}
    if session_code:
        sess = client.get_session(session_code=session_code)
    else:
        try:
            mint = json.loads((out / "mint.json").read_text())
        except (OSError, json.JSONDecodeError):
            mint = {}
        negotiation_id = mint.get("negotiation_id") or ""
        if not negotiation_id:
            raise SessionNotFoundError("no session-code and no local mint.json")
        sess = client.get_session(session_id=_sshsign_session_id(negotiation_id))

    session_id = str(sess.get("session_id") or "")
    negotiation_id = _negotiation_id_from_sshsign_session_id(session_id)
    role = _configured_role_from_output_dir(out)
    state = state_store.read_state(negotiation_id) if negotiation_id else None
    reconstructable = False
    reconstructed_state = None
    if not state and role:
        reconstructed_state = _state_from_session_role(sess=sess, role=role, output_dir=out)
        reconstructable = bool(reconstructed_state)

    sshsign_host = os.environ.get("SSHSIGN_HOST", "sshsign.dev")
    history_rows = _ssh_history(negotiation_id, sshsign_host=sshsign_host) if negotiation_id else []
    history_rows = history_rows or []
    due_role = "founder" if len(history_rows) % 2 == 0 else "investor"
    if history_rows and history_rows[-1].get("type") == "accept":
        due_role = "signing"

    deliveries: list[dict] = []
    delivery_error = ""
    if session_id:
        try:
            deliveries = client.list_deliveries(session_id)
        except SshsignSessionError as e:
            delivery_error = str(e)

    return {
        "session_code": sess.get("session_code") or session_code,
        "session_id": session_id,
        "negotiation_id": negotiation_id,
        "status": sess.get("status") or "",
        "group_chat_id": sess.get("group_chat_id") or 0,
        "members": [
            {
                "role": m.get("role"),
                "bot_handle": m.get("bot_handle") or "",
                "telegram_user_id": m.get("telegram_user_id") or "",
            }
            for m in (sess.get("members") or [])
            if isinstance(m, dict)
        ],
        "round_count": len(history_rows),
        "last_round": history_rows[-1] if history_rows else None,
        "due_role": due_role,
        "local_role": role,
        "local_state_present": bool(state),
        "local_state_reconstructable": bool(state or reconstructable),
        "delivery_count": len(deliveries),
        "delivery_error": delivery_error,
    }


def _format_session_status(report: dict) -> str:
    group = report.get("group_chat_id") or "not bound"
    lines = [
        f"Session: {report.get('session_code') or '-'}",
        f"Status: {report.get('status') or '-'}",
        f"Group: {group}",
        f"Rounds: {report.get('round_count', 0)}",
        f"Next: {report.get('due_role') or '-'}",
        f"Local role: {report.get('local_role') or '-'}",
        "Local state: " + (
            "present" if report.get("local_state_present")
            else "reconstructable" if report.get("local_state_reconstructable")
            else "missing"
        ),
    ]
    members = report.get("members") or []
    if members:
        lines.append("Members:")
        for member in members:
            ident = member.get("telegram_user_id") or "no telegram id"
            handle = member.get("bot_handle") or "no bot handle"
            lines.append(f"- {member.get('role')}: {ident}, {handle}")
    if report.get("delivery_error"):
        lines.append(f"Deliveries: unavailable ({report['delivery_error']})")
    else:
        lines.append(f"Deliveries: {report.get('delivery_count', 0)}")
    return "\n".join(lines) + "\n"


def run_status(
    session_code: str = "",
    output_dir: str = "/tmp/safe_negotiate",
    json_output: bool = False,
    session_client=None,
) -> int:
    try:
        report = _session_status_report(
            session_code=session_code,
            output_dir=output_dir,
            session_client=session_client,
        )
    except SshsignSessionError as e:
        sys.stderr.write(f"status: {e}\n")
        return 3
    if json_output:
        sys.stdout.write(json.dumps(report, indent=2) + "\n")
    else:
        sys.stdout.write(_format_session_status(report))
    return 0


def run_smoke(output_dir: str = "/tmp/safe_negotiate", session_client=None) -> int:
    """Fast local smoke for the self-healing path.

    This intentionally avoids Telegram sends and real AI turns. It proves the
    installed skill can read current session state, reconstruct local state
    when possible, and produce a usable diagnostic report.
    """
    try:
        report = _session_status_report(
            output_dir=output_dir,
            session_client=session_client,
        )
    except SshsignSessionError as e:
        sys.stderr.write(f"smoke: {e}\n")
        return 3
    failures = []
    if not report.get("session_id"):
        failures.append("missing session")
    if not report.get("local_state_reconstructable"):
        failures.append("local state not reconstructable")
    if report.get("status") in ("open", "joined") and not report.get("members"):
        failures.append("missing members")
    if failures:
        sys.stderr.write("smoke failed: " + ", ".join(failures) + "\n")
        sys.stdout.write(_format_session_status(report))
        return 1
    sys.stdout.write("ok    self-healing smoke\n")
    sys.stdout.write(_format_session_status(report))
    return 0


def run_operator_setup(
    role: str = "",
    bot_username: str = "",
    sshsign_host: str = "",
    scan_interval: str = "",
    user_did: str = "",
    env_file: str = "",
    persister=None,
) -> int:
    """Persist operator-level skill env vars via OpenClaw config."""
    try:
        file_updates = load_env_file(env_file) if env_file else {}
        role = role or file_updates.get("NEGOTIATE_SAFE_BOT_ROLE", "")
        bot_username = bot_username or file_updates.get("TELEGRAM_BOT_USERNAME", "")
        sshsign_host = sshsign_host or file_updates.get("SSHSIGN_HOST", "")
        scan_interval = scan_interval or file_updates.get("CLAW_NEGOTIATE_SCAN_INTERVAL", "")
        user_did = user_did or file_updates.get("USER_DID", "")
        updates = build_operator_updates(
            role=role,
            bot_username=bot_username,
            sshsign_host=sshsign_host,
            scan_interval=scan_interval,
        )
        if user_did.strip():
            updates["USER_DID"] = user_did.strip()
    except (OSError, ValueError) as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    persist_fn = persister or persist_operator_updates
    failures = persist_fn(updates)
    for key, value in updates.items():
        status = "fail" if key in failures else "ok"
        sys.stdout.write(f"{status:<5} {key}={value}\n")
    if failures:
        sys.stderr.write(f"Failed to persist: {', '.join(failures)}\n")
        return 1
    return 0


def run_manifest() -> int:
    """Print the install/deploy manifest as JSON."""
    sys.stdout.write(json.dumps(load_skill_manifest(), indent=2) + "\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SAFE negotiation skill")
    sub = parser.add_subparsers(dest="command")

    prep = sub.add_parser("prepare", help="Parse NL message into constraints")
    prep.add_argument("--message", default="", help="The negotiation request text")
    prep.add_argument("--message-file", default="", help="Path to file containing the request (avoids shell $ expansion)")
    prep.add_argument("--output-dir", required=True)
    prep.add_argument("--founder-name", default=os.environ.get("FOUNDER_NAME", ""))
    prep.add_argument("--founder-title", default="CEO")
    prep.add_argument(
        "--chat-id",
        default="",
        help="Telegram chat id to push the confirm card to (falls back to openclaw sessions.json)",
    )

    neg = sub.add_parser("negotiate", help="Mint tokens and run negotiation")
    neg.add_argument("--output-dir", required=True)
    neg.add_argument(
        "--chat-id",
        default="",
        help="Telegram chat id to push events to (falls back to openclaw sessions.json)",
    )

    setup = sub.add_parser(
        "setup",
        help="Parse a self-introduction and persist identity env vars "
             "(also used for profile updates — any fields present in the "
             "message overwrite the previous values).",
    )
    setup.add_argument("--message", default="", help="Self-intro text")
    setup.add_argument("--message-file", default="")
    setup.add_argument("--chat-id", default="")

    profile = sub.add_parser(
        "profile",
        help="Show the user's currently saved identity",
    )
    profile.add_argument("--chat-id", default="")

    sub.add_parser(
        "doctor",
        help="Validate operator install/configuration before running a negotiation.",
    )
    status = sub.add_parser(
        "status",
        help="Show self-healing status for an INV code or the current output dir.",
    )
    status.add_argument("--session-code", default="")
    status.add_argument("--output-dir", default="/tmp/safe_negotiate")
    status.add_argument("--json", action="store_true")

    smoke = sub.add_parser(
        "smoke",
        help="Run a fast self-healing smoke check without Telegram sends.",
    )
    smoke.add_argument("--output-dir", default="/tmp/safe_negotiate")

    sub.add_parser(
        "manifest",
        help="Print the skill install/deploy manifest as JSON.",
    )

    operator_setup = sub.add_parser(
        "operator-setup",
        help="Persist operator-level skill configuration (role, bot handle, services).",
    )
    operator_setup.add_argument("--env-file", default="", help="Read setup values from a KEY=VALUE file.")
    operator_setup.add_argument("--role", default="", choices=["", "founder", "investor"])
    operator_setup.add_argument("--bot-username", default="")
    operator_setup.add_argument("--sshsign-host", default="")
    operator_setup.add_argument("--negotiate-repo-path", default="", help=argparse.SUPPRESS)
    operator_setup.add_argument("--scan-interval", default="")
    operator_setup.add_argument("--user-did", default="")

    cancel = sub.add_parser(
        "cancel",
        help="Cancel the in-flight negotiation. Automatically chooses "
             "between canceled and rescinded_after_sign based on whether "
             "the user has already signed their side.",
    )
    cancel.add_argument("--output-dir", required=True)
    cancel.add_argument("--chat-id", default="")

    bind = sub.add_parser(
        "bind",
        help="Phase 8: bind a two-party negotiation to the current "
             "Telegram group. Invoked by OC when the founder types "
             "/bind INV-XXXXX in a group.",
    )
    bind.add_argument(
        "--message",
        default="",
        help="The full /bind message body; the code is extracted from it.",
    )
    bind.add_argument(
        "--message-file",
        default="",
        help="Path to file containing the /bind message body.",
    )
    bind.add_argument(
        "--session-code",
        default="",
        help="Explicit INV-XXXXX (overrides --message parsing).",
    )
    bind.add_argument(
        "--chat-id",
        required=True,
        help="The GROUP chat_id where /bind was typed (negative int).",
    )
    bind.add_argument(
        "--from-id",
        required=True,
        help="The Telegram user_id of the sender of /bind.",
    )
    bind.add_argument(
        "--dm-chat-id",
        default="",
        help="Founder's DM chat_id (positive int). Used to steer the "
             "wrong-chat-type error back to the DM when /bind is typed "
             "in the DM by mistake.",
    )

    sub.add_parser(
        "scan",
        help="P7-5: resume any two-party negotiation whose investor "
             "has joined but the founder hasn't yet started streaming. "
             "Invoked by an OpenClaw cron job; idempotent across ticks.",
    )

    args = parser.parse_args()

    if args.command == "prepare":
        message = args.message
        if not message and args.message_file:
            message = Path(args.message_file).read_text().strip()
        if not message:
            sys.stderr.write("Provide --message or --message-file.\n")
            return 2
        return run_prepare(
            message,
            args.output_dir,
            args.founder_name,
            args.founder_title,
            chat_id_flag=args.chat_id or None,
        )
    elif args.command == "negotiate":
        return run_negotiate(args.output_dir, chat_id_flag=args.chat_id or None)
    elif args.command == "setup":
        message = args.message
        if not message and args.message_file:
            message = Path(args.message_file).read_text().strip()
        if not message:
            sys.stderr.write("Provide --message or --message-file for setup.\n")
            return 2
        return run_setup(message, chat_id_flag=args.chat_id or None)
    elif args.command == "profile":
        return run_profile(chat_id_flag=args.chat_id or None)
    elif args.command == "doctor":
        return run_doctor()
    elif args.command == "status":
        return run_status(
            session_code=args.session_code,
            output_dir=args.output_dir,
            json_output=args.json,
        )
    elif args.command == "smoke":
        return run_smoke(output_dir=args.output_dir)
    elif args.command == "manifest":
        return run_manifest()
    elif args.command == "operator-setup":
        return run_operator_setup(
            role=args.role,
            bot_username=args.bot_username,
            sshsign_host=args.sshsign_host,
            scan_interval=args.scan_interval,
            user_did=args.user_did,
            env_file=args.env_file,
        )
    elif args.command == "cancel":
        return run_cancel(args.output_dir, chat_id_flag=args.chat_id or None)
    elif args.command == "bind":
        message = args.message
        if not message and args.message_file:
            message = Path(args.message_file).read_text().strip()
        if _telegram_startgroup_payload(message):
            return 0
        code = (args.session_code or "").strip().upper()
        if not code:
            code = _extract_bind_code(message) or ""
        if not code:
            sys.stderr.write("bind: no INV-XXXXX code found in --session-code, --message, or --message-file.\n")
            return 2
        # OC's Telegram envelope encodes ids as `telegram:<numeric>`;
        # tolerate that prefix plus any leading/trailing whitespace.
        def _coerce_id(raw: str) -> int:
            s = (raw or "").strip()
            if ":" in s:
                s = s.rsplit(":", 1)[-1]
            return int(s)
        try:
            group_chat_id = _coerce_id(args.chat_id)
            from_user_id = _coerce_id(args.from_id)
        except ValueError as e:
            sys.stderr.write(f"bind: --chat-id and --from-id must be integers: {e}\n")
            return 2
        dm_flag = args.dm_chat_id or None
        if dm_flag and ":" in dm_flag:
            dm_flag = dm_flag.rsplit(":", 1)[-1]
        return run_bind(
            session_code=code,
            group_chat_id=group_chat_id,
            from_user_id=from_user_id,
            dm_chat_id_flag=dm_flag,
        )
    elif args.command == "scan":
        return run_scan()
    else:
        parser.print_help()
        return 2


if __name__ == "__main__":
    sys.exit(main())
