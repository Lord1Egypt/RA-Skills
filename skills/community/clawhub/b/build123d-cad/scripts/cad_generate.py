#!/usr/bin/env python3
"""Execute a build123d script and export STEP/STL/SVG. All in subprocess."""

import argparse
from helpers import run_sandboxed, output_json, WORKSPACE


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--format", choices=["step", "stl", "svg"], default="step")
    p.add_argument("--filename", default="model")
    args = p.parse_args()

    out_path = str(WORKSPACE / f"{args.filename}.{args.format}")

    sandbox_script = f'''
import json, os, traceback

# --- user script ---
{args.script}
# --- end user script ---

_rp = os.environ["_RESULT_PATH"]
_ws = os.environ["_WORKSPACE"]
_out = {repr(out_path)}
_fmt = {repr(args.format)}

try:
    _part = result.part if hasattr(result, "part") else result
    os.makedirs(os.path.dirname(_out), exist_ok=True)

    from build123d import export_step, export_stl, export_svg
    if _fmt == "step": export_step(_part, _out)
    elif _fmt == "stl": export_stl(_part, _out)
    elif _fmt == "svg": export_svg(_part, _out)

    _bb = _part.bounding_box()
    with open(_rp, "w") as f:
        json.dump({{
            "success": True,
            "artifact_path": _out,
            "format": _fmt,
            "file_size_bytes": os.path.getsize(_out),
            "bounding_box_mm": {{"x": round(_bb.size.X, 2), "y": round(_bb.size.Y, 2), "z": round(_bb.size.Z, 2)}},
        }}, f)
except Exception:
    with open(_rp, "w") as f:
        json.dump({{"success": False, "error": traceback.format_exc()[-2000:]}}, f)
'''

    output_json(run_sandboxed(sandbox_script))


if __name__ == "__main__":
    main()
