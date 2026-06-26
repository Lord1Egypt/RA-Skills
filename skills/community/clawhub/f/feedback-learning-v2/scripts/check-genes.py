#!/usr/bin/env python3
"""
check-genes.py v2 — View and manage promoted rules (genes).
Configurable via $FEEDBACK_LEARNING_DIR.

Usage:
  python3 check-genes.py                       # list all active rules
  python3 check-genes.py --all                 # include inactive/expired
  python3 check-genes.py --filter exec_fail    # filter by type
  python3 check-genes.py --resolve <gene_id>   # mark gene as resolved
  python3 check-genes.py --stale <gene_id>     # mark gene as stale
  python3 check-genes.py --json                # output raw JSON
"""
import json
import os
import sys
from datetime import datetime, timezone

DIR = os.environ.get("FEEDBACK_LEARNING_DIR",
                     os.path.expanduser("~/.openclaw/shared/learning"))
GENES_FILE = os.path.join(DIR, "genes.json")


def load_genes():
    if not os.path.exists(GENES_FILE):
        return {"version": "2.1", "rules": []}
    with open(GENES_FILE) as f:
        return json.load(f)


def save_genes(data):
    data["updated"] = datetime.now(timezone.utc).isoformat()
    with open(GENES_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    args = sys.argv[1:]
    show_all = "--all" in args
    json_out = "--json" in args
    filter_type = None
    resolve_id = None
    stale_id = None

    i = 0
    while i < len(args):
        if args[i] == "--filter" and i + 1 < len(args):
            filter_type = args[i + 1]
            i += 2
        elif args[i] == "--resolve" and i + 1 < len(args):
            resolve_id = args[i + 1]
            i += 2
        elif args[i] == "--stale" and i + 1 < len(args):
            stale_id = args[i + 1]
            i += 2
        else:
            i += 1

    data = load_genes()
    rules = data.get("rules", [])

    # Handle mutations
    if resolve_id:
        changed = False
        for r in rules:
            if r["id"] == resolve_id:
                r["status"] = "resolved"
                r["active"] = False
                r["resolved_at"] = datetime.now(timezone.utc).isoformat()
                changed = True
                print(f"✅ Gene {resolve_id} marked as resolved.")
                break
        if not changed:
            print(f"❌ Gene {resolve_id} not found.")
        else:
            save_genes(data)
        return

    if stale_id:
        changed = False
        for r in rules:
            if r["id"] == stale_id:
                r["status"] = "stale"
                changed = True
                print(f"⚠️  Gene {stale_id} marked as stale.")
                break
        if not changed:
            print(f"❌ Gene {stale_id} not found.")
        else:
            save_genes(data)
        return

    # Filter
    visible = []
    for r in rules:
        if not show_all and not r.get("active", True):
            continue
        if filter_type and r.get("type") != filter_type:
            continue
        visible.append(r)

    if json_out:
        print(json.dumps(visible, ensure_ascii=False, indent=2))
        return

    if not visible:
        print("No genes found. (Use --all to include inactive)")
        return

    STATUS_ICONS = {
        "active": "✅",
        "stale": "⚠️ ",
        "resolved": "✔️ ",
        "expired": "♻️ ",
        "wont-fix": "🚫",
    }

    print(f"\n{'='*60}")
    print(f"  GENES — Promoted Rules ({len(visible)} shown)")
    print(f"{'='*60}\n")

    for r in sorted(visible, key=lambda x: x.get("promoted_at", ""), reverse=True):
        status = r.get("status", "active")
        icon = STATUS_ICONS.get(status, "❓")
        print(f"{icon} [{r['id']}]  status={status}  hits={r.get('occurrences', '?')}")
        print(f"   CONDITION: {r.get('condition', r.get('rule', '(none)'))[:90]}")
        print(f"   ACTION:    {r.get('action', '(see condition)')[:90]}")
        if r.get("context"):
            print(f"   CONTEXT:   {r['context'][:90]}")
        print(f"   Agents: {', '.join(r.get('agents', []))}  |  Promoted: {r.get('promoted_at', '?')[:10]}")
        print()

    # Summary
    by_status = {}
    for r in rules:
        s = r.get("status", "active")
        by_status[s] = by_status.get(s, 0) + 1
    print(f"{'='*60}")
    print("  Summary: " + "  ".join(f"{STATUS_ICONS.get(s,'?')} {s}={c}" for s, c in sorted(by_status.items())))
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
