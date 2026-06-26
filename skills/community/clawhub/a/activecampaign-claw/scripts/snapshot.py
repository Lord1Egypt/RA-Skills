#!/usr/bin/env python3
"""
snapshot.py — Versioned local taxonomy snapshot for diff / audit use.

Wraps `account_archive.py` with a date-stamped filename and a manifest entry.
Pair with `schema_diff.py` to see what changed between two snapshots.

The output is a local JSON file under `~/.activecampaign-skill/snapshots/`.
Nothing is transmitted anywhere.

Usage:
  python3 snapshot.py
  python3 snapshot.py --scope all --confirm --dir ~/.activecampaign-skill/snapshots
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, emit_files
from account_archive import fetch as archive_fetch  # type: ignore

DEFAULT_DIR = Path.home() / ".activecampaign-skill" / "snapshots"


_CONFIRM_NOTICE = """\
# Snapshot — confirmation required for `--scope all`

`--scope all` writes a versioned local JSON file containing the full
taxonomy plus every contact + every deal. On a large account that file
can be tens of megabytes. The file is local on your machine — never
transmitted anywhere — but it still contains customer data and should
be treated as such.

To proceed:

  python3 scripts/snapshot.py --scope all --confirm

For lighter scopes that don't need confirmation:

  python3 scripts/snapshot.py
  python3 scripts/snapshot.py --scope contacts
"""


def main():
    parser = argparse.ArgumentParser(
        description="Versioned local taxonomy snapshot for diff / audit"
    )
    parser.add_argument("--scope", choices=["taxonomy", "contacts", "deals", "all"], default="taxonomy")
    parser.add_argument("--confirm", action="store_true",
                        help="Required when --scope all is used.")
    parser.add_argument("--dir", default=str(DEFAULT_DIR))
    args = parser.parse_args()

    if args.scope == "all" and not args.confirm:
        print(_CONFIRM_NOTICE)
        sys.exit(0)

    out_dir = Path(args.dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = out_dir / f"snapshot-{stamp}-{args.scope}.json"

    client = ACClient()
    data = archive_fetch(client, args.scope)
    out_path.write_text(json.dumps(data, indent=2, default=str))
    sz = out_path.stat().st_size

    manifest = out_dir / "manifest.jsonl"
    with manifest.open("a") as f:
        f.write(json.dumps({
            "snapshot": out_path.name,
            "stamp": stamp,
            "scope": args.scope,
            "bytes": sz,
            "counts": {
                "lists": len(data.get("taxonomy", {}).get("lists", [])),
                "tags": len(data.get("taxonomy", {}).get("tags", [])),
                "fields": len(data.get("taxonomy", {}).get("fields", [])),
                "automations": len(data.get("taxonomy", {}).get("automations", [])),
                "contacts": len(data.get("contacts", [])) if "contacts" in data else None,
                "deals": len(data.get("deals", [])) if "deals" in data else None,
            },
        }) + "\n")
    print(f"Wrote {out_path} ({sz:,} bytes)")
    print(f"Wrote {manifest}")
    emit_files(out_path, manifest)


if __name__ == "__main__":
    main()
