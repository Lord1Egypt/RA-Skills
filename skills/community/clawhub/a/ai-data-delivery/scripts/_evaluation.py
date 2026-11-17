"""Evaluation provenance and explicit, time-bounded exception declarations."""
import datetime as dt
from _contract import digest, evidence, snapshot


def valid_waiver(case):
    waiver = case.get("declared_conflict")
    if not isinstance(waiver, dict) or not all(waiver.get(k) for k in ("ref", "note", "owner", "expires_on")):
        return False
    if case.get("id") not in waiver.get("case_ids", []):
        return False
    try:
        return dt.date.fromisoformat(waiver["expires_on"]) >= dt.datetime.now(dt.timezone.utc).date()
    except (ValueError, TypeError):
        return False


def report_evidence(args, cases_path):
    mode = "mock" if args.mode == "mock" else ("live" if args.endpoint else "offline")
    db_hash = None
    if args.db:
        conn, db_hash = snapshot(args.db)
        conn.close()
    return evidence(args.model, cases_path, mode=mode, data_snapshot_sha256=db_hash,
                    actual_sha256=digest(args.actual) if args.actual else None,
                    gold_results_sha256=digest(args.gold_results) if args.gold_results else None,
                    multihop_sha256=digest(args.multihop) if args.multihop else None,
                    endpoint=args.endpoint)
