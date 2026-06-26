#!/usr/bin/env python3
"""
Find draw.io NATIVE shapes (vector stencils built into diagrams.net) for a
service name. Use this to preview which native shape a node will map to when
building a diagram with `drawio_shapes` enabled.

These shapes render only in .drawio (not Excalidraw). AWS shapes come out as the
official colored resourceIcon square; GCP shapes are self-colored; Azure shapes
are monochrome.

Usage:
    python find_drawio_shape.py "Lambda" --provider aws -n 5
    python find_drawio_shape.py "BigQuery" --provider gcp
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from find_icon import score as icon_score

INDEX = Path(__file__).resolve().parent.parent / "references" / "drawio-shape-index.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--provider", help="aws | gcp | azure (comma list)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not INDEX.exists():
        sys.exit("Shape index missing. Run build_drawio_shape_index.py first.")
    shapes = json.loads(INDEX.read_text("utf-8"))
    if args.provider:
        allow = {p.strip() for p in args.provider.split(",")}
        shapes = [s for s in shapes if s["shape_provider"] in allow]

    ranked = sorted(shapes, key=lambda s: icon_score(args.query, s), reverse=True)[:args.n]
    out = [dict(s, score=round(icon_score(args.query, s), 3)) for s in ranked]

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for r in out:
            print(f"{r['score']:>5}  [{r['shape_provider']:<5}] "
                  f"{r['name']:<34} {r['key']}  {r.get('color','')}")


if __name__ == "__main__":
    main()
