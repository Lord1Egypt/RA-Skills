#!/usr/bin/env python3
"""Generate a 2D cross-section SVG. All in subprocess."""

import argparse
from helpers import run_sandboxed, output_json, WORKSPACE


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--plane", choices=["XY", "XZ", "YZ"], default="XY")
    p.add_argument("--offset", type=float, default=0.0)
    p.add_argument("--filename", default=None)
    args = p.parse_args()

    fname = args.filename or f"section_{args.plane}_{args.offset}"
    out_path = str(WORKSPACE / f"{fname}.svg")

    sandbox_script = f'''
import json, os, traceback

# --- user script ---
{args.script}
# --- end user script ---

_rp = os.environ["_RESULT_PATH"]
_out = {repr(out_path)}

try:
    from build123d import Plane, export_svg

    _part = result.part if hasattr(result, "part") else result
    _planes = {{"XY": Plane.XY, "XZ": Plane.XZ, "YZ": Plane.YZ}}
    _section = _part.section(plane=_planes[{repr(args.plane)}].offset({args.offset}))

    os.makedirs(os.path.dirname(_out), exist_ok=True)
    export_svg(_section, _out)

    with open(_rp, "w") as f:
        json.dump({{
            "success": True,
            "artifact_path": _out,
            "plane": {repr(args.plane)},
            "offset_mm": {args.offset},
            "section_edge_count": len(_section.edges()) if hasattr(_section, "edges") else 0,
        }}, f)
except Exception:
    with open(_rp, "w") as f:
        json.dump({{"success": False, "error": traceback.format_exc()[-2000:]}}, f)
'''

    output_json(run_sandboxed(sandbox_script))


if __name__ == "__main__":
    main()
