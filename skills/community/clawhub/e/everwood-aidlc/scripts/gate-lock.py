#!/usr/bin/env python3
"""Lock an approved AIDLC gate artifact into session scratch (workspace SoT)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

GATE_KEYS = {
    "0": "gate-0-context",
    "1": "gate-1-assess",
    "2": "gate-2-decompose",
    "3": "gate-3-design",
    "4": "gate-4-plan",
    "gate-0-context": "gate-0-context",
    "gate-1-assess": "gate-1-assess",
    "gate-2-decompose": "gate-2-decompose",
    "gate-3-design": "gate-3-design",
    "gate-4-plan": "gate-4-plan",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve_session_dir(root: Path, session_id: str | None) -> tuple[str, Path]:
    sessions = root / "aidlc-sessions"
    if not session_id:
        current = sessions / "CURRENT"
        if not current.is_file():
            raise FileNotFoundError("No CURRENT session; run session-init.py first")
        session_id = current.read_text(encoding="utf-8").strip()
    session_id = str(uuid.UUID(session_id))
    session_dir = sessions / session_id
    if not session_dir.is_dir():
        raise FileNotFoundError(f"session dir missing: {session_dir}")
    return session_id, session_dir


def main() -> int:
    p = argparse.ArgumentParser(description="Lock approved AIDLC gate into session scratch")
    p.add_argument("--root", default=os.environ.get("OPENCLAW_WORKSPACE") or str(Path.cwd()))
    p.add_argument("--session-id", default="")
    p.add_argument("--gate", required=True, help="0..4 or gate-N-name")
    p.add_argument("--artifact-file", required=True)
    p.add_argument("--status", choices=("approved", "soft-approved"), default="approved")
    p.add_argument("--objective", default="")
    p.add_argument("--linear-issue", default="")
    args = p.parse_args()

    root = Path(args.root).resolve()
    gate_key = GATE_KEYS.get(str(args.gate).strip())
    if not gate_key:
        print(json.dumps({"ok": False, "error": f"unknown gate: {args.gate}"}), file=sys.stderr)
        return 2

    artifact_path = Path(args.artifact_file)
    if not artifact_path.is_file():
        print(json.dumps({"ok": False, "error": f"artifact not found: {artifact_path}"}), file=sys.stderr)
        return 2
    artifact = artifact_path.read_text(encoding="utf-8")
    if not artifact.strip():
        print(json.dumps({"ok": False, "error": "artifact empty"}), file=sys.stderr)
        return 2

    session_id, session_dir = resolve_session_dir(root, args.session_id or None)
    gates_dir = session_dir / "gates"
    gates_dir.mkdir(exist_ok=True)
    out_name = f"{gate_key}.md"
    out_path = gates_dir / out_name
    out_path.write_text(artifact, encoding="utf-8")

    meta_path = session_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    gate_n = int(gate_key.split("-")[1])
    meta.update(
        {
            "session_id": session_id,
            "last_approved_gate": gate_n,
            "last_gate_key": gate_key,
            "status": args.status,
            "phase": "plan-approved" if gate_n >= 4 else "inception",
            "updated_at": utc_now(),
        }
    )
    if args.objective:
        meta["objective"] = args.objective
    if args.linear_issue:
        meta["linear_issue"] = args.linear_issue
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    approvals = session_dir / "APPROVALS.md"
    with approvals.open("a", encoding="utf-8") as fh:
        fh.write(f"## {gate_key} — {args.status} @ {utc_now()}\n\n")
        fh.write(f"Artifact: `gates/{out_name}`\n\n")

    print(
        json.dumps(
            {
                "ok": True,
                "session_id": session_id,
                "gate_key": gate_key,
                "artifact_path": str(out_path),
                "meta": meta,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        raise SystemExit(1)
