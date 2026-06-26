#!/usr/bin/env python3
"""compare_snapshots.py — Diff two Moltbook snapshots to track rank movement.

Usage:
    python3 compare_snapshots.py <older.json> <newer.json> [--top N]

Args:
    older.json  Snapshot A (the earlier/baseline snapshot)
    newer.json  Snapshot B (the newer snapshot to compare against A)
    --top N     Number of top posts to compare (default: 25)

Output: Markdown diff report to stdout.
"""

import json
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path


def load_snapshot(path):
    """Load a snapshot JSON file and return (metadata, ranked posts list)."""
    with open(path) as f:
        data = json.load(f)
    posts = data.get("posts", [])
    # Assign ranks based on order in the file (1-indexed)
    for i, p in enumerate(posts):
        p["_rank"] = i + 1
        p["_score"] = p.get("upvotes", 0) - p.get("downvotes", 0)
        p["_author"] = p.get("author", {}).get("name", "[deleted]")
    return data, posts


def truncate(text, maxlen=70):
    """Truncate text with ellipsis."""
    if len(text) <= maxlen:
        return text
    return text[:maxlen-3] + "..."


def main():
    # Parse args
    args = sys.argv[1:]
    top_n = 25
    paths = []

    i = 0
    while i < len(args):
        if args[i] == "--top" and i + 1 < len(args):
            try:
                top_n = int(args[i + 1])
                if top_n < 1:
                    raise ValueError
            except ValueError:
                print(f"ERROR: --top requires a positive integer, got '{args[i + 1]}'", file=sys.stderr)
                sys.exit(1)
            i += 2
        else:
            paths.append(args[i])
            i += 1

    if len(paths) != 2:
        print("Usage: python3 compare_snapshots.py <older.json> <newer.json> [--top N]", file=sys.stderr)
        sys.exit(1)

    now_utc = datetime.now(timezone.utc)

    data_a, posts_a = load_snapshot(paths[0])
    data_b, posts_b = load_snapshot(paths[1])

    name_a = Path(paths[0]).name
    name_b = Path(paths[1]).name

    req_a = data_a.get("request", {})
    req_b = data_b.get("request", {})

    # Build lookup maps: id -> post
    map_a = OrderedDict((p["id"], p) for p in posts_a[:top_n] if p.get("id"))
    map_b = OrderedDict((p["id"], p) for p in posts_b[:top_n] if p.get("id"))

    ids_a = set(map_a.keys())
    ids_b = set(map_b.keys())

    shared = ids_a & ids_b
    only_a = ids_a - ids_b
    only_b = ids_b - ids_a

    # Rank changes for shared posts
    rank_changes = []
    for pid in shared:
        pa = map_a[pid]
        pb = map_b[pid]
        rank_delta = pa["_rank"] - pb["_rank"]  # positive = rose in B
        score_delta = pb["_score"] - pa["_score"]
        rank_changes.append({
            "id": pid,
            "title": pb.get("title", "(untitled)"),
            "author": pb["_author"],
            "rank_a": pa["_rank"],
            "rank_b": pb["_rank"],
            "rank_delta": rank_delta,
            "score_a": pa["_score"],
            "score_b": pb["_score"],
            "score_delta": score_delta,
        })

    rose = sorted([r for r in rank_changes if r["rank_delta"] > 0], key=lambda x: x["rank_delta"], reverse=True)
    fell = sorted([r for r in rank_changes if r["rank_delta"] < 0], key=lambda x: x["rank_delta"])
    stable = [r for r in rank_changes if r["rank_delta"] == 0]

    # Author analysis
    authors_a = set(p["_author"] for p in posts_a[:top_n])
    authors_b = set(p["_author"] for p in posts_b[:top_n])
    authors_shared = authors_a & authors_b
    authors_new = authors_b - authors_a
    authors_left = authors_a - authors_b

    # Score level shift
    scores_a = [p["_score"] for p in posts_a[:top_n]]
    scores_b = [p["_score"] for p in posts_b[:top_n]]
    avg_a = sum(scores_a) / len(scores_a) if scores_a else 0
    avg_b = sum(scores_b) / len(scores_b) if scores_b else 0

    # ---- Build report ----
    lines = []
    lines.append(f"# Moltbook Snapshot Comparison")
    lines.append(f"")
    lines.append(f"Generated: {now_utc.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"Comparing top {top_n} posts from each snapshot.")
    lines.append(f"")
    lines.append(f"| | Snapshot A (older) | Snapshot B (newer) |")
    lines.append(f"|---|---|---|")
    lines.append(f"| **File** | {name_a} | {name_b} |")
    lines.append(f"| **Submolt** | {req_a.get('submolt','-')} | {req_b.get('submolt','-')} |")
    lines.append(f"| **Timeframe** | {req_a.get('timeframe','-')} | {req_b.get('timeframe','-')} |")
    lines.append(f"| **Posts** | {len(posts_a)} | {len(posts_b)} |")
    lines.append(f"| **Avg Score (top {top_n})** | {avg_a:.1f} | {avg_b:.1f} |")
    lines.append(f"| **Created** | {data_a.get('createdAt','-')} | {data_b.get('createdAt','-')} |")
    lines.append(f"")

    # ---- Score level shift ----
    shift = avg_b - avg_a
    pct = (shift / avg_a * 100) if avg_a else 0
    direction = "UP" if shift > 0 else "DOWN" if shift < 0 else "FLAT"
    lines.append(f"## Score Level Shift")
    lines.append(f"")
    lines.append(f"Average score moved from **{avg_a:.1f}** to **{avg_b:.1f}** ({direction} {abs(shift):.1f}, {abs(pct):.1f}%)")
    lines.append(f"")

    # ---- Rose in rank ----
    lines.append(f"## Rose in Rank ({len(rose)} posts)")
    lines.append(f"")
    if rose:
        lines.append(f"| Title | Author | Rank A | Rank B | Change | Score Delta |")
        lines.append(f"|---|---|---|---|---|---|")
        for r in rose:
            lines.append(f"| {truncate(r['title'])} | {r['author']} | {r['rank_a']} | {r['rank_b']} | +{r['rank_delta']} | +{r['score_delta']} |")
    else:
        lines.append("None.")
    lines.append(f"")

    # ---- Fell in rank ----
    lines.append(f"## Fell in Rank ({len(fell)} posts)")
    lines.append(f"")
    if fell:
        lines.append(f"| Title | Author | Rank A | Rank B | Change | Score Delta |")
        lines.append(f"|---|---|---|---|---|---|")
        for r in fell:
            lines.append(f"| {truncate(r['title'])} | {r['author']} | {r['rank_a']} | {r['rank_b']} | {r['rank_delta']} | {r['score_delta']:+d} |")
    else:
        lines.append("None.")
    lines.append(f"")

    # ---- Stable ----
    lines.append(f"## Stable ({len(stable)} posts — same rank)")
    lines.append(f"")
    if stable:
        lines.append(f"| Title | Author | Rank | Score Delta |")
        lines.append(f"|---|---|---|---|")
        for r in stable:
            lines.append(f"| {truncate(r['title'])} | {r['author']} | {r['rank_a']} | {r['score_delta']:+d} |")
    else:
        lines.append("None.")
    lines.append(f"")

    # ---- New entrants ----
    lines.append(f"## New Entrants ({len(only_b)} posts — in B but not A)")
    lines.append(f"")
    if only_b:
        lines.append(f"| # | Title | Author | Rank in B | Score |")
        lines.append(f"|---|---|---|---|---|")
        new_posts = sorted([map_b[pid] for pid in only_b], key=lambda x: x["_rank"])
        for i, p in enumerate(new_posts, 1):
            lines.append(f"| {i} | {truncate(p.get('title',''))} | {p['_author']} | {p['_rank']} | {p['_score']} |")
    else:
        lines.append("None.")
    lines.append(f"")

    # ---- Dropped out ----
    lines.append(f"## Dropped Out ({len(only_a)} posts — in A but not B)")
    lines.append(f"")
    if only_a:
        lines.append(f"| # | Title | Author | Was Rank | Score in A |")
        lines.append(f"|---|---|---|---|---|")
        dropped = sorted([map_a[pid] for pid in only_a], key=lambda x: x["_rank"])
        for i, p in enumerate(dropped, 1):
            lines.append(f"| {i} | {truncate(p.get('title',''))} | {p['_author']} | {p['_rank']} | {p['_score']} |")
    else:
        lines.append("None.")
    lines.append(f"")

    # ---- Author consistency ----
    lines.append(f"## Author Consistency")
    lines.append(f"")
    lines.append(f"| Metric | Count | Names |")
    lines.append(f"|---|---|---|")
    lines.append(f"| **In both** | {len(authors_shared)} | {', '.join(sorted(authors_shared)[:10])}{'...' if len(authors_shared) > 10 else ''} |")
    lines.append(f"| **New in B** | {len(authors_new)} | {', '.join(sorted(authors_new)[:10])}{'...' if len(authors_new) > 10 else ''} |")
    lines.append(f"| **Left (in A only)** | {len(authors_left)} | {', '.join(sorted(authors_left)[:10])}{'...' if len(authors_left) > 10 else ''} |")
    lines.append(f"")

    # ---- Summary ----
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"- **Overlap:** {len(shared)}/{top_n} posts appear in both snapshots ({len(shared)/top_n*100:.0f}% stability)")
    lines.append(f"- **Turnover:** {len(only_b)} new entrants, {len(only_a)} dropped out")
    lines.append(f"- **Score shift:** {direction} {abs(shift):.1f} ({abs(pct):.1f}%)")
    lines.append(f"- **Author churn:** {len(authors_new)} new authors, {len(authors_left)} departed")
    lines.append(f"")

    report = "\n".join(lines)

    # Print to stdout
    print(report)

    # Save to reports directory
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    reports_dir = skill_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = now_utc.strftime("%Y-%m-%d_%H%M%S")
    report_file = reports_dir / f"{timestamp}_comparison.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nComparison saved to: {report_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
