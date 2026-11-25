#!/usr/bin/env python3
"""bench.py — build a comparison table from geo-scan JSON outputs.

    python3 bench.py out/*.json > out/benchmark.md

Input paths must resolve inside the working directory (symlinks resolved), the
same boundary the scanner's writes keep — registry finding SDI-3, 2026-11-23.
"""
import glob
import json
import sys
import time
from pathlib import Path

ORDER = ["robots", "machine", "snippet", "structure", "quotable", "fresh"]


def contained(p):
    """Resolve a report path and require it to sit inside the working directory."""
    root = Path.cwd().resolve()
    rp = Path(p).resolve()
    if rp != root and root not in rp.parents:
        raise ValueError(f"{p}: outside the working directory {root}")
    return rp


def main(paths):
    rows = []
    for p in paths:
        try:
            d = json.load(open(contained(p), encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"skip {p}: {e}", file=sys.stderr)
            continue
        axes = {c["id"]: c for c in d.get("checks", [])}
        sig = d.get("signals", {})
        sm = d.get("sitemap", {}) or {}
        rows.append({
            "site": d.get("root", p),
            "score": d.get("score", 0),
            "grade": d.get("grade", "?"),
            "axes": "/".join(f"{axes.get(a, {}).get('score', 0):g}" for a in ORDER),
            "pages": len(d.get("pages", [])),
            "urls": sm.get("pages") and len(sm["pages"]) or sm.get("urls", 0),
            "llms": "yes" if sig.get("llms_txt") else "no",
            "lastmod": f"{sm.get('with_lastmod', len(sm.get('lastmods', [])))}/{sm.get('urls', 0)}",
        })
    rows.sort(key=lambda r: -r["score"])
    print(f"# geo-scan benchmark — {time.strftime('%Y-%m-%d')}\n")
    print("| site | score | grade | crawlers/machine/snippet/structure/quotable/fresh | pages sampled | sitemap URLs | llms.txt | lastmod coverage |")
    print("|---|---:|---|---|---:|---:|---|---|")
    for r in rows:
        print(f"| {r['site']} | {r['score']} | {r['grade']} | {r['axes']} | {r['pages']} | "
              f"{r['urls']} | {r['llms']} | {r['lastmod']} |")
    print()
    print("Numbers produced live by `geo_scan.py` on the date above; each report sits next to this file.")


if __name__ == "__main__":
    args = sys.argv[1:] or sorted(glob.glob("out/*.json"))
    main(args)
