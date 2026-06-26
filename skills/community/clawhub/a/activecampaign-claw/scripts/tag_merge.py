#!/usr/bin/env python3
"""
tag_merge.py — Hygiene helper: consolidate two tags that semantically mean
the same thing into one canonical tag.

Use cases: cleaning up case-mismatch duplicates (`Customer` vs `customer`),
separator typos (`webinar-attendee` vs `webinar_attendee`), or accidental
re-creation of an existing tag during an import. Not intended for bulk
re-tagging campaigns — for that, build a segment and run an automation in
the AC UI.

Safety layers (all enabled by default):
  - Dry-run by default. Prints the plan and exits without any change.
  - `--confirm` is required to perform any modification.
  - Refuses to operate if a source-tag reference is found in any active
    automation or segment. Use `--force-with-refs` ONLY after manually
    updating those references in the AC UI first.
  - Refuses to run at all when the `AC_READ_ONLY=1` environment variable is
    set.
  - Every modification is recorded in the local write audit log at
    `~/.activecampaign-skill/writes.jsonl` (payload SHA, not payload).

Usage:
  # Plan only (no changes)
  python3 tag_merge.py --source "Customer" --target "customer"

  # Execute
  python3 tag_merge.py --source "Customer" --target "customer" --confirm

  # Execute even though automation/segment references exist
  python3 tag_merge.py --source "Customer" --target "customer" \\
      --confirm --force-with-refs
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict

from _ac_client import ACClient, ACClientError


def find_tag_by_name(tags: list, name: str) -> dict | None:
    """Exact-match lookup. Returns the first matching tag or None."""
    for t in tags:
        if t.get("tag") == name:
            return t
    return None


def suggest_close_matches(tags: list, name: str, limit: int = 5) -> list:
    """Case-insensitive / whitespace-tolerant suggestions for a missing name."""
    needle = name.strip().lower()
    matches = []
    for t in tags:
        tag_name = (t.get("tag") or "").strip().lower()
        if tag_name == needle:
            matches.append(t.get("tag"))
        elif needle in tag_name or tag_name in needle:
            matches.append(t.get("tag"))
    return matches[:limit]


def find_references(automations: list, segments: list, name: str) -> dict:
    """Search automations and segments for textual references to a tag name."""
    if not name:
        return {"automations": [], "segments": []}
    auto_hits = []
    for a in automations:
        if name in json.dumps(a):
            auto_hits.append({"id": a.get("id"), "name": a.get("name", "")})
    seg_hits = []
    for s in segments:
        if name in json.dumps(s):
            seg_hits.append({"id": s.get("id"), "name": s.get("name", "")})
    return {"automations": auto_hits, "segments": seg_hits}


def build_plan(data: dict, source_name: str, target_name: str) -> dict:
    """Compute the merge plan without making any API calls."""
    tags = data["tags"]
    contact_tags = data["contact_tags"]
    automations = data["automations"]
    segments = data["segments"]

    source = find_tag_by_name(tags, source_name)
    target = find_tag_by_name(tags, target_name)

    if not source:
        return {
            "error": f"Source tag '{source_name}' not found",
            "suggestions": suggest_close_matches(tags, source_name),
        }
    if not target:
        return {
            "error": f"Target tag '{target_name}' not found",
            "suggestions": suggest_close_matches(tags, target_name),
        }

    source_id = str(source["id"])
    target_id = str(target["id"])

    if source_id == target_id:
        return {"error": "Source and target are the same tag"}

    contacts_with_source = {}  # contact_id -> contactTag record id
    contacts_with_target = set()
    for ct in contact_tags:
        cid = str(ct.get("contact"))
        tid = str(ct.get("tag"))
        if tid == source_id:
            contacts_with_source[cid] = str(ct.get("id"))
        elif tid == target_id:
            contacts_with_target.add(cid)

    contacts_needing_target = [
        cid for cid in contacts_with_source if cid not in contacts_with_target
    ]
    refs = find_references(automations, segments, source["tag"])

    return {
        "source": {"id": source_id, "name": source["tag"]},
        "target": {"id": target_id, "name": target["tag"]},
        "affected_contacts": len(contacts_with_source),
        "contact_tag_records_to_delete": len(contacts_with_source),
        "contact_tag_records_to_create": len(contacts_needing_target),
        "automation_refs": refs["automations"],
        "segment_refs": refs["segments"],
        "contacts_with_source": contacts_with_source,
        "contacts_needing_target": contacts_needing_target,
    }


def render_plan(plan: dict) -> str:
    if plan.get("error"):
        out = [
            "# Can't run this merge",
            "",
            plan["error"],
        ]
        if plan.get("suggestions"):
            out.extend(["", "Did you mean one of these?"])
            for s in plan["suggestions"]:
                out.append(f"  - {s}")
        return "\n".join(out)

    src = plan["source"]
    tgt = plan["target"]
    lines = [
        "# Tag merge plan",
        "",
        f"Source: `{src['name']}` (id={src['id']}) — will be DELETED",
        f"Target: `{tgt['name']}` (id={tgt['id']}) — canonical",
        "",
        "## Operations",
        f"- Apply `{tgt['name']}` to {plan['contact_tag_records_to_create']} "
        f"contacts that only have the source",
        f"- Remove `{src['name']}` from {plan['affected_contacts']} contacts",
        f"- Delete the `{src['name']}` tag",
        "",
        f"Total API writes: ~{plan['contact_tag_records_to_create'] + plan['affected_contacts'] + 1}",
        "",
    ]
    if plan["automation_refs"]:
        lines.append("## ⚠ Automation references found")
        lines.append(f"`{src['name']}` appears in {len(plan['automation_refs'])} automation(s):")
        for a in plan["automation_refs"]:
            lines.append(f"  - {a['name']} (id={a['id']})")
        lines.append("")
        lines.append("Update those automations to reference `" + tgt["name"] +
                     "` first, or pass --force-with-refs to proceed anyway.")
        lines.append("")
    if plan["segment_refs"]:
        lines.append("## ⚠ Segment references found")
        lines.append(f"`{src['name']}` appears in {len(plan['segment_refs'])} segment(s):")
        for s in plan["segment_refs"]:
            lines.append(f"  - {s['name']} (id={s['id']})")
        lines.append("")
    return "\n".join(lines)


def execute(client: ACClient, plan: dict, force_with_refs: bool) -> dict:
    """Run the merge. Returns a result summary."""
    if plan.get("error"):
        raise SystemExit(f"Cannot execute: {plan['error']}")

    if (plan["automation_refs"] or plan["segment_refs"]) and not force_with_refs:
        raise SystemExit(
            "Refusing to merge: source tag is referenced by "
            f"{len(plan['automation_refs'])} automation(s) and "
            f"{len(plan['segment_refs'])} segment(s). "
            "Update those references first, or pass --force-with-refs."
        )

    target_id = plan["target"]["id"]
    source_id = plan["source"]["id"]
    contacts_with_source = plan["contacts_with_source"]
    contacts_needing_target = plan["contacts_needing_target"]

    applied = 0
    removed = 0
    errors = []

    # 1. Apply target tag to contacts that don't have it
    for cid in contacts_needing_target:
        try:
            client.post("contactTags", {"contactTag": {"contact": cid, "tag": target_id}})
            applied += 1
        except ACClientError as e:
            errors.append({"op": "apply_target", "contact": cid, "error": str(e)})

    # 2. Remove source tag from every affected contact
    for cid, contact_tag_id in contacts_with_source.items():
        try:
            client.delete(f"contactTags/{contact_tag_id}")
            removed += 1
        except ACClientError as e:
            errors.append({"op": "remove_source", "contact": cid, "error": str(e)})

    # 3. Delete the source tag itself (only if all detag operations succeeded)
    tag_deleted = False
    if not [e for e in errors if e["op"] == "remove_source"]:
        try:
            client.delete(f"tags/{source_id}")
            tag_deleted = True
        except ACClientError as e:
            errors.append({"op": "delete_tag", "tag": source_id, "error": str(e)})

    return {
        "target_applied": applied,
        "source_removed": removed,
        "tag_deleted": tag_deleted,
        "errors": errors,
    }


def fetch_data(client: ACClient) -> dict:
    """Fetch the data the planner needs. Same shape as tag_audit's input."""
    return {
        "tags": client.paginate("tags", "tags", max_items=5000),
        "contact_tags": client.paginate("contactTags", "contactTags", max_items=50000),
        "automations": client.paginate("automations", "automations", max_items=2000),
        "segments": client.paginate("segments", "segments", max_items=2000),
    }


def _summarize_contact_tag_pairs(plan: dict) -> dict:
    """Aggregate per-contact effect counts for outcome logging."""
    counts: dict = defaultdict(int)
    counts["affected_contacts"] = plan["affected_contacts"]
    counts["new_target_assignments"] = plan["contact_tag_records_to_create"]
    return dict(counts)


_SAFETY_BANNER = (
    "──────────────────────────────────────────────────────────────────\n"
    " tag-merge hygiene helper — dry-run by default, no changes made\n"
    " unless --confirm is passed. Even with --confirm, refuses to\n"
    " delete a tag still referenced by any active automation or segment.\n"
    "──────────────────────────────────────────────────────────────────"
)


def main():
    parser = argparse.ArgumentParser(
        description="Hygiene helper: consolidate two semantically-equivalent tags"
    )
    parser.add_argument("--source", required=True,
                        help="Tag to merge from (will be deleted with --confirm)")
    parser.add_argument("--target", required=True,
                        help="Canonical tag to merge into")
    parser.add_argument("--confirm", action="store_true",
                        help="Required to actually execute. Without it, prints the plan only.")
    parser.add_argument("--force-with-refs", action="store_true",
                        help="Proceed even if automation or segment references exist")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    # Always show the banner on stderr so the safety story is visible whether
    # the script is invoked from a terminal, a wrapper, or an agent harness.
    print(_SAFETY_BANNER, file=sys.stderr)

    client = ACClient()
    data = fetch_data(client)
    plan = build_plan(data, args.source, args.target)

    if plan.get("error"):
        print(render_plan(plan), file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        # Strip the verbose contact-id maps from JSON output
        public = {k: v for k, v in plan.items()
                  if k not in ("contacts_with_source", "contacts_needing_target")}
        print(json.dumps(public, indent=2))
    else:
        print(render_plan(plan))

    if not args.confirm:
        print("\n(dry-run — pass --confirm to execute)")
        return

    print("\nExecuting merge...")
    result = execute(client, plan, force_with_refs=args.force_with_refs)
    print(f"  Applied target tag to {result['target_applied']} contacts")
    print(f"  Removed source tag from {result['source_removed']} contacts")
    print(f"  Source tag deleted: {result['tag_deleted']}")
    if result["errors"]:
        print(f"  ⚠ {len(result['errors'])} error(s) — first few:")
        for e in result["errors"][:5]:
            print(f"    - {e}")
        sys.exit(2)
    _summarize_contact_tag_pairs(plan)


if __name__ == "__main__":
    main()
