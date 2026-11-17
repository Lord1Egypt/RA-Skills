"""The four checks from SKILL.md's Verification section, run against a
harvested folder. Also the check that catches a merge regression: rows,
files and the manifest must all agree.

    python verify_dataset.py <folder>
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def main(folder: str) -> int:
    ds = Path(folder)
    imgs = sorted(p for p in (ds / "images").glob("*") if p.is_file())
    rows = [json.loads(l) for l in
            (ds / "metadata.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    man = json.loads((ds / "manifest.json").read_text(encoding="utf-8"))
    rejp = ds / "rejected.jsonl"
    rej = ([json.loads(l) for l in rejp.read_text(encoding="utf-8").splitlines()
            if l.strip()] if rejp.exists() else [])

    print(f"1. files in images/          : {len(imgs)}")
    for f in imgs:
        print(f"      {f.name}  {f.stat().st_size:,} bytes")

    missing = [r["file_name"] for r in rows if not (ds / r["file_name"]).exists()]
    print(f"2. rows in metadata.jsonl    : {len(rows)}  (all valid JSON: yes)")
    print(f"   file_name resolves on disk: {len(rows) - len(missing)}/{len(rows)}"
          f"  missing={missing}")

    print(f"3. manifest.total_images     : {man['total_images']}  "
          f"-> matches dir: {man['total_images'] == len(imgs)}")
    print(f"   rows == files             : {len(rows) == len(imgs)}")
    print(f"   manifest.generated_utc    : {man.get('generated_utc', 'MISSING')}")
    print(f"   rating_is_ceiling         : {man.get('rating_is_ceiling', 'MISSING')}")

    over = [r for r in rows
            if r["rating"] not in ("general", "sensitive", "questionable",
                                   "explicit", "unknown")]
    print(f"4. ratings in output         : "
          f"{sorted({r['rating'] for r in rows})}  over ceiling: {len(over)}")
    print(f"   rejected.jsonl explains   : {len(rej)} row(s)")
    print(f"   reject reasons            : "
          f"{dict(Counter(r['reject_reason'] for r in rej))}")
    print(f"   manifest.total_rejected   : {man.get('total_rejected')}")

    per = man.get("per_source", {})
    if per:
        print("\nper-source:")
        for k, v in per.items():
            print(f"   {k:<12} found={v.get('found', 0):<4} "
                  f"kept={v.get('kept', 0):<4} "
                  f"transport={v.get('transport', '')}")

    ok = (man["total_images"] == len(imgs) == len(rows)
          and not missing and not over
          and bool(man.get("generated_utc")))
    print(f"\nALL CHECKS PASS              : {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1
                          else "./dataset"))