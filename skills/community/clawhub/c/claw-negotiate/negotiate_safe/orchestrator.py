"""Shared, short-lived orchestrator for two-bot SAFE negotiations.

This is Option B's core: OpenClaw turns call `reconcile_state` and exit. The
orchestrator reads sshsign as shared truth, projects missing local-role cards,
and, when this bot's role is due, runs exactly one AI turn under a sshsign
lease. No process waits for the counterparty's next message.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import projector
import delivery_store
from artifacts import build_artifact_uri
from format_event import format_event, group_setup_reply_markup
from reconcile import has_executed_delivered, mark_executed_delivered
from session_flow import sshsign_session_id
from sshsign_session import LeaseHeldError, SshsignSession, SshsignSessionError
from telegram_push import send_signing_url_to_dm, send_telegram
from trace_log import write_trace
from executed_pdf import finalize_executed_pdf
from upstream import ssh_history, synthesize_offer_event


TURN_HELPER = Path(__file__).with_name("_turn_once.py")


@dataclass(frozen=True)
class ReconcileResult:
    status: str
    projected: int = 0
    turn_ran: bool = False
    signing_event: dict | None = None


def _holder(output_dir: Path, role: str) -> str:
    host = (os.environ.get("HOSTNAME") or "local").split(".")[0]
    return f"claw-negotiate-orchestrator:{host}:{os.getpid()}:{role}:{output_dir.name}"


def _lease_generation(lease: dict | None) -> int:
    if not isinstance(lease, dict):
        return 1
    try:
        return int(lease.get("generation", 1))
    except (TypeError, ValueError):
        return 1


def _check_lease(client, *, session_id: str, role: str, action: str, holder: str, lease: dict | None) -> bool:
    try:
        client.check_lease(
            session_id=session_id,
            role=role,
            action=action,
            holder=holder,
            generation=_lease_generation(lease),
        )
        return True
    except SshsignSessionError:
        return False


def _session_group_chat_id(sess: dict) -> str | None:
    raw = sess.get("group_chat_id")
    if raw in (None, "", 0, "0"):
        return None
    return str(raw)


def _group_prompt_marker(output_dir: Path, negotiation_id: str) -> Path:
    return output_dir / f".group_prompted_{negotiation_id}"


def _send_group_setup_if_needed(
    *,
    output_dir: Path,
    negotiation_id: str,
    session_code: str,
    sess: dict,
    dm_chat_id: str,
    sender,
) -> bool:
    if not dm_chat_id:
        return False
    marker = _group_prompt_marker(output_dir, negotiation_id)
    try:
        with marker.open("x") as f:
            f.write("1\n")
    except FileExistsError:
        return False
    except OSError:
        if marker.exists():
            return False

    founder_handle = ""
    investor_handle = ""
    investor_label = "your investor"
    try:
        meta_pub_raw = sess.get("metadata_public") or "{}"
        meta_pub = json.loads(meta_pub_raw) if isinstance(meta_pub_raw, str) else (meta_pub_raw or {})
        founder_handle = (meta_pub.get("founder_bot_handle") or "").strip()
        inv_name = (meta_pub.get("investor_name") or "").strip()
        inv_firm = (meta_pub.get("investor_firm") or "").strip()
        if inv_name and inv_firm:
            investor_label = f"{inv_name} at {inv_firm}"
        elif inv_name or inv_firm:
            investor_label = inv_name or inv_firm
        for member in sess.get("members") or []:
            if not isinstance(member, dict):
                continue
            if (member.get("role") or "").lower() == "investor":
                investor_handle = (member.get("bot_handle") or "").strip()
                break
    except (json.JSONDecodeError, AttributeError):
        pass

    body = format_event({
        "type": "create_group_for_founder",
        "session_code": session_code,
        "founder_bot_handle": founder_handle,
        "investor_bot_handle": investor_handle,
        "investor_label": investor_label,
    })
    markup = group_setup_reply_markup({
        "session_code": session_code,
        "founder_bot_handle": founder_handle,
        "investor_bot_handle": investor_handle,
    })
    if not body:
        return False
    sender(dm_chat_id, message=body, reply_markup=markup)
    return True


def _due_role(history_rows: list[dict]) -> str:
    # SAFE schema first mover is founder. Rounds alternate by accepted
    # authoritative history count: 0 founder, 1 investor, 2 founder, ...
    return "founder" if len(history_rows) % 2 == 0 else "investor"


def _as_float(value) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _constraint_bool_required(constraints: dict, field: str) -> bool:
    value = constraints.get(field)
    if isinstance(value, dict):
        return bool(value.get("required"))
    return str(value or "").lower() == "required" or bool(constraints.get(f"{field}_required"))


def _terms_fit_constraints(terms: dict, constraints: dict) -> bool:
    checks = (
        ("valuation_cap", "valuation_cap_min", "valuation_cap_max"),
        ("investment_amount", "investment_amount_min", "investment_amount_max"),
        ("discount_rate", "discount_min", "discount_max"),
    )
    for term_key, min_key, max_key in checks:
        value = _as_float(terms.get(term_key))
        min_value = _as_float(constraints.get(min_key))
        max_value = _as_float(constraints.get(max_key))
        if value is None:
            continue
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
    if _constraint_bool_required(constraints, "pro_rata") and terms.get("pro_rata") is not True:
        return False
    if _constraint_bool_required(constraints, "mfn") and terms.get("mfn") is not True:
        return False
    return True


def _blocked_delivery_key(role: str, row: dict) -> str:
    return "apoa_blocked:{role}:{party}:{round}:{etype}".format(
        role=role,
        party=row.get("from") or "",
        round=row.get("round"),
        etype=row.get("type") or "",
    )


def _claim_private_notice(client, session_id: str, key: str, target: str) -> bool:
    if client is None:
        if delivery_store.has_delivery(session_id, key):
            return False
        return True
    payload = client.claim_delivery(session_id, key, target=target)
    return bool(payload.get("created"))


def _send_blocked_notice_if_needed(
    *,
    session_id: str,
    role: str,
    rows: list[dict],
    constraints: dict,
    dm_chat_id: str,
    sender,
    client,
) -> bool:
    if not rows or _due_role(rows) != role:
        return False
    latest = rows[-1]
    if latest.get("from") == role:
        return False
    event = synthesize_offer_event(latest)
    if not event:
        return False
    terms = event.get("terms") or {}
    if not terms or _terms_fit_constraints(terms, constraints):
        return False
    key = _blocked_delivery_key(role, latest)
    if not _claim_private_notice(client, session_id, key, str(dm_chat_id)):
        return False
    body = format_event({"type": "apoa_blocked_counterparty_offer", "role": role})
    if not body:
        return False
    result = sender(dm_chat_id, message=body)
    if client is None:
        delivery_store.mark_delivery(
            session_id,
            key,
            str(dm_chat_id),
            message_id=getattr(result, "message_id", None),
        )
    return True


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _accepted(history_rows: list[dict]) -> bool:
    return bool(history_rows) and (history_rows[-1].get("type") == "accept")


def _pending_path(output_dir: Path, negotiation_id: str, role: str) -> Path:
    return output_dir / f"{negotiation_id}_{role}_pending.txt"


def _negotiation_output_dir(mint: dict, fallback: Path) -> Path:
    return fallback


def _role_for_key_id(mint: dict, key_id: str) -> str:
    if not key_id:
        return ""
    for field, role in (
        ("founder_config_path", "founder"),
        ("investor_config_path", "investor"),
    ):
        path = mint.get(field) or ""
        if not path:
            continue
        try:
            cfg = json.loads(Path(path).read_text())
        except (OSError, json.JSONDecodeError):
            continue
        keys = {
            cfg.get("signing_key_id"),
            cfg.get("founder_signing_key_id"),
            cfg.get("investor_signing_key_id"),
        }
        if key_id in keys:
            return role
    return ""


def _session_signature_status(
    session_id: str,
    sshsign_host: str,
    runner=subprocess.run,
) -> dict | None:
    try:
        result = runner(
            ["ssh", sshsign_host, "session", "--id", session_id],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0 or not (result.stdout or "").strip():
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) and not payload.get("error") else None


def _write_session_pending_files(
    *,
    output_dir: Path,
    negotiation_id: str,
    mint: dict,
    signature_status: dict,
) -> None:
    signer_roles: list[tuple[str, str]] = []
    for signer in signature_status.get("signers") or []:
        if not isinstance(signer, dict):
            continue
        role = _role_for_key_id(mint, str(signer.get("key_id") or ""))
        pending_id = str(signer.get("pending_id") or "")
        if pending_id:
            signer_roles.append((role, pending_id))
        if role in ("founder", "investor") and pending_id:
            _pending_path(output_dir, negotiation_id, role).write_text(pending_id)

    known = {role for role, _pending_id in signer_roles if role in ("founder", "investor")}
    unknown = [pending_id for role, pending_id in signer_roles if role not in ("founder", "investor")]
    if len(signer_roles) == 2 and len(known) == 1 and len(unknown) == 1:
        missing_role = "investor" if "founder" in known else "founder"
        _pending_path(output_dir, negotiation_id, missing_role).write_text(unknown[0])


def _both_party_pending_ids(output_dir: Path, negotiation_id: str) -> dict[str, str] | None:
    ids: dict[str, str] = {}
    for role in ("founder", "investor"):
        path = _pending_path(output_dir, negotiation_id, role)
        try:
            pending_id = path.read_text().strip()
        except OSError:
            return None
        if not pending_id:
            return None
        ids[role] = pending_id
    return ids


def _run_turn_helper(
    *,
    output_dir: Path,
    negotiate_repo: str = "",
    sshsign_host: str,
    runner=subprocess.run,
    heartbeat_sender=None,
    heartbeat_chat_id: str | int | None = None,
    heartbeat_role: str = "",
    heartbeat_session_id: str = "",
    heartbeat_delivery_client=None,
    heartbeat_round: int | None = None,
    heartbeat_after: float = 25.0,
    still_working_after: float = 90.0,
) -> tuple[int, list[dict]]:
    cmd = [
        sys.executable,
        "-u",
        str(TURN_HELPER),
        "--output-dir",
        str(output_dir),
        "--negotiate-repo",
        negotiate_repo,
        "--sshsign-host",
        sshsign_host,
    ]
    if runner is subprocess.run:
        result = _run_turn_helper_with_heartbeats(
            cmd,
            heartbeat_sender=heartbeat_sender,
            heartbeat_chat_id=heartbeat_chat_id,
            heartbeat_role=heartbeat_role,
            heartbeat_session_id=heartbeat_session_id,
            heartbeat_delivery_client=heartbeat_delivery_client,
            heartbeat_round=heartbeat_round,
            heartbeat_after=heartbeat_after,
            still_working_after=still_working_after,
        )
    else:
        result = runner(cmd, capture_output=True, text=True, timeout=180)
    events: list[dict] = []
    for raw in (result.stdout or "").splitlines():
        line = raw.strip()
        if not line.startswith("{"):
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    if result.returncode != 0:
        err = (result.stderr or "").strip()
        if err:
            sys.stderr.write(err + "\n")
        if _is_token_expired_error(err):
            events.append({"type": "session_expired", "id": "apoa_token_expired"})
    return result.returncode, events


def _is_token_expired_error(stderr: str) -> bool:
    text = (stderr or "").lower()
    return "invalid apoa token" in text and "expired" in text


def _project_and_close_expired_session(
    *,
    client,
    session_id: str,
    negotiation_id: str,
    role: str,
    output_dir: Path,
    events: list[dict],
    projected: int,
    constraints: dict,
    dm_chat_id: str,
    group_chat_id: str | None,
    sender,
    dm_sender,
) -> ReconcileResult:
    for event in events:
        if event.get("type") != "session_expired":
            continue
        if projector.project_event(
            session_id=session_id,
            event=event,
            constraints=constraints,
            dm_chat_id=dm_chat_id,
            group_chat_id=group_chat_id,
            sender=sender,
            dm_sender=dm_sender,
            delivery_client=client,
        ):
            projected += 1
        try:
            client.cancel_session(session_id=session_id)
        except (AttributeError, SshsignSessionError):
            pass
        write_trace(
            output_dir,
            "orchestrator.session_expired",
            negotiation_id=negotiation_id,
            role=role,
        )
        return ReconcileResult("session_expired", projected=projected)
    return ReconcileResult("turn_failed", projected=projected)


def _send_signing_started_once(
    *,
    client,
    session_id: str,
    group_chat_id: str | None,
    sender,
) -> bool:
    if not group_chat_id:
        return False
    event = {"type": "signing_group_started"}
    if not projector._claim_delivery(
        delivery_client=client,
        session_id=session_id,
        key=projector.delivery_key(event),
        target=str(group_chat_id),
    ):
        return False
    from telegram import SIGNING_GROUP_PLACEHOLDER

    sender(group_chat_id, message=SIGNING_GROUP_PLACEHOLDER)
    return True


def _run_turn_helper_with_heartbeats(
    cmd: list[str],
    *,
    heartbeat_sender=None,
    heartbeat_chat_id: str | int | None = None,
    heartbeat_role: str = "",
    heartbeat_session_id: str = "",
    heartbeat_delivery_client=None,
    heartbeat_round: int | None = None,
    heartbeat_after: float = 25.0,
    still_working_after: float = 90.0,
) -> subprocess.CompletedProcess:
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    started = time.monotonic()
    heartbeat_sent = False
    still_sent = False
    timed_out = False
    while proc.poll() is None:
        elapsed = time.monotonic() - started
        if (
            heartbeat_sender
            and heartbeat_chat_id
            and not heartbeat_sent
            and elapsed >= heartbeat_after
        ):
            body = format_event({"type": "turn_heartbeat", "role": heartbeat_role})
            if body:
                result = heartbeat_sender(heartbeat_chat_id, message=body)
                message_id = str(getattr(result, "message_id", "") or "")
                if message_id and heartbeat_session_id and heartbeat_round is not None:
                    key = projector.heartbeat_delivery_key(heartbeat_role, heartbeat_round)
                    if heartbeat_delivery_client is None:
                        delivery_store.mark_delivery(
                            heartbeat_session_id,
                            key,
                            str(heartbeat_chat_id),
                            message_id=message_id,
                        )
                    else:
                        try:
                            heartbeat_delivery_client.claim_delivery(
                                heartbeat_session_id,
                                key,
                                target=str(heartbeat_chat_id),
                                message_id=message_id,
                            )
                        except Exception:
                            pass
            heartbeat_sent = True
        if (
            heartbeat_sender
            and heartbeat_chat_id
            and not still_sent
            and elapsed >= still_working_after
        ):
            body = format_event({"type": "turn_still_working", "role": heartbeat_role})
            if body:
                heartbeat_sender(heartbeat_chat_id, message=body)
            still_sent = True
        if elapsed >= 180:
            proc.kill()
            timed_out = True
            break
        time.sleep(1)
    stdout, stderr = proc.communicate()
    if timed_out:
        stderr = ((stderr or "") + "\nturn helper timed out after 180s").strip()
    return subprocess.CompletedProcess(
        cmd,
        124 if timed_out else int(proc.returncode or 0),
        stdout=stdout or "",
        stderr=stderr or "",
    )


def reconcile_state(
    state: dict,
    *,
    session_client=None,
    sender=send_telegram,
    dm_sender=send_signing_url_to_dm,
    history_fn=ssh_history,
    turn_runner=subprocess.run,
) -> ReconcileResult:
    negotiation_id = state.get("negotiation_id") or ""
    output_dir_raw = state.get("output_dir") or ""
    role = (state.get("role") or "").lower()
    if role not in ("founder", "investor") or not negotiation_id or not output_dir_raw:
        return ReconcileResult("invalid_state")

    output_dir = Path(output_dir_raw)
    try:
        config = _load_json(output_dir / "config.json")
        mint = _load_json(output_dir / "mint.json")
    except (OSError, json.JSONDecodeError):
        return ReconcileResult("missing_local_files")

    constraints = config.get("constraints") or {}
    if isinstance(constraints, dict):
        constraints = {**constraints, "mode": "two_party", "role": role}
    raw_dm_chat_id = (
        state.get("founder_dm_chat_id")
        if role == "founder"
        else state.get("investor_dm_chat_id")
    )
    dm_chat_id = str(raw_dm_chat_id or "")
    if not dm_chat_id:
        return ReconcileResult("missing_dm")

    sshsign_host = os.environ.get("SSHSIGN_HOST", "sshsign.dev")
    session_id = sshsign_session_id(negotiation_id)
    client = session_client or SshsignSession(host=sshsign_host)
    try:
        sess = client.get_session(session_id=session_id)
    except SshsignSessionError as e:
        write_trace(output_dir, "orchestrator.session_error", negotiation_id=negotiation_id, role=role, error=str(e))
        return ReconcileResult("session_error")

    status = (sess.get("status") or "").lower()
    if status not in ("joined", "created"):
        return ReconcileResult(f"terminal:{status}")
    group_chat_id = _session_group_chat_id(sess)
    if status != "joined":
        return ReconcileResult("waiting_for_group")
    if not group_chat_id:
        if role == "founder":
            sent = _send_group_setup_if_needed(
                output_dir=output_dir,
                negotiation_id=negotiation_id,
                session_code=state.get("session_code") or sess.get("session_code") or "",
                sess=sess,
                dm_chat_id=dm_chat_id,
                sender=sender,
            )
            if sent:
                write_trace(
                    output_dir,
                    "orchestrator.group_prompted",
                    negotiation_id=negotiation_id,
                    role=role,
                    chat_id=dm_chat_id,
                )
        return ReconcileResult("waiting_for_group")

    rows = history_fn(negotiation_id, sshsign_host=sshsign_host) or []
    projected = projector.project_history(
        session_id=session_id,
        history_rows=rows,
        constraints=constraints,
        dm_chat_id=dm_chat_id,
        group_chat_id=group_chat_id,
        sender=sender,
        dm_sender=dm_sender,
        delivery_client=client,
    )

    if _accepted(rows):
        pending_dir = _negotiation_output_dir(mint, output_dir)
        local_pending = _pending_path(pending_dir, negotiation_id, role)
        if not local_pending.exists():
            holder = _holder(output_dir, role)
            try:
                lease = client.acquire_lease(
                    session_id=session_id,
                    role=role,
                    action="negotiate",
                    holder=holder,
                    ttl_seconds=240,
                )
            except LeaseHeldError:
                return ReconcileResult("sign_lease_held", projected=projected)
            except SshsignSessionError as e:
                write_trace(output_dir, "orchestrator.sign_lease_error", negotiation_id=negotiation_id, role=role, error=str(e))
                return ReconcileResult("sign_lease_error", projected=projected)
            try:
                rc, events = _run_turn_helper(
                    output_dir=output_dir,
                    sshsign_host=sshsign_host,
                    runner=turn_runner,
                    heartbeat_sender=sender,
                    heartbeat_chat_id=group_chat_id,
                    heartbeat_role=role,
                    heartbeat_session_id=session_id,
                    heartbeat_delivery_client=client,
                    heartbeat_round=len(rows),
                )
                if rc != 0:
                    expired = _project_and_close_expired_session(
                        client=client,
                        session_id=session_id,
                        negotiation_id=negotiation_id,
                        role=role,
                        output_dir=output_dir,
                        events=events,
                        projected=projected,
                        constraints=constraints,
                        dm_chat_id=dm_chat_id,
                        group_chat_id=group_chat_id,
                        sender=sender,
                        dm_sender=dm_sender,
                    )
                    if expired.status == "session_expired":
                        return expired
                    return ReconcileResult("sign_failed", projected=projected)
                for event in events:
                    if event.get("type") == "signing":
                        _send_signing_started_once(
                            client=client,
                            session_id=session_id,
                            group_chat_id=group_chat_id,
                            sender=sender,
                        )
                        event = {**event, "_suppress_group_placeholder": True}
                        if projector.project_event(
                            session_id=session_id,
                            event=event,
                            constraints=constraints,
                            dm_chat_id=dm_chat_id,
                            group_chat_id=group_chat_id,
                            sender=sender,
                            dm_sender=dm_sender,
                            delivery_client=client,
                        ):
                            projected += 1
                        return ReconcileResult(
                            "signing_requested",
                            projected=projected,
                            signing_event=event,
                        )
            finally:
                try:
                    client.release_lease(
                        session_id=session_id,
                        role=role,
                        action="negotiate",
                        holder=holder,
                        generation=_lease_generation(lease),
                    )
                except SshsignSessionError:
                    pass

        signature_status = _session_signature_status(session_id, sshsign_host)
        if signature_status:
            _write_session_pending_files(
                output_dir=pending_dir,
                negotiation_id=negotiation_id,
                mint=mint,
                signature_status=signature_status,
            )
        if (
            role == "founder"
            and signature_status
            and signature_status.get("status") == "complete"
            and not has_executed_delivered(output_dir, negotiation_id)
        ):
            party_pending_ids = _both_party_pending_ids(pending_dir, negotiation_id)
            if not party_pending_ids:
                write_trace(
                    output_dir,
                    "orchestrator.finalize_waiting_for_both_pendings",
                    negotiation_id=negotiation_id,
                    role=role,
                )
                return ReconcileResult("awaiting_both_signatures", projected=projected)
            holder = _holder(output_dir, "creator")
            try:
                lease = client.acquire_lease(
                    session_id=session_id,
                    role="creator",
                    action="finalize",
                    holder=holder,
                    ttl_seconds=300,
                )
            except LeaseHeldError:
                return ReconcileResult("finalize_lease_held", projected=projected)
            except SshsignSessionError as e:
                write_trace(output_dir, "orchestrator.finalize_lease_error", negotiation_id=negotiation_id, role=role, error=str(e))
                return ReconcileResult("finalize_lease_error", projected=projected)
            try:
                pending_id = party_pending_ids[role]
                sender(group_chat_id, message="\U0001f4c4 Generating executed file\u2026")
                pdf_path = finalize_executed_pdf(output_dir, pending_id, sshsign_host)
                if not pdf_path:
                    return ReconcileResult("finalize_failed", projected=projected)
                if not _check_lease(
                    client,
                    session_id=session_id,
                    role="creator",
                    action="finalize",
                    holder=holder,
                    lease=lease,
                ):
                    return ReconcileResult("finalize_lease_lost", projected=projected)
                sender(group_chat_id, media_path=str(pdf_path))
                if not _check_lease(
                    client,
                    session_id=session_id,
                    role="creator",
                    action="finalize",
                    holder=holder,
                    lease=lease,
                ):
                    return ReconcileResult("finalize_lease_lost", projected=projected)
                try:
                    client.complete_session(
                        session_id=session_id,
                        executed_artifact=build_artifact_uri(
                            session_id,
                            Path(pdf_path),
                            creator_pending_id=pending_id,
                            creator_role=role,
                        ),
                        lease_holder=holder,
                        lease_generation=_lease_generation(lease),
                    )
                except SshsignSessionError as e:
                    write_trace(output_dir, "orchestrator.complete_session_error", negotiation_id=negotiation_id, error=str(e))
                    return ReconcileResult("complete_session_error", projected=projected)
                mark_executed_delivered(output_dir, negotiation_id)
                return ReconcileResult("finalized", projected=projected)
            finally:
                try:
                    client.release_lease(
                        session_id=session_id,
                        role="creator",
                        action="finalize",
                        holder=holder,
                        generation=_lease_generation(lease),
                    )
                except SshsignSessionError:
                    pass

        return ReconcileResult("awaiting_signatures", projected=projected)

    if _send_blocked_notice_if_needed(
        session_id=session_id,
        role=role,
        rows=rows,
        constraints=constraints,
        dm_chat_id=dm_chat_id,
        sender=sender,
        client=client,
    ):
        write_trace(
            output_dir,
            "orchestrator.apoa_blocked_counterparty_offer",
            negotiation_id=negotiation_id,
            role=role,
            round=rows[-1].get("round") if rows else None,
        )

    if _due_role(rows) != role:
        return ReconcileResult("waiting_for_counterparty", projected=projected)

    holder = _holder(output_dir, role)
    try:
        lease = client.acquire_lease(
            session_id=session_id,
            role=role,
            action="negotiate",
            holder=holder,
            ttl_seconds=240,
        )
    except LeaseHeldError:
        return ReconcileResult("lease_held", projected=projected)
    except SshsignSessionError as e:
        write_trace(output_dir, "orchestrator.lease_error", negotiation_id=negotiation_id, role=role, error=str(e))
        return ReconcileResult("lease_error", projected=projected)

    signing_event = None
    try:
        rc, events = _run_turn_helper(
            output_dir=output_dir,
            sshsign_host=sshsign_host,
            runner=turn_runner,
            heartbeat_sender=sender,
            heartbeat_chat_id=group_chat_id,
            heartbeat_role=role,
            heartbeat_session_id=session_id,
            heartbeat_delivery_client=client,
            heartbeat_round=len(rows),
        )
        if rc != 0:
            write_trace(output_dir, "orchestrator.turn_failed", negotiation_id=negotiation_id, role=role, returncode=rc)
            return _project_and_close_expired_session(
                client=client,
                session_id=session_id,
                negotiation_id=negotiation_id,
                role=role,
                output_dir=output_dir,
                events=events,
                projected=projected,
                constraints=constraints,
                dm_chat_id=dm_chat_id,
                group_chat_id=group_chat_id,
                sender=sender,
                dm_sender=dm_sender,
            )
        for event in events:
            if event.get("type") == "noop":
                continue
            if event.get("type") == "signing":
                _send_signing_started_once(
                    client=client,
                    session_id=session_id,
                    group_chat_id=group_chat_id,
                    sender=sender,
                )
                event = {**event, "_suppress_group_placeholder": True}
                signing_event = event
            if projector.project_event(
                session_id=session_id,
                event=event,
                constraints=constraints,
                dm_chat_id=dm_chat_id,
                group_chat_id=group_chat_id,
                sender=sender,
                dm_sender=dm_sender,
                delivery_client=client,
            ):
                projected += 1
    finally:
        try:
            client.release_lease(
                session_id=session_id,
                role=role,
                action="negotiate",
                holder=holder,
                generation=_lease_generation(lease),
            )
        except SshsignSessionError:
            pass

    return ReconcileResult(
        "turn_ran",
        projected=projected,
        turn_ran=True,
        signing_event=signing_event,
    )


def reconcile_active(
    *,
    states: list[dict],
    session_client=None,
    sender=send_telegram,
    dm_sender=send_signing_url_to_dm,
) -> list[ReconcileResult]:
    return [
        reconcile_state(
            state,
            session_client=session_client,
            sender=sender,
            dm_sender=dm_sender,
        )
        for state in states
    ]
