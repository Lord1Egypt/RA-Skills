#!/usr/bin/env python3
"""Execute a build123d script and return measurements. All in subprocess."""

import argparse
from helpers import run_sandboxed, output_json


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    args = p.parse_args()

    sandbox_script = f'''
import json, os, traceback

# --- user script ---
{args.script}
# --- end user script ---

_rp = os.environ["_RESULT_PATH"]

try:
    _part = result.part if hasattr(result, "part") else result
    _bb = _part.bounding_box()
    _com = _part.center()
    with open(_rp, "w") as f:
        json.dump({{
            "success": True,
            "bounding_box_mm": {{"x": round(_bb.size.X, 2), "y": round(_bb.size.Y, 2), "z": round(_bb.size.Z, 2)}},
            "volume_mm3": round(_part.volume, 2),
            "surface_area_mm2": round(_part.area, 2),
            "center_of_mass_mm": {{"x": round(_com.X, 2), "y": round(_com.Y, 2), "z": round(_com.Z, 2)}},
            "face_count": len(_part.faces()),
            "edge_count": len(_part.edges()),
        }}, f)
except Exception:
    with open(_rp, "w") as f:
        json.dump({{"success": False, "error": traceback.format_exc()[-2000:]}}, f)
'''

    output_json(run_sandboxed(sandbox_script))


if __name__ == "__main__":
    main()
