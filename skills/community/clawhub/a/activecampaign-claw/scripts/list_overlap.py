#!/usr/bin/env python3
"""
list_overlap.py — How many contacts are on each pair of lists.

Pre-merge sanity check. Surfaces lists that 100% overlap (one is a subset)
and lists with significant cross-membership.

Usage:
  python3 list_overlap.py
  python3 list_overlap.py --min-overlap 10 --format json
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from _ac_client import ACClient, cli_main


def fetch(client: ACClient, max_items: int = 50000) -> dict:
    lists = client.paginate("lists", "lists", max_items=2000)
    contact_lists = client.paginate("contactLists", "contactLists", max_items=max_items)
    return {"lists": lists, "contact_lists": contact_lists}


def analyze(data: dict, min_overlap: int) -> dict:
    list_name = {str(lst["id"]): lst.get("name", "") for lst in data["lists"]}
    members = defaultdict(set)  # list_id -> set of contact ids (active only)
    for cl in data["contact_lists"]:
        if str(cl.get("status")) == "1":
            members[str(cl.get("list"))].add(str(cl.get("contact")))

    results = []
    for a, b in combinations(sorted(members.keys()), 2):
        sa, sb = members[a], members[b]
        inter = sa & sb
        if len(inter) < min_overlap:
            continue
        results.append({
            "list_a": list_name.get(a, a),
            "list_b": list_name.get(b, b),
            "a_count": len(sa),
            "b_count": len(sb),
            "overlap": len(inter),
            "a_pct_in_b": (len(inter) / len(sa) * 100) if sa else 0,
            "b_pct_in_a": (len(inter) / len(sb) * 100) if sb else 0,
        })
    results.sort(key=lambda x: -x["overlap"])

    subsets = [r for r in results if r["a_pct_in_b"] >= 95 or r["b_pct_in_a"] >= 95]
    return {
        "lists_compared": len(members),
        "overlap_pairs": results,
        "subset_pairs": subsets,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# List Overlap",
        "",
        f"- Lists compared (active members only): {r['lists_compared']}",
        f"- Pairs with overlap above threshold: {len(r['overlap_pairs'])}",
        f"- Subset pairs (one is ≥95% of the other): **{len(r['subset_pairs'])}**",
        "",
    ]
    if r["subset_pairs"]:
        lines.append("## Subset pairs (likely duplicate-ish)")
        for p in r["subset_pairs"]:
            lines.append(
                f"- `{p['list_a']}` ({p['a_count']}) ⇄ `{p['list_b']}` ({p['b_count']}): "
                f"overlap {p['overlap']} — A in B: {p['a_pct_in_b']:.1f}%, B in A: {p['b_pct_in_a']:.1f}%"
            )
        lines.append("")
    if r["overlap_pairs"]:
        lines.append("## All overlapping pairs")
        lines.append("| List A | List B | Overlap | A in B % | B in A % |")
        lines.append("|---|---|---|---|---|")
        for p in r["overlap_pairs"][:50]:
            lines.append(
                f"| {p['list_a']} | {p['list_b']} | {p['overlap']} | "
                f"{p['a_pct_in_b']:.1f}% | {p['b_pct_in_a']:.1f}% |"
            )
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--min-overlap", type=int, default=1)
    parser.add_argument("--max-items", type=int, default=50000)


def _fetch(client, args):
    return fetch(client, max_items=args.max_items)


def _analyze(data, args):
    return analyze(data, args.min_overlap)


def main():
    cli_main(
        description="Compute list overlap",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
