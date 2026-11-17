#!/usr/bin/env python3
"""Initialize an AIDLC session scratch directory and UUID."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    p = argparse.ArgumentParser(description="Init AIDLC session scratch")
    p.add_argument(
        "--root",
        default="",
        help="Workspace root (default: cwd or OPENCLAW_WORKSPACE)",
    )
    p.add_argument("--objective", default="", help="Optional objective text")
    p.add_argument("--json", action="store_true", help="Print JSON summary")
    args = p.parse_args()

    import os

    root = Path(args.root or os.environ.get("OPENCLAW_WORKSPACE") or Path.cwd()).resolve()
    sessions = root / "aidlc-sessions"
    sessions.mkdir(parents=True, exist_ok=True)

    session_id = str(uuid.uuid4())
    session_dir = sessions / session_id
    session_dir.mkdir(parents=True, exist_ok=False)

    (session_dir / "session-id").write_text(session_id + "\n", encoding="utf-8")
    meta = {
        "session_id": session_id,
        "created_at": utc_now(),
        "objective": args.objective or None,
        "last_approved_gate": None,
        "phase": "inception",
        "status": "active",
    }
    (session_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (session_dir / "gates").mkdir()
    (session_dir / "APPROVALS.md").write_text(
        f"# AIDLC Approvals\n\nSession: `{session_id}`\nCreated: {meta['created_at']}\n\n",
        encoding="utf-8",
    )

    # Convenience pointer for "current" session in this workspace
    current = sessions / "CURRENT"
    current.write_text(session_id + "\n", encoding="utf-8")

    if args.json:
        print(
            json.dumps(
                {
                    "ok": True,
                    "session_id": session_id,
                    "session_dir": str(session_dir),
                    "current_pointer": str(current),
                },
                indent=2,
            )
        )
    else:
        print(session_id)
        print(session_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
