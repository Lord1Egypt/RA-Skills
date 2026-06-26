#!/usr/bin/env python3
"""
tag_audit.py — Surface tag hygiene problems.

Finds: tags used <N times (likely typos), tags applied to >X% of contacts
(likely useless), tags with no automation/segment dependency (dead),
tags that always co-occur with another (consolidation candidates).

Usage:
  python3 tag_audit.py
  python3 tag_audit.py --rare-threshold 5 --common-threshold 0.5
  python3 tag_audit.py --format json --output tag_audit.json
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict

from _ac_client import ACClient, cli_main


def fetch_data(client: ACClient, max_contact_tags: int = 50000,
               progress=None) -> dict:
    """Pull taxonomy + stream-aggregate the contact-tag link table.

    Streaming the contact-tag pairs (rather than materializing the full list)
    keeps memory bounded to the pre-aggregated structures, which are typically
    1–2 orders of magnitude smaller than the raw record stream on big accounts.
    """
    if progress is None:
        def progress(_msg):
            return None
    progress("Pulling tag definitions...")
    tags = client.paginate("tags", "tags", max_items=5000)

    progress(f"Streaming contact-tag pairs (cap {max_contact_tags:,})...")
    tag_count: Counter = Counter()
    contact_tag_pairs: dict[str, set[str]] = defaultdict(set)
    seen = 0
    for x in client.stream("contactTags", "contactTags", max_items=max_contact_tags):
        tag_id = str(x.get("tag"))
        contact_id = str(x.get("contact"))
        if tag_id and contact_id:
            tag_count[tag_id] += 1
            contact_tag_pairs[contact_id].add(tag_id)
        seen += 1
        if seen % 5000 == 0:
            progress(f"  ...{seen:,} pairs processed")

    progress("Pulling automations + segments for dead-tag check...")
    automations = client.paginate("automations", "automations", max_items=2000)
    segments = client.paginate("segments", "segments", max_items=2000)
    return {
        "tags": tags,
        "tag_count": tag_count,
        "contact_tag_pairs": contact_tag_pairs,
        "automations": automations,
        "segments": segments,
    }


def _scan_text_for_tag_refs(text: str, tag_id: str, tag_name: str) -> bool:
    if not text:
        return False
    return tag_name and tag_name in text


def analyze(data: dict, rare_threshold: int, common_threshold: float) -> dict:
    tags = data["tags"]
    tag_by_id = {t["id"]: t for t in tags}

    # Accept either the new pre-aggregated shape (from streaming fetch_data)
    # or the legacy raw `contact_tags` list (kept for backward compat with
    # existing test fixtures and any external callers).
    if "tag_count" in data and "contact_tag_pairs" in data:
        tag_count = data["tag_count"]
        contact_tag_pairs = data["contact_tag_pairs"]
    else:
        tag_count = Counter()
        contact_tag_pairs = defaultdict(set)
        for x in data.get("contact_tags", []):
            tag_id = str(x.get("tag"))
            contact_id = str(x.get("contact"))
            if tag_id and contact_id:
                tag_count[tag_id] += 1
                contact_tag_pairs[contact_id].add(tag_id)

    total_contacts_tagged = len(contact_tag_pairs)

    rare = []
    common = []
    for t in tags:
        tid = t["id"]
        n = tag_count.get(tid, 0)
        if n < rare_threshold:
            rare.append({"id": tid, "name": t["tag"], "count": n})
        if total_contacts_tagged and (n / total_contacts_tagged) >= common_threshold:
            common.append({
                "id": tid, "name": t["tag"], "count": n,
                "pct": n / total_contacts_tagged * 100,
            })

    # find co-occurrence: pairs of tags that always appear together
    cooc = Counter()
    for tag_set in contact_tag_pairs.values():
        ids = sorted(tag_set)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                cooc[(ids[i], ids[j])] += 1

    consolidation = []
    for (a, b), c in cooc.items():
        ca, cb = tag_count.get(a, 0), tag_count.get(b, 0)
        if ca == 0 or cb == 0:
            continue
        # if both tags appear together >= 95% of the time
        if c >= 5 and c / max(ca, cb) >= 0.95:
            consolidation.append({
                "a": tag_by_id[a]["tag"], "b": tag_by_id[b]["tag"],
                "co_count": c, "a_count": ca, "b_count": cb,
            })

    # dead tags: not referenced in any automation or segment
    auto_blob = json.dumps(data["automations"])
    seg_blob = json.dumps(data["segments"])
    dead = []
    for t in tags:
        name = t["tag"]
        if not name:
            continue
        if name not in auto_blob and name not in seg_blob:
            dead.append({"id": t["id"], "name": name, "count": tag_count.get(t["id"], 0)})

    return {
        "total_tags": len(tags),
        "total_tagged_contacts": total_contacts_tagged,
        "rare": sorted(rare, key=lambda x: x["count"]),
        "common": sorted(common, key=lambda x: -x["pct"]),
        "consolidation": sorted(consolidation, key=lambda x: -x["co_count"])[:20],
        "dead": dead,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Tag Audit",
        "",
        f"- Total tags: **{r['total_tags']}**",
        f"- Tagged contacts: **{r['total_tagged_contacts']}**",
        f"- Rare tags (likely typos or one-off): **{len(r['rare'])}**",
        f"- Common tags (>=threshold of all tagged contacts): **{len(r['common'])}**",
        f"- Consolidation candidates (always co-occur): **{len(r['consolidation'])}**",
        f"- Dead tags (no automation/segment reference): **{len(r['dead'])}**",
        "",
    ]
    if r["rare"]:
        lines.append("## Rare tags (consider deleting)")
        for t in r["rare"][:30]:
            lines.append(f"- `{t['name']}` (id={t['id']}) — {t['count']}")
        lines.append("")
    if r["common"]:
        lines.append("## Over-applied tags (do they still discriminate?)")
        for t in r["common"][:20]:
            lines.append(f"- `{t['name']}` — {t['count']} contacts ({t['pct']:.1f}%)")
        lines.append("")
    if r["consolidation"]:
        lines.append("## Consolidation candidates (95%+ co-occurrence)")
        for c in r["consolidation"]:
            lines.append(f"- `{c['a']}` + `{c['b']}` — co-occur {c['co_count']}× (a={c['a_count']}, b={c['b_count']})")
        lines.append("")
    if r["dead"]:
        lines.append("## Dead tags (no automation/segment uses them)")
        for t in r["dead"][:50]:
            lines.append(f"- `{t['name']}` — {t['count']} uses")
        lines.append("")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--rare-threshold", type=int, default=5)
    parser.add_argument("--common-threshold", type=float, default=0.5)
    parser.add_argument("--max-items", type=int, default=50000)


def _fetch(client, args):
    return fetch_data(client, max_contact_tags=args.max_items, progress=args.progress)


def _analyze(data, args):
    return analyze(data, args.rare_threshold, args.common_threshold)


def main():
    cli_main(
        description="Audit tag hygiene",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
