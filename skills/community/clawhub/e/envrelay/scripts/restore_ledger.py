#!/usr/bin/env python3
"""Per-item restore ledger: what happened to every entry in the manifest.

restore_ledger.py LEDGER.json init --manifest MANIFEST.json
restore_ledger.py LEDGER.json set --kind K --id ID --status S [--reason R] [--next-action A]
restore_ledger.py LEDGER.json get --kind K --id ID
restore_ledger.py LEDGER.json list [--kind K] [--status S]
restore_ledger.py LEDGER.json report

`init` seeds one `pending` line per manifest entry, so "did I finish?" is a
query against the ledger, not a memory exercise, and an interrupted restore
resumes from `list --status pending`. `set` records an outcome (attempts are
counted across repeated sets of the same item). `report` prints the
human-readable summary that becomes the restore report.

Statuses are validated against the vocabulary in references/manifest.md —
the ledger is where that vocabulary is enforced, not just documented. The
script writes nothing but its own ledger file, atomically.
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

GENERIC = {"pending", "failed", "requires-user-action"}
VOCABULARY = {
    "file": {"restored", "skipped-exists", "merged"},
    "credential": {"restored", "skipped-exists"},
    "repo": {"cloned", "restored-files", "head-unreachable", "path-exists", "clone-failed"},
    "software": {
        "installed", "already-present", "compatible-alias", "not-found",
        "version-unavailable", "blocked-by-trust", "blocked-by-tls", "unknown-source",
    },
    "app": {
        "installed", "already-present", "alternate-path", "requires-app-store",
        "requires-enterprise-enrollment", "unknown-source",
    },
    "agent": {
        "restored", "config-restored", "extensions-partial", "needs-login",
        "not-installed", "skipped",
    },
    "other": set(),
}
# Everything that still needs a human: not yet done, failed, or done-ness
# that consists of handing the item to the user.
ATTENTION = GENERIC | {
    "not-found", "version-unavailable", "blocked-by-trust", "blocked-by-tls",
    "unknown-source", "requires-app-store", "requires-enterprise-enrollment",
    "head-unreachable", "clone-failed", "path-exists",
    "config-restored", "extensions-partial", "needs-login", "not-installed",
}


def fail(message):
    print(f"restore_ledger: {message}", file=sys.stderr)
    sys.exit(1)


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path, must_exist):
    if not os.path.exists(path):
        if must_exist:
            fail(f"{path} does not exist; run init first")
        return {"created_at": now(), "items": {}}
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as error:
        fail(f"cannot read {path}: {error}")


def save(path, ledger):
    directory = os.path.dirname(os.path.abspath(path))
    handle = tempfile.NamedTemporaryFile(
        "w", dir=directory, prefix=".ledger-", suffix=".tmp", delete=False, encoding="utf-8"
    )
    try:
        with handle:
            json.dump(ledger, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(handle.name, path)
    except BaseException:
        os.unlink(handle.name)
        raise


def seed(ledger, kind, item_id):
    key = f"{kind}:{item_id}"
    if key not in ledger["items"]:
        ledger["items"][key] = {
            "kind": kind,
            "id": item_id,
            "status": "pending",
            "attempts": 0,
            "updated_at": now(),
        }


def cmd_init(args):
    try:
        with open(args.manifest, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError) as error:
        fail(f"cannot read manifest {args.manifest}: {error}")

    ledger = load(args.ledger, must_exist=False)
    ledger.setdefault("backup_id", manifest.get("backup_id"))
    for item in manifest.get("files", []):
        seed(ledger, "file", item.get("archive") or item.get("original", "?"))
    for item in manifest.get("credentials", []):
        seed(ledger, "credential", item.get("archive") or item.get("original", "?"))
    for item in manifest.get("git_repos", []):
        seed(ledger, "repo", item.get("original", "?"))
    for item in manifest.get("software", []):
        seed(ledger, "software", f"{item.get('manager', '?')}:{item.get('name', '?')}")
    for item in manifest.get("apps", []):
        seed(ledger, "app", item.get("bundle_id") or item.get("name", "?"))
    for item in manifest.get("agents", []):
        seed(ledger, "agent", item.get("id") or item.get("name", "?"))
    save(args.ledger, ledger)
    print(json.dumps({"items": len(ledger["items"])}))


def cmd_set(args):
    allowed = VOCABULARY[args.kind] | GENERIC
    if args.status not in allowed:
        fail(
            f"'{args.status}' is not a {args.kind} status; "
            f"allowed: {', '.join(sorted(allowed))} (see references/manifest.md)"
        )
    ledger = load(args.ledger, must_exist=False)
    key = f"{args.kind}:{args.id}"
    if key not in ledger["items"]:
        # Usually a typo'd id: init seeded the real one, which stays pending.
        print(
            f"restore_ledger: note: {key} was not seeded by init; creating it "
            f"(run list to see the seeded ids)",
            file=sys.stderr,
        )
    item = ledger["items"].setdefault(key, {"kind": args.kind, "id": args.id, "attempts": 0})
    item["status"] = args.status
    item["attempts"] = item.get("attempts", 0) + 1
    item["updated_at"] = now()
    for field, value in (("reason", args.reason), ("next_action", args.next_action)):
        if value:
            item[field] = value
    save(args.ledger, ledger)
    print(json.dumps(item, sort_keys=True))


def cmd_get(args):
    ledger = load(args.ledger, must_exist=True)
    item = ledger["items"].get(f"{args.kind}:{args.id}")
    if item is None:
        fail(f"no ledger entry {args.kind}:{args.id}")
    print(json.dumps(item, sort_keys=True))


def selected(ledger, kind, status):
    return [
        item
        for _key, item in sorted(ledger["items"].items())
        if (kind is None or item["kind"] == kind)
        and (status is None or item["status"] == status)
    ]


def cmd_list(args):
    ledger = load(args.ledger, must_exist=True)
    json.dump(selected(ledger, args.kind, args.status), sys.stdout, indent=2, sort_keys=True)
    print()


def cmd_report(args):
    ledger = load(args.ledger, must_exist=True)
    items = selected(ledger, None, None)
    if ledger.get("backup_id"):
        print(f"Restore report for {ledger['backup_id']}")
    print(f"{len(items)} items\n")

    by_kind = {}
    for item in items:
        by_kind.setdefault(item["kind"], {}).setdefault(item["status"], []).append(item)
    for kind in sorted(by_kind):
        counts = ", ".join(
            f"{len(entries)} {status}" for status, entries in sorted(by_kind[kind].items())
        )
        print(f"  {kind}: {counts}")

    open_items = [item for item in items if item["status"] in ATTENTION]
    if open_items:
        print("\nNeeds attention:")
        for item in open_items:
            line = f"  [{item['status']}] {item['kind']} {item['id']}"
            if item.get("reason"):
                line += f" — {item['reason']}"
            if item.get("next_action"):
                line += f" → {item['next_action']}"
            print(line)
    else:
        print("\nNothing left open.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ledger", help="path to the ledger JSON file")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="seed pending items from a manifest")
    init.add_argument("--manifest", required=True)

    setter = commands.add_parser("set", help="record an item's outcome")
    setter.add_argument("--kind", required=True, choices=sorted(VOCABULARY))
    setter.add_argument("--id", required=True)
    setter.add_argument("--status", required=True)
    setter.add_argument("--reason")
    setter.add_argument("--next-action")

    getter = commands.add_parser("get", help="print one item")
    getter.add_argument("--kind", required=True, choices=sorted(VOCABULARY))
    getter.add_argument("--id", required=True)

    lister = commands.add_parser("list", help="print items as JSON")
    lister.add_argument("--kind", choices=sorted(VOCABULARY))
    lister.add_argument("--status")

    commands.add_parser("report", help="print the human-readable summary")

    args = parser.parse_args()
    {"init": cmd_init, "set": cmd_set, "get": cmd_get, "list": cmd_list, "report": cmd_report}[
        args.command
    ](args)


if __name__ == "__main__":
    main()
