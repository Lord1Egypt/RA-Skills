#!/usr/bin/env python3
"""Run exactly one due negotiation turn without external negotiate repo deps."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from local_protocol import (
    NegotiationState,
    ProtocolSchema,
    load_apoa_token,
    validate_apoa_constraints,
    validate_offer_structure,
)
from openclaw_turn_agent import OpenClawTurnAgent, make_validated_offer
from upstream import ssh_history, synthesize_offer_event


def _emit(event: dict) -> None:
    sys.stdout.write(json.dumps(event) + "\n")
    sys.stdout.flush()


def _run_ssh(host: str, args: list[str], stdin_data: str | None = None) -> dict:
    remote_cmd = " ".join(shlex.quote(a) for a in args)
    result = subprocess.run(
        ["ssh", host, remote_cmd],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "ssh command failed").strip())
    return json.loads(result.stdout or "{}")


def _log_offer(
    *,
    host: str,
    negotiation_id: str,
    round_num: int,
    from_party: str,
    offer_type: str,
    metadata: dict,
    previous_tx: int | None,
) -> dict:
    return _run_ssh(host, [
        "log-offer",
        "--negotiation-id", negotiation_id,
        "--round", str(round_num),
        "--from", from_party,
        "--type", offer_type,
        "--metadata", json.dumps(metadata, separators=(",", ":")),
        "--previous-tx", str(previous_tx or 0),
    ])


def _sign_document(
    *,
    host: str,
    key_id: str,
    doc_type: str,
    payload: str,
    metadata: dict,
    session_id: str,
) -> dict:
    return _run_ssh(host, [
        "sign",
        "--type", doc_type,
        "--key-id", key_id,
        "--metadata", json.dumps(metadata, separators=(",", ":")),
        "--session-id", session_id,
    ], stdin_data=payload)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _history_to_offer(row: dict) -> dict | None:
    event = synthesize_offer_event(row)
    if not event:
        return None
    offer = {
        "type": event["type"],
        "from": event["party"],
        "round": event["round"],
        "terms": event.get("terms") or {},
        "message": event.get("message") or "",
    }
    if row.get("immudb_tx") is not None:
        offer["immudb_tx"] = row.get("immudb_tx")
    if row.get("audit_tx_id") is not None:
        offer["immudb_tx"] = row.get("audit_tx_id")
    return offer


def _config_for_role(mint: dict, role: str) -> dict:
    path = mint.get(f"{role}_config_path") or ""
    return _load_json(Path(path)) if path else {}


def _document_hash(negotiation_id: str, terms: dict, parties: dict, history: list[dict]) -> str:
    payload = {
        "negotiation_id": negotiation_id,
        "terms": terms,
        "parties": parties,
        "history": history,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _handle_agreement(
    *,
    output_dir: Path,
    negotiation_id: str,
    role: str,
    mint: dict,
    config: dict,
    state: NegotiationState,
    host: str,
) -> None:
    agreed = state.agreed_terms()
    if not agreed:
        return
    role_cfg = _config_for_role(mint, role)
    founder_cfg = _config_for_role(mint, "founder")
    investor_cfg = _config_for_role(mint, "investor")
    terms = {
        **agreed,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    terms.setdefault("investment_amount", role_cfg.get("investment_amount") or 500_000.0)
    parties = {
        "founder": {
            "company": founder_cfg.get("company_name") or config.get("constraints", {}).get("company_name") or "Company",
            "name": founder_cfg.get("name") or config.get("constraints", {}).get("founder_name") or "Founder",
            "title": founder_cfg.get("title") or config.get("constraints", {}).get("founder_title") or "",
        },
        "investor": {
            "name": investor_cfg.get("name") or config.get("constraints", {}).get("investor_name") or "Investor",
            "firm": investor_cfg.get("investor_firm") or config.get("constraints", {}).get("investor_firm") or "",
        },
    }
    doc_hash = _document_hash(negotiation_id, terms, parties, state.history)
    key_id = (
        role_cfg.get(f"{role}_signing_key_id")
        or role_cfg.get("signing_key_id")
        or role_cfg.get("founder_signing_key_id")
        or role_cfg.get("investor_signing_key_id")
        or ""
    )
    if not key_id:
        raise RuntimeError(f"missing signing key for {role}")
    metadata = {
        "company_name": parties["founder"]["company"],
        "valuation_cap": agreed.get("valuation_cap"),
        "discount_rate": agreed.get("discount_rate"),
        "pro_rata": agreed.get("pro_rata"),
        "mfn": agreed.get("mfn", False),
        "investment_amount": agreed.get("investment_amount"),
        "founder_name": parties["founder"]["name"],
        "founder_title": parties["founder"]["title"],
        "investor_name": parties["investor"]["name"],
        "investor_firm": parties["investor"]["firm"],
        "_signer_role": role.capitalize(),
    }
    result = _sign_document(
        host=host,
        key_id=key_id,
        doc_type="safe-agreement",
        payload=doc_hash,
        metadata=metadata,
        session_id=f"session_{negotiation_id}",
    )
    if result.get("error"):
        raise RuntimeError(str(result["error"]))
    pending_id = result.get("pending_id")
    if result.get("status") == "pending_cosign" and pending_id:
        pending_file = output_dir / f"{negotiation_id}_{role}_pending.txt"
        pending_file.write_text(str(pending_id), encoding="utf-8")
        _emit({
            "type": "signing",
            "pending_id": pending_id,
            "approval_url": result.get("approval_url"),
            "requires_signature": result.get("requires_signature", False),
        })


async def _run(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    config = _load_json(output_dir / "config.json")
    mint = _load_json(output_dir / "mint.json")
    role = str((config.get("constraints") or {}).get("role") or mint.get("user_role") or "").lower()
    if role not in ("founder", "investor"):
        raise RuntimeError(f"turn-once requires distributed role, got {role!r}")

    negotiation_id = mint["negotiation_id"]
    schema = ProtocolSchema.load()
    schema.negotiation_id = negotiation_id
    state = NegotiationState(schema=schema)

    history_raw = ssh_history(negotiation_id, sshsign_host=args.sshsign_host) or []
    agent_history: list[dict] = []
    previous_tx: int | None = None
    for row in history_raw:
        offer = _history_to_offer(row)
        if not offer:
            continue
        previous_tx = offer.get("immudb_tx") or previous_tx
        state.record_offer(offer)
        agent_history.append(offer)

    if state.terminated:
        if state.outcome == "accepted":
            pending_file = output_dir / f"{negotiation_id}_{role}_pending.txt"
            if not pending_file.exists():
                _handle_agreement(
                    output_dir=output_dir,
                    negotiation_id=negotiation_id,
                    role=role,
                    mint=mint,
                    config=config,
                    state=state,
                    host=args.sshsign_host,
                )
                return 0
        _emit({"type": "noop", "reason": "terminated"})
        return 0
    if state.whose_turn() != role:
        _emit({
            "type": "noop",
            "reason": "not_my_turn",
            "next_role": state.whose_turn(),
            "history_count": len(state.history),
        })
        return 0

    role_cfg = _config_for_role(mint, role)
    token_path = role_cfg.get("token") or mint.get(f"{role}_token_path")
    pubkey_path = role_cfg.get("pubkey") or ""
    if token_path:
        _token, constraints = load_apoa_token(token_path, pubkey_path)
    else:
        constraints = config.get("constraints") or {}

    agent = OpenClawTurnAgent(role=role, constraints=constraints)

    def _validate_structure(candidate: dict) -> tuple[bool, str]:
        candidate["from"] = role
        candidate["negotiation_id"] = negotiation_id
        candidate["round"] = state.current_round
        return validate_offer_structure(candidate, schema, previous_offer=state.last_offer())

    def _validate_constraints(terms: dict) -> tuple[bool, list[str]]:
        return validate_apoa_constraints(terms, constraints)

    offer = await make_validated_offer(
        agent=agent,
        history=agent_history,
        validate=_validate_structure,
        constraint_validate=_validate_constraints,
    )
    offer["from"] = role
    offer["negotiation_id"] = negotiation_id
    offer["round"] = state.current_round
    offer["timestamp"] = datetime.now(timezone.utc).isoformat()
    offer["apoa_validated"] = True

    tx_result = _log_offer(
        host=args.sshsign_host,
        negotiation_id=negotiation_id,
        round_num=state.current_round,
        from_party=role,
        offer_type=offer["type"],
        metadata={**offer.get("terms", {}), "_message": offer.get("message", "")},
        previous_tx=previous_tx,
    )
    offer["immudb_tx"] = tx_result.get("immudb_tx") or tx_result.get("audit_tx_id")
    _emit({
        "type": offer["type"],
        "party": role,
        "round": state.current_round,
        "terms": offer.get("terms", {}),
        "message": offer.get("message", ""),
        "immudb_tx": offer.get("immudb_tx"),
    })
    if offer["type"] == "accept":
        state.record_offer(offer)
        _handle_agreement(
            output_dir=output_dir,
            negotiation_id=negotiation_id,
            role=role,
            mint=mint,
            config=config,
            state=state,
            host=args.sshsign_host,
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one self-contained negotiation turn")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--negotiate-repo", default="", help="Ignored; kept for backwards compatibility.")
    parser.add_argument("--sshsign-host", default=os.environ.get("SSHSIGN_HOST", "sshsign.dev"))
    args = parser.parse_args()
    try:
        return asyncio.run(_run(args))
    except Exception as exc:  # noqa: BLE001 - CLI helper should surface concise failure
        sys.stderr.write(str(exc) + "\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
